%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# disabled to begin with
%bcond_with tests

%global pypi_name chaospy

%global desc %{expand: \
Chaospy is a numerical tool for performing uncertainty
 quantification using polynomial.}

Name:           python-%{pypi_name}
Version:        2.3.4
Release:        1%{?dist}
Summary:        Numerical tool for performing uncertainty quantification using polynomial
License:        BSD
URL:            https://github.com/jonathf/chaospy
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
%{desc}

%if %{with py2}
%package -n python2-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires:	python2-networkx
Requires:	python2-numpy
Requires:	python2-scipy
Requires:	python2-scikit-learn
	
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-networkx
Requires:       python3-numpy
Requires:       python3-scipy
Requires:	python3-scikit-learn

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

%check
%if %{with tests}
%if %{with py2}
%{__python2} setup.py test
%endif
%{__python3} setup.py test
%endif

%if %{with py2}
%files -n python2-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif 

%files -n python3-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Mon Nov 26 2018 Luis Bazan <lbazan@fedoraproject.org> - 2.3.4-1
- New upstream
