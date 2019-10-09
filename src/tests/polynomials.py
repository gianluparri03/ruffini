from unittest import TestCase

from ruffini import Monomial as M
from ruffini import Polynomial as P
from ruffini import VariablesDict as VD


class Test (TestCase):
    def setUp (self):
        # Monomials
        self.m0 = M(10, {'a': 4})
        self.m1 = M(-4, {'a': 4})
        self.m2 = M(7, {'y': 1})
        self.m3 = M(9, {'x': 1})
        self.m4 = M(-13, {'y': 1})
        self.m5 = M(-1, {'x': 1})

        # Polynomials
        self.p0 = P(self.m0, self.m1, self.m2) # 6a**4 + 7y
        self.p1 = P(self.m1, self.m3, self.m5) # -4a**4 +8x
        self.p2 = P(self.m4, self.m0) # -13y +10a**4
        self.p3 = P(self.m3 , self.m1) # 9x -4a**4

    def test_new_init (self):
        # terms must be monomials or number
        self.assertRaises(TypeError, P, "lol")

        # terms instance of int or float are
        # converted to monomial
        self.assertIsInstance(P(3)[0], M)

        # if more terms have the same variables
        # they are summed together
        self.assertEqual(self.p0.term_coefficient(VD(a=4)), 6)

        # if term_coefficient find nothing, the result is 0
        self.assertEqual(self.p0.term_coefficient(VD(k=2, b=1)), 0)

    def test_add_sub (self):
        # works only with monomials, polynomials and numbers
        self.assertRaises(TypeError, lambda: self.p0 + "something")
        self.assertRaises(TypeError, lambda: self.p0 - [])

        # works with monomial
        self.assertEqual(self.p0 + self.m2, P(M(6, VD(a=4)), M(14, VD(y=1))))
        self.assertEqual(self.p0 - self.m4, P(M(6, VD(a=4)), M(20, VD(y=1))))

        # works with number
        self.assertEqual(self.p0 + 3, P(M(6, VD(a=4)), M(7, VD(y=1)), M(3, {})))
        self.assertEqual(self.p0 - 18, P(M(6, VD(a=4)), M(7, VD(y=1)), M(-18, {})))

        # works with polynomial
        self.assertEqual(self.p0 + self.p2, P(M(16, VD(a=4)), M(-6, VD(y=1))))
        self.assertEqual(self.p0 - self.p2, P(M(20, VD(y=1)), M(-4, VD(a=4))))

    def test_mul (self):
        # works only with monomials, polynomials and numbers
        self.assertRaises(TypeError, lambda: self.p0 * "something")

        # works with monomial
        self.assertEqual(self.p0 * self.m2, P(M(42, VD(a=4, y=1)), M(49, VD(y=2))))

        # works with number
        self.assertEqual(self.p0 * 3, P(M(18, VD(a=4)), M(21, VD(y=1))))

        # works with polynomial
        self.assertEqual(self.p0 * self.p2, P(M(-8, VD(a=4, y=1)), M(60, VD(a=8)), M(-91, VD(y=2))))

    def test_reverses(self):
        # reverse add
        self.assertEqual(19 + P(M(3, VD())), P(22))
        self.assertRaises(TypeError, lambda: "" + self.p0)

        # reverse sub
        self.assertEqual(8 - P(M(3, VD())), P(5))
        self.assertRaises(TypeError, lambda: "" - self.p1)

        # reverse mul
        self.assertEqual(18 * P(M(3, VD())), P(54))
        self.assertRaises(TypeError, lambda: "" * self.p2)

    def test_str_repr(self):
        # a positive term is preceded by '+'
        # only if it isn't the first term
        self.assertEqual(str(self.p2), "-13y +10a**4")
        self.assertEqual(str(self.p0), "6a**4 +7y")

        # a negative term is preceded by '-'
        self.assertEqual(str(self.p3), "9x -4a**4")

        # test repr
        self.assertEqual(repr(self.p2), "Polynomial(Monomial(-13, {'y': 1}), Monomial(10, {'a': 4}))")

    def test_eq(self):
        # two polynomials are not equal if
        # they have not the same lenght
        self.assertFalse(self.p3 == P(self.m5))

        # two polynomials can be equals but with
        # the terms in a different order
        self.assertEqual(self.p3, P(self.m1, self.m3))

        # a polynomial with a single term can be
        # compared to a monomial
        self.assertEqual(P(M(3, {'a': 2, 'b': 2})), M(3, {'a': 2, 'b': 2}))
        self.assertEqual(P(M(6, {})), 6)

        # otherwise the result is false
        self.assertFalse(self.p2 == "string")

    def test_neg(self):
        # test neg
        self.assertEqual(-self.p2, P(-self.m4, -self.m0))
