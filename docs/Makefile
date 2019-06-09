# Minimal makefile for Sphinx documentation

clean:
	rm -rf _* *.js *.html

html:
	sphinx-build -b html source .
	rm -rf .doctrees
	rm .buildinfo objects.inv

apidoc:
	rm source/*.rst
	sphinx-apidoc -o source ../src/ruffini
	cp source/modules.rst source/index.rst

doctest:
	python3 -m doctest ../src/ruffini/monomials.py
	python3 -m doctest ../src/ruffini/polynomials.py
