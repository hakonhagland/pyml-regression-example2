#ROOT := $(dir $(lastword $(MAKEFILE_LIST)))
ROOT := $(shell pwd)

.PHONY: coverage docs mypy test publish-to-pypi tox
.PHONY: ruff-check ruff-fix ruff-format rstcheck view-docs

coverage:
	coverage run -m pytest tests
	coverage report -m

docs:
	cd "$(ROOT)"/docs && make clean && make html

view-docs:
	@xdg-open "file://$(ROOT)/docs/_build/html/index.html"

mypy:
	mypy --strict src/ tests/

ruff-check:
	ruff check src tests

ruff-fix:
	ruff check --fix src tests

ruff-format:
	ruff format src tests

rstcheck:
	rstcheck -r docs/

publish-to-pypi:
	uv build
	twine upload dist/*

test:
	pytest tests/

tox:
	tox
