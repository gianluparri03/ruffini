from math import gcd, sqrt

from .variables import VariablesDict


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
    and divided togheter (and with numbers).
    lcm and gcd between monomials (and numbers) is
    available, too.

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

        >>> print(Monomial(17, {'k': 3}))
        17k**3

        The variables will be stored in a VariableDict, so:

        - all the letters will be made lowercase
        - the letters can be only alphabetical and
          with a lenght of one character
        - the exponent must be positive and integer

        >>> type(Monomial(3, {'a': 5}).variables)
        <class 'ruffini.variables.VariablesDict'>

        When initialized the monomial, this method calculates
        the monomial's total degree (the sum of all the degrees)

        >>> Monomial(-2, {'a': 2, 'b': 1, 'c': 3}).degree
        6

        It also calculates if the monomial is a cube or a square

        >>> Monomial(4, {'a': 2, 'k': 4}).is_square
        True
        >>> Monomial(6, {'b': 27}).is_cube
        False

        **NB** if the coefficient is instance of float
        but it's a whole number (such as 18.0), it will
        be transformed in 18

        >>> Monomial(7.0, {'a': 2})
        Monomial(7, {'a': 2})

        :type coefficient: int, float
        :type coefficient: dict, VariablesDict
        :raise: ValueError, TypeError
        """

        # Check the coefficient
        if isinstance(coefficient, float) and coefficient.is_integer():
            self.coefficient = int(coefficient)
        elif isinstance(coefficient, (int, float)):
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

        # Check if it's a square or a cube
        if self.coefficient < 0:
            self.is_square = False
            self.is_cube = ((-self.coefficient) ** (1./3.)).is_integer() and self.variables % 3

        elif self.coefficient > 0:
            self.is_square = sqrt(self.coefficient).is_integer() and self.variables % 2
            self.is_cube = (self.coefficient ** (1./3.)).is_integer() and self.variables % 3

        else:
            self.is_square = False
            self.is_cube = False

    ### Utility Methods ###

    def similar_to(self, other):
        """
        Check if two monomials are similar (if
        the have the same variables).

        >>> m1 = Monomial(3, {'x': 1, 'y': 1})
        >>> m2 = Monomial(-6, {'x': 1, 'y': 3})
        >>> m3 = Monomial(2.6, {'x': 1, 'y': 1})
        >>> m4 = Monomial(3.14, {})
        >>> m1.similar_to(m4)
        False
        >>> m1.similar_to(m3)
        True

        If the second operand is not a monomial
        the result will always be False

        >>> m3.similar_to("")
        False
        >>> m4.similar_to({})
        False

        The only one exception is when the
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
        Traceback (most recent call last):
        ...
        TypeError: Can't calculate gcd between Monomial and float
        >>> a.gcd(Monomial(3.14, {}))
        Traceback (most recent call last):
        ...
        ValueError: Monomial coefficient must be int
        >>> b.gcd(0)
        Traceback (most recent call last):
        ...
        ValueError: Value can't be equal to zero

        **NB** the result will be always positive

        >>> c = Monomial(-30, {'x': 1, 'y': 1})
        >>> b.gcd(c)
        Monomial(15, {'x': 1})

        If you want to calculate the gcd with more
        operators, you can just do

        >>> from functools import reduce
        >>> reduce(lambda m1, m2: m1.gcd(m2), (a, b, c))
        Monomial(5, {'x': 1})

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
            raise TypeError("Can't calculate gcd between Monomial"
                            f" and {type(other).__name__}")

        # Check value of the operators
        if self.coefficient == 0 or other.coefficient == 0:
            raise ValueError("Value can't be equal to zero")

        # Calculate the gcd of the coefficients
        coefficient = int(gcd(self.coefficient, other.coefficient))

        # Calculate the gcd of the variables
        variables = {}
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
        As the name say, this method is used
        to sum two monomials, or a number, too

        >>> Monomial(5, {'x': 1, 'y':3}) + Monomial(-1.52, {'x':1, 'y':3})
        Monomial(3.48, {'x': 1, 'y': 3})

        >>> Monomial(1, {'z': 1}) + 17
        Polynomial(Monomial(1, {'z': 1}), Monomial(17, {}))

        You can also add a polynomial (in this case,
        it will use the :func:`Polynomial.__add__` method)

        >>> from ruffini import Polynomial
        >>> print(Monomial(1, {'a': 2}) + Polynomial(Monomial(2, {'b': 1})))
        2b +a**2

        Otherwise, it will raise a TypeError

        >>> Monomial(2, {'z': 1}) - ""
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for -: 'Monomial' and 'str'

        :type other: Monomial, Polynomial, int, float
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        from . import Polynomial

        if isinstance(other, Monomial):
            # Opposite monomial
            if self == -other:
                return Monomial(0, {})

            # Simil monomial
            elif self.similar_to(other):
                return Monomial(self.coefficient + other.coefficient, self.variables)

            # Generic monomial
            else:
                return Polynomial(self, other)

        elif isinstance(other, (int, float)):
            if self.variables.empty:
                return Monomial(self.coefficient + other, {})

            else:
                return Polynomial(self, other)

        elif isinstance(other, Polynomial):
            return other + self

        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Monomial' and '{other.__class__.__name__}'")

    def __sub__(self, other):
        """
        Return the subtraction between this monomial
        and another one

        >>> Monomial(5, {'x': 1}) - Monomial(3, {'x': 1})
        Monomial(2, {'x': 1})

        If the monomials are not similar or the second
        operator is a number, the result will be a
        polynomial

        >>> Monomial(5, {'x': 1, 'y': 3}) - Monomial(3, {'x': 1})
        Polynomial(Monomial(5, {'x': 1, 'y': 3}), Monomial(-3, {'x': 1}))
        >>> Monomial(17, {'a': 1, 'b': 1}) - 2.5
        Polynomial(Monomial(17, {'a': 1, 'b': 1}), Monomial(-2.5, {}))

        You can also subtract a polynomial (in this case,
        it will use the :func:`Polynomial.__sub__` method)

        >>> from ruffini import Polynomial
        >>> print(Monomial(1, {'a': 2}) - Polynomial(Monomial(2, {'b': 1})))
        -2b +a**2

        Otherwise, it will raise a TypeError

        >>> Monomial(2, {'z': 1}) - ""
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for -: 'Monomial' and 'str'

        :type other: Polynomial, Monomial, int, float
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        from . import Polynomial

        if isinstance(other, (Polynomial, Monomial, int, float)):
            return self + (-other)

        else:
            raise TypeError(f"unsupported operand type(s) for -: 'Monomial' and '{other.__class__.__name__}'")

    def __mul__(self, other):
        """
        Multiplicate this monomial by another
        monomial or a number (int / float)

        >>> Monomial(5, {'x': 1, 'y': 2}) * Monomial(2, {'a': 1, 'b': 1})
        Monomial(10, {'a': 1, 'b': 1, 'x': 1, 'y': 2})
        >>> Monomial(3, {'c': 2}) * 5
        Monomial(15, {'c': 2})
        >>> Monomial(1, {'k': 3}) * Monomial(1, {'k': 3})
        Monomial(1, {'k': 6})

        Also multiplication by a polynomial is enabled
        (it will use the :func:`Polynomial.__mul__` method)

        >>> from ruffini import Polynomial
        >>> print(Monomial(1, {'a': 2}) * Polynomial(Monomial(2, {'b': 1})))
        2a**2b

        If the second operator isn't mentioned
        above, it will raise a TypeError

        >>> Monomial(4, {}) * {}
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for *: 'Monomial' and 'dict'

        :type other: Polynomial, Monomial, int, float
        :rtype: Polynomial, Monomial
        :raise: TypeError
        """

        from . import Polynomial

        # numbers
        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        # monomials
        if isinstance(other, Monomial):
            coefficient = self.coefficient * other.coefficient
            variables = self.variables + other.variables

            return Monomial(coefficient, variables)

        # polynomials
        elif isinstance(other, Polynomial):
            return other * self

        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Monomial' and '{other.__class__.__name__}'")

    def __truediv__(self, other):
        """
        Divide this monomial by another monomial or
        by a number (int / float)

        >>> Monomial(6, {'a': 3}) / Monomial(3, {'a': 1})
        Monomial(2, {'a': 2})
        >>> Monomial(18, {'k': 3}) / 6
        Monomial(3, {'k': 3})
        >>> Monomial(27, {'x': 6}) / Monomial(3, {'x': 6})
        Monomial(9, {})

        If second monomial's variable's exponent
        are higher than first's, it will raise a
        ValueError

        >>> Monomial(5, {}) / Monomial(4, {'x': 1})
        Traceback (most recent call last):
        ...
        ValueError: Exponent must be positive

        Otherwise, if the second operator isn't a monomial
        or a number, it will raise a TypeError

        >>> Monomial(30, {}) / {}
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for /: 'Monomial' and 'dict'

        :type other: Monomial, int, float
        :rtype: Monomial
        :raise: ValueError, TypeError
        """

        if isinstance(other, (int, float)):
            other = Monomial(other, {})

        if isinstance(other, Monomial):
            coefficient = self.coefficient / other.coefficient
            variables = self.variables - other.variables
            return Monomial(coefficient, variables)

        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Monomial' and '{other.__class__.__name__}'")

    def __pow__(self, exp):
        """
        Raise a monomial to power

        >>> Monomial(5, {'x': 1}) ** 2
        Monomial(25, {'x': 2})
        >>> Monomial(4, {'c': 6}) ** 3
        Monomial(64, {'c': 18})

        If the exponent is 0, the result will be always 1

        >>> Monomial(5, {'k': 6}) ** 0
        1

        If the monomial is a square, you can
        calcolate the square root

        >>> Monomial(4, {'x': 2}).is_square
        True
        >>> Monomial(4, {'x': 2}) ** (1/2)
        Monomial(2, {'x': 1})

        You can do the same thing with a cube

        >>> Monomial(27, {'y': 6}).is_cube
        True
        >>> Monomial(27, {'y': 6}) ** (1/3)
        Monomial(3, {'y': 2})

        In all the other cases, a float exponent
        will raise a TypeError

        >>> Monomial(3.14, {'a': 3}) ** 2.5
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for ** or pow(): 'Monomial' and 'float'

        When the exponent is negative, it will raise
        a ValueError

        >>> Monomial(17, {'k': 1}) ** (-1)
        Traceback (most recent call last):
        ...
        ValueError: Exponent can't be negative


        :type exp: int
        :rtype: Monomial
        :raise: ValueError, TypeError
        """

        # if the exponent is not an integer...
        if not isinstance(exp, int):
            # if the monomial is a square and the exponent
            # is 1/2, return the square root
            if exp == 1/2 and self.is_square:
                return Monomial(int(sqrt(self.coefficient)), self.variables / 2)

            # if the monomial is a cube and the exponent
            # is 1/3, return the cube root
            elif exp == 1/3 and self.is_cube:
                return Monomial(int(self.coefficient ** (1/3)), self.variables / 3)

            # otherwise raise an error
            else:
                raise TypeError(f"unsupported operand type(s) for ** or pow(): 'Monomial' and '{exp.__class__.__name__}'")

        # return 1 if the exponent is 0
        if exp == 0:
            return 1

        # Raise an error if exponent is negative
        elif not exp > 0:
            raise ValueError("Exponent can't be negative")

        return Monomial(self.coefficient ** exp, self.variables * exp)

    ### Reversed Operations Method ###

    def __radd__(self, other):
        """
        This function is the reverse for :func:`Monomial.__add__`.
        With this function, you can swap the two operands
        of the addition:

        >>> 18 + Monomial(3, {})
        Monomial(21, {})

        For more informations, see :func:`Monomial.__add__` docs.

        :type other: Polynomial, int, float
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        try:
            return self + other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for +: '{other.__class__.__name__}' and 'Monomial'")

    def __rsub__(self, other):
        """
        This function is the reverse for :func:`Monomial.__sub__`.
        With this function, you can swap the two operands
        of the subtraction:

        >>> 9 - Monomial(4, {})
        Monomial(5, {})

        For more informations, see :func:`Monomial.__sub__` docs.

        :type other: Polynomial, int, float
        :rtype: Polynomial, Monomial, int, float
        :raise: TypeError
        """

        try:
            return (- self) + other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for -: '{other.__class__.__name__}' and 'Monomial'")

    def __rmul__(self, other):
        """
        This function is the reverse for :func:`Monomial.__mul__`.
        With this function, you can swap the two operands
        of the multiplication:

        >>> 5 * Monomial(2, {'x': 2})
        Monomial(10, {'x': 2})

        For more informations, see :func:`Monomial.__mul__` docs.

        :type other: Polynomial, int, float
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        try:
            return self * other
        except TypeError:
            raise TypeError(f"unsupported operand type(s) for *: '{other.__class__.__name__}' and 'Monomial'")

    def __rtruediv__(self, other):
        """
        This function is the reverse for :func:`Monomial.__truediv__`.
        With this function, you can swap the two operands
        of the division:

        >>> 8 / Monomial(4, {})
        Monomial(2, {})

        For more informations, see :func:`Monomial.__truediv__ docs`.

        :type other: int, float
        :rtype: Monomial
        :raise: ValueError, TypeError
        """

        if not isinstance(other, (int, float)):
            raise TypeError(f"unsupported operand type(s) for /: '{other.__class__.__name__}' and 'Monomial'")

        if self.variables:
            raise ValueError("Exponent must be positive")

        return Monomial(other/self.coefficient, {})

    ### Magic Methods ###

    def __call__(self, **values):
        """
        Evaluate the monomial, giving the values
        of the variables to the method

        >>> m = Monomial(5, {'x': 1, 'y': 1})
        >>> m(x=2, y=3)
        30

        If you omit some variables values, the
        variables will remain there

        >>> m(x=2)
        Monomial(10, {'y': 1})

        You can declare some variables values
        which aren't in the monomial and the
        result won't change

        >>> m(b=7)
        Monomial(5, {'x': 1, 'y': 1})

        **NB** as for the initialization, the variable
        isn't case sensitive

        >>> m(x=2) == m(X=2)
        True


        :type values: int, float
        :rtype: int, float, Monomial
        :raise: TypeError
        """

        coefficient = self.coefficient
        variables = {}
        values = dict(zip(map(lambda v: v.lower(), values.keys()), values.values()))

        # substitute values
        for var in self.variables:

            if var in values and isinstance(values[var], (int, float)):
                coefficient *= (values[var] ** self.variables[var])
            elif var in values:
                raise TypeError(f"{var}'s value can't be set to {values[var]}")
            else:
                variables[var] = self.variables[var]

        # if there are no variables left return an int/float
        if not variables:
            return coefficient

        return Monomial(coefficient, variables)

    def __str__(self):
        """
        Return the monomial as a string in a human-readable
        mode. Normally, it will return the coefficient and
        the variables without spaces or *.
        The power is indicated with **.

        Examples:

        Normal monomial:

        >>> print(Monomial(5, {'x': 1, 'y': 1}))
        5xy

        coefficient = 1 and there are variables

        >>> print(Monomial(1, {'a': 2}))
        a**2

        coefficient = -1 and there are variables

        >>> print(Monomial(-1, {'k': 3}))
        -k**3

        coefficient = 0

        >>> print(Monomial(0, {'s': 5}))
        0

        coefficient = 1 and there aren't variables

        >>> print(Monomial(1, {}))
        1

        coefficient = -1 and there aren't variables

        >>> print(Monomial(-1, {}))
        -1

        **NB** the variables are displayed in
        alphabetical order

        >>> print(Monomial(5, {'k': 2, 'b': 3}))
        5b**3k**2

        :rtype: str
        """

        variables = ""

        # order the variables
        for letter in sorted(self.variables.keys()):
            if self.variables[letter] > 1:
                variables += f"{letter}**{self.variables[letter]}"
            else:
                variables += letter

        # coefficient == 1 w/ variables
        if self.coefficient == 1 and variables:
            return variables

        # coefficient == -1 and w/ variables
        elif self.coefficient == -1 and self.variables:
            return '-' + variables

        # coefficient == 0
        elif self.coefficient == 0:
            return '0'

        # coefficient == 1 w/o variables
        elif self.coefficient == 1 and not self.variables:
            return '1'

        # coefficient == -1 w/o variables
        elif self.coefficient == -1 and not self.variables:
            return '-1'

        # normal monomial
        else:
            return str(self.coefficient) + variables

    def __repr__(self):
        """
        Return the monomial as a string

        >>> Monomial(5, {'x': 5})
        Monomial(5, {'x': 5})
        >>> Monomial(-1, {'a': 2, 'c': 3})
        Monomial(-1, {'a': 2, 'c': 3})

        **NB** the variables are displayed in
        alphabetical order

        >>> Monomial(5, {'k': 2, 'b': 3})
        Monomial(5, {'b': 3, 'k': 2})

        :rtype: str
        """

        return f"Monomial({self.coefficient}, {self.variables})"

    def __eq__(self, other):
        """
        Check if two monomials are equivalent,
        comparing coefficients and variables

        >>> Monomial(5, {'x': 1}) == Monomial(5, {'x': 1})
        True

        If there are no variables, it can be
        compared also to a number

        >>> Monomial(4, {}) == 4
        True

        If the second operator isn't a monomial or
        a number, it will return False.

        :type other: Monomial, int, float
        :rtype: bool
        :raise: TypeError
        """

        # monomial == monomial
        if isinstance(other, Monomial):
            return self.coefficient == other.coefficient \
                and self.variables == other.variables

        # monomial == int, float
        elif isinstance(other, (int, float)) and self.variables.empty:
            return self.coefficient == other

        else:
            return False

    def __neg__(self):
        """
        Return the opposite of the monomial,
        inverting the coefficient

        >>> - Monomial(5, {'x': 1, 'y': 1})
        Monomial(-5, {'x': 1, 'y': 1})
        >>> - Monomial(-3, {'a': 1, 'b': 4})
        Monomial(3, {'a': 1, 'b': 4})

        :rtype: Monomial
        """
        return Monomial(-self.coefficient, self.variables)

    def __abs__(self):
        """
        Return the absolute value of the monomial,
        calculating the absolute value of the coefficient

        >>> abs(Monomial(-3, {'a': 1, 'b': 4}))
        Monomial(3, {'a': 1, 'b': 4})
        >>> abs(Monomial(5, {'x': 1, 'y': 1}))
        Monomial(5, {'x': 1, 'y': 1})

        :rtype: Monomial
        """
        return Monomial(abs(self.coefficient), self.variables)

    def __hash__(self):
        """
        Return the hash for the Monomial

        >>> hash(Monomial(1, {'a': 1})) == hash(Monomial(1, {'a': 1}))
        True

        The hash for 8xy, for example, is equal
        to the hash of (8, ('x', 1), ('y', 1)).

        If the monomial has no variables, its hash
        will be equal to the coefficient's hash

        >>> hash(Monomial(3, {})) == hash(3)
        True

        :rtype: int
        """

        if self.variables == {}:
            return hash(self.coefficient)

        variables = ((k, self.variables[k]) for k in self.variables)

        return hash((self.coefficient, ) + tuple(list(variables)))
