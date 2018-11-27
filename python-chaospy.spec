%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

%bcond_without tests

# Fail to build
%bcond_with docs

%global pypi_name chaospy

%global desc %{expand: \
Chaospy is a numerical tool for performing uncertainty quantification using
polynomial.}

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
BuildRequires:  %{py2_dist setuptools}
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist pytest-runner}
BuildRequires:  %{py2_dist pytest-cov}
BuildRequires:  %{py2_dist scikit-learn}
BuildRequires:  %{py2_dist seaborn}
BuildRequires:  %{py2_dist networkx}
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist scipy}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist seaborn}
Requires:   %{py2_dist networkx}
Requires:   %{py2_dist numpy}
Requires:   %{py2_dist scipy}
Requires:   %{py2_dist scikit-learn}

%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-runner}
BuildRequires:  %{py3_dist pytest-cov}
BuildRequires:  %{py3_dist scikit-learn}
BuildRequires:  %{py3_dist seaborn}
BuildRequires:  %{py3_dist networkx}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist seaborn}
# docs
%if %{with docs}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinxcontrib-bibtex}
%endif
Requires:       %{py3_dist networkx}
Requires:       %{py3_dist numpy}
Requires:       %{py3_dist scipy}
Requires:       %{py3_dist scikit-learn}

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

%if %{with docs}
pushd doc
    make SPHINXBUILD=sphinx-build-3 html
    rm -rf build/.doctrees
    rm -rf build/.buildinfo
popd
%endif

%install
%if %{with py2}
%py2_install
%endif
%py3_install

%check
%if %{with tests}
%if %{with py2}
export PYTHONPATH=$RPM_BUILD_ROOT/%{python2_sitelib}
pytest-%{python2_version} tests
%endif

export PYTHONPATH=$RPM_BUILD_ROOT/%{python3_sitelib}
pytest-%{python3_version} tests
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

%files doc
%license LICENSE.txt
%doc tutorial
%if %{with docs}
%doc doc/build/html
%endif


%changelog
* Mon Nov 26 2018 Luis Bazan <lbazan@fedoraproject.org> - 2.3.4-1
- New upstream
