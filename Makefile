VERSION=$(shell grep -o version=\'.\*\' setup.py | awk -F= -e '/version=/ { print $$2 }' | tr -d \')
RC_RELEASE ?= $(shell date -u +0.1.%Y%m%d%H%M%S)
TAG=r$(VERSION)

ZANATA_PULL_ARGS = --transdir ./po/
ZANATA_PUSH_ARGS = --srcdir ./po/ --push-type source --force

tests := $(wildcard tests/*py tests/commands/*py tests/tools/*py)

NOSEARGS=-s -v -I __init__.py -I baseclass.py --processes=-1 $(tests)

COVERAGE=coverage3
PYTHON?=/usr/bin/python3

MOCKCHROOT ?= fedora-rawhide-$(shell uname -m)

all:
	$(MAKE) -C po

po-pull:
	rpm -q zanata-python-client &>/dev/null || ( echo "need to run: dnf install zanata-python-client"; exit 1 )
	zanata pull $(ZANATA_PULL_ARGS)

docs:
	$(MAKE) -C docs html text
	curl -A "programmers-guide" -o docs/programmers-guide "https://fedoraproject.org/w/index.php?title=PykickstartIntro&action=raw"

check:
ifneq ($(PYTHON),/usr/bin/python3)
	$(error The check target is only supported for python3)
endif
	@echo "*** Running pylint to verify source ***"
	PYTHONPATH=. tests/pylint/runpylint.py
	@echo "*** Running tests on translatable strings ***"
	$(MAKE) -C po pykickstart.pot
	PYTHONPATH=translation-canary $(PYTHON) -m translation_canary.translatable po/pykickstart.pot
	git checkout -- po/pykickstart.pot || true

# Left here for backwards compability - in case anyone was running the test target.  Now you always get coverage.
test: coverage

coverage:
ifneq ($(PYTHON),/usr/bin/python3)
	$(error The coverage/test target is only supported for python3)
endif
	@which $(COVERAGE) || (echo "*** Please install coverage (python3-coverage) ***"; exit 2)
	@echo "*** Running unittests with coverage ***"
	PYTHONPATH=. $(PYTHON) -m nose --with-coverage --cover-erase --cover-branches --cover-package=pykickstart --cover-package=tools $(NOSEARGS)
	-$(COVERAGE) combine
	-$(COVERAGE) report -m --include="pykickstart/*,tools/*" | tee coverage-report.log

clean:
	-rm *.tar.gz pykickstart/*.pyc pykickstart/*/*.pyc tests/*.pyc tests/*/*.pyc docs/programmers-guide *log .coverage
	$(MAKE) -C po clean
	$(PYTHON) setup.py -q clean --all

install:
	$(PYTHON) setup.py install --root=$(DESTDIR)
	$(MAKE) -C po install

tag:
	git tag -a -m "Tag as $(TAG)" -f $(TAG)
	@echo "Tagged as $(TAG)"

# Order matters, so run make twice instead of declaring them as dependencies
release:
	$(MAKE) bumpver && $(MAKE) archive
	@echo "*** Remember to run 'make pypi' afterwards ***"

pypi:
	twine upload dist/pykickstart-$(VERSION).tar.gz

archive: check test tag docs
	mkdir -p pykickstart-$(VERSION)
	git archive --format=tar --prefix=pykickstart-$(VERSION)/ $(TAG) | tar -xf -
	cp -r po/*.po pykickstart-$(VERSION)/po/
	$(MAKE) -C pykickstart-$(VERSION)/po
	cp docs/_build/text/kickstart-docs.txt docs/programmers-guide pykickstart-$(VERSION)/docs/
	PYTHONPATH=translation-canary $(PYTHON) -m translation_canary.translated --release pykickstart-$(VERSION)
	( cd pykickstart-$(VERSION) && $(PYTHON) setup.py -q sdist --dist-dir .. )
	rm -rf pykickstart-$(VERSION)
	git checkout -- po/pykickstart.pot
	@echo "The archive is in pykickstart-$(VERSION).tar.gz"

local: docs po-pull
	cp docs/_build/text/*.txt docs/
	@$(PYTHON) setup.py -q sdist --dist-dir .
	@echo "The archive is in pykickstart-$(VERSION).tar.gz"

rpmlog:
	@git log --pretty="format:- %s (%ae)" $(TAG).. |sed -e 's/@.*)/)/' | grep -v "Merge pull request"

bumpver: po-pull docs
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 2` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,3` ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	sed -i "s/version = '$(VERSION)'/version = '$$NEWVERSION'/" docs/conf.py ; \
	make -C po pykickstart.pot ; \
	zanata push $(ZANATA_PUSH_ARGS)

scratch-bumpver: docs
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 2` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,3` ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	sed -i "s/version = '$(VERSION)'/version = '$$NEWVERSION'/" docs/conf.py ; \
	make -C po pykickstart.pot

scratch: docs
	@rm -rf pykickstart-$(VERSION).tar.gz
	@rm -rf /tmp/pykickstart-$(VERSION) /tmp/pykickstart
	@dir=$$PWD; cp -a $$dir /tmp/pykickstart-$(VERSION)
	@cd /tmp/pykickstart-$(VERSION) ; $(PYTHON) setup.py -q sdist
	@cp /tmp/pykickstart-$(VERSION)/dist/pykickstart-$(VERSION).tar.gz .
	@rm -rf /tmp/pykickstart-$(VERSION)
	@echo "The archive is in pykickstart-$(VERSION).tar.gz"

rc-release: scratch-bumpver scratch
	if [ -z "$(SPECFILE)" ]; then echo "SPECFILE must be set for this target" ; exit 1; fi
	mock -r $(MOCKCHROOT) --scrub all || exit 1
	mock -r $(MOCKCHROOT) --buildsrpm  --spec $(SPECFILE) --sources . --resultdir $(shell pwd) || exit 1
	mock -r $(MOCKCHROOT) --rebuild *src.rpm --resultdir $(shell pwd)  || exit 1

ci:
	$(MAKE) PYTHON=$(PYTHON) check coverage
	$(MAKE) docs

.PHONY: check clean install tag archive local docs release
