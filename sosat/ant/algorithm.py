import numpy as np
import sosat.algorithm as algo


class AntColonyAlgorithm(algo.Algorithm):
    NUM_ANTS = 250                 # range: [1, inf)
    EXP_PH = 1                     # range: (-inf, inf)
    EXP_MCV = 1                    # range: (-inf, inf)
    PH_REDUCE_FACTOR = 0.15     # range: (0, 1)
    MAX_ITERATIONS = 10000
    BLUR_ITERATIONS = 3
    BLUR_BASIC = 0.9
    BLUR_DECLINE = 50.0
    WEIGHT_ADAPTION_DURATION = 250

    def __init__(self, num_vars=0, clauses=[], config={}):
        # clause form: [-x1, x1, -x2, x2, -x3, x3, ...] (0/1)
        super(AntColonyAlgorithm, self).__init__(num_vars, clauses, config)
        print self.raw_clauses

        self.initialize_constants()
        self.initialize_variables()
        self.initialize_clause_weights()
        self.initialize_pheromones()
        self.initialize_mcv_heuristic()
        self.initialize_probabilities()

    def initialize_clauses(self):
        super(AntColonyAlgorithm, self).initialize_clauses()
        self.int_clauses = self.clauses.astype(int)

    def initialize_variables(self):
        self.candidate_counter = 0

    def initialize_constants(self):
        self.PH_MAX = self.num_vars / (1.0 - self.PH_REDUCE_FACTOR)
        self.PH_MIN = self.PH_MAX / self.num_lits
        print "PH_MIN: ", self.PH_MIN, ", PH_MAX: ", self.PH_MAX

    def initialize_clause_weights(self):
        self.clause_weights = np.ones(len(self.clauses))

    def initialize_mcv_heuristic(self):
        '''
        Most Constrained Variable (MCV) heuristic: variables that appear in most
        clauses are more important and visited more often.
        '''
        self.mcv = np.sum(self.int_clauses, axis=0)
        print "init mcv: ", self.mcv

    def initialize_pheromones(self):
        '''
        All pheromone values are initialized to PH_MAX.
        '''
        self.pheromones = np.ndarray((2, self.num_vars), float)
        self.pheromones.fill(self.PH_MAX)

    def initialize_probabilities(self):
        self.probabilities = np.ndarray((2, self.num_vars), float)
        self.update_probabilities()

    def update_probabilities(self):
        self.probabilities = self.pheromones**self.EXP_PH * self.mcv**self.EXP_MCV

    def choose_nodes(self):
        normalization_vector = np.sum(self.pheromones, axis=0) ** -1
        chosen = np.random.rand(self.num_vars) < normalization_vector * self.pheromones[0]
        return chosen

    def evaluate_solution(self, chosen):
        self.candidate_counter += 1

        solved_clauses = self.evaluate_candidate(chosen)
        num_solved_clauses = np.sum(solved_clauses)
        evaluation = np.sum(solved_clauses * self.clause_weights)

        if self.candidate_counter == self.WEIGHT_ADAPTION_DURATION:
            self.clause_weights += ~solved_clauses
            self.candidate_counter = 0

        #print "evaluation: ", chosen_nodes, evaluation, solved_clauses
        return evaluation, num_solved_clauses

    def update_pheromones(self, chosen, evaluation):
        self.pheromones = self.pheromones * (1.0 - self.PH_REDUCE_FACTOR) + self.full_candidate(chosen) * evaluation
        self.update_pheromones_bounds()

    def update_pheromones_bounds(self):
        self.pheromones[self.pheromones < self.PH_MIN] = self.PH_MIN
        self.pheromones[self.pheromones > self.PH_MAX] = self.PH_MAX

    def blur_pheromones(self, max_divergence):
        self.pheromones += self.pheromones * (np.random.rand(2, self.num_vars) * max_divergence * 2 - max_divergence)
        self.update_pheromones_bounds()
        self.update_probabilities()
        #print "BLUR: ", max_divergence, self.pheromones

    def run(self):
        for i in range(self.MAX_ITERATIONS):
            best_solution = None
            best_evaluation = -1
            best_solved = 0

            for a in range(self.NUM_ANTS):
                nodes = self.choose_nodes()
                evaluation, solved_clauses = self.evaluate_solution(nodes)

                if evaluation > best_evaluation:
                    best_evaluation = evaluation
                    best_solution = nodes
                    best_solved = solved_clauses

                if solved_clauses == self.num_clauses:
                    print "DONE: ", nodes
                    exit()

            #print "Solution: ", best_solution, best_evaluation, best_solved, "/", len(self.clauses)

            self.update_pheromones(best_solution, evaluation)
            #print "Pheromones: ", self.pheromones
            self.update_probabilities()
            #print "Probablilities: ", self.probabilities

            if i > 0 and i % self.BLUR_ITERATIONS == 0:
                self.blur_pheromones(self.BLUR_BASIC * np.e**(-i/self.BLUR_DECLINE))

