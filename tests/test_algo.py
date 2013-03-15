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

    def test_clause_creation(self):
        a = algo.Algorithm(4, [[-1, 2, -4]])
        exp = [[False, True, False, False], [True, False, False, True]]
        assert_equal(list(a.clauses[0][0]), exp[0])
        assert_equal(list(a.clauses[0][1]), exp[1])
