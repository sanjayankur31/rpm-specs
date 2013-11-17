%global module_name catkin
%global ros_release groovy

# For documentation. Using a tagged release
%global commit 36c38906f63fafc00afafe42d8e5144963135c70
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           ros-%{module_name}-%{ros_release}
Version:        0.5.64
Release:        1%{?dist}
Summary:        a collection of cmake macros and associated python code used to build some parts of ROS

License:        BSD
URL:            https://github.com/ros/%{module_name}
Source0:        https://github.com/ros/%{module_name}/archive/%{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-catkin_pkg python-empy python-nose gtest-devel
# BuildRequires:  python-devel 
BuildRequires:  cmake
## Requires:       

%description
A collection of cmake macros and associated python code used to build some
parts of ROS

%prep
%setup -q -n %{module_name}-%{version}


%build
mkdir build
pushd build
    %cmake -DSETUPTOOLS_DEB_LAYOUT:BOOL=OFF -DCATKIN_BUILD_BINARY_PACKAGE="1" -DCMAKE_BUILD_TYPE=Release ..
    # option unimplemented
    # sed -ibackup 's|--install-layout=deb||' catkin_generated/python_distutils_install.sh
    make %{?_smp_mflags}
popd




%install
rm -rf $RPM_BUILD_ROOT
pushd build
    make install DESTDIR=$RPM_BUILD_ROOT
popd

# Can be removed. Not needed in binary distribution
sed -i 's|@SETUP_DIR@|%{python_sitelib}/%{module_name}/|' $RPM_BUILD_ROOT/usr/setup.sh
mv $RPM_BUILD_ROOT/%{_prefix}/*.{sh,bash,zsh} $RPM_BUILD_ROOT/%{_datadir}/%{module_name}/
mv $RPM_BUILD_ROOT/%{_prefix}/.{rosinstall,catkin} $RPM_BUILD_ROOT/%{_datadir}/%{module_name}/
mv $RPM_BUILD_ROOT/%{_prefix}/*.py $RPM_BUILD_ROOT/%{_datadir}/%{module_name}/

# %check
# ctest

%files
%doc
%{_datadir}/%{module_name}/
%{_bindir}/%{module_name}*
%{_prefix}/lib/pkgconfig/%{module_name}.pc
%{python_sitelib}/%{module_name}/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{_datadir}/eigen/cmake/eigen*.cmake




%changelog
* Sat Mar 16 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.64-1
- Initial rpm build

