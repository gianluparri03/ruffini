from functools import reduce
from fractions import _gcd
from collections import Counter, defaultdict


def _lcm(x, y): return int((x*y) / _gcd(x, y))


class Monomial:

    def __init__(self, coefficient: int = 1, variables: list = []):
        """
        Create a Monomial object, made by an integer
        or floating coefficient (1 for default) and
        a list of variables, empty for default.
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

    def similar_to(self, other: 'Monomial') -> bool:
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
        """

        if not type(self) == type(other):
            raise ValueError("Not a monomial")

        return self.variables == other.variables

    def gcd(self, *others: 'Monomial') -> 'Monomial':
        """
        This method returns the greatest common divisor
        of two or more monomials (*others):

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> print(a.gcd(b, c))
        x
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

    def lcm(self, *others: 'Monomial') -> 'Monomial':
        """
        This method returns the least common multiple
        of two or more monomials (*others):

        >>> a = Monomial(5, ["x", "y"])
        >>> b = Monomial(8, ["x"])
        >>> c = Monomial(-13, ["x", "y"])
        >>> print(a.lcm(b, c))
        520xy
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

    def __str__(self) -> str:
        """
        Return the monomial as a string (without *
        operator):

        >>> str(Monomial(14, ["x", "y"]))
        '14xy'
        >>> str(Monomial(-1, ["a"]))
        '-a'
        >>> str(Monomial(1, ["y^2"]))
        'y^2'
        """

        variables = "".join(self.variables)
        coefficient = str(self.coefficient)

        # Some exceptions
        if coefficient == "1":
            coefficient = ""
        elif coefficient == "-1":
            coefficient = "-"
        elif coefficient == "0":
            return "0"

        monomial = coefficient + variables

        # Other exceptions
        if monomial == "":
            return "1"
        elif monomial == "-":
            return "-1"
        else:
            return monomial

    def __eq__(self, other) -> bool:
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
        """
        return self.coefficient == other.coefficient \
            and self.variables == other.variables

    def __pos__(self) -> 'Monomial':
        """
        Return the positive monomial, which
        is basically the monomial itself with
        no changes (implemented only for future
        purposes, now it has no utility)

        >>> print(+Monomial(14, ["x"]))
        14x
        >>> print(+Monomial(-8, ["b"]))
        -8b
        """
        return self

    def __neg__(self) -> 'Monomial':
        """
        Return the opposite of the monomial,
        inverting the coefficient:

        >>> print(-Monomial(14, ["x"]))
        -14x
        >>> print(-Monomial(-8, ["b"]))
        8b
        """
        return Monomial(-self.coefficient, self.variables)

    def __abs__(self) -> 'Monomial':
        """
        Return the absolute value of the monomial
        (the monomial without the sign) calculating
        the absolute value of the coefficient:

        >>> print(abs(Monomial(14, ["x"])))
        14x
        >>> print(abs(Monomial(-8, ["b"])))
        8b
        """
        return Monomial(abs(self.coefficient), self.variables)

    def __round__(self, n: int = 0) -> 'Monomial':
        """
        This method is used to round the
        coefficient of the monomial with a custom
        number of decimals (n, default 0)

        >>> print(round(Monomial(15.3918, ["c"])))
        15.0c
        >>> print(round(Monomial(15.3918, ["c"]), 2))
        15.39c
        """
        return Monomial(round(self.coefficient, n), self.variables)

    def __add__(self, other: 'Monomial') -> 'Monomial':
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
        >>> print(d + b) # They're not similar
        Traceback (most recent call last):
        ...
        ValueError: The monomials are not similar
        """
        if self.similar_to(other):
            return Monomial(self.coefficient + other.coefficient,
                            self.variables)
        else:
            raise ValueError("The monomials are not similar")

    def __sub__(self, other: 'Monomial') -> 'Monomial':
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
        >>> print(d + b) # They're not similar
        Traceback (most recent call last):
        ...
        ValueError: The monomials are not similar
        """
        return self + (-other)

    def __mul__(self, other: 'Monomial') -> 'Monomial':
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
        """

        # Make an exception for integer / float
        if not type(other) == type(self):
            return Monomial(self.coefficient * other, self.variables)

        return Monomial(self.coefficient * other.coefficient,
                        self.variables + other.variables)

    def __truediv__(self, other: 'Monomial') -> 'Monomial':
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
        ValueError: Not a monomial
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

    def __pow__(self, n: int) -> 'Monomial':
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
