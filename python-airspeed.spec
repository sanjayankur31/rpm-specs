%bcond_without tests

%global pypi_name airspeed

%global _description %{expand:
Airspeed is a powerful and easy-to-use templating engine for Python that aims
for a high level of compatibility with the popular Velocity library for Java.

- Compatible with Velocity templates
- Compatible with Python 2.6 and greater, including Jython
- Features include macros definitions, conditionals, sub-templates and much more
- Airspeed is already being put to serious use
- Comprehensive set of unit tests; the entire library was written test-first
- Reasonably fast
- A single Python module of a few kilobytes, and not the 500kb of Velocity
- Liberal licence (BSD-style)}

Name:           python-%{pypi_name}
Version:        0.5.11
Release:        1%{?dist}
Summary:        A lightweight template engine compatible with Velocity

License:        BSD
URL:            https://pypi.org/pypi/%{pypi_name}
Source0:        https://github.com/purcell/%{pypi_name}/archive/%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist cachetools}
BuildRequires:  %{py3_dist six}
%if %{with tests}
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist coverage}
%endif
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%py3_build

%install
%py3_install

%check
%if %{with tests}
%{__python3} setup.py test
%endif

%files -n python3-%{pypi_name}
%license LICENCE
%doc README.md
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{pypi_name}

%changelog
* Sat Jul 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.11-1
- Initial build
