from unittest import TestCase

from ruffini import VariablesDict as VD
from ruffini import Monomial as M
from ruffini import Polynomial as P
from ruffini import FPolynomial as FP


class Test (TestCase):
    def setUp (self):
        # Monomials
        self.m = [
                  M(2, VD(x=1)),
                  M(5, VD(y=2)),
                  M(17, VD(z=1))
                 ]

        # Polynomials
        self.p = [
                  P(self.m[0], 3),           # 2x + 3
                  P(self.m[1], self.m[2])    # 5y**2 + 17z
                 ]

        # FPolynomials
        self.fp = [
                   FP(self.p[1], self.p[0]), # (5y**2 + 17z)(2x + 3)
                   FP(5, self.p[0]),         # 5(2x + 3)
                   FP(self.m[0], self.p[1]), # 2x(5y**2 + 17z)
                   FP(self.p[0], self.p[0]), # (2x + 3)**2
                  ]

    def test (self):
        # FPolynomial is an instance of tuple
        self.assertIsInstance(self.fp[2], tuple)

        # There must be at least a polynomial
        self.assertRaises(TypeError, FP, self.m[2], 5)

        # Factors must be polynomials, monomials or numbers
        self.assertRaises(TypeError, FP, "", self.p[1])

        # default string representation
        self.assertEqual(str(self.fp[0]), '(5y**2 + 17z)(2x + 3)')

        # if the first factor is a monomial there are no brackets
        self.assertEqual(str(self.fp[1]), '5(2x + 3)')
        self.assertEqual(str(self.fp[2]), '2x(5y**2 + 17z)')

        # with factors that appears two times
        self.assertEqual(str(self.fp[3]), '(2x + 3)**2')
        self.assertEqual(str(FP(self.p[0], self.m[0], self.m[0])), '(2x)**2(2x + 3)')

        # eval
        self.assertEqual(self.fp[1].eval(), P(M(10, VD(x=1)), 15))
