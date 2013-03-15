import numpy as np
import sosat.algorithm as algo


class GeneticAlgorithm(algo.Algorithm):
    NUM_CHROMOSOMES = 10
    ELIRATE = 0.1
    NUM_ELITES = NUM_CHROMOSOMES * ELIRATE

    def __init__(self, num_vars=0, clauses=[]):
        super(GeneticAlgorithm, self).__init__(num_vars, clauses)

        self.generate_initial_population()

    def generate_initial_population(self):
        size = self.num_vars * self.NUM_CHROMOSOMES
        print self.num_vars
        # generate list from random choice
        self.pop = np.random.choice([True, False], size)
        # make an array from the list
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
