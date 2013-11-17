%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global module_name hl7

Name:           python-%{module_name}
Version:        0.2.0
Release:        2%{?dist}
# append my cmake path before swig is included
Summary:        Python library parsing HL7 v2.x and v3.x messages

License:        BSD
URL:            http://pypi.python.org/pypi/%{module_name}

Source0:        http://pypi.python.org/packages/source/h/%{module_name}/%{module_name}-0.2.0.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

%description
python-%{module_name} is a simple library for parsing messages of 
Health Level 7 (HL7) v2.x into Python objects.

%prep
%setup -q  -n %{module_name}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

# Make docs
# These modes appear to be enough
pushd docs/
    make html
    make singlehtml
    make man
    make htmlhelp
popd


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Install the man page to the correct location
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
install -p -m 0644 docs/_build/man/%{name}.1 -t $RPM_BUILD_ROOT/%{_mandir}/man1/

# Delete buildinfo file
find docs/_build/ -name ".buildinfo" -execdir rm -fv '{}' \;
 
%files
%{python_sitelib}/%{module_name}/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%doc docs/_build/html docs/_build/htmlhelp docs/_build/singlehtml LICENSE README.rst
%{_mandir}/man1/%{name}.1*


%changelog
* Thu Jul 21 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.0-2
- Correct description
- Make additional docs

* Sun Jul 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.0-1
- Use the original source

* Thu Jul 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.1_xml.4-0.1.20110714git97ddbe9
- Initial rpm build
