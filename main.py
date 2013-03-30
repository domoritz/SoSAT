import argparse
import sys
import multiprocessing
from multiprocessing import Process, Queue
import time

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser
import sosat.preprocessing as preprocessing

class MyProcess(Process):
    def run(self):
        Process.run(self)

def print_solution(instance_solution):
    instance, p_solution = instance_solution

    if p_solution is not None:
        solution = preprocessing.restore_original_solution(instance, p_solution)

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

    num_vars, clauses = parser.parse(args.infile)
    factored_instances = preprocessing.factored_instances(num_vars, clauses, args.f)

    if args.verbose:
        print "Reduced instances:"

        for i in factored_instances:
            print i[0], " / ", num_vars
     
    def start(instance, seed, queue):
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

    for i in xrange(len(seeds) * len(factored_instances)):
        solution = queue.get()
        if solution is not None:
            print_solution(solution)
     
            for process in processes:
                process.terminate()
    
            exit()
    
    print_solution(None)
