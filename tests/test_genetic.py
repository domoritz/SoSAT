import unittest
import numpy as np
import numexpr as ne
from nose.tools import assert_equal

import sosat.genetic as ga


class TestSequenceFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.num_vars = 20
        cls.clauses = [[10, 12, 15, 5, 3, 0], [6, 13, 14, -11, 20, 0]]

    def test_initialization(self):
        a = ga.Algorithm(self.num_vars, self.clauses)
        assert_equal(a.num_vars, self.num_vars)
        assert_equal(a.clauses, self.clauses)
        assert_equal(a.pop.shape, (20, a.NUM_CHROMOSOMES))

    def test_mutate(self):
        arr = np.array([True, False, True], dtype=np.bool)
        arr = arr.reshape(3, 1)
        copy = arr.copy()
        a = ga.Algorithm(1)
        a.mutate_chromosomes(arr)

        vecfunc = np.vectorize(lambda x: not x)
        expected = vecfunc(copy)
        for i in range(len(arr)):
            assert_equal(arr[i], expected[i])

if __name__ == '__main__':
    unittest.main()
