# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# %%if 0%%{?fedora} < 30
# %%global with_py2 1
# %%else
# %%global with_py2 0
# %%endif

# This package is required for fsleyes which only supports py3, so we don't
# support py2 for this either.
%global with_py2 0

%global srcname fsleyes-props

%global desc %{expand: \
%{name} is a library which is used by used by FSLeyes, and which allows you to:

- Listen for change to attributes on a python object,
- Automatically generate wxpython widgets which are bound to attributes of a
  python object
- Automatically generate a command line interface to set values of the
  attributes of a python object.

To do this, you just need to subclass the .HasProperties class, and add some
PropertyBase types as class attributes.}



Name:           python-%{srcname}
Version:        1.6.4
Release:        1%{?dist}
Summary:        [wx]Python event programming framework

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist mock}
BuildRequires:  %{py3_dist pytest-cov}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist wxpython}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist six}
BuildRequires:  %{py3_dist deprecation}
BuildRequires:  xorg-x11-server-Xvfb

Requires:  %{py3_dist six}
Requires:  %{py3_dist deprecation}
Requires:  %{py3_dist numpy}
Requires:  %{py3_dist matplotlib}
Requires:  %{py3_dist wxpython}

%description
%{desc}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist sphinx}
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist mock}
BuildRequires:  %{py2_dist pytest-cov}
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist wxpython}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist six}
BuildRequires:  %{py2_dist deprecation}

Requires:  %{py2_dist six}
Requires:  %{py2_dist deprecation}
Requires:  %{py2_dist numpy}
Requires:  %{py2_dist matplotlib}
Requires:  %{py2_dist wxpython}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%package doc
Summary:        %{summary}

%description doc
This package contains documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version}
rm -rfv fsleyes_props.egg-info

%build
%py3_build

%if %{with_py2}
%py2_build
%endif

# Build documentation
%{__python3} setup.py doc

%install
%if %{with_py2}
%py2_install
%endif

%py3_install


%check
%if %{with_py2}
xvfb-run pytest-2 tests
%endif

xvfb-run pytest-3 tests

%if %{with_py2}
%files -n python2-%{srcname}
%license LICENSE COPYRIGHT
%doc README.rst
%{python2_sitelib}/fsleyes_props/
%{python2_sitelib}/fsleyes_props-%{version}-py2.?.egg-info
%endif

%files -n python3-%{srcname}
%license LICENSE COPYRIGHT
%doc README.rst
%{python3_sitelib}/fsleyes_props/
%{python3_sitelib}/fsleyes_props-%{version}-py3.?.egg-info

%files doc
%license LICENSE COPYRIGHT
%doc doc/html

%changelog
* Thu Nov 08 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.6.4-1
- WIP: needs fslpy and fsleyes-widgets, so will continue on this after.
