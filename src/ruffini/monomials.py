from .variables import VariablesDict
from functools import reduce
from math import gcd


class Monomial:
    """
    A Monomial object is composed by variables
    and coefficient; the coefficient can be
    whathever you want, but it has to be numerical
    (instance of int or float). The variables
    instead must have three features:
    - positive and integer exponent
    - all the variables names must be a letter
    of the alphabet (a, b, c, d, e, f...)

    Monomials can be added, subtracted, multiplied
    and divided togheter (multiplication and division
    can be done also between monomials and numbers).
    You can also calculate lcmd and gcd between
    monomials (and numbers).

    You can also assign a value to the variables and
    calculate the value of that monomial with the
    value you assigned.
    """

    def __init__(self, coefficient, variables):
        """
        Create a Monomial object by giving the
        numerical coefficient and the variables,
        stored in a dict (the keys are the letters
        and the values the degrees).

        The variables will be stored in a VariableDict, so:
        - all the letters will be made lowercase
        - the letters can be only alphabetical and
          with a lenght of one
        - the exponent must be positive and integer

        When initialized the monomial, this method calculates
        the monomial's total degree (the sum of all the degrees)

        :type coefficient: int, float
        :type coefficient: dict, VariablesDict
        :raise: ValueError, TypeError
        """

        # Check the coefficient
        if isinstance(coefficient, (int, float)):
            self.coefficient = coefficient
        else:
            raise TypeError("Coefficient must be int or float")

        # Check the variables
        if isinstance(variables, VariablesDict):
            self.variables = variables
        elif isinstance(variables, dict):
            self.variables = VariablesDict(**variables)
        else:
            raise TypeError("Variables must be stored in a dict")

        # Calculate the degree
        self.degree = sum(self.variables.values())

    ### Utility Methods ###

    def similar_to(self, other):
        """
        Check if two monomials are similar (if
        the have the same variables).

        >>> m1 = Monomial(3, {'x': 1, 'x': 1}))
        >>> m2 = Monomial(-6, {'x': 1, 'x': 3}))
        >>> m3 = Monomial(2.6, {'x': 1, 'x': 1}))
        >>> m4 = Monomial(3.14, {}))
        >>> m1.similar_to(m4)
        True
        >>> m1.similar_to(m2)
        False

        If 'other' is not a monomial the result
        will always be False

        >>> m3.similar_to("")
        False
        >>> m4.similar_to({})
        False

        The only one exception: is when the
        monomial has no variables and it's
        compared to an int or a float; in this
        case, the result will be positive

        >>> m4.similar_to(6.28)
        True

        :type other: Monomial, int, float
        :rtype: bool
        """

        if self.variables.empty and isinstance(other, (int, float)):
            return True
        elif not isinstance(other, Monomial):
            return False

        return self.variables == other.variables

    def gcd(self, other):
        """
        Calculate the greatest common divisor
        of two monomials (or numbers)

        >>> a = Monomial(5, {'x': 1, 'y': 1})
        >>> b = Monomial(15, {'x': 1})
        >>> a.gcd(b)
        Monomial(5, {'x': 1})

        It works only with integer coefficient/numbers
        different from zero

        >>> a.gcd(3.14)
        Traceback: (most recent call last)
        ...
        ValueError: Monomial coefficient must be int
        >>> b.gcd(0)
        Traceback: (most recent call last)
        ...
        ValueError: Value can't be equal to zero

        NB. the result will be always positive

        >>> c = Monomial(-30, {'x': 1, 'y': 1})
        >>> b.gcd(c)
        Monomial(15, {'x': 1})

        If you want to calculate the gcd with more
        operators, you can just do

        >>> from functools import reduce
        >>> monomials = (a, b, c)
        >>> reduce(lambda m1, m2: m1.gcd(m2), monomials)
        Monomial(30, {'x': 1})

        :type others: Monomial, int, float
        :rtype: Monomial, int
        :raise: TypeError, ValueError
        """

        # Check types of the operators
        if isinstance(other, int):
            other = Monomial(other, {})
        elif isinstance(other, Monomial):
            if any(isinstance(m.coefficient, float) for m in [self, other]):
                raise ValueError("Monomial coefficient must be int")
        else:
            raise TypeError("Can't calculate gcd between Monomials " + \
                            f" and {type(other)}")

        # Check value of the operators
        if self.coefficient == 0 or other.coefficient == 0:
            raise ValueError("Value can't be equal to zero")

        # Calculate the gcd of the coefficients
        coefficient = int(gcd(self.coefficient, other.coefficient))

        # Calculate the gcd of the variables
        variables = VariablesDict()
        for variable in self.variables:
            if variable in other.variables:
                variables[variable] = min(self.variables[variable],
                                          other.variables[variable])

        return Monomial(coefficient, variables)

    def lcm(self, other):
        """
        Calculate the least common multiple
        of two or monomials (or numbers)

        >>> a = Monomial(2, {'x': 1, 'y': 1})
        >>> b = Monomial(-9, {'y': 3})
        >>> a.lcm(b)
        Monomial(18, {'x': 1, 'y': 3})

        If you want to know others informations
        like errors and limits, please check the
        documentation of Monomial().gcd()

        :type others: Monomial, int, float
        :rtype: Monomial, int, float
        :raise: TypeError, ValueError
        """

        return abs(self * other) / self.gcd(other)

    ### Operations Methods ###

    def __add__(self, other):
        """
        Return the sum of this monomial and another one
        If the monomials are not similar, the result
        will be a polynomial.

        :type other: Monomial, 0
        :rtype: Monomial, Polynomial, NotImplemented, 0
        :raise: TypeError
        """

        if other == (-self):
            return 0
        elif other == 0:
            return self
        elif self.similar_to(other):
            return Monomial(self.coefficient + other.coefficient,
                            self.variables)
        elif isinstance(other, Monomial):
            from .polynomials import Polynomial
            return Polynomial(self, other)
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        Return the subtraction between this monomial
        and another one. If the monomials are not
        similar , the result will be a polynomial

        :type other: Monomial, 0
        :rtype: Monomial, Polynomial, NotImplemented, 0
        :raise: TypeError
        """

        return self + (-other)

    def __mul__(self, other):
        """
        Multiplicate this monomial for another
        monomial or for a number (int / float)

        :type other: Monomial, int, float
        :rtype: Monomial, NotImplemented
        :raise: TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        if isinstance(other, Monomial):
            coefficient = self.coefficient * other.coefficient
            variables = self.variables + other.variables
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

        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        if isinstance(other, Monomial):
            coefficient = self.coefficient / other.coefficient
            if isinstance(coefficient, float) and coefficient.is_integer:
                coefficient = int(coefficient)
            variables = self.variables - other.variables
            if variables == {}:
                return coefficient
            else:
                return Monomial(coefficient, variables)
        else:
            return NotImplemented

    def __pow__(self, exp):
        """
        Raise a monomial to power

        :type exp: int
        :rtype: Monomial, NotImplemented
        :raise: ValueError, TypeError
        """

        # Raise an error if the exponent is not an integer
        if not isinstance(exp, int):
            return NotImplemented

        # Raise an error if exponent is negative
        if not abs(exp) == exp:
            raise ValueError("Exponent can't be negative")

        # Raise the variables to power
        variables = VariablesDict()
        for var in self.variables:
            variables[var] = self.variables[var] * exp

        return Monomial(self.coefficient ** exp, variables)

    def __rmul__(self, other):
        """
        Multiply a number (int / float) for a monomial

        :type other: int, float
        :rtype: Monomial, NotImplemented
        :raise: TypeError
        """

        try:
            return self.__mul__(other)
        except TypeError:
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

        result = self.coefficient
        for var in self.variables:
            result *= (values[var]**self.variables[var])
        return result

    def __str__(self):
        """
        Return the monomial as a string (without *)

        :rtype: str
        """
        variables = ""
        for letter in sorted(self.variables.keys()):
            if self.variables[letter] > 1:
                variables += f"{letter}^{self.variables[letter]}"
            else:
                variables += letter

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
        :rtype: bool, NotImplemented
        :raise: TypeError
        """
        if isinstance(other, Monomial):
            return self.coefficient == other.coefficient \
                and self.variables == other.variables
        elif self.variables == {}:
            return self.coefficient == other
        else:
            return NotImplemented

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
        Return the monomial as a string

        :rtype: str
        """

        return f"Monomial({self.coefficient}, {self.variables})"

    def __hash__(self):
        """
        Return the hash for the Monomial

        :rtype: int
        """

        if self.variables == {}:
            return hash(self.coefficient)

        variables = map(lambda l: f"{l}{self.variables[l]}",
                        set(self.variables.elements()))

        return hash((self.coefficient, ) + tuple(variables))
