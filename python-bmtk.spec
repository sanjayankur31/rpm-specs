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

%global srcname bmtk

%global desc %{expand: \
A software development package for building, simulating and analyzing
large-scale networks of different levels of resolution..}

Name:           python-%{srcname}
Version:        0.0.6
Release:        1%{?dist}
Summary:        Brain Modeling Toolkit

License:        BSD
URL:            https://alleninstitute.github.io/%{srcname}/
Source0:        https://github.com/AllenInstitute/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist pandas}
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist lxml}
BuildRequires:  %{py2_dist mpi4py}
BuildRequires:  %{py2_dist six}
BuildRequires:  %{py2_dist networkx}
BuildRequires:  %{py2_dist jsonschema}
BuildRequires:  %{py2_dist nest}
BuildRequires:  %{py2_dist neuron}
%if %{with tests}
BuildRequires:  %{py2_dist pytest}
%endif
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pandas}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist lxml}
BuildRequires:  %{py3_dist mpi4py}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist six}
BuildRequires:  %{py3_dist networkx}
BuildRequires:  %{py3_dist jsonschema}
BuildRequires:  %{py3_dist nest}
BuildRequires:  %{py3_dist neuron}
%if %{with tests}
BuildRequires:  %{py3_dist pytest}
%endif
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version}

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%py3_build

%if %{with py2}
%py2_build
%endif


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

%if %{with tests}
%check
%if %{with py2}
%{__python2} setup.py test
%endif
%{__python3} setup.py test
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
%doc docs/*

%changelog
* Sat Feb 02 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.6-1
- Initial rpm
