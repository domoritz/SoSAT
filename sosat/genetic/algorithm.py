import numpy as np
import bottleneck as bn
import sosat.algorithm as algo


class GeneticAlgorithm(algo.Algorithm):
    NUM_CHROMOSOMES = 100
    ELIRATE = 0.2
    SELRATE = 0.3
    NUM_ELITES = NUM_CHROMOSOMES * ELIRATE
    # actual selection is twice the size so that we always get pairs
    NUM_SELECTED = NUM_CHROMOSOMES * SELRATE
    MUTATION_RATE = 0.3

    def __init__(self, num_vars=0, clauses=[], config={}):
        super(GeneticAlgorithm, self).__init__(num_vars, clauses, config)

        self.fitnesses = np.zeros(self.NUM_CHROMOSOMES, dtype=np.int)
        self.generate_initial_population()

    def generate_initial_population(self):
        shape = (self.NUM_CHROMOSOMES, self.num_vars)
        self.pop = np.random.choice([True, False], shape)

    def mutate_offspring(self, chromosomes):
        size = len(chromosomes)
        where_to_toggle = np.random.randint(1, self.num_vars - 1, size=size)
        for i, x in enumerate(where_to_toggle[self.MUTATION_RATE * size:]):
            chromosomes[i][x] = not chromosomes[i][x]

    def crossover(self, c1, c2):
        cop = np.random.randint(0, self.num_vars)
        return np.concatenate([c1[:cop], c2[cop:]])

    def calculate_fitness(self, chromosome):
        return sum(self.evaluate_candidate(chromosome))

    def evaluate_fitnesses(self, popuation, fitnesses):
        for i, chromosome in enumerate(popuation):
            fitnesses[i] = self.calculate_fitness(chromosome)

    def evaluate_fitness_of_population(self):
        self.evaluate_fitnesses(self.pop, self.fitnesses)

    def get_non_elites(self):
        # get indexes of chromosomes that are not elites
        indexes = bn.argpartsort(-self.fitnesses, n=self.NUM_ELITES)
        num_no_elites = self.NUM_CHROMOSOMES - self.NUM_ELITES
        no_elites = indexes[-num_no_elites:]
        np.random.shuffle(no_elites)
        return no_elites[:self.NUM_SELECTED]

    def get_selection(self):
        # selects random parents
        return np.random.randint(0, self.NUM_CHROMOSOMES, size=2 * self.NUM_SELECTED)

    def show(self):
        print "Population:"
        for i, chromosome in enumerate(self.pop):
            print i, chromosome, self.fitnesses[i]
        print max(self.fitnesses), 'of', self.num_clauses

    def run(self):
        assert(self.NUM_CHROMOSOMES - self.NUM_ELITES > self.NUM_SELECTED)
        self.evaluate_fitness_of_population()

        offspring = np.zeros((self.NUM_SELECTED, self.num_vars), dtype=np.bool)
        offspring_fitnesses = np.zeros(self.NUM_SELECTED, dtype=np.int)
        for iteration in xrange(self.MAX_ITERATIONS):
            selection = self.get_selection().reshape(self.NUM_SELECTED, 2)
            for i, pair in enumerate(selection):
                offspring[i] = self.crossover(self.pop[pair[0]], self.pop[pair[1]])
            self.mutate_offspring(offspring)
            self.evaluate_fitnesses(offspring, offspring_fitnesses)
            no_elites = self.get_non_elites()
            self.pop[no_elites] = offspring
            self.fitnesses[no_elites] = offspring_fitnesses

            if self.num_clauses in self.fitnesses:
                break

            if self.VERBOSE:
                print max(self.fitnesses), 'of', self.num_clauses

        index_of_best = list(self.fitnesses).index(self.num_clauses)
        best = self.pop[index_of_best]
        return best
