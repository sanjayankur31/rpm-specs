%global commit 90db8ac29bd53b7544de8243778cd35fef4589dd
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global module_name catkin_pkg
Name:           python-%{module_name}
Version:        0.1.18
Release:        1%{?dist}
Summary:        Library for retrieving information about catkin packages

License:        BSD
URL:            https://github.com/ros-infrastructure/%{module_name}
Source0:        https://github.com/ros-infrastructure/%{module_name}/archive/%{commit}/%{module_name}-%{version}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools

%description
Library for retrieving information about catkin packages

%prep
%setup -q -n %{module_name}-%{commit}


%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc README.rst
%{_bindir}/catkin_create_pkg
%{_bindir}/catkin_generate_changelog
%{_bindir}/catkin_tag_changelog
%{_bindir}/catkin_test_changelog
%{python_sitelib}/%{module_name}/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info


%changelog
* Wed Jul 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.18-1
- Update to 0.1.18
- https://bugzilla.redhat.com/show_bug.cgi?id=926034

* Sat Mar 16 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.10-1
- Initial rpm build



