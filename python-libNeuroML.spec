%global srcname libNeuroML

%global with_py2 0

%global _description \
This package provides Python libNeuroML, for working with neuronal models \
specified in NeuroML 2 (http://neuroml.org/neuromlv2).  NeuroML provides an \
object model for describing neuronal morphologies, ion channels, synapses and \
3D network structure.  Documentation is available at \
http://readthedocs.org/docs/libneuroml/en/latest/


Name:           python-%{srcname}
Version:        0.2.45
Release:        4%{?dist}
Summary:        Python libNeuroML for working with neuronal models specified in NeuroML

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %{pypi_source}
# These require a mongodb db set up, so we disable them
Patch0:         %{srcname}-%{version}-disable-mongodb-test.patch

BuildArch:      noarch

%description
%{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist lxml}
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist tables}
BuildRequires:  %{py3_dist jsonpickle}
BuildRequires:  %{py3_dist pymongo}
BuildRequires:  %{py3_dist sphinx}
Requires:  %{py3_dist lxml}
Requires:  %{py3_dist numpy}
Requires:  %{py3_dist tables}
Requires:  %{py3_dist jsonpickle}
Requires:  %{py3_dist pymongo}
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
BuildRequires:  %{py2_dist nose}
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist tables}
BuildRequires:  %{py2_dist jsonpickle}
BuildRequires:  %{py2_dist pymongo}
Requires:  %{py2_dist lxml}
Requires:  %{py2_dist numpy}
Requires:  %{py2_dist tables}
Requires:  %{py2_dist jsonpickle}
Requires:  %{py2_dist pymongo}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{_description}
%endif

%prep
%autosetup -p 1 -n %{srcname}-%{version}

# correct end of line encoding
sed -i 's/\r$//' neuroml/examples/test_files/tmp2.swc

# remove shebang
sed -i '1d' neuroml/nml/nml.py

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
* Fri Oct 26 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.45-4
- Correct license
- Remove bcond
- Remove hidden buildinfo file
- Correct end of line encoding
- Remove unneeded shebang (https://github.com/NeuralEnsemble/libNeuroML/issues/77)
- Add missing requires

* Thu Oct 25 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.45-3
- Correct doc build
- Temporarily use bcond

* Thu Oct 25 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.45-2
- Correct doc sub package name

* Thu Oct 25 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.45-1
- Initial build
