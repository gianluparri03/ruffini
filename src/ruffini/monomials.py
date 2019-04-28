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
                raise ValueError("Not a monomial")
            elif exp == 1:
                self.degrees[var] = 1
                self.variables.append(var)
            else:
                self.degrees[var] = exp
                self.variables.append(var + "^" + str(exp))

        self.variables.sort()
        self.degree = sum(self.degrees.values())

    def similar_to(self, other):
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

        :type other: Monomial
        :rtype: bool
        """

        if not type(self) == type(other):
            raise ValueError("Not a monomial")

        return self.variables == other.variables

    def gcd(self, *others):
        """
        This method returns the greatest common divisor
        of two or more monomials (*others):

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> print(a.gcd(b, c))
        Monomial(1, ['x'])

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
        Monomial(520, ['x', 'y'])

        :param others: The others monomial 
        :type others: Monomial
        :rtype: Monomial
        """

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

    def __str__(self):
        """
        Return the monomial as a string (without *
        operator):

        >>> str(Monomial(14, ["x", "y"]))
        "Monomial(14, ['x', 'y'])"
        >>> str(Monomial(-1+3, ["a"]))
        "Monomial(2, ['a'])"
        >>> str(Monomial(1, ["y", "y"]))
        "Monomial(1, ['y^2'])"

        :rtype: str
        """

        return f"Monomial({self.coefficient}, {self.variables})"

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

    def __pos__(self):
        """
        Return the positive monomial, which
        is basically the monomial itself with
        no changes (implemented only for future
        purposes, now it has no utility)

        >>> print(+Monomial(14, ["x"]))
        Monomial(14, ['x'])
        >>> print(+Monomial(-8, ["b"]))
        Monomial(-8, ['b'])

        :rtype: Monomial
        """
        return self

    def __neg__(self):
        """
        Return the opposite of the monomial,
        inverting the coefficient:

        >>> print(-Monomial(14, ["x"]))
        Monomial(-14, ['x'])
        >>> print(-Monomial(-8, ["b"]))
        Monomial(8, ['b'])

        :rtype: Monomial
        """
        return Monomial(-self.coefficient, self.variables)

    def __abs__(self):
        """
        Return the absolute value of the monomial
        (the monomial without the sign) calculating
        the absolute value of the coefficient:

        >>> print(abs(Monomial(14, ["x"])))
        Monomial(14, ['x'])
        >>> print(abs(Monomial(-8, ["b"])))
        Monomial(8, ['b'])

        :rtype: Monomial
        """
        return Monomial(abs(self.coefficient), self.variables)

    def __round__(self, n=0):
        """
        This method is used to round the
        coefficient of the monomial with a custom
        number of decimals (n, default 0)

        >>> print(round(Monomial(15.3918, ["c"])))
        Monomial(15.0, ['c'])
        >>> print(round(Monomial(15.3918, ["c"]), 2))
        Monomial(15.39, ['c'])

        :param n: Numbers of decimals
        :type n: int
        :rtype: Monomial
        """
        return Monomial(round(self.coefficient, n), self.variables)

    def __add__(self, other):
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
        Monomial(-8, ['x', 'y'])
        >>> print(d + c)
        Monomial(-10.7, ['x', 'y'])
        >>> print(a + d)
        Monomial(7.3, ['x', 'y'])
        >>> print(d + b) # They're not similar
        Traceback (most recent call last):
        ...
        ValueError: The monomials are not similar

        :type other: Monomial
        :rtype: Monomial
        :raise: ValueError
        """
        if self.similar_to(other):
            return Monomial(self.coefficient + other.coefficient,
                            self.variables)
        else:
            raise ValueError("The monomials are not similar")

    def __sub__(self, other):
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
        Monomial(-8, ['x', 'y'])
        >>> print(c - a)
        Monomial(8, ['x', 'y'])
        >>> print(c - d)
        Monomial(15, ['x', 'y'])
        >>> print(d + b) # They're not similar
        Traceback (most recent call last):
        ...
        ValueError: The monomials are not similar

        :type other: Monomial
        :rtype: Monomial
        :raise: ValueError
        """
        return self + (-other)

    def __mul__(self, other):
        """
        Return the multiplication of this
        monomial and another one, which can
        be a monomial or a number too

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> print(a * b)
        Monomial(40, ['x^2', 'y'])
        >>> print(c * a)
        Monomial(-65, ['x^2', 'y^2'])
        >>> print(c * 2)
        Monomial(-26, ['x', 'y'])
        >>> print(b * 1.3)
        Monomial(10.4, ['x'])

        :type other: Monomial, int, float
        :rtype: Monomial
        """

        # Make an exception for integer / float
        if not type(other) == type(self):
            return Monomial(self.coefficient * other, self.variables)

        return Monomial(self.coefficient * other.coefficient,
                        self.variables + other.variables)

    def __truediv__(self, other):
        """
        Return the division between this
        monomial and another one, which can
        be a monomial or a number too

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-10, ["x", "y"])
        >>> print(a / b)
        Monomial(0.625, ['y'])
        >>> print(a / c)
        Monomial(-0.5, [])
        >>> print(c / -2)
        Monomial(5.0, ['x', 'y'])
        >>> print(b / a) #= 1.6y^(-1), it is not a monomial
        Traceback (most recent call last):
        ...
        ValueError: Not a monomial

        :type other: Monomial, int, float
        :rtype: Monomial
        :raise: ValueError
        """

        # Make an exception for integer / float
        if not type(other) == type(self):
            return Monomial(self.coefficient / other, self.variables)

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

    def __pow__(self, n):
        """
        Raise a monomial to power

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(16, ["x^6"])
        >>> print(a ** 2)
        Monomial(25, ['x^2', 'y^2'])
        >>> print(b ** 3)
        Monomial(512, ['x^3'])
        >>> print(c ** .5) # square root
        Monomial(4.0, ['x^3'])

        :type n: int, float
        :rtype: monomial
        :raise: ValueError
        """

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
