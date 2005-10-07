Summary:  A python library for manipulating kickstart files
Name: pykickstart
Version: 0.3
Release: 1
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: System Environment/Libraries
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: python-devel
Requires: python >= %(%{__python} -c "import sys; print sys.version[:3]")

%description
The pykickstart package is a python library for manipulating kickstart
files.

%prep
%setup -q
make

%build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=${RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog COPYING
%{_libdir}/python?.?/site-packages/pykickstart

%changelog
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
