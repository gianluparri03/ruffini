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

**General:**
- [ ] Create a new logo
- [ ] Add `Polynomial().eval()`

**Factoring algorythms:**
- [ ] `AX + BX + AY + BY = (A + B)(X + Y)`
- [ ] `X**2 + (P + Q)X + PQ = (X + P)(X + Q)`
- [ ] `A**3 + 3A**2B + 3AB**2 + B**2 = (A + B)**3`
- [ ] `A**2 + B**2 + C**2 + 2AB + 2BC + 2AC = (A + B + C)**2`
- [ ] `A**3 + B**3 = (A + B)(A**2 - AB + B**2)`
- [ ] `A**3 - B**3 = (A - B)(A**2 + AB + B**2)`
- [ ] Ruffini's Rule

### Done

- [X] Change monomial initialization (`Monomial(5, {'x': 1})` -> `Monomial(5, x=1)`) _NB: variables will be transformed in VariablesDict however_
- [X] Add monomial's default values (`coefficient=1`, `variables={}`)
- [X] Add `Polynomial().__hash__()`
- [X] Make legal `Monomial(2, {'x': 1}).eval(x=Monomial(2, {'y': 2}))`
- [X] Add `gcd(*args)` and `lcm(*args)` in `__init__.py` as shortands
- [X] Make `__repr__()` equals to `__str__()`

- [X] Add `VariablesDict().__truediv__()`
- [X] Implement `Monomial().__pow__()` with floating-point exponent
- [X] Create the `FPolynomial` class
- [X] Adjust `FPolynomial().__eq__()`

- [X] `AX + AY = A(X + Y)`
- [X] `A**2 +2AB + B**2 = (A + B)**2`
