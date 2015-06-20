Name:           google-api-python-client
Version:        1.3.1
Release:        1%{?dist}
Summary:        Google APIs Client Library for Python

License:        ASL 2.0
URL:            http://github.com/google/%{name}/
Source0:        https://pypi.python.org/packages/source/g/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:   python-uri-templates
Requires:   python-httplib2

%description
Written by Google, this library provides a small, flexible, and powerful 
Python client library for accessing Google APIs.


%prep
%setup -q

# remove egg info
rm -rf google_api_python2_client.egg-info


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

for lib in $RPM_BUILD_ROOT%{python2_sitelib}/googleapiclient/*.py; do
 sed '1{\@^#!/usr/bin/python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

 
%files
%doc LICENSE CHANGELOG
%{python2_sitelib}/apiclient
%{python2_sitelib}/googleapiclient
%{python2_sitelib}/google_api_python_client-%{version}-py?.?.egg-info

%changelog
* Sat Feb 14 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.3.1-1
- Update to latest version

* Sat Jul 27 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.1-1
- Initial rpm package

