from .monomials import Monomial
from collections import Counter


class Polynomial:
    def __init__(self, *terms):
        """
        Initialize the polynomial

        This method calculate also the degree of the
        polynomial and the degree for each letter

        :param *terms: Terms of the polynomial
        :type *terms: Monomials
        :raise: TypeError
        """

        self.terms = [*terms]
        self.__reduce()

        # Add polynomial degree
        self.degree = max(m.degree for m in self.terms)

        # Calculate the degree for each letter
        self.variables = {}
        letters = set()
        for term in self.terms:  # Find all the letters
            letters |= set(list(term.variables))
        for letter in letters:  # Calculate its degree
            self.variables[letter] = max(
                term.variables[letter] for term in self.terms)

    ### Utility Methods ###

    def __reduce(self):
        """
        Sum all the simil monomials, so reduce
        the polynomial.
        It is automatically called when the
        polynomial is initialized.
        """

        # If there are some, sum them
        counter = Counter()
        for term in self.terms:
            counter[term.variables] += term.coefficient

        # And rewrite the terms
        self.terms.clear()
        for variables, coefficient in counter.items():
            self.terms.append(Monomial(coefficient, variables))

    # Operations Methods ###

    def __add__(self, other):
        """
        Add a polynomial with
        - another polynomial
        - a monomial
        - an integer / a float

        :type other: Monomial, Polynomial, int, float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other)

        if isinstance(other, Polynomial):
            return Polynomial(*self.terms, *other.terms)
        elif isinstance(other, Monomial):
            return Polynomial(*self.terms, other)
        else TypeError:
            return NotImplemented

    def __sub__(self, other):
        """
        Subtract from a polynomial:
        - another polynomial
        - a monomial
        - an integer / a float

        :type other: Monomial, Polynomial, int, float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        if isinstance(other, Polynomial):
            return Polynomial(*self.terms, *(-other))
        elif isinstance(other, Monomial):
            return Polynomial(*self.terms, -other)
        else TypeError:
            return NotImplemented

    def __mul__(self, other):
        """
        Multiply two polynomials, a polynomial and a
        monomial or a polynomial and a number (int/float)

        :type other: Monomial, Polynomial, int or float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        if isinstance(other, (Monomial, int, float)):
            return Polynomial(*(t*other for t in self.terms))
        elif isinstance(other, Polynomial):
            return Polynomial(*(a*b for a in self.terms for b in other.terms))
        else TypeError:
            return NotImplemented

    def __radd__(self, other):
        """
        Add a polynomial to a monomial or to a number
        (int / float).

        :type other: Monomial, int, float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        try:
            return self.__add__(other)
        except TypeError:
            return NotImplemented

    def __rsub__(self, other):
        """
        Subtract a monomial or a number (int / float)
        from a polynomial

        :type other: Monomial, int, float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        try:
            return (-self).__add__(other)
        except TypeError:
            return NotImplemented

    def __rmul__(self, other):
        """
        Multiply a polynomial for a monomial
        or a number (int / float).

        :type other: Monomial, int, float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        try:
            return self.__mul__(other)
        except TypeError:
            return NotImplemented

    ### Magic Methods ###

    def __str__(self):
        """
        Return the polynomial as a string, adding
        a space between each term

        """
        result = str(self.terms[0])
        for term in self.terms[1:]:
            if term.coefficient > 0:
                result += f" +{term}"
            elif term.coefficient < 0:
                result += f" {term}"
        return result

    def __iter__(self):
        """
        Return the iterator for the polynomial.
        The iteration will iter over the polynomial's
        terms. As a magic method, you can access it
        calling the iter() function with the polynomial
        as argument
        """
        self.__iter_n = -1
        return self

    def __next__(self):
        """
        The next magic method (to use with iter)
        returns the next terms of the polynomials
        itered. When it's finished, it raise StopIteration
        """

        self.__iter_n += 1
        if self.__iter_n <= len(self.terms) - 1:
            return self.terms[self.__iter_n]
        else:
            raise StopIteration

    def __getitem__(self, key):
        """
        Enable the indexing of polynomial's terms.
        Also negative indexing is enabled

        :raise: IndexError, TypeError
        """
        return self.terms[key]

    def __eq__(self, other):
        """
        Check if two polynomials are equivalent,
        comparating each term

        If a polynomial has a single term, it can
        also be compared to a monomial

        Otherwise, the result will be False

        :type other: Polynomial, Monomial
        :rtype: bool
        """

        if isinstance(other, Polynomial):
            if not len(self) == len(other):
                return False
            else:
                def sort(l): return sorted(
                    l, key=lambda term: term.coefficient)
                first, second = sort(self), sort(other)
                return all(first[i] == second[i] for i in range(len(first)))
        elif isinstance(other, Monomial) and len(self) == 1:
            return self[0] == other
        else:
            return False

    def __neg__(self):
        """
        Return the opposite of the polynomial,
        changing the sign at all it's terms:

        :rtype: Polynomial
        """
        return Polynomial(*(-m for m in self))

    def __len__(self):
        """
        Return the number of terms of the
        polynomial

        :rtype: int
        """
        return len(self.terms)

    def __repr__(self):
        """
        Return the polynomial as a string

        """
        terms = ', '.join([repr(t) for t in self.terms])

        return f"Polynomial({terms})"
