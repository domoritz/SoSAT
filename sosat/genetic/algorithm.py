import numpy as np
import bottleneck as bn
import sosat.algorithm as algo


class GeneticAlgorithm(algo.Algorithm):
    NUM_CHROMOSOMES = 100
    ELIRATE = 0.1
    SELRATE = 0.2
    NUM_ELITES = NUM_CHROMOSOMES * ELIRATE
    # actual selection is twice the size so that we always get pairs
    NUM_SELECTED = NUM_CHROMOSOMES * SELRATE

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
        return np.concatenate([c1[:cop], c2[cop:]])

    def calculate_fitness(self, chromosome):
        return sum(self.evaluate_candidate(chromosome))

    def evaluate_fitnesses(self, popuation):
        fitnesses = np.zeros(shape=(len(popuation), 1))
        for i, chromosome in enumerate(popuation):
            fitnesses[i] = self.calculate_fitness(chromosome)
        return fitnesses

    def evaluate_fitness_of_population(self):
        for i, chromosome in enumerate(self.pop):
            self.fitnesses[i] = self.calculate_fitness(chromosome)

    def get_non_elites(self):
        # get indexes of chromosomes that are not elites
        indexes = bn.argpartsort(-self.fitnesses.flatten(), n=self.NUM_ELITES)
        num_no_elites = self.NUM_CHROMOSOMES - self.NUM_ELITES
        no_elites = indexes[-num_no_elites:]
        np.random.shuffle(no_elites)
        return no_elites[:self.NUM_SELECTED]

    def get_selection(self):
        # selects random parents
        return np.random.randint(0, self.NUM_CHROMOSOMES, size=2 * self.NUM_SELECTED)

    def run(self):
        assert(self.NUM_CHROMOSOMES - self.NUM_ELITES > self.NUM_SELECTED)
        self.evaluate_fitness_of_population()

        offspring = np.zeros(shape=(self.NUM_SELECTED, self.num_vars), dtype=np.bool)
        while True:
            selection = self.get_selection().reshape(self.NUM_SELECTED, 2)

            for i, pair in enumerate(selection):
                offspring[i] = self.crossover(self.pop[pair[0]], self.pop[pair[1]])
            offspring_fitnesses = self.evaluate_fitnesses(offspring)
            no_elites = self.get_non_elites()
            self.pop[no_elites] = offspring
            self.fitnesses[no_elites] = offspring_fitnesses
            break
