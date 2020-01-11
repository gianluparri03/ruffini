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

        Every factor that is equal to 1 is not inserted
        in the fpolynomial

        >>> len(FPolynomial(5, p, 1))
        2

        In the factors must be present at least a polynomial

        >>> FPolynomial(5)
        Traceback (most recent call last):
        ...
        TypeError: There must be at least a polynomial

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
            elif factor == 1:
                continue
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

        # Return the result without parenthesis if there
        # is only a factor and its exponent is 1
        if len(self) == 1:
            return str(self[0])

        for factor in self:
            # Check if it is already written
            if factor in done:
                continue

            exponent = self.count(factor)

            # if exponent is greater than one
            if exponent > 1:
                factors += f'({factor})**{exponent}'
            # if it's a monomial
            elif len(factor) == 1 and len(done) == 0:
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
        <class 'ruffini.polynomials.Polynomial'>

        :rtype: Polynomial
        """

        return reduce(lambda x, y: x*y, self)


def gcf(polynomial):
    """
    Factorize a polynomial with the gcf (greates common
    facor) method. In theory, it works like this:

    `AX + AY + ... = A(X + Y + ...)`

    for example:

    >>> print(gcf(Polynomial(Monomial(10, x=1), 15)))
    5(2x + 3)

    If there isn't a gcf, it will return the starting polynomial

    >>> print(gcf(Polynomial(Monomial(11, x=1), 15)))
    11x + 15

    The function will always return a FPolynomial.

    :type p: Polynomial
    :rtype: FPolynomial
    :raise: TypeError
    """

    # raise a TypeError if polynomial isn't a polynomial
    if not isinstance(polynomial, Polynomial):
        raise TypeError(f"Can't use gcf with an object of type '{polynomial.__class__.__name__}'")

    # Calculate the greatest common factor
    gcd = reduce(lambda x, y: x.gcd(y), polynomial)

    # If there is no gcf, return the given polynomial
    if gcd == 1:
        return FPolynomial(polynomial)

    # Otherwise, return the gcf and the reduced polynomial
    polynomial = Polynomial(*[t/gcd for t in polynomial])
    return FPolynomial(gcd, polynomial)


def binomial_square(polynomial):
    """
    Factorize a polynomial with the gcf (greates common
    facor) method. In theory, it works like this:

    `A**2 + B**2 + 2AB = (A + B)**2`

    for example:

    >>> p = Polynomial(Monomial(4, x=2), Monomial(9, y=4), Monomial(-12, x=1, y=2))
    >>> print(binomial_square(p))
    (2x - 3y**2)**2

    *NB:* order of terms doesn't matter.

    If the given argument isn't an instance of Polynomial,
    it will raise a TypeError

    >>> binomial_square('a doggo')
    Traceback (most recent call last):
    ...
    TypeError: Can't use binomial_square with an object of type 'str'

    It can raise also ValueError, in three cases:

    1. When polynomial's length isn't 3:

    >>> binomial_square(Polynomial())
    Traceback (most recent call last):
    ...
    ValueError: Not a binomial square

    2. When there aren't at least two squares:

    >>> p = Polynomial(Monomial(4, x=2), Monomial(9, y=5), Monomial(3))
    >>> binomial_square(Polynomial())
    Traceback (most recent call last):
    ...
    ValueError: Not a binomial square

    3. When the third term isn't the product of the firsts:

    >>> p = Polynomial(Monomial(4, x=2), Monomial(9, y=4), Monomial(3))
    >>> binomial_square(Polynomial())
    Traceback (most recent call last):
    ...
    ValueError: Not a binomial square

    :type p: Polynomial
    :rtype: FPolynomial
    :raise: TypeError, ValueError
    """

    # raise a TypeError if polynomial isn't a polynomial instance
    if not isinstance(polynomial, Polynomial):
        raise TypeError(f"Can't use binomial_square with an object of type '{polynomial.__class__.__name__}'")

    # Raise a ValueError if polynomial's length isn't 3 (not a binomial square)
    if len(polynomial) != 3:
        raise ValueError("Not a binomial square")

    # Sort the polynomial
    polynomial = sorted(polynomial, key=lambda t: t.is_square, reverse=True)

    # Check if there are two squares (otherwise raise a ValueError)
    if not polynomial[1].is_square:
        raise ValueError("Not a binomial square")

    # Calculate squares
    a = polynomial[0] ** (1/2)
    b = polynomial[1] ** (1/2)

    # Check if the third term is the product of the first two
    if 2*a*b != abs(polynomial[2]):
        raise ValueError("Not a binomial square")

    # If the third term is negative, make negative one of the firsts
    if polynomial[2].coefficient < 0:
        b = -b

    return FPolynomial(Polynomial(a, b), Polynomial(a, b))


def factorize(polynomial):
    """
    Factorize the given polynomial using some algorythms
    (sub functions), such as

    :func:`gcf`, group [todo], squares difference [todo],
    cubes sum [todo], cubes difference [todo],
    binomial square [todo], :func:`factorize_binomia_square`,
    trinomial square [todo].

    It works in recursive mode.

    #>>> print(factorize(Polynomial(Monomial(10, x=1), 15)))
    #5(2x + 3)

    If you pass a monomial or a number at the function
    instead of a polynomial, it will return exactly the same
    monomial/number

    #>>> print(factorize(Monomial(5, x=1)))
    #5x

    Otherwise, it will raise a TypeError

    #>>> print(factorize('John'))
    #Traceback (most recent call last):
    #...
    #TypeError: Can't factorize object of type 'str'

    :type polynomial: Polynomial, Monomial, int, float
    :rtype: FPolynomial, Monomial, int, float
    :raises: TypeError
    """

    # Raise a TypeError if polynomial is not a polynomial
    if not isinstance(polynomial, Polynomial):
        raise TypeError(f"Can't factorize object of type '{polynomial.__class__.__name__}'")

    # initialize factors
    factors = tuple()

    # apply gcf() to polynomial, then iterate the result
    for factor in gcf(polynomial):

        # if the factor is not a polynomial, add it to the factors list
        if not isinstance(factor, Polynomial):
            factors += (factor, )

        # if it's a polynomial of length one, add it to the list
        elif len(factor) == 1:
            factors += (factor[0], )

        # if it's a polynomial of length one, try binomial square
        elif len(factor) == 3:
            try:
                factors += binomial_square(factor)
            except ValueError:
                pass

        # otherwise, add it to the list
        else:
            factors += (factor, )

    # Return the result
    return FPolynomial(*factors)
