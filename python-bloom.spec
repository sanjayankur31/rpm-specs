%global commit 0e563e5964d01673dfc6e227625353d1a2a847ef
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global module_name bloom
Name:           python-%{module_name}
Version:        0.4.4
Release:        1%{?dist}
Summary:        A ROS release automation tool for catkin packages

License:        BSD
URL:            https://github.com/ros-infrastructure/%{module_name}
Source0:        https://github.com/ros-infrastructure/%{module_name}/archive/%{commit}/%{module_name}-%{version}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools python-sphinx

%description
A tool for helping release software into gitbuildpackage repositories

%prep
%setup -q -n %{module_name}-%{commit}


%build
%{__python} setup.py build

# Dunno, can't get it to work
#cd doc/
#make dirhtml 
#make singlehtml 
#make man 
#cd ..


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


# Tests are in the wrong place
rm -rvf $RPM_BUILD_ROOT/%{python_sitelib}/test/

# Haven't figured out how to use the tests yet
# %check 
# %{__python} setup.py test
 
%files
%doc  CHANGELOG.rst README.rst LICENSE.txt 
%{_bindir}/bloom*
%{_bindir}/git-bloom*
%{python_sitelib}/bloom/
%{python_sitelib}/bloom-%{version}-py?.?.egg-info/

%changelog
* Wed Jul 24 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.4.4-1
- Initial rpmbuild

