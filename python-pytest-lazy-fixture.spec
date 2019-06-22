# Enabled by default
%bcond_without tests

%global pypi_name pytest-lazy-fixture

%global _description %{expand:
Use fixtures in pytest.mark.parametrize.}

Name:           python-%{pypi_name}
Version:        0.5.2
Release:        1%{?dist}
Summary:        Use fixtures in pytest.mark.parametrize

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %pypi_source %{pypi_name}

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}
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
PYTHONPATH="%{buildroot}/%{python3_sitelib}/" pytest-3
%endif

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/pytest_lazy_fixture-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/pytest_lazyfixture.py
%{python3_sitelib}/__pycache__/pytest_lazyfixture.cpython-%{python3_version_nodots}*

%changelog
* Sat Jun 22 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.2-1
- Initial package
