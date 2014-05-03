import unittest
from nose.tools import assert_equal
from nose.tools import raises

import sosat.parser as parser


class TestSequenceFunctions(unittest.TestCase):
    def test_parse_simple_file(self):
        parsed = parser.parse(['c foo bar', 'p cnf 20 2', '10 12 15 5 3 0', '6 13 14 -11 20 0'])
        assert_equal(parsed, (20, [[10, 12, 15, 5, 3], [6, 13, 14, -11, 20]]))

    @raises(AssertionError)
    def test_knf(self):
        parser.parse(['p knf 20 0'])

    def test_cse573(self):
        data = ['ParentOf(Tom,Jill)',
                '!ParentOf(Frank,Frank) Ancestor(Frank,Frank) !ParentOf(Tom,Jill)']
        parsed = parser.parse_cse573(data)
        assert_equal(parsed, (3, [[1], [-2, 3, -1]],
                     {1: 'ParentOf(Tom,Jill)', 2: 'ParentOf(Frank,Frank)', 3: 'Ancestor(Frank,Frank)'}))


if __name__ == '__main__':
    unittest.main()
