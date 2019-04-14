from .monomials import Monomial
from collections import Counter

class Polynomial:
    def __init__(self, *monomials):
        """
        Initialize the polynomial
        """
        self.terms = list(monomials)
        self.reduce()

    def reduce(self):
        """
        Sum all the simil monomials
        """
        old_terms = self.terms.deepcopy()
        self.terms.clear()

        # Make a counter and sum simil monomials
        counter = Counter()
        var_to_list = {}
        for term in old_terms:
            counter[term.variables_str()] += term.coefficient

        # Create new monomials from the sums
        for var in counter:
            self.terms.append(Monomial(counter[var], var_to_list[var]))

        # Add polynomial degree
        self.degree = max(term.degree for term in self.terms)
