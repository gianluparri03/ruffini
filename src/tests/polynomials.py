from unittest import TestCase

from ruffini import Monomial as M
from ruffini import Polynomial as P


class Test(TestCase):
    def setUp(self):
        # Monomials
        self.m = [
                  M(10, a=4),
                  M(-4, a=4),
                  M(7, y=1),
                  M(9, x=1),
                  M(-13, y=1),
                  M(-1, x=1)
                 ]

        # Polynomials
        self.p = [
                  P(self.m[0], self.m[1], self.m[2]), # 6a**4 + 7y
                  P(self.m[1], self.m[3], self.m[5]), # -4a**4 +8x
                  P(self.m[4], self.m[0]),            # -13y +10a**4
                  P(self.m[3], self.m[1]),            # 9x -4a**4
                 ]

    def test_new_init(self):
        # terms must be monomials or number
        self.assertRaises(TypeError, P, "lol")

        # terms instance of int or float are
        # converted to monomial
        self.assertIsInstance(P(3)[0], M)

        # if more terms have the same variables
        # they are summed together
        self.assertEqual(self.p[0].term_coefficient(a=4), 6)

        # if term_coefficient find nothing, the result is 0
        self.assertEqual(self.p[0].term_coefficient(k=2, b=1), 0)

    def test_add_sub(self):
        # works only with monomials, polynomials and numbers
        self.assertRaises(TypeError, lambda: self.p[0] + "something")
        self.assertRaises(TypeError, lambda: self.p[0] - [])

        # works with monomial
        self.assertEqual(self.p[0] + self.m[2], P(M(6, a=4), M(14, y=1)))
        self.assertEqual(self.p[0] - self.m[4], P(M(6, a=4), M(20, y=1)))

        # works with number
        self.assertEqual(self.p[0] + 3, P(M(6, a=4), M(7, y=1), M(3)))
        self.assertEqual(self.p[0] - 18, P(M(6, a=4), M(7, y=1), M(-18)))

        # works with polynomial
        self.assertEqual(self.p[0] + self.p[2], P(M(16, a=4), M(-6, y=1)))
        self.assertEqual(self.p[0] - self.p[2], P(M(20, y=1), M(-4, a=4)))

    def test_mul(self):
        # works only with monomials, polynomials and numbers
        self.assertRaises(TypeError, lambda: self.p[0] * "something")

        # works with monomial
        self.assertEqual(self.p[0] * self.m[2], P(M(42, a=4, y=1), M(49, y=2)))

        # works with number
        self.assertEqual(self.p[0] * 3, P(M(18, a=4), M(21, y=1)))

        # works with polynomial
        self.assertEqual(self.p[0] * self.p[2], P(M(-8, a=4, y=1), M(60, a=8), M(-91, y=2)))

    def test_reverses(self):
        # reverse add
        self.assertEqual(19 + P(M(3)), P(22))
        self.assertRaises(TypeError, lambda: "" + self.p[0])

        # reverse sub
        self.assertEqual(8 - P(M(3)), P(5))
        self.assertRaises(TypeError, lambda: "" - self.p[1])

        # reverse mul
        self.assertEqual(18 * P(M(3)), P(54))
        self.assertRaises(TypeError, lambda: "" * self.p[2])

    def test_str_repr(self):
        # a positive term is preceded by '+'
        # only if it isn't the first term
        self.assertEqual(str(self.p[2]), "-13y + 10a**4")
        self.assertEqual(str(self.p[0]), "6a**4 + 7y")

        # a negative term is preceded by '-'
        self.assertEqual(str(self.p[3]), "9x - 4a**4")

        # test repr
        self.assertEqual(repr(self.p[2]), "Polynomial(Monomial(-13, y=1), Monomial(10, a=4))")

    def test_eq_hash(self):
        # two polynomials are not equal if
        # they have not the same lenght
        self.assertFalse(self.p[3] == P(self.m[5]))

        # two polynomials can be equals but with
        # the terms in a different order
        self.assertEqual(self.p[3], P(self.m[1], self.m[3]))

        # a polynomial with a single term can be
        # compared to a monomial
        self.assertEqual(P(M(3, a=2, b=2)), M(3, a=2, b=2))
        self.assertEqual(P(M(6)), 6)

        # otherwise the result is false
        self.assertFalse(self.p[2] == {1, 7, 9})

    def test_neg(self):
        # test neg
        self.assertEqual(-self.p[2], P(-self.m[4], -self.m[0]))
