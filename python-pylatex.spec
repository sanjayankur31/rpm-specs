# Enabled by default
# If the package needs to download data for the test which cannot be done in
# koji, these can be disabled in koji by using `bcond_with` instead, but the
# tests must be validated in mock with network enabled like so:
# mock -r fedora-rawhide-x86_64 rebuild <srpm> --enable-network --rpmbuild-opts="--with tests"
%bcond_without tests

# Enabled by default
%bcond_without docs

%global pypi_name pylatex
%global fancy_name PyLaTeX

%global desc %{expand: \
PyLaTeX is a Python library for creating and compiling LaTeX files or snippets.
The goal of this library is being an easy, but extensible interface between
Python and LaTeX.}

Name:           python-%{pypi_name}
Version:        1.3.0
Release:        1%{?dist}
Summary:        A Python library for creating LaTeX files and snippets

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
License:        MIT
URL:            https://jeltef.github.io/PyLaTeX/
Source0:        https://github.com/JelteF/%{fancy_name}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

# Will also pull a lot of texlive, but that cannot be helpeb
Requires:       /usr/bin/latexmk
Requires:       /usr/bin/pdflatex
# From `ag packages.append``
Requires:       tex(fontenc.sty)
Requires:       tex(inputenc.sty)
Requires:       tex(lmodern.sty)
Requires:       tex(textcomp.sty)
Requires:       tex(lastpage.sty)
Requires:       tex(parskip.sty)
Requires:       tex(microtype.sty)
Requires:       tex(geometry.sty)
Requires:       tex(xcolor.sty)

%{?python_enable_dependency_generator}

%description
%{desc}

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist nose}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist quantities}
BuildRequires:  tex(siunitx.sty)
BuildRequires:  /usr/bin/pdflatex
BuildRequires:  tex(fontenc.sty)
BuildRequires:  tex(inputenc.sty)
BuildRequires:  tex(lmodern.sty)
BuildRequires:  tex(textcomp.sty)
BuildRequires:  tex(lastpage.sty)
BuildRequires:  tex(parskip.sty)
BuildRequires:  tex(microtype.sty)
BuildRequires:  tex(geometry.sty)
BuildRequires:  tex(xcolor.sty)
BuildRequires:  texlive-metafont
BuildRequires:  texlive-gsftopk
BuildRequires:  texlive-ec

%endif

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{desc}

%if %{with docs}
%package doc
Summary:        %{summary}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist ordered-set}
BuildRequires:  %{py3_dist sphinx_rtd_theme}

%description doc
Documentation for %{name}.
%endif

%prep
%autosetup -n %{fancy_name}-%{version}
rm -rf %{fancy_name}.egg-info

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%py3_build

pushd docs
    make SPHINXBUILD=sphinx-build-3 html
    rm -rf _build/html/.doctrees
    rm -rf _build/html/.buildinfo
popd

%install
%py3_install

%check
%if %{with tests}
# Run tests
nosetests-3 tests/*

# Test examples
pushd examples
for f in *.py; do
    %{__python3} $f
done
popd
%endif

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{fancy_name}-%{version}-py3.?.egg-info
%{python3_sitelib}/%{pypi_name}

%if %{with docs}
%files doc
%license LICENSE
%doc docs/_build/html examples
%endif

%changelog
* Mon Jun 17 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.0-1
- Initial rpm build
