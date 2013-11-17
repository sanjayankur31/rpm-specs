# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global module_name rosdep
Name:           python-%{module_name}
Version:        0.10.14
Release:        1%{?dist}
Summary:        Command-line tool for installing system dependencies on a variety of platforms

License:        BSD
URL:            https://pypi.python.org/pypi/%{module_name}
Source0:        https://pypi.python.org/packages/source/r/%{module_name}/%{module_name}-%{version}.tar.gz

# It looks for pip, but we provide pip
Patch0:         0001-rosdep-0.10.14-pip-python-fedora.patch

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools

%description
Command-line tool for installing system dependencies on a variety of platforms


%prep
%setup -q -n %{module_name}-%{version}
%patch0 -p0


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ros/rosdep/sources.list.d/
touch $RPM_BUILD_ROOT%{_sysconfdir}/ros/rosdep/sources.list.d/20-default.list

 
%files
%doc
%{_bindir}/%{module_name}
%{python_sitelib}/%{module_name}2/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info/
%dir %{_sysconfdir}/ros/rosdep/
%dir %{_sysconfdir}/ros/rosdep/sources.list.d/
%ghost %{_sysconfdir}/ros/rosdep/sources.list.d/20-default.list


%changelog
* Sat Mar 16 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.14-1
- Initial rpm build

