Name:           google-api-python-client
Version:        1.1
Release:        1%{?dist}
Summary:        Google APIs Client Library for Python

License:        ASL 2.0
URL:            http://code.google.com/p/%{name}/
Source0:        http://google-api-python-client.googlecode.com/files/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-oauth2
BuildRequires:  python-gflags
BuildRequires:  python-setuptools
# To be packaged
Requires:   python-uri-templates

Requires:   python-oauth2
Requires:   python-oauth2client
Requires:   python-httplib2
Requires:   python-simplejson
Requires:   python-gflags

%description
Written by Google, this library provides a small, flexible, and powerful 
Python client library for accessing Google APIs.

%package -n python-oauth2client
Requires:   python-oauth2
Summary:    Library to simplify connections via OAuth 2.0

%description -n python-oauth2client
The oauth2client library makes it easy to connect to resources protected by 
OAuth 2.0.

%prep
%setup -q

# remove egg info
rm -rf google_api_python_client.egg-info

# A separate package for uritemplates
rm -rf uritemplate
sed -i "/uritemplate/d" setup.py

pushd oauth2client
sed -i "1 d" xsrfutil.py 
sed -i "1 d" util.py 
sed -i "1 d" crypt.py 
popd

pushd apiclient
sed -i "1 d" model.py
sed -i "1 d" errors.py
popd

%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc LICENSE CHANGELOG FAQ README
%{_bindir}/enable-app-engine-project
%{python_sitelib}/apiclient
%{python_sitelib}/google_api_python_client-%{version}-py?.?.egg-info

%files -n python-oauth2client
%{python_sitelib}/oauth2client

%changelog
* Sat Jul 27 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.1-1
- Initial rpm package

