import unittest
import doctest
from ruffini import monomials, polynomials, variables

# Create the suite
suite = unittest.TestSuite()
suite.addTest(doctest.DocTestSuite(monomials))
suite.addTest(doctest.DocTestSuite(polynomials))
suite.addTest(doctest.DocTestSuite(variables))

# Test it
runner = unittest.TextTestRunner()
runner.run(suite)
