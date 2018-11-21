# Package is py3 only

%bcond_without tests

%bcond_with docs

%global srcname pingouin

%global desc %{expand: \
Pingouin is an open-source statistical package written in Python 3 and based on
Pandas and NumPy.

It provides easy-to-grasp functions for computing several statistical
functions:

- ANOVAs: one- and two-ways, repeated measures, mixed, ancova
- Post-hocs tests and pairwise comparisons
- Robust correlations
- Partial correlation, repeated measures correlation and intraclass correlation
- Bayes Factor
- Tests for sphericity, normality and homoscedasticity
- Effect sizes (Cohen's d, Hedges'g, AUC, Glass delta, eta-square...)
- Parametric/bootstrapped confidence intervals around an effect size or a
  correlation coefficient
- Circular statistics
- Linear/logistic regression and mediation analysis

Pingouin is designed for users who want simple yet exhaustive statistical functions.

Documentation is available at https://raphaelvallat.github.io/pingouin/build/html/index.html.}

Name:           python-%{srcname}
Version:        0.2.1
Release:        1%{?dist}
Summary:        Pingouin: statistical package for Python

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/raphaelvallat/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pandas} >= 0.23
BuildRequires:  %{py3_dist numpy} >= 1.15
BuildRequires:  %{py3_dist scipy} >= 1.1
BuildRequires:  %{py3_dist scikit-learn}
BuildRequires:  %{py3_dist statsmodels}
%if %{with docs}
BuildRequires:  %{py3_dist sphinx}
%endif
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%if %{with docs}
%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.
%endif

%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info

%build
%py3_build

%if %{with docs}
sphinx-build-%{python3_version} -b html docs html
# rm -rf build/html/.doctrees
# rm -rf build/html/.buildinfo
%endif

%install
%py3_install

%check
%if %{with tests}
export PYTHONPATH=%{buildroot}%{python3_sitelib}
pytest-%{python3_version}
%endif

%files -n python3-%{srcname}
%license COPYING
%doc README.rst
%{python3_sitelib}/%{srcname}-%{version}-py3.?.egg-info
%{python3_sitelib}/%{srcname}

%if %{with docs}
%files doc
%license COPYING
%doc docs/build/html
%endif

%changelog
* Wed Nov 21 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.1-1
- Initial build
