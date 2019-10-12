
<p id="header" align="center">
    <img id="logo" width="220" src="https://raw.githubusercontent.com/gianluparri03/ruffini/master/logo.png" alt="Ruffini">
</p>

![](https://img.shields.io/codacy/grade/8bf3533a27104f44bdc0dad621d0de73.svg)
![](https://img.shields.io/codacy/coverage/8bf3533a27104f44bdc0dad621d0de73.svg)
![](https://img.shields.io/readthedocs/ruffini.svg)
![](https://img.shields.io/pypi/v/ruffini.svg?color=success)
![](https://img.shields.io/github/license/gianluparri03/ruffini.svg)

**Ruffini** (/rʊˈfiːni/, reference to [Paolo Ruffini](https://en.wikipedia.org/wiki/Paolo_Ruffini), Italian mathematician)
is a simple python library to compute monomials and polynomials.

## Installing

### Installing via PyPI

You can easily install the most recent release of the `ruffini` package by
downloading it from the Python Package Index (PyPI) by just doing:

```bash
pip install ruffini
```

### Installing from source

If you want to download and install the latest version of `ruffini` from this repo, type

```bash
git clone https://github.com/gianluparri03/ruffini.git
cd ruffini/src
python3 setup.py install
```

## Documentation

Documentation for this project can be found in the Read the Docs [Ruffini's page](https://ruffini.rtfd.io) in two versions:

- **latest**: the docs updated on every commit of the `master` branch
- **stable**: the docs from the latest stable release of ruffini

## Contributing

You can fork ruffini every time you want; If you are submitting a pull request, just make sure your changes are working and they aren't in conflict with the present code and tests.
If you want to test your changes, check the [testing section](#testing).
If you want to contribute, but you don't know how, just have a look at the [TODO section](#TODO).

### Testing

To test the docstring of ruffini, just go to the `src` folder and type `make doctest`.
Instead, if you want to run the unittest, the command is `make unittest`.
The Makefile also has a coverage function: if you want to see the lines of code which aren't tested with the unittest, use `make coverage`.

### Todo

- [ ] Polynomial factoring
	- [ ] Add `VariablesDict().__truediv__()`
	- [ ] Add `Monomial().__mod__()` like `VariablesDict().__mod__()`
	- [ ] Implement `Monomial().__pow__()` with floating-point exponent


## Authors

- **Parri Gianluca** - *Creator and main developer* - [@gianluparri03](https://github.com/gianluparri03)

Click on [this link](https://github.com/gianluparri03/ruffini/graphs/contributors) to see the list of contributors who participated in this project.

## License

This project is licensed under the MIT License -
see the [LICENSE.md](LICENSE.md) file for more details.
