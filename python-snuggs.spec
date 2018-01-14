%global srcname snuggs

Name:           python-%{srcname}
Version:        1.4.1
Release:        1%{?dist}
Summary:        Snuggs are s-expressions for Numpy

License:        MIT
URL:            https://github.com/mapbox/snuggs
# No tests in PyPI tarball.
Source0:        https://github.com/mapbox/snuggs/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%global _description \
Snuggs are sexpressions for NumPy. Snuggs wraps NumPy in expressions with the \
following syntax: expression "(" (operator | function) *arg ")" where \
arg = expression | name | number | string

%description %{_description}


%package -n     python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
BuildRequires:  python2-click
BuildRequires:  python2-numpy
BuildRequires:  python2-pyparsing

Requires:       python2-click
Requires:       python2-numpy
Requires:       python2-pyparsing

%description -n python2-%{srcname} %{_description}


%package -n     python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-click
BuildRequires:  python3-numpy
BuildRequires:  python3-pyparsing

Requires:       python3-click
Requires:       python3-numpy
Requires:       python3-pyparsing
%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname}-%{version}

# Remove bundled egg-info
rm -rf %{srcname}.egg-info

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install


%check
pytest-3 -v
pytest-2 -v

%files -n python2-%{srcname}
%doc README.rst AUTHORS.txt CHANGES.txt
%license LICENSE
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py?.?.egg-info

%files -n python3-%{srcname}
%doc README.rst AUTHORS.txt CHANGES.txt
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info


%changelog
* Sat Jan 13 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.4.1-1
- Initial package.
