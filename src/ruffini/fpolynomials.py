from .monomials import Monomial, Variable
from .polynomials import Polynomial
from .equations import Equation

from functools import reduce
from fractions import Fraction


class FPolynomial(tuple):
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

    def __new__(cls, *factors):
        """
        Create the factorized polynomial giving it a list
        of factors (int, float, Fraction, Monomial or Polynomial).

        >>> p = Polynomial(Monomial(2, x=2, y=2))
        >>> FPolynomial(5, p)
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

        It converts all the factors to Polynomial
        and sort them by frequency.

        :type *factors: int, float, Fraction, Monomial, Polynomial
        :raise: TypeError
        """

        # adjust argument's order
        if len(factors) == 1 and type(factors[0]) in (tuple, list, set):
            factors = factors[0]

        mapped_factors = []

        # Check if there's at least a polynomial
        if not any([isinstance(f, Polynomial) for f in factors]):
            raise TypeError("There must be at least a polynomial")

        for factor in factors:
            # Check if its type is valid
            if not isinstance(factor, (int, float, Fraction, Polynomial, Monomial)):
                raise TypeError("FPolynomial elements must be int, float, Polynomial or Monomial instance")

            # Ensure that all the factors are polynomials
            elif factor == 1:
                continue
            elif isinstance(factor, Polynomial):
                mapped_factors.append(factor)
            else:
                mapped_factors.append(Polynomial(factor))

        return super().__new__(cls, mapped_factors)

    ### Utilty Methods ###

    def eval(self):
        """
        Return the starting polynomial multiplying
        all the factors

        >>> f = FPolynomial(5, Polynomial(Monomial(2, x=1), 3))
        >>> f
        5(2x + 3)
        >>> f.eval()
        10x + 15

        The result will always be a Polynomial

        >>> type(f.eval())
        <class 'ruffini.polynomials.Polynomial'>

        :rtype: Polynomial
        """

        return reduce(lambda x, y: x*y, self)

    ### Magic Methods ###

    def __str__(self):
        """
        Return the factorized polynomial as a string.

        >>> p1 = Polynomial(2, Monomial(3, x=1))
        >>> p2 = Polynomial(Monomial(2, y=1), 17)
        >>> print(FPolynomial(p1, p2))
        (2 + 3x)(2y + 17)

        If the first element is a monomial, an integer
        or a float, its brackets will be omitted

        >>> print(FPolynomial(5, p1))
        5(2 + 3x)

        Otherwise, if a factor appears two times, the result
        will be like this

        >>> print(FPolynomial(p2, p2))
        (2y + 17)**2

        >>> print(FPolynomial(p2, p2, 5))
        5(2y + 17)**2

        :rtype: str
        """

        # if there is only a factor, print it without parenthesis
        if len(self) == 1:
            return str(self[0])

        # initialize variables
        monomials = []
        polynomials = []
        result = ""

        # divide factors in monomials and polynomials
        for f in self:
            if len(f) == 1:
                monomials.append(f)
            else:
                polynomials.append(f)

        # sort them
        sorting_factor = lambda f: (self.count(f), len(str(f)))
        monomials = sorted(list(set(monomials)), key=sorting_factor)
        polynomials = sorted(list(set(polynomials)), key=sorting_factor)

        # iterate the factors
        for sublist in (monomials, polynomials):
            for factor in sublist:
                # if its exponent is 1...
                if self.count(factor) == 1:
                    # ...if it's a monomial and result is
                    # empty, add the monomial without parenthesis
                    if sublist == monomials and result == "":
                        result += str(factor)
                    # ... otherwise add it, but without exponent
                    else:
                        result += f"({factor})"
                # in all the other cases, add it with exponent notation
                else:
                    result += f"({factor})**{self.count(factor)}"

        return result

    def __repr__(self):
        """
        Return the factorized polynomial as a string.

        >>> p1 = Polynomial(2, Monomial(3, x=1))
        >>> p2 = Polynomial(Monomial(2, y=1), 17)
        >>> repr(FPolynomial(p1, p2))
        '(2 + 3x)(2y + 17)'

        For more informations, see :func:FPolynomial.__str__()`.

        :rtype: str
        """

        return self.__str__()

    def __eq__(self, other):
        """
        Compare two factorized polynomials to see if they're
        equivalent.

        >>> p = Polynomial(Monomial(5, x=2), 3)
        >>> m = Monomial(2, y=1)
        >>> FPolynomial(p, m) == FPolynomial(p, m)
        True

        If we swap factors, the result doesn't change

        >>> FPolynomial(p, m) == FPolynomial(m, p)
        True

        If we compare two factorized polynomials
        with different factors, but which - once evaluated - they
        are equivalent, the result is true. For example:

        >>> x = Variable("x")
        >>> y = Variable("y")
        >>>
        >>> fp1 = FPolynomial(2*x - 3*y**2, 2*x - 3*y**2)
        >>> fp2 = FPolynomial(3*y**2 - 2*x, 3*y**2 - 2*x)
        >>>
        >>> fp1.eval() == fp2.eval()
        True
        >>> fp1 == fp2
        True

        :type other: FPolynomial
        :rtype: bool
        """

        if not isinstance(other, FPolynomial):
            return False

        return self.eval() == other.eval()


def gcf(polynomial):
    """
    Factorize a polynomial with the gcf (greates common
    facor) method. It works like this:

    `AX + AY + ... = A(X + Y + ...)`

    for example:

    >>> gcf(Polynomial(Monomial(10, x=1), 15))
    (5, 2x + 3)

    If there isn't a gcf, it will return the starting polynomial

    >>> gcf(Polynomial(Monomial(11, x=1), 15))
    (11x + 15,)

    The function returns a tuple.

    :type p: Polynomial
    :rtype: tuple
    :raise: TypeError
    """

    # raise a TypeError if polynomial isn't a polynomial
    if not isinstance(polynomial, Polynomial):
        raise TypeError(f"Can't use gcf with an object of type '{polynomial.__class__.__name__}'")

    # Calculate the greatest common factor
    gcd = reduce(lambda x, y: x.gcd(y), polynomial)

    # If there is no gcf, return the given polynomial
    if gcd == 1:
        return (polynomial, )

    # Otherwise, return the gcf and the reduced polynomial
    polynomial = Polynomial([t/gcd for t in polynomial])
    return gcd, polynomial

def binomial_square(polynomial):
    """
    Check if the polynomial is a binomial
    square. It works like this:

    `A*2 + B**2 + 2AB = (A + B)**2`

    for example:

    >>> p = Polynomial(Monomial(4, x=2), Monomial(9, y=4), Monomial(-12, x=1, y=2))
    >>> p
    4x**2 + 9y**4 - 12xy**2
    >>> binomial_square(p)
    (2x - 3y**2, 2x - 3y**2)

    It can raise ValueError in three cases:

    1. When polynomial's length isn't 3:

    >>> binomial_square(Polynomial(1))
    Traceback (most recent call last):
    ...
    ValueError: Not a binomial square

    2. When there aren't at least two squares:

    >>> p = Polynomial(Monomial(4, x=2), Monomial(9, y=5), Monomial(3))
    >>> binomial_square(p)
    Traceback (most recent call last):
    ...
    ValueError: Not a binomial square

    3. When the third term isn't the product of the firsts:

    >>> p = Polynomial(Monomial(4, x=2), Monomial(9, y=4), Monomial(3))
    >>> binomial_square(p)
    Traceback (most recent call last):
    ...
    ValueError: Not a binomial square

    :type p: Polynomial
    :rtype: tuple
    :raise: TypeError, ValueError
    """

    # raise a TypeError if polynomial isn't a polynomial instance
    if not isinstance(polynomial, Polynomial):
        raise TypeError(f"Can't use binomial_square with an object of type '{polynomial.__class__.__name__}'")

    # Raise a ValueError if polynomial's length isn't 3 (not a binomial square)
    if len(polynomial) != 3:
        raise ValueError("Not a binomial square")

    # Sort the polynomial
    polynomial = sorted(polynomial, key=lambda t: t.has_root(2), reverse=True)

    # Check if there are two squares (otherwise raise a ValueError)
    if not polynomial[1].has_root(2):
        raise ValueError("Not a binomial square")

    # Calculate squares
    a = polynomial[0].root(2)
    b = polynomial[1].root(2)

    # Check if the third term is the product of the first two
    if 2*a*b != abs(polynomial[2]):
        raise ValueError("Not a binomial square")

    # If the third term is negative, make negative one of the firsts
    if polynomial[2].coefficient < 0:
        b = -b

    return Polynomial(a, b), Polynomial(a, b)

def ruffinis_rule(polynomial):
    """
    Try to factorize the polynomial with the Ruffini's rule.

    >>> ruffinis_rule(Polynomial(Monomial(3, x=3), Monomial(2, x=2), Monomial(-3, x=1), Monomial(-2)))
    (x - 1, 3x**2 + 2 + 5x)

    If it didn't work, it raises a ValueError.

    If polynomial isn't a :class:`Polynomial` instance it raises a TypeError

    >>> ruffinis_rule('Pepe the frog')
    Traceback (most recent call last):
    ...
    TypeError: Can't use ruffini's rule with an object of type 'str'

    :type polynomial: Polynomial
    :rtype: tuple
    :raise: TypeError, ValueError
    """

    # raise a TypeError if polynomial isn't a polynomial instance
    if not isinstance(polynomial, Polynomial):
        raise TypeError(f"Can't use ruffini's rule with an object of type '{polynomial.__class__.__name__}'")

    # Get the variable
    variable = polynomial.variables[0]

    for zero in polynomial.zeros:
        # Calculate the coefficients
        coefficients = [polynomial.term_coefficient({variable: polynomial.degree})]
        try:
            for exponent in range(polynomial.degree)[::-1]:
                coefficients.append(coefficients[-1] * zero + polynomial.term_coefficient({variable: exponent}))

            # Check that the remider is 0 (otherwise try with another zero)
            if coefficients[-1]:
                raise RuntimeError

            result = 0

            # Build the monomials
            for d in range(len(coefficients) - 1):
                result += Monomial(coefficients[d], {variable: polynomial.degree - d - 1})

            return Monomial(1, {variable: 1}) - zero, Polynomial(result)
        except RuntimeError:
            continue

    raise ValueError("Can't factor the polynomial with Ruffini's rule")

def factorize(polynomial):
    """
    Factorize the given polynomial using some algorythms
    (sub functions), such as

    :func:`gcf`, group [todo], squares difference [todo],
    cubes sum [todo], cubes difference [todo],
    binomial square [todo], :func:`factorize_binomia_square`,
    trinomial square [todo].

    It works in recursive mode.

    >>> factorize(Polynomial(Monomial(10, x=1), 15))
    5(2x + 3)

    If polynomial isn't a polynomial, it will raise a TypeError

    >>> factorize('John')
    Traceback (most recent call last):
    ...
    TypeError: Can't factorize object of type 'str'

    :type polynomial: Polynomial
    :rtype: FPolynomial
    :raises: TypeError
    """

    # Raise a TypeError if polynomial is not a polynomial
    if not isinstance(polynomial, Polynomial):
        raise TypeError(f"Can't factorize object of type '{polynomial.__class__.__name__}'")

    # initialize factors
    factors = []
    new_factors = list(gcf(polynomial))

    # while there are things to factorize, factorize them!
    while not factors == new_factors:
        factors = new_factors
        new_factors = []

        # for each factor
        for factor in factors:
            # leave it like it was if it isn't a polynomial, if it's a polynomial
            # of first degree or if it has more than a variable
            if not isinstance(factor, Polynomial) or not len(factor.variables) == 1 or factor.degree < 2:
                new_factors.append(factor)
                continue

            # try with a binomial square
            if len(factor) == 3 and factor.degree == 2:
                try:
                    new_factors.extend(binomial_square(factor))
                    continue
                except ValueError:
                    pass

            # if it is a trinomial try with an equation
            if len(factor) == 3 and factor.degree == 2:
                try:
                    x1, x2 = Equation(factor, 0).solve()
                    variable = Monomial(1, {factor.variables[0]: 1})
                    new_factors.extend([factor.term_coefficient(variable**2), variable - x1, variable - x2])
                    continue
                except AssertionError:
                    pass

            # try with ruffini's rule
            if factor.degree >= 2:
                try:
                    new_factors.extend(ruffinis_rule(factor))
                    continue
                except ValueError:
                    pass

            new_factors.append(factor)

    # Return the result
    return FPolynomial(*factors)
