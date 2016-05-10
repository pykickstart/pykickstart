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

Requires: python3-kickstart

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

* Fri Jan 30 2015 Chris Lumens <clumens@redhat.com> - 1.99.66-1
- network: add support for bridge to F22 (#1075195) (rvykydal)
- Use %license in pykickstart.spec (bcl)

* Mon Dec 15 2014 Chris Lumens <clumens@redhat.com> - 1.99.65-1
- Add support for setting user account ssh key (bcl)
- Add = to the output for various network options (#1171926). (clumens)
- When ksflatten fails, return a failure code (#1162881). (clumens)

* Mon Nov 24 2014 Chris Lumens <clumens@redhat.com> - 1.99.64-1
- Get rid of an unused variable. (clumens)
- network: add support for bridge to RHEL7 (#1075195) (rvykydal)
- Add new RHEL7 logvol objects to master (vpodzime)
- Add new RHEL7 volgroup objects to master (vpodzime)
- RHEL7 supports the ostreesetup command. (clumens)

* Fri Oct 10 2014 Chris Lumens <clumens@redhat.com> - 1.99.63-1
- Move the test for --nombr option to the right class (vpodzime)
- Add the --nombr bootloader option in pykickstart (gczarcinski)

* Tue Oct 07 2014 Chris Lumens <clumens@redhat.com> - 1.99.62-1
- Allow recommended flag for non-prexisting logical volumes (#1149718) (amulhern)
- Apply a couple more 2to3 fixes, still avoiding the hard ones.(#985310). (clumens)
- Apply the obvious easy changes from 2to3 (#985310). (clumens)

* Fri Oct 03 2014 Chris Lumens <clumens@redhat.com> - 1.99.61-1
- Add support for specifying thin pool profile (vpodzime)
- Add missing import (mkolman)
- Add tests for --interfacename validation (mkolman)
- Validate network interface name when parsing the kickstart (#1081982) (mkolman)

* Wed Sep 24 2014 Chris Lumens <clumens@redhat.com> - 1.99.60-1
- Make --size and --percent mutually exclusive in logvol. (dlehman)
- Add support for F22. (clumens)

* Wed Sep 17 2014 Chris Lumens <clumens@redhat.com> - 1.99.59-1
- Some tests for --size and --percent (#1117908) (amulhern)
- Update tests where necessary with --size flag (#1117908) (amulhern)
- Supply regex values for assert_parse_error calls in logvol.py (#1117908) (amulhern)
- Check the regular expression when asserting a parse error (#1117908) (amulhern)
- Do not reference non-existant attribute (#1117908) (amulhern)
- Move some statically detectable kickstart errors out of anaconda (#1117908) (amulhern)
- Remove --disable-override from tx arguments. (clumens)
- Add the bootloader --disabled option for RHEL7 as well. (clumens)

* Tue Aug 12 2014 Chris Lumens <clumens@redhat.com> - 1.99.58-1
- Add --install flag to repo command (#1119867) (bcl)

* Wed Jul 02 2014 Chris Lumens <clumens@redhat.com> - 1.99.57-1
- Replace python-setuptools-devel BR with python-setuptools (toshio). (clumens)
- Add autopart --fstype support (#1112697) (bcl)
- Add some more tests to bump up the "make coverage" numbers. (clumens)

* Thu Jun 19 2014 Chris Lumens <clumens@redhat.com> - 1.99.56-1
- Add support for --disklabel to clearpart (#1078537) (bcl)
- Make print statements Python 3 compatible (mkolman)

* Fri May 16 2014 Chris Lumens <clumens@redhat.com> - 1.99.55-1
- Do not set any magic default PE size in pykickstart (vpodzime)
- ostreesetup: Fix noGpg attribute (walters)
- Fix bogus changelog in pykickstart.spec (sagarun)
- Stop shipping a ChangeLog file. (clumens)
- We can use descriptive pylint message names on the command line, too. (clumens)

* Tue Apr 22 2014 Chris Lumens <clumens@redhat.com> - 1.99.54-1
- Move ks tools from optparse to argparse (#1083913). (clumens)
- Use descriptive pylint messages instead of numbers. (clumens)
- Fix up some printing problems in some of the tools. (clumens)
- Add support for the --listversions option to ksverdiff too. (clumens)
- Run pylint on tools/, and fix up all the errors. (clumens)
- disable-msg -> disable for pylint. (clumens)

* Mon Mar 31 2014 Chris Lumens <clumens@redhat.com> - 1.99.53-1
- ostreesetup: New command (walters)
- Move commandMap and dataMap setting into the individual handler classes. (clumens)

* Fri Mar 21 2014 Chris Lumens <clumens@redhat.com> - 1.99.52-1
- Take care of all the unused argument warnings. (clumens)
- Take care of all the unused variable warnings. (clumens)
- Remove unused imports. (clumens)
- Don't do relative import any more, either. (clumens)
- Stop doing wildcard imports. (clumens)
- Add an option to disable even installing the core group. (clumens)

* Tue Mar 18 2014 Chris Lumens <clumens@redhat.com> - 1.99.51-1
- Use the correct indentation for the new network stuff. (clumens)
- Add network --interfacename option for vlans (#1061646) (rvykydal)

* Mon Mar 17 2014 Chris Lumens <clumens@redhat.com> - 1.99.50-1
- Add a new bootloader --disabled option (#1074522). (clumens)
- Add support for F21. (clumens)
- Fix an error on the printing side of handling environments. (clumens)
- Add support for fcoe --autovlan option (#1055779) (rvykydal)

* Wed Feb 05 2014 Chris Lumens <clumens@redhat.com> - 1.99.49-1
- Provide syntax for specifying environments (#1061296). (clumens)
- Use the correct LogVolData object (#1058520). (clumens)
- Don't do string comparisons in "make test" (#1057573). (clumens)

* Mon Nov 25 2013 Chris Lumens <clumens@redhat.com> - 1.99.48-1
- Specify a kickstart version when running package-related tests. (clumens)
- We need python-urlgrabber to do builds now. (clumens)

* Mon Nov 25 2013 Chris Lumens <clumens@redhat.com> - 1.99.47-1
- Add missing version bumps for RHEL7 command control map (#1032738) (mkolman)
- Run "make test" as part of the RPM build process (#1025226). (clumens)
- Include test cases in the source distribution. (clumens)
- With the previous patch, RAID test formatting needs to change. (clumens)
- Do not add a list of PVs or RAID members when writing out --useexisting (#1021274). (clumens)
- Raise an error if bootloader --boot-drive gets more than one argument. (clumens)

* Thu Nov 14 2013 Chris Lumens <clumens@redhat.com> - 1.99.46-1
- Add support for network team devices (#1003591) (rvykydal)
- Work on test coverage a little bit. (clumens)
- Don't use OrderedDict. (clumens)
- Add tests for tmpfs usage (mkolman)
- Add tmpfs support (#918621) (mkolman)

* Fri Nov 01 2013 Chris Lumens <clumens@redhat.com> - 1.99.45-1
- Set bootloader location constructor default value to "none" (#916529) (amulhern)

* Fri Oct 25 2013 Chris Lumens <clumens@redhat.com> - 1.99.44-1
- method getattr should default to handler.url (bcl)
  Related: rhbz#1016801

* Wed Oct 16 2013 Chris Lumens <clumens@redhat.com> - 1.99.43-1
- Use F20_Raid for RHEL7. (#997146) (dlehman)

* Tue Oct 08 2013 Chris Lumens <clumens@redhat.com> - 1.99.42-1
- Remove a triple-X message that is no longer needed (mkolman)
- Add --remove-service option for the firewall command (#1016008) (mkolman)

* Wed Sep 25 2013 Chris Lumens <clumens@redhat.com> - 1.99.41-1
- New 'eula' command (#1000409) (vpodzime)

* Tue Sep 24 2013 Chris Lumens <clumens@redhat.com> 1.99.40-2
- Only BuildRequire transifex on OSes that include it.

* Tue Sep 24 2013 Chris Lumens <clumens@redhat.com> - 1.99.40-1
- Don't error out if volgroup --useexisting is given with no members. (clumens)

* Tue Sep 10 2013 Chris Lumens <clumens@redhat.com> - 1.99.39-1
- Call the right attribute method (#1004889) (bcl)
- Reset method seen attrs when switching method (#1004889) (bcl)

* Tue Sep 03 2013 Brian C. Lane <bcl@redhat.com> - 1.99.38-1
- Return None for attributes if no method has been set (#1001081) (dshea)
- Fix up a couple pylint errors in the tools. (clumens)

* Wed Aug 21 2013 Chris Lumens <clumens@redhat.com> - 1.99.37-1
- Correct exception raising style. (clumens)
- Fix up how we call pylint for 1.0.0. (clumens)
- Set method.method when attempted. (dshea)

* Mon Aug 19 2013 Chris Lumens <clumens@redhat.com> - 1.99.36-1
- When method.method is set, also set the right seen attribute (#994553). (clumens)
- Add tests for incorrect command usage detection (mkolman)
- Add class for independent multi-line command sequence tests (mkolman)
- Raise an error if autopart is combined with partitioning commands (#886010) (mkolman)

* Mon Jul 29 2013 Chris Lumens <clumens@redhat.com> - 1.99.35-1
- Add aliases for all the old method classes (#986069). (clumens)
- Check syntax version before issuing a deprecation warning (#972098). (clumens)

* Mon Jul 15 2013 Chris Lumens <clumens@redhat.com> - 1.99.34-1
- Always create self.handler on-demand in the test cases. (clumens)
- Also set the seen attribute when __call__ is used. (clumens)
- Mark the upgrade command as deprecated. (clumens)
- Add the method test case back in. (clumens)
- Set the seen attribute when parsing in test cases, too. (clumens)
- Add a proxy method command object. (clumens)
- Add an interactive kickstart shell command, ksshell. (clumens)
- Fix string substitution errors in translatable text. (clumens)
- Break the method command out into individual commands. (clumens)

* Tue Jul 09 2013 Chris Lumens <clumens@redhat.com> - 1.99.33-1
- Add support for lvm thin provisioning. (dlehman)
- Add support for F20. (clumens)
- Add a new test for the group command. (clumens)
- In the test cases, error on all non-deprecation warnings. (clumens)
- Remove unused imports from the test suite. (clumens)

* Fri Jun 14 2013 Chris Lumens <clumens@redhat.com> - 1.99.32-1
- transifex.net is now transifex.com (bcl)
- Update raid --device to be an array name specifier. (dlehman)
- Add more tests for the realm command (mkolman)
- RHEL7 is now more or less based on F19, at least for kickstart. (clumens)
- realm: Fix --no-password option (stefw)
- Add man pages for all programs (#948440). (clumens)

* Wed May 15 2013 Chris Lumens <clumens@redhat.com> - 1.99.31-1
- Fix F18/F19 cdrom methods (bcl)

* Thu May 09 2013 Chris Lumens <clumens@redhat.com> - 1.99.30-1
- Add support for the realm command (mkolman)
- Add liveimg install method (bcl)

* Thu May 09 2013 Chris Lumens <clumens@redhat.com> - 1.99.29-1
- add --extlinux option (mattdm)

* Tue Apr 23 2013 Chris Lumens <clumens@redhat.com> - 1.99.28-1
- Add network --ipv6gateway option (#905226) (rvykydal)
- Add lang --addsupport option (#912364) (rvykydal)

* Wed Apr 10 2013 Chris Lumens <clumens@redhat.com> - 1.99.27-1
- A new user's group should default to None, not 0 (#929204). (clumens)

* Fri Mar 22 2013 Chris Lumens <clumens@redhat.com> - 1.99.26-1
- parser.py: Allow shlex to strip lines (fedora.dm0)
- Fix a bug in logvol duplicate reporting (#924579, mhuth). (clumens)
- Add gid attribute to User command and associated data structure (msivak)
- Make sure tests can run and report import errors (bcl)
- Add network --vlanid option to Fedora. (rvykydal)

* Mon Mar 04 2013 Chris Lumens <clumens@redhat.com> - 1.99.25-1
- pylint appears to have gotten pickier. (clumens)
- Fix typo in --wpakey string representation method (rvykydal)
- Also add the F19 handler file. (clumens)
- Don't strip the newline from reboot or shutdown commands (#915013). (clumens)
- Add bonding support to RHEL 7 (rvykydal)
- Add bonding support to F19 (rvykydal)
- Add support for F19 (rvykydal)

* Wed Feb 13 2013 Chris Lumens <clumens@redhat.com> - 1.99.24-1
- Add a seen attribute to commands, sections, and the packages object. (clumens)

* Mon Jan 14 2013 Chris Lumens <clumens@redhat.com> - 1.99.23-1
- Don't print any of the autopart command if autopart is disabled (#888841). (clumens)
- Call sys.exit instead of os._exit (#891419, gconradi AT factset.com). (clumens)
- Beware of possible unicode strings (#876293) (vpodzime)
- Remove the lang.apply method (#882186). (clumens)
- Add 'make coverage' command to the make file (stefw)

* Tue Nov 20 2012 Chris Lumens <clumens@redhat.com> - 1.99.22-1
- Add support for url --mirrorlist, needed by anaconda (#868558). (clumens)
- Only write out a logging line if one was provided (#873242). (clumens)
- If no timezone was provided, do not write out an empty timezone command. (clumens)

* Wed Oct 24 2012 Chris Lumens <clumens@redhat.com> - 1.99.21-1
- Add support for layout switching options (vpodzime)

* Mon Oct 15 2012 Chris Lumens <clumens@redhat.com> - 1.99.20-1
- Disable pylint warnings related to the previous patch. (clumens)
- Revert "Fix superclass constructor call in F18_Keyboard." (clumens)
- Fix superclass constructor call in F18_Keyboard. (dlehman)
- Add cipher option for encrypting block devices. (dlehman)
- Change keyboard command to accept VConsole keymap and X layouts (vpodzime)
- add unsupported_hardware command (#824963) (bcl)

* Fri Sep 14 2012 Chris Lumens <clumens@redhat.com> - 1.99.19-1
- bonding support: add network --bondslaves --bondopts options (rvykydal)
- vlan support: add network --vlanid option. (rvykydal)

* Thu Sep 06 2012 Chris Lumens <clumens@redhat.com> - 1.99.18-1
- Fix the multilib package test case. (clumens)
- Add support for --multilib option to %packages. (dlehman)
- Mark --nobase as deprecated. (notting)

* Tue Aug 28 2012 Chris Lumens <clumens@redhat.com> - 1.99.17-1
- Add ksdata.network.hostname (readonly) property (rvykydal)

* Wed Aug 22 2012 Chris Lumens <clumens@redhat.com> - 1.99.16-1
- Add swap --hibernation to logvol command (vpodzime)

* Thu Aug 09 2012 Chris Lumens <clumens@redhat.com> - 1.99.15-1
- No argument needs to be given to rootpw if you're just locking the account. (clumens)

* Thu Jul 26 2012 Chris Lumens <clumens@redhat.com> - 1.99.14-1
- add reboot test (bcl)
- add correct halt command handling (bcl)
- return parsed object from assert_parse (bcl)
- The monitor command has been deprecated since F10.  Get rid of it. (clumens)
- Add --hibernation option for swap size specification (vpodzime)
- Add leavebootorder test (hamzy)

* Tue Jun 19 2012 Chris Lumens <clumens@redhat.com> - 1.99.13-1
- Support bootloader --leavebootorder for F18 and RHEL7 (#824801) (pjones)
- Allow %include in %pre and %post (#827269) (bcl)

* Mon Jun 18 2012 Chris Lumens <clumens@redhat.com> - 1.99.12-1
- Add --nontp option and a way to specify NTP servers to the timezone command (vpodzime)
- fix TypeError in network.py with ipv6 static addresses (wwoods)
- Layouts may include spaces, so put them in quotes (vpodzime)

* Mon May 07 2012 Chris Lumens <clumens@redhat.com> - 1.99.11-1
- pylint doesn't like .setter syntax at all. (clumens)
- Modify keyboard command to handle multiple layouts (vpodzime)
- Add support for F18. (vpodzime)
- Fix traceback if modules cannot be loaded when running tests (vpodzime)

* Mon Apr 02 2012 Chris Lumens <clumens@redhat.com> - 1.99.10-1
- Add resize option to partition and logvol commands. (dlehman)
- Add --list= mode to clearpart for explicit list of partitions to remove. (dlehman)

* Thu Mar 22 2012 Chris Lumens <clumens@redhat.com> - 1.99.9-1
- Add __ne__ methods to every object with an __eq__ method. (clumens)
- Use the older exception syntax for python 2.4 compatibility. (clumens)
- Add an __eq__ method to the method command. (clumens)

* Wed Mar 14 2012 Chris Lumens <clumens@redhat.com> - 1.99.8-1
- Add support for RHEL7 (#802369).
- Add a method to set a command back to its initial blank state.
- btrfs likes its raid levels in lower case. (#799154) (dlehman)
- iscsi: add support for interface binding to F17 (rvykydal)
- iscsi: add support for interface binding (#500273) (rvykydal)

* Wed Jan 11 2012 Chris Lumens <clumens@redhat.com> - 1.99.7-1
- Add --type option to autopart command. (dlehman)
- Add btrfs command. (dlehman)

* Tue Nov 15 2011 Chris Lumens <clumens@redhat.com> - 1.99.6-1
- Add --boot-drive option to bootloader command to pick boot drive. (dlehman)
- Add support for F17. (clumens)
- The guts of a script could include a line starting with a % (#746928). (clumens)

* Wed Oct 19 2011 Chris Lumens <clumens@redhat.com> - 1.99.5-1
- Don't error out if raid --useexisting is given with no members (#741728). (clumens)
- When %end is missing, include the unterminated section in the error message. (clumens)

* Wed Sep 14 2011 Chris Lumens <clumens@redhat.com> - 1.99.4-1
- --reserved-space and --reserved-percent should be checked on a callback. (clumens)
- Add a volgroup unit test, and fix a bug it uncovered. (clumens)
- Add support for reserved space in volume group. (dlehman)
- Allow a %include to come in the middle of a section (#733455). (clumens)
- Add a test case for %include inside %packages. (clumens)

* Mon Aug 22 2011 Chris Lumens <clumens@redhat.com> - 1.99.3-1
- Ignore reimport warnings. (clumens)
- Add support for 'autopart --nolvm' (jlaska)
- autopart - Inherit error checking from base class (jlaska)
- Let's just use url.size instead.  That's defined for both FTP and HTTP. (clumens)
- It's url.hdr now, not url.info. (clumens)
- Support end-of-line comments in the %packages section (#728563). (clumens)

* Mon Jun 27 2011 Chris Lumens <clumens@redhat.com> - 1.99.2-1
- Don't do "make po-pull" during installation. (clumens)

* Mon Jun 27 2011 Chris Lumens <clumens@redhat.com> - 1.99.1-1
- Fix a couple Makefile typos. (clumens)
- typo fix (vpodzime)
- option for wpa wifi connection specification added (vpodzime)
- Update Makefiles to work with new translation system. (clumens)
- BuildRequires transifex-client. (clumens)
- Ignore po/*.po files. (clumens)
- Remove translation files. (clumens)
- Add transifex-client configuration file. (clumens)
- Fix po files so "msgfmt -c" passes and they can be uploaded to transifex. (clumens)

* Tue Jun 07 2011 Chris Lumens <clumens@redhat.com> 1.99.0-1
- Add a way to tell how often a section has been handled. (clumens)
- Add a NullSection that just ignores any section provided. (clumens)
- Add test cases for the parser itself. (clumens)
- Allow for defining your own kickstart %sections. (clumens)
- The docs need to be fetched from an HTTPS location now. (clumens)
- Write out --onboot=off if it's False. (clumens)
