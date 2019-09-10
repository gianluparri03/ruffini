from unittest import TestCase

from ruffini import Monomial as M
from ruffini import Polynomial as P
from ruffini import VariablesDict as VD


class Test (TestCase):
    def setUp (self):
        # Monomials
        m0 = M(2, {'x': 1, 'y': 1})
        m1 = M(-6, {'x': 1, 'y': 3})
        m2 = M(8, {'x': 1, 'y': 1})

        # Polynomials
        self.p0 = P(m0, m1, m2)

    def test_new_init (self):
        # terms must be monomials or number
        self.assertRaises(TypeError, P, "lol")

        # terms instance of int or float are
        # converted to monomial
        self.assertIsInstance(P(3)[0], M)

        # if more terms have the same variables
        # they are summed together
        self.assertEqual(self.p0.term_coefficient(VD(x=1, y=1)), 10)

        # if term_coefficient find nothing, the result is 0
        self.assertEqual(self.p0.term_coefficient(VD(k=2, b=1)), 0) 
