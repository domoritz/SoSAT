import time
import signal
import json
from contextlib import contextmanager

import sosat.genetic.algorithm as ga
import sosat.ant.algorithm as aa
import sosat.parser as parser

import matplotlib.pyplot as plt


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


NAME = 'ga_popsize_ksat13'


def run():
    algo = ga.GeneticAlgorithm
    filenames = ['instances/random_ksat13.dimacs']
    files = [open(x) for x in filenames]

    results = {}

    f = files[0]
    num_vars, clauses = parser.parse(f)

    data = range(30, 100, 10) + [150, 200, 300, 400, 600, 800, 1000]
    for i, popsize in enumerate(data):
        print i, 'of', len(data)
        times = []
        TIMEOUT = 8
        for seed in range(3):
            conf = {
                'NUM_CHROMOSOMES': popsize,
                'SEED': 42 + seed
            }
            a = algo(num_vars, clauses, conf)

            start = time.time()
            try:
                # tmeout in seconds
                with time_limit(TIMEOUT):
                    a.run()
            except TimeoutException, msg:
                print msg
            else:
                elapsed = time.time() - start
                times.append(elapsed)

        # timeout
        results[popsize] = {
            'no_to': 0,
            'avg': TIMEOUT,
            'min': TIMEOUT,
            'values': [TIMEOUT]
        }
        if len(times):
            results[popsize] = {
                'no_to': len(times),
                'avg': sum(times) / len(times),
                'min': min(times),
                'values': times
            }
    return results


def plot(results):

    xs = []
    ys = []
    maxy = 0
    for k in results.keys():
        for v in results[k]['values']:
            xs.append(k)
            ys.append(v)
        maxy = max([maxy, results[k]['avg']])
    #plt.plot(xs, ys, 'bo', alpha=0.5)
    plt.ylim([0, maxy * 1.1])

    xs = results.keys()
    xs.sort()
    avgs = [results[x]['avg'] for x in xs]
    mins = [results[x]['min'] for x in xs]

    plt.plot(xs, avgs, 'ro--', label="Average")
    plt.plot(xs, mins, 'go--', label="Minimum")

    # Styling
    plt.xlabel('Population size')
    plt.ylabel('Seconds')
    plt.title('Genetic Algorithm - Population sizes')
    plt.grid(True, which="both", linestyle="dotted")
    plt.legend()

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
