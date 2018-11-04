# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
%if 0%{?fedora} < 30
%global with_py2 1
%else
%global with_py2 0
%endif

%global srcname duecredit

%global _description %{expand: \
duecredit is being conceived to address the problem of inadequate citation of
scientific software and methods, and limited visibility of donation requests
for open-source software.

It provides a simple framework (at the moment for Python only) to embed
publication or other references in the original code so they are automatically
collected and reported to the user at the necessary level of reference detail,
i.e. only references for actually used functionality will be presented back if
software provides multiple citeable implementations.}

Name:           python-%{srcname}
Version:        0.6.4
Release:        2%{?dist}
Summary:        Automated collection and reporting of citations

License:        BSD
URL:            https://github.com/%{srcname}/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch

BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist six}
BuildRequires:  %{py3_dist lxml}
BuildRequires:  %{py3_dist citeproc-py}
BuildRequires:  %{py3_dist requests}
BuildRequires:  %{py3_dist vcrpy}
BuildRequires:  %{py3_dist contextlib2}

Requires:       %{py3_dist six}
Requires:       %{py3_dist citeproc-py}
Requires:       %{py3_dist requests}

%description
%{_description}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
# Test deps
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist six}
BuildRequires:  %{py2_dist lxml}
BuildRequires:  %{py2_dist citeproc-py}
BuildRequires:  %{py2_dist requests}
BuildRequires:  %{py2_dist vcrpy}
BuildRequires:  %{py2_dist contextlib2}

Requires:       %{py2_dist six}
Requires:       %{py2_dist citeproc-py}
Requires:       %{py2_dist requests}

%description -n python2-%{srcname}
%{_description}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel

%description -n python3-%{srcname}
%{_description}

%package doc
Summary:        Documentation for %{name}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version}
rm -rfv *egg-info

%build
%if %{with_py2}
%py2_build
%endif

%py3_build

%install
%if %{with_py2}
%py2_install
%endif

%py3_install

%check
# Skip tests requiring network
%if %{with_py2}
PYTHONPATH=%{buildroot}/%{python2_sitelib} pytest-2 duecredit/tests --ignore=duecredit/tests/test_io.py
%endif

PYTHONPATH=%{buildroot}/%{python3_sitelib} pytest-3 duecredit/tests --ignore=duecredit/tests/test_io.py

%if %{with_py2}
%files -n python2-%{srcname}
%doc examples README.md CHANGELOG.md CONTRIBUTING.md
%license LICENSE
%{python2_sitelib}/%{srcname}*
%endif

%files -n python3-%{srcname}
%license LICENSE
%{_bindir}/%{srcname}
%{python3_sitelib}/%{srcname}*

%files doc
%license LICENSE
%doc examples/


%changelog
* Sun Nov 04 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6.4-2
- Shorten summary
- Remove stray empty line in description
- Improve description for doc package

* Sat Nov 03 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6.4-1
- Update to new version
- Only install py3 bin
- Use macro for description
- use pydist macros
- use pypi_source macro

* Wed Nov 11 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.4.4.1-1
- Initial package
