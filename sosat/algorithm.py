import numpy as np


class Algorithm(object):
    SEED = 42

    def __init__(self, num_vars=0, clauses=[]):
        self.num_vars = num_vars
        self.raw_clauses = clauses

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

    def evaluate_candidate(self, candidate):
        full_candiate = np.array([candidate, ~candidate])
        return np.any(self.clauses & full_candiate, axis=(2, 1))
