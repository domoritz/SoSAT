import sosat.genetic.algorithm as ga
import sosat.parser as parser

import matplotlib.pyplot as plt
import numpy as np


def run():
    algo = ga.GeneticAlgorithm
    f = open('instances/random_ksat13.dimacs')
    num_vars, clauses = parser.parse(f)

    conf = {
        'COLLECT_STATS': True,
        'MAX_ITERATIONS': 1500,
        'MUTATION_RATE': 0.5,
        'CATASTROPHY_THRESHOLD': 2.3,
        'CATASTROPHES': True
    }

    a = algo(num_vars, clauses, conf)
    a.run()

    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

    xs = []
    ys = []
    for k, d in enumerate(a.progress):
        for v in d['values']:
            xs.append(k)
            ys.append(v)

    import matplotlib.cm as cm
    from matplotlib.colors import LogNorm
    x_range = max(xs) - min(xs)
    y_range = max(ys) - min(ys)

    #ax1.scatter(xs, ys, s=10, alpha=0.15)

    #'''
    h = ax1.hist2d(xs, ys, bins=(x_range, y_range), norm=LogNorm())
    f.subplots_adjust(right=0.8)
    #f.colorbar(h[3], ax=ax1)
    #'''
    '''
    ax1.hexbin(xs, ys, gridsize=(x_range, y_range), cmap=cm.jet, bins=None)
    ax1.axis([min(xs), max(xs), min(ys), max(ys)])

    #cb = plt.colorbar()
    #cb.set_label('Number of clauses')
    #'''

    data = np.array([x['best'] for x in a.progress])
    xs = range(len(data))
    ys = data
    #ys = np.abs(data - len(clauses))
    #plt.ylim([0, np.max(data)])
    plt.xlim([0, len(data)])
    #plt.semilogy(xs, ys, 'bo-', label='Performance')
    ax1.plot(xs, ys, 'ro-', label='Best performance')

    # average
    data = np.array([x['values'] for x in a.progress])
    xs = range(len(data))
    ys = np.average(data, axis=1)
    plt.xlim([0, len(data)])
    ax1.plot(xs, ys, 'go-', label='Average performance')

    # std
    data = np.array([x['values'] for x in a.progress])
    xs = range(len(data))
    ys = np.std(data, axis=1)
    ax2.plot(xs, ys, 'b-', label='Standard derivative')

    # mr
    data = np.array([x['mr'] for x in a.progress])
    xs = range(len(data))
    ys = data
    ax3.plot(xs, ys, 'g-', label='Mutation rate')

    # Styling
    f.subplots_adjust(hspace=0)
    plt.xlabel('Iteration')
    ax1.set_ylabel('Satisfied clauses')
    ax2.set_ylabel('Value')
    ax1.set_title('Genetic Algorithm - Performance')
    ax1.grid(True, which="both", linestyle="dotted")
    ax1.legend()
    ax2.legend()
    ax3.legend()

    from matplotlib.backends.backend_pdf import PdfPages
    pp = PdfPages('plots/ga_performance_ksat13.pdf')
    plt.savefig(pp, format='pdf')
    pp.close()

    print "Plotted"
    plt.show()

if __name__ == '__main__':
    run()
