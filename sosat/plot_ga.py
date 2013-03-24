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
        'MAX_ITERATIONS': 1000
    }

    a = algo(num_vars, clauses, conf)
    a.run()

    xs = []
    ys = []
    for k, d in enumerate(a.progress):
        for v in d['values']:
            xs.append(k)
            ys.append(v)
    plt.scatter(xs, ys, s=10, alpha=0.15)
    '''
    # or hist2d
    import matplotlib.cm as cm
    plt.hexbin(xs, ys, gridsize=45, cmap=cm.jet, bins=None)
    plt.axis([min(xs), max(xs), min(ys), max(ys)])

    cb = plt.colorbar()
    cb.set_label('Number of clauses')'''

    data = np.array([x['best'] for x in a.progress])

    xs = range(len(data))
    ys = data
    #ys = np.abs(data - len(clauses))
    #plt.ylim([0, np.max(data)])
    plt.xlim([0, len(data)])

    #plt.semilogy(xs, ys, 'bo-', label='Performance')
    plt.plot(xs, ys, 'ro-', label='Performance')

    # Styling
    plt.xlabel('Iteration')
    plt.ylabel('Satisfied clauses')
    plt.title('Genetic Algorithm - Performance')
    plt.grid(True, which="both", linestyle="dotted")

    from matplotlib.backends.backend_pdf import PdfPages
    pp = PdfPages('plots/ga_performance_ksat13.pdf')
    plt.savefig(pp, format='pdf')
    pp.close()

    plt.show()

if __name__ == '__main__':
    run()
