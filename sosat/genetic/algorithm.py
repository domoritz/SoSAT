import numpy as np
import bottleneck as bn
import sosat.algorithm as algo
import sosat.annealing.algorithm as sa


class GeneticAlgorithm(algo.Algorithm):
    # Population size
    NUM_CHROMOSOMES = 200

    # Relative number of elites
    ELITES_RATE = 0.10

    # Relative number of individuals selected for
    # breeding offspring.
    SELECTION_RATE = 0.2

    # Probability for mutation of offspring
    # if mutation rate is dynamic, this is the initial rate
    MUTATION_RATE = 0.4

    # Number of individuals where false clauses are forced true
    NUM_FORCED = 2

    # Number of random individuals that are generated as offspring
    NUM_NEW_RANDOM = 0

    # Absolute number of individuals that are generated by
    # simulated annealing and used in the initial population
    NUM_GOOD_START = 1

    # We can wither select randomly or the once with a better performance with
    # a higher probability
    SELECT_PROBABILITY = True

    # Enable or disable mutation rate adaption
    MR_ADAPTION = False
    # how often mutation rate is adapted
    ADAPT_EVERY = 20
    # If the standard derivative goes below this value,
    # mutation rate is increased
    ADAPTION_THRESHOLD = 2.6

    # Enable or disable distasters that destroy parts of the population
    # you should decrease the mutation rate (i.e. to 0.5), if you enable this
    CATASTROPHES = False
    # Catastrope if std below this value
    CATASTROPHE_THRESHOLD = 2.3
    # [not before x iterations, at least every x iterations]
    CATASTROPHE_BOUNDS = [120, 800]

    profiles = [
        {
            'MUTATION_RATE': 0.5,
            'CATASTROPHES': True
        },
        {
            'NUM_FORCED': 10
        }
    ]

    def __init__(self, num_vars=0, clauses=[], config={}):
        super(GeneticAlgorithm, self).__init__(num_vars, clauses, config)

        # We need at least one elite
        self.NUM_ELITES = max(1, int(self.NUM_CHROMOSOMES * self.ELITES_RATE))
        # Actual selection is twice the size so that we always get pairs
        self.NUM_SELECTED = int(2 * (self.NUM_CHROMOSOMES * (self.SELECTION_RATE / 2)))

        self.INI_MUTATION_RATE = self.MUTATION_RATE

        self.last_catastrophe = 0

        self.fitnesses = np.zeros(self.NUM_CHROMOSOMES, dtype=np.int)
        self.generate_initial_population()

    def generate_initial_population(self):
        a = sa.SimulatedAnnealing(self.num_vars, self.raw_clauses, {'SEED': self.SEED})
        shape = (self.NUM_CHROMOSOMES, self.num_vars)
        self.pop = np.random.choice([True, False], shape)
        for i in range(self.NUM_GOOD_START):
            self.pop[i] = a.run()

    def mutate_chromosomes(self, chromosomes):
        size = len(chromosomes)
        where_to_toggle = np.random.randint(0, self.num_vars, size=self.MUTATION_RATE * size)
        for i, x in enumerate(where_to_toggle):
            chromosomes[i][x] = not chromosomes[i][x]

    def crossover(self, c1, c2):
        cop = np.random.randint(0, self.num_vars)
        return np.concatenate([c1[:cop], c2[cop:]])

    def evaluate_fitnesses(self, popuation, fitnesses):
        for i, chromosome in enumerate(popuation):
            fitnesses[i] = np.sum(self.evaluate_candidate(chromosome))

    def evaluate_fitness_of_population(self):
        self.evaluate_fitnesses(self.pop, self.fitnesses)

    def get_elites(self, limit=None):
        limit = limit or self.NUM_ELITES
        indexes = bn.argpartsort(-self.fitnesses, n=limit)
        return indexes[:limit]

    def get_non_elites(self, limit):
        # get indexes of chromosomes that are not elites
        indexes = bn.argpartsort(-self.fitnesses, n=self.NUM_ELITES)
        num_no_elites = self.NUM_CHROMOSOMES - self.NUM_ELITES
        no_elites = indexes[-num_no_elites:]
        np.random.shuffle(no_elites)
        return no_elites[:limit]

    def get_selection(self):
        if self.SELECT_PROBABILITY:
            # timeit -n10000 np.random.choice(100, (50, 2), replace=False)
            # 10000 loops, best of 3: 61 us per loop
            p = self.fitnesses.astype(np.float32)
            p -= max(0, np.min(p) - 1)
            p /= np.sum(p)
            return np.random.choice(
                self.NUM_CHROMOSOMES, (self.NUM_SELECTED, 2),
                p=p, replace=False)
        else:
            # selects random parents, faster than choice
            # timeit np.random.randint(0, 100, (50, 2))
            # 100000 loops, best of 3: 2.87 us per loop
            return np.random.randint(0, self.NUM_CHROMOSOMES, (self.NUM_SELECTED, 2))

    def show(self, chromosomes=None):
        print "Chromosomes:"
        chromosomes = chromosomes if chromosomes is not None else self.pop
        for i, chromosome in enumerate(chromosomes):
            print i, chromosome, self.fitnesses[i]
        print max(self.fitnesses), 'of', self.num_clauses

    def force_missing(self):
        no_elites = self.get_non_elites(self.NUM_FORCED)
        elites = self.get_elites(self.NUM_FORCED)
        for i, elite in enumerate(elites):
            elite_chromosome = self.pop[elite].copy()
            e = self.evaluate_candidate(elite_chromosome)
            # get unsatisfied clause
            clause = self.clauses[np.where(e == False)[0][0]]
            # need one literal that can be toggled because it is defined
            # first look for such a literal in the negative literals
            select = 0 if np.any(clause[0]) else 1
            one_lit = np.where(clause[select] == True)[0][0]
            elite_chromosome[one_lit] = not elite_chromosome[one_lit]
            self.pop[no_elites[i]] = elite_chromosome
            self.fitnesses[no_elites[i]] = np.sum(self.evaluate_candidate(elite_chromosome))

    def add_random(self, no_elites):
        # replaces last in no_elites
        shape = (self.NUM_NEW_RANDOM, self.num_vars)
        new_random = np.random.choice([True, False], shape)
        index = no_elites[-self.NUM_NEW_RANDOM:]
        self.pop[index] = new_random
        self.fitnesses[index] = np.sum(self.evaluate_candidate(new_random))

    def collect(self):
        self.progress.append(
            {
                'best': np.amax(self.fitnesses),
                'values': self.fitnesses.copy(),
                'mr': self.MUTATION_RATE
            })

    def adapt_mutation_rate_if_needed(self, iteration, std=0):
        #self.MUTATION_RATE = max([self.INI_MUTATION_RATE - 1e-9 * iteration ** 4, 0.2])
        #self.MUTATION_RATE = max([self.INI_MUTATION_RATE - 1e-2 * iteration ** 0.5, 0.2])
        #self.MUTATION_RATE = max([self.MUTATION_RATE - 5e-4 * 10, 0.2])

        #print self.MUTATION_RATE

        diff = 5e-4 * 10
        if std < self.ADAPTION_THRESHOLD:
            self.MUTATION_RATE = min([self.MUTATION_RATE + diff, 0.8])
        else:
            self.MUTATION_RATE = max([self.MUTATION_RATE - diff, 0.2])

    def catastrophe(self, iteration):
        if self.VERBOSE:
            print 'c', 'Catastrophe', np.std(self.fitnesses)
        self.last_catastrophe = iteration
        no_elites = self.get_non_elites(self.NUM_SELECTED)
        shape = (len(no_elites), self.num_vars)
        random = np.random.choice([True, False], shape)
        random_fitnesses = np.zeros(len(no_elites), dtype=np.int)
        self.evaluate_fitnesses(random, random_fitnesses)
        self.pop[no_elites] = random
        self.fitnesses[no_elites] = random_fitnesses

    def catastrophe_if_necessary(self, iteration, std=0):
        diff = iteration - self.last_catastrophe
        if diff < self.CATASTROPHE_BOUNDS[0]:
            pass
        elif diff > self.CATASTROPHE_BOUNDS[1]:
            self.catastrophe(iteration)
        elif std < self.CATASTROPHE_THRESHOLD:
            self.catastrophe(iteration)

    def run(self):
        if self.VERBOSE:
            print "c Population:", self.NUM_CHROMOSOMES
            print "c Selection: ", self.NUM_SELECTED
            print "c Elites:    ", self.NUM_ELITES
            print "c Forced:    ", self.NUM_FORCED

        # for stats
        self.progress = []

        # cannot select individuals when there are not enough or too many elites
        assert(2 * self.NUM_SELECTED < self.NUM_CHROMOSOMES - self.NUM_ELITES)
        # cannot have more forced and random than we have selected
        assert(self.NUM_FORCED + self.NUM_NEW_RANDOM < self.NUM_SELECTED)
        self.evaluate_fitness_of_population()

        offspring = np.zeros((self.NUM_SELECTED, self.num_vars), dtype=np.bool)
        offspring_fitnesses = np.zeros(self.NUM_SELECTED, dtype=np.int)
        for iteration in xrange(self.MAX_ITERATIONS):
            if not (iteration + 1) % self.ADAPT_EVERY:
                if self.MR_ADAPTION or self.CATASTROPHES:
                    std = np.std(self.fitnesses)
                if self.MR_ADAPTION:
                    self.adapt_mutation_rate_if_needed(iteration, std)
                if self.CATASTROPHES:
                    self.catastrophe_if_necessary(iteration, std)

            selection = self.get_selection()
            for i, pair in enumerate(selection):
                offspring[i] = self.crossover(self.pop[pair[0]], self.pop[pair[1]])
            self.mutate_chromosomes(offspring)
            self.evaluate_fitnesses(offspring, offspring_fitnesses)
            no_elites = self.get_non_elites(self.NUM_SELECTED)
            self.pop[no_elites] = offspring
            self.fitnesses[no_elites] = offspring_fitnesses

            if self.num_clauses in self.fitnesses:
                index_of_best = np.where(self.fitnesses == self.num_clauses)[0][0]
                best = self.pop[index_of_best]
                if self.COLLECT_STATS:
                    self.collect()
                return best

            if self.NUM_FORCED:
                self.force_missing()
            if self.NUM_NEW_RANDOM:
                self.add_random(no_elites)

            if self.VERBOSE:
                #print 'c', 'Iteration', iteration
                #print 'c', max(self.fitnesses), 'of', self.num_clauses
                pass
            if self.COLLECT_STATS:
                self.collect()

        return None
