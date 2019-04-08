%global srcname versioneer

%global desc %{expand: \
Easy VCS-based management of project version strings}

Name:           python-%{srcname}
Version:        0.18
Release:        1%{?dist}
Summary:        Easy VCS-based management of project version strings

License:        Public Domain
URL:            https://pypi.org/project/versioneer/
Source0:        %pypi_source

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

%build
%py3_build

%install
%py3_install

%check
# Do not run flake tests
%{__python3} setup.py make_versioneer
%{__python3} -m unittest test
%{__python3} test/git/test_git.py -v
%{__python3} test/git/test_invocations.py -v

%files -n python3-%{srcname}
%doc README.md details.md developers.md
%{python3_sitelib}/%{srcname}-%{version}-py3.?.egg-info
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/__pycache__/%{srcname}.*

%changelog
* Mon Apr 08 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.18-1
- Initial rpm
