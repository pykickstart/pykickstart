PKGNAME=pykickstart
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' ${PKGNAME}.spec | sed -e 's|%.*$$||g')
TAG=r$(VERSION)-$(RELEASE)

MANDIR=/usr/share/man
PREFIX=/usr

PYCHECKEROPTS=--no-shadowbuiltin --no-argsused --no-miximport --maxargs 0 --no-local -\# 0 --only

default: all

all:
	$(MAKE) -C po

docs:
	curl -A "pykickstart-build" -o docs/kickstart-docs.txt "http://fedoraproject.org/wiki/Anaconda/Kickstart?action=raw"

check:
	PYTHONPATH=. pychecker $(PYCHECKEROPTS) pykickstart/*.py pykickstart/commands/*.py pykickstart/handlers/*.py

clean:
	-rm *.tar.gz pykickstart/*.pyc pykickstart/commands/*.pyc pykickstart/handlers/*.pyc docs/kickstart-docs.txt
	$(MAKE) -C po clean
	python setup.py -q clean --all

install: all
	python setup.py install --root=$(DESTDIR)
	$(MAKE) -C po install

tag:
	git tag -f $(TAG)

archive: tag docs
	git-archive --format=tar --prefix=${PKGNAME}-$(VERSION)/ $(TAG) > ${PKGNAME}-$(VERSION).tar
	mkdir -p ${PKGNAME}-$(VERSION)/docs/
	cp docs/kickstart-docs.txt ${PKGNAME}-$(VERSION)/docs/
	tar -rf ${PKGNAME}-$(VERSION).tar ${PKGNAME}-$(VERSION)
	gzip -9 ${PKGNAME}-$(VERSION).tar
	rm -rf ${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

local: docs
	@rm -rf ${PKGNAME}-$(VERSION).tar.gz
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@dir=$$PWD; cp -a $$dir /tmp/${PKGNAME}-$(VERSION)
	@cd /tmp/${PKGNAME}-$(VERSION) ; python setup.py -q sdist
	@cp /tmp/${PKGNAME}-$(VERSION)/dist/${PKGNAME}-$(VERSION).tar.gz .
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

.PHONY: check clean install tag archive local docs
