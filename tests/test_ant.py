import unittest
from nose.tools import assert_equal

import sosat.ant.algorithm as aa


class TestSequenceFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.num_vars = 20
        cls.clauses = [[10, 12, 15, 5, 3], [6, 13, 14, -11, 20]]

    def test_initialization(self):
        a = aa.AntColonyAlgorithm(self.num_vars, self.clauses)
