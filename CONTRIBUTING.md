# Contributing

You can fork ruffini every time you want; If you are submitting a pull request, just make sure your changes are working and they're documented.
If you want to test your changes, check the [testing section](#testing).
If you want to contribute, but you don't know how, just have a look at the [TODO section](#TODO).

### Testing

To test the docstring of ruffini, just go to the `src` folder and type `make doctest`.
Instead, if you want to run the unittest, the command is `make unittest`.
The Makefile also has a coverage function: if you want to see the lines of code which aren't tested with the unittest, use `make coverage`.

**NB:** If you want to run coverage tests, make sure you have installed `coverage`

### Todo

- [ ] Create a new logo
- [ ] Add `Polynomial().eval()`
- [ ] Make `Polynomial().term_coefficient(x**2)` legal

#### Done

- [X] Created tutorials in docs
- [X] Adjusted references

- [X] Added `VariablesDict().__truediv__()`
- [X] Added `Monomial().root()`
- [X] Added `Polynomial().__hash__()`
- [X] Added `FPolynomial` class

- [X] Added `gcd(*args)` and `lcm(*args)` shortands
- [X] Added `Variable()` shorthand

- [X] Made legal `Monomial(2, {'x': 1}).eval(x=Monomial(2, {'y': 2}))`
- [X] Made `__repr__()` equals to `__str__()`

- [X] Added multiple initializations (`Monomial(5, {'x': 1})` and `Monomial(5, x=1)`)
- [X] Add monomial's default values (`coefficient=1`, `variables=VariablesDict()`)

- [X] `AX + AY = A(X + Y)`
- [X] `A**2 +2AB + B**2 = (A + B)**2`
- [X] Ruffini's Rule
