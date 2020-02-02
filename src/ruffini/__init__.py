from .variables import *
from .monomials import *
from .polynomials import *
from .fpolynomials import *


# Delete some (ugly) things
del variables
del monomials
del polynomials
del fpolynomials


# Variables shorthands
def variable(letter):
    return Monomial(1, {str(letter): 1})

# GCD shorthand
def gcd(*args):
    """
    A shorthand to calculate the gcd between two or more monomials.
    For more informations, see :func:`Monomial.gcd`
    """

    if not isinstance(args[0], Monomial):
        args = (Monomial(args[0]),) + args[1:]

    return reduce(lambda x, y: x.gcd(y), args)

# LCM shorthand
def lcm(*args):
    """
    A shorthand to calculate the lcm between two or more monomials.
    For more informations, see :func:`Monomial.lcm`
    """

    if not isinstance(args[0], Monomial):
        args = (Monomial(args[0]),) + args[1:]

    return reduce(lambda x, y: x.lcm(y), args)
