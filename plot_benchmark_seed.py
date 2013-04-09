import time
import signal
import json
import numpy as np
from contextlib import contextmanager
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

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

SAMPLES = 50
NAME = 'aa_seed_ksat3'


def run():
    algo = aa.AntColonyAlgorithm
    filenames = ['instances/random_ksat3.dimacs']
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

    xs_tmp = np.array(results.keys())
    xs_tmp.sort()
    xs = map(int, xs_tmp)
    ys = np.array([results[k] for k in xs_tmp])
    maxy = max(results.values())
    #plt.plot(xs, ys, 'bo', alpha=0.5)
    #plt.ylim([0, maxy * 1.1])

    #plt.plot(xs, ys, 'ro--', label="Time")
    #plt.bar(range(SAMPLES), ys, color='r', align='center')
    ax = host_subplot(111)
    print results.keys()
    ax.plot(xs, ys, marker='x', color='red')
    ax.set_xlim((42,91))
    ax.set_ylim((0,4))
    labels = [item.get_text() for item in ax.get_yticklabels()]
    labels[1] = 'timeout'
    #ax.set_yticklabels(['0', '5', '10', '15', 'timeout'])

    #plt.xticks(range(SAMPLES), xs)

    # Styling
    plt.xlabel('seed')
    plt.ylabel('runtime (seconds)')
    plt.grid(True, which="both", linestyle="dotted")
    #plt.legend()

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
    
