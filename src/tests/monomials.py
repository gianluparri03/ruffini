from unittest import TestCase

from ruffini import gcd, lcm
from ruffini import Monomial as M
from ruffini import Polynomial as P


class Test(TestCase):
    def setUp(self):
        # Monomials
        self.m = [
                  M(2, x=1, y=4),
                  M(-6, x=1, y=3),
                  M(8, x=1, y=4),
                  M(3),
                  M(1.16, a=4),
                  M(-9, y=3)
                 ]

    def test_init(self):
        # Coefficient must be int or float
        self.assertRaises(TypeError, M, "3")

        # default coefficient is 1
        self.assertEqual(M().coefficient, 1)

        # default variables is empty
        self.assertTrue(M().variables.is_empty)

        # if the coefficient is a whole number
        # it will be an integer
        self.assertIsInstance(M(3.0, a=2).coefficient, int)

        # check the degree
        self.assertEqual(M(2, x=2, y=7).degree, 9)

        # check is_square
        self.assertFalse(self.m[0].is_square)
        self.assertTrue(M(4, a=2, b=4).is_square)
        self.assertFalse(M(-4, a=2, b=4).is_square)

        # check is_cube
        self.assertFalse(self.m[1].is_cube)
        self.assertTrue(M(27, a=3).is_cube)
        self.assertTrue(M(-27, a=3).is_cube)

    def test_similarity(self):
        # two monomials are simimlar if they have the
        # same variables
        self.assertTrue(self.m[0].similar_to(self.m[2]))
        self.assertFalse(self.m[0].similar_to(self.m[1]))

        # if the second operator is not a monomial
        # they are never similar
        self.assertFalse(self.m[2].similar_to(""))

        # if the first operator has no variables, it
        # can be compared to floats or integers
        self.assertTrue(self.m[3].similar_to(6.28))

    def test_gcd_lcm(self):
        # only works with numbers and monomials
        self.assertRaises(TypeError, self.m[0].gcd, "")
        self.assertRaises(TypeError, self.m[0].lcm, [])

        # can work with numbers
        self.assertEqual(self.m[1].gcd(3), self.m[1].gcd(M(3)))

        # only integer coefficient
        self.assertRaises(ValueError, self.m[3].gcd, self.m[4])
        self.assertRaises(ValueError, self.m[4].gcd, self.m[3])

        # always positive result
        self.assertGreater(self.m[0].gcd(self.m[5]).coefficient, 0)
        self.assertGreater(self.m[2].lcm(self.m[3]).coefficient, 0)

        # return 0 if one term is 0
        self.assertRaises(ValueError, self.m[5].gcd, 0)
        self.assertRaises(ValueError, M(0).gcd, self.m[3])

        # values
        self.assertEqual(self.m[1].gcd(self.m[2]), M(2, x=1, y=3))
        self.assertEqual(self.m[0].lcm(self.m[5]), M(18, x=1, y=4))

        # commutative property
        self.assertEqual(self.m[0].gcd(self.m[2]), self.m[2].gcd(self.m[0]))
        self.assertEqual(self.m[0].lcm(self.m[2]), self.m[2].lcm(self.m[0]))

        # test shorthands
        self.assertEqual(gcd(3, self.m[1], self.m[5]), 3)
        self.assertEqual(lcm(6, self.m[2], self.m[3]), M(24, x=1, y=4))

    def test_add_sub(self):
        # M + (-M) = 0
        self.assertEqual(self.m[5] + (-self.m[5]), M(0))

        # M + 0 = M
        self.assertEqual(self.m[3] + 0, self.m[3])

        # The sum of two similar monomials is a monomial
        self.assertEqual(self.m[0] + self.m[2], M(10, x=1, y=4))

        # The sum of two NON similar monomials is a polynomial
        self.assertEqual(self.m[1] + self.m[3], P(self.m[1], self.m[3]))

        # The sum of a monomial and a number is a polynomial
        self.assertEqual(self.m[4] + 6.28, P(self.m[4], M(6.28)))

        # m[1] - m[2] = m[1] + (-m[2])
        self.assertEqual(self.m[0] - self.m[3], self.m[0] + (-self.m[3]))

        # only works with monomials and numbers
        self.assertRaises(TypeError, lambda: self.m[1] + [])
        self.assertRaises(TypeError, lambda: self.m[4] - "")

        # works with polynomial
        self.assertEqual(self.m[0] + P(self.m[3]), P(self.m[0], self.m[3]))
        self.assertEqual(self.m[2] - P(self.m[4]), P(self.m[2], -self.m[4]))

        # the monomial remain equal after the operation
        self.assertEqual(self.m[0], M(2, x=1, y=4))
        self.assertEqual(self.m[4], M(1.16, a=4))

    def test_mul_div(self):
        # only works with monomials and numbers
        self.assertRaises(TypeError, lambda: self.m[2] * [])
        self.assertRaises(TypeError, lambda: self.m[3] / {})

        # works with monomials
        self.assertEqual(self.m[5] * self.m[1], M(54, x=1, y=6))
        self.assertEqual(self.m[1] / self.m[5], M(2/3, x=1))

        # works with numbers
        self.assertEqual(self.m[0] * self.m[3], self.m[0] * 3)
        self.assertEqual(self.m[0] / 2, M(x=1, y=4))

        # multiplication works with polynomials
        self.assertEqual(self.m[5] * P(self.m[1]), P(self.m[5]*self.m[1]))

        # second operator's exponent must be lower than first's
        self.assertRaises(ValueError, lambda: self.m[3] / self.m[4])

        # the monomial remain equal after the operation
        self.assertEqual(self.m[1], M(-6, x=1, y=3))
        self.assertEqual(self.m[0], M(2, x=1, y=4))

    def test_pow(self):
        # works only with whole positive exponents
        self.assertRaises(ValueError, lambda: M(5) ** (-3))
        self.assertRaises(TypeError, lambda: M(17) ** 2.14)

        # if the exponentn is 0, the result is 1
        self.assertEqual(self.m[5]**0, 1)

        # you can calculate square/cube root if the
        # monomial is a square/cube
        self.assertEqual(M(4, x=2) ** (1/2), M(2, x=1))
        self.assertEqual(M(8, y=9) ** (1/3), M(2, y=3))

        # you can't do it if the monomial isn't a square or a cube
        self.assertRaises(TypeError, lambda: M(8, y=27) ** (1/2))

        # test result
        self.assertEqual(self.m[5] ** 3, M(-729, y=9))

        # the monomial remain equal after the operation
        self.assertEqual(self.m[5], M(-9, y=3))

    def test_reverses(self):
        # reverse add
        self.assertEqual(19 + self.m[3], 22)
        self.assertRaises(TypeError, lambda: "" + self.m[2])

        # reverse sub
        self.assertEqual(8 - self.m[3], 5)
        self.assertRaises(TypeError, lambda: "" - self.m[2])

        # reverse mul
        self.assertEqual(18 * self.m[3], 54)
        self.assertRaises(TypeError, lambda: "" * self.m[2])

        # reverse div
        self.assertEqual(21 / self.m[3], 7)
        self.assertRaises(TypeError, lambda: "" / self.m[2])
        self.assertRaises(ValueError, lambda: 5 / self.m[5])

    def test_eval(self):
        # test value
        self.assertEqual(self.m[5].eval(y=2), -72)

        # if a variable value isn't specified
        # it will stay there
        self.assertEqual(self.m[0].eval(x=5), M(10, y=4))

        # if there are no variables left returns an int/float
        self.assertIsInstance(self.m[5].eval(y=2), int)

        # otherwise it return a monomial
        self.assertIsInstance(self.m[2].eval(x=3), M)

        # if a variable isn't in the monomial, nothing change
        self.assertEqual(self.m[4].eval(b=7), self.m[4])

        # works only with number and monomials
        self.assertRaises(TypeError, self.m[0].eval, x="")

        # the monomial remain equal after evaluating it
        self.m[2].eval(x=2)
        self.assertEqual(self.m[2], M(8, x=1, y=4))

        # it's not case sensitive
        self.assertEqual(self.m[0].eval(x=2), self.m[0].eval(X=2))

        # a variable's value can be a monomial
        self.assertEqual(self.m[2].eval(y=M(2, x=3)), M(128, x=13))

    def test_str_repr(self):
        # normal monomial
        self.assertEqual(str(M(5, x=1, y=4)), '5xy**4')
        self.assertEqual(repr(M(5, x=1, y=4)), 'Monomial(5, x=1, y=4)')

        # coefficient == 1 w/ variables
        self.assertEqual(str(M(a=2)), 'a**2')
        self.assertEqual(repr(M(a=2)), 'Monomial(a=2)')

        # coefficient == -1 and w/ variables
        self.assertEqual(str(M(-1, k=3)), '-k**3')

        # coefficient == 0
        self.assertEqual(str(M(0, s=5)), '0')

        # w/o variables
        self.assertEqual(str(M(7)), '7')
        self.assertEqual(repr(M(7)), 'Monomial(7)')

        # coefficient == 1 w/o variables
        self.assertEqual(str(M()), '1')
        self.assertEqual(repr(M()), 'Monomial(1)')

        # coefficient == -1 w/o variables
        self.assertEqual(str(M(-1)), '-1')

    def test_eq(self):
        # same coefficient, same variables
        self.assertTrue(self.m[4] == self.m[4])

        # same variables, different coefficient
        self.assertFalse(self.m[0] == self.m[2])

        # same coefficient, different variables
        self.assertFalse(self.m[1] == M(-6, a=2))

        # different coefficient, different variables
        self.assertFalse(self.m[4] == self.m[3])

        # if there aren't variables, it can be compared
        # to a number
        self.assertTrue(self.m[3] == 3)
        self.assertFalse(self.m[3] == 17)

        # can compare only to monomials and numbers
        self.assertEqual(self.m[4].__eq__({}), False)

    def test_neg_abs(self):
        # neg
        self.assertEqual(-self.m[0], M(-self.m[0].coefficient, **self.m[0].variables))

        # abs
        self.assertEqual(abs(self.m[1]), M(abs(self.m[1].coefficient), **self.m[1].variables))

    def test_hash(self):
        # w/ variables
        self.assertEqual(hash(self.m[2]), hash((8, ('x', 1), ('y', 4))))

        # w/o variables
        self.assertEqual(hash(self.m[3]), hash(3))
