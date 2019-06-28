from functools import reduce
from math import gcd
from collections import Counter, defaultdict, OrderedDict


def lcm(x, y): return int((x*y) / gcd(x, y))


class Monomial:

    def __init__(self, coefficient=1, variables={}):
        """
        Create a Monomial object, made by an integer
        or floating coefficient (1 for default) and
        a dict representing the variables, empty for
        default.

        For example, if you want to create a monomial
        like 5xy^3, the variables dict will be
        {'x': 1, 'y': 3}
        where the keys are the variable name and the
        values the degrees

        >>> print(Monomial(15*3, {'x': 1, 'z': 2}))
        45xz^2

        NB: The variables are always in lowercase:
        >>> print(Monomial(5, {'X': 1}))
        5x

        The __init__ method also calculate the total
        degree of the monomial:
        >>> Monomial(15*3, {'x': 1, 'z': 2}).degree
        3


        :param coefficient: The coefficient of the monomial
        :type coefficient: int, float
        :param variables: The variables of the monomial
        :type coefficient: dict
        """

        # Initialize the monomial
        self.coefficient = coefficient
        self.variables = defaultdict(lambda: 0, **variables)
        self.degree = sum(self.variables.values())

        # Check if the variables are ok
        for v in self.variables:
            if len(v) > 1 or not v.isalpha():
                raise ValueError(f"Variable name not valid ({v})")
            elif v.isupper():
                self.variables[v.lower()] = self.variables[v]
                del self.variables[v]
            elif self.variables[v] < 0:
                raise ValueError(f"Not a monomial: negative exponent ('{v}')")

    ### Utility Methods ###

    def similar_to(self, other):
        """
        Check if two monomials are similar,
        so if they've got the same variables:

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(8, {'x': 1})
        >>> c = Monomial(-13, {'x': 1, 'y': 1})
        >>> a.similar_to(b)
        False
        >>> a.similar_to(c)
        True

        :type other: Monomial
        :rtype: bool
        """

        if type(other) == type(self):
            return self.variables == other.variables
        else:
            return False

    def gcd(self, *others):
        """
        Calculate the greatest common divisor
        of two or more monomials (*others):

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(8, {'x': 1})
        >>> c = Monomial(-13, {'x': 1, 'y': 1})
        >>> a.gcd(b, c)
        Monomial(1, {'x': 1})

        :param others: The others monomial 
        :type others: Monomial
        :rtype: Monomial
        :raise: TypeError
        """

        # Check types of the arguments
        for i in range(len(others)):
            if type(others[i]) in [int, float]:
                others[i] = Monomial(others[i])
            elif not type(others[i]) == type(self):
                raise TypeError("Can't calculate gcd between Monomials"
                                f" and {type(others[i])}")

        monomials = self, *others

        # Calculate the gcd of the coefficients
        coefficients = [m.coefficient for m in monomials]
        coefficient_gcd = abs(reduce(gcd, coefficients))

        # Calculate the gcd of the variables
        vars_gcd = {}
        variables = [m.variables for m in monomials]
        for letter in variables[0]:
            if all(letter in v for v in variables):
                vars_gcd[letter] = max(v[letter] for v in variables)

        return Monomial(coefficient_gcd, vars_gcd)

    def lcm(self, *others):
        """
        Calculate the least common multiple
        of two or more monomials (*others):

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(8, {'x': 1})
        >>> c = Monomial(-13, {'x': 1, 'y': 1})
        >>> a.lcm(b, c)
        Monomial(520, {'y': 1, 'x': 1})

        :param others: The others monomial 
        :type others: Monomial
        :rtype: Monomial
        :raise: TypeError
        """

        # Check types of the arguments
        for i in range(len(others)):
            if type(others[i]) in [int, float]:
                others[i] = Monomial(others[i])
            elif not type(others[i]) == type(self):
                raise TypeError("Can't calculate lcm between Monomials"
                                f" and {type(others[i])}")

        monomials = self, *others

        # Calculate the lcm of the coefficients
        coefficients = [m.coefficient for m in monomials]
        coefficient_lcm = abs(reduce(lcm, coefficients))

        # Calculate the lcm of the variables
        vars_lcm = {}
        variables = [m.variables for m in monomials]
        letters = set()
        for v in variables:
            letters |= v.keys()

        vars_lcm = {l: max([m.variables[l] for m in monomials])
                    for l in letters}

        return Monomial(coefficient_lcm, vars_lcm)

    def eval(self, **values):
        """
        Evaluate the monomial, giving the values
        of the variables to the method

        >>> Monomial(5, {'x': 1}).eval(x=2)
        10
        >>> Monomial(-1, {'x': 1, 'y': 1}).eval(x=8, y=3)
        -24

        If a value isn't specified, the method
        will raise an error

        >>> Monomial(1.2, {'a': 1, 'b': 1}).eval(b=3)
        Traceback (most recent call last):
        ...
        KeyError: 'a'

        :type values: int, float
        :rtype: int, float
        :raise: KeyError
        """

        result = self.coefficient
        for var in self.variables:
            result *= (values[var]**self.variables[var])
        return result

    ### Operations Methods ###

    def __add__(self, other):
        """
        Return the sum of this monomial
        and another one

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(8, {'x': 1})
        >>> c = Monomial(-13, {'x': 1, 'y': 1})
        >>> d = Monomial(2.3, {'x': 1, 'y': 1})
        >>> a + c
        Monomial(-8, {'x': 1, 'y': 1})
        >>> d + c
        Monomial(-10.7, {'x': 1, 'y': 1})
        >>> a + d
        Monomial(7.3, {'x': 1, 'y': 1})

        If the monomials are not similar or the second
        operator is a polynomial, the result will be
        a polynomial

        >>> type(d + b) # They're not similar
        <class ruffini.polynomials.Polynomial>

        :type other: Monomial
        :rtype: Monomial, Polynomial, NotImplemented
        :raise: TypeError
        """

        if self.similar_to(other):
            return Monomial(self.coefficient + other.coefficient,
                            self.variables)
        elif type(other) == type(self):
            from .polynomials import Polynomial
            return Polynomial(self, other)
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        Return the subtraction between this
        monomial and another one

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(8, {'x': 1})
        >>> c = Monomial(13, {'x': 1, 'y': 1})
        >>> d = Monomial(-2, {'x': 1, 'y': 1})
        >>> a - c
        Monomial(-8, {'x': 1, 'y': 1})
        >>> c - a
        Monomial(8, {'x': 1, 'y': 1})
        >>> c - d
        Monomial(15, {'x': 1, 'y': 1})

        If the monomials are not similar or the second
        operator is a polynomial, the result will be
        a polynomial (see Polynomial.__radd__ for more)

        >>> type(d - b) # not similar
        <class ruffini.polynomials.Polynomial>

        :type other: Monomial
        :rtype: Monomial, Polynomial, NotImplemented
        :raise: TypeError
        """

        if self.similar_to(other):
            return Monomial(self.coefficient - other.coefficient,
                            self.variables)
        elif type(other) == type(self):
            from .polynomials import Polynomial
            return Polynomial(self, other)
        else:
            return NotImplemented

    def __mul__(self, other):
        """
        Multiplicate this monomial and another monomial
        or a number (inf / float)

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(8, {'x': 1})
        >>> c = Monomial(-13, {'x': 1, 'y': 1})
        >>> a * b
        Monomial(40, {'x': 2, 'y': 1})
        >>> c * a
        Monomial(-65, {'x': 2, 'y': 2})
        >>> c * 2
        Monomial(-26, {'x': 1, 'y': 1})
        >>> b * 1.3
        Monomial(10.4, {'x': 1})

        :type other: Monomial, int, float
        :rtype: Monomial, NotImplemented
        :raise: TypeError
        """

        if type(other) in [int, float]:
            other = Monomial(other)

        if type(other) == type(self):
            coefficient = self.coefficient * other.coefficient
            letters = set(list(self.variables) + list(other.variables))
            variables = {}
            for l in letters:
                if self.variables[l] + other.variables[l] != 0:
                    variables[l] = self.variables[l] + other.variables[l]
            return Monomial(coefficient, variables)
        else:
            return NotImplemented

    def __truediv__(self, other):
        """
        Divide this monomial per another monomial or
        per a number (int / float)

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(8, {'x': 1})
        >>> c = Monomial(-10, {'x': 1, 'y': 1})
        >>> a / b
        Monomial(0.625, {'y': 1})
        >>> a / c
        Monomial(-0.5, {})
        >>> c / -2
        Monomial(5.0, {'x': 1, 'y': 1})
        >>> b / a #= 1.6y^(-1), it is not a monomial
        Traceback (most recent call last):
        ...
        ValueError: Not a monomial: negative exponent ('y')

        :type other: Monomial, int, float
        :rtype: Monomial, NotImplemented
        :raise: ValueError, TypeError
        """

        if type(other) in [int, float]:
            other = Monomial(other)

        if type(other) == type(self):
            coefficient = self.coefficient / other.coefficient
            letters = set(list(self.variables) + list(other.variables))
            variables = {}
            for l in letters:
                if self.variables[l] - other.variables[l] != 0:
                    variables[l] = self.variables[l] - other.variables[l]
            return Monomial(coefficient, variables)
        else:
            return NotImplemented

    def __pow__(self, n):
        """
        Raise a monomial to power

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(8, {'x': 1})
        >>> c = Monomial(16, {'x': 6})
        >>> a ** 2
        Monomial(25, {'x': 2, 'y': 2})
        >>> b ** 3
        Monomial(512, {'x': 3})

        :type n: int
        :rtype: Monomial, NotImplemented
        :raise: ValueError, TypeError
        """

        # Raise an error if the exponent is not a number
        if not isinstance(n, int):
            return NotImplemented

        # Raise the variables to power
        variables = {}
        for var in self.variables:
            variables[var] = self.variables[var] * n

        return Monomial(self.coefficient ** n, variables)

    def __rmul__(self, other):
        """
        Multiply a number (int / float) for amonomial

        >>> m1 = Monomial(17, {'x': 1, 'y': 1})
        >>> m2 = Monomial(-3, {'y': 1})
        >>> 8 * m1
        Monomial(136, {'x': 1, 'y': 1})
        >>> 0.13 * m2
        Monomial(-0.39, {'y': 1})

        :type other: int, float
        :rtype: Monomial, NotImplemented
        :raise: TypeError   
        """

        try:
            return self.__mul__(other)
        except:
            return NotImplemented

    ### Magic Methods ###

    def __hash__(self):
        """
        Thanks to this method you can create a set of
        monomials, for example.

        >>> m1 = Monomial(5, {'x': 1, 'y': 1})
        >>> m2 = Monomial(-3, {'y': 1, 'z': 1})
        >>> m3 = Monomial(variables={'a': 4, 'b': 1})
        >>> m = {m1, m2, m3}
        >>> # No error is raised (without __hash__ would
        >>> # be raised a TypeError)

        :rtype: int
        """
        return hash(str(self))

    def __str__(self):
        """
        Return the monomial as a string (without *
        operator):

        >>> str(Monomial(14, {'x': 1, 'y': 1}))
        '14xy'
        >>> str(Monomial(-1+3, {'a': 1}))
        '2a'
        >>> str(Monomial(1, {'y': 2}))
        'y^2'

        :rtype: str
        """
        variables = ""
        for l in self.variables:
            if self.variables[l] > 1:
                variables += f"{l}^{self.variables[l]}"
            else:
                variables += l

        if self.coefficient == 1 and variables:
            return variables
        elif self.coefficient == -1 and self.variables:
            return '-' + variables
        elif self.coefficient == 0:
            return '0'
        elif self.coefficient == 1 and not self.variables:
            return '1'
        elif self.coefficient == -1 and not self.variables:
            return '-1'
        else:
            return str(self.coefficient) + variables

    def __eq__(self, other):
        """
        Check if two monomials are equivalent,
        comparing coefficients and variables

        >>> Monomial(14, {'a': 1}) == Monomial(14, {'a': 1})
        True
        >>> Monomial(14, {'a': 1}) == Monomial(14, {'a': 2})
        False
        >>> Monomial(14, {'a': 1}) == Monomial(-14, {'a': 1})
        False
        >>> Monomial(14, {'a': 1}) == Monomial(19, {'a': 1})
        False

        :type other: Monomial
        :rtype: bool
        """
        return self.coefficient == other.coefficient \
            and self.variables == other.variables

    def __neg__(self):
        """
        Return the opposite of the monomial,
        inverting the coefficient:

        >>> -Monomial(14, {'x': 1})
        Monomial(-14, {'x': 1})
        >>> -Monomial(-8, {'b': 1})
        Monomial(8, {'b': 1})

        :rtype: Monomial
        """
        return Monomial(-self.coefficient, self.variables)

    def __abs__(self):
        """
        Return the absolute value of the monomial
        (the monomial without the sign) calculating
        the absolute value of the coefficient:

        >>> abs(Monomial(14, {'x': 1}))
        Monomial(14, {'x': 1})
        >>> abs(Monomial(-8, {'b': 1}))
        Monomial(8, {'b': 1})

        :rtype: Monomial
        """
        return Monomial(abs(self.coefficient), self.variables)

    def __repr__(self):
        """
        Return the monomial as a string, but
        like this:

        >>> repr(Monomial(-14, {'x': 1})) # repr
        "Monomial(-14, {'x': 1})"
        >>> str(Monomial(-14, {'x': 1})) # str
        '-14x'
        """

        variables = dict(self.variables)
        return f"Monomial({self.coefficient}, {variables})"
