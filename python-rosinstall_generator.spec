%global module_name  rosinstall_generator

Name:           python-%{module_name}
Version:        0.1.7
Release:        1%{?dist}
Summary:        Generates rosinstall files

License:        BSD
URL:            http://wiki.ros.org/%{module_name}

# wget --content-disposition
# https://github.com/ros-infrastructure/rosinstall_generator/archive/0.1.7.tar.gz

Source0:        %{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
The rosinstall_generator generates rosinstall files containing information
about repositories with ROS packages/stacks. 

%prep
%setup -q -n %{module_name}-%{version}


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc LICENSE.txt README.rst
%{python2_sitelib}/%{module_name}
%{python2_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{_bindir}/%{module_name}


%changelog
* Sat Feb 08 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.7-1
- Updated as per comments in rhbz 1062843
-  Initial rpm build
