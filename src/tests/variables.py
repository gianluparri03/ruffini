from unittest import TestCase

from ruffini import VariablesDict as VD


class Test(TestCase):
    def test_general(self):
        # Keys has to be made lowecasse
        self.assertEqual(VD(X=3), VD(x=3))

        # VariablesDict is immutable
        self.assertRaises(TypeError, lambda: VD().__setitem__('b', 2))
        self.assertRaises(TypeError, lambda: VD().__delitem__('s'))
        self.assertRaises(TypeError, lambda: VD().clear())
        self.assertRaises(TypeError, lambda: VD().pop('c'))

        # Keys' lenght must be 1
        self.assertRaises(ValueError, lambda: VD(ab=5))

        # Keys must be alphabetical
        self.assertRaises(ValueError, lambda: VD(_5a=1))

        # If a pair key:value doesn't exist,
        # the exponent is 0
        self.assertEqual(VD()['x'], 0)

        # Exponent must be int or float
        self.assertRaises(TypeError, lambda: VD(a=[]))

        # Exponent must be a whole number
        self.assertRaises(ValueError, lambda: VD(b=5.3))

        # Exponent must be positive
        self.assertRaises(ValueError, lambda: VD(c=-2))

        # If exponent is float and has no decimals
        # it will be made int
        self.assertEqual(VD(a=5.0), VD(a=5))

        # If the exponent is 0 the variables won't
        # be inserted into the dictionary
        self.assertEqual(VD(c=0), VD())

        # check empty
        self.assertTrue(VD(b=0).is_empty)
        self.assertFalse(VD(c=1).is_empty)

        # check hash
        self.assertEqual(hash(VD(x=2, y=3)), hash((('x', 2), ('y', 3))))

    def test_str_repr(self):
        # str() work as a normal dict
        self.assertEqual(str(VD(x=2)), str({'x': 2}))

        # repr()
        self.assertEqual(repr(VD(y=7)), 'VariablesDict(y=7)')

        # subtraction and sum only between VariablesDict
        self.assertRaises(TypeError, lambda: VD() + {})
        self.assertRaises(TypeError, lambda: VD() - {})

    def test_operations(self):
        # test sum
        self.assertEqual(VD(x=2, y=3) + VD(x=6), VD(x=8, y=3))

        # test subtraction
        self.assertEqual(VD(x=2, y=3) - VD(x=2), VD(y=3))
        self.assertRaises(ValueError, lambda: VD(x=2, y=3) - VD(x=3))

        # test multiplication
        self.assertRaises(TypeError, lambda: VD() * 3.14)
        self.assertRaises(ValueError, lambda: VD() * (-1))
        self.assertEqual(VD(a=2, b=5) * 2, VD(a=4, b=10))

        # test module
        self.assertRaises(TypeError, lambda: VD() % 4.12)
        self.assertRaises(ValueError, lambda: VD() % (-7))
        self.assertFalse(VD(a=2, b=5) % 2)
        self.assertTrue(VD(a=2, b=4) % 2)
        self.assertTrue(VD(a=3, b=6) % 3)

        # test division
        self.assertEqual(VD(a=2, b=4) / 2, VD(a=1, b=2))
        self.assertRaises(ValueError, lambda: VD(a=3) / 2)
        self.assertRaises(TypeError, lambda: VD(a=3) / 2.56)
