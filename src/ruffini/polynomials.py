from .monomials import Monomial
from collections import Counter, defaultdict
from functools import reduce


class Polynomial:
    def __init__(self, *monomials):
        """
        Initialize the polynomial
        """

        self.terms = list(monomials)
        self.reduce()

        # Add polynomial degrees
        self.degree = max(m.degree for m in self.terms)
        self.degrees = {}

        # Calculate it for each letter
        letters = set()
        for m in self.terms:
            letters |= set(m.degrees.keys())
        for l in letters:
            self.degrees[l] = max(m.degrees[l] for m in self.terms)

        self.ishomogeneous = all(
            self.terms[0].degree == m.degree for m in self.terms)

    def reduce(self):
        """
        Sum all the simil monomials
        """

        # Make a counter and sum simil monomials
        counter = Counter()
        for m in self.terms:
            counter[" ".join(m.variables)] += m.coefficient

        # Create new monomials from the sums
        self.terms.clear()
        for var in counter:
            self.terms.append(Monomial(counter[var],
                                       var.split(" ")))

    def __str__(self):
        """
        Return the polynomial as a string
        """
        return "".join(str(m) for m in self.terms)
