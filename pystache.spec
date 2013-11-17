Name:           pystache
Version:        0.3.1
Release:        1%{?dist}
Summary:        Mustache for Python

License:        MIT
URL:            http://pypi.python.org/pypi/%{name}/
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

%description
Inspired by ctemplate and et, Mustache is a framework-agnostic way to render
logic-free views.

As ctemplates says, "It emphasizes separating logic from presentation: it is
impossible to embed application logic in this template language."

Pystache is a Python implementation of Mustache. It has been tested with Python
2.6.1.

%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc PKG-INFO HISTORY.rst README.rst
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info

%changelog
* Wed Oct 26 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.1-1
Initial rpmbuild
