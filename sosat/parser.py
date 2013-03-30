TESTING = True

def parse(f):
    # Parser for DIMACS format
    num_vars = 0
    clauses = []
    for line in f:
        pline = line.split()
        if pline[0] != 'c':
            if pline[0] == 'p':
                assert pline[1] == 'cnf'
                num_vars = int(pline[2])
            else:
                clauses.append(map(int, pline)[:-1])
    return num_vars, clauses

