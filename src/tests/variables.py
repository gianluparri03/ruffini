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

        # check empty
        self.assertTrue(VD(b=0).empty)
        self.assertFalse(VD(c=1).empty)

        # str() work as a normal dict
        self.assertEqual(str(VD(x=2)), str({'x': 2}))

        # repr()
        self.assertEqual(repr(VD(y=7)), 'VariablesDict(y=7)')

        # subtraction and sum only between VariablesDict
        self.assertRaises(TypeError, lambda: VD() + {})
        self.assertRaises(TypeError, lambda: VD() - {})

        # test sum
        self.assertEqual(VD(x=2, y=3) + VD(x=6), VD(x=8, y=3))

        # test subtraction
        self.assertEqual(VD(x=2, y=3) - VD(x=2), VD(y=3))
        self.assertRaises(ValueError, lambda: VD(x=2, y=3) - VD(x=3))

        # check hash
        self.assertEqual(hash(VD(x=2, y=3)), hash((('x', 2), ('y', 3))))
