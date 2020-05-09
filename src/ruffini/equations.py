from math import sqrt, gcd as math_gcd
from fractions import Fraction

from .monomials import Monomial
from .polynomials import Polynomial


class Equation:
    """
    You know what an equation is. Well,
    if you're reading this docs I hope you know. Anyway.

    The sides of the equations are polynomials.
    """

    def __init__(self, first, second):
        """
        Initialize the Equation by giving the two sides.

        >>> Equation(Monomial(2, x=1), 4)
        2x - 4 = 0

        As you may have noticed, it moves all the terms to the first side.
        It calculates the equation's variable and degree.

        >>> equation = Equation(Monomial(2, x=1), 4)
        >>> equation.first
        2x - 4
        >>> equation.second
        0
        >>> equation.degree
        1
        >>> equation.variable
        'x'

        NB: It raises a NotImplementedError if you try to create an
        equation with more than one variable

        >>> Equation(Monomial(3, x=1), Monomial(2, y=1))
        Traceback (most recent call last):
        ...
        NotImplementedError: Too many variables

        :type first: Polynomial
        :type second: Polynomial
        :raise: NotImplementedError
        """

        # Check if there is a denominator
        if isinstance(first, Fraction) and isinstance(second, Fraction):
            denominator = math_gcd(first.denominator, second.denominator)
        elif isinstance(first, Fraction):
            denominator = first.denominator
        elif isinstance(second, Fraction):
            denominator = second.denominator
        else:
            denominator = 1

        # If there is, multiply each term for it
        first *= denominator
        second *= denominator

        # Move all to the first side and calculate the degree
        self.first = Polynomial(first - second)
        self.second = Polynomial(0)
        self.degree = self.first.degree

        # Check if there is more than a variable
        if not len(self.first.variables) == 1:
            raise NotImplementedError("Too many variables")

        self.variable = self.first.variables[0]

    def __str__(self):
        """
        Return the equation formatted as a string

        >>> print(Equation(Monomial(2, x=1), 4))
        2x - 4 = 0

        :rtype: str
        """

        return f"{self.first} = {self.second}"

    def __repr__(self):
        """
        Return the equation formatted as a string

        >>> Equation(Monomial(2, x=1), 4)
        2x - 4 = 0

        For more informations, see :func:`Equation.__str__()`.

        :rtype: str
        """
        
        return str(self)

    def solve(self):
        """
        Solve the equation.

        >>> Equation(Monomial(x=2), 4).solve()
        (Fraction(2, 1), Fraction(-2, 1))

        It works only with equations of degree 1 or 2;
        if it's higher, it raises a NotImplementedError.

        >>> Equation(Monomial(x=3), 27).solve()
        Traceback (most recent call last):
        ...
        NotImplementedError: Can't solve equations with degree higher than 2

        If the result is impossible or indeterminate
        it raises a ValueError

        >>> Equation(Monomial(0, x=1), 0).solve()
        Traceback (most recent call last):
        ...
        ValueError: Equation impossible or indeterminate

        :raise: ValueError, NotImplementedError
        """

        if self.degree == 1:
            a = self.first.term_coefficient({self.variable: 1})
            if a == 0:
                raise ValueError("Equation impossible or indeterminate")

            return Fraction(self.second, a)

        elif self.degree == 2:
            # Fetch a, b, c
            a = self.first.term_coefficient({self.variable: 2})
            b = self.first.term_coefficient({self.variable: 1})
            c = self.first.term_coefficient()

            # Calculate delta
            delta = b**2 - 4*a*c
            if not delta >= 0:
                raise ValueError("Equation impossible or indeterminate")

            # Return the solutions
            delta = Fraction.from_float(sqrt(delta))
            return Fraction(-b + delta, 2*a), Fraction(-b - delta, 2*a)

        else:
            raise NotImplementedError("Can't solve equations with degree higher than 2")
