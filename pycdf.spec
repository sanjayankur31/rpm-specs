# Does not support py3 yet
%global with_python3 0
%global actual_version 0.6-3b


Name:           pycdf
Version:        0.6.3b
Release:        1%{?dist}
Summary:        A python interface to the Unidata netCDF library

License:        Public Domain
URL:            http://pysclint.sourceforge.net/pycdf/
Source0:        http://downloads.sourceforge.net/pysclint/%{name}-%{actual_version}.tar.gz  

BuildRequires:  python2-devel python-setuptools
BuildRequires:  numpy
BuildRequires:  netcdf-devel


%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:  netcdf4-python3
%endif # if with_python3

# Some filters
%{?filter_setup:
%filter_provides_in %{_docdir} 
%filter_requires_in %{_docdir}
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}


%description
pycdf is a python interface to the Unidata netCDF library.  It provides an
almost complete coverage of the netCDF C API, wrapping it  inside easy to use
python classes.

%if 0%{?with_python3}
%package -n python3-pycdf
Group:          Applications/System
Summary:        A python interface to the Unidata netCDF library

%description -n python3-pycdf
pycdf is a python interface to the Unidata netCDF library.  It provides an
almost complete coverage of the netCDF C API, wrapping it  inside easy to use
python classes.

%endif # with_python3


%package doc
Summary:    Documentation for %{name}
BuildArch:  noarch

%description doc
pycdf is a python interface to the Unidata netCDF library.  It provides an
almost complete coverage of the netCDF C API, wrapping it  inside easy to use
python classes.

%prep
%setup -q -n %{name}-%{actual_version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3


chmod 0755 $RPM_BUILD_ROOT/%{python_sitearch}/%{name}/_pycdfext.so
 
%files
%doc CHANGES README
%{python_sitearch}/%{name}/
# Brilliant, another format for the version. Hallelujah!
%{python_sitearch}/%{name}-0.6_3b-py?.?.egg-info


%if 0%{?with_python3}
%files -n python3-pycdf
%doc
%{python3_arch}/%{name}/
%endif # with_python3

%files doc
%doc doc examples CHANGES README

%changelog
* Tue Mar 26 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.6.3b-1
- Initial rpmbuild

