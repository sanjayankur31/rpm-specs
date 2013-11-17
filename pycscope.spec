Name:           pycscope
Version:        0.3
Release:        3%{?dist}
Summary:        Generates a cscope index of Python source trees

License:        GPLv2
URL:            http://pypi.python.org/pypi/%{name}/0.3
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
# chmod 0644 to correct permissions

BuildArch:      noarch
BuildRequires:  python2-devel

%description
A python script to generate a cscope index from a Python source tree. %{name}
uses Python's own parser and AST to generate the index, so it is a bit more
accurate than plain cscope.


%prep
%setup -q


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc README LICENSE
%{_bindir}/%{name}.py
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info


%changelog
* Sat Mar 24 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3-3
- Removed rm commands https://bugzilla.redhat.com/show_bug.cgi?id=806517#c4

* Sat Mar 24 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3-2
- Changed to python2-devel

* Sat Mar 24 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3-1
- Initial rpmbuild

