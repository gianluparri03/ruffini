from unittest import TestCase

from ruffini import Monomial as M
from ruffini import Polynomial as P
from ruffini import FPolynomial as FP
from ruffini import factorize


class Test(TestCase):
    def setUp(self):
        # Monomials
        self.m = [
                  M(2, x=1),
                  M(5, y=2),
                  M(17, z=1)
                 ]

        # Polynomials
        self.p = [
                  P(self.m[0], 3),           # 2x + 3
                  P(self.m[1], self.m[2]),   # 5y**2 + 17z
                  P(M(10, x=1), 15)          # 10x + 15
                 ]

        # FPolynomials
        self.fp = [
                   FP(self.p[1], self.p[0]), # (5y**2 + 17z)(2x + 3)
                   FP(5, self.p[0]),         # 5(2x + 3)
                   FP(self.m[0], self.p[1]), # 2x(5y**2 + 17z)
                   FP(self.p[0], self.p[0]), # (2x + 3)**2
                  ]

    def test_class(self):
        # FPolynomial is an instance of tuple
        self.assertIsInstance(self.fp[2], tuple)

        # factors that are equal to 1 aren't inserted
        self.assertEqual(len(FP(self.p[2], 1)), 1)

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
        self.assertEqual(self.fp[1].eval(), P(M(10, x=1), 15))

    def test_factorization(self):
        # test shorthand
        self.assertEqual(self.p[0].factorize(), factorize(self.p[0]))

        # can factorize only polynomials
        self.assertRaises(TypeError, factorize, 159)

        # test gcf
        self.assertEqual(str(factorize(self.p[2])), str(self.fp[1]))
