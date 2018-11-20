# Only Py3+

# disabled to begin with
%bcond_with tests

%global srcname configupdater
%global pretty_name ConfigUpdater

%global desc %{expand: \
The sole purpose of ConfigUpdater is to easily update an INI config file with
no changes to the original file except the intended ones. This means comments,
the ordering of sections and key/value-pairs as wells as their cases are kept
as in the original file. Thus ConfigUpdater provides complementary
functionality to Python’s ConfigParser which is primarily meant for reading
config files and writing new ones.

The key differences to ConfigParser are:

- minimal invasive changes in the update configuration file,
- proper handling of comments,
- only a single config file can be updated at a time,
- empty lines in values are not valid,
- the original case of sections and keys are kept,
- control over the position of a new section/key

Following features are deliberately not implemented:

- interpolation of values,
- propagation of parameters from the default section,
- conversions of values,
- passing key/value-pairs with default argument,
- non-strict mode allowing duplicate sections and keys.}

Name:           python-%{srcname}
Version:        0.3.2
Release:        1%{?dist}
Summary:        Parser like ConfigParser but for updating configuration files

License:        MIT
URL:            https://github.com/pyscaffold/configupdater
Source0:        %pypi_source %{pretty_name}

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
%autosetup -n %{pretty_name}-%{version}
rm -rf %{srcname}.egg-info

%build
%py3_build

%install
%py3_install

%check
%if %{with tests}
%{__python3} setup.py test
%endif

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.rst AUTHORS.rst CHANGELOG.rst CONTRIBUTING.rst

%changelog
* Tue Nov 20 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.2-1
- Initial build
