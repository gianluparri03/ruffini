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

def factorize(polynomial):
    """
    Factorize the given polynomial using some algorythms
    (sub functions), such as

    :func:`factorize.gcf`, group [todo], squares difference [todo],
    cubes sum [todo], cubes difference [todo],
    binomial square [todo], binomial cube [todo],
    trinomial square [todo].

    It works in recursive mode.

    >>> print(factorize(Polynomial(Monomial(10, x=1), 15)))
    5(2x + 3)

    If you polynomial is not a Polynomial instance, it raises
    a TypeError

    >>> print(factorize('John'))
    Traceback (most recent call last):
    ...
    TypeError: Can't factorize object of type 'str'

    :type polynomial: Polynomial
    :rtype: FPolynomial
    :raises: TypeError
    """

    def gcf(p, fp=()):
        """
        Factorize a polynomial with the gcf (greates common
        facor) method. In theory, it works like this:

        `AX + AY + ... = A(X + Y + ...)`

        for example:
        
        >>> gcf((), Polynomial(Monomial(10, x=1), 15))
        (5,), Polynomial(Monomial(2, x=1), 3)

        The first argument is the polynomial to factorize.
        The second one, is an optional list of factors; if you pass it
        at the function, it will just add factors to it.
        The results are, in order, the factors and the resulting
        polynomial, that could be factorized again.

        For example, if you pass some factors in the function call...

        >>> gcf((3), Polynomial(Monomial(10, x=1), 15))
        (3, 5), Polynomial(Monomial(2, x=1), 3)

        ... you'll se that the factor 5 is added to the list of
        factors passed in the function call

        :type p: Polynomial
        :type fp: tuple
        :rtype: tuple
        """

        # Calculate the greatest common factor
        gcd = reduce(lambda x, y: x.gcd(y), p)

        # If there is no gcf, return the given arguments
        if gcd == 1:
            return p, fp

        # Otherwise, return the new factors and the polynomial
        p = Polynomial(*[t/gcd for t in p])
        return p, fp + (gcd,)

    # Raise a TypeError if it's not a polynomial
    if not isinstance(polynomial, Polynomial):
        raise TypeError(f"Can't factorize object of type '{polynomial.__class__.__name__}'")

    # Initialize the factors list
    factors = []

    while True:
        polynomial, factors = gcf(polynomial)
        break

    # Return the result
    return FPolynomial(*factors, polynomial)
