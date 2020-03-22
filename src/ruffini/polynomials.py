from .variables import VariablesDict
from .monomials import Monomial, Variable

from collections import Counter


def get_divisors(n):
    n = abs(n)
    divs = {m for m in range(1, int(n/2) + 1) if not n % m}
    divs |=  {int(n / m) for m in divs}
    return divs

class Polynomial(tuple):
    """
    A Polynomial object is the sum of two or more
    monomials and/or numbers.

    You can sum, subtract and multiplicate instances
    of Polynomial.

    You can assign a value to the variables and
    calculate the value of that polynomial with the
    value you assigned.

    **NB** The Polynomial class is a subclass of tuple,
    so all the methods of tuple are automatically
    inherited from Polynomial; many of these methods
    are not in this docs.
    """

    def __new__(cls, terms=(), *args):
        """
        Create the polynomial by giving it a list
        of terms (a term can be a Monomial or a
        number); if two or more terms have the
        same variables, it will sum them toghether

        >>> Polynomial(Monomial(2, x=2, y=2), Monomial(3, x=2, y=2))
        5x**2y**2

        :type *terms: Monomials, int, float
        :raise: TypeError
        """

        # adjust arguments' order
        if not isinstance(terms, (tuple, list, set)):
            terms = (terms, ) + args

        counter = Counter()

        # Sum the similar terms
        for term in terms:
            if isinstance(term, (int, float)):
                term = Monomial(term)
            elif isinstance(term, Monomial):
                pass
            else:
                raise TypeError(f"{term} is not a valid term")

            counter[term.variables] += term.coefficient

        # Rewrite them
        terms = [Monomial(c, v) for v, c in counter.items()]

        return super().__new__(cls, terms)

    def __init__(self, terms=(), *args):
        """
        Initialize the polynomial, then calculate
        its degree (the highest degree between terms' ones)

        >>> p = Polynomial(Monomial(a=1), Monomial(3))
        >>> p
        a + 3
        >>> p.degree
        1

        :type *terms: Monomials, int, float
        """

        # Add polynomial degree
        self.degree = max(m.degree for m in self) if self else 0

    ### Utility Methods ###

    def term_coefficient(self, variables=None, **kwargs):
        """
        Return the coefficient of the term with
        the given variables

        >>> x = Variable('x')
        >>> y = Variable('y')
        >>>
        >>> p = 2*x*y - 6*x*y**3 + 8*x*y
        >>> p
        10xy - 6xy**3
        >>>
        >>> p.term_coefficient(x=1, y=1)
        10

        If none is found, the result will be 0

        >>> p.term_coefficient(k=1, b=2)
        0

        You can also give directly the variables as an argument

        >>> p.term_coefficient(x*y)
        10

        :type variables: dict, VariablesDict
        :rtype: int, float
        """

        # adjust arguments
        if not variables:
            variables = kwargs

        elif isinstance(variables, Monomial) and variables.coefficient == 1:
            variables = variables.variables

        elif not isinstance(variables, VariablesDict):
            variables = VariablesDict(variables)

        for term in self:
            if term.variables == variables:
                return term.coefficient

        # if nothing is found
        return 0

    def factorize(self):
        """
        With this method you can factorize the polynomial.

        For more informations, see :func:`factorize` docs.

        :rtype: FPolynomial
        """

        from .fpolynomials import factorize

        return factorize(self)

    @property
    def zeros(self):
        """
        Return a set of zeros for the polynomial

        >>> x = Variable('x')
        >>> p = 3*x**3 + 2*x**2 - 3*x - 2
        >>> p.zeros
        {-0.6666666666666666, 1.0, -1.0}

        It works only with polynomials with only a variable
        and a constant term

        >>> Polynomial(3*x, Monomial(2, y=1)).zeros
        Traceback (most recent call last):
        ...
        ValueError: Can't calculate zeros for polynomials with more than a variable

        >>> Polynomial(3*x, 5*x**2).zeros
        Traceback (most recent call last):
        ...
        ValueError: Can't calculate zeros for polynomials without a constant term

        :rtype: set
        :raises: ValueError
        """

        # Fetch variables and the constant term
        variable = {v for m in self for v in m.variables.keys()}
        constant_term = self.term_coefficient()

        # Raise a ValueError if there are more than one variable
        # or if there isn't a constant term
        if len(set(variable)) != 1:
            raise ValueError("Can't calculate zeros for polynomials with more than a variable")
        elif not constant_term:
            raise ValueError("Can't calculate zeros for polynomials without a constant term")

        variable = tuple(variable)[0]
        coefficient = self.term_coefficient({variable: self.degree})

        # Create a list of candidates
        constant_term_divs = {d for n in get_divisors(constant_term) for d in (+n, -n)}
        coefficient_divs = get_divisors(coefficient)
        candidates = {a/b for a in constant_term_divs for b in coefficient_divs}

        # Try every candidate
        zeros = set()

        for candidate in candidates:
            if self.eval({variable: candidate}) == 0:
                zeros.add(candidate)

        return zeros

    def eval(self, values=VariablesDict(), **kwargs):
        """
        Evaluates the polynomial, giving values
        for each variable

        >>> p = Polynomial(Monomial(5, x=1), Monomial(3, y=1))
        >>> p.eval(x=2, y=3)
        19

        For more informations, see :func:`Monomial.eval`.

        :rtype: int, float, Monomial, Polynomial
        """

        # multiple initializations
        if not values:
            values = kwargs

        # eval each term of the polynomial, then return it
        return Polynomial([t.eval(values) for t in self])

    ### Operations Methods ###

    def __add__(self, other):
        """
        Sum the polynomial with another polynomial, a monomial
        or a number, too.

        >>> x = Variable('x')
        >>> y = Variable('y')
        >>> p = 3*x + 2*y
        >>>
        >>> p + (3*y + 2)
        3x + 5y + 2
        >>>
        >>> p + 2*x
        5x + 2y
        >>>
        >>> p + 1
        3x + 2y + 1

        :type other: Polynomial, Monomial, int, float
        :rtype: Polynomial
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other)

        if isinstance(other, Polynomial):
            return Polynomial(*self, *other)

        elif isinstance(other, Monomial):
            return Polynomial(*self, other)

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Polynomial' and '{other.__class__.__name__}'")

    def __sub__(self, other):
        """
        Subtract the polynomial from another polynomial,
        a monomial or a number.

        >>> x = Variable('x')
        >>> y = Variable('y')
        >>>
        >>> p = 3*x + 2*y
        >>>
        >>> p - (3*y + 2)
        3x - y - 2
        >>>
        >>> p - 2*x
        x + 2y
        >>>
        >>> p - 1
        3x + 2y - 1

        :type other: Polynomial, Monomial, int, float
        :rtype: Polynomial
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other)

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

        >>> x = Variable('x')
        >>> y = Variable('y')
        >>>
        >>> p = 3*x + 2*y
        >>>
        >>> p * (3*y + 2)
        9xy + 6x + 6y**2 + 4y
        >>>
        >>> p * x
        3x**2 + 2xy
        >>>
        >>> p * 4
        12x + 8y

        :type other: Monomial, Polynomial, int, float
        :rtype: Polynomial
        :raise: TypeError
        """

        if isinstance(other, (Monomial, int, float)):
            return Polynomial([t*other for t in self])

        elif isinstance(other, Polynomial):
            return Polynomial([a*b for a in self for b in other])

        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Polynomial' and '{other.__class__.__name__}'")

    ### Reverse Operations Methods ###

    def __radd__(self, other):
        """
        This method is the reverse for :func:`Polynomial.__add__`.
        With this method, you can swap the two operands
        of the addition:

        >>> 8 + Polynomial(Monomial(4, a=2))
        4a**2 + 8

        For more informations, see :func:`Polynomial.__add__` docs.

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
        This method is the reverse for :func:`Polynomial.__sub__`.
        With this method, you can swap the two operands
        of the addition:

        >>> 5 - Polynomial(Monomial(7, k=1))
        -7k + 5

        For more informations, see :func:`Polynomial.__sub__ docs`.

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
        This method is the reverse for :func:`Polynomial.__mul__`.
        With this method, you can swap the two operands
        of the addition:

        >>> 10 * Polynomial(Monomial(3.5, b=3))
        35b**3

        For more informations, see :func:`Polynomial.__mul__` docs.

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
        Return the polynomial as a string.
        Powers are indicated with **.

        >>> str(Polynomial(Monomial(4, a=4, b=1)))
        '4a**4b'
        >>> str(Polynomial(Monomial(a=2), Monomial(-2, c=2)))
        'a**2 - 2c**2'
        >>> str(Polynomial(Monomial(3, x=2), Monomial(6, y=3)))
        '3x**2 + 6y**3'

        To see how the single terms are printed, see the
        :func:`Monomial.__str__` docs.

        :rtype: str
        """

        result = str(self[0])
        for term in self[1:]:
            if term.coefficient == abs(term.coefficient):  # positive
                result += " + " + str(term)
            else:  # negative
                result += " - " + str(term)[1:]
        return result

    def __repr__(self):
        """
        Return the polynomial as a string.

        >>> repr(Polynomial(Monomial(4, a=4, b=1)))
        '4a**4b'

        For more informations, see :func:`Polynomial.__str__`.

        :rtype: str
        """

        return self.__str__()

    def __eq__(self, other):
        """
        Check if two polynomials are equivalent,
        comparing each term

        >>> p0 = Polynomial(Monomial(4, a=4, b=1))
        >>> p1 = Polynomial(Monomial(1, a=2), Monomial(-2, c=2))
        >>> p2 = Polynomial(Monomial(-2, c=2), Monomial(1, a=2))
        >>>
        >>> p0 == p1
        False
        >>> p0 == p0
        True
        >>> p1 == p2
        True

        If a polynomial has a single term, it can
        also be compared to a monomial

        >>> Polynomial(Monomial(3, f=2)) == Monomial(3, f=2)
        True

        Since a monomial with no variables can be
        compared to a number, if a polynomial has only
        a term - which is a monomial with no variables -
        it can be compared to a number

        >>> Polynomial(Monomial(7)) == 7
        True

        In any other case, the result will be False.

        >>> Polynomial() == {1, 2, 3}
        False

        :type other: Polynomial, Monomial, int, float
        :rtype: bool
        """

        try:
            return hash(self) == hash(other)
        except TypeError:
            return False

    def __neg__(self):
        """
        Return the opposite of the polynomial, changing
        the sign of each term of the polynomial

        >>> -Polynomial(Monomial(4, x=1), Monomial(2, y=2))
        -4x - 2y**2

        :rtype: Polynomial
        """
        return Polynomial([-m for m in self])

    def __hash__(self):
        """
        Return the hash for the Polynomial

        The hash for 8xy + 2, for example, is equal
        to the hash of ((8, ('x', 1), ('y', 1)), 2).

        If the polynomial has only a term, its hash
        will be equal to the hash of that term

        >>> hash(Polynomial(Monomial(3, x=1))) == hash(Monomial(3, x=1))
        True

        If that term has no variables, the hash will be equal
        to the coefficient's

        >>> hash(Polynomial(Monomial(3))) == hash(3)
        True

        :rtype: int
        """

        if len(self) == 1:
            return hash(self[0])

        return hash(tuple(sorted(self, key=str)))
