# Minimal makefile for PyPi

clean:
	rm ruffini-*

build:
	cp -r ../src/* .
	python3 setup.py sdist bdist_wheel
	rm setup.py
	mv dist/* .
	rm -rf build ruffini.egg-info ruffini dist

push:
	cp ruffini* to_upload
	twine upload to_upload/*
	rm -rf to_upload
