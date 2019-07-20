%global commit c278f7bae33757e52df554c93a83dfc117119da3
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%bcond_without tests

%global pypi_name NeuroMLlite

%global _description %{expand:
A common framework for reading/writing/generating network specifications.

Work in progress.  For the background to this see here:
https://github.com/NeuroML/NetworkShorthand.}

Name:           python-%{pypi_name}
Version:        0.1.8
Release:        20190720git%{shortcommit}%{?dist}
Summary:        A common framework for reading/writing/generating network specifications

License:        LGPLv3
URL:            https://pypi.org/pypi/%{pypi_name}
Source0:        https://github.com/NeuroML/%{pypi_name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# https://github.com/NeuroML/NeuroMLlite/pull/4
Patch0:         0001-Correct-print-method-call.patch
BuildArch:      noarch

%{?python_enable_dependency_generator}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  git-core
# Required for tests
BuildRequires:  %{py3_dist neuron}
BuildRequires:  %{py3_dist pyneuroml}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist PyQt5}
BuildRequires:  %{py3_dist tables}
BuildRequires:  %{py3_dist h5py}
BuildRequires:  %{py3_dist pyelectro}
BuildRequires:  %{py3_dist graphviz}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist netpyne}

Requires:  %{py3_dist neuron}
Requires:  %{py3_dist pyneuroml}
Requires:  %{py3_dist numpy}
Requires:  %{py3_dist PyQt5}
Requires:  %{py3_dist tables}
Requires:  %{py3_dist h5py}
Requires:  %{py3_dist pyelectro}
Requires:  %{py3_dist graphviz}
Requires:  %{py3_dist scipy}
Requires:  %{py3_dist matplotlib}
Requires:  %{py3_dist netpyne}

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{commit} -S git -p1
rm -rf %{pypi_name}.egg-info

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%py3_build

%install
%py3_install

%check
%if %{with tests}
%{__python3} setup.py test
%endif

%files -n python3-%{pypi_name}
%license LICENSE.lesser
%doc README.md
%{_bindir}/nmllite-ui
%{python3_sitelib}/neuromllite-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/neuromllite

%changelog
* Sat Jul 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.8-20190720gitc278f7ba
- initial build
