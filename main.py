import argparse
import sys

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser

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
    clp.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                     default=sys.stdin)

    args = clp.parse_args()

    num_vars, clauses = parser.parse(args.infile)

    options = {
        'VERBOSE': args.verbose,
        'SEED': args.seed
    }

    if args.algo == 'genetic':
        a = ga.GeneticAlgorithm(num_vars, clauses, options)
    elif args.algo == 'ant':
        a = aa.AntColonyAlgorithm(num_vars, clauses, options)
    else:
        print "No such algorithm."

    a.run()
