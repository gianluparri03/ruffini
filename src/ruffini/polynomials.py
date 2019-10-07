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
        same variables, it will sum them toghether

        >>> print(Polynomial(Monomial(2, {'x': 2, 'y': 2})))
        2x^2y^2

        :type *terms: Monomials, int, float
        :raise: TypeError
        """

        counter = Counter()

        # Sum the similar terms
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

        >>> print(Polynomial(Monomial(1, {'a': 1}), Monomial(3, {})))
        a +3

        :type *terms: Monomials, int, float
        """

        # Add polynomial degree
        self.degree = max(m.degree for m in self) if self else 0

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
        :rtype: Polynomial
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        if isinstance(other, Polynomial):
            return Polynomial(*self, *other)

        elif isinstance(other, Monomial):
            return Polynomial(*self, other)

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Polynomial' and '{other.__class__.__name__}'")

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
        :rtype: Polynomial
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        if isinstance(other, Polynomial):
            return Polynomial(*self, *(-other))

        elif isinstance(other, Monomial):
            return Polynomial(*self, -other)

        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Polynomial' and '{other.__class__.__name__}'")

    def __mul__(self, other):
        """
        This method is used to multiply a polynomial
        by a polynomial, a monomial or a number:

        >>> m0 = Monomial(10, {'a': 4})
        >>> m1 = Monomial(-4, {'a': 4})
        >>> m2 = Monomial(7, {'y': 1})
        >>> m3 = Monomial(9, {'x': 1})
        >>> m4 = Monomial(-13, {'y': 1})
        >>> p = Polynomial(m1, m2, m4) # -4a^4 -6y
        >>> # polynomial * polynomial
        >>> print(p * Polynomial(m0, m1, m4))
        -24a^8 +16a^4y +78y^2
        >>> # polynomial * monomial
        >>> print(p * m3)
        -36a^4x -54xy
        >>> # polynomial * number
        >>> print(p * 3)
        -12a^4 -18y

        If the second operator type is not mentioned
        above, it will raise a TypeError

        >>> p * {}
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for *: 'Polynomial' and 'dict'

        :type other: Monomial, Polynomial, int, float
        :rtype: Polynomial
        :raise: TypeError
        """

        if isinstance(other, (Monomial, int, float)):
            return Polynomial(*(t*other for t in self))

        elif isinstance(other, Polynomial):
            return Polynomial(*(a*b for a in self for b in other))

        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Polynomial' and '{other.__class__.__name__}'")

    ### Reverse Operations Methods ###

    def __radd__(self, other):
        """
        This method is the reverse for :func:ruffini.Polynomial.__add__.
        With this method, you can swap the two operands
        of the addition:

        >>> print(8 + Polynomial(Monomial(4, {'a': 2})))
        4a^2 +8

        For more informations, see :func:ruffini.Polynomial.__add__ docs.

        :type other: Monomial, int, float
        :rtype: Polynomial
        :raise: TypeError
        """

        try:
            return self + other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for +: '{other.__class__.__name__}' and 'Polynomial'")

    def __rsub__(self, other):
        """
        This method is the reverse for :func:ruffini.Polynomial.__sub__.
        With this method, you can swap the two operands
        of the addition:

        >>> print(5 - Polynomial(Monomial(7, {'k': 1})))
        -7k +5

        For more informations, see :func:ruffini.Polynomial.__sub__ docs.

        :type other: Monomial, int, float
        :rtype: Polynomial
        :raise: TypeError
        """

        try:
            return (-self) + other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for -: '{other.__class__.__name__}' and 'Polynomial'")

    def __rmul__(self, other):
        """
        This method is the reverse for :func:ruffini.Polynomial.__mul__.
        With this method, you can swap the two operands
        of the addition:

        >>> print(10 * Polynomial(Monomial(3.5, {'b': 3})))
        35.0b^3

        For more informations, see :func:ruffini.Polynomial.__mul__ docs.

        :type other: Monomial, int, float
        :rtype: Polynomial, NotImplemented
        :raise: TypeError
        """

        try:
            return self * other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for *: '{other.__class__.__name__}' and 'Polynomial'")

    ### Magic Methods ###

    def __str__(self):
        """
        Return the polynomial as a string in a human-readable
        mode. The exponent for the variables is indicated with a ^.

        >>> str(Polynomial(Monomial(4, {'a': 4, 'b': 1})))
        '4a^4b'
        >>> str(Polynomial(Monomial(1, {'a': 2}), Monomial(-2, {'c': 2})))
        'a^2 -2c^2'
        >>> str(Polynomial(Monomial(3, {'x': 2}), Monomial(6, {'y': 3})))
        '3x^2 +6y^3'

        To see how the single terms are printed, see the
        Monomial().__str__() docs.

        :rtype: str
        """

        result = str(self[0])
        for term in self[1:]:
            if term.coefficient == abs(term.coefficient): # positive
                result += f" +{term}"
            else: # negative
                result += f" {term}"
        return result

    def __repr__(self):
        """
        Return the polynomial as a string in a less human-readable
        mode than str()

        >>> repr(Polynomial(Monomial(4, {'a': 4, 'b': 1})))
        "Polynomial(Monomial(4, {'a': 4, 'b': 1}))"
        >>> repr(Polynomial(Monomial(1, {'a': 2}), Monomial(-2, {'c': 2})))
        "Polynomial(Monomial(1, {'a': 2}), Monomial(-2, {'c': 2}))"
        >>> repr(Polynomial(Monomial(3, {'x': 2}), Monomial(6, {'y': 3})))
        "Polynomial(Monomial(3, {'x': 2}), Monomial(6, {'y': 3}))"

        NB. When you have a lot of terms, this method
        will return a certain ammount of spam.

        To see how the single terms are printed, you can
        see the Monomial().__repr__() docs.

        :rtype: str
        """
        terms = ', '.join([repr(t) for t in self])

        return f"Polynomial({terms})"


    def __eq__(self, other):
        """
        Check if two polynomials are equivalent,
        comparating each term

        >>> p0 = Polynomial(Monomial(4, {'a': 4, 'b': 1}))
        >>> p1 = Polynomial(Monomial(1, {'a': 2}), Monomial(-2, {'c': 2}))
        >>> p2 = Polynomial(Monomial(-2, {'c': 2}), Monomial(1, {'a': 2}))
        >>> p0 == p1
        False
        >>> p0 == p0
        True
        >>> p1 == p2
        True

        If a polynomial has a single term, it can
        also be compared to a monomial

        >>> Polynomial(Monomial(3, {'f': 2})) == Monomial(3, {'f': 2})
        True

        NB. Since a monomial with no variables can be
        compared to a number, if a polynomial has only
        a term, which is a monomial with no variables,
        it can be compared to a number, too!

        >>> Polynomial(Monomial(7,{})) == 7
        True

        If the second operator in not mentione above,
        the result will be False.

        >>> Polynomial() == {1, 2, 3}
        False

        :type other: Polynomial, Monomial, int, float
        :rtype: bool
        """

        if isinstance(other, Polynomial):
            if not len(self) == len(other):
                return False
            else:
                return set(self) == set(other)

        elif isinstance(other, (Monomial, int, float)) and len(self) == 1:
            return self[0] == other

        else:
            return False

    def __neg__(self):
        """
        This method return the opposite of
        the polynomial, changing the sign of
        each term of the polynomial

        >>> print(-Polynomial(Monomial(4, {'x': 1}), Monomial(2, {'y': 2})))
        -4x -2y^2
        >>> print(-Polynomial(Monomial(-6, {'b': 2}), Monomial(3, {'k': 3})))
        6b^2 -3k^3

        :rtype: Polynomial
        """
        return Polynomial(*(-m for m in self))
