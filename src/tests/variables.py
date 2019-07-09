from unittest import TestCase

from ruffini import VariablesDict as VD


class Test (TestCase):
    def test(self):
        # Keys has to be made lowecasse
        self.assertEqual(VD(X=3), VD(x=3))
        # Keys must be string
        self.assertRaises(TypeError, VD().__setitem__, [], 5)
        # Keys' lenght must be 1
        self.assertRaises(ValueError, VD().__setitem__, "", 5)
        self.assertRaises(ValueError, VD().__setitem__, "ab", 5)
        # Keys must be alphabetical
        self.assertRaises(ValueError, VD().__setitem__, "$a", 5)

        # If a pair key:value doesn't exist,
        # the exponent is 0
        self.assertEqual(VD()['x'], 0)
        # Exponent must be int or float
        self.assertRaises(TypeError, VD().__setitem__, 'a', [])
        # Exponent must be a whole number
        self.assertRaises(ValueError, VD().__setitem__, 'b', 5.3)
        # Exponent must be positive
        self.assertRaises(ValueError, VD().__setitem__, 'c', -2)
        # If exponent is float and has no decimals
        # it will be made int
        self.assertEqual(VD(a=5.0), VD(a=5))
        # If the exponent is 0 the variables won't
        # be inserted into the dictionary
        self.assertEqual(VD(c=0), VD())

        # str() and repr() are the same for dict and
        # VariablesDict
        self.assertEqual(str(VD(x=2)), str({'x': 2}))
        self.assertEqual(repr(VD(y=7)), repr({'y': 7}))
