print "AA1"
import argparse
import sys

print "AA2"
import sosat.algorithm as algo
print "AA2"
import sosat.genetic.algorithm as ga
print "AA3"
import sosat.ant.algorithm as aa
print "AA4"
import sosat.parser as parser

print "AA"

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
        a = ga.GeneticAlgorithm(num_vars, clauses)
    elif args.algo == 'ant':
        print "starting ant"
        a = aa.AntColonyAlgorithm(num_vars, clauses)
    else:
        print "No such algorithm."

    a.run()