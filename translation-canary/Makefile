# This Makefile is just for running the tests

PYVER = $(shell python3 -c 'import sys; print("%d.%d" % (sys.version_info[0], sys.version_info[1]))')

all:
	@echo "nothing to build"

check:
	PYTHONPATH=.:$(HOME)/.local/lib/python$(PYVER)/site-packages tests/pylint/runpylint.py
	python3 -m unittest discover tests/unittests

test-projects:
	PYTHONPATH=.:$(HOME)/.local/lib/python$(PYVER)/site-packages tests/project-tests/test_projects.sh tests/project-tests/project_list.txt

ci:
	$(MAKE) check
