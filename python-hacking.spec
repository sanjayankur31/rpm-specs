%global pypi_name hacking

Name:           python-%{pypi_name}
Version:        0.5.3
Release:        1%{?dist}
Summary:        OpenStack Hacking Guidline Enforcement

License:        ASL 2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        http://pypi.python.org/packages/source/h/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-d2to1
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-flake8


%description
OpenStack Hacking Guidline Enforcement


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove /usr/bin/env from core.py
sed -i '1d' hacking/core.py

# remove /usr/bin/env from tests/test_doctest.py
sed -i '1d' hacking/tests/test_doctest.py

%build
%{__python} setup.py build

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%check
%{__python} setup.py test

%files
%doc html README.rst LICENSE
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python_sitelib}/%{pypi_name}

%changelog
* Mon Apr 29 2013 Matthias Runge <mrunge@redhat.com> - 0.5.3-1
- Initial package.
