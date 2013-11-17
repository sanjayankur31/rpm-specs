# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global module_name rospkg
Name:           python-%{module_name}
Version:        1.0.19
Release:        1%{?dist}
Summary:        Library for retrieving information about ROS packages and stacks

License:        BSD
URL:            https://pypi.python.org/pypi/%{module_name}
Source0:        https://pypi.python.org/packages/source/r/%{module_name}/%{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools

%description
Library for retrieving information about ROS packages and stacks

%prep
%setup -q -n %{module_name}-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc
%{_bindir}/rosversion
%{python_sitelib}/%{module_name}/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info/


%changelog
* Sat Mar 16 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0.19-1
- Initial rpmbuild


