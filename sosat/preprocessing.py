import numpy as np
from collections import Counter

def most_constrained_variables(clauses):
    """
    Sorts variables by constrainedness, i.e. how often the variable is mentioned in all clauses.
    """
    variables = reduce(lambda x, y: x + y, clauses)
    variables = np.absolute(np.array(variables))
    var_counted = sorted(dict(Counter(variables)).items(), key=lambda x: x[1])
    var_counted.reverse()
    return map(lambda x: x[0], var_counted)

def factored_instances(num_vars, clauses, factors):
    """
    Factors the instance {factores} times by the next most constrained variable.
    """
    variables = most_constrained_variables(clauses)
    instances = [clauses]

    for i in range(factors):
        instances = factor_by_variable(instances, variables[i])
    
    return map(lambda i: preprocess(num_vars, i, []), instances)

def factor_by_variable(instances, variable):
    """
    Factors a list of instances by a variable. Generates two new instances for every instance, with [{variable}] and [-{variable}] as new clauses.
    """
    new_instances = []

    for i in instances:
        new_instances.append(i + [[variable]])
        new_instances.append(i + [[-variable]])

    return new_instances

def preprocess(num_vars, clauses, assumptions):
    """
    Preprocesses an instance. Recursively removes clauses with one literal and removes variables not constrained anymore.
    """
    for c in clauses:
        if len(c) == 1:
            # found a clause consisting of only one literal
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

            # recursively continue processing until no clause can be removed
            return preprocess(num_vars, new_clauses, new_assumptions)

    # remove unconstrained variables
    return reduce_instance(num_vars, clauses, assumptions)

def reduce_instance(num_vars, clauses, assumptions):
    """
    Removes unconstrained variables that aren't used in any clause.
    """
    if len(clauses) == 0:
        # no clauses left, already found solution
        return 0, [], assumptions, {}

    mapping = {}
    current_var = 0

    for v in range(1, num_vars + 1):
        if (
            # variable is not used in assumptions and...
            v not in np.abs(np.array(assumptions)) and
             # ... variable is constrained
            v in map(lambda x: abs(x), reduce(lambda x, y: x + y, clauses))):
                # keep variable in the reduced instance
                current_var += 1
                mapping[v] = current_var

    # modify clauses according to variable mapping
    new_clauses = map(lambda c: map(lambda l: np.sign(l) * mapping[abs(l)], c), clauses)
    return current_var, new_clauses, assumptions, mapping

def restore_original_solution(instance, solution, num_vars_orig):
    """
    Applies inverse variable mapping to solution and adds assumptions.
    """
    num_vars, clauses, assumptions, mapping = instance
    inv_mapping = {v:k for k, v in mapping.items()}

    int_solution = []
    # apply inverse mapping
    for l in range(len(solution)):
        if solution[l]:
            int_solution.append(inv_mapping[l + 1])
        else:
            int_solution.append(-inv_mapping[l + 1])

    # add assumptions
    int_solution += assumptions
    
    # add removed (unconstrained) variables
    for v in range(1, num_vars_orig + 1):
        if v not in int_solution and -v not in int_solution and v not in assumptions and -v not in assumptions:
            # variable was not part of the solution and no assumption
            int_solution.append(v)
    
    # sort and convert to boolean arrary
    return map(lambda l: l > 0, sorted(int_solution, key=lambda l: abs(l)))

