# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global casename    PyAIBO

Name:           pyaibo
Version:        0.2.2
Release:        1%{?dist}
Summary:        This is a Python extension module for PyAIBO

License:        GPLv3
URL:            http://code.google.com/p/%{name}/
Source0:        http://%{name}.googlecode.com/files/%{casename}-0.22.zip
Patch0:         pyaibo-0.2.2-stddef-inc.patch

BuildRequires:  python-devel

%description
A python extension module for %{casename}

%package devel
Requires:   %{name}%{?_isa} = %{version}-%{release}
Summary:    C++ development files for %{casename}

%prep
%setup -q -n %{casename}
%patch0 -p0

%description devel
This package contains the headers and shared library required for writing C++
programs using %{casename}

%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} %{name}_ext_setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} %{name}_ext_setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_includedir}/
install -p -t $RPM_BUILD_ROOT/%{_includedir}/ pyaibo*.h
 
%files
%doc COPYING README.txt doc/pyaibo_intro.pdf
%{python_sitearch}/%{casename}-%{version}-py?.?.egg-info
%{python_sitearch}/%{casename}.so

%files devel
%{_includedir}/pyaibo*.h

%changelog
* Mon Sep 03 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.2.2-1
- Initial rpmbuild

