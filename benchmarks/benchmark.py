import time
import itertools as it

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser

#'''
parameters = {
    'algo': ga.GeneticAlgorithm,
    'files': ['instances/random_ksat13.dimacs'],
    'params': {
        'ELIRATE': [0.1, 0.2, 0.3, 0.4],
        'NUM_FOR_FORCE': [0, 1, 2],
        'SELRATE': [0.2]
    }
}
'''
parameters = {
    'algo': ga.GeneticAlgorithm,
    'files': ['instances/random_ksat13.dimacs'],
    'params': {
        'ELIRATE': [0.1, 0.2, 0.3, 0.4],
        'NUM_FOR_FORCE': [0, 1, 2],
        'SELRATE': [0.2]
    }
}
'''


def run():
    algo = parameters['algo']
    files = [open(x) for x in parameters['files']]
    configs = []
    p = parameters['params']

    # generate configurations as compination of possible
    # keys and product of values
    for keys in it.combinations(p.keys(), len(p.keys())):
        v = [p[k] for k in keys]
        for values in it.product(*v):
            config = {}
            for i, k in enumerate(keys):
                config[k] = values[i]
            configs.append(config)
    for f in files:
        for conf in configs:
            print "=========="
            print f.name
            print conf

            f.seek(0)
            num_vars, clauses = parser.parse(f)
            a = algo(num_vars, clauses, conf)

            start = time.time()
            a.run()
            elapsed = time.time() - start

            print elapsed, 'seconds'
    print "=========="
    print "Done"

if __name__ == '__main__':
    run()
