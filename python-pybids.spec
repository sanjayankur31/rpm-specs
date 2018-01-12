%global srcname     pybids

Name:       python-%{srcname}
Version:    0.4.2
Release:    1%{?dist}
Summary:    Interface with datasets conforming to BIDS

License:    MIT
URL:        http://bids.neuroimaging.io
Source0:    https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/INCF/pybids/master/LICENSE


BuildArch:      noarch

%description
PyBIDS is a Python module to interface with datasets conforming BIDS.

%package -n python2-%{srcname}
Summary:        %{sum}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist numpy scipy}
Requires:  %{py2_dist numpy scipy}

Recommends:   python2-scipy python2-h5py python2-igor
# Not in fedora yet, to be updated as these are added
# Recommends:   python2-klusta python2-nixio python2-stfio

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
PyBIDS is a Python module to interface with datasets conforming BIDS.


%package -n python3-%{srcname}
Summary:        %{sum}
BuildRequires:  python3-devel
BuildRequires:  %{py2_dist numpy scipy}
Requires:  %{py2_dist numpy scipy}
# Not in fedora yet, to be updated as these are added
# Recommends:   python3-klusta python3-nixio python3-stfio
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
PyBIDS is a Python module to interface with datasets conforming BIDS.

%prep
%autosetup -n %{srcname}-%{version}
cp %{SOURCE1} .

# stray backup file?
rm -rf *.egg-info

%build
%py2_build
%py3_build


%install
%py2_install
%py3_install

# no tests here

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
* Fri Jan 12 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-1
- Initial build
