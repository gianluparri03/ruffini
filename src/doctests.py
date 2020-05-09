import unittest, doctest

from ruffini import variables, monomials, polynomials, fpolynomials, equations


# Create the suite
suite = unittest.TestSuite()
suite.addTest(doctest.DocTestSuite(variables))
suite.addTest(doctest.DocTestSuite(monomials))
suite.addTest(doctest.DocTestSuite(polynomials))
suite.addTest(doctest.DocTestSuite(fpolynomials))
suite.addTest(doctest.DocTestSuite(equations))

# Test it
runner = unittest.TextTestRunner()
runner.run(suite)
