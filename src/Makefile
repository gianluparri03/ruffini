test:
	python3 -m unittest discover -v

coverage:
	coverage run -m unittest discover
	coverage report -m
	rm .coverage

coverage-push:
	coverage run -m unittest discover
	coverage xml
	python-codacy-coverage -r coverage.xml
	rm coverage.xml .coverage
