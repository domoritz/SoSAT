import time
import itertools as it
import os
import multiprocessing
from multiprocessing import Process, Semaphore

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser

#'''
parameters = {
    'algo': aa.AntColonyAlgorithm,
    'files': map(lambda d: 'benchmark_instances/' + d, os.listdir('benchmark_instances')),
    'params': {
        'NUM_ANTS': [25, 150, 250],
        'EXP_PH': [1],
        'EXP_MCV': [0.1, 0.5, 1],
        'PH_REDUCE_FACTOR': [0.15, 0.25, 0.5],
        'BLUR_ITERATIONS': [1, 25, 100],
        'BASIC_BLUR': [0.2, 0.5, 1.0],
        'BLUR_DECLINE': [50, 250, 2000],
        'WEIGHT_ADAPTION_DURATION': [10, 100, 250],
        'EPSILON': [0.0000001],
        'SEED': [42],
        'MAX_ITERATIONS': [25000]
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

class MyProcess(Process):
    def run(self):
        Process.run(self)

def run():
    algo = parameters['algo']
    files = [open(x) for x in parameters['files']]
    configs = []
    p = parameters['params']
    max_processes = 3
    semaphore = Semaphore(max_processes)

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
            config = {'FILENAME': f.name}
            config.update(conf)

            f.seek(0)
            num_vars, clauses = parser.parse(f)
            
            p = MyProcess(target=run_algorithm, args=(algo, num_vars, clauses, config, semaphore))
            
            semaphore.acquire()
            p.start()


def run_algorithm(algo, num_vars, clauses, config, semaphore):
    start = time.time()
    a = algo(num_vars, clauses, config)
    result = a.run()
    elapsed = time.time() - start
    config.update({'TIME': elapsed, 'SOLVED_SUCCESSFULLY': result is not None})
    print config
    semaphore.release()
    
if __name__ == '__main__':
    run()
