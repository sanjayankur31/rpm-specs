%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           python-distutils2
Version:        1.0a3
Release:        1%{?dist}
Summary:        New version of Python's distutils

License:        PSF
URL:            http://pypi.python.org/pypi/Distutils2
Source0:        http://pypi.python.org/packages/source/D/Distutils2/Distutils2-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

%description
Distutils2 is the new version of Distutils. It's not backward compatible with
Distutils but provides more features, and implement most new packaging
standards.


%prep
%setup -q -n Distutils2-%{version}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc
# For noarch packages: sitelib
%{python_sitelib}/*


%changelog
