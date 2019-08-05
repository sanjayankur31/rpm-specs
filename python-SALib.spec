%bcond_without tests

%global srcname SALib

%global _description %{expand:
Python implementations of commonly used sensitivity analysis methods. Useful in
systems modeling to calculate the effects of model inputs or exogenous factors
on outputs of interest.

Herman, J. and Usher, W. (2017) SALib: An open-source Python library for
sensitivity analysis. Journal of Open Source Software, 2(9).

Methods included:

- Sobol Sensitivity Analysis (Sobol 2001, Saltelli 2002, Saltelli et al. 2010)
- Method of Morris, including groups and optimal trajectories (Morris 1991,
  Campolongo et al. 2007)
- Fourier Amplitude Sensitivity Test (FAST) (Cukier et al. 1973, Saltelli et
  al. 1999)
- Delta Moment-Independent Measure (Borgonovo 2007, Plischke et al. 2013)
- Derivative-based Global Sensitivity Measure (DGSM) (Sobol and Kucherenko
  2009)
- Fractional Factorial Sensitivity Analysis (Saltelli et al. 2008)}

Name:           python-%{srcname}
Version:        1.3.7
Release:        1%{?dist}
Summary:        Sensitivity Analysis Library in Python

License:        MIT
URL:            http://salib.github.io/SALib/
Source0:        %pypi_source

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel

# Not mentioned in setup.py, so won't be picked up by the generator
Requires:  %{py3_dist pandas}
Requires:  %{py3_dist numpy} >= 1.9.0
Requires:  %{py3_dist scipy}
Requires:  %{py3_dist matplotlib} >= 1.4.3

%if %{with tests}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-cov}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist numpy} >= 1.9.0
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib} >= 1.4.3
BuildRequires:  %{py3_dist pyscaffold}
%endif

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%package doc
Summary:        %{summary}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist recommonmark}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info
# Remove uneeded version lock on pyscaffold
sed -i "s/pyscaffold.*']/pyscaffold']/" setup.py

%build
%py3_build

make -C docs SPHINXBUILD=sphinx-build-3 html
rm -rf docs/_build/html/{.doctrees,.buildinfo} -vf

%install
%py3_install

%check
%if %{with tests}
PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitelib} pytest-%{python3_version}
%endif

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.rst README-advanced.md CHANGELOG.rst CITATIONS.rst AUTHORS.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%{_bindir}/salib
%{_bindir}/salib.py

%files doc
%license LICENSE.txt
%doc docs/_build/html

%changelog
* Mon Aug 05 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.7-1
- Update to new release

* Tue Jan 29 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.3-1
- Initial build
