# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
%if 0%{?fedora} < 30
%global with_py2 1
%else
%global with_py2 0
%endif

%global srcname petlink

%global desc %{expand: \
Decode and encode Petlink data streams (32 and 64 bit)
The encode and decode routines are written in C and are wrapped with Python.}

Name:           python-%{srcname}
Version:        0.3.2
Release:        1%{?dist}
Summary:        Decode and encode Petlink data streams (32 and 64 bit)

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source
# https://raw.githubusercontent.com/spedemon/petlink/master/LICENSE
Source1:        LICENSE.%{srcname}

BuildRequires:  gcc

%description
%{desc}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist simplewrap} >= 0.3.3
Requires:       %{py2_dist numpy}
Requires:       %{py2_dist simplewrap} >= 0.3.3
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist simplewrap} >= 0.3.3
Requires:       %{py3_dist numpy}
Requires:       %{py3_dist simplewrap} >= 0.3.3
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}


%prep
%autosetup -n %{srcname}-%{version}
cp -v %{SOURCE1} .

rm -rfv %{srcname}.egg-info

%build
%py3_build

%if %{with_py2}
%py2_build
%endif

%install
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
%license LICENSE.%{srcname}
%doc README.rst
%{python2_sitearch}/%{srcname}-%{version}-py2.?.egg-info
%{python2_sitearch}/%{srcname}
%endif

%files -n python3-%{srcname}
%license LICENSE.%{srcname}
%doc README.rst
%{python3_sitearch}/%{srcname}-%{version}-py3.?.egg-info
%{python3_sitearch}/%{srcname}

%changelog
* Thu Nov 08 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.2-1
- Initial build
