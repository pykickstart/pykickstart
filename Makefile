PKGNAME=pykickstart
VERSION=$(shell awk '/Version:/ { print $$2 }' $(PKGNAME).spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' $(PKGNAME).spec | sed -e 's|%.*$$||g')
TAG=r$(VERSION)-$(RELEASE)

TX_PULL_ARGS = -a --disable-overwrite
TX_PUSH_ARGS = -s

MANDIR=/usr/share/man
PREFIX=/usr

TESTSUITE:=tests/baseclass.py

all:
	$(MAKE) -C po

po-pull:
	tx pull $(TX_PULL_ARGS)

docs:
	curl -A "pykickstart-build" -o docs/kickstart-docs.txt "https://fedoraproject.org/w/index.php?title=Anaconda/Kickstart&action=raw"
	curl -A "programmers-guide" -o docs/programmers-guide "https://fedoraproject.org/w/index.php?title=PykickstartIntro&action=raw"

check:
	@echo "*** Running pylint to verify source ***"
	PYTHONPATH=. pylint tools/* pykickstart/*.py pykickstart/*/*.py --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}' --rcfile=/dev/null -r n --disable=C,R --dummy-variables-rgx=_ --disable=deprecated-lambda,bad-builtin,star-args,protected-access,arguments-differ,fixme,global-statement,broad-except

test:
	@echo "*** Running unittests ***"
	PYTHONPATH=. python $(TESTSUITE) -v

coverage:
	@which coverage || (echo "*** Please install python-coverage ***"; exit 2)
	@echo "*** Running unittests with coverage ***"
	PYTHONPATH=. coverage run $(TESTSUITE) -v
	PYTHONPATH=. coverage report --show-missing --include='pykickstart/*'

clean:
	-rm *.tar.gz pykickstart/*.pyc pykickstart/*/*.pyc tests/*.pyc tests/*/*.pyc docs/kickstart-docs.txt docs/programmers-guide ChangeLog
	$(MAKE) -C po clean
	python setup.py -q clean --all

install:
	python setup.py install --root=$(DESTDIR)
	$(MAKE) -C po install

ChangeLog:
	(GIT_DIR=.git git log > .changelog.tmp && mv .changelog.tmp ChangeLog; rm -f .changelog.tmp) || (touch ChangeLog; echo 'git directory not found: installing possibly empty changelog.' >&2)

tag:
	git tag -a -m "Tag as $(TAG)" -f $(TAG)
	@echo "Tagged as $(TAG)"

archive: check test tag docs
	@rm -f ChangeLog
	@make ChangeLog
	git archive --format=tar --prefix=$(PKGNAME)-$(VERSION)/ $(TAG) > $(PKGNAME)-$(VERSION).tar
	mkdir -p $(PKGNAME)-$(VERSION)
	cp -r po $(PKGNAME)-$(VERSION)/po/
	mkdir -p $(PKGNAME)-$(VERSION)/docs/
	cp docs/kickstart-docs.txt $(PKGNAME)-$(VERSION)/docs/
	cp docs/programmers-guide $(PKGNAME)-$(VERSION)/docs/
	cp ChangeLog $(PKGNAME)-$(VERSION)/
	tar -rf $(PKGNAME)-$(VERSION).tar $(PKGNAME)-$(VERSION)
	gzip -9 $(PKGNAME)-$(VERSION).tar
	rm -rf $(PKGNAME)-$(VERSION)
	git checkout -- po/$(PKGNAME).pot
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

local: docs po-pull
	@rm -f ChangeLog
	@make ChangeLog
	@rm -rf $(PKGNAME)-$(VERSION).tar.gz
	@rm -rf /tmp/$(PKGNAME)-$(VERSION) /tmp/$(PKGNAME)
	@dir=$$PWD; cp -a $$dir /tmp/$(PKGNAME)-$(VERSION)
	@cd /tmp/$(PKGNAME)-$(VERSION) ; python setup.py -q sdist
	@cp /tmp/$(PKGNAME)-$(VERSION)/dist/$(PKGNAME)-$(VERSION).tar.gz .
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

rpmlog:
	@git log --pretty="format:- %s (%ae)" $(TAG).. |sed -e 's/@.*)/)/'
	@echo

bumpver: po-pull
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 3` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,2,4` ; \
	DATELINE="* `date "+%a %b %d %Y"` `git config user.name` <`git config user.email`> - $$NEWVERSION-1"  ; \
	cl=`grep -n %changelog pykickstart.spec |cut -d : -f 1` ; \
	tail --lines=+$$(($$cl + 1)) pykickstart.spec > speclog ; \
	(head -n $$cl pykickstart.spec ; echo "$$DATELINE" ; make --quiet rpmlog 2>/dev/null ; echo ""; cat speclog) > pykickstart.spec.new ; \
	mv pykickstart.spec.new pykickstart.spec ; rm -f speclog ; \
	sed -i "s/Version: $(VERSION)/Version: $$NEWVERSION/" pykickstart.spec ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py ; \
	make -C po $(PKGNAME).pot ; \
	tx push $(TX_PUSH_ARGS)

.PHONY: check clean install tag archive local docs
