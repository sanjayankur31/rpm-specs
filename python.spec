# Enabled by default
# If the package needs to download data for the test which cannot be done in
# koji, these can be disabled in koji by using `bcond_with` instead, but the
# tests must be validated in mock with network enabled like so:
# mock -r fedora-rawhide-x86_64 rebuild <srpm> --enable-network --rpmbuild-opts="--with tests"
%bcond_without tests

# Enabled by default
%bcond_without docs

%global pypi_name example

%global desc %{expand: \
Add a description here.}

Name:           python-%{pypi_name}
Version:        1.2.3
Release:        1%{?dist}
Summary:        An example python module

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
License:
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %pypi_source %{pypi_name}

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
# DELETE ME: Use standard names
BuildRequires:  %{py3_dist ...}

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{desc}

%if %{with docs}
%package doc
Summary:        %{summary}
BuildRequires:  %{py3_dist sphinx}

%description doc
Documentation for %{name}.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%py3_build

pushd doc
    make SPHINXBUILD=sphinx-build-3 html
    rm -rf _build/html/.doctrees
    rm -rf _build/html/.buildinfo
popd

%install
%py3_install

%check
%if %{with tests}
%{__python3} setup.py test
%endif

%files -n python3-%{pypi_name}
%license COPYING
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py3.?.egg-info
%{python3_sitelib}/%{pypi_name}

%if %{with docs}
%files doc
%license COPYING
%doc doc/_build/html
%endif

%changelog
