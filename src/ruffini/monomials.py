from .variables import VariablesDict
from functools import reduce
from math import gcd
from collections import Counter


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
        self.variables = VariablesDict(**variables)
        self.degree = sum(self.variables.values())

        # Check if the variables are ok
        for v in self.variables:
            if self.variables[v] < 0:
                raise ValueError(f"Not a monomial: negative exponent ('{v}')")

    ### Utility Methods ###

    def similar_to(self, other):
        """
        Check if two monomials are similar,
        so if they've got the same variables:

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

        :param others: Others monomial 
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

        :param others: Others monomial 
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

    ### Operations Methods ###

    def __add__(self, other):
        """
        Return the sum of this monomial
        and another one

        If the monomials are not similar or the second
        operator is a polynomial, the result will be
        a polynomial

        :type other: Monomial, 0
        :rtype: Monomial, Polynomial, NotImplemented, 0
        :raise: TypeError
        """

        if self.similar_to(other):
            r = Monomial(self.coefficient + other.coefficient,
                         self.variables)
            if r.coefficient == 0:
                return 0
            else:
                return r
        elif type(other) == type(self):
            from .polynomials import Polynomial
            return Polynomial(self, other)
        elif other == 0:
            return self
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        Return the subtraction between this
        monomial and another one

        If the monomials are not similar or the second
        operator is a polynomial, the result will be
        a polynomial (see Polynomial.__radd__ for more)

        :type other: Monomial, 0
        :rtype: Monomial, Polynomial, NotImplemented, 0
        :raise: TypeError
        """

        if self.similar_to(other):
            return self + (-other)
        elif type(other) == type(self):
            from .polynomials import Polynomial
            return Polynomial(self, -other)
        elif other == 0:
            return self
        else:
            return NotImplemented

    def __mul__(self, other):
        """
        Multiplicate this monomial and another monomial
        or a number (inf / float)

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

        :type other: Monomial, int, float
        :rtype: Monomial, NotImplemented, int, float
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
            if coefficient == 1 and variables == {}:
                return 1
            else:
                return Monomial(coefficient, variables)
        else:
            return NotImplemented

    def __pow__(self, n):
        """
        Raise a monomial to power

        :type n: int
        :rtype: Monomial, NotImplemented
        :raise: ValueError, TypeError
        """

        # Raise an error if the exponent is not an integer
        if not isinstance(n, int):
            return NotImplemented

        # Raise an error if exponent is negative
        if not abs(n) == n:
            raise ValueError("Exponent can't be negative")

        # Raise the variables to power
        variables = {}
        for var in self.variables:
            variables[var] = self.variables[var] * n

        return Monomial(self.coefficient ** n, variables)

    def __rmul__(self, other):
        """
        Multiply a number (int / float) for amonomial

        :type other: int, float
        :rtype: Monomial, NotImplemented
        :raise: TypeError   
        """

        try:
            return self.__mul__(other)
        except:
            return NotImplemented

    ### Magic Methods ###

    def __call__(self, **values):
        """
        Evaluate the monomial, giving the values
        of the variables to the method

        If a value isn't specified, the method
        will raise an error

        :type values: int, float
        :rtype: int, float
        :raise: KeyError, TypeError
        """

        values = dict(
            zip(map(lambda v: v.casefold(), values), values.values()))

        result = self.coefficient
        for var in self.variables:
            result *= (values[var]**self.variables[var])
        return result

    def __hash__(self):
        """
        Thanks to this method you can create a set of
        monomials, for example.

        :rtype: int
        """
        return hash(repr(self))

    def __str__(self):
        """
        Return the monomial as a string (without *
        operator):

        :rtype: str
        """
        variables = ""
        for l in sorted(self.variables.keys()):
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

        :type other: Monomial, int, float
        :rtype: bool
        """
        if isinstance(other, Monomial):
            return self.coefficient == other.coefficient \
                and self.variables == other.variables
        elif self.variables == {}:
            return self.coefficient == other
        else:
            return False

    def __neg__(self):
        """
        Return the opposite of the monomial,
        inverting the coefficient:

        :rtype: Monomial
        """
        return Monomial(-self.coefficient, self.variables)

    def __abs__(self):
        """
        Return the absolute value of the monomial
        (the monomial without the sign) calculating
        the absolute value of the coefficient:

        :rtype: Monomial
        """
        return Monomial(abs(self.coefficient), self.variables)

    def __repr__(self):
        """
        Return the monomial as a string, but
        like this
        """

        return f"Monomial({self.coefficient}, {self.variables})"
