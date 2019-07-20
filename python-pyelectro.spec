%bcond_without tests

%global commit 7a64bc7fb131fbc4ee12a457d8e7355c66b3dd0c
%global shortcommit %(c=%{commit}; echo ${c:0:7}) 

%global pypi_name pyelectro

%global _description %{expand:
Tool for analysis of electrophysiology in Python.

This package was originally developed by Mike Vella. This has been updated by
Padraig Gleeson and others (and moved to NeuralEnsemble) to continue
development of pyelectro and Neurotune for use in OpenWorm, Open Source Brain
and other projects.}

Name:           python-%{pypi_name}
Version:        0.1.9
Release:        20190720git%{shortcommit}%{?dist}
Summary:        A library for analysis of electrophysiological data

License:        BSD
URL:            https://github.com/NeuralEnsemble/%{pypi_name}
Source0:        https://github.com/NeuralEnsemble/%{pypi_name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel

# For documentation
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist mock}

Requires:       %{py3_dist scipy}
Requires:       %{py3_dist numpy}
Requires:       %{py3_dist matplotlib}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{pypi_name}-%{commit}
rm -rf %{pypi_name}.egg-info

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%py3_build

make -C doc SPHINXBUILD=sphinx-build-3 html
rm -rf doc/_build/html/{.doctrees,.buildinfo} -vf

%install
%py3_install

%check
%if %{with tests}
nosetests-%{python3_version}
%endif

%files -n python3-%{pypi_name}
%doc README.md
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{pypi_name}

%files doc
%doc doc/_build/html

%changelog
* Sat Jul 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.9-20190720git7a64bc7
- Initial build
