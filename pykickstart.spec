%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary:  A python library for manipulating kickstart files
Name: pykickstart
Version: 0.38
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: System Environment/Libraries
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: python-devel
BuildRequires: gettext
Requires: python >= %(%{__python} -c "import sys; print sys.version[:3]")
Requires: python-urlgrabber

%description
The pykickstart package is a python library for manipulating kickstart
files.

%prep
%setup -q
make

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog COPYING docs/programmers-guide
%{python_sitelib}/pykickstart
/usr/bin/ksvalidator
/usr/share/locale/*/*/*

%changelog
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
- Reorder %packages section output.
- Output %packages header options.
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
