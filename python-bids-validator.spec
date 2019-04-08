%global srcname bids-validator

%global desc %{expand: \
Validator for the Brain Imaging Data Structure}

Name:           python-%{srcname}
Version:        1.2.2
Release:        1%{?dist}
Summary:        Validator for the Brain Imaging Data Structure

License:        MIT
URL:            https://pypi.org/project/bids-validator/
Source0:        %pypi_source
Source1:        https://raw.githubusercontent.com/bids-standard/bids-validator/master/LICENSE

# https://github.com/bids-standard/bids-validator/issues/757: not included in pypi for some reason
Source2:        https://raw.githubusercontent.com/bids-standard/bids-validator/master/bids-validator/versioneer.py

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}


%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info

cp %{SOURCE1} .
cp %{SOURCE2} .

%build
%py3_build

%install
%py3_install

# No tests

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/bids_validator-%{version}-py3.?.egg-info
%{python3_sitelib}/bids_validator

%changelog
* Mon Apr 08 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.2-1
- Initial package
