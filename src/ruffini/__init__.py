from .variables import *
from .monomials import *
from .polynomials import *
from .fpolynomials import *


# Delete some (ugly) things
del variables
del monomials
del polynomials
del fpolynomials


# Define some shorthands

def gcd(*args):
    """
    A shorthand to calculate the gcd between two or more monomials.
    For more informations, see :func:`Monomial.gcd`
    """

    if not isinstance(args[0], Monomial):
        args = (Monomial(args[0]),) + args[1:]

    return reduce(lambda x, y: x.gcd(y), args)

def lcm(*args):
    """
    A shorthand to calculate the lcm between two or more monomials.
    For more informations, see :func:`Monomial.lcm`
    """

    if not isinstance(args[0], Monomial):
        args = (Monomial(args[0]),) + args[1:]

    return reduce(lambda x, y: x.lcm(y), args)
