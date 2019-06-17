# Minimal makefile for Sphinx documentation

clean:
	rm -rf *.rst

apidoc:
	rm source/*.rst
	sphinx-apidoc -o source ../src/ruffini
	cp source/modules.rst source/index.rst

doctest:
	python3 -m doctest ../src/ruffini/monomials.py
	python3 -m doctest ../src/ruffini/polynomials.py
