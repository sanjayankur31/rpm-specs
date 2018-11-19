# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2 0
%endif

# disabled to begin with
%bcond_with tests

%global srcname SALib

%global desc %{expand: \
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
Version:        1.1.3
Release:        1%{?dist}
Summary:        Sensitivity Analysis Library in Python

License:        MIT
URL:            http://salib.github.io/SALib/
Source0:        %pypi_source

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist numpy} >= 1.9.0
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib} >= 1.4.3
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist pytest}

# Not yet packaged
BuildRequires:  %{py3_dist pyscaffold}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}


%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info

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
%files -n python2-%{srcname}
%license LICENSE.md
%doc README.md README-advanced.md CHANGES.rst CITATIONS.rst AUTHORS.rst
# %{python2_sitelib}/*
%endif

%files -n python3-%{srcname}
%license LICENSE.md
%doc README.md README-advanced.md CHANGES.rst CITATIONS.rst AUTHORS.rst
# %{python3_sitelib}/*
# %{_bindir}/sample-exec

%changelog
* Mon Nov 19 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.3-1
- Initial build
