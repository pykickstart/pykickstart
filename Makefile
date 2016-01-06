PKGNAME=pykickstart
SPECFILE=$(PKGNAME).spec
VERSION=$(shell awk '/Version:/ { print $$2 }' $(SPECFILE))
RELEASE=$(shell awk '/Release:/ { print $$2 }' $(SPECFILE) | sed -e 's|%.*$$||g')
RC_RELEASE ?= $(shell date -u +0.1.%Y%m%d%H%M%S)
TAG=r$(VERSION)-$(RELEASE)

ZANATA_PULL_ARGS = --transdir ./po/
ZANATA_PUSH_ARGS = --srcdir ./po/ --push-type source --force

MANDIR=/usr/share/man
PREFIX=/usr

NOSEARGS=-s -v -I __init__.py -I baseclass.py tests/*py tests/commands/*py tests/parser/*py

PYTHON?=python3
COVERAGE?=coverage3
ifeq ($(PYTHON),python)
  COVERAGE=coverage
else
  # Coverage + multiprocessing does not work under python2.  Oh well, just don't use multiprocessing there.
  # We default to python3 now so everyone else can just deal with the slowness.
  NOSEARGS+=--processes=-1
endif

MOCKCHROOT ?= fedora-rawhide-$(shell uname -m)

all:
	$(MAKE) -C po

po-pull:
	rpm -q zanata-python-client &>/dev/null || ( echo "need to run: dnf install zanata-python-client"; exit 1 )
	zanata pull $(ZANATA_PULL_ARGS)

po-empty:
	for lingua in $$(gawk 'match($$0, /locale>(.*)<\/locale/, ary) {print ary[1]}' ./zanata.xml) ; do \
		[ -f ./po/$$lingua.po ] || \
		msginit -i ./po/$(PKGNAME).pot -o ./po/$$lingua.po --no-translator || \
		exit 1 ; \
	done

docs:
	curl -A "programmers-guide" -o docs/programmers-guide "https://fedoraproject.org/w/index.php?title=PykickstartIntro&action=raw"

check:
	@echo "*** Running pylint to verify source ***"
	PYTHONPATH=. tests/pylint/runpylint.py
	@echo "*** Running tests on translatable strings ***"
	PYTHONPATH=translation-canary python3 -m translation_canary.translatable po/$(PKGNAME).pot
	@echo "*** Running tests on translated strings ***"
	PYTHONPATH=translation-canary python3 -m translation_canary.translated .

# Left here for backwards compability - in case anyone was running the test target.  Now you always get coverage.
test: coverage

coverage:
	@which $(COVERAGE) || (echo "*** Please install coverage (python3-coverage) ***"; exit 2)
	@echo "*** Running unittests with coverage ***"
	PYTHONPATH=. $(PYTHON) -m nose --with-coverage --cover-erase --cover-branches --cover-package=pykickstart $(NOSEARGS)
	$(COVERAGE) combine
	$(COVERAGE) report -m | tee coverage-report.log
	@which mypy || (echo "*** Please install mypy (python3-mypy) ***"; exit 2)
	@echo "*** Running type checks ***"
	PYTHONPATH=. mypy --use-python-path pykickstart

clean:
	-rm *.tar.gz pykickstart/*.pyc pykickstart/*/*.pyc tests/*.pyc tests/*/*.pyc docs/programmers-guide
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

archive: check test tag docs
	mkdir -p $(PKGNAME)-$(VERSION)
	git archive --format=tar --prefix=$(PKGNAME)-$(VERSION)/ $(TAG) | tar -xf -
	cp -r po/*.po $(PKGNAME)-$(VERSION)/po/
	$(MAKE) -C $(PKGNAME)-$(VERSION)/po
	cp docs/programmers-guide $(PKGNAME)-$(VERSION)/docs/
	PYTHONPATH=translation-canary python3 -m translation_canary.translated --release $(PKGNAME)-$(VERSION)
	( cd $(PKGNAME)-$(VERSION) && $(PYTHON) setup.py -q sdist --dist-dir .. )
	rm -rf $(PKGNAME)-$(VERSION)
	git checkout -- po/$(PKGNAME).pot
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

local: docs po-pull
	@$(PYTHON) setup.py -q sdist --dist-dir .
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

rpmlog:
	@git log --pretty="format:- %s (%ae)" $(TAG).. |sed -e 's/@.*)/)/' | grep -v "Merge pull request"

bumpver: po-pull
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 2` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,3` ; \
	DATELINE="* `date "+%a %b %d %Y"` `git config user.name` <`git config user.email`> - $$NEWVERSION-1"  ; \
	cl=`grep -n %changelog $(SPECFILE) |cut -d : -f 1` ; \
	tail --lines=+$$(($$cl + 1)) $(SPECFILE) > speclog ; \
	(head -n $$cl $(SPECFILE) ; echo "$$DATELINE" ; make --quiet rpmlog 2>/dev/null ; echo ""; cat speclog) > $(SPECFILE).new ; \
	mv $(SPECFILE).new $(SPECFILE) ; rm -f speclog ; \
	sed -i "s/Version:   $(VERSION)/Version:   $$NEWVERSION/" $(SPECFILE) ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	make -C po $(PKGNAME).pot ; \
	zanata push $(ZANATA_PUSH_ARGS)

scratch-bumpver: po-empty
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 2` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,3` ; \
	DATELINE="* `date "+%a %b %d %Y"` `git config user.name` <`git config user.email`> - $$NEWVERSION-$(RC_RELEASE)"  ; \
	cl=`grep -n %changelog $(SPECFILE) |cut -d : -f 1` ; \
	tail --lines=+$$(($$cl + 1)) $(SPECFILE) > speclog ; \
	(head -n $$cl $(SPECFILE) ; echo "$$DATELINE" ; make --quiet rpmlog 2>/dev/null ; echo ""; cat speclog) > $(SPECFILE).new ; \
	mv $(SPECFILE).new $(SPECFILE) ; rm -f speclog ; \
	sed -i "s/Version:   $(VERSION)/Version:   $$NEWVERSION/" $(SPECFILE) ; \
	sed -i "s/Release:   $(RELEASE)/Release:   $(RC_RELEASE)/" $(SPECFILE) ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	make -C po $(PKGNAME).pot

scratch: docs po-empty
	@rm -rf $(PKGNAME)-$(VERSION).tar.gz
	@rm -rf /tmp/$(PKGNAME)-$(VERSION) /tmp/$(PKGNAME)
	@dir=$$PWD; cp -a $$dir /tmp/$(PKGNAME)-$(VERSION)
	@cd /tmp/$(PKGNAME)-$(VERSION) ; $(PYTHON) setup.py -q sdist
	@cp /tmp/$(PKGNAME)-$(VERSION)/dist/$(PKGNAME)-$(VERSION).tar.gz .
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

rc-release: scratch-bumpver scratch
	mock -r $(MOCKCHROOT) --scrub all || exit 1
	mock -r $(MOCKCHROOT) --buildsrpm  --spec ./$(SPECFILE) --sources . --resultdir $(PWD) || exit 1
	mock -r $(MOCKCHROOT) --rebuild *src.rpm --resultdir $(PWD)  || exit 1

ci:
	$(MAKE) PYTHON=python3 check coverage

.PHONY: check clean install tag archive local docs release
