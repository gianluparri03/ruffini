from unittest import TestCase
from re import escape as escape_regex

from ruffini import *


class Test(TestCase):
    def assertRaises(self, exception, error, callable, *args, **kwargs):
        self.assertRaisesRegex(exception, escape_regex(error), callable, *args, **kwargs)

    def test_initialization(self):
        # Variables aren't case sensitive
        self.assertEqual(VariablesDict(X=3), VariablesDict(x=3))

        # Variables must be string, alphabetical and one character long
        self.assertRaises(TypeError, "variable's name must be a string", VariablesDict, {9: 9})
        self.assertRaises(ValueError, "variable's name length must be one", VariablesDict, ab=5)
        self.assertRaises(ValueError, "variable's name must be alphabetical", VariablesDict, _5a=1)

        # Exponents must be positive whole numbers
        self.assertRaises(TypeError, "variable's exponent must be int", VariablesDict, a="5.3")
        self.assertRaises(ValueError, "variable's exponent must be positive", VariablesDict, c=-2)
        self.assertRaises(TypeError, "variable's exponent must be a whole number", VariablesDict, b=5.3)
        self.assertEqual(VariablesDict(a=5.0), VariablesDict(a=5))

        # Variables with exponent equal to 0 arent't stored
        self.assertEqual(VariablesDict(c=0), VariablesDict())

        # is_empty
        self.assertTrue(VariablesDict(b=0).is_empty)
        self.assertFalse(VariablesDict(c=1).is_empty)

    def test_setters_getters(self):
        # If a variable isn't in the dict its exponent is 0
        self.assertEqual(VariablesDict(a=2)['a'], 2)

        # If a variable isn't in the dict its exponent is 0
        self.assertEqual(VariablesDict()['x'], 0)

        # __getitem__'s errors
        self.assertRaises(TypeError, "variable's name must be a string", VariablesDict().__getitem__, [])
        self.assertRaises(ValueError, "variable's name length must be one", VariablesDict().__getitem__, 'ab')
        self.assertRaises(ValueError, "variable's name must be alphabetical", VariablesDict().__getitem__, '_5a')

        # VariablesDict is immutable
        self.assertRaises(AttributeError, "'VariablesDict' object has no attribute '__setitem__'", lambda: VariablesDict().__setitem__('b', 2))
        self.assertRaises(AttributeError, "'VariablesDict' object has no attribute '__delitem__'", lambda: VariablesDict().__delitem__('s'))

    def test_str_repr_hash(self):
        # __str__() works as a normal dict
        self.assertEqual(str(VariablesDict(x=2)), str({'x': 2}))

        # __repr__() == __str__()
        self.assertEqual(repr(VariablesDict(y=4)), str(VariablesDict(y=4)))

        # __hash__()
        self.assertEqual(hash(VariablesDict(x=2, y=3)), hash((('x', 2), ('y', 3))))

    def test_operations(self):
        # __add__()
        self.assertEqual(VariablesDict(x=2, y=3) + VariablesDict(x=2), VariablesDict(x=4, y=3))
        self.assertRaises(TypeError, "unsupported operand type(s) for +: 'VariablesDict' and 'dict'", lambda: VariablesDict() + {})

        # __sub__()
        self.assertEqual(VariablesDict(x=2, y=3) - VariablesDict(x=2), VariablesDict(y=3))
        self.assertRaises(ValueError, "variable's exponent must be positive", lambda: VariablesDict(x=2, y=3) - VariablesDict(x=3))
        self.assertRaises(TypeError, "unsupported operand type(s) for -: 'VariablesDict' and 'dict'", lambda: VariablesDict() - {})

        # __mul__()
        self.assertEqual(VariablesDict(a=2, b=5) * 2, VariablesDict(a=4, b=10))
        self.assertRaises(ValueError, "can't multiply a VariablesDict by a negative number", lambda: VariablesDict() * (-1))
        self.assertRaises(TypeError, "unsupported operand type(s) for *: 'VariablesDict' and 'dict'", lambda: VariablesDict() * {})

        # __truediv__()
        self.assertEqual(VariablesDict(a=2, b=4) / 2, VariablesDict(a=1, b=2))
        self.assertRaises(ValueError, "can't divide this VariablesDict by 2", lambda: VariablesDict(a=3) / 2)
        self.assertRaises(TypeError, "unsupported operand type(s) for /: 'VariablesDict' and 'float'", lambda: VariablesDict(a=3) / 2.56)

        # __mod__()
        self.assertFalse(VariablesDict(a=2, b=3) % 2)
        self.assertTrue(VariablesDict(a=2, b=4) % 2)
        self.assertRaises(TypeError, "unsupported operand type(s) for %: 'VariablesDict' and 'float'", lambda: VariablesDict() % 4.12)
        self.assertRaises(ValueError, "can't use modulus with VariablesDict and negative numbers", lambda: VariablesDict() % (-7))
