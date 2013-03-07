

class GeneticAlgorithm(object):
    def __init__(self, num_vars, clauses):
        self.num_vars = num_vars
        self.clauses = clauses
        print num_vars, clauses

    def run(self):
        print "run"
