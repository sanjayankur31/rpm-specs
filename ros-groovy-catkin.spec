%global module_name catkin
%{?scl:%scl_package catkin}
%{!?scl:%global pkg_name %{name}}

# Python globals
%global pybasever 2.7
%global pylibdir %{_libdir}/python%{pybasever}
%global scl_python_sitearch %{pylibdir}/site-packages
%global scl_python_sitelib %{_prefix}/lib/python%{pybasever}/site-packages

Name:           %{?scl_prefix}%{module_name}
Version:        0.5.71
Release:        1%{?dist}
Summary:        ROS groovy %{module_name} module.
BuildArch:      noarch

License:        BSD
URL:            http://www.ros.org/wiki/catkin

# wget --content-disposition https://github.com/ros/catkin/archive/0.5.71.tar.gz
Source0:        %{module_name}-%{version}.tar.gz

# BuildRequires
BuildRequires:       cmake
BuildRequires:       gtest-devel
BuildRequires:       python2-devel
BuildRequires:       python-catkin_pkg
BuildRequires:       python-empy
BuildRequires:       python-nose
BuildRequires:       git

BuildRequires:       python-rospkg
BuildRequires:       python-argparse
BuildRequires:       python-setuptools-devel

# Documents
BuildRequires:       python-sphinx
BuildRequires:       python-catkin-sphinx

# Tests
BuildRequires:       python-subprocess32
BuildRequires:       python-mock
BuildRequires:       python-rosinstall
BuildRequires:       python-dateutil
BuildRequires:       python-yaml



# Requires
Requires:        cmake
Requires:        gtest
Requires:        python
Requires:        python-catkin_pkg >= 0.1.12
Requires:        python-empy
Requires:        python-nose


%{?scl:Requires: %scl_runtime}

%description
Low-level build system macros and infrastructure for ROS.

%package devel
Summary: Development files for %{name}
Requires:  %{?scl_prefix}%{module_name} = %{version}-%{release}
Requires:  python-setuptools-devel

%description devel
%{summary}.

%prep
%setup -q -n %{module_name}-%{version}


%build
mkdir build
pushd build
    %cmake  .. -DSETUPTOOLS_DEB_LAYOUT=OFF
    make %{?_smp_mflags}
popd

pushd doc
# Sphinx fails with errors
    make html
    make man
popd


%install
pushd build
    make install DESTDIR=$RPM_BUILD_ROOT
popd

#mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
rm $RPM_BUILD_ROOT%{?_scl_root}%{_usr}/.rosinstall
rm $RPM_BUILD_ROOT%{?_scl_root}%{_usr}/.catkin

# _usr needs the scl_root, but _datadir doesn't
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ros
mv $RPM_BUILD_ROOT%{?_scl_root}%{_usr}/setup.* $RPM_BUILD_ROOT%{_datadir}/ros
mv $RPM_BUILD_ROOT%{?_scl_root}%{_usr}/env.sh $RPM_BUILD_ROOT%{_datadir}/ros

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig
mv -v $RPM_BUILD_ROOT/%{?_scl_root}/%{_usr}/lib/pkgconfig/%{module_name}.pc $RPM_BUILD_ROOT/%{_datadir}/pkgconfig

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{module_name}/profile.d
mv -v $RPM_BUILD_ROOT%{?_scl_root}%{_usr}/etc/%{module_name}/profile.d/* $RPM_BUILD_ROOT/%{_sysconfdir}/%{module_name}/profile.d


# Do these need genmsg installed? 
# I thought genmsg needs to be built later.
# %check
#nosetests test/


%files
%doc LICENSE README.rst CHANGELOG.rst
#%doc doc/_build/html
%{_bindir}/*
%dir %{_sysconfdir}/%{module_name}
%dir %{_sysconfdir}/%{module_name}/profile.d
%config(noreplace) %{_sysconfdir}/%{module_name}/profile.d/*
%exclude %{_datadir}/%{module_name}/cmake
%{_datadir}/%{module_name}
%{scl_python_sitelib}/*
%{_datadir}/ros/*
%{_datadir}/eigen/cmake/eigen*cmake
%{?_scl_root}/%{_usr}/_setup_util.py*

%files devel
%{_datadir}/pkgconfig/*
%{_datadir}/%{module_name}/cmake

%changelog
# Need to replace it with today's date
* Sun Aug 04 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.71 -1
- Initial rpm build

