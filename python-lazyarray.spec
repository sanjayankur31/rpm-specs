%global module_name     lazyarray
%global with_python3 1

Name:       python-%{module_name}
Version:    0.2.7
Release:    1%{?dist}
Summary:    A lazily-evaluated numerical array class

License:    BSD
URL:        http://bitbucket.org/apdavison/lazyarray/
Source0:    https://pypi.python.org/packages/source/l/%{module_name}/%{module_name}-%{version}.tar.gz
# https://bitbucket.org/apdavison/lazyarray/raw/01cee2e7334b61519365be6325f1d832bcf66cfc/doc/conf.py
# Not included in the pypi release for some reason
Source1:    lazyarray-doc-conf.py
Source2:    Makefile.lazyarray

BuildRequires:  python2-devel python-setuptools numpy python-nose
BuildRequires:  python-sphinx
Requires:       numpy
BuildArch:      noarch

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools python3-numpy
BuildRequires:  python3-nose
%endif # if with_python3

%description
lazyarray is a Python package that provides a lazily-evaluated numerical array
class, ``larray``, based on and compatible with NumPy arrays.

Lazy evaluation means that any operations on the array (potentially including
array construction) are not performed immediately, but are delayed until
evaluation is specifically requested. Evaluation of only parts of the array is
also possible.

Use of an ``larray`` can potentially save considerable computation time and
memory in cases where:

    * arrays are used conditionally (i.e. there are cases in which the array is
      never used)
    * only parts of an array are used (for example in distributed computation,
      in which each MPI node operates on a subset of the elements of the array)
      
Documentation: http://lazyarray.readthedocs.org/

%package docs
Summary:    Documentation for %{name}
BuildArch:  noarch

%description docs
This package contains generated HTML documentation for %{name}.


%if 0%{?with_python3}
%package -n python3-%{module_name}
Summary:    A lazily-evaluated numerical array class
Requires:   python3-numpy

%description -n python3-%{module_name}
lazyarray is a Python package that provides a lazily-evaluated numerical array
class, ``larray``, based on and compatible with NumPy arrays.

Lazy evaluation means that any operations on the array (potentially including
array construction) are not performed immediately, but are delayed until
evaluation is specifically requested. Evaluation of only parts of the array is
also possible.

Use of an ``larray`` can potentially save considerable computation time and
memory in cases where:

    * arrays are used conditionally (i.e. there are cases in which the array is
      never used)
    * only parts of an array are used (for example in distributed computation,
      in which each MPI node operates on a subset of the elements of the array)
      
Documentation: http://lazyarray.readthedocs.org/

%package -n python3-%{module_name}-docs
Summary:    Documentation for python3-%{module_name}
BuildArch:  noarch

%description -n python3-%{module_name}-docs
This package contains generated HTML documentation for python3-%{module_name}.
%endif

%prep
%setup -q -n %{module_name}-%{version}
cp %{SOURCE1} doc/conf.py
cp %{SOURCE2} doc/Makefile

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python2} setup.py build

# only needs to be built once
pushd doc
make html
rm _build/html/.buildinfo

pushd _build/html/
iconv -f iso8859-1 -t utf-8 objects.inv > objects.inv.conv && mv -f objects.inv.conv objects.inv
popd

popd

sed -i 's/\r$//' doc/_build/html/_static/jquery.js

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
nosetests test

%if 0%{?with_python3}
pushd %{py3dir}
nosetests-3.4 test
popd
%endif

%files
%doc LICENSE changelog.txt README 
%{python2_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{python2_sitelib}/%{module_name}.py*

%files docs
%doc doc/_build/html

%if 0%{?with_python3}
%files -n python3-%{module_name}
%doc LICENSE changelog.txt README
%{python3_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{python3_sitelib}/__pycache__/%{module_name}*
%{python3_sitelib}/%{module_name}*.py

%files -n python3-%{module_name}-docs
%doc doc/_build/html

%endif

%changelog
* Wed Oct 08 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.2.7-1
- Split documentation to separate sub package

* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.2.7-1
- Added tests
- Corrected file lists
- Added docs

* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.2.7-1
- Initial rpm build

