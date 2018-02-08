Name:      pykickstart
Version:   3.11
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
BuildRequires: python2-coverage
BuildRequires: python2-devel
BuildRequires: python2-nose
BuildRequires: python2-ordered-set
BuildRequires: python2-setuptools
BuildRequires: python2-requests

BuildRequires: python3-coverage
BuildRequires: python3-devel
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
%package -n python2-kickstart
%{?python_provide:%python_provide python2-kickstart}
%{?python_provide:%python_provide python2-pykickstart}
Summary:  Python 2 library for manipulating kickstart files.
Requires: python2-six
Requires: python2-requests
Requires: python2-ordered-set

%description -n python2-kickstart
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

%files -n python2-kickstart
%defattr(-,root,root,-)
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.txt
%{python2_sitelib}/pykickstart*egg*
%{python2_sitelib}/pykickstart/
%{python2_sitelib}/pykickstart/commands/
%{python2_sitelib}/pykickstart/handlers/
%{python2_sitelib}/pykickstart/locale/

%files -n python3-kickstart
%defattr(-,root,root,-)
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.txt
%{python3_sitelib}/pykickstart*egg*
%{python3_sitelib}/pykickstart/
%{python3_sitelib}/pykickstart/commands/
%{python3_sitelib}/pykickstart/handlers/
%{python3_sitelib}/pykickstart/locale/

%changelog
* Thu Feb 08 2018 Chris Lumens <clumens@redhat.com> - 3.11-1
- Logging level should be always set (#1543194) (vponcova)
- Copy txt files from _build folder on make local call (jkonecny)

* Thu Jan 25 2018 Chris Lumens <clumens@redhat.com> - 3.10-1
- Update Python 2 dependency declarations to new packaging standards

* Thu Jan 04 2018 Chris Lumens <clumens@redhat.com> - 3.9-1
- Fix directory ownership (lbalhar, #202). (clumens)
- firewall: add --use-system-defaults arg to command (#1526486) (dusty)
- Add lineno as an attribute on KickstartParseError. (clumens)
- Don't modify the original command and data mappings. (vponcova)

* Thu Nov 30 2017 Chris Lumens <clumens@redhat.com> - 3.8-1
- Add support for hmc command in Fedora (vponcova)
- Commands for specifying base repo are mentioned in docs (jkonecny)
- Add list of installation methods to the method doc (jkonecny)
- Fix pylint warnings in the mount command (vponcova)
- Fix test for the mount command (vponcova)
- Add clearpart --cdl option. (sbueno+anaconda)
- Add Fedora 28 support (vponcova)
- Add a new 'mount' command (vpodzime)
- Pylint fixes (vponcova)
- Add command hmc to support SE/HMC file access in RHEL7 (vponcova)
- Add timeout and retries options to %packages section in RHEL7 (vponcova)
- Call the _ method from i18n.py (jkonecny)
- Backport spec file changes from downstream (jkonecny)
- network: add network --bindto option (Fedora) (#1483981) (rvykydal)
- network: add network --bindto option (RHEL) (#1483981) (rvykydal)
- Add url --metalink support (#1464843) (rvykydal)
- Update doc of repo --mirrorlist and --baseurl with --metalink (#1464843) (rvykydal)
- Add repo --metalink support (#1464843) (rvykydal)
- Add Fedora 27 support. (rvykydal)
- Update Repo command tests. (rvykydal)
- Split the import of commands to multiple lines (vponcova)
- Move the installclass command to the %anaconda section (vponcova)
- Mention that repo name must not contain spaces (brunovern.a)

* Fri Sep 15 2017 Jiri Konecny <jkonecny@redhat.com> - 3.7-2
- Backport of the Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> from downstream spec
  Python 2 binary package renamed to python2-pykickstart
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Tue Jul 18 2017 Chris Lumens <clumens@redhat.com> - 3.7-1
- Add a Makefile target for uploading to pypi (#162). (clumens)
- Remove some old, unneeded stuff from the Makefile. (clumens)
- Add tests for method command (vponcova)
- Rewrite the method command. (vponcova)
- More documentation for bypassing the bootloader (#159) (amtlib-dot-dll)
- Output any sections registered with NullSection (#154). (clumens)
- Add new installclass command in master (vponcova)

* Tue May 16 2017 Chris Lumens <clumens@redhat.com> - 3.6-1
- Ignore errors from coverage tests (#138) (jkonecny)
- Fix bumpver target when "changelog" is in the spec file more than once. (clumens)
- Ignore a couple false positives coming from the re module. (clumens)
- Fix snapshot command (jkonecny)
- Generate documentation in ci tests (jkonecny)
- Fix snapshot documentation (jkonecny)
- Add tests for a new snapshot command (#1113207) (jkonecny)
- Add support of --when param to snapshot command (#1113207) (jkonecny)
- Add new snapshot KS command (#1113207) (jkonecny)
- Add realm command test (jkonecny)
- Add --nohome, --noboot and --noswap options to autopart command. (vponcova)
- Add --nohome option to autopart command in RHEL7. (vponcova)
- Add support for --chunksize option to RHEL7. (vponcova)
- Add link to online docs to the README (#137) (martin.kolman)
- Add --hibernation to the list of logvol size options (#1408666). (clumens)
- Handle KickstartVersionError in ksflatten (#1412249). (clumens)
- Fix the glob used to reference comps files in docs (#135). (clumens)
- docs: Note under %include that most sections don't do merging (#134) (walters)
- Fix handling # in passwords. (clumens)
- Pass comments=True to shlex.split calls in the test functions. (clumens)
- Don't forget to add tests to the NOSEARGS. (clumens)

* Wed Nov 30 2016 Chris Lumens <clumens@redhat.com> - 3.5-1
- Include README.rst in the MANIFEST.in again. (clumens)
- Disable running "make coverage" or "make check" with python2. (clumens)
- rootpw: document that password isn't required with --lock (atodorov)
- Run the docs makefile during RTD build (mkolman)
- Remove the type annotations (dshea)
- Remove mypy checks. (dshea)
- Fix python2 compatibility when printing to stderr (jkonecny)
- Add a type stub for the new F26 support. (clumens)
- Fix and add tests for F26 and new displaymode (jkonecny)
- Add non-interactive option to graphical and text modes (jkonecny)
- Add Fedora 26 support (jkonecny)
- fix markup a bit (add ) (gitDeveloper)
- Print errors to stderr when errors aren't fatal (jkonecny)
- Add build insturctions for the docs (martin.kolman)
- More test coverage for base.py (atodorov)
- Warn about using removed keywords in kickstart commands (atodorov)
- More test coverage for network.py (atodorov)
- Refactoring and more tests for partition (atodorov)
- Add documentation for mouse (atodorov)
- Add documentation for langsupport (atodorov)
- Refactor lang and add more tests (atodorov)
- Refactor iscsiname and more tests (atodorov)
- Add short description for interactive command (atodorov)
- Nuke all the pykickstart-2.x %changelog history. (clumens)
- Update network command documentation also in option help strings. (rvykydal)
- Retroactively fix checks for reqpart and autopart (atodorov)
- More tests for zfcp (atodorov)
- More tests for volgroup (atodorov)
- More tests for url (atodorov)
- Add help documentation and more tests for upgrade.py (atodorov)
- More tests and refactoring for timezone.py, fixes #112 (atodorov)
- More test coverage for sshpw (atodorov)
- Refactor and add more tests for sshkey (atodorov)
- Remove duplicate assert (atodorov)
- Add more tests for rootpw (atodorov)
- Refactoring and additional test coverage for raid command (atodorov)
- More tests for FC3_NFS (atodorov)
- Refactor logging.py and add tests (atodorov)
- Additional tests for FC3_HardDrive (atodorov)
- More tests for F12_GroupData (atodorov)
- Additional test coverage for commands/firewall.py (atodorov)
- Add missing documentation for device command (atodorov)
- Explain ks= vs. inst.ks= in the documentation (#109). (clumens)
- Include the built documentation in the package tarball. (clumens)
- Update the documentation when bumpver is run. (clumens)
- Add commands*.rst and sections.rst to the repo. (clumens)
- Another path change in docs/conf.py for readthedocs. (clumens)
- Fix a couple pylint errors. (clumens)
- Disable assertion in HelpAndDescription_TestCase (atodorov)
- Refactor HelpAndDescription_TestCase to properly patch KSOptionParser (atodorov)
- Add docs to the path in docs/conf.py too. (clumens)
- Set the version in docs/conf.py with "make bumpver". (clumens)
- Set PYTHONPATH when running sphinx-build. (clumens)
- The build now requires sphinx to build documentation. (clumens)
- Test if prog, help or description are empty (atodorov)
- Clean up TODO comments (atodorov)
- Add Sphinx extension which parses the 'versionremoved' directive (atodorov)
- Automatically build kickstart command & sections documentation (atodorov)
- Add a backward compatibility class for the lilo command (atodorov)
- Split upgrade and install commands and update handlers after F20 (atodorov)
- Don't skip DeprecatedCommands when testing handler mappings (atodorov)
- network refactoring and more tests (atodorov)
- iscsiname - small refactoring (atodorov)
- firewall refactoring and more tests (atodorov)
- clearpart: refactoring and more tests (atodorov)
- More tests for multipath (atodorov)
- user: more tests and refactoring (atodorov)
- updates refactoring (atodorov)
- timezone refactoring and more tests (atodorov)
- fcoe more tests (atodorov)
- sshpw: new tests and refactoring (atodorov)
- services refactoring to reduce mutations (atodorov)
- rootpw: refactoring and new tests (atodorov)
- reboot: add two more tests (atodorov)
- monitor: new test (atodorov)
- method: refactoring and a few more tests (atodorov)
- logvol: refactoring and more tests (atodorov)
- iscsi: refactoring and update tests (atodorov)
- ignoredisk: refactor to kill all mutants (atodorov)
- realm: fix missing writePriority and add more test coverage (atodorov)
- driverdisk: remove writePriority from _DriverDiskData constructor and other refactoring (atodorov)
- btrfs: more mutation tests & refactoring (atodorov)
- dmraid: more mutation and test coverage (atodorov)
- volgroup: refactoring and more tests (atodorov)
- xconfig: more tests to kill remaining mutations (atodorov)
- displaymode: extra mutation and test coverage (atodorov)
- zfcp: more mutation tests and bump code coverage (atodorov)
- keyboard: refactoring to reduce mutations (atodorov)
- liveimg: more tests (atodorov)
- multipath:  to  refactoring (atodorov)
- ostreesetup: refactoring  into  and more tests (atodorov)
- zerombr: more tests (atodorov)
- vnc: new test (atodorov)
- cdrom: Remove source of mutations (atodorov)
- eula: minor fixes and more tests (atodorov)
- mouse: add more tests to kill some mutants (atodorov)
- user: fix for deleting of != '' change (atodorov)
- Delete str != "" comparisons to remove 8*110 possible mutations (atodorov)
- rescue: new test to kill remaining mutants (atodorov)
- reqpart: new test to kill remaining mutants (atodorov)
- interactive, lilocheck, mediacheck: kill remaining mutants (atodorov)
- unsupported_hardware: new test to kill remaining mutants (atodorov)
- skipx: new test to kill remaining mutants (atodorov)
- autostep: new test to kill remaining mutants (atodorov)
- Remove unnecessary nargs=1 parameter (atodorov)
- Pass writePriority to KickstartCommand.__init__ (atodorov)
- Add test for writePriority (atodorov)
- Refactor mock.patch so it works with Cosmic-Ray (atodorov)

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
