# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# Failing tests
# https://github.com/INCF/nineml-python/issues/40
%bcond_with tests

# Docs fail to build:
# https://github.com/INCF/nineml-python/issues/41
%bcond_with api_docs

# MPI versions of h5py required also:
# https://bugzilla.redhat.com/show_bug.cgi?id=1649939

%global srcname nineml

%global desc %{expand: \
NineML (9ML) is a language for describing the dynamics and connectivity of
neuronal network simulations (http://nineml.net), which is defined by the
NineML specification.

The NineML Python Library is a software package written in Python, which maps
the NineML object model onto Python classes for convenient creation,
manipulation and validation of NineML models, as well as handling their
serialisation to and from XML, JSON, YAML, and HDF5.

Links
- Online documentation: http://nineml-python.readthedocs.org
- Mailing list: NeuralEnsemble Google Group
- Issue tracker: https://github.com/INCF/nineml-python/issues
}

Name:           python-%{srcname}
Version:        1.0
Release:        1%{?dist}
Summary:        A tool for reading, writing and generally working with 9ML


License:        BSD
URL:            https://github.com/INCF/nineml-python
# Include tests and license
Source0:        https://github.com/INCF/%{srcname}-python/archive/%{version}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  hdf5-devel

%description
%{desc}

%if %{with py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist nose}
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist sympy}
BuildRequires:  %{py2_dist h5py}
BuildRequires:  %{py2_dist pyyaml}
BuildRequires:  %{py2_dist lxml}
Requires:       %{py2_dist sympy}
Requires:       %{py2_dist h5py}
Requires:       %{py2_dist pyyaml}
Requires:       %{py2_dist lxml}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx_rtd_theme}
BuildRequires:  %{py3_dist numpydoc}
BuildRequires:  %{py3_dist sympy}
BuildRequires:  %{py3_dist h5py}
BuildRequires:  %{py3_dist pyyaml}
BuildRequires:  %{py3_dist lxml}
Requires:       %{py3_dist sympy}
Requires:       %{py3_dist h5py}
Requires:       %{py3_dist pyyaml}
Requires:       %{py3_dist lxml}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%package doc
Summary:    %{summary}

%description doc
Documentatation for %{name}.


%prep
%autosetup -n %{srcname}-python-%{version}
rm -rf %{srcname}.egg-info

sed -i '/^#!\/usr\/bin\/env python/ d' nineml/abstraction/connectionrule/base.py

# https://github.com/INCF/nineml-python/issues/40
sed -i 's/sympy.parsing.sympy_tokenize/tokenize/' nineml/abstraction/expressions/parser.py

%build
%py3_build

%if %{with py2}
%py2_build
%endif

%if %{with api_docs}
pushd doc
    make html
    rm -rfv build/html/.buildinfo
    rm -rfv build/html/.doctrees
popd
%endif

%install
%if %{with py2}
%py2_install
%endif

%py3_install

%check
%if %{with tests}
%if %{with py2}
nosetests-%{python2_version}
%endif
nosetests-%{python3_version}
%endif

%if %{with py2}
%files -n python2-%{srcname}
%license LICENSE.txt
%doc README.rst
%{python2_sitelib}/%{srcname}-%{version}-py2.?.egg-info
%{python2_sitelib}/%{srcname}
%endif

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{srcname}-%{version}-py3.?.egg-info
%{python3_sitelib}/%{srcname}

%files doc
%license LICENSE.txt
%doc examples
%if %{with api_docs}
%doc doc/build/html
%endif

%changelog
* Wed Nov 14 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.0-1
- Initial package
