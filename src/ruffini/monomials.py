from functools import reduce
from fractions import gcd
from collections import Counter, defaultdict


def lcm(x, y): return int((x*y) / gcd(x, y))


class Monomial:
    def __init__(self, coefficient=1, variables=[]):
        """
        Initialize the monomial
        """

        # Set the coefficient type
        if type(coefficient) == str:
            coefficient = eval(coefficient)

        # Initialize the monomial
        self.coefficient = coefficient
        self.variables = variables
        self.regroup_variables()
        self.degree = sum(self.degrees.values())

    """
    Utility Methods
    """

    def regroup_variables(self):
        """
        Regroup the variables of the monomial
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
                exponent = int(exponent)
            else:
                exponent = 1

            # Add them to the counter
            counter[letter] += exponent

        # Rewrite the variables
        self.variables.clear()
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

        # Sort them
        self.variables.sort()

    def similar_to(self, other):
        """
        Return True if the given Monomial is 
        similar to this Monomial, otherwise
        return False
        """

        # Raise an error if "other" is not a monomial
        if not type(self) == type(other):
            raise ValueError("Not a monomial")

        return self.variables == other.variables

    def gcd(self, *others):
        """
        Return the great common divisor for
        this monomial and others.
        """

        monomials = others + (self, )

        # Calculate the gcd of the coefficients
        coefficients = [m.coefficient for m in monomials]
        coefficient = reduce(gcd, coefficients)
        if 0 < coefficient < 1:
            coefficient = 1

        # Regroup the variables
        variables = []
        exponents = Counter()
        for monomial in monomials:
            variables += monomial.variables

        # Select the great exponent
        for var in variables:
            l = var.split("^")[0]
            if "^" in var:
                exp = int(var.split("^")[1])
            else:
                exp = 1
            exponents[l] = gcd(exponents[l], exp)

        # Rewrite the variables
        variables = [f"{l}^{exponents[l]}"
                     for l in exponents]

        return Monomial(coefficient, variables)

    def lcm(self, *others):
        """
        Return the great common divisor for
        this monomial and others.
        """

        monomials = others + (self, )

        # Calculate the lcm of the coefficients
        coefficients = [m.coefficient for m in monomials]
        coefficient = reduce(lcm, coefficients)

        # Regroup the variables
        variables = []
        for monomial in monomials:
            variables += monomial.variables
        variables.sort()

        # Calculate the lcm of the variables
        exponents = Counter()
        for variable in variables:
            l = variable.split("^")[0]
            if "^" in variable:
                exp = int(variable.split("^")[1])
            else:
                exp = 1
            if exponents[l] == 0:
                exponents[l] = exp
            exponents[l] = lcm(exponents[l], exp)

        # Rewrite the variables
        variables = [f"{l}^{exponents[l]}"
                     for l in exponents]

        return Monomial(coefficient, variables)

    """
    Magic Methods
    """

    def __str__(self):
        """
        Return the monomial as a string
        """

        variables = "".join(self.variables)
        coefficient = str(self.coefficient)

        # Make exceptions to write it better
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

    def __eq__(self, other):
        """
        Return True if the monomials are equivalent
        """
        return self.coefficient == other.coefficient \
            and self.variables == other.variables

    def __pos__(self):
        """
        Return the monomial itself
        """
        return Monomial(self.coefficient, self.variables)

    def __neg__(self):
        """
        Return the opposite of the monomial
        """
        return Monomial(-self.coefficient,
                        self.variables)

    def __abs__(self):
        """
        Return the absolute value of the monomial
        """
        return Monomial(abs(self.coefficient),
                        self.variables)

    def __round__(self, n=0):
        """
        Return the rounded value of the monomial
        """
        return Monomial(round(self.coefficient, n),
                        self.variables)

    """
    Mathematical operations
    """

    def __add__(self, other):
        """
        Add two monomials
        """
        if self.similar_to(other):
            return Monomial(self.coefficient + other.coefficient,
                            self.variables)
        else:
            raise ValueError("The variables are not equals")

    def __sub__(self, other):
        """
        Subtract two monomials
        """
        if self.similar_to(other):
            return Monomial(self.coefficient - other.coefficient,
                            self.variables)
        else:
            raise ValueError("The variables are not equals")

    def __mul__(self, other):
        """
        Multiply two monomials
        """

        # Make an exception for integer / float
        if not type(other) == type(self):
            return Monomial(self.coefficient * other,
                            self.variables)

        return Monomial(self.coefficient * other.coefficient,
                        self.variables + other.variables)

    def __truediv__(self, other):
        """
        Divide two monomials
        """

        # Make an exception for integer / float
        if not type(other) == type(self):
            return Monomial(self.coefficient / other,
                            self.variables)

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
