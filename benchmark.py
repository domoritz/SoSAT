import time
import itertools as it
import os
import multiprocessing
from multiprocessing import Process, Semaphore
import numpy as np

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser

#'''
parameters = {
    'algo': ga.GeneticAlgorithm,
    'files': ['benchmark_instances/random_ksat3.dimacs'], #map(lambda d: 'benchmark_instances/' + d, os.listdir('benchmark_instances')),
    'params': {
        'NUM_CHROMOSOMES': [100, 150, 200],
        'ELIRATE': [0.01, 0.1, 0.2],
        'SELRATE': [0.1, 0.2, 0.4],
        'MUTATION_RATE': [0.2, 0.4, 0.7],
        'NUM_FORCED': [0, 1, 5],
        'NUM_NEW_RANDOM': [0, 1, 2],
        'NUM_GOOD_START': [0, 1, 10],
        #'ADAPTION_THRESHOLD': [1.0, 2.0, 3.0],
        #'CATASTROPHES': [True],
        #'CATASTROPHES_BOUNDS': [[100, 800], [1000, 200], [100, 250]],
        #'BLUR_BASIC': [0.2, 0.5, 1.0],
        #'BLUR_DECLINE': [50, 250, 2000],
        #'BLUR_ITERATIONS': [1, 25, 100],
        #'EXP_MCV': [0.1, 0.5, 1.0],
        #'PH_REDUCE_FACTOR': [0.15, 0.25, 0.5],
        #'WEIGHT_ADAPTION_DURATION': [10, 100, 250],
        #'NUM_ANTS': [25, 150, 250],
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

semaphore=0
class MyProcess(Process):
    def run(self):
        Process.run(self)

def run():
    global semaphore
    algo = parameters['algo']
    files = [open(x) for x in parameters['files']]
    algo_configs= [0,0,0]

    configs = []
    p = parameters['params']
    max_processes = 1
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

    proc = [0, 0, 0]
    start_proc = [time.time(), time.time(), time.time()]

    for f in files:
        for conf in configs:        
            config = {'FILENAME': f.name}
            config.update(conf)

            f.seek(0)
            num_vars, clauses = parser.parse(f)
            
            tp = 0
            started_it = False
            
            while not started_it:
                for i in range(3):
                    if proc[i] == 0 or not proc[i].is_alive() or time.time() - start_proc[i] > 45:
                        try:
                            algo_configs[i].update({'TIME': -2})
                            if time.time() - start_proc[i] > 45:
                                print algo_configs[i]
                            proc[i].terminate()
                        except Exception:
                            pass

                        proc[i] = MyProcess(target=run_algorithm, args=(algo, num_vars, clauses, config))
                        algo_configs[i] = config
                        start_proc[i] = time.time()
                        proc[i].start()
                        started_it = True
                        time.sleep(0.5)

            #tp = MyProcess(target=process_killer, args=(p, config, 20))
             
            #semaphore.release() 
            #tp.start()


def run_wrapper(algo, num_vars, clauses, config):
    global semaphore
    ap = MyProcess(target=run_algorithm, args=(algo, num_vars, clauses, config))
    ap.start()
    print config
    print ap.join(1)
    semaphore.release()


def run_algorithm(algo, num_vars, clauses, config):
    start = time.time()
    a = algo(num_vars, clauses, config)
    try:
      result = a.run()
    except Exception:
      config.update({'TIME': -1})
      print config
      #semaphore.release()
      return -1

    elapsed = time.time() - start
    config.update({'TIME': elapsed, 'SOLVED_SUCCESSFULLY': result is not None})
    print config

    return 0

if __name__ == '__main__':
    run()
