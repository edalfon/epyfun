tests:
	pytest -s tests/ --cov=epyfun

nox310:
	nox --python=3.10

.PHONY: tests
