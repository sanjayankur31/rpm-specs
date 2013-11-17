%global module_name genmsg
%global ros_release groovy

Name:		ros-%{module_name}-%{ros_release}
Version:	0.4.18
Release:	1%{?dist}
Summary:	Standalone Python library for generating ROS message and service data structures for various languages

BuildArch:      noarch
License:	BSD
URL:            https://github.com/ros/%{module_name}
Source0:        https://github.com/ros/%{module_name}/archive/%{module_name}-%{version}.tar.gz

BuildRequires:	cmake ros-catkin-groovy python-empy gtest-devel
BuildRequires:  python-catkin_pkg

%description
Standalone Python library for generating ROS message and service data
structures for various languages


%prep
%setup -q -n %{module_name}-%{version}


%build
mkdir build
pushd build
    %cmake .. -Dcatkin_DIR:STRING=$RPM_BUILD_ROOT/%{_datadir}/catkin/cmake/catkinConfig.cmake -DSETUPTOOLS_DEB_LAYOUT:BOOL=OFF

    make %{?_smp_mflags}
popd


%install
pushd build
    make install DESTDIR=$RPM_BUILD_ROOT
popd

# Not required for binary package
mv $RPM_BUILD_ROOT/%{_prefix}/*.{sh,bash,zsh} $RPM_BUILD_ROOT/%{_datadir}/%{module_name}/
mv $RPM_BUILD_ROOT/%{_prefix}/.{rosinstall,catkin} $RPM_BUILD_ROOT/%{_datadir}/%{module_name}/
mv $RPM_BUILD_ROOT/%{_prefix}/*.py $RPM_BUILD_ROOT/%{_datadir}/%{module_name}/


%files
%doc
%{_datadir}/%{module_name}/
%{python_sitelib}/%{module_name}/
%{_prefix}/lib/pkgconfig/%{module_name}.pc
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info



%changelog
* Sun Mar 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.4.18-1
- initial rpm build


