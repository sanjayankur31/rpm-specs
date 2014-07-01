Name:           python3-dugong
Version:        3.0
Release:        1%{?dist}
Summary:        Python 3.x HTTP 1.1 client module
License:        Python
URL:            https://bitbucket.org/nikratio/python-dugong
Source0:        https://pypi.python.org/packages/source/d/dugong/dugong-%{version}.tar.bz2
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools

%description
The Python Dugong module provides an API for communicating with HTTP 1.1 
servers. It is an alternative to the standard library's http.client 
(formerly httplib) module. In contrast to http.client, Dugong:

- Allows you to send multiple requests right after each other without 
having to read the responses first.

- Supports waiting for 100-continue before sending the request body.

- Raises an exception instead of silently delivering partial data if the 
connection is closed before all data has been received.

- Raises one specific exception (ConnectionClosed) if the connection has been
closed (while http.client connection may raise any of BrokenPipeError, 
~http.client.BadStatusLine, ConnectionAbortedError, ConnectionResetError,
~http.client.IncompleteRead or simply return '' on read)

- Supports non-blocking, asynchronous operation and is compatible with the 
asyncio module.

- Not compatible with old HTTP 0.9 or 1.0 servers.

All request and response headers are represented as str, but must be encodable
in latin1. Request and response body must be bytes-like objects or binary 
streams.

%prep
%setup -qn dugong-%{version}
rm -frv dugong.egg-info

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}

%check
py.test-%{python3_version} test

%files
%doc Changes.rst LICENSE README.rst
%{python3_sitelib}/dugong/
%{python3_sitelib}/dugong-%{version}-py%{python3_version}.egg-info/

%changelog
* Thu Jun 19 2014 Christopher Meng <rpm@cicku.me> - 3.0-1
- Initial Package.
