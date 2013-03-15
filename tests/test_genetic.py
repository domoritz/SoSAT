import unittest
import numpy as np
from nose.tools import assert_equal

import sosat.genetic.algorithm as ga


class TestSequenceFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.num_vars = 20
        cls.clauses = [[10, 12, 15, 5, 3], [6, 13, 14, -11, 20]]

    def test_initialization(self):
        a = ga.GeneticAlgorithm(self.num_vars, self.clauses)
        assert_equal(a.pop.shape, (a.NUM_CHROMOSOMES, self.num_vars))

    def test_evaluate(self):
        a = ga.GeneticAlgorithm(4, [[-1, 2, -4], [1, 2]])
        r = np.zeros(1)
        a.evaluate_fitnesses(np.array([[True, True, False, False]]), r)
        assert_equal(r[0], 2)

    def test_evaluate_pop(self):
        a = ga.GeneticAlgorithm(self.num_vars, self.clauses, {'NUM_CHROMOSOMES': 22})
        a.evaluate_fitness_of_population()
        assert_equal(len(a.fitnesses), 22)

    def test_crossover(self):
        a = ga.GeneticAlgorithm(3)
        for x in range(5):
            r = a.crossover(np.array([1, 1, 1]), np.array([2, 2, 2]))
            assert list(r) in [[1, 1, 1], [1, 1, 2], [1, 2, 2], [2, 2, 2]]

    def test_run(self):
        a = ga.GeneticAlgorithm(self.num_vars, self.clauses)
        a.run()

if __name__ == '__main__':
    unittest.main()
