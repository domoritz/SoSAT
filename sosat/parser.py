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


def parse_cse573(f):
    num_vars = 0
    clauses = []
    mapping = {}

    for line in f:
        pline = line.strip().split(' ')
        clause = []
        for lit in pline:
            lit = lit.strip()
            neg = lit.startswith('!')
            if neg:
                lit = lit[1:]
            if lit not in mapping:
                mapping[lit] = num_vars + 1
                num_vars += 1
            clause.append((-1 if neg else 1) * mapping[lit])
        clauses.append(clause)

    return num_vars, clauses, {v: k for k, v in mapping.items()}
