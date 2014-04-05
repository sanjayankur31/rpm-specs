# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global source_name catkin_lint

Name:           python-%{source_name}
Version:        1.3.4
Release:        1%{?dist}
Summary:        Check catkin packages for common errors

License:        BSD
URL:            https://pypi.python.org/pypi/%{source_name}
Source0:        https://pypi.python.org/packages/source/c/%{source_name}/%{source_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

Requires:       python-catking_pkg

%description
catkin_lint checks package configurations for the catkin build system of ROS.
It is part of an ongoing effort to aid developers with their ROS packaging (see
also: issue #153).

%prep
%setup -q -n %{source_name}-%{version}


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

for lib in $RPM_BUILD_ROOT%{python_sitelib}/%{source_name}/*.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

for lib in $RPM_BUILD_ROOT%{python_sitelib}/%{source_name}/checks/*.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

#%check
#pushd test
#    %{__python2} test_all_checks.py
#popd
 
%files
%doc changelog.txt README.rst README_API.rst 
%{python_sitelib}/%{source_name}-%{version}-py?.?.egg-info
%{python_sitelib}/%{source_name}/
%{_bindir}/%{source_name}

%dir %{_sysconfdir}/bash_completion.d/
%{_sysconfdir}/bash_completion.d/%{source_name}


%changelog
* Sat Apr 05 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.3.4-1
- Initial package build
