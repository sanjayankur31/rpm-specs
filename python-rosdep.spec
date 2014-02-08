%global realname rosdep

Name:           python-rosdep
Version:        0.10.25
Release:        1%{?dist}
Summary:        ROS System Dependency Installer

License:        BSD
URL:            http://ros.org/wiki/rosdep

# wget --content-disposition
# https://github.com/ros-infrastructure/rosinstall_generator/archive/0.1.7.tar.gz
Source0:        %{realname}-%{version}.tar.gz

# Change all "pip" executable references to "python-pip"
# Fedora-only patch, not submitted upstream.
Patch0:         %{realname}-0.10.14-pythonpip.patch
# Disable catkin-sphinx for now, until it's packaged
Patch1:         %{realname}-0.10.14-catkinsphinx.patch
BuildArch:      noarch

BuildRequires:  PyYAML
BuildRequires:  python-catkin_pkg
BuildRequires:  python-devel
BuildRequires:  python-nose
BuildRequires:  python-rospkg
BuildRequires:  python-setuptools-devel
BuildRequires:  python-sphinx

Requires:       PyYAML
Requires:       python-catkin_pkg
Requires:       python-rospkg
Requires:       ros-release


%description
rosdep is a command-line tool for installing system dependencies. For 
end-users, rosdep helps you install system dependencies for software that 
you are building from source. For developers, rosdep simplifies the problem 
of installing system dependencies on different platforms. Instead of having to 
figure out which Debian package on Ubuntu Oneiric contains Boost, you can just 
specify a dependency on 'boost'.


%prep
%setup -qn %{realname}-%{version}
%patch0 -p0 -b .pythonpip
%patch1 -p0 -b .catkinsphinx

%build
%{__python} setup.py build
pushd doc
make man
# HTML requires ros-theme
#make html
popd


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{realname}
install -p -m 0644 manifest.xml $RPM_BUILD_ROOT%{_datadir}/%{realname}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 0644 doc/man/rosdep.1 $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ros/rosdep/sources.list.d/
touch $RPM_BUILD_ROOT%{_sysconfdir}/ros/rosdep/sources.list.d/20-default.list

# Get rid of non-executable-script errors from rpmlint
sed -i 's|#!/usr/bin/env python||' $RPM_BUILD_ROOT%{python_sitelib}/rosdep2/*.py
sed -i 's|#!/usr/bin/env python||' $RPM_BUILD_ROOT%{python_sitelib}/rosdep2/platforms/*.py


%files
%{_bindir}/*
%{python_sitelib}/%{realname}-%{version}-py?.?.egg-info
%{python_sitelib}/%{realname}2
%{_mandir}/man1/*.gz
%{_datadir}/%{realname}
%dir %{_sysconfdir}/ros/rosdep/
%dir %{_sysconfdir}/ros/rosdep/sources.list.d/
%ghost %{_sysconfdir}/ros/rosdep/sources.list.d/20-default.list


%changelog
* Sat Feb 08 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.25-1
- Update to latest upstream release

* Mon Aug 19 2013 Rich Mattes <richmattes@gmail.com> - 0.10.21-1
- Update to release 0.10.21
- Depend on python-catkin_pkg (rhbz#975896)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.18-2.20130601git91fb685
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 01 2013 Rich Mattes <richmattes@gmail.com> - 0.10.18-1.20130601git91fb6852
- Update to release 0.10.18
- Update github source url

* Mon Mar 18 2013 Rich Mattes <richmattes@gmail.com> - 0.10.14-1.20130318git76a8fef
- Update to release 0.10.14
- Fix installer to look for python-pip instead of pip (rhbz922296)
- Move rosdep cache to /var/cache instead of /etc

* Sun Oct 28 2012 Rich Mattes <richmattes@gmail.com> - 0.10.7-1.20121028gita9d29d2
- Update to 0.10.7
- Depend on /etc/ros from ros-release
- Separate build and install steps

* Mon Sep 17 2012 Rich Mattes <richmattes@gmail.com> - 0.9.7-1.20120917git5e1ecef
- Update to 0.9.7

* Sat Jun 16 2012 Rich Mattes <richmattes@gmail.com> - 0.9.5-1
- Update to 0.9.5

* Sun Apr 29 2012 Rich Mattes <richmattes@gmail.com> - 0.9.3-1
- Initial package
