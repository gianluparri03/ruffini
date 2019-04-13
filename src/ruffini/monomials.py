from functools import reduce
from fractions import gcd
from collections import Counter


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
        self.variables_str = lambda: "".join(self.variables)
        self.regroup_variables()

    def regroup_variables(self):
        """
        Regroup the variables of the monomial

        Ex:
        Monomial(2, [y^2", "y", "x^5"])
        => Monomial(2, ["x^5", "y^3"])
        """

        counter = self.count_variables()

        # Rewrite the variables
        self.variables.clear()
        for var in counter.keys():
            if counter[var] == 0:
                continue
            elif counter[var] < 0:
                raise ValueError("Not a monomial")
            elif counter[var] > 1:
                var += "^" + str(counter[var])
            self.variables.append(var)

        # Sort them
        self.variables.sort()

        # Add the monomial degree
        self.degree = sum(counter.values())

    def __str__(self):
        """
        Return the monomial as a string

        Ex:
        Monomial(2, ["x^5", "y^3"]) => 2x^5y^3
        """
        if self.coefficient == 1 and self.variables == []:
            return "1"
        elif self.coefficient == 1:
            return self.variables_str()
        elif self.coefficient == -1:
            return "-" + self.variables_str()
        elif self.coefficient == 0:
            return "0"
        else:
            return str(self.coefficient) + self.variables_str()

    def __eq__(self, other):
        """
        Return True if the monomials are equivalent
        """
        return all([self.coefficient == other.coefficient,
                   self.variables == other.variables])

    def __add__(self, other):
        """
        Add two monomials

        Ex.
        Monomial(2, ["x", "y"]) + Monomial(7, ["x", "y"])
        => Monomial(9, ["x", "y"])
        """
        if self.similar_to(other):
            return Monomial(self.coefficient + other.coefficient,
                            self.variables)
        else:
            raise ValueError("The variables are not equals")

    def __sub__(self, other):
        """
        Subtract two monomials

        Ex.
        Monomial(2, ["x", "y"]) - Monomial(7, ["x", "y"])
        => Monomial(-5, ["x", "y"])
        """
        if self.similar_to(other):
            return Monomial(self.coefficient - other.coefficient,
                            self.variables)
        else:
            raise ValueError("The variables are not equals")

    def __mul__(self, other):
        """
        Multiply two monomials

        Ex.
        Monomial(2, ["x", "y"]) * Monomial(7, ["x", "y"])
        => Monomial(14, ["x^2", "y^2"])
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

        Ex.
        Monomial(18, ["x^2", "y"]) * Monomial(9, ["x", "y"])
        => Monomial(2, ["x"])
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
        Rise a monomial to power

        Ex.
        Monomial(2, ["x^2", "y"]) ** 2
        => Monomial(4, ["x^4", "y^2"])
        """

        # Raise the variables to power
        variables = []
        for var in self.variables:
            letter = var.split("^")[0]
            if "^" in var:
                exponent = int(var.split("^")[1]) * n
            else:
                exponent = 1 * n
            variables.append(letter + "^" + str(exponent))

        return Monomial(self.coefficient ** n, variables)

    def __pos__(self):
        """
        Return the monomial itself
        """
        return Monomial(self.coefficient, self.variables)

    def __neg__(self):
        """
        Return the opposite of the monomial
        """
        return Monomial(- self.coefficient, self.variables)

    def __abs__(self):
        """
        Return the absolute value of the monomial
        """
        return Monomial(abs(self.coefficient), self.variables)

    def __round__(self, n=0):
        """
        Return the rounded value of the monomial
        """
        return Monomial(round(self.coefficient, n), self.variables)

    def degree_variable(self, var):
        """
        Return the degree of a specified variable
        """

        # Raise an error if var is not a variable
        if not var.isalpha() or len(var) > 1:
            raise ValueError("Not a variable")

        if any(v.startswith(var) for v in self.variables):
            for v in self.variables:
                if v.startswith(var):
                    if "^" in v:
                        return v["^"][1]
                    else:
                        return 1
        else:
            return 0

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

    def count_variables(self):
        """
        Return the variable counter
        """

        counter = Counter()

        # Extract letters and exponents
        for var in self.variables:
            letter = var.split("^")[0]
            if "^" in var:
                exponent = var.split("^")[1]
                if "(" in exponent:
                    exponent = exponent.replace("(", "")
                    exponent = exponent.replace(")", "")
                exponent = int(exponent)
            else:
                exponent = 1

            # Add them to the counter
            counter[letter] += exponent

        return counter

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
            letter = var.split("^")[0]
            if "^" in var:
                exponent = int(var.split("^")[1])
            else:
                exponent = 1
            exponents[letter] = gcd(exponents[letter], exponent)

        # Rewrite the variables
        variables = [f"{l}^{exponents[l]}" for l in exponents]

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
            letter = variable.split("^")[0]
            if "^" in variable:
                exponent = int(variable.split("^")[1])
            else:
                exponent = 1
            if exponents[letter] == 0:
                exponents[letter] = exponent
            exponents[letter] = lcm(exponents[letter], exponent)

        # Rewrite the variables
        variables = [f"{l}^{exponents[l]}" for l in exponents]

        return Monomial(coefficient, variables)
