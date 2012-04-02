%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:  A python library for manipulating kickstart files
Name: pykickstart
Url: http://fedoraproject.org/wiki/pykickstart
Version: 1.99.10
Release: 1%{?dist}
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0: %{name}-%{version}.tar.gz

License: GPLv2
Group: System Environment/Libraries
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel, gettext, python-setuptools-devel
BuildRequires: transifex-client
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

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README ChangeLog COPYING docs/programmers-guide
%doc docs/kickstart-docs.txt
%{python_sitelib}/*
%{_bindir}/ksvalidator
%{_bindir}/ksflatten
%{_bindir}/ksverdiff

%changelog
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

* Wed May 04 2006 Chris Lumens <clumens@redhat.com> 0.27-1
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
