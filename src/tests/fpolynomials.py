from unittest import TestCase

from ruffini import Monomial as M
from ruffini import Polynomial as P
from ruffini import FPolynomial as FP
from ruffini import gcf, binomial_square, factorize


class Test(TestCase):
    def setUp(self):
        # Polynomials
        self.p = [
                  P(M(2, x=1), 3),          # 2x + 3
                  P(M(10, x=1), 15),        # 10x + 15
                  P(M(2, x=2), M(3, y=1))   # 2x**2 + 3y
                 ]

        # FPolynomials
        self.fp = [
                   FP(self.p[1], self.p[0]), # (10x + 15)(2x + 3)
                   FP(5, self.p[0])          # 5(2x + 3)
                  ]

    def test_fpolynomial(self):
        # FPolynomial is an instance of tuple
        self.assertIsInstance(self.fp[1], tuple)

        # factors that are equal to 1 aren't inserted
        self.assertEqual(len(FP(self.p[1], 1)), 1)

        # There must be at least a polynomial
        self.assertRaises(TypeError, FP, M(17, z=1), 5)

        # Factors must be polynomials, monomials or numbers
        self.assertRaises(TypeError, FP, "", self.p[1])

        # default string representation
        self.assertEqual(str(self.fp[0]), '(2x + 3)(10x + 15)')

        # repr is the same of str
        self.assertEqual(str(self.fp[0]), repr(self.fp[0]))

        # if the first factor is a monomial there are no brackets
        self.assertEqual(str(self.fp[1]), '5(2x + 3)')
        self.assertEqual(str(FP(M(2, x=1), self.p[0])), '2x(2x + 3)')

        # with factors that appears two times
        self.assertEqual(str(FP(self.p[1], self.p[1])), '(10x + 15)**2')
        self.assertEqual(str(FP(self.p[0], M(2, x=1), M(2, x=1))), '(2x)**2(2x + 3)')

        # with factors that appears more times and a monomial
        self.assertEqual(str(FP(self.p[0], self.p[0], 5)), '5(2x + 3)**2')

        # if there is only a factor with exponent 1, str() returns that factor
        self.assertEqual(str(FP(self.p[0])), str(self.p[0]))

        # eval
        self.assertEqual(self.fp[1].eval(), P(M(10, x=1), 15))

        # eq
        self.assertEqual(FP(self.p[1], 5), FP(5, self.p[1]))
        self.assertFalse(self.fp[0] == {'a', 'b', 'x'})

    def test_factorization(self):
        # test shorthand
        self.assertEqual(self.p[0].factorize(), factorize(self.p[0]))

        # can factorize only polynomials
        self.assertRaises(TypeError, factorize, 159)

        # test gcf + binomial_square
        polynomial = self.p[2] * self.p[2] * 5
        factorization = FP(5, P(M(2, x=2), M(3, y=1)), P(M(2, x=2), M(3, y=1)))
        self.assertEqual(polynomial.factorize(), factorization)

    def test_gcf(self):
        # works only with polynomials
        self.assertRaises(TypeError, gcf, 'a number')

        # always return a FPolynomial
        self.assertIsInstance(gcf(self.p[1]), FP)

        # return the same polynomial if it's not factorizable with gcf
        self.assertEqual(gcf(self.p[0]), FP(self.p[0]))

        # otherwise return the gcf and the polynomial reduced
        self.assertEqual(gcf(self.p[1]), self.fp[1])

        # commutative property
        self.assertEqual(gcf(self.p[1]), gcf(P(*self.p[1][::-1])))

    def test_binomial_square(self):
        # works only with polynomials
        self.assertRaises(TypeError, binomial_square, 'a number')

        # raise ValueError if polynomial's length isn't 3
        self.assertRaises(ValueError, binomial_square, self.p[0])

        # raise ValueError if there aren't two squares in polynomial
        self.assertRaises(ValueError, binomial_square, P(*self.p[2], 5))

        # raise ValueError if the third term isn't the product of the first two
        self.assertRaises(ValueError, binomial_square, P(M(4, x=2), M(9, y=4), 3))

        # test with a binomial square
        polynomial = self.p[2]*self.p[2]
        factorized = FP(self.p[2], self.p[2])
        self.assertEqual(binomial_square(polynomial), factorized)

        # test with a negative binomial square
        polynomial -= M(24, x=2, y=1)
        factorized = FP(*[P(self.p[2][0], -self.p[2][1])] * 2)
        self.assertEqual(binomial_square(polynomial), factorized)

        # commutative property
        polynomial = P(*polynomial[::-1])
        self.assertEqual(binomial_square(polynomial), factorized)
