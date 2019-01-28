# Py2 only

# Require X, so we cannot run them
%bcond_with tests

%global srcname brian

%global desc %{expand: \
The brian simulator, version 1. Unless necessary, users should use Brian2.}

Name:           python-%{srcname}
Version:        1.4.4
Release:        1%{?dist}
Summary:        A clock-driven simulator for spiking neural networks, version 1


License:        CeCILL
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/brian-team/%{srcname}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  gsl-devel

%description
%{desc}

%{?python_enable_dependency_generator}

%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist numpy} >= 1.4.1
BuildRequires:  %{py2_dist scipy} >= 0.7.0
BuildRequires:  %{py2_dist matplotlib} >= 0.90.1
BuildRequires:  %{py2_dist sympy}
BuildRequires:  %{py2_dist nose}
Requires:  %{py2_dist sympy}

Suggests:       %{py2_dist ipython}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}

%prep
%autosetup -n %{srcname}-%{version}

# Remove unnecessary files
find . -name ".gitignore" -print -delete
rm -rvf %{srcname}.egg-info

# Correct shebang and encoding
find examples -name "*.py" -exec sed -i 's|^#!.*/usr/bin/env python|#!/usr/bin/python2|' '{}' \;
find brian -name "setup.py" -exec sed -i '/^#!.*\/usr\/bin\/env/ d' '{}' \;
find brian -name "*.py" -exec sed -i 's|^#!.*/usr/bin/env python|#!/usr/bin/python2|' '{}' \;
find examples -name "*.py" -exec sed -i 's/\r$//' '{}' \;
find examples -name "*.txt" -exec sed -i 's/\r$//' '{}' \;
find tutorials -name "*.py" -exec sed -i 's/\r$//' '{}' \;
find tutorials -name "*.txt" -exec sed -i 's/\r$//' '{}' \;
sed -i 's/\r$//' README.txt

%build
# Fail build if c extensions do not build correctly
export BRIAN_SETUP_FAIL_ON_ERROR=1
%py2_build

%install
%py2_install

%check
%if %{with tests}
PYTHONPATH=$RPM_BUILD_ROOT/%{python2_sitearch}/ %{__python2} -c 'from brian import *; brian_sample_run()'
%endif


%files -n python2-%{srcname}
%license license.txt
%doc README.txt
%doc examples tutorials
%{python2_sitearch}/%{srcname}
%{python2_sitearch}/%{srcname}-%{version}-py2.?.egg-info
%{python2_sitearch}/%{srcname}*unit*.py*

%changelog
* Sat Dec 29 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.4-1
- Initial build
