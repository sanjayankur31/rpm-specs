%global module_name genmsg
%{?scl:%scl_package genmsg}
%{!?scl:%global pkg_name %{name}}

# Python globals
%global pybasever 2.7
%global pylibdir %{_libdir}/python%{pybasever}
%global scl_python_sitearch %{pylibdir}/site-packages
%global scl_python_sitelib %{_prefix}/lib/python%{pybasever}/site-packages


Name:           %{?scl_prefix}%{module_name}
Version:        0.4.21
Release:        1%{?dist}
Summary:        ROS groovy %{module_name} module
BuildArch:      noarch

BuildArch:      noarch
License:        BSD
URL:            http://www.ros.org/wiki/genmsg

# wget --content-disposition https://github.com/ros/genmsg/archive/0.4.21.tar.gz
Source0:        %{module_name}-%{version}.tar.gz

# BuildRequires
BuildRequires:       ros-groovy-catkin-devel >= 0.5.68

# not autodetected
BuildRequires:       gtest-devel
BuildRequires:       python2-devel
BuildRequires:       python-sphinx
BuildRequires:       python-catkin-sphinx



%{?scl:Requires: %scl_runtime}

%description
Standalone Python library for generating ROS message and service data
structures for various languages.

%package devel
Summary: Development files for %{name}
Requires:  %{?scl_prefix}%{module_name} = %{version}-%{release}
Requires:  python-setuptools-devel

%description devel
Development files for %{module_name}



%prep
%setup -q -n %{module_name}-%{version}


%build
%{?scl:scl -l}

%{?scl:scl enable %{scl} - << \EOF}
python -c 'import sys; print sys.path'

mkdir build
pushd build
    %cmake  .. -DCATKIN_BUILD_BINARY_PACKAGE="1" -DSETUPTOOLS_DEB_LAYOUT=OFF
    make %{?_smp_mflags}
popd
pushd doc
    export PYTHONPATH=$(pwd)/src/genmsg
    make html man
popd
%{?scl:EOF}

%install
%{?scl:scl -l}
%{?scl:scl enable %{scl} "}
make -C build install DESTDIR=$RPM_BUILD_ROOT
%{?scl:"}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig
mv -v $RPM_BUILD_ROOT/%{?_scl_root}/%{_usr}/lib/pkgconfig/%{module_name}.pc $RPM_BUILD_ROOT/%{_datadir}/pkgconfig

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
mv -v doc/_build/man/* $RPM_BUILD_ROOT%{_mandir}/man1/

# language generators
mkdir -p %{buildroot}/%{_sysconfdir}/ros-langs

%check

%files
%doc doc/_build/html CHANGELOG.rst
%{_mandir}/man1/%{module_name}*
%exclude %{_datadir}/%{module_name}/cmake
%{_datadir}/%{module_name}
%{scl_python_sitelib}/*
%dir %{_sysconfdir}/ros-langs

%files devel
%{_datadir}/pkgconfig/*
%{_datadir}/%{module_name}/cmake

%changelog
# Need to replace it with today's date
* Sun Aug 04 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.21 -1
- Initial rpm build

