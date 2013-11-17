Name: python-pymodbus
Version: 0.9.0
Release: 1%{?dist}
Summary: A Modbus Protocol Stack in Python

Group: Development/Languages
License: BSD
URL: http://code.google.com/p/pymodbus/
Source0: http://pymodbus.googlecode.com/files/pymodbus-%{version}.tar.gz
BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools-devel 
Requires: python-twisted >= 2.5.0
Requires: python-nose >= 0.9.3
Requires: pyserial >= 2.4

%description
Pymodbus is a full Modbus protocol implementation using twisted for its
asynchronous communications core.

The library currently supports the following:

Client Features

    * Full read/write protocol on discrete and register
    * Most of the extended protocol (diagnostic/file/pipe/setting/information)
    * TCP, UDP, Serial ASCII, Serial RTU, and Serial Binary
    * asynchronous(powered by twisted) and synchronous versions
    * Payload builder/decoder utilities 

Server Features

    * Can function as a fully implemented Modbus server
    * TCP, UDP, Serial ASCII, Serial RTU, and Serial Binary
    * asynchronous(powered by twisted) and synchronous versions
    * Full server control context (device information, counters, etc)
    * A number of backing contexts (database, redis, a slave device) 

%prep
%setup -q -n pymodbus-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__rm} -rf $RPM_BUILD_ROOT%{python_sitelib}/test

%files
%{python_sitelib}/*

%changelog
* Wed Dec 07 2011 Christian Krause <chkr@fedoraproject.org> - 0.9.0-1
- Initial Spec file

