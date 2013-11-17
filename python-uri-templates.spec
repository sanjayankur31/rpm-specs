%global commit e947a8affa793f24cd3526a1d18f21e0729672da
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-uri-templates
Version:        0.5.2
Release:        1%{?dist}
Summary:        A Python implementation of URI Template

License:        ASL 2.0
URL:            https://github.com/uri-templates/uritemplate-py
Source0:        https://github.com/uri-templates/uritemplate-py/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:  python-simplejson

%description
This is a Python implementation of RFC6570, URI Template, and can 
expand templates up to and including Level 4 in that specification.

%prep
%setup -q -n uritemplate-py-%{commit}

# Remove shebang
sed -i "1 d" uritemplate/uritemplate.py

%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# tests are a separate repository?
 
%files 
%doc README.rst
%{python_sitelib}/uritemplate-%{version}-py?.?.egg-info
%{python_sitelib}/uritemplate/


%changelog
* Sat Jul 27 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.2-1
- Initial rpmbuild

