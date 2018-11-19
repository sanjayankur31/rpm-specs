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

%global srcname uncertainpy

%global desc %{expand: \
A python toolbox for uncertainty quantification and sensitivity analysis

Uncertainpy is a python toolbox for uncertainty quantification and sensitivity
analysis of computational models and features of the models.

Uncertainpy is model independent and treats the model as a black box where the
model can be left unchanged. Uncertainpy implements both quasi-Monte Carlo
methods and polynomial chaos expansions using either point collocation or the
pseudo-spectral method. Both of the polynomial chaos expansion methods have
support for the rosenblatt transformation to handle dependent input parameters.

Uncertainpy is feature based, i.e., if applicable, it recognizes and calculates
the uncertainty in features of the model, as well as the model itself. Examples
of features in neuroscience can be spike timing and the action potential shape.

Uncertainpy is tailored towards neuroscience models, and comes with several
common neuroscience models and features built in, but new models and features
can easily be implemented. It should be noted that while Uncertainpy is
tailored towards neuroscience, the implemented methods are general, and
Uncertainpy can be used for many other types of models and features within
other fields.}

Name:           python-%{srcname}
Version:        1.1.4
Release:        1%{?dist}
Summary:        Uncertainty quantification and sensitivity analysis of computational models and their features

License:        GPLv3
URL:            https://pypi.python.org/pypi/%{srcname}
# Use github source for docs and tests
Source0:        https://github.com/simetenn/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

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
BuildRequires:  %{py3_dist tqdm}
BuildRequires:  %{py3_dist h5py}
BuildRequires:  %{py3_dist multiprocess}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist xvfbwrapper}
BuildRequires:  %{py3_dist six}
BuildRequires:  %{py3_dist neo}
BuildRequires:  %{py3_dist seaborn}
BuildRequires:  %{py3_dist quantities}
BuildRequires:  %{py3_dist click}

# Not yet packaged
BuildRequires:  %{py3_dist SALib}
BuildRequires:  %{py3_dist efel}
BuildRequires:  %{py3_dist elephant}
BuildRequires:  %{py3_dist chaospy}
uncertainpy_require = ["chaospy", "tqdm", "h5py", "multiprocess", "numpy",
                       "scipy", "seaborn", "matplotlib>=2", "xvfbwrapper", "six",
                       "SALib"]

efel_features = ["efel"]
network_features = ["elephant", "neo", "quantities"]

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
%license LICENSE.txt
%doc README.md
# %{python2_sitelib}/*
%endif

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.md
# %{python3_sitelib}/*
# %{_bindir}/sample-exec

%changelog
* Mon Nov 19 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.4-1
- Initial build
