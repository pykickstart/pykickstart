%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Summary:  A python library for manipulating kickstart files
Name: pykickstart
Url: http://fedoraproject.org/wiki/pykickstart
Version: 1.99.66.16
Release: 1%{?dist}
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0: %{name}-%{version}.tar.gz

License: GPLv2
Group: System Environment/Libraries
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel, gettext, python-setuptools
BuildRequires: python-urlgrabber
Requires: python, python-urlgrabber

%description
The pykickstart package is a python library for manipulating kickstart
files.

%prep
%setup -q

%build
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
%find_lang %{name}

%clean
rm -rf %{buildroot}

%check
make test

%files -f %{name}.lang
%defattr(-,root,root,-)
%license COPYING
%doc README docs/programmers-guide
%doc docs/kickstart-docs.rst
%{python_sitelib}/*
%{_bindir}/ksvalidator
%{_bindir}/ksflatten
%{_bindir}/ksverdiff
%{_bindir}/ksshell
%{_mandir}/man1/*

%changelog
* Tue Dec 12 2017 Chris Lumens <clumens@redhat.com> - 1.99.66.16-1
- Pull in updated translations.
  Resolves: rhbz#1481222

* Fri Nov 10 2017 Chris Lumens <clumens@redhat.com> - 1.99.66.15-1
- Fix import in the mount command (vponcova)
  Related: rhbz#1450922
- Add a new 'mount' command (vpodzime)
  Related: rhbz#1450922

* Mon Oct 16 2017 Chris Lumens <clumens@redhat.com> - 1.99.66.14-1
- Add timeout and retries options to %packages section (#1482912) (vponcova)
- Add command hmc to support SE/HMC file access (#1498829) (vponcova)
- Add tests for method command (vponcova)
- Rewrite the method command. (vponcova)

* Tue Sep 05 2017 Chris Lumens <clumens@redhat.com> - 1.99.66.13-1
- network: add network --bindto option (rvykydal)
  Resolves: rhbz#1483981

* Wed Apr 05 2017 Chris Lumens <clumens@redhat.com> - 1.99.66.12-1
- Add documentation for the snapshot feature (jkonecny)
  Related: rhbz#1113207
- Add tests for a new snapshot command (jkonecny)
  Related: rhbz#1113207
- Add support of --when param to snapshot command (jkonecny)
  Related: rhbz#1113207
- Add new snapshot KS command (jkonecny)
  Related: rhbz#1113207

* Wed Mar 01 2017 Chris Lumens <clumens@redhat.com> - 1.99.66.11-1
- Document %%traceback and %%onerror. (clumens)
  Related: rhbz#1412538
- Add an %%onerror script section. (clumens)
  Related: rhbz#1412538
- Add more test coverage around Group and Script objects. (clumens)
  Related: rhbz#1412538
- Add --nohome option to autopart command. (#141) (vponcova)
  Related: rhbz#663099
- Add --chunksize option to raid command. (#140) (vponcova)
  Related: rhbz#1332316

* Thu Aug 18 2016 Chris Lumens <clumens@redhat.com> - 1.99.66.10-1
- Support file URLs for ostree. (clumens)
  Resolves: rhbz#1367933

* Fri Jun 17 2016 Chris Lumens <clumens@redhat.com> - 1.99.66.9-1
- Support timezone command usage without timezone specification (mkolman)
  Related: rhbz#1312135

* Thu Jun 02 2016 Chris Lumens <clumens@redhat.com> - 1.99.66.8-1
- Add --no-activate option to network command (#1277975) (rvykydal)

* Mon Feb 29 2016 Chris Lumens <clumens@redhat.com> - 1.99.66.7-1
- Add sshkey command to RHEL7 (#1311755) (bcl)
- Add --sshkey to sshpw command (#1240410) (bcl)
- Add %%pre-install section to be used after mounting filesystems (bcl)
- There is no F7_Key class - use RHEL5_Key instead. (clumens)
- ostree repos can only be HTTP or HTTPS. (clumens)
- Fix class inheritance in RHEL6_VolGroup (ccoyle)

* Tue Sep 22 2015 Chris Lumens <clumens@redhat.com> - 1.99.66.6-1
- Update the RHEL7 version constant. (clumens)

* Tue Jul 07 2015 Chris Lumens <clumens@redhat.com> - 1.99.66.5-1
- Reorder the expected output in the clearpart CDL test. (clumens)
- Fix whitespace error in clearpart --cdl test (#1232849) (sbueno+anaconda)
- Add clearpart --cdl option. (#1232849) (sbueno+anaconda)
- Avoid polluting generated kickstarts by unexpected reqpart commands (#1164660) (mkolman)
- Don't allow using --fsprofile and --mkfsopts at the same time. (clumens)

* Wed Jun 24 2015 Chris Lumens <clumens@redhat.com> - 1.99.66.4-1
- transifex-client is no longer needed to build. (clumens)
- Add kickstart docs to the source tree (clumens)
- Add options for LVM cache specs to the 'logvol' command (vpodzime)

* Thu Jun 18 2015 Chris Lumens <clumens@redhat.com> - 1.99.66.3-1
- Add --mkfsoptions to btrfs, logvol, partition, and raid commands. (clumens)
- Merge pull request #25 from bcl/rhel7-1207747 (clumens)
- Allow skipping the errors on unknown sections. (#1180255) (sbueno+anaconda)
- Add --kexec flag to reboot (#1207747) (bcl)

* Tue Jun 02 2015 Chris Lumens <clumens@redhat.com> - 1.99.66.2-1
- Add rc-release Makefile target (bcl)
- Add a new command to only make those partitions required by the platform. (clumens)

* Tue Apr 28 2015 Chris Lumens <clumens@redhat.com> - 1.99.66.1-1
- Rebuild for RHEL7.

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

* Fri Mar 25 2011 Chris Lumens <clumens@redhat.com> - 1.83-1
- Add kickstart network --nodefroute option (#668417) (rvykydal)
- Add support for network --bootproto ibft option (#668417) (rvykydal)
- Add network --activate option (#668417) (rvykydal)
- Add support for F16. (clumens)

* Fri Feb 18 2011 Chris Lumens <clumens@redhat.com> - 1.82-1
- Add support for "logvol --label=" (#677571). (clumens)

* Wed Jan 19 2011 Chris Lumens <clumens@redhat.com> - 1.81-1
- Add support for "raid --label=" (#670643). (clumens)
- --baseurl/--mirrorlist are no longer required for the repo command. (clumens)
- Make use of the "interactive" command an error. (clumens)

* Fri Dec 10 2010 Chris Lumens <clumens@redhat.com> - 1.80-1
- Remove preceededInclude= support (#639372). (clumens)
- support noverifyssl on the rhel6-branch (method, repo) (#660340). (akozumpl)
- l10n: Added Low German translation (ncfiedler)

* Mon Nov 08 2010 Chris Lumens <clumens@redhat.com> 1.79-1
- Move from pychecker to pylint, since the latter actually works.
- Lots of minor corrections for pylint.
- Add bootloader --iscrypted (#554870).
- Add support for F15.

* Fri Sep 10 2010 Chris Lumens <clumens@redhat.com> - 1.78-1
- Raise KickstartError instead of IOError (#618002). (clumens)
- It's --biospart, not --biosdisk (#620855). (clumens)
- Translation updates.

* Tue Jul 20 2010 Chris Lumens <clumens@redhat.com> - 1.77-1
- Send the key command down the memory hole. (clumens)
- Deprecate interactive kickstart mode. (clumens)

* Thu Jul 08 2010 Chris Lumens <clumens@redhat.com> - 1.76-1
- method: new parameter '--noverifyssl' after --url. (akozumpl)
- repo: new parameter '--noverifyssl'. (akozumpl)

* Tue Jun 22 2010 Chris Lumens <clumens@redhat.com> - 1.75-1
- Update translation files. (clumens)
- Remove everything from pykickstart that's been deprecated forever. (clumens)
- Using the knowledge of what command supports what option, condense test cases. (clumens)
- Add a method to list all supported options for a command being tested. (clumens)
- Add support for F14. (clumens)
- The %end at the end of a section is now required. (clumens)

* Thu Jun 10 2010 Chris Lumens <clumens@redhat.com> - 1.74-1
- If an option is deprecated, do not care if it takes a value (#602303). (clumens)
- Don't compare the dest ("telnet") with the option string ("--telnet"). (clumens)
- The --connect= parameter wasn't really deprecated in FC6. (clumens)

* Tue Jun 01 2010 Chris Lumens <clumens@redhat.com> - 1.73-1
- Allow "ignoredisk" to explicitly specify interactive usage (#596804) (pjones)

* Fri Apr 23 2010 Chris Lumens <clumens@redhat.com> - 1.72-1
- Return non-zero on error from ksvalidator (#585284). (clumens)

* Wed Apr 14 2010 Chris Lumens <clumens@redhat.com> - 1.71-1
- Don't overwrite the excluded group list after every %packages line (#577334). (clumens)
- Add a bunch of test cases for the packages section. (clumens)

* Wed Mar 31 2010 Chris Lumens <clumens@redhat.com> - 1.70-1
- Add support for RAID4 (#578514). (clumens)
- Escape percent signs in the changelog. (clumens)

* Wed Mar 10 2010 Chris Lumens <clumens@redhat.com> - 1.69-1
- Add driverdisk --biospart= (#570437). (clumens)
- Fix IOError catching in ksflatten (jgregusk, #558650).

* Thu Jan 14 2010 Chris Lumens <clumens@redhat.com> - 1.68-1
- Support removing groups that were included by a glob (#554717). (clumens)
- Make sure that everything in version.versionMap has a handler. (clumens)
- Add support for RHEL6 (#552230). (clumens)
- Don't consider RHEL versions as developmental even if they're latest. (clumens)
- Add lineno to BaseData and derived classes (version 2) (hdegoede)
- Give the non mandatory iscsi --port argument a sane default (hdegoede)
- Change python_sitelib macro to use %%global for new rpm (hdegoede)
- Fix typo in iscsi parsing error message (hdegoede)

* Thu Dec 03 2009 Chris Lumens <clumens@redhat.com> - 1.67-1
- Don't use action="append_const" in firewall.py.
- Make "make archive" depend on test and check passing again.
- versionToString now works in all cases we test for.
- Fix the few pychecker errors outstanding in options.py.
- Fix make docs to make docs dir before trying to download files there (hdegoede)

* Wed Nov 25 2009 Hans de Goede <hdgoede@redhat.com> - 1.66-1
- Add --dcb option to fcoe command (#513011)
- Remove rhpl from tests
- Port bootloader --hvargs option added in rhel5
- Ignore comments when looking for %%ksappend lines (#525676)
- Use python 2.x exception syntax

* Thu Nov 12 2009 Chris Lumens <clumens@redhat.com> - 1.65-1
- Add additional arguments to BaseHandler.__init__ for better map control.
- Return the KickstartCommand/KickstartData object from dispatcher.
- Add an "sshpw" command for changing the passwords in anaconda's env.
- Add --proxy support to the url and repo commands.
- Add support for F13.  Is it really that time already?

* Wed Sep 30 2009 Chris Lumens <clumens@redhat.com> - 1.64-1
- Update the zfcp command for F12 (#526360).
- Move "make" to %%build (#524215).

* Wed Sep 16 2009 Chris Lumens <clumens@redhat.com> - 1.63-1
- Add encryption key escrow support (mitr, #508963).
- Fix the repo test cases to expect quotes around the repo's name.

* Thu Sep 10 2009 Chris Lumens <clumens@redhat.com> - 1.62-1
- Support translated help text in optparse (#479519).
- If the input kickstart file cannot be read, raise IOError (#519477).

* Thu Aug 27 2009 Chris Lumens <clumens@redhat.com> - 1.61-1
- Include the error messages from URLGrabError in the exception (#518443).

* Tue Aug 11 2009 Chris Lumens <clumens@redhat.com> - 1.60-1
- Put quotes around the repo's name (Marc.Herbert@gmail.com).
- Make duplicate entries warnings, not errors (#516338).

* Tue Jul 28 2009 Chris Lumens <clumens@redhat.com> - 1.59-1
- Handle a few more places where a urlgrabber error could happen (#512951).
- Error out if the same partition/repo/network is defined twice (#512956).
- Call parent class tests first. (jlaska)
- Add KSOptionParser to FC3 upgrade command. (jlaska)
- Correct missing return stmt in _getArgsAsStr() (jlaska)

* Fri Jul 17 2009 Chris Lumens <clumens@redhat.com> - 1.58-1
- Adjust writePriority to fix lvm-on-raid0 test cases (jlaska).
- Add F12 to the version number tests. (clumens)
- F12_User test case. (dcantrell)
- Add --gecos argument to the 'user' command (dcantrell)
- Convert user.py to use _getArgsAsStr() (dcantrell)

* Fri Jul 10 2009 Chris Lumens <clumens@redhat.com> - 1.57-1
- Another patch to make the bootloader test work (jlaska).

* Thu Jul 09 2009 Chris Lumens <clumens@redhat.com> - 1.56-1
- Make sure to import the gettext stuff in fcoe. (clumens)
- Correctly deprecate bootloader --lba32 (jlaska).
- pykickstart: fix zfcp command writepriority (hdegoede)
- pykickstart: Add fcoe command (take 2) (hdegoede)
- Add a test case for RAID (jlaska).

* Thu Jul 02 2009 Chris Lumens <clumens@redhat.com> - 1.55-1
- Add support for the group command to F12 (#509119).
- RHEL5 now supports RAID 10.
- The f12 hander class should be called F12Handler. (jgranado)
- Remove bootloader --lba32.
- Add a new version of the driverdisk command without --type=.
- Add initial support for F12.
- Fetch the programmers-guide from the wiki now.

* Mon May 18 2009 Chris Lumens <clumens@redhat.com> - 1.54-1
- Make sure the F11 handler gets used for "partition" and "part" (#501020).

* Wed Apr 29 2009 Chris Lumens <clumens@redhat.com> - 1.53-1
- Move lineno= from KSOptionParser.__init__ to parse_args (#497149). (clumens)
- Use the F11 version of the partition command. (clumens)
- Remove the --start and --end options since anaconda no longer uses them. (clumens)
- Remove a broken test case. (clumens)

* Wed Feb 18 2009 Chris Lumens <clumens@redhat.com> - 1.52-1
- Add lots more test cases (alindebe, mgracik, stickster).
- Add a skip attribute on key to shut up pychecker.
- Only show autostep command when requested (jlaska)
- Strip spaces from service names, and require an option to be provided.
- Surround services lists in double quotes.
- Remove the extra space from the services __str__ method.
- Fix output formatting bugs in firewall, partition, and repo (mgracik).
- Specifying both or neither of --drives and --only-use should be an error.
- Corrected newline char in return value of FC6_Method. (mgracik)
- Make --drives a required option for FC3, and catch no args on F8.
- Fix final printing of the rescue command (mgracik).
- Surround output strings in double quotes.
- Fix a typo in the deviceprobe command.
- Revert the more strict option processing on displaymode.
- Properly handle erroring on extra args, not just extra options.
- Don't use the logging class since it interferes with the logging test.
- port without host should raise KickstartParseError, not kickstartValueError.
- Add the --key option to option processing, since it's a valid argument.
- Fix test cases that were failing due to the new use of KSOptionParser.
- Teach driverdisk.py command to reject extra partitions (stickster).
- Add KSOptionParser to all commands ... enables more strick option checking (jlaska).
- Use KSOptionParser so we can catch bad command options (jlaska).

* Thu Jan 29 2009 Chris Lumens <clumens@redhat.com> - 1.51-1
- Make a couple changes to how the logging command is handled.
- Add a lot of test cases (clumens, alindebe, jlaska, fcami, adamwill, pfrields).
- Fix output formatting for the rootpw command.
- For commands that take exactly one argument, check and error correctly.
- Surround module options in quotes on the output side (jlaska).
- Set module opts in the FC3 handler correctly.
- Fix newlines on the device command output (jlaska).
- If --autoscreenshot is not specified, still output "autostep".
- Move the currentCmd and currentLine into getParser(). (jlaska)
- Write out an selinux line if set to disabled, but not if None.
- F9_LogVolData should inherit from FC4_LogVolData, not FC3_LogVolData (jlaska).
- Add unittest framework along with logvol and vnc unittests. (jlaska)
- Don't set the KSOption.required attribute in the constructor (jlaska).

* Sat Jan 10 2009 Chris Lumens <clumens@redhat.com> - 1.50-1
- Add a script to diff two versions of kickstart syntax.
- Add an option to ksvalidator to list all available syntax versions.
- Remove a couple extra newlines in output formatting.
- Add documentation for the new %%include representation.
- Add support %include to the pykickstart data objects.

* Thu Jan 08 2009 Chris Lumens <clumens@redhat.com> - 1.49-1
- Add upgrade --root-device (atodorov, #471232).
- Use python's builtin set rather than the Sets module (#477836, dcantrell).

* Tue Dec 23 2008 Chris Lumens <clumens@redhat.com> - 1.48-1
- Allow ignoring group metadata from repos, using a '--ignoregroups'
  boolean. (notting)
- Add initial support for F11.
- Specify the command versions in the handlers instead of making copies.
- Remove empty and pointless __init__ methods.
- Pass arguments to superclasses via *args and **kwargs, all the way up.
- Add removedKeywords and removedAttrs lists on Commands and Data.
- Fix version regexes to handle double digits and minor releases (jlaska).

* Thu Oct 30 2008 Chris Lumens <clumens@redhat.com> - 1.47-1
- Fix enabling services we specify by specific options.

* Mon Oct 27 2008 Chris Lumens <clumens@redhat.com> - 1.46-1
- Add support for firewall --service (#467005).

* Tue Oct 14 2008 Chris Lumens <clumens@redhat.com> - 1.45-1
- Lots of translation updates.
- Remove use of string.partition for python2.4 (atodorov).

* Mon Sep 22 2008 Chris Lumens <clumens@redhat.com> - 1.44-1
- Add support for reverse CHAP to the kickstart iscsi command (hans)
- Fix typo (katzj)

* Wed Sep 03 2008 Chris Lumens <clumens@redhat.com> - 1.43-1
- Revert "Do not include passphrases for encrypted block devices in
  anaconda-ks.cfg." (dlehman)
- yum doesn't like when mirrorlist is "". (clumens)

* Mon Aug 11 2008 Chris Lumens <clumens@redhat.com> - 1.42-1
- Add rescue command to pykickstart (atodorov)
- Sort %%packages output (katzj)
- Fix a typo (atodorov).

* Fri Aug 01 2008 Chris Lumens <clumens@redhat.com> - 1.41-1
- RHEL5 supports ignoredisk --only-use now too. (clumens)
- Do not include passphrases for encrypted block devices in
  anaconda-ks.cfg. (dlehman)
- Fix F9,F10,RHEL5 "part" commands to use the same class as
  "partition". (dlehman)
- Add an apply method() for commands and implement for lang (katzj)

* Tue Jul 15 2008 Chris Lumens <clumens@redhat.com> - 1.40-1
- RHEL5_LogVolData should inherit from FC4, not FC3.
  Also fix FC9->F9 typo. (dlehman)
- Support creation of encrypted block devices in RHEL5. (#449830) (dlehman)
- Use the right LogVolData objects for RHEL3 and 4 (jlaska). (clumens)
- We no longer use rhpl for translations. (clumens)
- All the base classes should derive from object. (clumens)

* Fri Jun 13 2008 Chris Lumens <clumens@redhat.com> - 1.39-1
- It's helpful to return the parser object. (clumens)

* Tue Jun 10 2008 Chris Lumens <clumens@redhat.com> - 1.38-1
- Fix loading the Handler object by looking for a more specific
  name (#450740). (clumens)

* Sun Jun 08 2008 Chris Lumens <clumens@redhat.com> - 1.37-1
- XConfig is still used by other projects, so just deprecate some
  options. (clumens)

* Thu May 29 2008 Chris Lumens <clumens@redhat.com> - 1.36-1
- It should be repo --cost, not repo --priority. (clumens)

* Fri May 23 2008 Chris Lumens <clumens@redhat.com> - 1.35-1
- Bring driverdisk command in line with the docs. (clumens)
- Change RAID command print priorities (jlaska).
- According to docs, physvols are space delimited. (jlaska)
- Don't write the label out twice (jlaska).
- Deprecate monitor and xconfig commands. (clumens)

* Wed May 07 2008 Chris Lumens <clumens@redhat.com> - 1.34-1
- Load the handler module automatically. (clumens)
- Add support for F10. (clumens)
- Initialize cmd.handler earlier; fixes repo.methodToRepo() (markmc)
- Don't shadow builtin function names. (clumens)
- Running check is now required before pykickstart can be packaged. (clumens)
- Reorganize code a little bit to pass pychecker. (clumens)

* Tue Apr 08 2008 Chris Lumens <clumens@redhat.com> - 1.33-1
- Fix whitespace when printing out the bootloader command (pmeyers).
- Fix the type on bootloader --timeout processing. (clumens)

* Wed Apr 02 2008 Chris Lumens <clumens@redhat.com> - 1.32-1
- Make the string reader act like the file reader upon EOF. (clumens)
- Add syntax for encrypted logical volumes. (clumens)

* Tue Mar 25 2008 Chris Lumens <clumens@redhat.com> - 1.31-1
- Support end-of-line comments. (clumens)
- Lots of translation updates.

* Tue Feb 26 2008 Chris Lumens <clumens@redhat.com> - 1.30-1
- Reverse writePriorities of iscsi and iscsname (#434965, jlaska).
- Fix printing of iscsiname command (#434945, jlaska).
- Don't traceback on ENOENT. (pnasrat)
- Store the mouse name as a string, not a list. (clumens)
- Update translations.

* Wed Jan 30 2008 Chris Lumens <clumens@redhat.com> - 1.29-1
- Renamed bootproto=ask to bootproto=query, add to RHEL5 as well. (clumens)

* Wed Jan 23 2008 Chris Lumens <clumens@redhat.com> - 1.28-1
- Fix traceback on volgroup command. (clumens)

* Thu Jan 17 2008 Chris Lumens <clumens@redhat.com> - 1.27-1
- The bootprotoList needs to be defined before it's used. (clumens)

* Thu Jan 17 2008 Chris Lumens <clumens@redhat.com> - 1.26-1
- Add support for network --bootproto=ask. (clumens)

* Tue Jan 15 2008 Chris Lumens <clumens@redhat.com> - 1.25-1
- Add the version to the output ks file. (clumens)
- Add syntax for encrypted partitions and raid devices. (clumens)

* Thu Jan 10 2008 Chris Lumens <clumens@redhat.com> - 1.24-1
- Make inheritance and overriding of %%packages work (#427768). (clumens)
- Add an option for which languages should be installed. (katzj)
- Use the right name for the iscsi --target variable (#418781). (clumens)

* Mon Dec 10 2007 Chris Lumens <clumens@redhat.com> - 1.23-1
- Take Makefile improvements from anaconda.
- Fix a traceback on F9 zerombr command (#395431).
- Update to handle new Python eggs packaging.

* Tue Nov 20 2007 Chris Lumens <clumens@redhat.com> 1.22-1
- Don't process or write out vnc --enabled (jlaska AT redhat DOT com).
- Fix a traceback in the clearpart command.

* Tue Nov 06 2007 Chris Lumens <clumens@redhat.com> 1.21-1
- Save script line numbers for debugging.
- More internal cleanups.

* Wed Oct 31 2007 Chris Lumens <clumens@redhat.com> 1.20-1
- Pull wiki docs from the new location.
- Fix error messages for options that have been removed after having been
  previously deprecated.
- zerombr no longer takes any arguments.
- %%packages --ignoredeps --resolvedeps have been removed.
- firewall --high --medium have been removed.
- vnc --connect has been removed.
- xconfig options from monitor have now been removed.
- --bytes-per-inode has been marked as deprecated.
- Fix typos.
- Add --fsprofile option to disk commands (pjones).
- Add F9 support (pjones).
- Lots of internal fixes (clumens, pjones).

* Tue Oct 23 2007 Chris Lumens <clumens@redhat.com> 1.19-1
- Fix a traceback on the cdrom method.

* Thu Oct 18 2007 Chris Lumens <clumens@redhat.com> 1.18-1
- Don't write out %%end to packages and scripts if the syntax version doesn't
  support it.
- Remove obsolete translation (#332221).

* Thu Oct 04 2007 Chris Lumens <clumens@redhat.com> 1.17-1
- Simplify argument processing and printing.

* Wed Oct 03 2007 Chris Lumens <clumens@redhat.com> 1.16-1
- Undeprecate %%packages --excludedocs.
- Fix a traceback in the device command handling.
- Add bootloader --timeout (katzj).

* Tue Oct 02 2007 Chris Lumens <clumens@redhat.com> 1.15-1
- Update translations (#259121).
- The device command no longer takes a type argument.

* Fri Sep 28 2007 Chris Lumens <clumens@redhat.com> 1.14-1
- Fix output formatting for packages section header (#310211).
- Add a script to flatten kickstart files containing includes (katzj).

* Wed Sep 12 2007 Chris Lumens <clumens@redhat.com> 1.13-1
- Add a function to convert URL method strings into repo objects
  (jkeating).
- Writer formatting fixes.
- Add kickstart documentation from the Fedora Wiki.

* Tue Sep 04 2007 Chris Lumens <clumens@redhat.com> 1.12-1
- Fix lots of problems in processing the bootloader, device, network, and
  raid commands.
- Add %%end when writing out scripts and packages.
- Add a makefile target to run pychecker to cut down on errors in
  releases.

* Mon Sep  3 2007 Jeremy Katz <katzj@redhat.com> - 1.11-1
- fix a few tracebacks

* Fri Aug 31 2007 Chris Lumens <clumens@redhat.com> 1.10-1
- Add network --ipv6=.

* Fri Aug 24 2007 Chris Lumens <clumens@redhat.com> 1.9-1
- Add support for the %%end directive to be placed at the end of scripts
  and packages sections.  Deprecate old syntax.
- Clean up after ksvalidator if pykickstart issues a traceback.
- Add support for repo --priority --includepkgs --excludepkgs.
- Fix newline at end of reboot --eject output (#253562).

* Mon Aug 13 2007 Chris Lumens <clumens@redhat.com> 1.8-1
- Fix type checking of string values.

* Thu Aug 09 2007 Chris Lumens <clumens@redhat.com> 1.7-1
- Clarify license in spec file and all source files.
- Check string values to options to make sure they're not other options
  (#251318).

* Thu Aug 02 2007 Chris Lumens <clumens@redhat.com> 1.6-1
- Fix a couple tracebacks in ksvalidator.
- Change --class to --dhcpclass (#248912).

* Thu Jul 19 2007 Chris Lumens <clumens@redhat.com> 1.5-2
- Require rhpl (#248953).

* Tue Jul 17 2007 Chris Lumens <clumens@redhat.com> 1.5-1
- Fix traceback when calling preprocessKickstart.

* Tue Jul 17 2007 Chris Lumens <clumens@redhat.com> 1.4-1
- Add methods to handle the %%ksappend directive.
- Fix ignoredisk --disks.

* Wed Jul 11 2007 Chris Lumens <clumens@redhat.com> - 1.3-1
- Add support for ignoredisk --only-use.
- Fix traceback in raid command printing method (#246709).

* Fri Jun 08 2007 Chris Lumens <clumens@redhat.com> - 1.2-2
- Fix package review problems (#226334).

* Mon Jun 04 2007 Chris Lumens <clumens@redhat.com> - 1.2-1
- Fix harddrive install method error checking (#232492).
- Set authentication information from the input line to preserve quoting
  (#241657).
- Allow included files to be given by URL.
- Fix typo in user --iscrypted option.

* Mon May 14 2007 Chris Lumens <clumens@redhat.com> - 1.1-1
- Better regexes for splitting version strings into family and version.
- Add basic support for RHEL3.
- Update translations.

* Fri Apr 13 2007 Chris Lumens <clumens@redhat.com> - 1.0-1
- Update documentation.
- Update translations.

* Mon Mar 19 2007 Chris Lumens <clumens@redhat.com> - 0.100-1
- bootloader should be written out after upgrade/install.
- Treat class names as unicode strings (#231053).

* Wed Mar 07 2007 Chris Lumens <clumens@redhat.com> - 0.99-1
- The timezone command didn't recognize --isUtc before FC6 (#231189).
- Recognize %%ksappend lines in ksvalidator.
- Don't set default values in some command __init__ methods.
- Added an updates command.
- Add support for RAID10.

* Mon Feb 26 2007 Chris Lumens <clumens@redhat.com> - 0.98-1
- Fix device command syntax to match anaconda.
- Fix __call__ on method command.

* Wed Feb 21 2007 Chris Lumens <clumens@redhat.com> - 0.97-1
- Fix traceback when not overriding default mappings (#229505).

* Tue Feb 20 2007 Chris Lumens <clumens@redhat.com> - 0.96-1
- Fix __str__ methods for langsupport and reboot commands.
- Renamed BaseHandler.empty to BaseHandler.maskAllExcept.
- Split command objects out into their own files in commands/.
- Rename command objects to start with Version_.
- Support extended group selection syntax.

* Wed Feb 14 2007 Chris Lumens <clumens@redhat.com> - 0.95-1
- KickstartParser no longer takes a version argument.
- Be more lenient in what strings stringToVersion accepts.
- Allow setting state on one data object from multiple files.

* Wed Feb 07 2007 Chris Lumens <clumens@redhat.com> - 0.94-1
- Add a newline to the end of the key command output.
- Use network bootproto constants (#197694).
- Fix tracebacks in subclass __str__ methods (#226734).

* Wed Jan 31 2007 Chris Lumens <clumens@redhat.com> - 0.93-2
- Make some minor spec file changes to get closer to the extras guidelines.

* Thu Jan 25 2007 Chris Lumens <clumens@redhat.com> - 0.93-1
- Add support for FC3, RHEL4, and RHEL5.
- The key command was not supported until after FC6.
- Accept more strings in stringToVersion.

* Fri Jan 19 2007 Chris Lumens <clumens@redhat.com> - 0.92-1
- Fix KickstartVersionError reporting.
- Add a version attribute to handler objects.
- Fix line number reporting on lots of commands.
- Add initial support for Fedora 7 and remove deprecated commands.
- Accept a --default argument to the %%packages header (#221305).

* Wed Jan 17 2007 Chris Lumens <clumens@redhat.com> - 0.91-1
- Add a method to read kickstart files from strings.

* Tue Jan 16 2007 Chris Lumens <clumens@redhat.com> - 0.90-1
- Support multiple versions of kickstart syntax from one code base
  (#189348).
- Fix inconsistency between Script parser and writer (#222877).

* Fri Dec 15 2006 Chris Lumens <clumens@redhat.com> - 0.43-1
- Pull in new translations (#216620).

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.42-2
- rebuild against python 2.5

* Tue Dec 05 2006 Chris Lumens <clumens@redhat.com> - 0.42-1
- Fix traceback when writing out repo command (#218274).

* Fri Dec 01 2006 Chris Lumens <clumens@redhat.com> - 0.41-1
- Fix traceback when using deprecated commands (#218047, #218059).

* Thu Nov 30 2006 Chris Lumens <clumens@redhat.com> - 0.40-1
- Pull in new translations (#216620).
- Add --level argument to logging command writer.

* Tue Oct 24 2006 Chris Lumens <clumens@redhat.com> - 0.39-2
- Fix release number.

* Tue Oct 24 2006 Chris Lumens <clumens@redhat.com> - 0.39-1
- Add writer for --key (#211997).

* Tue Oct 17 2006 Jeremy Katz <katzj@redhat.com> - 0.38-1
- allow --skip for installation number as well (#207029)

* Mon Oct 16 2006 Jeremy Katz <katzj@redhat.com> - 0.37-1
- support for installation numbers (#207029)

* Fri Oct 13 2006 Bill Nottingham <notting@redhat.com> - 0.36-1
- use valid charsets in translations (#210720)

* Fri Sep 29 2006 Chris Lumens <clumens@redhat.com> - 0.35-1
- Fix traceback in harddrive command (#208557).

* Mon Sep 25 2006 Chris Lumens <clumens@redhat.com> - 0.34-1
- Add support for --biospart option to harddrive (#207585).
- Update writer for syntax changes.

* Wed Sep 20 2006 Jeremy Katz <katzj@redhat.com> - 0.33-1
- improved iscsi syntax
- allow multiple zfcp devs

* Thu Jul 20 2006 Chris Lumens <clumens@redhat.com> 0.32-1
- Limit --bootproto to what anaconda supports.
- Add --noipv4 and --noipv6 network options.

* Tue Jun 20 2006 Chris Lumens <clumens@redhat.com> 0.31-1
- Handle nfs --opts (katzj).
- RAID devices should be integers instead of strings (#176537).
- Add initial support for iscsi (katzj).

* Tue Jun 06 2006 Chris Lumens <clumens@redhat.com> 0.30-2
- Add BuildRequires to fix building under mock (#194156,  Joost Soeterbroek
  <fedora AT soeterbroek.com>).

* Thu May 25 2006 Chris Lumens <clumens@redhat.com> 0.30-1
- Change order of LVM-related writing functions (#193073).
- Require urlgrabber.
- Return a more useful error message on unknown commands.
- Fix logvol writing typo.
- Make ksvalidator validate from a URL in addition to a file.
- Don't write out an empty packages section (#192851).

* Tue May 23 2006 Chris Lumens <clumens@redhat.com> 0.29-1
- Add multipath command, handlers, and data objects (pjones).
- Rename --ports to --port in writer.

* Mon May 15 2006 Chris Lumens <clumens@redhat.com> 0.28-1
- Support --mtu for the network command (#191328).
- Accept --isUtc for backwards compatibility.

* Thu May 04 2006 Chris Lumens <clumens@redhat.com> 0.27-1
- Output formatting fixes.
- Added commands for managing users and services.

* Mon Apr 17 2006 Chris Lumens <clumens@redhat.com> 0.26-1
- Ignore spaces before group names (#188095).
- Added some translations.
- Add options for repo command.
- Reorder %%packages section output.
- Output %%packages header options.
- Initialize RAID and volume group members to empty lists.

* Mon Mar 27 2006 Chris Lumens <clumens@redhat.com> 0.25-1
- Add support for the logging command.

* Mon Mar 27 2006 Chris Lumens <clumens@redhat.com> 0.24-1 
- Don't write out a blank xconfig line.
- Reorder output handlers to group like commands together.
- Mark strings for translation.

* Tue Mar 07 2006 Chris Lumens <clumens@redhat.com> 0.23-1
- Backwards compatibility support for options to zerombr.

* Fri Feb 24 2006 Chris Lumens <clumens@redhat.com> 0.22-1
- Get ignoredisk working again (#182934).

* Fri Feb 17 2006 Chris Lumens <clumens@redhat.com> 0.21-1
- Provide an option to not traceback on missing include files (#181760).
- Update programming documentation.

* Mon Feb 13 2006 Chris Lumens <clumens@redhat.com> 0.20-1
- Correctly set --noformat and --useexisting on lvm and raid.

* Mon Feb 13 2006 Chris Lumens <clumens@redhat.com> 0.19-1
- --onboot requires a value (#180987).
- Be more strict about commands that don't take arguments.

* Thu Feb 09 2006 Chris Lumens <clumens@redhat.com> 0.18-1
- Fix some errors pychecker caught.
- Allow exceptions to not be fatal so ksvalidator can spot more errors in
  a single pass (#179894).

* Wed Feb 01 2006 Chris Lumens <clumens@redhat.com> 0.17-1
- Don't set a default port for vnc.

* Tue Jan 31 2006 Chris Lumens <clumens@redhat.com> 0.16-1
- Give dmraid string an initial value.
- Handle None on partition size.

* Tue Jan 31 2006 Peter Jones <pjones@redhat.com> 0.15-1
- Add dmraid support

* Mon Jan 30 2006 Chris Lumens <clumens@redhat.com> 0.14-1
- Fix VNC parameter parsing (#179209).
- Deprecate --connect.  Add --host and --port instead.

* Thu Jan 19 2006 Chris Lumens <clumens@redhat.com> 0.13-1
- Recognize the --eject parameter to shutdown/halt.
- Store the exact post-installation action in ksdata.

* Mon Jan 09 2006 Chris Lumens <clumens@redhat.com> 0.12-1
- Clean up output quoting.
- Finish removing monitor-related stuff from xconfig.

* Mon Dec 12 2005 Chris Lumens <clumens@redhat.com> 0.11-1
- Deprecate monitor-related options to xconfig.

* Thu Dec 08 2005 Chris Lumens <clumens@redhat.com> 0.10-1
- Support --bytes-per-inode on raid
  (Curtis Doty <Curtis at GreenKey.net> #175288).

* Wed Nov 16 2005 Jeremy Katz <katzj@redhat.com> - 0.9-1
- fixup network --onboot

* Thu Nov 03 2005 Chris Lumens <clumens@redhat.com> 0.8-1
- Default to SELINUX_ENFORCING.
- Default partition sizes to None for anaconda (#172378).
- Don't call shlex.split on anything inside a script (#172313).

* Tue Nov 01 2005 Chris Lumens <clumens@redhat.com> 0.7-1
- Fix clearpart --all.
- vnc command does not require --connect option (#172192).
- network --onboot does not take any option.
- Remove extra spaces from firewall --ports and --trust.
- Write out network --<service> options.

* Fri Oct 28 2005 Chris Lumens <clumens@redhat.com> 0.6-1
- Add --resolvedeps and --ignoredeps as deprecated options.
- Pass line number to header functions.

* Mon Oct 24 2005 Chris Lumens <clumens@redhat.com> 0.5-1
- Add line numbers to exception reporting.
- Added ksvalidator.

* Wed Oct 19 2005 Chris Lumens <clumens@redhat.com> 0.4-1
- Correct deprecated attribute on options.
- Added programming documentation.

* Thu Oct 13 2005 Chris Lumens <clumens@redhat.com> 0.3-2
- Correct python lib directory on 64-bit archs (#170621).

* Fri Oct 07 2005 Chris Lumens <clumens@redhat.com> 0.3-1
- Add a deprecated attribute to options.
- Add --card option back to xconfig and mark as deprecated.
- Throw a deprecation warning on mouse and langsupport commands.
- Rename Writer to KickstartWriter for consistency.
- Collapse scripts into a single list and add an attribute on Script to
  differentiate.

* Wed Oct 05 2005 Chris Lumens <clumens@redhat.com> 0.2-1
- Rename module to pykickstart to avoid conflicts in anaconda.
- Rename data classes for consistency.
- Add default bytesPerInode settings.

* Wed Oct 05 2005 Chris Lumens <clumens@redhat.com> 0.1-1
- Created package from anaconda.
