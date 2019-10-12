# Tests

unittest:
	python3 -m unittest discover

doctest:
	python3 doctests.py

# Coverage

coverage:
	coverage run -m unittest discover
	coverage report -m
	rm .coverage

coverage-push:
	coverage run -m unittest discover
	coverage xml
	python-codacy-coverage -r coverage.xml
	rm coverage.xml .coverage

# PyPI

build-clean:
	rm ruffini-*

build:
	cp -r ../src/ruffini .
	cp -r ../src/setup.py .
	python3 setup.py sdist bdist_wheel
	rm setup.py
	mv dist/* .
	rm -rf build ruffini.egg-info ruffini dist

build-push:
	mkdir to_upload
	cp ruffini* to_upload
	twine upload to_upload/*
	rm -rf to_upload

