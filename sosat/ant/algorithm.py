import numpy as np

class AntColonyAlgorithm(object):
   SEED = 42
   PH_MAX = 10.0              # range: (0, inf)
   NUM_ANTS = 5               # range: [1, inf)
   EXP_PH = 1                 # range: (-inf, inf)
   EXP_MCV = 1                # range: (-inf, inf)
   CHOOSE_ALLOW_CONTRADICTIONS = True
   PH_REDUCE_FACTOR = 0.15    # range: (0, 1)

   def __init__(self, num_vars=0, clauses=[]):
      self.num_vars = num_vars
      self.clauses = clauses
      print num_vars, clauses

      np.random.seed(self.SEED)

      self.initialize_pheromones()
      self.initialize_mcv_heuristic()
      self.initialize_probabilities()

   def initialize_mcv_heuristic(self):
      '''
      Most Constrained Variable (MCV) heuristic: variables that appear in most
      clauses are more important and visited more often.
      '''
      self.mcv = np.ndarray((2*self.num_vars), int)
      self.mcv.fill(1)

   def initialize_pheromones(self):
      '''
      All pheromone values are initialized to PH_MAX.
      '''
      self.pheromones = np.ndarray((2*self.num_vars), float)
      self.pheromones.fill(PH_MAX)

   def initialize_probabilities(self):
      self.probabilites = np.ndarray((2*self.num_vars), float)
      self.update_probabilities()

   def update_probabilities(self):
      self.probabilites = self.pheromones**EXP_PH * self.mcv**EXP_MCV

   def choose_nodes(self):
      nodes = np.copy(this.pheromones)
      chosen = np.ndarray((self.num_vars))

      for i in range(self.num_vars):
         cumulated = np.cumsum(nodes)
         chosen[i] = np.searchsorted(cumulated, np.random.rand()*cumulated[-1])
         nodes[i] = 0.0

         if !self.CHOOSE_ALLOW_CONTRADICTIONS:
            nodes[(i/2)*2] = 0.0
            nodes[(i/2)*2+1] = 0.0
      
      return chosen     

   def update_pheromones(self, chosen_nodes):
      # reduce pheromones
      self.pheromones = self.pheromones * (1.0-PH_REDUCE_FACTOR)
      # increase pheromones
