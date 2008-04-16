PKGNAME=pykickstart
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' ${PKGNAME}.spec | sed -e 's|%.*$$||g')
TAG=r$(VERSION)-$(RELEASE)

MANDIR=/usr/share/man
PREFIX=/usr

default: all

all:
	$(MAKE) -C po

clean:
	-rm *.tar.gz pykickstart/*.pyc
	$(MAKE) -C po clean
	python setup.py -q clean --all

install: all
	python setup.py install --root=$(DESTDIR)
	$(MAKE) -C po install

tag:
	git tag -a -m "Tag as $(TAG)" -f $(TAG)
	@echo "Tagged as $(TAG)"

archive: create-archive

src: create-archive
	@rpmbuild -ts --nodeps pykickstart-$(VERSION).tar.bz2 || exit 1
	@rm -f pykickstart-$(VERSION).tar.bz2

build: src
	@rm -rf /tmp/pykickstart
	@mkdir /tmp/pykickstart
	cd /tmp/pykickstart ; cvs co common ; cd common ; ./cvs-import.sh -b RHEL-5 $(SRPMDIR)/pykickstart-$(VERSION)-$(RELEASE).src.rpm
	@rm -rf /tmp/pykickstart
	brew build $(COLLECTION) 'cvs://cvs.devel.redhat.com/cvs/dist?pykickstart/RHEL-5#$(TAG)'

create-snapshot: tag
	@git-archive --format=tar --prefix=$(PKGNAME)-$(VERSION)/ $(TAG) | bzip2 > pykickstart-$(VERSION).tar.bz2
	@echo "the final archive is in pykickstart-$(VERSION).tar.bz2"

create-archive:
	make create-snapshot
