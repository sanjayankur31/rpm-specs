%global gitrev 644910c

Name:           catkin
Version:        0.5.71
Release:        1.git%{gitrev}%{?dist}
Summary:        Collection of CMake macros for ROS

License:        BSD
URL:            http://ros.org/doc/fuerte/api/catkin/html/
#wget --content-disposition https://github.com/ros/catkin/tarball/0.4.5
Source0:        ros-%{name}-%{version}-0-g%{gitrev}.tar.gz
# Moves all instances of /usr/etc to /etc
# Patch0:         %{name}-0.4.5-etc.patch
# Moves the helper file catkin_util.sh to /usr/share
# Patch1:         %{name}-0.4.5-catkinutil.patch
# Remove dependencies on catkin-sphinx utilities (not yet packaged)
# Patch2:         %{name}-0.4.5-catkinsphinx.patch
# Remove #!/usr/bin/env from python helpers.  Not upstream
# Patch3:         %{name}-0.4.5-scripts.patch
# Add LIB_SUFFIX to pkg-config installation directory
# Patch4:         %{name}-0.4.5-libdir.patch

Provides:       ros-%{name} = %{version}-%{release}
BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  gtest
BuildRequires:  git
BuildRequires:  python-argparse
BuildRequires:  python-empy
BuildRequires:  python-nose
BuildRequires:  python-rospkg
BuildRequires:  python-setuptools-devel
BuildRequires:  python-sphinx
BuildRequires:  python-yaml
BuildRequires:  ros-release
BuildRequires:  python-catkin_pkg
BuildRequires:  python-catkin-sphinx

Requires:  cmake
Requires:  gtest
Requires:  python-argparse
Requires:  python-empy
Requires:  python-nose
Requires:  python-rospkg
Requires:  python-yaml
Requires:  ros-release

%description
Catkin is the Willow Garage low-level build system macros and infrastructure.

%package devel
Summary: Development files for %{name}
Provides: ros-%{name}-devel = %{version}-%{release}
Requires:  %{name} = %{version}-%{release}
Requires:  python-setuptools-devel

%description devel
%{summary}.

%prep
%setup -q -n ros-%{name}-%{gitrev}
# %patch0 -p0 
# %patch1 -p0 -b .catkinutil
# %patch2 -p0 -b .catkinsphinx
# %patch3 -p0
# %patch4 -p0 -b .libdir

%build
mkdir build
pushd build
%cmake -DSETUPTOOLS_DEB_LAYOUT=OFF ..
popd

pushd doc
make html
rm -fr _build/html/.buildinfo
popd

%install
rm -rf $RPM_BUILD_ROOT
make -C build install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
rm $RPM_BUILD_ROOT%{_usr}/.rosinstall
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ros
mv $RPM_BUILD_ROOT%{_usr}/setup.* $RPM_BUILD_ROOT%{_datadir}/ros
mv $RPM_BUILD_ROOT%{_usr}/env.sh $RPM_BUILD_ROOT%{_datadir}/ros

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/catkin.pc $RPM_BUILD_ROOT/%{_datadir}/pkgconfig

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/profile.d
mv $RPM_BUILD_ROOT%{_usr}/etc/%{name}/profile.d/* $RPM_BUILD_ROOT/etc/%{name}/profile.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc doc/_build/html
%{_bindir}/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/profile.d
%config(noreplace) %{_sysconfdir}/%{name}/profile.d/00.*
%exclude %{_datadir}/%{name}/cmake
%{_datadir}/%{name}
%{python_sitelib}/*
%{_datadir}/ros/*

%files devel
%{_datadir}/pkgconfig/*
%{_datadir}/%{name}/cmake

%changelog
* Fri Aug 23 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.71-1.git.g644910c
- Update to 0.5.71

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-8.gitd4f1f24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Rich Mattes <richmattes@gmail.com> - 0.4.5-7.gitd4f1f24
- Make pkg-config templates respect lib64 on 64 bit systems

* Thu Mar 28 2013 Rich Mattes <richmattes@gmail.com> - 0.4.5-6.gitd4f1f24
- Remove shebangs from shell templates and python helper functions

* Mon Mar 25 2013 Rich Mattes <richmattes@gmail.com> - 0.4.5-5.gitd4f1f24
- Rename to "catkin"
- Add clean section for epel6

* Thu Mar 21 2013 Rich Mattes <richmattes@gmail.com> - 0.4.5-4.gitd4f1f24
- Moved /usr/bin/catkin_util.sh to /usr/share/catkin
- Removed shebangs from environment setup files
- Added html documentation

* Mon Jan 28 2013 Rich Mattes <richmattes@gmail.com> - 0.4.5-3.gitd4f1f24
- Update patches and install paths

* Mon Jan 14 2013 Rich Mattes <richmattes@gmail.com> - 0.4.5-2.gitd4f1f24
- Remove "ros-release" requirement

* Sun Jan 13 2013 Rich Mattes <richmattes@gmail.com> - 0.4.5-1.gitd4f1f24
- Initial fuerte release
