import unittest
import numpy as np
from nose.tools import assert_equal

import sosat.genetic as ga


class TestSequenceFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.num_vars = 20
        cls.clauses = [[10, 12, 15, 5, 3], [6, 13, 14, -11, 20]]

    def test_initialization(self):
        a = ga.Algorithm(self.num_vars, self.clauses)
        assert_equal(a.pop.shape, (20, a.NUM_CHROMOSOMES))

    def test_mutate(self):
        arr = np.array([True, False, True], dtype=np.bool)
        arr = arr.reshape(3, 1)
        copy = arr.copy()
        a = ga.Algorithm(1)
        a.mutate_chromosomes(arr)

        vecfunc = np.vectorize(lambda x: not x)
        expected = vecfunc(copy)
        assert_equal(list(arr), list(expected))

if __name__ == '__main__':
    unittest.main()
