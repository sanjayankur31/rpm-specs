# Docs fail to build. Need to be reported
%bcond_with docs

%global pypi_name elephant

Name:           python-%{pypi_name}
Version:        0.6.2
Release:        1%{?dist}
Summary:        Elephant is a package for analysis of electrophysiology data in Python
BuildArch:      noarch

License:        BSD
URL:            http://neuralensemble.org/elephant
Source0:        https://github.com/neuralensemble/%{pypi_name}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3dist(neo)
BuildRequires:  python3dist(nose)
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(pandas)
BuildRequires:  python3dist(quantities)
BuildRequires:  python3dist(scikit-learn)
BuildRequires:  python3dist(scipy)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(six)

%if %{with docs}
BuildRequires:  python3dist(nbsphinx)
BuildRequires:  python3dist(numpydoc)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  python3dist(sphinx-gallery)
BuildRequires:  python3dist(sphinxcontrib-bibtex)
%endif

%description
Elephant - Electrophysiology Analysis Toolkit Elephant is a package for the
analysis of neurophysiology data, based on Neo.

# Add for F29
%{?python_enable_dependency_generator}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}


%description -n python3-%{pypi_name}
Elephant - Electrophysiology Analysis Toolkit Elephant is a package for the
analysis of neurophysiology data, based on Neo.

%if %{with docs}
%package -n python-%{pypi_name}-doc
Summary:        elephant documentation

%description -n python-%{pypi_name}-doc
Documentation for elephant

%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

for lib in $(find . -type f -name "*.py"); do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

# remove neo version constraints
sed -i 's/neo.*/neo/' requirements.txt

%build
%py3_build

%if %{with docs}
pushd doc
    make SPHINXBUILD=sphinx-build-3 html
    rm -rf build/.doctrees
    rm -rf build/.buildinfo
popd
%endif

%install
%py3_install

%check
# Ignore tests:
# test_unitary_event_analysis: tries to download data
# test_cubic: seems to fail on 32 bit machines. NEEDS TO BE REPORTED UPSTREAM with more information.
nosetests-3 -I test_unitary_event_analysis.py -I test_cubic.py

%files -n python3-%{pypi_name}
%license LICENSE.txt elephant/spade_src/LICENSE
%doc README.rst elephant/current_source_density_src/README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with docs}
%files -n python-%{pypi_name}-doc
%doc doc/_build/html
%license LICENSE.txt elephant/spade_src/LICENSE
%endif

%changelog
* Fri Jun 07 2019 Luis Bazan <lbazan@fedoraproject.org - 0.6.2-1
- Initial package.
