%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# disabled to begin with
%bcond_with tests

%global pypi_name pynwb

%global desc %{expand: \
PyNWB is a Python package for working with NWB files. It provides a high-level /
API for efficiently working with Neurodata stored in the NWB format. /
https://pynwb.readthedocs.io/en/latest/}

Name:           python-%{pypi_name}
Version:        0.6.1
Release:        2%{?dist}
Summary:        PyNWB is a Python package for working with NWB files
License:        BSD
URL:            https://github.com/NeurodataWithoutBorders/pynwb
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-certifi
BuildRequires:  python2-chardet
BuildRequires:  python2-h5py
BuildRequires:  python2-idna
BuildRequires:  python2-numpy
BuildRequires:  python2-dateutil
BuildRequires:  python2-requests
BuildRequires:  python2-ruamel-yaml
BuildRequires:  python2-six
BuildRequires:  python2-urllib3
BUildRequires:  python2-pandas

%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-certifi
BuildRequires:	python3-chardet
BuildRequires:	python3-h5py
BuildRequires:	python3-idna
BuildRequires:	python3-numpy
BuildRequires:	python3-dateutil
BuildRequires:  python3-requests
BuildRequires:	python3-ruamel-yaml
BuildRequires:	python3-six
BuildRequires:  python3-urllib3
BUildRequires:  python3-pandas

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{desc}

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py3_build
%if %{with py2}
%py2_build
%endif

%install
%if %{with py2}
%py2_install
%endif
%py3_install
 
#%check
#%if %{with tests}
#%if %{with py2}
#%{__python2} setup.py test
#%endif
#%{__python3} setup.py test
#%endif

%if %{with py2}
%files -n python2-%{pypi_name}
%license license.txt
%doc README.rst
%{python2_sitelib}/%{pypi_name}-%{version}-py2.?.egg-info
%{python2_sitelib}/%{pypi_name}
%endif 

%files -n python3-%{pypi_name}
%license license.txt
%doc README.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info

%changelog
* Mon Nov 26 2018 Luis Bazan <lbazan@fedoraproject.org> - 0.6.1-2
- Fix comment 2 in BZ 1651365

* Mon Nov 26 2018 Luis Bazan <lbazan@fedoraproject.org> - 0.6.1-1
- New upstream
