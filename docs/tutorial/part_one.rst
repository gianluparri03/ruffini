Part One: Monomials
===================

Ok, so:
we have imported ruffini because we wanted to use monomials
and polynomials in python, right? Then, let's create a monomial!

But, hey, how should we can create a monomial without any variable?
Nah, we can't, so first of all we're initializing variables:

>>> x = ruffini.variable('x')

Done. Now we can finally create a monomial!

>>> 3*x # that's a monomial!
3x

\*thinks\*

>>> y = ruffini.variable('y')
>>> -5*y
-5y

Uhm, yea... f-funny... uhm... what could we do next? We can
do operations with them:

>>> (3*x) + (5*x) # Sum!
8x
>>> 
>>> (7*y) - (-3*y) # Subtraction!
10y
>>> 
>>> (7*y) * (2*x) # Multiplication!
14xy
>>> 
>>> (7*y) ** 2 # Power!
49y**2
>>> 
>>> 5*x / 3*y # Division!
Traceback (most recent call last):
...
ValueError: variable's exponent must be positive

ouch, we can't divide by ``3y`` if there are no ``y`` in
the first term... let's try another time:

>>> (15*x*y) / (3*y) # Division! Again!
5x

It worked!

We can also calculate gcd *(greatest common divisor)* or
lcm *(least common multiplier)*, like this:

>>> gcd(15*x*y, 3*x, 3)
3
>>> lcm(15*x*y, 3*x, 2*y)
30xy

Hmmm, what's left... oh, found.

We can also evaluate a monomial:

>>> monomial = 3*x

ok, let's think. If you know that ``x = 7``, what
will 3x be equal to? You're right, 21!

>>> monomial.eval(x=7)
21

And yes, we can also set a variable's value to a monomial:

>>> monomial.eval(x=(3*y)) # 3(3y) = 9y
9y

Nice!

----

**NB:** in this tutorial, we created monomials by doing operations
with variables. We can also initialize it directly with

>>> ruffini.Monomial(5, x=1, y=2)
5xy**2

or

>>> ruffini.Monomial(5, {'x': 1, 'y': 2})
5xy**2

It's just more verbose and less readable.

----

Ok, I think we're done with monomials: let's jump to polynomials!
