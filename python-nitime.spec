# Use a git commit with fixes
%global commit 1fab57162a016351f530a7db2c77c1c1b3355476
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global run_tests 1


# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
%if 0%{?fedora} < 30
%global with_py2 1
%else
%global with_py2 0
%endif

%global srcname nitime

%global desc %{expand: \
Nitime is library of tools and algorithms for the analysis of time-series data
from neuroscience experiments. It contains a implementation of numerical
algorithms for time-series analysis both in the time and spectral domains, a
set of container objects to represent time-series, and auxiliary objects that
expose a high level interface to the numerical machinery and make common
analysis tasks easy to express with compact and semantically clear code.

Current information can always be found at the nitime website. Questions and
comments can be directed to the mailing list:
http://mail.scipy.org/mailman/listinfo/nipy-devel.
}


Name:           python-%{srcname}
Version:        0.8
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        An example python module

License:        BSD
URL:            http://nipy.org/%{srcname}
Source0:        https://github.com/nipy/nitime/archive/%{commit}/%{srcname}-%{shortcommit}.tar.gz
Patch0:         %{srcname}-0.7-remove-six.patch

BuildRequires:  python3-devel

BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist networkx}
BuildRequires:  %{py3_dist nibabel}
BuildRequires:  %{py3_dist cython}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist nose}
BuildRequires:  gcc
BuildRequires:  texlive-latex
BuildRequires:  texlive-ucs
BuildRequires:  tex(amsthm.sty)

Requires:       %{py3_dist numpy}
Requires:       %{py3_dist scipy}
Requires:       %{py3_dist matplotlib}
Requires:       %{py3_dist networkx}
Requires:       %{py3_dist nibabel}
Requires:       %{py3_dist cython}
Requires:       %{py3_dist six}

%description
%{desc}

%if %{with_py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist sphinx}
BuildRequires:  %{py2_dist networkx}
BuildRequires:  %{py2_dist nibabel}
BuildRequires:  %{py2_dist cython}
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist nose}

Requires:       %{py2_dist numpy}
Requires:       %{py2_dist scipy}
Requires:       %{py2_dist matplotlib}
Requires:       %{py2_dist networkx}
Requires:       %{py2_dist nibabel}
Requires:       %{py2_dist cython}
Requires:       %{py2_dist six}
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
Summary:    Documentation for %{name}.

%description doc
Documentation files for %{name}.

%prep
%autosetup -n %{srcname}-%{commit} -p1
rm -rvf %{srcname}.egg-info
rm -f nitime/six.py
find . -name "*.so" -exec rm -fv '{}' \;

# Correct shebangs to python3
sed -i 's|^#!/usr/bin/env python|#!/usr/bin/python3|' setup.py
sed -i 's|python|python3|' doc/Makefile
pushd tools
    for f in *; do
        sed -E -i 's|^#!/usr/bin/env python|#!/usr/bin/python3|' "$f"
    done
popd

%build
%py3_build

%if %{with_py2}
%py2_build
%endif

pushd doc &&
    PYTHONPATH=../ make html &&
popd


%install
%if %{with_py2}
%py2_install
%endif

%py3_install

%check
%if %{run_tests}
# From https://github.com/neurodebian/nitime/blob/3ca5a131ba1ea839e047a7a2e008b754be9fe4bb/debian/rules#L47
%if %{with_py2}
PYTHONPATH=$RPM_BUILD_ROOT/%{python2_sitearch} nosetests-2 '--exclude=test_(coherence_linear_dependence|lazy_reload)' nitime
%endif
PYTHONPATH=$RPM_BUILD_ROOT/%{python3_sitearch} nosetests-3 '--exclude=test_(coherence_linear_dependence|lazy_reload)' nitime
%endif

%if %{with_py2}
%files -n python2-%{srcname}
%license LICENSE THANKS
%doc README.txt
%{python2_sitearch}/%{srcname}-%{version}.dev0-py2.?.egg-info
%{python2_sitearch}/%{srcname}
%endif

%files -n python3-%{srcname}
%license LICENSE
%doc README.txt THANKS
%{python3_sitearch}/%{srcname}-%{version}.dev0-py3.?.egg-info
%{python3_sitearch}/%{srcname}

%files doc
%license LICENSE
%doc doc/_build/html

%changelog
* Sun Nov 04 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8-0.1.git1fab571
- Initial build
