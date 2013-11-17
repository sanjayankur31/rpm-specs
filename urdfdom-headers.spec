%global realname urdfdom_headers

Name:		urdfdom-headers
Version:	0.2.2
Release:	2%{?dist}
Summary:	The URDF (U-Robot Description Format) headers

Group:		Development/Libraries
License:	BSD
URL:		http://ros.org/wiki/urdf
# Use the script generate-tarball-urdfdom-headers to check out source and
# create export the correct branch
Source0:	%{name}-%{version}.tar.bz2
Source1:	generate-tarball-%{name}.sh
# This patch moves the pkgconfig file to /usr/share and moves the headers
# to the "urdf" subdirectory of /usr/include
# Not submitted upstream.
Patch0:		urdf-0.2.0-fedora.patch
BuildArch:	noarch
BuildRequires:	cmake

%description
%{summary}

%package devel
Summary: The URDF (U-Robot Description Format) headers
Requires: pkgconfig
BuildArch: noarch
Provides: %{name}-static = %{version}-%{release}

%description devel
The URDF (U-Robot Description Format) headers provides core data structure
headers for URDF.

For now, the details of the URDF specifications reside on
http://ros.org/wiki/urdf

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .fedora

%build
mkdir build; pushd build
%cmake ..
popd
make -C build %{?_smp_mflags}


%install
make -C build install DESTDIR=%{buildroot}

# LICENSE file is not correct, don't include it
%files devel
%doc README.txt
%{_includedir}/urdf
%{_includedir}/urdf_world
%{_datadir}/pkgconfig/*.pc
%{_datadir}/%{realname}

%changelog
* Tue Apr 09 2013 Rich Mattes <richmattes@gmail.com> - 0.2.2-2
- Added -static virtual provides to -devel subpackage
- Moved package description to -devel subpackage

* Tue Mar 12 2013 Rich Mattes <richmattes@gmail.com> - 0.2.2-1
- Update to release 0.2.2
- Don't install incorrect LICENSE file

* Tue Oct 16 2012 Rich Mattes <richmattes@gmail.com> - 0.2.1-1
- Update to release 0.2.1

* Wed Sep 26 2012 Rich Mattes <richmattes@gmail.com> - 0.2.0-1
- Initial package
