# What is this package?
NLSPACKAGE	= pykickstart
POTFILE		= $(NLSPACKAGE).pot
INSTALL		= /usr/bin/install -c
INSTALL_DATA	= $(INSTALL) -m 644
INSTALL_DIR	= /usr/bin/install -d

# destination directory
PYTHON?=python
DESTDIR ?= $(RPM_BUILD_ROOT)
INSTALL_NLS_DIR = $(DESTDIR)/`$(PYTHON) -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"`/$(NLSPACKAGE)/locale

# PO catalog handling
MSGMERGE	= msgmerge -v
XGETTEXT	= xgettext --default-domain=$(NLSPACKAGE) --add-comments --sort-output
MSGFMT		= msgfmt --statistics --verbose

# What do we need to do
POFILES		= $(wildcard *.po)
MOFILES		= $(patsubst %.po,%.mo,$(POFILES))
PYSRC		= $(wildcard ../pykickstart/*.py) $(wildcard ../pykickstart/*/*.py)
SRCFILES 	= $(PYSRC) $(wildcard ../tools/ks*)

all::  update-po $(MOFILES)

$(POTFILE): $(SRCFILES)
	$(XGETTEXT) -L Python --keyword=_ --keyword=N_ $(SRCFILES)
	@if cmp -s $(NLSPACKAGE).po $(POTFILE); then \
	    rm -f $(NLSPACKAGE).po; \
	else \
	    mv -f $(NLSPACKAGE).po $(POTFILE); \
	fi; \

update-po: Makefile $(POTFILE) refresh-po

refresh-po: Makefile
	for cat in $(POFILES); do \
		lang=`basename $$cat .po`; \
		if $(MSGMERGE) $$lang.po $(POTFILE) > $$lang.pot ; then \
			mv -f $$lang.pot $$lang.po ; \
			echo "$(MSGMERGE) of $$lang succeeded" ; \
		else \
			echo "$(MSGMERGE) of $$lang failed" ; \
			rm -f $$lang.pot ; \
		fi \
	done

clean:
	@rm -fv *mo *~ .depend

install: $(MOFILES)
	@for n in $(MOFILES); do \
	    l=`basename $$n .mo`; \
	    $(INSTALL_DIR) $(INSTALL_NLS_DIR)/$$l/LC_MESSAGES; \
	    $(INSTALL_DATA) --verbose $$n $(INSTALL_NLS_DIR)/$$l/LC_MESSAGES/$(NLSPACKAGE).mo; \
	done

%.mo: %.po
	$(MSGFMT) -o $@ $<

.PHONY: missing depend


