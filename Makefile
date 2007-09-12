PKGNAME=pykickstart
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' ${PKGNAME}.spec | sed -e 's|%.*$$||g')
CVSTAG=r$(subst .,_,$(VERSION)-$(RELEASE))

MANDIR=/usr/share/man
PREFIX=/usr

PYCHECKEROPTS=--no-shadowbuiltin --no-argsused --no-miximport --maxargs 0 --no-local -\# 0 --only

default: all

all:
	$(MAKE) -C po

docs:
	curl -A "pykickstart-build" -o docs/kickstart-docs.txt "http://fedoraproject.org/wiki/AnacondaKickstart?action=raw"

check:
	PYTHONPATH=. pychecker $(PYCHECKEROPTS) pykickstart/*.py pykickstart/commands/*.py pykickstart/handlers/*.py

clean:
	-rm *.tar.gz pykickstart/*.pyc pykickstart/commands/*.pyc pykickstart/handlers/*.pyc docs/kickstart-docs.txt
	$(MAKE) -C po clean
	python setup.py -q clean --all

install: all docs
	python setup.py install --root=$(DESTDIR)
	$(MAKE) -C po install

tag:
	cvs tag -FR $(CVSTAG)

archive: tag docs
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@CVSROOT=`cat CVS/Root`; cd /tmp; cvs -d $$CVSROOT export -r$(CVSTAG) ${PKGNAME}
	@cp docs/kickstart-docs.txt /tmp/${PKGNAME}/docs/
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@cd /tmp/${PKGNAME}-$(VERSION) ; python setup.py -q sdist
	@cp /tmp/${PKGNAME}-$(VERSION)/dist/${PKGNAME}-$(VERSION).tar.gz .
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
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
