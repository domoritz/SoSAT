import time
import signal
import json
from contextlib import contextmanager

import sosat.genetic.algorithm as ga
import sosat.parser as parser

import matplotlib.pyplot as plt
import numpy as np


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


NAME = 'ga_seed_sensitivity'


def run():
    algo = ga.GeneticAlgorithm
    f = open('instances/random_ksat3.dimacs')

    results = {}

    num_vars, clauses = parser.parse(f)

    in_data = {
        'MUTATION_RATE': [float(x) / 20 for x in range(1, 18)],
        'SELRATE': [float(x) / 40 for x in range(1, 20)]
    }

    for parameter in in_data.keys():
        print parameter
        data = in_data[parameter]
        results[parameter] = {}
        for i, value in enumerate(data):
            print i, 'of', len(data)
            times = []
            for seed in range(10):
                conf = {
                    parameter: value,
                    'SEED': 42 + seed,
                    'ELIRATE': 0
                }
                a = algo(num_vars, clauses, conf)

                start = time.time()
                try:
                    # timeout in seconds
                    with time_limit(20):
                        a.run()
                except TimeoutException, msg:
                    print msg
                else:
                    elapsed = time.time() - start
                    times.append(elapsed)

            if len(times) > 1:
                results[parameter][value] = {
                    'std': np.std(np.array(times)),
                    'avg': sum(times) / len(times)
                }
    return results


def plot(results):
    ax1 = plt.subplot2grid((2, 1), (0, 0))
    ax2 = plt.subplot2grid((2, 1), (1, 0))

    d = results['MUTATION_RATE']
    xs = sorted(d.keys())
    mr_avgs = [d[x]['avg'] for x in xs]
    mr_stds = [d[x]['std'] for x in xs]

    ax1.plot(xs, mr_stds, 'go--', label="variable mutation rate")
    ax2.plot(xs, mr_avgs, 'go--', label="variable mutation rate")

    d = results['SELRATE']
    xs = sorted(d.keys())
    sr_avgs = [d[x]['avg'] for x in xs]
    sr_stds = [d[x]['std'] for x in xs]

    ax1.plot(xs, sr_stds, 'bo--', label="variable selection rate")
    ax2.plot(xs, sr_avgs, 'bo--', label="variable selection rate")

    ## Styling

    # no space between plots
    plt.subplots_adjust(hspace=0)
    ax1.set_xticklabels([])

    plt.xlim([0.1, 0.9])
    plt.xlabel('rate')
    ax1.grid(True, which="both", linestyle="dotted")
    ax2.grid(True, which="both", linestyle="dotted")
    ax1.legend(loc='upper right')
    #ax2.legend(loc='upper right')

    ax1.set_ylabel('standard derivative')
    ax2.set_ylabel('average')

    from matplotlib.backends.backend_pdf import PdfPages
    pp = PdfPages('plots/{}.pdf'.format(NAME))
    plt.savefig(pp, format='pdf')
    pp.close()

    plt.show()


def save(data):
    with open('data/{}.json'.format(NAME), 'wb') as fp:
        json.dump(data, fp)


def load():
    with open('data/{}.json'.format(NAME), 'rb') as fp:
        return json.load(fp)

if __name__ == '__main__':
    #'''
    results = run()
    save(results)
    '''
    results = load()
    #'''
    plot(results)
