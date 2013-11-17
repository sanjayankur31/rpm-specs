%global module_name gencpp
%global ros_release groovy


Name:           ros-gencpp-groovy
Version:        0.4.12
Release:        1%{?dist}
Summary:        ROS C++ message definition and serialization generators

License:        BSD
URL:            https://github.com/ros/%{module_name}
Source0:        https://github.com/ros/%{module_name}/archive/%{module_name}-%{version}.tar.gz

BuildRequires:  cmake python-empy gtest-devel python-nose
BuildRequires:  python-catkin_pkg 
BuildRequires:  ros-catkin-groovy
BuildRequires:  ros-genmsg-groovy

%description
ROS C++ message definition and serialization generators


%prep
%setup -q -n %{module_name}-%{version}


%build
mkdir build
pushd build
%cmake .. -DCMAKE_PREFIX_PATH=$RPM_BUILD_ROOT/%{_datadir}/genmsg/cmake
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd


%files
%doc



%changelog
* Sun Mar 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.4.12-1
- initial rpmbuild

