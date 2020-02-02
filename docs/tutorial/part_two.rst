Part Two: Polynomials
=====================

Welcome back!
So... we were talking about monomials, right?

When we tried sum and subtraction between monomials, the
variables were the same between terms, as you can see by doing

>>> (3*x).similar_to(5*x)
True

but, what happens when you sum two monomials that
aren't similar? Let's find out!

>>> (3*x) + (5*y)
3x + 5y

wow! a polynomial!

>>> (3*x) + (5*y) - 9
3x + 5y - 9

another polynomial!

*"C-Can I do operations between polynomials?"*
It depends.
You can do sums, subtractions and multiplications:

>>> ((3*x) + (5*y)) + ((-3*y) - 2) # Sum!
3x + 2y - 2
>>>
>>> (x + 3) - (2y + 1) # Subtraction!
x + 2 - 2y
>>>
>>> ((3*x) + (5*y)) * ((3*y) - 2) # Multiplication!
9xy - 6x + 15y**2 - 10y

but I've not finished factorization yet, so division and
power aren't legal

>>> (x + 2) / 4
Traceback (most recent call last):
...
TypeError: unsupported operand type(s) for /: 'Polynomial' and 'int'

sad.

Before you go crying in your bed, let me show you few other things.

We know polynomials are a sum of monomials, so they could
be considered tuples. In fact, they are. Therefore, indexing
is enabled:

>>> (2*x + 3)[0]
2x

but they're immutable objects

>>> (2*x + 3)[0] = 9
Traceback (most recent call last):
...
TypeError: 'Polynomial' object does not support item assignment

If we need the coefficient of a variable(s), we can use
a new method, called ``term_coefficient``:

>>> (5*x + 2*y - 3).term_coefficient(x)
5
>>> (5*x + 2*y - 3).term_coefficient(x=1)
5
>>> (5*x + 2*y - 3).term_coefficient({'x': 1})
5

----

Yes. There is, again, a more verbous and less readable way.
This time is *really* verbous. But, if you want...

>>> Polynomial(2*x, 5*y, -9)
2x + 5y - 9

more verbous!

>>> Polynomial(Monomial(2, x=1), Monomial(5, y=1), -9))
2x + 5y - 9

convinced?

.. doctest::
	>>> 2+ 3
	7



----

Eww, as I said before, factoring isn't finished yet, so
our tutorial should end here...

\*goes crying in his bed\*
