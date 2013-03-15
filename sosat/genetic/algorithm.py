import numpy as np
import sosat.algorithm as algo


class GeneticAlgorithm(algo.Algorithm):
    NUM_CHROMOSOMES = 10
    ELIRATE = 0.1
    NUM_ELITES = NUM_CHROMOSOMES * ELIRATE

    def __init__(self, num_vars=0, clauses=[], config={}):
        super(GeneticAlgorithm, self).__init__(num_vars, clauses, config)

        self.fitnesses = np.zeros(shape=(self.NUM_CHROMOSOMES, 1), dtype=np.int)
        self.generate_initial_population()

    def generate_initial_population(self):
        shape = (self.NUM_CHROMOSOMES, self.num_vars)
        self.pop = np.random.choice([True, False], shape)

    def mutate_chromosomes(self, chromosomes):
        where_to_toggle = np.random.randint(0, self.num_vars, size=len(chromosomes))
        for i, x in enumerate(where_to_toggle):
            chromosomes[i][x] = not chromosomes[i][x]

    def crossover(self, c1, c2):
        cop = np.random.randint(0, self.num_vars)
        return c1[cop:] + c2[:cop]

    def calculate_fitness(self, chromosome):
        return sum(self.evaluate_candidate(chromosome))

    def evaluate_fitness_of_population(self):
        for i, chromosome in enumerate(self.pop):
            self.fitnesses[i] = self.calculate_fitness(chromosome)

    def run(self):
        self.evaluate_fitness_of_population()
        while True:
            break
