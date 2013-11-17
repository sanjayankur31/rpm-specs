Name:           python-passfd
Version:        0.2
Release:        1%{?dist}
Summary:        Python functions to pass file descriptors across UNIX domain sockets

License:        GPLv2+
URL:            http://code.google.com/p/python-passfd/
Source0:        http://python-passfd.googlecode.com/files/python-passfd-0.2.tar.gz

BuildRequires:  python2-devel

%description
This simple extension provides two functions to pass and receive file
descriptors across UNIX domain sockets, using the BSD-4.3+ sendmsg() and
recvmsg() interfaces. Direct bindings to sendmsg() and recvmsg() are not
provided, as the API does not map nicely into Python.

Please note that this only supports BSD-4.3+ style file descriptor passing, and
was only tested on Linux. Patches are welcomed!

For more information, see one of the R. Stevens' books:

    Richard Stevens: Unix Network Programming, Prentice Hall, 1990; chapter
6.10 

    Richard Stevens: Advanced Programming in the UNIX Environment,
Addison-Wesley, 1993; chapter 15.3 


%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check
%{__python2} t/test_passfd.py
 
%files
%doc COPYING PKG-INFO
%{python_sitearch}/*passfd*
%{python_sitearch}/python_passfd-%{version}-py?.?.egg-info


%changelog
* Tue Oct 22 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.2-1
- Initial rpmbuild
