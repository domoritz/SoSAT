import numpy as np
from collections import Counter

def most_constrained_variables(clauses):
    variables = reduce(lambda x, y: x + y, clauses)
    variables = np.absolute(np.array(variables))
    var_counted = sorted(dict(Counter(variables)).items(), key=lambda x: x[1])
    var_counted.reverse()
    return map(lambda x: x[0], var_counted)

def factored_instances(num_vars, clauses, factors):
    variables = most_constrained_variables(clauses)
    instances = [clauses]

    for i in range(factors):
        instances = factor_by_variable(instances, variables[i])
    
    return map(lambda i: preprocess(num_vars, i, []), instances)

def factor_by_variable(instances, variable):
    new_instances = []

    for i in instances:
        new_instances.append(i + [[variable]])
        new_instances.append(i + [[-variable]])

    return new_instances

def preprocess(num_vars, clauses, assumptions):
    for c in clauses:
        if len(c) == 1:
            var = c[0]

            new_clauses = []
            new_assumptions = list(assumptions) + [var]

            for d in clauses:
                if var in d and -var in d:
                    # clause is solved
                    pass
                if -var in d:
                    new_clause = list(d)
                    new_clause.remove(-var)
                    new_clauses.append(new_clause)

                    if len(new_clause) == 0:
                        # instance with these assumptions is unsolvable
                        return False
                    
                elif var in d:
                    # clause is solved
                    pass
                else:
                    new_clauses.append(d)

            return preprocess(num_vars, new_clauses, new_assumptions)

    return reduce_instance(num_vars, clauses, assumptions)

def reduce_instance(num_vars, clauses, assumptions):
    if len(clauses) == 0:
        # no clauses left, already found solution
        return 0, [], assumptions, {}

    mapping = {}
    current_var = 0

    for v in range(1, num_vars + 1):
        if v not in np.abs(np.array(assumptions)) and v in map(lambda x: abs(x), reduce(lambda x, y: x + y, clauses)):
            current_var += 1
            mapping[v] = current_var

    new_clauses = map(lambda c: map(lambda l: np.sign(l) * mapping[abs(l)], c), clauses)
    return current_var, new_clauses, assumptions, mapping

def restore_original_solution(instance, solution, num_vars_orig):
    num_vars, clauses, assumptions, mapping = instance
    inv_mapping = {v:k for k, v in mapping.items()}

    int_solution = []
    for l in range(len(solution)):
        if solution[l]:
            int_solution.append(inv_mapping[l + 1])
        else:
            int_solution.append(-inv_mapping[l + 1])

    int_solution += assumptions
    
    # Add removed variables
    for v in range(1, num_vars_orig + 1):
        if v not in int_solution and -v not in int_solution and v not in assumptions and -v not in assumptions:
            int_solution.append(v)

    return map(lambda l: l > 0, sorted(int_solution, key=lambda l: abs(l)))
