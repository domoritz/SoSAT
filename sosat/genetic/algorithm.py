import numpy as np
import numexpr as ne


class GeneticAlgorithm(object):
    NUM_CHROMOSOMES = 10
    ELIRATE = 0.1
    NUM_ELITES = NUM_CHROMOSOMES * ELIRATE
    SEED = 42

    def __init__(self, num_vars=0, clauses=[]):
        self.num_vars = num_vars
        self.clauses = clauses
        print num_vars, clauses

        np.random.seed(self.SEED)

        self.generate_initial_population()

    def generate_clause_masks(self):
        '''
        defined_masks contains True, wherever we have a value in a clause
        true_masks contrains True for clause if we have a positive literal
        '''
        num_clauses = len(self.clauses)
        shape = (num_clauses, self.num_vars)
        defined_masks = np.zeros(dtype=np.bool, shape=shape)
        true_masks = defined_masks.copy()
        for i, clause in enumerate(self.clauses):
            for x in clause:
                defined_masks[i][abs(x) - 1] = True
            for x in filter(lambda x: x > 0, clause):
                true_masks[i][x - 1] = True
        self.defined_masks = defined_masks
        self.true_masks = true_masks

    def generate_initial_population(self):
        size = self.num_vars * self.NUM_CHROMOSOMES
        # generate list from random choice
        self.pop = np.random.choice([True, False], size)
        # we want bool, so let's convert to bool
        self.pop = self.pop.astype(np.bool, copy=False)
        # amek an array from the list
        self.pop = self.pop.reshape(self.num_vars, self.NUM_CHROMOSOMES)

    def mutate_chromosomes(self, array):
        where_to_toggle = np.random.randint(0, self.num_vars, size=len(array))
        for i, x in enumerate(where_to_toggle):
            array[i][x] = not array[i][x]

    def calculate_fitness(self):
        pass

    def run(self):
        while True:
            break
