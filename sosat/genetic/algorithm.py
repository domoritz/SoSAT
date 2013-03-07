import numpy as np


class GeneticAlgorithm(object):
    NUM_INDIVIDUALS = 10
    SEED = 42

    def __init__(self, num_vars, clauses):
        self.num_vars = num_vars
        self.clauses = clauses
        print num_vars, clauses

        np.random.seed(self.SEED)

        self.generate_initial_population()

    def generate_initial_population(self):
        size = self.num_vars * self.NUM_INDIVIDUALS
        # generate list from random choice
        self.pop = np.random.choice([True, False], size)
        # we want bool, so let's convert to bool
        self.pop = self.pop.astype(np.bool, copy=False)
        # amek an array from the list
        self.pop = self.pop.reshape(self.num_vars, self.NUM_INDIVIDUALS)
        print self.pop

    def run(self):
        print "run"
