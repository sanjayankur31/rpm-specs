# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# Latest commit
%global commit b54346e8743b66c768fa31bdd925b94ce5fe4fc5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global checkout_date  20191229

# Enabled by default
# If the package needs to download data for the test which cannot be done in
# koji, these can be disabled in koji by using `bcond_with` instead, but the
# tests must be validated in mock with network enabled like so:
# mock -r fedora-rawhide-x86_64 rebuild <srpm> --enable-network --rpmbuild-opts="--with tests"
%bcond_without tests

%global pypi_name tvb-library

%global desc %{expand: \
The Virtual Brain Project (TVB Project) has the purpose of offering some modern
tools to the Neurosciences community, for computing, simulating and analyzing
functional and structural data of human brains.

"TVB Scientific Library" is the most important scientific contribution of TVB
Project, but only a part of our code. In order to use this TVB Python Library
(modify/run/test), you are advised to follow the steps described here:
http://docs.thevirtualbrain.com/manuals/ContributorsManual/ContributorsManual.html#contributors-manual
}

Name:           python-%{pypi_name}
Version:        1.5.6
Release:        1.%{checkout_date}git%{shortcommit}%{?dist}
Summary:        The Virtual Brain scientific library

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
License:        GPLv3
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://github.com/the-virtual-brain/%{pypi_name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python2-devel
# DELETE ME: Use standard names
BuildRequires:  %{py2_dist ...}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
# DELETE ME: Use standard names
BuildRequires:  %{py3_dist networkx}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist numba}
BuildRequires:  %{py3_dist numexpr}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist scikit-learn}
BuildRequires:  %{py3_dist scipy}
# Not yet in Fedora
BuildRequires:  python3-tvb-geodesic
BuildRequires:  python3-tvb-data

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
%autosetup -n %{pypi_name}-%{commit}
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
* Sat Dec 29 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5.6-1.20181229gitb54346e
- Initial build

