import numpy as np

class AntColonyAlgorithm(object):
   SEED = 42
   NUM_ANTS = 1000             # range: [1, inf)
   EXP_PH = 1                 # range: (-inf, inf)
   EXP_MCV = 1                # range: (-inf, inf)
   CHOOSE_ALLOW_CONTRADICTIONS = False
   PH_REDUCE_FACTOR = 0.1    # range: (0, 1)
   MAX_ITERATIONS = 10000
   WEIGHT_ADAPTION_DURATION = 250

   def __init__(self, num_vars=0, clauses=[]):
      # clause form: [-x1, x1, -x2, x2, -x3, x3, ...] (0/1)
      self.num_vars = num_vars
      print "num_vars: ", num_vars

      self.initialize_instance(clauses)
      self.initialize_constants()
      self.initialize_variables()
      self.initialize_clause_weights()
      self.initialize_pheromones()
      self.initialize_mcv_heuristic()
      self.initialize_probabilities()

   def initialize_variables(self):
      self.solution_counter = 0

   def initialize_constants(self):
      np.random.seed(self.SEED)
      self.PH_MAX = self.num_vars / (1.0-self.PH_REDUCE_FACTOR)
      self.PH_MIN = self.PH_MAX / (2*self.num_vars)
      print "PH_MIN: ", self.PH_MIN, ", PH_MAX: ", self.PH_MAX

   def initialize_instance(self, clauses):
      self.clauses = []

      for c in clauses:
         clause = np.ndarray((2*self.num_vars), int)
         clause.fill(0)
         
         for literal in c:
            clause[(abs(literal)-1)*2 + min(1, np.sign(literal)+1)] = 1
         
         print "clause: ", clause 
         self.clauses += [clause]

   def initialize_clause_weights(self):
      self.clause_weights = np.ndarray((len(self.clauses)), float)
      self.clause_weights.fill(1.0)

   def initialize_mcv_heuristic(self):
      '''
      Most Constrained Variable (MCV) heuristic: variables that appear in most
      clauses are more important and visited more often.
      '''
      self.mcv = np.ndarray((2*self.num_vars), int)
      self.mcv.fill(0)

      for c in self.clauses:
         self.mcv += c

      print "init mcv: ", self.mcv

   def initialize_pheromones(self):
      '''
      All pheromone values are initialized to PH_MAX.
      '''
      self.pheromones = np.ndarray((2*self.num_vars), float)
      self.pheromones.fill(self.PH_MAX)

   def initialize_probabilities(self):
      self.probabilities = np.ndarray((2*self.num_vars), float)
      self.update_probabilities()

   def update_probabilities(self):
      self.probabilities = self.pheromones**self.EXP_PH * self.mcv**self.EXP_MCV

   def choose_nodes(self):
      #print "Choosing..."

      nodes = np.copy(self.pheromones)
      chosen = np.ndarray((2*self.num_vars), int)
      chosen.fill(0)

      for i in range(self.num_vars):
         cumulated = np.cumsum(nodes)
         next_var = np.searchsorted(cumulated, np.random.rand()*cumulated[-1])
         #print "next_var: ", next_var
         chosen[next_var] = 1

         if not self.CHOOSE_ALLOW_CONTRADICTIONS:
            #print "Forbidding ", next_var/2*2, next_var/2*2+1
            nodes[(next_var/2)*2] = 0.0
            nodes[(next_var/2)*2+1] = 0.0
         else:
            nodes[next_var] = 0.0
      
      return chosen     

   def update_clause_weights(self, chosen_nodes):
      self.clause_weights += 1.0
      self.clause_weights 

   def evaluate_solution(self, chosen_nodes):
      evaluation = 0
      solved_clauses = 0
       
      for c_idx in range(len(self.clauses)):
         if not -1 in chosen_nodes-self.clauses[c_idx]:
            evaluation += self.clause_weights[c_idx]
            solved_clauses += 1
         elif self.solution_counter == self.WEIGHT_ADAPTION_DURATION:
            self.clause_weights[c_idx] += 1

      if self.solution_counter == self.WEIGHT_ADAPTION_DURATION:
         self.solution_counter = 0
      
      self.solution_counter += 1

      return evaluation, solved_clauses

   def update_pheromones(self, chosen_nodes, evaluation):
      self.pheromones = self.pheromones * (1.0-self.PH_REDUCE_FACTOR) + chosen_nodes*evaluation
      self.pheromones[self.pheromones < self.PH_MIN] = self.PH_MIN
      self.pheromones[self.pheromones > self.PH_MAX] = self.PH_MAX

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

            if solved_clauses == len(self.clauses):
               print "DONE: ", nodes
               exit()

         print "Solution: ", best_solution, best_evaluation, best_solved, "/", len(self.clauses)

         self.update_pheromones(best_solution, evaluation)
         print "Pheromones: ", self.pheromones
         self.update_probabilities()
         print "Probablilities: ", self.probabilities



