from .monomials import Monomial
from .variables import VariablesDict

from collections import Counter


class Polynomial (tuple):
    """
    A Polynomial object is the sum of two or more
    monomials and/or numbers.

    With a Polynomial() instance, you can do sums,
    subtractions, multiplications and divisions.

    You can also assign a value to the variables and
    calculate the value of that polynomial with the
    value you assigned.

    NB. the Polynomial class is a subclass of tuple,
    so all the methods of tuple are automatically
    inherited from Polynomial; many of these methods
    are not in this docs.
    """

    def __new__ (cls, *terms):
        """
        Create the polynomial giving it a list
        of terms (a term can be a Monomial or a
        number); if two or more terms have the
        same variablesm, it will sum them toghether

        :param *terms: Terms of the polynomial
        :type *terms: Monomials, int, float
        :raise: TypeError
        """

        counter = Counter()

        # Sum the simil terms
        for term in terms:
            if isinstance(term, (int, float)):
                term = Monomial(term, {})
            elif isinstance(term, Monomial):
                pass
            else:
                raise TypeError(f"{term} is not a valid term")

            counter[term.variables] += term.coefficient

        # Rewrite them
        terms = [Monomial(c, v) for v, c in counter.items()]

        return super().__new__(cls, terms)

    def __init__ (self, *terms):
        """
        Initialize the polynomial, then calculate
        the polynomial degree (the highest degree
        of the terms)

        :param *terms: Terms of the polynomial
        :type *terms: Monomials, int, float
        """

        # Add polynomial degree
        self.degree = max(m.degree for m in self)

    ### Utility Methods ###

    def term_coefficient(self, variables):
        """
        Return the coefficient of the term with
        the given variables

        >>> m0 = Monomial(2, {'x': 1, 'y': 1})
        >>> m1 = Monomial(-6, {'x': 1, 'y': 3})
        >>> m2 = Monomial(8, {'x': 1, 'y': 1})
        >>> p = Polynomial(m0, m1, m2)
        >>> p.term_coefficient({'x': 1, 'y': 1})
        10

        If none is found, the result will be 0

        >>> p.term_coefficient({'k': 1, 'b': 2})
        0

        :type variables: dict, VariablesDict
        :param variables: The variables of the coefficient you're looking for
        :rtype: int, float
        """

        variables = VariablesDict(**variables)

        for term in self:
            if term.variables == variables:
                return term.coefficient

        # if nothing is found
        return 0

    ### Operations Methods ###

    def __add__(self, other):
        """
        As the name say, this method will sum this
        polynomial with another polynomial, a monomial
        or a number, too.
        
        >>> m0 = Monomial(10, {'a': 4})
        >>> m1 = Monomial(-4, {'a': 4})
        >>> m2 = Monomial(7, {'y': 1})
        >>> m3 = Monomial(9, {'x': 1})
        >>> m4 = Monomial(-13, {'y': 1})
        >>> p = Polynomial(m1, m2, m4) # -4a^4 -6y
        >>>
        >>> # polynomial + polynomial
        >>> print(p + Polynomial(m0, m3, m2))
        6a^4 +y +9x
        >>> # polynomial + monomial
        >>> print(p + m3)
        -4a^4 -6y +9x
        >>> # polynomial + number
        >>> print(p + 9)
        -4a^4 -6y +9

        If the second operator isn't in the list above,
        it will raise a TypeError

        >>> p + "placeholder"
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for +: 'Polynomial' and 'str'

        :type other: Polynomial, Monomial, int, float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        if isinstance(other, Polynomial):
            return Polynomial(*self, *other)
        elif isinstance(other, Monomial):
            return Polynomial(*self, other)
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        As the name say, this method will subtract this
        polynomial from another polynomial, a monomial
        or a number, too.

        >>> m0 = Monomial(10, {'a': 4})
        >>> m1 = Monomial(-4, {'a': 4})
        >>> m2 = Monomial(7, {'y': 1})
        >>> m3 = Monomial(9, {'x': 1})
        >>> m4 = Monomial(-13, {'y': 1})
        >>> p = Polynomial(m1, m2, m4) # -4a^4 -6y
        >>>
        >>> # polynomial - polynomial
        >>> print(p - Polynomial(m0, m3, m2))
        -14a^4 -13y -9x
        >>> # polynomial - monomial
        >>> print(p - m3)
        -4a^4 -6y -9x
        >>> # polynomial - number
        >>> print(p - 9)
        -4a^4 -6y -9

        If the second operator isn't in the list above,
        it will raise a TypeError

        >>> p - []
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for -: 'Polynomial' and 'list'

        :type other: Polynomial, Monomial, int, float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        if isinstance(other, Polynomial):
            return Polynomial(*self, *(-other))
        elif isinstance(other, Monomial):
            return Polynomial(*self, -other)
        else:
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
            return Polynomial(*(t*other for t in self))
        elif isinstance(other, Polynomial):
            return Polynomial(*(a*b for a in self for b in other))
        else:
            return NotImplemented

    ### Reverse Operations Methods ###

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
        result = str(self[0])
        for term in self[1:]:
            if term.coefficient > 0:
                result += f" +{term}"
            elif term.coefficient < 0:
                result += f" {term}"
        return result

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

    def __repr__(self):
        """
        Return the polynomial as a string

        """
        terms = ', '.join([repr(t) for t in self])

        return f"Polynomial({terms})"
