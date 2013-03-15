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

    def test_mutate(self):
        arr = np.array([True, False, True], dtype=np.bool)
        arr = arr.reshape(3, 1)
        copy = arr.copy()
        a = ga.GeneticAlgorithm(1)
        a.mutate_chromosomes(arr)

        vecfunc = np.vectorize(lambda x: not x)
        expected = vecfunc(copy)
        assert_equal(list(arr), list(expected))

    def test_evaluate_pop(self):
        a = ga.GeneticAlgorithm(self.num_vars, self.clauses)
        a.evaluate_fitness_of_population()

    def test_crossover(self):
        a = ga.GeneticAlgorithm(3)
        for x in range(5):
            r = a.crossover([1, 1, 1], [2, 2, 2])
            assert r in [[1, 1, 1], [1, 1, 2], [1, 2, 2], [2, 2, 2]]

if __name__ == '__main__':
    unittest.main()
