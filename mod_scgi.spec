%global _hardened_build 1
# Filter out passfd since it's an internal library only this application is
# supposed to use.
%global __provides_exclude ^passfd\\.so$


Name:           mod_scgi
Version:        1.14
Release:        1%{?dist}
Summary:        Apache2 module for the SCGI protocol

Group:          Applications/Internet
License:        MIT and CNRI
URL:            http://python.ca/scgi/
Source0:        http://python.ca/scgi/releases/scgi-%{version}.tar.gz
Source1:        scgi.conf
# Patches are required to make the package build with the new apache API
# I've mailed upstream, who appears to be the debian maintainer, requesting a
# new release including these patches, but haven't heard from yet
# http://patch-tracker.debian.org/patch/series/view/scgi/1.13-1.1/port-to-apache24
Patch1:         python-scgi-apache24.patch

BuildRequires:  httpd-devel, python2-devel, pcre-devel
Requires:       httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing)

%description
The SCGI protocol is a replacement for the Common Gateway
Interface (CGI) protocol. It is a standard for applications
to interface with HTTP servers. It is similar to FastCGI
but is designed to be easier to implement.

%package -n python-scgi
Summary:    Python implementation of the SCGI protocol

%description -n python-scgi
The SCGI protocol is a replacement for the Common Gateway
Interface (CGI) protocol. It is a standard for applications
to interface with HTTP servers. It is similar to FastCGI
but is designed to be easier to implement.

This is a Python package implementing the server side of the SCGI protocol.


%prep
%setup -q -n scgi-%{version}
%patch1 -p1


%build
CFLAGS="%{optflags}" %{__python2} setup.py build
%{_bindir}/apxs -c apache2/mod_scgi.c

%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT 
install -D -m 0755 apache2/.libs/mod_scgi.so  $RPM_BUILD_ROOT/%{_libdir}/httpd/modules/mod_scgi.so
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/scgi.conf

sed -i "1d" $RPM_BUILD_ROOT/%{python_sitearch}/scgi/quixote_handler.py
sed -i "1d" $RPM_BUILD_ROOT/%{python_sitearch}/scgi/scgi_server.py
sed -i "1d" $RPM_BUILD_ROOT/%{python_sitearch}/scgi/test_passfd.py

# Rename
cp apache2/README.txt README.apache2.txt

%files
%doc CHANGES.txt LICENSE.txt README.txt doc/* README.apache2.txt
%config(noreplace) %{_sysconfdir}/httpd/conf.d/scgi.conf
%{_libdir}/httpd/modules/mod_scgi.so

%files -n python-scgi
%doc CHANGES.txt LICENSE.txt README.txt doc/*
%{python_sitearch}/scgi
%{python_sitearch}/scgi-%{version}-py?.?.egg-info


%changelog
* Tue Oct 22 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.14-1
- Filter passfd since it's only to be used by the handlers this package
  provides
- Follow debian packaging and break into two separate packages
- http://packages.debian.org/sid/python-scgi
- http://packages.debian.org/sid/alpha/libapache2-mod-scgi 
- Updated as per https://bugzilla.redhat.com/show_bug.cgi?id=1013485#c8

* Sat Oct 19 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.14-1
- Fix as per re-review request 1013485
- Remove uneeded patches
- Update license
- Remove bundled passfd
- Update to 1.14

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 30 2009 Jesse Keating <jkeating@redhat.com> - 1.13-3
- Bump for F12 mass rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 12 2008 Marek Mahut <mmahut@fedoraproject.org> - 1.13-1
- Initial build
