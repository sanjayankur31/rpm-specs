%global gitrev f0fdb1e

Name:           ros
Version:        1.8.10
Release:        2%{?dist}
Summary:        The Robot Operating System

License:        BSD
URL:            http://ros.org/
# svn export http://code.ros.org/svn/ros/stacks/ros/tags/ros-1.8.10 ros-1.8.10
# tar cjf ros-1.8.10.tar.bz2 ros-1.8.10/
Source0:        ros-%{version}.tar.bz2
Provides:       ros-%{name}%{?_isa} = %{version}-%{release}

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gtest-devel
BuildRequires:  ros-catkin-devel
BuildRequires:  ros-rospack-devel
BuildRequires:  ros-release

Requires:       ros-release

%description
ROS is a meta-operating system for your robot.  It provides language-
independent and network-transparent communication for a distributed 
robot control system.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: ros-%{name}-devel%{?_isa} = %{version}-%{release}
Summary:  Development files for %{name}

%description devel
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build
source %{_datadir}/ros/setup.sh
mkdir build
pushd build
%cmake -DSETUPTOOLS_DEB_LAYOUT=OFF ..
popd

%install
rm -rf $RPM_BUILD_ROOT
make -C build install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_usr}/etc $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/{lib,%{_lib}}/*.so
mv $RPM_BUILD_ROOT/usr/{lib,%{_lib}}/pkgconfig

%files
%doc AUTHORS LICENSE/LICENSE README
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/catkin/profile.d/*
%{_libdir}/*.so
%exclude %{_datadir}/*/cmake/
%{_datadir}/%{name}/*
%{_datadir}/rosbash
%{_datadir}/roscreate
%{_datadir}/rosboost_cfg
%{_datadir}/rosclean
%{_datadir}/roslang
%{_datadir}/roslib
%{_datadir}/rosmake
%{_datadir}/rosunit
%{python_sitelib}/*

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
%{_datadir}/*/cmake/

%changelog
* Mon Mar 25 2013 Rich Mattes <richmattes@gmail.com> - 1.8.10-2
- Require ros-release for /usr/share/ros

* Sun Jan 13 2013 Rich Mattes <richmattes@gmail.com> - 1.8.10-1
- Initial fuerte package

