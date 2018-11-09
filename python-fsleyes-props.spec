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
fsleyes-props is a library which is used by used by FSLeyes, and which allows
you to:

- Listen for change to attributes on a python object,
- Automatically generate wxpython widgets which are bound to attributes of
  a python object
- Automatically generate a command line interface to set values of the
  attributes of a python object.}


Name:           python-%{srcname}
Version:        1.6.4
Release:        1%{?dist}
Summary:        [wx]Python event programming framework

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch

%description
%{desc}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist six}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist wxPython}
BuildRequires:  %{py2_dist deprecation}
BuildRequires:  %{py2_dist fsleyes-widgets}
BuildRequires:  %{py2_dist fslpy}
BuildRequires:  %{py2_dist sphinx}
BuildRequires:  %{py2_dist sphinx_rtd_theme}
BuildRequires:  %{py2_dist mock}
BuildRequires:  %{py2_dist pytest pytest-cov}
BuildRequires:  xorg-x11-server-Xvfb

Requires:  %{py2_dist six}
Requires:  %{py2_dist matplotlib}
Requires:  %{py2_dist wxPython}
Requires:  %{py2_dist deprecation}
Requires:  %{py2_dist fsleyes-widgets}
Requires:  %{py2_dist fslpy}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist six}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist wxPython}
BuildRequires:  %{py3_dist deprecation}
BuildRequires:  %{py3_dist fsleyes-widgets}
BuildRequires:  %{py3_dist fslpy}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx_rtd_theme}
BuildRequires:  %{py3_dist mock}
BuildRequires:  %{py3_dist pytest pytest-cov}
BuildRequires:  xorg-x11-server-Xvfb

Requires:  %{py3_dist six}
Requires:  %{py3_dist matplotlib}
Requires:  %{py3_dist wxPython}
Requires:  %{py3_dist deprecation}
Requires:  %{py3_dist fsleyes-widgets}
Requires:  %{py3_dist fslpy}
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

find . -name "*py" -exec sed -i '/#!\/usr\/bin\/env python/ d' '{}' \;


%build
%py3_build

%if %{with_py2}
%py2_build
%endif

# Build documentation
PYTHONPATH=.  sphinx-build-3 doc html
# Remove artefacts
rm -frv html/.buildinfo
rm -frv html/.doctrees

%install
%if %{with_py2}
%py2_install
%endif

%py3_install


%check
# These tests fail. Upstream says tests are not reliable, but work on his Ubuntu setup
%if %{with_py2}
xvfb-run pytest-2 tests --ignore=tests/test_widget_boolean.py --ignore=tests/test_widget_number.py --ignore=tests/test_widget_point.py
%endif

xvfb-run pytest-3 tests --ignore=tests/test_widget_boolean.py --ignore=tests/test_widget_number.py --ignore=tests/test_widget_point.py

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
%doc html

%changelog
* Thu Nov 08 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.6.4-1
- Initial build
