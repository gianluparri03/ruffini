from unittest import TestCase

from ruffini import Monomial as M
from ruffini import Polynomial as P
from ruffini import VariablesDict


class Test (TestCase):
    def test_initializing(self):
        a = M(3.4/2, {'X': 1, 'y': 3})

        # giving a wrong coefficient type
        self.assertRaises(TypeError, M, 'foo', {})

        # giving a wrong variables type
        self.assertRaises(TypeError, M, 3, [])

        # testing degree value
        self.assertEqual(a.degree, 4)

    def test_similarity(self):
        a = M(1, {'X': 1, 'y': 3})
        b = M(-4, {'x': 1, 'y': 3})
        c = M(8, {'X': 1})
        d = M(3.15, {'X': 2, 'y': 3})

        # variable omitted
        self.assertFalse(b.similar_to(c))

        # variable degree changed
        self.assertFalse(b.similar_to(d))

    def test_gcd_lcm(self):
        a = M(1, {'X': 1, 'y': 3})
        b = M(-4, {'x': 1, 'y': 3})
        c = M(8, {'X': 1})
        d = 7
        e = M(3, {})

        # commutative property
        self.assertEqual(a.gcd(b, c), b.gcd(c, a))
        self.assertEqual(a.gcd(b, c), c.gcd(a, b))
        self.assertEqual(a.lcm(b, c), b.lcm(c, a))
        self.assertEqual(a.lcm(b, c), c.lcm(a, b))
        self.assertEqual(a.lcm(b), abs(a*b) / a.gcd(b))


        # return type
        self.assertIsInstance(b.gcd(c, d), int)
        self.assertIsInstance(b.lcm(c, d), M)
        self.assertIsInstance(e.lcm(d), int)

        # arguments type
        self.assertRaises(TypeError, a.gcd, 'test')
        self.assertRaises(TypeError, a.lcm, 'anothertest')

    def test_add_sub(self):
        a = M(1, {'X': 1, 'y': 3})
        b = M(-4, {'x': 1, 'y': 3})
        c = M(8, {'x': 1})

        # return type
        self.assertIsInstance(a+c, P)
        self.assertIsInstance(b-c, P)
        self.assertEqual(a+(-a), 0)
        self.assertEqual(b-b, 0)

        # arguments type
        self.assertEqual(a+0, a)
        self.assertEqual(b-0, b)

        # commutative property
        self.assertEqual(a-b, -b+a)

    def test_mul_rmul(self):
        a = M(-4, {'x': 1, 'y': 3})
        b = M(3.15, {'X': 2, 'y': 3})

        # commutative property
        self.assertEqual(a*b, b*a)
        self.assertEqual(a*5, 5*a)

        # return type
        self.assertIsInstance(a*b, M)

        # argument type
        self.assertRaises(TypeError, lambda: a * 'foo')

    def test_truediv(self):
        a = M(-4, {'x': 1, 'y': 3})
        b = M(8, {'y': 2})
        d = M(2, {'x': 2})

        # return type
        self.assertIsInstance((7*a)/a, float)
        self.assertIsInstance(a/b, M)

        # argument variables
        self.assertRaises(ValueError, lambda: a/d)

    def test_pow(self):
        a = M(1, {'x': 2, 'y': 3})
        b = M(4, {'x': 5, 'y': 8})

        # return type
        self.assertIsInstance(a**5, M)
        self.assertIsInstance(b**2, M)

        # argument type
        self.assertRaises(TypeError, lambda: a**0.5)
        self.assertRaises(ValueError, lambda: a**(-3))

    def test_call(self):
        a = M(-4, {'x': 1, 'y': 3})

        # return value
        self.assertEqual(a(x=5, y=2.5), -312.5)

        # variable omitted
        self.assertRaises(KeyError, a, x=3)

        # wrong argument type
        self.assertRaises(TypeError, a, x="foo")

    def test_eq(self):
        a = M(-4, {'x': 1, 'y': 3})
        b = M(-4, {'x': 1})
        c = M(4, {'y': 3, 'x': 1})

        # variable omitted
        self.assertFalse(a == b)

        # changed coefficient
        self.assertFalse(a == c)

        # argument type
        self.assertTrue(M(5, {}) == 5)
        self.assertFalse(a == 'foo')

    def test_neg_abs(self):
        a = M(-4, {'x': 1, 'y': 3})
        b = M(3.15, {'X': 2, 'y': 3})

        # Test __neg__
        self.assertEqual(-a, M(4, {'x': 1, 'y': 3}))
        self.assertEqual(-b, M(-3.15, {'X': 2, 'y': 3}))

        # Test __abs__
        self.assertEqual(abs(a), -a)
        self.assertEqual(abs(b), b)

    def test_str_repr(self):
        a = M(1, {'X': 1, 'y': 3})
        b = M(0, {'x': 5, 'y': 7})
        c = M(1, {})

        # Test __str__
        self.assertEqual(str(a), "xy^3")
        self.assertEqual(str(-a), "-xy^3")
        self.assertEqual(str(b), "0")
        self.assertEqual(str(c), "1")
        self.assertEqual(str(-c), "-1")

        # Test __repr__
        self.assertEqual(repr(a), "Monomial(1, {'x': 1, 'y': 3})")
        self.assertEqual(repr(b), "Monomial(0, {'x': 5, 'y': 7})")
        self.assertEqual(repr(c), "Monomial(1, {})")

    def test_hash(self):
        a = M(-4, {'x': 1, 'y': 3})
        b = M(-4, {'X': 1, 'y': 3})
        c = M(-4, {'x': 1})
        d = M(4, {'y': 3, 'x': 1})
        e = M(-4, {'y': 3, 'x': 1})

        # Test __hash__
        self.assertTrue(hash(a) == hash(b))
        self.assertFalse(hash(a) == hash(c))
        self.assertFalse(hash(a) == hash(d))
        self.assertTrue(hash(a) == hash(e))
        self.assertTrue(hash(M(9.4, {})) == hash(9.4))
