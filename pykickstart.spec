%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:  A python library for manipulating kickstart files
Name: pykickstart
Url: http://fedoraproject.org/wiki/pykickstart
Version: 1.5
Release: 2%{?dist}
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0: %{name}-%{version}.tar.gz

License: GPL
Group: System Environment/Libraries
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel, gettext
Requires: python, python-urlgrabber, rhpl

%description
The pykickstart package is a python library for manipulating kickstart
files.

%prep
%setup -q
make

%build

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README ChangeLog COPYING docs/programmers-guide
%{python_sitelib}/pykickstart
%{_bindir}/ksvalidator

%changelog
* Thu Jul 19 2007 Chris Lumens <clumens@redhat.com> 1.5-2
- Require rhpl (#248953).

* Tue Jul 17 2007 Chris Lumens <clumens@redhat.com> 1.5-1
- Fix traceback when calling preprocessKickstart.

* Tue Jul 17 2007 Chris Lumens <clumens@redhat.com> 1.4-1
- Add methods to handle the %ksappend directive.
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
- Recognize %ksappend lines in ksvalidator.
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
