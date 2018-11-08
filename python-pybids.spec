%global commit e35ced6e5161038c9638414fbbfb0e8c96bc9a8e
%global shortcommit %(c=%{commit}; echo ${c:0:7})


# Python nibabel is py3 only even in F29, so we do not provide this package for
# Py2 either.
%global with_py2 0

# Lots of tests fail, even in a clean pip environment
%global run_tests 1

%global _description %{expand: \
PyBIDS is a Python module to interface with datasets conforming BIDS.
}

%global srcname     pybids

Name:       python-%{srcname}
Version:    0.6.5
Release:    1.git%{shortcommit}%{?dist}
Summary:    Interface with datasets conforming to BIDS

License:    MIT
URL:        http://bids.neuroimaging.io
Source0:    https://github.com/INCF/%{srcname}/archive/%{commit}/%{srcname}-%{shortcommit}.tar.gz


BuildArch:      noarch

%description
%{_description}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:    Interface with datasets conforming to BIDS
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist setuptools}
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist grabbit} >= 0.2.5
BuildRequires:  %{py2_dist num2words}
BuildRequires:  %{py2_dist nibabel}
BuildRequires:  %{py2_dist patsy}
BuildRequires:  %{py2_dist scipy}
Requires:       %{py2_dist grabbit} >= 0.2.5
Requires:       %{py2_dist pandas}
Requires:       %{py2_dist six}
Requires:       %{py2_dist num2words}
Requires:       %{py2_dist duecredit}
Requires:       %{py2_dist nibabel}
Requires:       %{py2_dist patsy}
Requires:       %{py2_dist scipy}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{_description}
%endif


%package -n python3-%{srcname}
Summary:    Interface with datasets conforming to BIDS
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist grabbit} >= 0.2.5
BuildRequires:  %{py3_dist num2words}
BuildRequires:  %{py3_dist duecredit}
BuildRequires:  %{py3_dist nibabel}
BuildRequires:  %{py3_dist patsy}
BuildRequires:  %{py3_dist scipy}
Requires:       %{py3_dist grabbit} >= 0.2.5
Requires:       %{py3_dist pandas}
Requires:       %{py3_dist six}
Requires:       %{py3_dist num2words}
Requires:       %{py3_dist duecredit}
Requires:       %{py3_dist nibabel}
Requires:       %{py3_dist patsy}
Requires:       %{py3_dist scipy}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{_description}

%package doc
Summary:    Interface with datasets conforming to BIDS
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx_rtd_theme}
BuildRequires:  %{py3_dist m2r}
BuildRequires:  %{py3_dist numpydoc}

%description doc
Description for %{name}.

%prep
%autosetup -n %{srcname}-%{commit}

# stray backup file?
rm -rf *.egg-info


%build
%if %{with_py2}
%py2_build
%endif
%py3_build

pushd doc && \
    sphinx-build-3 . html
    rm -fv .buildinfo
popd


%install
%if %{with_py2}
%py2_install
%endif
%py3_install

%check
# test_split requires python-patsh 0.5.1
# https://bugzilla.redhat.com/show_bug.cgi?id=1647629
%if %{run_tests}
%if %{with_py2}
PYTHONPATH=. py.test -s -v -k-test_split .
%endif
PYTHONPATH=. py.test-3 -s -v -k-test_split .
%endif

%if %{with_py2}
%files -n python2-%{srcname}
%doc README.md
%license LICENSE
%{python2_sitelib}/%{srcname}-0+unknown-py2.?.egg-info
%{python2_sitelib}/bids/
%endif

%files -n python3-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{srcname}-0+unknown-py3.?.egg-info
%{python3_sitelib}/bids/

%files doc
%doc examples/ doc/html
%license LICENSE

%changelog
* Wed Nov 07 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6.5-1.gite35ced6
- Use latest git snapshot that fixes tests
- Add documentation and examples in subpackage

* Wed Nov 07 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6.3-2
- Enable tests now that duecredit is available in rawhide
- Disable py2 build since python-nibabel is only py3 even in F29

* Fri Jul 20 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6.3-1
- Update to latest release
- Use py.test
- Disable tests until nibabel is fixed

* Mon Jan 15 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-2
- Use github source for license and test suite
- Fix requires and build requires

* Fri Jan 12 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-1
- Initial build
