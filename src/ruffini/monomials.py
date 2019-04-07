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

        # Create a counter and count the variables
        counter = {}

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
            if letter in counter.keys():
                counter[letter] += exponent
            else:
                counter[letter] = exponent

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
        elif self.coefficient == 0:
            return "0"
        else:
            return str(self.coefficient) + self.variables_str()

    def __add__(self, other):
        """
        Add two monomials

        Ex.
        Monomial(2, ["x", "y"]) + Monomial(7, ["x", "y"])
        => Monomial(9, ["x", "y"])
        """
        if self.variables == other.variables:
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
        if self.variables == other.variables:
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
