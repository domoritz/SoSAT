TESTING = True


def parse(f):
    """
    >>> parse(['c foo bar', 'p cnf 20 2', '10 12 15 5 3 0', '6 13 14 -11 20 0'])
    (20, [[10, 12, 15, 5, 3, 0], [6, 13, 14, -11, 20, 0]])
    >>> parse(['p knf 20 0'])
    Traceback (most recent call last):
    ...
        assert pline[1] == 'cnf'
    AssertionError
    """
    num_vars = 0
    clauses = []
    for line in f:
        pline = line.split()
        if pline[0] != 'c':
            if pline[0] == 'p':
                assert pline[1] == 'cnf'
                num_vars = int(pline[2])
            else:
                clauses.append(map(int, pline))
    return num_vars, clauses


if __name__ == '__main__':
    if TESTING:
        import doctest
        doctest.testmod()
    else:
        with open('instances/random_ksat0.dimacs') as f:
            print parse(f)
