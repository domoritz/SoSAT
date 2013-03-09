import argparse
import sys

import genetic
import ant
import parser


if __name__ == '__main__':
    clp = argparse.ArgumentParser(description='SAT solver.')
    clp.add_argument('-a', '--algorithm', dest='algo',
                     default='genetic', choices=['genetic', 'ant', 'other'],
                     help='select algorithm for solving')
    clp.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                     default=sys.stdin)

    args = clp.parse_args()

    num_vars, clauses = parser.parse(args.infile)

    if args.algo == 'genetic':
        a = genetic.Algorithm(num_vars, clauses)
    elif args.algo == 'ant':
        a = ant.Algorithm(num_vars, clauses)
    else:
        print "No such algorithm."

    a.run()
