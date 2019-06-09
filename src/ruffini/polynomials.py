from .monomials import Monomial
from collections import Counter, defaultdict
from functools import reduce


class Polynomial:
    def __init__(self, *terms):
        """
        Initialize the polynomial

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> print(p)
        5xy -3yz +a^4b

        This method calculate also the degree of the
        polynomial, the degree for each letter

        >>> p.degree
        5
        >>> p.degrees["z"]
        1

        :param *terms: The terms of the monomial
        :type *terms: list of Monomial
        """

        self.terms = [*terms]
        self.reduce()

        # Add polynomial degrees
        self.degree = max(m.degree for m in self.terms)

        # Calculate the degree for each letter
        self.degrees = {}
        letters = set()
        for m in self.terms: # Find all the letters
            letters |= set(m.degrees.keys())
        for l in letters: # Calculate its degree
            self.degrees[l] = max(m.degrees[l] for m in self.terms)

    ### Utility Method ###

    def reduce(self):
        """
        Sum all the simil monomials, so reduce the polynomial
        """

        variables = [tuple(m.variables) for m in self.terms]

        # Check if there are simil monomial
        if not (len(set(variables)) == len(variables)):

            # If there are some, sum them
            terms_counter = Counter()
            for t in self.terms:
                terms_counter[' '.join(t.variables)] += t.coefficient

            # And rewrite the terms
            self.terms.clear()
            for v in terms_counter:
                self.terms.append(Monomial(terms_counter[v], v.split(" ")))

    ### Operations Methods ###

    def __add__ (self, other):
        if isinstance(other, type(self)):
            return Polynomial(*self.terms, *other.terms)
        elif isinstance(other, Monomial):
            return Polynomial(*self.terms, other)

    def __sub__ (self, other):
        if isinstance(other, type(self)):
            other = list(map(lambda m: -m, other))
            return Polynomial(*self.terms, *other)
        elif isinstance(other, Monomial):
            return Polynomial(*self.terms, -other)

    ### Magic Methods ###

    def __str__(self):
        """
        Return the polynomial as a string
        """
        result = str(self.terms[0])
        for t in self.terms[1:]:
            if t.coefficient > 0:
                result += f" +{t}"
            elif t.coefficient < 0:
                result += f" {str(t)}"
        return result

    def __iter__ (self):
        """
        Return the iterator for the polynomial.
        The iteration will iter over the polynomial's
        terms. As a magic method, you can access it
        calling the iter() function with the polynomial
        as argument
        
        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> i = iter(p)
        >>> # see __next__ for the next part
        """
        self._iter_n = -1
        return self

    def __next__ (self):
        """
        The next magic method (to use with iter)
        returns the next terms of the polynomials
        itered. When it's finished, it raise StopIteration
        
        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> i = iter(p)
        >>> print(next(i))
        5xy
        >>> print(next(i))
        -3yz
        >>> print(next(i))
        a^4b
        >>> next(i) # no more terms
        Traceback (most recent call last):
        ...
        StopIteration
        """

        self._iter_n += 1
        if self._iter_n <= len(self.terms) -1:
            return self.terms[self._iter_n]
        else:
            raise StopIteration
