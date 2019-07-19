%bcond_with tests

%global srcname pingouin

%global _description %{expand:
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

Pingouin is designed for users who want simple yet exhaustive statistical
functions.

Documentation is available at
https://raphaelvallat.github.io/pingouin/build/html/index.html.}

Name:           python-%{srcname}
Version:        0.2.7
Release:        1%{?dist}
Summary:        Statistical package for Python

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/raphaelvallat/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel

BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist seaborn}

%if %{with tests}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-remotedata}
# Need packaging
BuildRequires:  %{py3_dist pytest-sugar}
BuildRequires:  %{py3_dist openpyxl}
BuildRequires:  %{py3_dist mpmath}
BuildRequires:  %{py3_dist scikit-learn}
# Only required and works in TRAVIS, so not needed here
# BuildRequires:  python3-pytest-travis-fold}
%endif

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%package doc
Summary:        %{summary}
BuildRequires:  %{py3_dist numpydoc}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-bootstrap-theme}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info

%build
%py3_build

PYTHONPATH=. sphinx-build-%{python3_version} -b html docs html
rm -rf html/.doctrees
rm -rf html/.buildinfo
rm -rf html/.nojekyll

%install
%py3_install

%check
%if %{with tests}
export PYTHONPATH=%{buildroot}%{python3_sitelib}
pytest-%{python3_version}
%endif

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{srcname}

%files doc
%license LICENSE
%doc html

%changelog
* Fri Jul 19 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.7-1
- Initial build
