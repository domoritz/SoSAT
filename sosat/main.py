import argparse
import sys
import multiprocessing
from multiprocessing import Process, Queue
import time

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser
import sosat.preprocessing as preprocessing

VERBOSE = False

class MyProcess(Process):
    def run(self):
        Process.run(self)

def print_solution(instance_solution, num_vars):
    instance, p_solution = instance_solution

    if p_solution is False:
        sys.stdout.write("s UNSATISFIABLE\n")
    elif p_solution is not None:
        solution = preprocessing.restore_original_solution(instance, p_solution, num_vars)

        sol = []
        for i, lit in enumerate(solution):
            sol.append(str(i + 1 if lit else -i - 1))
        sys.stdout.write("v " + ' '.join(sol) + ' 0\n')
        sys.stdout.write("s SATISFIABLE\n")
    else:
        sys.stdout.write("s UNKNOWN\n")


if __name__ == '__main__':
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

    num_vars, clauses = parser.parse(args.infile)
    factored_instances = preprocessing.factored_instances(num_vars, clauses, min(args.f, num_vars))

    if args.verbose:
        print "c Reduced instances:"

        for i in factored_instances:
            print "c", i, " / ", num_vars, "original variables"

    def start(instance, seed, queue):
        if not instance == False:
            # detected that this is unsolvable during preprocessing
            queue.put((instance, False))
            return

        if len(instance[1]) == 0:
            # found solution during preprocessing
            queue.put((instance, []))
            return

        options = {
            'VERBOSE': args.verbose,
            'SEED': seed
        }

        if args.verbose:
            print "c Start one process with args", options

        if args.algo == 'genetic':
            a = ga.GeneticAlgorithm(instance[0], instance[1], options)
        elif args.algo == 'ant':
            a = aa.AntColonyAlgorithm(instance[0], instance[1], options)
        else:
            print "No such algorithm."

        solution = a.run()
        queue.put((instance, solution))

    processes = []
    queue = Queue()

    if not args.N:
        args.N = multiprocessing.cpu_count()

    seeds = range(args.seed, args.seed + args.N)
    for seed in seeds:
        for instance in factored_instances:
            p = MyProcess(target=start, args=(instance, seed, queue))
            p.start()
            processes.append(p)

    false_counter = 0

    if VERBOSE:
        print "c Waiting for at most", len(seeds) * len(factored_instances), "results..."

    for i in xrange(len(seeds) * len(factored_instances)):
        solution = queue.get()
        if solution[0] == False:
            false_counter += 1
        elif solution is not None:
            print_solution(solution, num_vars)

            for process in processes:
                process.terminate()

            exit()

    if false_counter == len(seeds) * len(factored_instances):
        print_solution(False, 0)
    else:
        print_solution(None, 0)
