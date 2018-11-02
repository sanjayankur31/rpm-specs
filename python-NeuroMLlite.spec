%global commit af6f7768527086ae820d3d4f988f33a4e7f977b2
%global shortcommit %(c=%{commit}; echo ${c:0:7})


# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
%if 0%{?fedora} < 30
%global with_py2 1
%else
%global with_py2 0
%endif

%global srcname neuromllite
%global pretty_name NeuroMLlite

%global desc \
A common framework for reading/writing/generating network specifications.

Name:           python-%{pretty_name}
Version:        0.1.4
Release:        1.20181102.git%{shortcommit}%{?dist}
Summary:        A common framework for reading/writing/generating network specifications

License:        LGPLv3
URL:            https://github.com/NeuroML/%{pretty_name}

# Use latest upstream commit as PyPi version does not build correctly
Source0:        https://github.com/NeuroML/%{pretty_name}/archive/%{commit}/%{srcname}-%{shortcommit}.tar.gz

# PR Opened: https://github.com/NeuroML/NeuroMLlite/pull/2
Source1:        LICENSE.lesser

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
%autosetup -n %{pretty_name}-%{commit}
rm -rf %{srcname}.egg-info
cp -v %{SOURCE1} .

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
%license LICENSE.lesser
%doc README.md
# update this, wild cards are now forbidden
# %{python2_sitelib}/*
%endif

%files -n python3-%{srcname}
%license LICENSE.lesser
%doc README.md
# update this, wild cards are now forbidden
# %{python3_sitelib}/*
# %{_bindir}/sample-exec

%changelog
* Fri Nov 02 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.4-1.20181102.gitaf6f776
- Initial build
