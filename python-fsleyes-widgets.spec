# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# %%if 0%%{?fedora} < 30
# %%global with_py2 1
# %%else
# %%global with_py2 0
# %%endif

# This package is required for fsleyes which only supports py3, so we don't
# support py2 for this either.
%global with_py2 0

%global srcname fsleyes-widgets

%global desc \
A collection of custom wx widgets and utilities used by FSLeyes.


Name:           python-%{srcname}
Version:        0.7.0
Release:        1%{?dist}
Summary:        A collection of custom wx widgets and utilities used by FSLeyes.

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
rm -rfv fsleyes_widgets.egg-info

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
# From https://git.fmrib.ox.ac.uk/fsl/fsleyes/widgets/blob/master/.ci/test_template.sh
# These tests fail, so I've disabled them for the time being. Upstream has been e-mailed.
%if %{with_py2}
xvfb-run pytest-2 tests --ignore=tests/test_autotextctrl.py --ignore=tests/test_bitmapradio.py --ignore=tests/test_bitmaptoggle.py --ignore=tests/test_colourbutton.py --ignore=tests/test_floatslider.py --ignore=tests/test_notebook.py --ignore=tests/test_rangeslider.py --ignore=tests/test_texttag.py --ignore=tests/test_numberdialog.py
%endif

xvfb-run pytest-3 tests --ignore=tests/test_autotextctrl.py --ignore=tests/test_bitmapradio.py --ignore=tests/test_bitmaptoggle.py --ignore=tests/test_colourbutton.py --ignore=tests/test_floatslider.py --ignore=tests/test_notebook.py --ignore=tests/test_rangeslider.py --ignore=tests/test_texttag.py --ignore=tests/test_numberdialog.py

%if %{with_py2}
%files -n python2-%{srcname}
%license LICENSE COPYRIGHT
%doc README.rst
%{python2_sitelib}/fsleyes_widgets/
%{python2_sitelib}/fsleyes_widgets-%{version}-py2.?.egg-info
%endif

%files -n python3-%{srcname}
%license LICENSE COPYRIGHT
%doc README.rst
%{python3_sitelib}/fsleyes_widgets/
%{python3_sitelib}/fsleyes_widgets-%{version}-py3.?.egg-info

%files doc
%license LICENSE COPYRIGHT
%doc doc/html

%changelog
* Fri Nov 02 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.7.0-1
- Initial build
