import unittest
from nose.tools import assert_equal

import sosat.genetic.algorithm as ga


class TestSequenceFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.num_vars = 20
        cls.clauses = [[10, 12, 15, 5, 3, 0], [6, 13, 14, -11, 20, 0]]

    def test_initialization(self):
        a = ga.GeneticAlgorithm(self.num_vars, self.clauses)
        assert_equal(a.num_vars, self.num_vars)
        assert_equal(a.clauses, self.clauses)

if __name__ == '__main__':
    unittest.main()
