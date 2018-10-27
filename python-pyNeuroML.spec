%global srcname pyNeuroML

%global with_py2 0

%global _description \
A single package in Python unifying scripts and modules for reading, writing, \
simulating and analysing NeuroML2/LEMS models.

Name:           python-%{srcname}
Version:        0.3.13
Release:        1%{?dist}
Summary:        Scripts and modules for reading, writing, simulating and analysing NeuroML2/LEMS models

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %{pypi_source}

BuildArch:      noarch

%description
%{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist lxml}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist asv}
BuildRequires:  %{py3_dist libNeuroML}
BuildRequires:  %{py3_dist neuromllite}
Requires:  %{py3_dist lxml}
Requires:  %{py3_dist matplotlib}
Requires:  %{py3_dist asv}
Requires:  %{py3_dist libNeuroML}
Requires:  %{py3_dist neuromllite}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{_description}

%package doc
Summary:    Documentation for %{srcname}

%description doc
%{_description}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist lxml}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist asv}
BuildRequires:  %{py2_dist libNeuroML}
BuildRequires:  %{py2_dist neuromllite}
Requires:  %{py2_dist lxml}
Requires:  %{py2_dist matplotlib}
Requires:  %{py2_dist asv}
Requires:  %{py2_dist libNeuroML}
Requires:  %{py2_dist neuromllite}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{_description}
%endif

%prep
%autosetup -n %{srcname}-%{version}

# remove egg info
rm -fv %{name}.egg-info

%build
%py3_build

%if %{with_py2}
%py2_build
%endif

# Make documentation
pushd doc && \
    make html SPHINXBUILD=sphinx-build-3 && \
    rm _build/html/.buildinfo -fv && \
popd || exit -1

%install
%py3_install

%if %{with_py2}
%py2_install
%endif

%check
nosetests-3

%if %{with_py2}
nosetests-2
%endif

%files -n python3-%{srcname}
%license LICENSE
%doc README.md AUTHORS
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/neuroml

%files doc
%license LICENSE
%doc README.md AUTHORS
%doc neuroml/examples doc/_build/html/

%if %{with_py2}
%files -n python2-%{srcname}
%license LICENSE
%doc README.md AUTHORS
%{python2_sitelib}/%{srcname}-*.egg-info/
%{python2_sitelib}/neuroml
%endif

%changelog
* Sat Oct 27 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.13-1
- Initial build
