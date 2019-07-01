from unittest import TestCase

from ruffini import VariablesDict as VD


class Test (TestCase):
    def test(self):
        self.assertEqual(VD()['b'], 0)
        self.assertEqual(VD(a=0), VD())
        self.assertEqual(VD(x=5), VD(X=5))
        self.assertEqual(VD(y=3), VD(y=3.0))
        self.assertRaises(TypeError, VD, c=3.5)
        self.assertRaises(ValueError, VD, foo=78)
        self.assertEqual(str(VD(z=2)), str({'z': 2}))
        self.assertEqual(repr(VD(k=7)), repr({'k': 7}))
