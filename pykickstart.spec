Name:      pykickstart
Version:   3.3
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
%doc README
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
%doc docs/kickstart-docs.rst
%{python2_sitelib}/pykickstart*egg*
%{python2_sitelib}/pykickstart/*py*
%{python2_sitelib}/pykickstart/commands/*py*
%{python2_sitelib}/pykickstart/handlers/*py*
%{python2_sitelib}/pykickstart/locale/

%files -n python3-kickstart
%defattr(-,root,root,-)
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.rst
%{python3_sitelib}/pykickstart*egg*
%{python3_sitelib}/pykickstart/*py*
%{python3_sitelib}/pykickstart/commands/*py*
%{python3_sitelib}/pykickstart/handlers/*py*
%{python3_sitelib}/pykickstart/locale/

%changelog
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

* Mon Jan 11 2016 Chris Lumens <clumens@redhat.com> - 2.24-1
- Add build requires on python-coverage and python3-mypy. (clumens)

* Mon Jan 11 2016 Chris Lumens <clumens@redhat.com> - 2.23-1
- Add type information to parser.py and sections.py. (clumens)
- Fix some of the types in base.py. (clumens)
- Don't set currentCmd on the handler object. (clumens)
- Remove logs and coverage files from the "clean" target. (clumens)
- Fix the if block in the Makefile to be much more clear. (clumens)
- Get rid of the BuildRequires: transifex. (clumens)
- Get rid of the "test" makefile target.  Use "coverage" for everything. (clumens)
- Use python3 by default in the spec file and Makefile. (clumens)
- Remove the #! line from setup.py. (clumens)
- Remove spec file history from before version 1.99. (clumens)
- Add some initial static typing information to pykickstart. (dshea)
- Fix a bug in how arguments were being passed to zanata. (clumens)

* Tue Jan 05 2016 Chris Lumens <clumens@redhat.com> - 2.22-1
- Use six.assertRaisesRegex to keep the tests working in python2. (dshea)
- Rename deprecated assert methods to whatever we're supposed to be using. (clumens)
- Fix class inheritance in RHEL6_VolGroup (ccoyle)
- Run the translation-canary tests during make archive (dshea)
- Run translation-canary tests from make check (dshea)
- Ignore translation-canary when running pylint. (dshea)
- Correct problems in translatable format strings. (dshea)
- Use the xgettext_werror to generate pykickstart.pot (dshea)
- Use setup.py's sdist to create the release tarball. (dshea)
- Squashed 'translation-canary/' content from commit 5a45c19 (dshea)

* Mon Nov 30 2015 Chris Lumens <clumens@redhat.com> - 2.21-1
- Add tests for all the preprocess functions. (clumens)
- Reimplement the existing preprocess functions. (clumens)
- Add new preprocess functions that return a string. (clumens)
- _preprocessStateMachine shouldn't do any writing to disk. (clumens)
- Import tempfile when it's needed, not globally. (clumens)

* Mon Nov 09 2015 Chris Lumens <clumens@redhat.com> - 2.20-1
- Only decode as utf-8 when using py3 (bcl)
- Add --sshkey to sshpw command (#1274104) (bcl)
- Fix an xconfig test case. (clumens)
- The xconfig --server option was apparently removed by FC6. (clumens)
- Add a test for the xconfig command. (clumens)
- Read kickstart files in binary, decode to utf-8 (bcl)

* Tue Nov 03 2015 Chris Lumens <clumens@redhat.com> - 2.19-1
- We don't actually need to BuildRequires python-pocketlint. (clumens)
- docs/kickstart-docs.rst: iscrypted has no argument (sol)

* Thu Oct 22 2015 Chris Lumens <clumens@redhat.com> - 2.18-1
- More tests for driverdisk, iscsi, ostreesetup, partition, raid and repo commands (atodorov)
- Add more unit tests (atodorov)
- pykickstart: don't set bootProto if --noipv4 (jbacik)
- Produce coverage-report.log for CI (atodorov)

* Wed Oct 07 2015 Chris Lumens <clumens@redhat.com> - 2.17-1
- Add Fedora 24 support. (clumens)
- Update the RHEL7 version constant. (clumens)
- ostree repos can only be HTTP or HTTPS. (clumens)
- Allow GIDs to be specified in the user --groups list. (dshea)
- docs: Add `--activate` as an explicit network option to the list (walters)

* Fri Sep 25 2015 Chris Lumens <clumens@redhat.com> - 2.16-1
- Add reqpart to docs (pbokoc)
- link to github docs instead of fedora wiki (mmckinst)
- Differentiate between empty and missing instLangs (dshea)
- Add tests for empty and missing --instLangs values. (dshea)

* Tue Sep 08 2015 Chris Lumens <clumens@redhat.com> - 2.15-1
- Fix a typo in the README. (clumens)
- Check whether requests actually fetched the URL (dshea)
- Return URL loads as str instead of bytes (dshea)
- Add test cases for including kickstart data via URL. (dshea)

* Thu Aug 27 2015 Chris Lumens <clumens@redhat.com> - 2.14-1
- Fix writing out an empty %packages section when using ksflatten. (clumens)
- Fix a typo in output from the RHEL6 logvol command. (clumens)
- Increase test coverage by a couple percent. (clumens)
- Fix zfcp equality testing for F12 and later. (clumens)
- Fix warning on adding a second user with the same name. (clumens)
- Directories have to be the same in harddrive equality testing. (clumens)

* Wed Aug 05 2015 Chris Lumens <clumens@redhat.com> - 2.13-1
- Fix liveimg equality check (bcl)
- improve test coverage for version.py (atodorov)

* Thu Jul 30 2015 Chris Lumens <clumens@redhat.com> - 2.12-1
- Avoid polluting generated kickstarts by unexpected reqpart commands (#1164660) (mkolman)
- Don't always assume the mock chroot is on x86_64. (clumens)
- Remove documentation compilation warnings (jkonecny)
- Use sys.exit instead of os._exit. (clumens)
- Add a new makefile target that does everything needed for jenkins. (clumens)

* Thu Jul 09 2015 Chris Lumens <clumens@redhat.com> - 2.11-1
- Run nosetests with the same python as was passed to make. (clumens)
- Looks like Group still needs to define __hash__ to be hashable. (clumens)

* Mon Jul 06 2015 Chris Lumens <clumens@redhat.com> - 2.10-1
- Don't forget to call the superclass's __init__ in Group now. (clumens)
- Group objects need to be hashable. (clumens)
- Ignore some more files. (clumens)
- Don't allow using --fsprofile and --mkfsopts at the same time. (clumens)

* Mon Jun 22 2015 Chris Lumens <clumens@redhat.com> - 2.9-1
- Add --mkfsoptions to btrfs, logvol, partition, and raid commands. (clumens)
- Document the unit used for the --cachesize option (vpodzime)
- Add options for LVM cache specs to the 'logvol' command (vpodzime) (clumens)
- Set PYTHONPATH when running "make check". (clumens)
- Add --mkfsoptions to btrfs, logvol, partition, and raid commands. (clumens)
- Avoid traceback in module loading failure paths. (dlehman)
- Install the python3 .mo files to python3_sitelib (dshea)
- add extra test coverage for commands/btrfs.py (atodorov)
- additional test coverage for commands/device.py (atodorov)
- additional test coverage for parser/sections.py (atodorov)
- add test documentation (atodorov)
- cover corner case in commands/eula.py test (atodorov)

* Tue Jun 02 2015 Chris Lumens <clumens@redhat.com> - 2.8-1
- Merge pull request #16 from atodorov/commands_partition_updates (clumens)
- Merge pull request #15 from atodorov/fix_zanata_warning (clumens)
- cover some corner cases in the current partitioning test revealed by python-coverage (atodorov)
- Merge pull request #14 from atodorov/check_if_nosetests_is_installed (clumens)
- Remove unnecessary part_cb() and related __init__() methods (atodorov)
- fix: Warning, the url https://fedora.zanata.org/, contains / at end,please check your URL in zanata.xml (atodorov)
- if zanata and coverage are not installed make the error messages more platform independent (atodorov)
- check if nosetest is installed and abort with error if not (atodorov)
- Merge pull request #13 from vpodzime/master-ntp_pools (clumens)
- Adapt the Timezone class to support NTP pools (vpodzime)
- Update kickstart-docs.rst (jkonecny)
- RHEL7 now supports the reqpart command, too. (clumens)
- Use isinstance instead of type. (clumens)
- Add a missing space before --profile= on the logvol command. (clumens)
- Add some missing removedKeywords/removedAttrs setting. (clumens)

* Tue Apr 28 2015 Chris Lumens <clumens@redhat.com> - 2.7-1
- Ignore some pylint warnings in the tools/ directory. (clumens)
- Move most pylint disable pragmas onto the line they apply to. (clumens)
- Allow skipping the errors on unknown sections. (clumens)

* Tue Apr 21 2015 Chris Lumens <clumens@redhat.com> - 2.6-1
- Merge pull request #8 from bcl/master-kexec (clumens)
- Merge pull request #10 from bcl/master-pre-install (clumens)
- Switch to using nosetests. (clumens)
- Allow multiple partitions with the "swap" mountpoint. (clumens)
- Add %pre-install section to be used after mounting filesystems (bcl)
- Convert reboot to use _getArgsAsStr (bcl)
- Merge pull request #9 from bcl/master-rc-release (clumens)
- Add rc-release Makefile target (bcl)
- Add --kexec flag to reboot (bcl)

* Fri Apr 17 2015 Chris Lumens <clumens@redhat.com> - 2.5-1
- Add a new command to only make those partitions required by the platform. (clumens)
- btrfs levels should be handled the same way as RAID levels. (clumens)
- Include test cases for lower-cased and just numeric versions of RAID levels. (clumens)
- Two more docs fixes. (clumens)

* Tue Apr 14 2015 Chris Lumens <clumens@redhat.com> - 2.4-1
- Move docs to the correct file name. (clumens)
- Handle two-digit version numbers on this branch. (clumens)

* Tue Apr 14 2015 Chris Lumens <clumens@redhat.com> - 2.3-1
- Merge pull request #5 from vpodzime/master-python3 (clumens)
- RHEL7 now uses the F21 versions of commands, typically. (clumens)
- Handle a %include line that starts with whitespace in a section. (clumens)
- Treat "RAID" as uppercased at all times. (clumens)
- Add support for Fedora 23. (clumens)
- Merge pull request #6 from vpodzime/master-docs (clumens)
- Switch from transifex to zanata. (clumens)
- Let's have the docs in the repository (vpodzime)
- Prevent recursion in hasattr and __getattr__ (vpodzime)

* Tue Mar 24 2015 Chris Lumens <clumens@redhat.com> - 2.2-1
- And then BuildRequires pocketlint. (clumens)
- Fix the couple last pylint warnings. (clumens)
- Tell pylint to ignore a couple places where we catch all exceptions. (clumens)
- Don't use [] as a default argument to loadModules. (clumens)
- Define bytesPerInode in __init__ methods. (clumens)
- Don't pointlessly redefine the command attr in some tests. (clumens)
- tstList -> tests (clumens)
- lan -> len (clumens)
- Fix wildcard imports and other import-related pylint problems. (clumens)
- Remove some unused variables. (clumens)
- Fix string substitutions into translatable strings. (clumens)
- Start using pocketlint to run pylint. (clumens)

* Thu Feb 26 2015 Chris Lumens <clumens@redhat.com> - 2.1-1
- Both library packages need to require python-six of some variety (#1195715). (clumens)
- Fix the python-six requirement for python3-kickstart (#1195719). (clumens)

* Fri Feb 20 2015 Chris Lumens <clumens@redhat.com> - 2.0-1
- Make sure pykickstart requires some version of the library. (clumens)
- Split into python2 and python3 specific packages. (clumens)
- Look for translations in their new location. (clumens)
- Install .mo files into the python site-packages directory. (clumens)
- Merge pull request #3 from tradej/python3 (clumens)
- Fixed pylint warnings (tradej)
- Fixed executables in tools + related parts of pykickstart.parser. (tradej)
- Explicitly closing files. Python 3 tests work now. (tradej)
- Implemented rich comparison for parser.Group. (tradej)
- Error parsing in test.commands.logvol matches Python 3's optparse. (tradej)
- Keeping order of contents in the %packages section with OrderedSet (under MIT license). (tradej)
- Redefined _ in pykickstart.i18n, importing. (tradej)
- Fixed assertRaisesRegexp function in Python3. (tradej)
- Replaced string.strip(pkgs) with str(pkgs).strip(). (tradej)
- Adapted Makefile to allow running tests under Python 3. (tradej)
- Converted syntax to Python 3-compatible (rhbz#985310) (tradej)
- Fix a problem pylint caught with the last patch merge. (clumens)
- Make sure pykickstart/*/*py messages get included in pykickstart.pot. (clumens)
- Merge pull request #2 from tradej/urlgrabber (clumens)
- Replaced URLGrabber with requests (rhbz#1141245) (tradej)
- Remove --nobase as an option. (clumens)
- Add support to rhel6 for specifying thin pool profile (vpodzime)
- Add support to rhel6 for custom layouts using lvm thin provisioning. (dlehman)
