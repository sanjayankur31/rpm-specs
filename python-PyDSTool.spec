# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# Enabled by default
# If the package needs to download data for the test which cannot be done in
# koji, these can be disabled in koji by using `bcond_with` instead, but the
# tests must be validated in mock with network enabled like so:
# mock -r fedora-rawhide-x86_64 rebuild <srpm> --enable-network --rpmbuild-opts="--with tests"
%bcond_without tests

%global pypi_name PyDSTool

%global desc %{expand: \
PyDSTool is a sophisticated & integrated simulation and analysis environment
for dynamical systems models of physical systems (ODEs, DAEs, maps, and hybrid
systems).

PyDSTool is platform independent, written primarily in Python with some
underlying C and Fortran legacy code for fast solving. It makes extensive use
of the numpy and scipy libraries. PyDSTool supports symbolic math,
optimization, phase plane analysis, continuation and bifurcation analysis, data
analysis, and other tools for modeling – particularly for biological
applications.

The project is fully open source with a BSD license, and welcomes contributions
from the community.}

Name:           python-%{pypi_name}
Version:        0.90.2
Release:        1%{?dist}
Summary:        Python dynamical systems simulation and modeling

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
License:        BSD
URL:            http://incf.github.io/nineml-spec/software/pydstool/
Source0:        %pypi_source %{pypi_name}

BuildRequires:  swig
BuildRequires:  gcc
BuildRequires:  gfortran

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist scipy}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist mock}
Recommends:     %{py2_dist ipython}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
# DELETE ME: Use standard names
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist mock}
Recommends:     %{py3_dist ipython}
# For documentation
BuildRequires:  %{py3_dist sphinx}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{desc}

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%py3_build

%if %{with py2}
%py2_build
%endif

pushd doc
    make SPHINXBUILD=sphinx-build-3 html
    rm -rf _build/html/.doctrees
    rm -rf _build/html/.buildinfo
popd

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
# If, however, we're installing separate executables for python2 and python3,
# the order needs to be reversed so the unversioned executable is the python2 one.
%if %{with py2}
%py2_install
%endif

%py3_install

%check
%if %{with tests}
%if %{with py2}
%{__python2} setup.py test
%endif
%{__python3} setup.py test
%endif

%if %{with py2}
%files -n python2-%{pypi_name}
%license COPYING
%doc README.rst
%{python2_sitelib}/%{pypi_name}-%{version}-py2.?.egg-info
%{python2_sitelib}/%{pypi_name}
%endif

%files -n python3-%{pypi_name}
%license COPYING
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py3.?.egg-info
%{python3_sitelib}/%{pypi_name}

%files doc
%license COPYING
%doc doc/_build/html

%changelog
* Mon Dec 03 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.90.2-1
- Initial build
