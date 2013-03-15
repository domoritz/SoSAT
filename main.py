import argparse
import sys
import os
import multiprocessing
from multiprocessing import Process, Event, Queue

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser


class MyProcess(Process):
    def __init__(self, event, *args, **kwargs):
        self.event = event
        Process.__init__(self, *args, **kwargs)

    def run(self):
        Process.run(self)
        self.event.set()


if __name__ == '__main__':
    clp = argparse.ArgumentParser(description='SAT solver.')
    clp.add_argument('-a', '--algorithm', dest='algo',
                     default='genetic', choices=['genetic', 'ant', 'other'],
                     help='select algorithm for solving')
    clp.add_argument('-v', '--verbose', dest='verbose',
                     default=False, action='store_true',
                     help='print stats and status message')
    clp.add_argument('-s', '--seed', dest='seed',
                     default=42,
                     help='seed for random number generator')
    clp.add_argument('-N', '--number', dest='N',
                     default=1, type=int,
                     help='number of processes')
    clp.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                     default=sys.stdin)

    args = clp.parse_args()

    num_vars, clauses = parser.parse(args.infile)

    processes = []
    queue = Queue()
    event = Event()

    def print_solution(solution):
        sol = []
        for i, lit in enumerate(solution):
            sol.append(str(i if lit else -i))
        sys.stdout.write("v " + ' '.join(sol) + '\n')
        sys.stdout.write("s SATISFIABLE\n")

    def start(seed, queue):
        options = {
            'VERBOSE': args.verbose,
            'SEED': seed
        }

        if args.verbose:
            print "Start one process with args", options

        if args.algo == 'genetic':
            a = ga.GeneticAlgorithm(num_vars, clauses, options)
        elif args.algo == 'ant':
            a = aa.AntColonyAlgorithm(num_vars, clauses, options)
        else:
            print "No such algorithm."
        queue.put(a.run())

    if not args.N:
        args.N = multiprocessing.cpu_count()

    seeds = range(args.seed, args.seed + args.N)
    for seed in seeds:
        p = MyProcess(event, target=start, args=(seed, queue))
        p.start()
        processes.append(p)

    event.wait()

    for process in processes:
        process.terminate()
    for process in processes:
        process.join()

    print_solution(queue.get())
