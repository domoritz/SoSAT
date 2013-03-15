import numba as nb
import numpy as np

NUM_ANTS = 25000                 # range: [1, inf)
EXP_PH = 1                     # range: (-inf, inf)
EXP_MCV = 1                    # range: (-inf, inf)
PH_REDUCE_FACTOR = 0.15     # range: (0, 1)
MAX_ITERATIONS = 10000
BLUR_ITERATIONS = 3
BLUR_BASIC = 0.9
BLUR_DECLINE = 50.0
WEIGHT_ADAPTION_DURATION = 250
SEED = 42

def initialize_clauses(num_vars, raw_clauses):
    num_clauses = len(raw_clauses)
    shape = (num_clauses, 2, num_vars)
    clauses = np.zeros(dtype=np.bool, shape=shape)
    for i, clause in enumerate(raw_clauses):
        for lit in clause:
            if lit > 0: 
                clauses[i][0][lit - 1] = True
            else:
                clauses[i][1][-lit - 1] = True

    return clauses

def update_probabilities(mcv, pheromones):
    return pheromones**EXP_PH * mcv**EXP_MCV

def debug_me(num):
    print "DEBUG: ", num
    
def choose_nodes(num_vars, pheromones):
    normalization_vector = np.sum(pheromones, axis=0) ** -1
    chosen = np.random.rand(num_vars) < normalization_vector * pheromones[0]
    return chosen

@nb.jit(nb.bool_[:,:](nb.bool_[:]))
def full_candidate(candidate):
    return np.array([candidate, ~candidate])

@nb.autojit
def update_pheromones(chosen, evaluation, pheromones, PH_MIN, PH_MAX):
    pheromones = pheromones * (1.0 - PH_REDUCE_FACTOR) + full_candidate(chosen) * evaluation
    pheromones = update_pheromones_bounds(pheromones, PH_MIN, PH_MAX)
    return pheromones

def update_pheromones_bounds(pheromones, PH_MIN, PH_MAX):
    pheromones[pheromones < PH_MIN] = PH_MIN
    pheromones[pheromones > PH_MAX] = PH_MAX
    return pheromones

def print_me(obj):
    print obj

@nb.jit(nb.int_(nb.int_, nb.int_[:,:]), 
    locals = dict(
        evaluation = nb.double, 
        best_evaluation = nb.double, 
        num_vars = nb.int_,
        num_lits = nb.int_,
        candidate_counter = nb.int_,
        clauses = nb.bool_[:,:,:],
        int_clauses = nb.int_[:,:,:],
        PH_MIN = nb.double,
        PH_MAX = nb.double,
        clause_weights = nb.double[:],
        mcv = nb.int_[:],
        pheromones = nb.double[:,:],
        best_solution = nb.bool_[:,:],
        solved_clauses = nb.double[:,:],
        num_solved_clauses = nb.int_,
        best_solved = nb.int_,
        nodes = nb.bool_[:,:],
        probabilites = nb.double[:,:],
        max_divergence = nb.double
        ))
def run(p_num_vars=0, raw_clauses=[]):
    num_vars = p_num_vars
    num_lits = 2 * num_vars
    candidate_counter = 0
    clauses = initialize_clauses(num_vars, raw_clauses)
    int_clauses = clauses.astype(int)
    PH_MAX = num_vars / (1.0 - PH_REDUCE_FACTOR) 
    PH_MIN = PH_MAX / num_lits
    clause_weights = np.ones(len(clauses))
    mcv = np.sum(int_clauses, axis=0)
    pheromones = np.ndarray((2, num_vars), float)
    pheromones.fill(PH_MAX)
    #print_me(pheromones)
    
    probabilities = update_probabilities(mcv, pheromones)
     
    for i in range(MAX_ITERATIONS):
        best_solution = np.array([[True]])   # should be None
        best_evaluation = -1.0
        best_solved = 0.0
        evaluation = 0.0
        print NUM_ANTS
    
        for a in range(NUM_ANTS):
            nodes = choose_nodes(num_vars, probabilities)
 
            candidate_counter += 1
            solved_clauses = np.any(clauses & np.array([nodes, ~nodes]), axis=(2, 1))
            num_solved_clauses = np.sum(solved_clauses)
            evaluation = np.sum(solved_clauses * clause_weights)

            if candidate_counter == WEIGHT_ADAPTION_DURATION:
                clause_weights += ~solved_clauses 
                candidate_counter = 0

            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_solution = nodes
                best_solved = num_solved_clauses

            if float(num_solved_clauses) == float(len(clauses)):
                pass
                print "DONE: " #, nodes
                return 0
        
#        print "Solution: ", best_solution, best_evaluation, best_solved, "/", len(clauses)
        pheromones = update_pheromones(best_solution, evaluation, pheromones, PH_MIN, PH_MAX)
#        print_me(best_solved)
        #print_me(pheromones)
        probabilities = update_probabilities(mcv, pheromones)
        #print_me(probabilities)
          
        if i > 0 and i % BLUR_ITERATIONS == 0:
            max_divergence = BLUR_BASIC * np.e**(-i/BLUR_DECLINE)
            pheromones += pheromones * (np.random.rand(2, num_vars) * max_divergence * 2 - max_divergence)
            pheromones = update_pheromones_bounds(pheromones, PH_MIN, PH_MAX)
            probabilities = update_probabilities(mcv, pheromones)
    
    return 1

def run_ant(p_num_vars=0, raw_clauses=[]):
    np.random.seed(SEED)
    run(p_num_vars, raw_clauses)
