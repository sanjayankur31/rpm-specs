%global commit d0b5ce1d8f42050a5674875b866a7dda6383a75b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           roscpp_core
Version:        0.2.6
Release:        1.20130605git%{shortcommit}%{?dist}
Summary:        The ROS C++ API

License:        BSD
URL:            http://www.ros.org/wiki/roscpp_core
Source0:        https://github.com/ros/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
# Add LIB_SUFFIX to lib installation dirs.  Not upstream
Patch0:         %{name}-0.2.6-libdir.patch

BuildRequires:  cmake
BuildRequires:  gtest
BuildRequires:  boost-devel
BuildRequires:  python-sphinx
BuildRequires:  ros-catkin-devel

%description
roscpp-core is an underlying library for support roscpp message data 
types. It is a lightweight/minimal library that can easily be used 
in non-ROS-based projects. 

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary:  Development files for %{name}

%description devel
Development files for %{name}

%prep
%setup -qn %{name}-%{commit}
%patch0 -p0 -b .libdir
%build
mkdir build
pushd build
%cmake -DSETUPTOOLS_DEB_LAYOUT=OFF ..
popd
pushd doc
make html
rm -f build/html/.buildinfo
popd

%install
make -C build install DESTDIR=%{buildroot}

%files
%exclude %{_datadir}/*/cmake
%{_libdir}/*.so
%{_datadir}/cpp_common
%{_datadir}/roscpp_core
%{_datadir}/roscpp_serialization
%{_datadir}/roscpp_traits
%{_datadir}/rostime

%files devel
%doc doc/build/html
%{_includedir}/ros
%{_libdir}/pkgconfig/*.pc
%{_datadir}/cpp_common/cmake
%{_datadir}/roscpp_serialization/cmake
%{_datadir}/roscpp_traits/cmake
%{_datadir}/rostime/cmake


%changelog
* Wed Jun 05 2013 Rich Mattes <richmattes@gmail.com> - 0.2.6-1.20130605gitd0b5ce1
- Update to release 0.2.6
- Update source to github guidelines

* Mon Mar 25 2013 Rich Mattes <richmattes@gmail.com> - 0.2.5-2.gite92f9eb
- Change name to roscpp_core
- Fix virtual provides

* Tue Sep 04 2012 Rich Mattes <richmattes@gmail.com> - 0.2.5-1.gite92f9eb
- Initial package
