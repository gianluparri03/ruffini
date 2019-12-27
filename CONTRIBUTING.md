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
	- [X] Implement `Monomial().__pow__()` with floating-point exponent
	- [ ] Create the `FPolynomial` class
	- [ ] Think about a method to implement factoring
	- [ ] Implement the algorythms for factoring

