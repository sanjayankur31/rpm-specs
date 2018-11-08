# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
%if 0%{?fedora} < 30
%global with_py2 1
%else
%global with_py2 0
%endif

%global srcname example

%global desc %{expand: \
Add a description here.}

Name:           python-%{srcname}
Version:        1.2.3
Release:        1%{?dist}
Summary:        An example python module

License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch
BuildRequires:  python3-devel

%description
%{desc}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel 
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}


%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%if %{with_py2}
%py2_build
%endif

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
# If, however, we're installing separate executables for python2 and python3,
# the order needs to be reversed so the unversioned executable is the python2 one.
%if %{with_py2}
%py2_install
%endif

%py3_install

%check
%if %{with_py2}
%{__python2} setup.py test
%endif
%{__python3} setup.py test

%if %{with_py2}
%files -n python2-%{srcname}
%license COPYING
%doc README.rst
# update this, wild cards are now forbidden
%{python2_sitelib}/*
%endif

%files -n python3-%{srcname}
%license COPYING
%doc README.rst
# update this, wild cards are now forbidden
%{python3_sitelib}/*
%{_bindir}/sample-exec

%changelog
