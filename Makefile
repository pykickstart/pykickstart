VERSION     = $(shell grep -o version=\'.\*\' setup.py | awk -F= -e '/version=/ { print $$2 }' | tr -d \')
RC_RELEASE ?= $(shell date -u +0.1.%Y%m%d%H%M%S)
TAG         = r$(VERSION)
PREVTAG    := $(shell git tag --sort=-creatordate | head -n 2 | tail -n 1)
COVERAGE   ?= coverage3
PYTHON     ?= python3
MOCKCHROOT ?= fedora-rawhide-$(shell uname -m)

PYTHON_VERSION = $(shell ${PYTHON} -c "print(__import__('sys').version_info[0])")

GPGKEY ?= $(shell git config user.signingkey)

WEBLATE_REPO = git@github.com:pykickstart/weblate
WEBLATE_BRANCH ?= $(shell git branch --show-current)

tests := $(wildcard tests/*py tests/commands/*py tests/tools/*py)

all:
	$(MAKE) -C po

po-pull:
	-rm -rf ./weblate/
	git clone --depth=1 -b $(WEBLATE_BRANCH) $(WEBLATE_REPO) ./weblate/
	cp ./weblate/*.po ./weblate/*.pot ./po/

po-push:
	make -C po pykickstart.pot
	-rm -rf ./weblate/
	git clone --depth=1 -b $(WEBLATE_BRANCH) $(WEBLATE_REPO) ./weblate/
	cp po/pykickstart.pot ./weblate/
	git -C ./weblate/ commit -m "Update pykickstart.pot" -- pykickstart.pot
	git -C ./weblate/ push

docs:
	$(MAKE) -C docs html text

check:
ifneq ($(PYTHON_VERSION),3)
	$(error The check target is only supported for python3)
endif
	@echo "*** Running pylint to verify source ***"
	PYTHONPATH=. tests/pylint/runpylint.py
	@echo "*** Running tests on translatable strings ***"
	$(MAKE) -C po pykickstart.pot
	PYTHONPATH=translation-canary $(PYTHON) -m translation_canary.translatable po/pykickstart.pot

# Left here for backwards compability - in case anyone was running the test target.  Now you always get coverage.
test: coverage

coverage:
ifneq ($(PYTHON_VERSION),3)
	$(error The coverage/test target is only supported for python3)
endif
	@which $(COVERAGE) || (echo "*** Please install coverage (python3-coverage) ***"; exit 2)
	@echo "*** Running unittests with coverage ***"
	PYTHONPATH=. $(COVERAGE) run -p --branch --source=pykickstart,tools -m unittest -v $(tests)
	-$(COVERAGE) combine
	-$(COVERAGE) report -m --include="pykickstart/*,tools/*" | tee coverage-report.log

clean:
	-rm *.tar.gz pykickstart/*.pyc pykickstart/*/*.pyc tests/*.pyc tests/*/*.pyc *log .coverage pykickstart.spec
	$(MAKE) -C po clean
	$(PYTHON) setup.py -q clean --all

install:
	$(PYTHON) setup.py install --root=$(DESTDIR)
	$(MAKE) -C po install

tag:
	git tag -u $(GPGKEY) -m "Tag as $(TAG)" -f $(TAG)
	@echo "Tagged as $(TAG)"

# Order matters, so run make twice instead of declaring them as dependencies
release:
	if [ -z "$(GPGKEY)" ]; then echo "ERROR: The git config user.signingkey must be set" ; exit 1; fi
	$(MAKE) po-pull && $(MAKE) bumpver && $(MAKE) check && $(MAKE) test && $(MAKE) tag && $(MAKE) archive && $(MAKE) sign

sign:
	gpg --armor --detach-sign -u $(GPGKEY) pykickstart-$(VERSION).tar.gz
	@echo "*** Remember to run 'make pypi' afterwards ***"

pypi:
	@echo "***************************************************************************"
	@echo "* Username and password are for your pypi.org login.                      *"
	@echo "* NOTE: You must be a listed maintainer for pykickstart for this to work. *"
	@echo "***************************************************************************"
	@echo
	twine upload --repository-url https://upload.pypi.org/legacy/ pykickstart-$(VERSION).tar.gz

archive: docs
	mkdir -p pykickstart-$(VERSION)
	git archive --format=tar --prefix=pykickstart-$(VERSION)/ $(TAG) | tar -xf -
	cp -r po/*.po pykickstart-$(VERSION)/po/
	$(MAKE) -C pykickstart-$(VERSION)/po
	cp docs/_build/text/kickstart-docs.txt docs/programmers-guide pykickstart-$(VERSION)/docs/
	PYTHONPATH=translation-canary $(PYTHON) -m translation_canary.translated --release pykickstart-$(VERSION)
	( cd pykickstart-$(VERSION) && $(PYTHON) setup.py -q sdist --dist-dir .. )
	rm -rf pykickstart-$(VERSION)
	@echo "The archive is in pykickstart-$(VERSION).tar.gz"

local: docs po-pull
	cp docs/_build/text/*.txt docs/
	@$(PYTHON) setup.py -q sdist --dist-dir .
	@echo "# To create the signature, run this command:" > pykickstart-$(VERSION).tar.gz.asc
	@echo "# gpg --detach-sign --armor pykickstart-$(VERSION).tar.gz" >> pykickstart-$(VERSION).tar.gz.asc
	@echo "The archive is in pykickstart-$(VERSION).tar.gz"

rpmlog:
	@git log --pretty="format:- %s (%ae)" $(PREVTAG)..$(TAG) |sed -e 's/@.*)/)/' | grep -v "Merge pull request"

bumpver: docs
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 2` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,3` ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	sed -i "s/version = '$(VERSION)'/version = '$$NEWVERSION'/" docs/conf.py ; \
	sed -i "s/__version__ = '$(VERSION)'/__version__ = '$$NEWVERSION'/" pykickstart/__init__.py ; \
	git add setup.py docs/conf.py pykickstart/__init__.py; \
	git commit -m "New release: $$NEWVERSION"

pykickstart.spec: pykickstart.spec.in
	sed -e "s/%%VERSION%%/$(VERSION)/" < $< > $@

scratch-bumpver: docs
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 2` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,3` ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	sed -i "s/version = '$(VERSION)'/version = '$$NEWVERSION'/" docs/conf.py ; \
	sed -i "s/__version__ = '$(VERSION)'/__version__ = '$$NEWVERSION'/" pykickstart/__init__.py

scratch: docs
	@rm -rf pykickstart-$(VERSION).tar.gz
	@rm -rf /tmp/pykickstart-$(VERSION) /tmp/pykickstart
	@dir=$$PWD; cp -a $$dir /tmp/pykickstart-$(VERSION)
	@cd /tmp/pykickstart-$(VERSION) ; $(PYTHON) setup.py -q sdist
	@cp /tmp/pykickstart-$(VERSION)/dist/pykickstart-$(VERSION).tar.gz .
	@rm -rf /tmp/pykickstart-$(VERSION)
	@echo "The archive is in pykickstart-$(VERSION).tar.gz"

rc-release: scratch-bumpver scratch pykickstart.spec
	if [ -z "$(SPECFILE)" ]; then echo "SPECFILE must be set for this target" ; exit 1; fi
	mock -r $(MOCKCHROOT) --scrub all || exit 1
	mock -r $(MOCKCHROOT) --buildsrpm  --spec $(SPECFILE) --sources . --resultdir $(shell pwd) || exit 1
	mock -r $(MOCKCHROOT) --rebuild *src.rpm --resultdir $(shell pwd)  || exit 1

.PHONY: check clean install tag archive local docs release sign
