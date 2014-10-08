%global module_name     quantities
%global with_python3 1

Name:       python-%{module_name}
Version:    0.10.1
Release:    1%{?dist}
Summary:    Support for physical quantities with units, based on numpy

License:    BSD
URL:        http://packages.python.org/quantities
Source0:    https://pypi.python.org/packages/source/q/%{module_name}/%{module_name}-%{version}.tar.gz
# From
# https://raw.githubusercontent.com/python-quantities/python-quantities/master/doc/user/license.rst
Source1:    license.rst

BuildRequires:  python2-devel python-setuptools numpy
Requires:       numpy
BuildArch:      noarch

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools python3-numpy
%endif # if with_python3

%description
Quantities is designed to handle arithmetic and conversions of physical
quantities, which have a magnitude, dimensionality specified by various units,
and possibly an uncertainty. See the tutorial for examples. Quantities builds
on the popular numpy library and is designed to work with numpy ufuncs, many of
which are already supported. Quantities is actively developed, and while the
current features and API are stable, test coverage is incomplete so the package
is not suggested for mission-critical applications.

%if 0%{?with_python3}
%package -n python3-%{module_name}
Summary:    Support for physical quantities with units, based on numpy
Requires:       python3-numpy

%description -n python3-%{module_name}
Quantities is designed to handle arithmetic and conversions of physical
quantities, which have a magnitude, dimensionality specified by various units,
and possibly an uncertainty. See the tutorial for examples. Quantities builds
on the popular numpy library and is designed to work with numpy ufuncs, many of
which are already supported. Quantities is actively developed, and while the
current features and API are stable, test coverage is incomplete so the package
is not suggested for mission-critical applications.
%endif

%prep
%setup -q -n %{module_name}-%{version}
cp %{SOURCE1} .

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3 

%check
%{__python2} setup.py test
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3 

%files
%doc CHANGES.txt README.txt license.rst
%{python2_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{python2_sitelib}/%{module_name}/

%if 0%{?with_python3}
%files -n python3-%{module_name}
%doc CHANGES.txt README.txt license.rst
%{python3_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{python3_sitelib}/%{module_name}/

%endif

%changelog
* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.1-1
- Include license file

* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.1-1
- Initial rpm build
