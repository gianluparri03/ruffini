from .monomials import Monomial
from .polynomials import Polynomial

from functools import reduce


class FPolynomial (tuple):
    """
    A FPolynomial (factorized polynomial) object
    is a multiplication of two or more polynomials.

    When you factor a polynomial, an FPolynomial istance
    is returned. On the other hand, you can multiply the
    polynomials of the fpolynomial and obtain the starting
    polynomial.

    You can't perform any math operation with a factorized
    polynomial

    **NB** The FPolynomial class is a subclass of tuple,
    so all the methods of tuple are automatically
    inherited from FPolynomial; many of these methods
    are not in this docs.
    """

    def __new__ (cls, *factors):
        """
        Create the factorized polynomial giving it a list
        of factors (int, float, Monomial or Polynomial).

        >>> p = Polynomial(Monomial(2, x=2, y=2))
        >>> fp = FPolynomial(5, p)
        >>> print(fp)
        5(2x**2y**2)

        In the factors must be present at least a polynomial

        >>> FPolynomial(5)
        Traceback (most recent call last):
        ...
        TypeError: there must be at least a polynomial

        **NB:** It converts all the factors to Polynomial
        and sort them by frequency.

        :type *factors: int, float, Monomial, Polynomial
        :raise: TypeError
        """

        mapped_factors = []

        # Check if there's at least a polynomial
        if not any((isinstance(f, Polynomial) for f in factors)):
            raise TypeError("There must be at least a polynomial")

        for factor in factors:
            # Check if its type is valid
            if not isinstance(factor, (int, float, Polynomial, Monomial)):
                raise TypeError("FPolynomial elements must be int, float, Polynomial or Monomial instance")

            # Ensure that all the factors are polynomials
            elif isinstance(factor, Polynomial):
                mapped_factors.append(factor)
            else:
                mapped_factors.append(Polynomial(factor))

        # Sort the factors by frequency
        mapped_factors = sorted(mapped_factors, key=mapped_factors.count, reverse=True)

        return super().__new__(cls, mapped_factors)

    def __str__ (self):
        """
        Return the factorized polynomial as a string.

        >>> p1 = Polynomial(2, Monomial(3, x=1))
        >>> p2 = Polynomial(Monomial(2, y=1), 7)
        >>> print(FPolynomial(p1, p2))
        (2 + 3x)(2y + 7)

        If the first element is a monomial, an integer
        or a float, its brackets will be omitted

        >>> print(FPolynomial(5, p1))
        5(2 + 3x)

        Otherwise, if a factor appears two times, the result
        will be like this

        >>> print(FPolynomial(p2, p2))
        (2y + 7)**2

        :rtype: str
        """

        factors = ""
        done = []

        for factor in self:
            # Check if it is already written
            if factor in done:
                continue

            exponent = self.count(factor)

            # if exponent is greater than one
            if exponent > 1:
                factors += f'({factor})**{exponent}'
            # if it's a monomial
            elif len(factor) == 1:
                factors += f'{factor}'
            # default
            else:
                factors += f'({factor})'

            done.append(factor)

        return factors


    def eval(self):
        """
        Return the starting polynomial multiplying
        all the factors

        >>> f = FPolynomial(5, Polynomial(Monomial(2, x=1), 3))
        >>> print(f)
        5(2x + 3)
        >>> print(f.eval())
        10x + 15

        The result will always be a Polynomial

        >>> type(f.eval())
        <class ruffini.polynomials.Polynomial>

        :rtype: Polynomial
        """

        return reduce(lambda x, y: x*y, self)
