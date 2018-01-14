%global srcname affine

Name:           python-%{srcname}
Version:        2.1.0
Release:        1%{?dist}
Summary:        Matrices describing affine transformation of the plane

License:        BSD
URL:            https://github.com/sgillies/affine
Source0:        https://files.pythonhosted.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz
# https://github.com/sgillies/affine/pull/34
Patch0001:      https://github.com/sgillies/affine/commit/238317e9a99a56b02173ad6a2454e90a30c461b9.patch
Patch0002:      https://github.com/sgillies/affine/commit/6b77ecbaea177b680f99da49807616f3dcdd5068.patch

BuildArch:      noarch
 
%global _description \
Matrices describing affine transformation of the plane. The Affine package is \
derived from Casey Duncan's Planar package. 

%description %{_description}


%package -n     python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
 
%description -n python2-%{srcname} %{_description}


%package -n     python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname}-%{version} -p1

# Remove bundled egg-info
rm -rf %{srcname}.egg-info


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install


%check
PYTHONPATH="%{buildroot}%{python3_sitearch}" \
    pytest-3 -v --pyargs affine
PYTHONPATH="%{buildroot}%{python2_sitearch}" \
    pytest-2 -v --pyargs affine


%files -n python2-%{srcname}
%doc README.rst
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py?.?.egg-info

%files -n python3-%{srcname}
%doc README.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info


%changelog
* Sat Jan 13 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.1.0-1
- Initial package.
