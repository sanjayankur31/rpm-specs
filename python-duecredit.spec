%global srcname duecredit

%global _description \
duecredit is being conceived to address the problem of inadequate citation of \
scientific software and methods, and limited visibility of donation requests \
for open-source software. \
\
It provides a simple framework (at the moment for Python only) to embed \
publication or other references in the original code so they are automatically \
collected and reported to the user at the necessary level of reference detail, \
i.e. only references for actually used functionality will be presented back if \
software provides multiple citeable implementations.

Name:           python-%{srcname}
Version:        0.6.4
Release:        1%{?dist}
Summary:        Automated collection and reporting of citations for used software/methods/datasets

License:        BSD
URL:            https://github.com/%{srcname}/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch

%description
%{_description}

%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
# Test deps
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist six}
BuildRequires:  %{py2_dist nose}
BuildRequires:  %{py2_dist citeproc-py}
BuildRequires:  %{py2_dist mock}
BuildRequires:  %{py2_dist requests}
BuildRequires:  %{py2_dist scipy}
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist scikit-learn}
BuildRequires:  %{py2_dist statsmodels}
BuildRequires:  %{py2_dist pandas}
BuildRequires:  %{py2_dist matplotlib}
Requires:       %{py2_dist six}
Requires:       %{py2_dist citeproc-py}
Requires:       %{py2_dist requests}

%description -n python2-%{srcname}
%{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
# Test deps
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist six}
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist citeproc-py}
BuildRequires:  %{py3_dist mock}
BuildRequires:  %{py3_dist requests}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scikit-learn}
BuildRequires:  %{py3_dist statsmodels}
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist matplotlib}
Requires:       %{py3_dist six}
Requires:       %{py3_dist citeproc-py}
Requires:       %{py3_dist requests}

%description -n python3-%{srcname}
%{_description}

%prep
%autosetup -n %{srcname}-%{version}
rm -rfv *egg-info

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
nosetests-%{python2_version} -v
nosetests-%{python3_version} -v

%files -n python2-%{srcname}
%doc examples README.md CHANGELOG.md CONTRIBUTING.md
%license LICENSE
%{python2_sitelib}/%{srcname}*

%files -n python3-%{srcname}
%license LICENSE
%{_bindir}/%{srcname}
%{python3_sitelib}/%{srcname}*

%changelog
* Wed Aug 22 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6.4-1
- Update to new version
- Only install py3 bin
- Use macro for description
- use pydist macros
- use pypi_source macro

* Wed Nov 11 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.4.4.1-1
- Initial package
