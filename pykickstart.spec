Name:      pykickstart
Version:   3.4
Release:   1%{?dist}
License:   GPLv2 and MIT
Group:     System Environment/Libraries
Summary:   Python utilities for manipulating kickstart files.
Url:       http://fedoraproject.org/wiki/pykickstart
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0:   %{name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires: gettext
BuildRequires: python-coverage
BuildRequires: python-devel
BuildRequires: python-nose
BuildRequires: python-ordered-set
BuildRequires: python-setuptools
BuildRequires: python-requests

BuildRequires: python3-coverage
BuildRequires: python3-devel
BuildRequires: python3-mypy
BuildRequires: python3-nose
BuildRequires: python3-ordered-set
BuildRequires: python3-requests
BuildRequires: python3-setuptools
BuildRequires: python3-six
BuildRequires: python3-sphinx

Requires: python3-kickstart = %{version}-%{release}

%description
Python utilities for manipulating kickstart files.  The Python 2 and 3 libraries
can be found in the packages python-kickstart and python3-kickstart
respectively.

# Python 2 library
%package -n python-kickstart
Summary:  Python 2 library for manipulating kickstart files.
Requires: python-six
Requires: python-requests
Requires: python-ordered-set

%description -n python-kickstart
Python 2 library for manipulating kickstart files.  The binaries are found in
the pykickstart package.

# Python 3 library
%package -n python3-kickstart
Summary:  Python 3 library for manipulating kickstart files.
Requires: python3-six
Requires: python3-requests
Requires: python3-ordered-set

%description -n python3-kickstart
Python 3 library for manipulating kickstart files.  The binaries are found in
the pykickstart package.

%prep
%setup -q

rm -rf %{py3dir}
mkdir %{py3dir}
cp -a . %{py3dir}

%build
make PYTHON=%{__python2}

pushd %{py3dir}
make PYTHON=%{__python3}
popd

%install
rm -rf %{buildroot}
make PYTHON=%{__python2} DESTDIR=%{buildroot} install

pushd %{py3dir}
make PYTHON=%{__python3} DESTDIR=%{buildroot} install
popd

%check
make PYTHON=%{__python2} test

pushd %{py3dir}
make PYTHON=%{__python3} test
popd

%files
%defattr(-,root,root,-)
%license COPYING
%doc README.rst
%doc data/kickstart.vim
%{_bindir}/ksvalidator
%{_bindir}/ksflatten
%{_bindir}/ksverdiff
%{_bindir}/ksshell
%{_mandir}/man1/*

%files -n python-kickstart
%defattr(-,root,root,-)
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.txt
%{python2_sitelib}/pykickstart*egg*
%{python2_sitelib}/pykickstart/*py*
%{python2_sitelib}/pykickstart/commands/*py*
%{python2_sitelib}/pykickstart/handlers/*py*
%{python2_sitelib}/pykickstart/locale/

%files -n python3-kickstart
%defattr(-,root,root,-)
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.txt
%{python3_sitelib}/pykickstart*egg*
%{python3_sitelib}/pykickstart/*py*
%{python3_sitelib}/pykickstart/commands/*py*
%{python3_sitelib}/pykickstart/handlers/*py*
%{python3_sitelib}/pykickstart/locale/

%changelog
* Thu Oct 06 2016 Chris Lumens <clumens@redhat.com> - 3.4-1
- Fix Python 2 builds by assigning to KSOptionParser.version properly (#106) (atodorov)
- Do not run translation-canary under python2. (clumens)
- Add network --no-activate option. (#104) (rvykydal)
- Don't run the ksvalidator test under python2. (clumens)
- Fix the check for the error raised by the logvol command on python2. (clumens)
- Support timezone command usage without timezone specification (mkolman)
- Formatting fixes (mkolman)
- Stylistic improvements as sugested by static chackers (#95) (martin.kolman)
- Fix unused-variable warning (atodorov)
- Fix command handler errors identified by previous test (atodorov)
- Test for older versions in new Fedora releases. Closes #28 (atodorov)
- Rename FC16 to F16 so we can find it later in versionMap (atodorov)
- Update sys.path in handlers/control.py if not already updated (atodorov)
- KSOptionParser accepts description, not help argument (atodorov)
- Remove unused import (atodorov)
- Fix class definition problems identified by previous test (atodorov)
- Test how command and data classes are defined (atodorov)
- Fix a couple problems with the previous ksvalidator patches. (clumens)
- Remove a bunch of history from the spec file. (clumens)
- Refactor ksvalidator and its tests (#90) (atodorov)
- Fix some code smells (#89) (atodorov)
- Enable Travis-CI (#88) (atodorov)
- Add versionToLongString to the type annotation file. (clumens)
- Update tests to reflect new positional arguments (atodorov)
- Add empty help/description for KSOptionParser (atodorov)
- Add custom help formatter for ArgumentParser (atodorov)
- Initial Sphinx configuration (atodorov)
- The pykickstart package should require a specific python3-kickstart. (clumens)
- Shuffle network command options for more logical order. (rvykydal)
- Update documentation of network command. (rvykydal)
- Update documentation of network command. (rvykydal)
- Download translations less frequently. (#83) (dshea)
- Adapt to the new version of mypy (#82) (dshea)
- Remove the locales from zanata.xml. (clumens)

* Tue May 10 2016 Chris Lumens <clumens@redhat.com> - 3.3-1
- Do not check translated strings during make check. (dshea)
- Merge the most recent translation-canary changes. (dshea)
- Squashed 'translation-canary/' changes from 5a45c19..840c2d6 (dshea)
- Add documentation for --excludeWeakdeps (dshea)
- Add support for --excludeWeakdeps option to %packages. (james)
- Numbers can be part of a kickstart command option. (clumens)
- It's authconfig, not autoconfig (in the kickstart.vim file). (clumens)
- Fix pylint no-member errors. (clumens)
- Support file URLs for ostree (#1327460). (clumens)
- Add ksvalidator test cases (jikortus)
- Add classes for pykickstart tools testing (jikortus)
- ksvalidator - don't require KS file with -l option (jikortus)

* Thu Apr 14 2016 Chris Lumens <clumens@redhat.com> - 3.2-1
- Fix a couple mistakes in the documentation. (clumens)
- Correctly move scripts after they've been installed. (clumens)
- Document %traceback and %onerror. (clumens)
- Add a new %onerror script section (#74). (clumens)
- Enable coverage reporting for pykickstart tools (jikortus)
- Fix really long lines in the documentation. (clumens)
- Lots of documentation updates. (clumens)

* Wed Mar 30 2016 Chris Lumens <clumens@redhat.com> - 3.1-1
- Fix the version of the parser in packages tests, too. (clumens)
- PWD doesn't work in the Makefile. (clumens)
- Disable the attrs test for python2. (clumens)
- Accept alternate names for some keyword arguments. (clumens)
- Don't change ignoredisk.ignoredisk in the __init__ method. (clumens)
- Fix bugs where F16 and F18 were using the wrong versions of objects. (clumens)
- Allow marking options as "notest". (clumens)
- Add a test case for various ways of setting attributes. (clumens)
- Add a dataClass attribute to KickstartCommand. (clumens)
- Add a test case for deprecated command corner cases. (clumens)
- Add --chunksize option to raid command. (vtrefny)
- Add a test case for the deprecated multipath command. (clumens)
- Mark the device, dmraid, and multipath commands as deprecated. (clumens)
- Get rid of the ver global variable. (clumens)
- Remove deprecated commands from the documentation. (clumens)
- Add Fedora 25 support. (vtrefny)
- Add some more tests for parser-related corner cases. (clumens)
- Fix processing of the #platform= comment. (clumens)
- Get rid of a bunch of unnecessary blank lines. (clumens)
- fix formating (Frodox)
- Change network example to working one (Frodox)
- Add DNF system-upgrade near FedUp references (github)

* Fri Mar 04 2016 Chris Lumens <clumens@redhat.com> - 3.0-1
- Make sure the script test references parser. (clumens)
- Don't use class attributes for the version or kickstart string. (clumens)
- Add a syntax highlighting file for vim. (clumens)
- Move tests/parser/* into the tests/ directory. (clumens)
- Use importlib to import modules. (dshea)
- Update kickstart documentation for ntp (jkonecny)
- It's self.sshkey, not self.key. (clumens)
- Remove orderedset.py (dshea)
- Remove the removal of the eintr checker, which has been removed (dshea)
- Improved method.py test coverage (jikortus)
- Verify that a password with a # sign doesn't get read as a comment. (clumens)
- Raise deprecation warnings in _setToSelf and _setToObj. (clumens)
- Do not log httpd messages in the load tests. (dshea)
- There is no F7_Key class - use RHEL5_Key instead. (clumens)
- The RHEL6 branch supported the key command. (clumens)
- Add more test coverage around Group and Script objects. (clumens)
- load.py initial test coverage + exception catch (jikortus)
- Fix more formatting problems under the part command. (clumens)
- Fix some indentation problems in the documentation. (clumens)
- Clear up confusing documentation about MB vs. MiB. (clumens)
- argparse error messages are different in python2 and python3. (clumens)
- Add a document describing how to adapt your code to pykickstart-3. (clumens)
- Promote _setToObj and _setToSelf to public functions. (clumens)
- Increase test coverage to 96%. (clumens)
- Don't duplicate autopart+volgroup checks in the volgroup handlers. (clumens)
- RHEL7 needs to use the correct version of FcoeData and Autopart. (clumens)
- Replace required=1 and deprecated=1 with =True. (clumens)
- Get rid of unnecessary args to add_argument. (clumens)
- Get rid of references to KickstartParseError in assert_parse_error. (clumens)
- Convert command objects to use argparse instead of optparse. (clumens)
- Remove KickstartValueError. (clumens)
- Add some custom actions and types to make things easier elsewhere. (clumens)
- _setToSelf and _setToObj now take a Namespace object. (clumens)
- Use the new ksboolean function where we were using the string. (clumens)
- Convert options.py to use argparse instead of optparse. (clumens)
- Remove the custom map and map_extend actions. (clumens)
- Try harder to test translations. (dshea)
