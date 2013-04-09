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


NAME = 'ga_elirate_ksat13'


def run():
    algo = ga.GeneticAlgorithm
    filenames = ['instances/random_ksat13.dimacs']
    files = [open(x) for x in filenames]

    results = {}

    f = files[0]
    num_vars, clauses = parser.parse(f)

    data = [float(x) / 100 for x in range(0, 50, 2)]
    for i, erate in enumerate(data):
        print i, 'of', len(data)
        times = []
        for seed in range(5):
            conf = {
                'ELIRATE': erate,
                'SEED': 42 + seed
            }
            a = algo(num_vars, clauses, conf)

            start = time.time()
            try:
                # timeout in seconds
                with time_limit(5):
                    a.run()
            except TimeoutException, msg:
                print msg
            else:
                elapsed = time.time() - start
                times.append(elapsed)

        results[erate] = {
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

    plt.plot(xs, avgs, 'ro--', label="average")
    plt.plot(xs, mins, 'go--', label="minimum")

    # Styling
    plt.xlabel('elite rate')
    plt.ylabel('seconds')
    plt.title('Genetic Algorithm - Elite rates')
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
