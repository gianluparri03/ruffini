# Contributing

You can fork ruffini every time you want; If you are submitting a pull request, just make sure your changes are working and they're documented.
If you want to test your changes, check the [testing section](#testing).
If you want to contribute, but you don't know how, just have a look at the [TODO section](#TODO).

### Testing

To test the docstring of ruffini, just go to the `src` folder and type `make doctest`.
Instead, if you want to run the unittest, the command is `make unittest`.
The Makefile also has a coverage function: if you want to see the lines of code which aren't tested with the unittest, use `make coverage`.

### Todo

- [ ] Polynomial factoring:
	- [X] Add `VariablesDict().__truediv__()`
	- [ ] Add `Monomial().__mod__()` like `VariablesDict().__mod__()`
	- [ ] Implement `Monomial().__pow__()` with floating-point exponent
	- [ ] Create the `FPolynomial` class
	- [ ] Implement the algorythms for factoring:
		- [ ] `XA + XB = X(A + B)`
		- [ ] `XA + XB +YA + YB = (X + Y)(A + B)`
		- [ ] `A**2 - B**2 = (A + B)(A - B)`
		- [ ] `A**2 +2AB + B**2 = (A + B)**2`
		- [ ] `A**3 + 3A**2B + 3AB**2 + B**2 = (A + B)**3`
		- [ ] `A**2 + B**2 + C**2 + 2AB + 2BC + 2AC = (A + B + C)**2`
		- [ ] `A**3 + B**3 = (A + B)(A**2 - AB + A**2)`
		- [ ] `A**3 - B**3 = (A - B)(A**2 + AB + B**2)`
		- [ ] `X**2 + (P + Q)X + PQ = (X + P)(X + Q)`
		- [ ] Ruffini's Rule

