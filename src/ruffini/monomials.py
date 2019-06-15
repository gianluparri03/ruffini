from functools import reduce
from fractions import _gcd
from collections import Counter, defaultdict


def _lcm(x, y): return int((x*y) / _gcd(x, y))


class Monomial:

    def __init__(self, coefficient=1, variables=[]):
        """
        Create a Monomial object, made by an integer
        or floating coefficient (1 for default) and
        a list of variables, empty for default.

        :param coefficient: The coefficient of the monomial
        :type coefficient: int, float
        :param variables: The variables of the monomial
        :type coefficient: list of string
        """

        # Initialize the monomial
        self.coefficient = coefficient
        self.variables = variables
        self.regroup_variables()

    ### Utility Methods ###

    def regroup_variables(self):
        """
        Rewrite the monomial variables regrouping
        them in a smaller list:

        >>> a = Monomial(14, ["x", "y", "x^2"])
        >>> a.variables
        ['x^3', 'y']

        N.B.: This method is automatically executed
        when a monomial is initialized.

        It also calculate the degrees for every
        variable and store them in a dictionary
        and their sum in another variable:

        >>> a = Monomial(14, ["x", "y", "x^2"])
        >>> a.degrees["x"]
        3
        >>> a.degree # Sum of all the degrees
        4

        :raise: ValueError
        """

        counter = Counter()
        self.degrees = defaultdict(lambda: 0)

        # Extract letters and exponents
        for var in self.variables:
            if any([n in var for n in map(str, range(10))]) and "^" not in var:
                raise ValueError(f"'{var}' is not a variable")
            letter = var.split("^")[0]
            if "^" in var:
                exponent = var.split("^")[1]
                exponent = exponent.replace("(", "")
                exponent = exponent.replace(")", "")
                exponent = int(eval(exponent))
            else:
                exponent = 1

            counter[letter] += exponent

        # Rewrite the variables
        self.variables = list()
        for var, exp in counter.items():
            if exp == 0:
                continue
            elif exp < 0:
                raise ValueError("Not a monomial (negative exponent)")
            elif exp == 1:
                self.degrees[var] = 1
                self.variables.append(var)
            else:
                self.degrees[var] = exp
                self.variables.append(var + "^" + str(exp))

        self.variables.sort()
        self.degree = sum(self.degrees.values())

    def similar_to(self, other):

        from .polynomials import Polynomial

        """
        This method is used to check if two monomials
        are similar, so if they've got the same
        variables, basically:

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> a.similar_to(b)
        False
        >>> a.similar_to(c)
        True

        It can also check between a monomial and a
        polynomial with only a term
        >>> a.similar_to(Polynomial(a))
        True

        To see an example of Monomial.similar_to(Polynomial),
        please see the Polynomial.__sub__() section

        :type other: Monomial, Polynomial
        :rtype: bool
        """

        if isinstance(other, type(self)):
            return self.variables == other.variables
        elif isinstance(other, Polynomial):
            return other == self
        else:
            return False

    def gcd(self, *others):
        """
        This method returns the greatest common divisor
        of two or more monomials (*others):

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> print(a.gcd(b, c))
        x

        :param others: The others monomial 
        :type others: Monomial
        :rtype: Monomial
        """
        monomials = self, *others

        # Calculate the gcd of the coefficients
        coefficients = [m.coefficient for m in monomials]
        coefficient = reduce(_gcd, sorted(coefficients))
        if 0 < coefficient < 1:
            coefficient = 1

        # Calculate the gcd of the variables
        variables = {}
        degrees = [m.degrees for m in monomials]
        for letter in degrees[0]:
            if all(letter in d for d in degrees):
                variables[letter] = max(d[letter] for d in degrees)

        variables = [f"{l}^{variables[l]}" for l in variables]

        return Monomial(coefficient, variables)

    def lcm(self, *others):
        """
        This method returns the least common multiple
        of two or more monomials (*others):

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> print(a.lcm(b, c))
        520xy

        :param others: The others monomial 
        :type others: Monomial
        :rtype: Monomial
        """

        if not all(type(m) == Monomial for m in others):
            raise TypeError("can calculate lcm only between monomials")

        monomials = self, *others

        # Calculate the lcm of the coefficients
        coefficients = [m.coefficient for m in monomials]
        coefficient = reduce(_lcm, coefficients)

        # Calculate the lcm of the variables
        variables = {}
        degrees = [m.degrees for m in monomials]
        for letter in degrees[0]:
            variables[letter] = min(filter(
                lambda x: x != 0, (d[letter] for d in degrees)))

        # Rewrite the variables
        variables = [f"{l}^{variables[l]}" for l in variables]

        return Monomial(coefficient, variables)

    def eval(self, **values):
        """
        Evaluate the monomial, giving the values
        of the variables to the method

        >>> Monomial(5, ["x"]).eval(x=2)
        10
        >>> Monomial(-1, ["x", "y"]).eval(x=8, y=3)
        -24

        If a value isn't specified, the method
        will raise an error

        >>> Monomial(1.2, ["a", "b"]).eval(b=3)
        Traceback (most recent call last):
        ...
        KeyError: 'a'

        :type values: int, float
        :rtype: int, float
        :raise: KeyError
        """

        r = "*".join(map(str, self.variables))
        for var in self.variables:
            r = r.replace(var, str(values[var]))
        return eval(r) * self.coefficient

    ### Operations Methods ###

    def __add__(self, other):

        from .polynomials import Polynomial

        """
        Return the sum of this monomial
        and another one, which is by the
        sum of the coefficients and the variables
        (which are equals in the two monomials)

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> d = Monomial(2.3, ["x", "y"])
        >>> print(a + c)
        -8xy
        >>> print(d + c)
        -10.7xy
        >>> print(a + d)
        7.3xy

        If the monomials are not similar or the second
        operator is a polynomial, the result will be
        a polynomial
        >>> print(d + b) # They're not similar
        2.3xy +8x

        To see an example of Monomial + Polynomial,
        please see the Polynomial.__add__() section

        :type other: Monomial, Polynomial
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        # monomial
        if self.similar_to(other):
            return Monomial(self.coefficient + other.coefficient,
                            self.variables)

        # monomial (not similar)
        elif isinstance(other, type(self)):
            return Polynomial(self, other)

        # polynomial
        elif isinstance(other, Polynomial):
            return Polynomial(self, *other)

        else:
            raise TypeError("unsupported operand type(s) for +:"
                            f" 'Monomial' and '{type(other).__name__}'")

    def __sub__(self, other):

        from .polynomials import Polynomial

        """
        Return the subtraction between this
        monomial and another one, which is the
        subtraction between the coefficients
        and the variables (which are equals
        in the two monomials)

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(13, ["x", "y"])
        >>> d = Monomial(-2, ["x", "y"])
        >>> print(a - c)
        -8xy
        >>> print(c - a)
        8xy
        >>> print(c - d)
        15xy

        If the monomials are not similar or the second
        operator is a polynomial, the result will be
        a polynomial
        >>> print(d - b) # not similar
        -2xy -8x

        To see an example of Monomial - Polynomial,
        please see the Polynomial.__sub__() section

        :type other: Monomial, Polynomial
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        # monomial
        if self.similar_to(other):
            return Monomial(self.coefficient - other.coefficient,
                            self.variables)

        # monomial (not similar)
        elif isinstance(other, type(self)):
            return Polynomial(self, -other)

        # polynomial
        elif isinstance(other, Polynomial):
            return Polynomial(self, *(-other))

        else:
            raise TypeError("unsupported operand type(s) for -:"
                            f" 'Monomial' and '{type(other).__name__}'")

    def __mul__(self, other):

        from .polynomials import Polynomial

        """
        Return the multiplication of this
        monomial and another one, which can
        be a monomial or a number too

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> print(a * b)
        40x^2y
        >>> print(c * a)
        -65x^2y^2
        >>> print(c * 2)
        -26xy
        >>> print(b * 1.3)
        10.4x

        To see an example of Monomial * Polynomial,
        please see the Polynomial.__mul__() section

        :type other: Monomial, int, float, Polynomial
        :rtype: Monomial, Polynomial
        :raise: TypeError
        """

        # int or float
        if isinstance(other, float) or isinstance(other, int):
            return Monomial(self.coefficient * other, self.variables)

        # monomial
        elif isinstance(other, type(self)):
            return Monomial(self.coefficient * other.coefficient,
                            self.variables + other.variables)
        # polynomial
        elif isinstance(other, Polynomial):
            return other * self
        else:
            raise TypeError("unsupported operand type(s) for *:"
                            f" 'Monomial' and '{type(other).__name__}'")

    def __truediv__(self, other):
        """
        Return the division between this
        monomial and another one, which can
        be a monomial or a number too

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-10, ["x", "y"])
        >>> print(a / b)
        0.625y
        >>> print(a / c)
        -0.5
        >>> print(c / -2)
        5.0xy
        >>> print(b / a) #= 1.6y^(-1), it is not a monomial
        Traceback (most recent call last):
        ...
        ValueError: Not a monomial (negative exponent)

        :type other: Monomial, int, float
        :rtype: Monomial
        :raise: ValueError, TypeError
        """

        # Make an exception for integer / float
        if isinstance(other, int) or isinstance(other, float):
            return Monomial(self.coefficient / other, self.variables)
        elif isinstance(other, type(self)):
            # Divide the variables
            variables = self.variables[:]
            for var in other.variables:
                letter = var.split("^")[0]
                if "^" in var:
                    exponent = - int(var.split("^")[1])
                else:
                    exponent = -1
                variables.append(letter + "^" + str(exponent))

            return Monomial(self.coefficient / other.coefficient,
                            variables)
        else:
            raise TypeError("unsupported operand type(s) for /:"
                            f" 'Monomial' and '{type(other).__name__}'")

    def __pow__(self, n):
        """
        Raise a monomial to power

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(16, ["x^6"])
        >>> print(a ** 2)
        25x^2y^2
        >>> print(b ** 3)
        512x^3
        >>> print(c ** .5) # square root
        4.0x^3

        :type n: int, float
        :rtype: monomial
        :raise: ValueError, TypeError
        """

        # Raise an error if the exponent is not a number
        if not (isinstance(n, int) or isinstance(n, float)):
            raise TypeError("unsupported operand type(s) for **:"
                            f" 'Monomial' and '{type(other).__name__}'")

        # Raise the variables to power
        variables = []
        for var in self.variables:
            letter = var.split("^")[0]
            if "^" in var:
                exponent = int(var.split("^")[1]) * n
            else:
                exponent = n
            variables.append(letter + "^" + str(exponent))

        return Monomial(self.coefficient ** n, variables)

    ### Magic Methods ###

    def __hash__(self):
        """
        __hash__ method is a magic method for useful
        for python. You can access it by calling the
        hash() function, giving the monomial as argument.
        Thanks to this method you can create a set of
        monomials, for example.

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> m = {m1, m2, m3}
        >>> # No error is raised (without __hash__ would
        >>> # be raised a TypeError)

        :rtipe: int
        """
        return hash(str(self))

    def __str__(self):
        """
        Return the monomial as a string (without *
        operator):

        >>> str(Monomial(14, ["x", "y"]))
        '14xy'
        >>> str(Monomial(-1+3, ["a"]))
        '2a'
        >>> str(Monomial(1, ["y", "y"]))
        'y^2'

        :rtype: str
        """
        if self.coefficient == 1 and self.variables:
            return ''.join(self.variables)
        elif self.coefficient == -1 and self.variables:
            return '-' + ''.join(self.variables)
        elif self.coefficient == 0:
            return '0'
        elif self.coefficient == 1 and not self.variables:
            return '1'
        elif self.coefficient == -1 and not self.variables:
            return '-1'
        else:
            return str(self.coefficient) + ''.join(self.variables)

    def __eq__(self, other):
        """
        Check if two monomials are equivalent,
        simply comparating the coefficients and
        the variables

        >>> Monomial(14, ["a"]) == Monomial(14, ["a"])
        True
        >>> Monomial(14, ["a"]) == Monomial(14, ["a^2"])
        False
        >>> Monomial(14, ["a"]) == Monomial(-14, ["a"])
        False
        >>> Monomial(14, ["a"]) == Monomial(19, ["a"])
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

        >>> print(-Monomial(14, ["x"]))
        -14x
        >>> print(-Monomial(-8, ["b"]))
        8b

        :rtype: Monomial
        """
        return Monomial(-self.coefficient, self.variables)

    def __abs__(self):
        """
        Return the absolute value of the monomial
        (the monomial without the sign) calculating
        the absolute value of the coefficient:

        >>> print(abs(Monomial(14, ["x"])))
        14x
        >>> print(abs(Monomial(-8, ["b"])))
        8b

        :rtype: Monomial
        """
        return Monomial(abs(self.coefficient), self.variables)

    def __round__(self, n=0):
        """
        This method is used to round the
        coefficient of the monomial with a custom
        number of decimals (n, default 0)

        >>> print(round(Monomial(15.3918, ["c"])))
        15.0c
        >>> print(round(Monomial(15.3918, ["c"]), 2))
        15.39c

        :param n: Numbers of decimals
        :type n: int
        :rtype: Monomial
        """
        return Monomial(round(self.coefficient, n), self.variables)
