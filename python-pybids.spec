%global srcname     pybids

Name:       python-%{srcname}
Version:    0.4.2
Release:    2%{?dist}
Summary:    Interface with datasets conforming to BIDS

License:    MIT
URL:        http://bids.neuroimaging.io
Source0:    https://github.com/INCF/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz


BuildArch:      noarch

%description
PyBIDS is a Python module to interface with datasets conforming BIDS.

%package -n python2-%{srcname}
Summary:        %{sum}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist setuptools}
BuildRequires:  %{py2_dist sphinx}
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist grabbit}
Requires:       %{py2_dist grabbit}
Requires:       %{py2_dist pandas}
Requires:       %{py2_dist six}

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
PyBIDS is a Python module to interface with datasets conforming BIDS.


%package -n python3-%{srcname}
Summary:        %{sum}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist grabbit}
Requires:  %{py3_dist grabbit}
Requires:       %{py3_dist pandas}
Requires:       %{py3_dist six}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
PyBIDS is a Python module to interface with datasets conforming BIDS.

%prep
%autosetup -n %{srcname}-%{version}

# stray backup file?
rm -rf *.egg-info

%build
%py2_build
%py3_build


%install
%py2_install
%py3_install

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{srcname}
%doc README.md
%license LICENSE
%{python2_sitelib}/%{srcname}-%{version}-py?.?.egg-info
%{python2_sitelib}/bids/

%files -n python3-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info
%{python3_sitelib}/bids/

%changelog
* Mon Jan 15 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-2
- Use github source for license and test suite
- Fix requires and build requires

* Fri Jan 12 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-1
- Initial build
