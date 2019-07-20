# Needs matplotlib-scalebar so currently disabled
%bcond_with tests

%global pypi_name netpyne

%global _description %{expand:
NetPyNE is a python package to facilitate the development, parallel simulation
and analysis of biological neuronal networks using the NEURON simulator.

For more details, installation instructions, documentation, tutorials, forums,
videos and more, please visit: www.netpyne.org

This package is developed and maintained by the Neurosim lab
(www.neurosimlab.org)}



Name:           python-%{pypi_name}
Version:        0.9.2
Release:        1%{?dist}
Summary:        Develop, simulate and analyse biological neuronal networks in NEURON

# stackedBarGraph.py is GPLv3+, but others are all MIT
License:        MIT and GPLv3+
URL:            https://pypi.org/project/%{pypi_name}
Source0:        https://github.com/Neurosim-lab/%{pypi_name}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist future}
BuildRequires:  %{py3_dist h5py}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist neuron}

# Needs packaging
# BuildRequires:  %%{py3_dist matplotlib-scalebar}

# For documentation
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-rtd-theme}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %_description

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

# Remove hidden files that are used by the OSB build service tests
rm -f examples/NeuroMLImport/test/.test*

# wrong end of line encoding
find examples -type f -exec sed -i 's/\r$//' '{}' \;
find examples -type f -exec chmod -x '{}' \;

# Remove shebang
sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' netpyne/support/stackedBarGraph.py

%build
%py3_build

sphinx-build-3 -b html doc/source/ html
rm -rf html/{.doctrees,.buildinfo} -vf
find html -type f -exec sed -i 's/\r$//' '{}' \;

%install
%py3_install

%check
%if %{with tests}
%{__python3} setup.py test
%endif

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{pypi_name}

%files doc
%license LICENSE
%doc html examples

%changelog
* Sat Jul 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.2-1
- Update license
- Remove hidden files

* Fri Jul 19 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.2-1
- Initial build
