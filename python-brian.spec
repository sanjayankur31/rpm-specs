# Py2 only

# Tests take a long time on koji. Have been tested locally, and issues
# submitted upstream
%bcond_with tests

%global srcname brian

# Documents disabled for the moment
%bcond_with docs

%global desc %{expand: \
Brian2 is a simulator for spiking neural networks available on almost all
platforms. The motivation for this project is that a simulator should not only
save the time of processors, but also the time of scientists.

It is the successor of Brian1 and shares its approach of being highly flexible
and easily extensible. It is based on a code generation framework that allows
to execute simulations using other programming languages and/or on different
devices.

Please report issues to the github issue tracker
(https://github.com/brian-team/brian2/issues) or to the brian support mailing
list (http://groups.google.com/group/briansupport/)

Documentation for Brian2 can be found at http://brian2.readthedocs.org}

Name:           python-%{srcname}
Version:        1.4.4
Release:        1%{?dist}
Summary:        A clock-driven simulator for spiking neural networks, version 1


License:        CeCILL
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/brian-team/%{srcname}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++ gcc
BuildRequires:  gsl-devel

%description
%{desc}

%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist numpy} >= 1.4.1
BuildRequires:  %{py2_dist scipy} >= 0.7.0
BuildRequires:  %{py2_dist matplotlib} >= 0.90.1
BuildRequires:  %{py2_dist sympy}
BuildRequires:  %{py2_dist nose}

Suggests:       %{py2_dist ipython}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}

%package doc
Summary:    %{summary}
BuildArch:  noarch

%description doc
Documentation and examples for %{name}.


%prep
%autosetup -n %{srcname}-%{version}

# Remove unnecessary files
find . -name ".gitignore" -print -delete
rm -rvf %{srcname}.egg-info
# Correct shebang for examples
find examples -name "*.py" -print -exec sed -i 's|^#!/usr/bin/env python|#!/usr/bin/python3|' '{}' \;


%build
# Fail build if c extensions do not build correctly
export BRIAN_SETUP_FAIL_ON_ERROR=1
%py2_build

%if %{with docs}
# Build documentation
PYTHONPATH=.
sphinx-build-3 docs_sphinx html
%endif



%install
%py2_install

%check
%if %{with tests}
PYTHONPATH=$RPM_BUILD_ROOT/%{python2_sitearch}/ %{__python2} -c 'import brian2; brian2.test()'
%endif


%files -n python2-%{srcname}
%license LICENSE
%doc README.rst AUTHORS
%{python2_sitearch}/%{srcname}
%{python2_sitearch}/%{srcname}-%{version}-py2.?.egg-info

%files doc
%license LICENSE
%doc examples tutorials
%if %{with docs}
%doc html
%endif

%changelog
* Sat Dec 29 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.4-1
- Initial build
