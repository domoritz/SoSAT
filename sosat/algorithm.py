import sys
import numpy as np


class Algorithm(object):
    SEED = 42
    VERBOSE = False

    def __init__(self, num_vars=0, clauses=[], config={}):
        self.num_vars = num_vars
        self.num_lits = 2 * num_vars
        self.raw_clauses = clauses
        self.num_clauses = len(clauses)

        self.__dict__.update(config)

        np.random.seed(self.SEED)

        self.initialize_clauses()

    def initialize_clauses(self):
        num_clauses = len(self.raw_clauses)
        shape = (num_clauses, 2, self.num_vars)
        clauses = np.zeros(dtype=np.bool, shape=shape)
        for i, clause in enumerate(self.raw_clauses):
            for lit in clause:
                if lit > 0:
                    clauses[i][0][lit - 1] = True
                else:
                    clauses[i][1][-lit - 1] = True
        self.clauses = clauses

    def full_candidate(self, candidate):
        return np.array([candidate, ~candidate])

    def evaluate_full_candidate(self, full_candidate):
        return np.any(self.clauses & full_candidate, axis=(2, 1))

    def evaluate_candidate(self, candidate):
        return self.evaluate_full_candidate(self.full_candidate(candidate))

    def return_solution(self, best):
        solution = []
        for i, lit in enumerate(best):
            solution.append(str(i if lit else -i))
        sys.stdout.write("v " + ' '.join(solution) + '\n')
        sys.stdout.write("s SATISFIABLE\n")
        exit()
