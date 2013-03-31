#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
SOSAT - Prove satisfiability for boolean formulas in CNF

Algorithms:
    ant colony optimization,
    genetic algorithm,
    simulated annealing (as a means to generate an initial population)

Authors:
    Dominik Moritz (dominik.moritz@student.hpi.uni-potsdam.de),
    Matthias Springer (matthias.springer@student.hpi.uni-potsdam.de)
"""

from __future__ import print_function

import argparse
import sys
import multiprocessing
from multiprocessing import Process, Queue
import numpy as np
import random

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser
import sosat.preprocessing as preprocessing

VERBOSE = False

def dprint(*args, **kwargs):
    if VERBOSE:
        __builtins__.print(*(['c'] + list(args)), **kwargs)

class MyProcess(Process):
    """
    Container class for running multiple instances of an algorithm simultaneously.
    """

    def run(self):
        Process.run(self)


def print_solution(instance_solution, num_vars):
    """
    Print the solution. To retrieve the correct solution, preprocessing steps have to be undone.
    """
    if instance_solution is False:
        # unsatisfiability can only be determined during preprocessing
        sys.stdout.write("s UNSATISFIABLE\n")
    elif instance_solution is not None:
        instance, p_solution = instance_solution
        solution = preprocessing.restore_original_solution(instance, p_solution, num_vars)

        sol = []
        for i, lit in enumerate(solution):
            sol.append(str(i + 1 if lit else -i - 1))
        sys.stdout.write("v " + ' '.join(sol) + ' 0\n')
        sys.stdout.write("s SATISFIABLE\n")
    else:
        sys.stdout.write("s UNKNOWN\n")


def main():
    # entry point for the program
    np.set_printoptions(linewidth=2000000000)

    clp = argparse.ArgumentParser(description='SAT solver.')
    clp.add_argument('-a', '--algorithm', dest='algo',
                     default='genetic', choices=['genetic', 'ant', 'other'],
                     help='select algorithm for solving')
    clp.add_argument('-v', '--verbose', dest='verbose',
                     default=False, action='store_true',
                     help='print stats and status message')
    clp.add_argument('-s', '--seed', dest='seed', type=int,
                     default=42,
                     help='seed for random number generator')
    clp.add_argument('-N', '--number', dest='N',
                     default=1, type=int,
                     help='number of processes')
    clp.add_argument('-f', '--factor', dest='f',
                     default=0, type=int,
                     help='number of factored (most-constrained) variables')
    clp.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                     default=sys.stdin)

    args = clp.parse_args()
    VERBOSE = args.verbose
   
    def dprint(*args, **kwargs):
        if VERBOSE:
            __builtins__.print(*(['c'] + list(args)), **kwargs)
                     
    # parse input file
    num_vars, clauses = parser.parse(args.infile)
    # preprocess instance and generate factored instances
    factored_instances = preprocessing.factored_instances(num_vars, clauses, min(args.f, num_vars))
    # filter unsatisfiable factored instances (detected during preprocessing)
    factored_instances = filter(lambda i: i is not False, factored_instances)
    # find instances solved completely during preprocessing
    solved_instances = filter(lambda i: len(i[1]) == 0, factored_instances)
    # initialize Python random with seed (not used during computation, only for choosing next configuration)
    random.seed(args.seed)
    
    if len(factored_instances) == 0:
        # if all factored instances are unsatisfiable, then the instance is unsatisfiable
        dprint("Proved unsatisfiable during preprocessing.")
        print_solution(False, 0)
        exit()
    elif len(solved_instances) > 0:
        dprint("Solved during preprocessing.")
        print_solution((solved_instances[0], []), num_vars)
        exit()

    if args.algo == 'genetic':
        dprint("Selected genetic algorithm.")
        algo = ga.GeneticAlgorithm
    elif args.algo == 'ant':
        dprint("Selected ant colony optimization.")
        algo = aa.AntColonyAlgorithm
    else:
        print("Argument error: No such algorithm.")

    dprint("Reduced instances:")

    for i in factored_instances:
        dprint(i, " / ", num_vars, "original variables")

    processes = []
    queue = Queue()
    MAX_ITERATIONS = 25000

    if not args.N:
        args.N = multiprocessing.cpu_count()

    # run profiles
    dprint("Run {} processes (N = {}, {} factored instances)".format(max(args.N, len(factored_instances)) ,args.N, len(factored_instances)))

    # run algorithm for every factored instance with every profile
    for instance in factored_instances:
        profile = algo.profiles[0]
        start_process(algo, instance, profile, args.seed, MAX_ITERATIONS, queue, args.verbose, processes)

    for i in range(args.N - len(factored_instances)):
        profile = random.choice(algo.profiles)
        instance = random.choice(factored_instances)
        start_process(algo, instance, profile, random.randint(1, 10000), MAX_ITERATIONS, queue, VERBOSE, processes)

    # wait for the first process to finish with a solution
    while True:
        solution = queue.get()
        
        for instance in factored_instances:
            MAX_ITERATIONS = int(MAX_ITERATIONS * 1.75)

            if solution[1] is not None:
                print_solution(solution, num_vars)

                for process in processes:
                    process.terminate()

                exit()

            else:
                # start another thread with more iterations and different configuration
                profile = random.choice(algo.profiles)
                start_process(algo, instance, profile, random.randint(1, 10000), MAX_ITERATIONS, queue, VERBOSE, processes)

def algorithm_start(instance, config, queue, algo):
    dprint("Start", config)
    dprint("Start one process with config", config)

    a = algo(instance[0], instance[1], config)

    solution = a.run()
    dprint("Solution", str(solution))
    queue.put((instance, solution))


def start_process(algo, instance, profile, seed, iterations, queue, verbose, processes):
    config = {
        'VERBOSE': verbose,
        'SEED': seed,
        'MAX_ITERATIONS': iterations
    }
    config.update(profile)
    p = MyProcess(target=algorithm_start, args=(instance, config, queue, algo))
    p.start()
    processes.append(p)

if __name__ == '__main__':
    main()
