import unittest
import numpy as np
from nose.tools import assert_equal

import sosat.algorithm as algo


class TestSequenceFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.num_vars = 20
        cls.clauses = [[10, 12, 15, 5, 3], [6, 13, 14, -11, 20]]

    def test_initialization(self):
        a = algo.Algorithm(self.num_vars, self.clauses)
        assert_equal(a.num_vars, self.num_vars)
        assert_equal(a.raw_clauses, self.clauses)
        assert_equal(a.SEED, 42)

    def test_config(self):
        a = algo.Algorithm(self.num_vars, self.clauses, {'SEED': 64})
        assert_equal(a.SEED, 64)

    def test_clause_creation(self):
        a = algo.Algorithm(4, [[-1, 2, -4]])
        exp = [[False, True, False, False], [True, False, False, True]]
        assert_equal(list(a.clauses[0][0]), exp[0])
        assert_equal(list(a.clauses[0][1]), exp[1])

    def test_evaluate_candidate(self):
        a = algo.Algorithm(4, [[-1, 2, -4], [1, 2]])
        r = a.evaluate_candidate(np.array([True, True, False, False]))
        assert_equal(list(r), [True, True])

        r = a.evaluate_candidate(np.array([False, False, True, False]))
        assert_equal(list(r), [True, False])

        r = a.evaluate_candidate(np.array([True, False, True, True]))
        assert_equal(list(r), [False, True])
