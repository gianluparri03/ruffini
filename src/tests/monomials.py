from unittest import TestCase

from ruffini import Monomial as M
from ruffini import Polynomial as P
from ruffini import VariablesDict as VD


class Test (TestCase):
    def setUp(self):
        self.m0 = M(2, {'x': 1, 'y': 1})
        self.m1 = M(-6, {'x': 1, 'y': 3})
        self.m2 = M(8, {'x': 1, 'y': 1})
        self.m3 = M(3, {})
        self.m4 = M(1.16, {'a': 4})
        self.m5 = M(-9, {'y': 3})

    def test_init (self):
        # Coefficient must be int or float
        self.assertRaises(TypeError, M, "3", {})

        # Variables must be a dict
        self.assertRaises(TypeError, M, 8, [])

        # Variables are stored in a new VariabesDict
        self.assertIsInstance(M(3, {}).variables, VD)
        variables = {}
        self.assertIsNot(M(2, variables).variables, variables)

        # If variables is a variablesdict, it won't
        # be regenerated
        variables = VD()
        self.assertIs(M(2, variables).variables, variables)

        # check the degree
        self.assertEqual(M(2, {'x': 2, 'y': 7}).degree, 9)

    def test_similarity(self):
        # two monomials are simimlar if they have the
        # same variables
        self.assertTrue(self.m0.similar_to(self.m2))
        self.assertFalse(self.m0.similar_to(self.m1))

        # if the second operator is not a monomial
        # they are never similar
        self.assertFalse(self.m2.similar_to(""))

        # if the first operator has no variables, it
        # can be compared to floats or integers
        self.assertTrue(self.m3.similar_to(6.28))

    def test_gcd_lcm(self):
        # only works with numbers and monomials
        self.assertRaises(TypeError, self.m0.gcd, "")
        self.assertRaises(TypeError, self.m0.lcm, [])

        # can work with numbers
        self.assertEqual(self.m1.gcd(3), self.m1.gcd(M(3, {})))

        # only integer coefficient
        self.assertRaises(ValueError, self.m3.gcd, self.m4)
        self.assertRaises(ValueError, self.m4.gcd, self.m3)

        # always positive result
        self.assertGreater(self.m0.gcd(self.m5).coefficient, 0)
        self.assertGreater(self.m2.lcm(self.m3).coefficient, 0)

        # return 0 if one term is 0
        self.assertRaises(ValueError, self.m5.gcd, 0)
        self.assertRaises(ValueError, M(0, {}).gcd, self.m3)

        # values
        self.assertEqual(self.m1.gcd(self.m2), M(2, {'x': 1, 'y': 1}))
        self.assertEqual(self.m0.lcm(self.m5), M(18, {'x': 1, 'y': 3}))

        # commutative property
        self.assertEqual(self.m0.gcd(self.m2), self.m2.gcd(self.m0))
        self.assertEqual(self.m0.lcm(self.m2), self.m2.lcm(self.m0))

    def test_add_sub(self):
        # M + (-M) = 0
        self.assertIsInstance(self.m5 + (-self.m5), int)

        # M + 0 = M
        self.assertEqual(self.m3 + 0, self.m3)

        # The sum of two similar monomials is a monomial
        self.assertEqual(self.m0 + self.m2, M(10, {'x': 1, 'y': 1}))

        # The sum of two NON similar monomials is a polynomial
        self.assertEqual(self.m1 + self.m3, P(self.m1, self.m3))

        # The sum of a monomial and a number is a polynomial
        self.assertEqual(self.m4 + 6.28, P(self.m4, M(6.28, {})))

        # The sum of a number and a monomial with no variables
        # is a number
        self.assertIsInstance(M(18, {}) + 3, int)

        # m1 - m2 = m1 + (-m2)
        self.assertEqual(self.m0 - self.m3, self.m0 + (-self.m3))

        # only works with monomials and numbers
        self.assertRaises(TypeError, lambda: self.m1 + [])
        self.assertRaises(TypeError, lambda: self.m4 - "")

        # the monomial remain equal after the operation
        self.assertEqual(self.m0, M(2, {'x': 1, 'y': 1}))
        self.assertEqual(self.m4, M(1.16, {'a': 4}))

    def test_mul_div(self):
        # only works with monomials and numbers
        self.assertRaises(TypeError, lambda: self.m2 * [])
        self.assertRaises(TypeError, lambda: self.m3 / {})

        # monomial * monomial
        self.assertEqual(self.m5 * self.m1, M(54, {'x': 1, 'y': 6}))

        # monomial * number
        self.assertEqual(self.m0 * self.m3, self.m0 * 3)

        # monomial / monomial
        self.assertEqual(self.m1 / self.m5, M(2/3, {'x': 1}))

        # monomial / number
        self.assertEqual(self.m0 / 2, M(1, {'x': 1, 'y': 1}))

        # if the first operator is a multiple of the
        # second, the result is a number
        self.assertIsInstance(self.m2 / self.m0, int)

        # the coefficient is automatically converted to int
        self.assertIsInstance((self.m1 / self.m0).coefficient, int)

        # second operator's exponent must be lower than first's
        self.assertRaises(ValueError, lambda: self.m3 / self.m4)

        # the monomial remain equal after the operation
        self.assertEqual(self.m1, M(-6, {'x': 1, 'y': 3}))
        self.assertEqual(self.m0, M(2, {'x': 1, 'y': 1}))

    def test_pow(self):
        # works only with whole positive exponents
        self.assertRaises(ValueError, lambda: M(5, {}) ** (-3))
        self.assertRaises(TypeError, lambda: M(17, {}) ** 2.14)

        # test result
        self.assertEqual(self.m5 ** 3, M(-729, {'y': 9}))

        # the monomial remain equal after the operation
        self.assertEqual(self.m5, M(-9, {'y': 3}))

    def test_reverses(self):
        # reverse add
        self.assertEqual(19 + self.m3, 22)
        self.assertEqual(self.m2.__radd__(""), NotImplemented)

        # reverse sub
        self.assertEqual(8 - self.m3, 5)
        self.assertEqual(self.m2.__rsub__(""), NotImplemented)

        # reverse mul
        self.assertEqual(18 * self.m3, 54)
        self.assertEqual(self.m2.__rmul__(""), NotImplemented)

        # reverse div
        self.assertEqual(21 / self.m3, 7)
        self.assertEqual(self.m2.__rtruediv__(""), NotImplemented)
        self.assertRaises(ValueError, lambda: 5 / self.m5)

    def test_call(self):
        # test value
        self.assertEqual(self.m5(y=2), -72)

        # if a variable value isn't specified
        # it will stay there
        self.assertEqual(self.m0(x=5), M(10, {'y': 1}))

        # if there are no variables left returns an int/float
        self.assertIsInstance(self.m5(y=2), int)

        # otherwise it return a monomial
        self.assertIsInstance(self.m2(x=3), M)

        # if a variable isn't in the monomial, nothing change
        self.assertEqual(self.m4(b=7), self.m4)

        # works only with number
        self.assertRaises(TypeError, self.m0, x="")

        # the monomial remain equal after evaluating it
        self.m2(x=2)
        self.assertEqual(self.m2, M(8, {'x': 1, 'y': 1}))

        # it's not case sensitive
        self.assertEqual(self.m0(x=2), self.m0(X=2))

    def test_str_repr(self):
        # normal monomial
        self.assertEqual(str(M(5, {'x': 1, 'y': 1})), '5xy')

        # coefficient == 1 w/ variables
        self.assertEqual(str(M(1, {'a': 2})), 'a^2')

        # coefficient == -1 and w/ variables
        self.assertEqual(str(M(-1, {'k': 3})), '-k^3')

        # coefficient == 0
        self.assertEqual(str(M(0, {'s': 5})), '0')

        # coefficient == 1 w/o variables
        self.assertEqual(str(M(1, {})), '1')

        # coefficient == -1 w/o variables
        self.assertEqual(str(M(-1, {})), '-1')

        # repr
        self.assertEqual(repr(M(5, {'b': 2, 'k': 3})), "Monomial(5, {'b': 2, 'k': 3})")

    def test_eq(self):
        # same coefficient, same variables
        self.assertTrue(self.m4 == self.m4)

        # same variables, different coefficient
        self.assertFalse(self.m0 == self.m2)

        # same coefficient, different variables
        self.assertFalse(self.m1 == M(-6, {'a': 2}))

        # different coefficient, different variables
        self.assertFalse(self.m4 == self.m3)

        # if there aren't variables, it can be compared
        # to a number
        self.assertTrue(self.m3 == 3)
        self.assertFalse(self.m3 == 17)

        # can compare only to monomials and numbers
        self.assertEqual(self.m4.__eq__({}), NotImplemented)

    def test_neg_abs(self):
        # neg
        self.assertEqual(-self.m0, M(-self.m0.coefficient, self.m0.variables))

        # abs
        self.assertEqual(abs(self.m1), M(abs(self.m1.coefficient), self.m1.variables))

    def test_hash(self):
        # w/ variables
        self.assertEqual(hash(self.m2), hash((8, ('x', 1), ('y', 1))))

        # w/o variables
        self.assertEqual(hash(self.m3), hash(3))
