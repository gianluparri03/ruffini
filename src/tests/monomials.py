from unittest import TestCase

from ruffini import Monomial as M
from ruffini import Polynomial as P
from ruffini import VariablesDict


class Test (TestCase):
    def test_initializing(self):
        a = M(3.4/2, {'X': 1, 'y': 3})

        # Test coefficient
        self.assertIsInstance(a.coefficient, float)
        self.assertRaises(TypeError, M, 'foo')

        # Test variables
        self.assertIsInstance(a.variables, VariablesDict)
        self.assertEqual(a.variables['x'], 1)
        self.assertEqual(a.variables['b'], 0)
        self.assertNotIn('b', a.variables)
        self.assertRaises(ValueError, M, 1, {'xy': 2})
        self.assertRaises(ValueError, M, 1, {'x': -3})
        self.assertRaises(TypeError, M, 59, [])
        self.assertIn('x', a.variables)
        self.assertNotIn('X', a.variables)

        # Test degree
        self.assertEqual(a.degree, 4)

    def test_similarity(self):
        a = M(1, {'X': 1, 'y': 3})
        b = M(-4, {'x': 1, 'y': 3})
        c = M(8, {'X': 1})
        d = M(3.15, {'X': 2, 'y': 3})

        # Test similarity
        self.assertTrue(b.similar_to(a))
        self.assertFalse(b.similar_to(c))
        self.assertFalse(b.similar_to(d))
        self.assertFalse(c.similar_to(a))

    def test_gcd_lcm(self):
        a = M(1, {'X': 1, 'y': 3})
        b = M(-4, {'x': 1, 'y': 3})
        c = M(8, {'X': 1})

        # Test gcd
        self.assertEqual(a.gcd(b, c), b.gcd(c, a))
        self.assertEqual(a.gcd(b, c), c.gcd(a, b))
        self.assertEqual(a.gcd(b, c), M(1, {'x': 1}))

        # Test lcm
        self.assertEqual(a.lcm(b, c), b.lcm(c, a))
        self.assertEqual(a.lcm(b, c), c.lcm(a, b))
        self.assertEqual(a.lcm(b, c), M(8, {'x': 1, 'y': 3}))

    def test_add_sub(self):
        a = M(1, {'X': 1, 'y': 3})
        b = M(-4, {'x': 1, 'y': 3})
        c = M(8, {'x': 1})

        # Test __add__
        self.assertEqual(a+b, M(-3, {'x': 1, 'y': 3}))
        self.assertIsInstance(a+c, P)
        self.assertEqual(a+(-a), 0)
        self.assertEqual(a+0, a)

        # Test __sub__
        self.assertEqual(a-b, a+(-b), M(5, {'x': 1, 'y': 3}))
        self.assertIsInstance(b-c, P)
        self.assertEqual(a-a, 0)

    def test_mul_rmul(self):
        a = M(-4, {'x': 1, 'y': 3})
        b = M(3.15, {'X': 2, 'y': 3})

        # Test __mul__
        self.assertEqual(a*5, M(-20, {'x': 1, 'y': 3}))
        self.assertEqual(a*b, b*a)
        self.assertEqual(a*b, M(-12.6, {'x': 3, 'y': 6}))
        self.assertRaises(TypeError, sum, [a, "foo"])

        # Test __rmul__
        self.assertEqual(a*5, 5*a)
        self.assertRaises(TypeError, sum, ["foo", b])

    def test_truediv(self):
        a = M(-4, {'x': 1, 'y': 3})
        b = M(8, {'X': 1, 'y': 3})
        c = M(-2, {'x': 1, 'y': 2})
        d = M(2, {'x': 2})

        # Test __truediv__
        self.assertEqual(a/b, M(-0.5, {}))
        self.assertEqual(a/c, M(2, {'y': 1}))
        self.assertRaises(ValueError, lambda: a/d)
        self.assertEqual(a/a, 1)

    def test_pow(self):
        a = M(1, {'x': 2, 'y': 3})
        b = M(4, {'x': 5, 'y': 8})

        # Test __pow__
        self.assertEqual(a**5, M(1, {'x': 10, 'y': 15}))
        self.assertEqual(b**2, M(16, {'x': 10, 'y': 16}))
        self.assertRaises(TypeError, lambda: a**0.5)
        self.assertRaises(ValueError, lambda: a**(-3))

    def test_call(self):
        a = M(-4, {'x': 1, 'y': 3})

        self.assertEqual(a(x=5, y=2), -160)
        self.assertEqual(a(x=5, y=2), a(X=5, y=2))
        self.assertRaises(KeyError, a, x=3)
        self.assertRaises(TypeError, a, x="foo")

    def test_eq(self):
        a = M(-4, {'x': 1, 'y': 3})
        b = M(-4, {'X': 1, 'y': 3})
        c = M(-4, {'x': 1})
        d = M(4, {'y': 3, 'x': 1})
        e = M(-4, {'x': 1, 'y': 3})

        # Test __eq__
        self.assertTrue(a == b)
        self.assertFalse(a == c)
        self.assertFalse(a == d)
        self.assertTrue(a == e)
        self.assertTrue(M(5) == 5)

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
        self.assertTrue(hash(M(9.4)) == hash(9.4))
