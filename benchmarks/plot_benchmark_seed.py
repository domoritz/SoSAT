import time
import signal
import json
import numpy as np
from contextlib import contextmanager

import sosat.genetic.algorithm as ga
import sosant.ant.algorithm as aa
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

SAMPLES = 50
NAME = 'ga_seed_ksat11'


def run():
    algo = aa.AntColonyAlgorithm
    filenames = ['instances/random_ksat11.dimacs']
    files = [open(x) for x in filenames]

    results = {}

    f = files[0]
    num_vars, clauses = parser.parse(f)

    for i, seed in enumerate(np.arange(SAMPLES) + 42):
        print i, 'of', SAMPLES
        conf = {
            'SEED': seed
        }
        a = algo(num_vars, clauses, conf)

        start = time.time()
        try:
            # timeout in seconds
            with time_limit(20):
                a.run()
        except TimeoutException, msg:
            print msg
        elapsed = time.time() - start

        results[seed] = elapsed
    return results


def plot(results):

    xs = np.array(results.keys())
    xs.sort()
    ys = np.array([results[k] for k in xs])
    maxy = max(results.values())
    #plt.plot(xs, ys, 'bo', alpha=0.5)
    plt.ylim([0, maxy * 1.1])

    #plt.plot(xs, ys, 'ro--', label="Time")
    plt.bar(range(SAMPLES), ys, color='r', align='center')
    plt.xticks(range(SAMPLES), xs)

    # Styling
    plt.xlabel('Seed')
    plt.ylabel('Seconds')
    plt.title('Genetic Algorithm - Seeds')
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
    '''
    results = run()
    save(results)
    '''
    results = load()
    #'''
    plot(results)
