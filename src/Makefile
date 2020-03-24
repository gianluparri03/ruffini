# Tests

unittest:
	python3 -m unittest discover

doctest:
	python3 doctests.py

coverage:
	coverage run -m unittest discover
	coverage report -m
	rm .coverage


# PyPI

delete-build:
	rm -rf dist

build:
	python3 setup.py sdist bdist_wheel
	rm -rf build ruffini.egg-info

build-push:
	twine upload dist/*
