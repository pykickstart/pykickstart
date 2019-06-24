# This Makefile is just for running the tests

PIP_PATH = $(shell $(PYTHON) -m pip show ordered_set | grep Location: | cut -d ' ' -f 2)

all:
	@echo "nothing to build"

check:
	PYTHONPATH=.:$(PIP_PATH) tests/pylint/runpylint.py
	python3 -m unittest discover tests/unittests

test-projects:
	PYTHONPATH=.:$(PIP_PATH) tests/project-tests/test_projects.sh tests/project-tests/project_list.txt

ci:
	$(MAKE) check
