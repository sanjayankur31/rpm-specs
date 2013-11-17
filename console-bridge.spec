%global realname console_bridge
%global gitrev 96c8951
Name:		console-bridge
Version:	0.1.4
Release:	2%{?dist}
Summary:	Lightweight set of macros used for reporting information in libraries

Group:		Development/Libraries
License:	BSD
URL:		http://ros.org/wiki/console_bridge
# wget --content-disposition https://github.com/ros/console_bridge/tarball/0.1.4
Source0:	ros-%{realname}-%{version}-0-g%{gitrev}.tar.gz
# Makes library installation directory configurable.  Not yet upstream
Patch0:		%{name}-0.1.4-libdir.patch

BuildRequires:	cmake
BuildRequires:	boost-devel

%description
A very lightweight set of macros that can be used for reporting information 
in libraries. The logged information can be forwarded to other systems.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
%summary 

%prep
%setup -q -n ros-%{realname}-%{gitrev}
%patch0 -p0 -b .libdir

%build
mkdir build; pushd build
%cmake ..
popd
make -C build %{?_smp_mflags}


%install
make -C build install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/%{realname}
%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{realname}


%changelog
* Tue Apr 09 2013 Rich Mattes <richmattes@gmail.com> - 0.1.4-2
- Add ldconfig calls
- Add patch to create a soversion, set it to 0

* Tue Mar 12 2013 Rich Mattes <richmattes@gmail.com> - 0.1.4-1
- Update to release 0.1.4

* Sun Dec 02 2012 Rich Mattes <richmattes@gmail.com> - 0.1.2-2
- Fixed library path in console_bridge-config.cmake

* Sat Oct 13 2012 Rich Mattes <richmattes@gmail.com> - 0.1.2-1
- Initial package
