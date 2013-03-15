import argparse
import sys
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


def print_solution(solution):
    if solution is not None:
        sol = []
        for i, lit in enumerate(solution):
            sol.append(str(i if lit else -i))
        sys.stdout.write("v " + ' '.join(sol) + '\n')
        sys.stdout.write("s SATISFIABLE\n")
    else:
        sys.stdout.write("s UNSATISFIABLE\n")


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

    def start(seed, queue=None):
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
        if queue:
            queue.put(a.run())
        else:
            print_solution(a.run())

    if args.N == 1:
        start(args.seed)
        exit()

    processes = []
    queue = Queue()
    event = Event()

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
    exit()
