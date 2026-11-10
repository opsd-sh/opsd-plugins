.DEFAULT_GOAL := help

PYTHON ?= python3
PROVIDER ?= openai

.PHONY: help build test

help:
	@printf '%s\n' \
		'make build  Build the production plugin and local marketplace' \
		'make test   Run the packaging checks'

build:
	$(PYTHON) scripts/build.py --provider "$(PROVIDER)"

test:
	$(PYTHON) -m unittest discover -s tests -v
