Name:		pjproject
Version:	1.10
Release:	2%{?dist}
Summary:	Libraries written in C language for building embedded/non-embedded VoIP applications

Group:		System Environment/Libraries
License:	GPLv2
URL:		http://www.pjsip.org
Source0:	http://www.pjsip.org/release/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:	alsa-lib-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig

%description
This package provides the Open Source, comprehensive, high
performance, small footprint multimedia communication libraries written in C
language for building embedded/non-embedded VoIP applications. 
It contain:
- PJSIP - Open Source SIP Stack
- PJMEDIA - Open Source Media Stack
- PJNATH - Open Source NAT Traversal Helper Library
- PJLIB-UTIL - Auxiliary Library
- PJLIB - Ultra Portable Base Framework Library

%package        devel
Summary:        Development files to use pjproject
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Header information for:
- PJSIP - Open Source SIP Stack
- PJMEDIA - Open Source Media Stack
- PJNATH - Open Source NAT Traversal Helper Library
- PJLIB-UTIL - Auxiliary Library
- PJLIB - Ultra Portable Base Framework Library


%prep
%setup -q


%build
%configure
make dep
make %{?_smp_mflags}


%install
rm -rf  %{buildroot}
make install DESTDIR=%{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING README.txt README-RTEMS INSTALL.txt
%{_libdir}/*.a

%files devel
%dir %{_includedir}/pj++
%dir %{_includedir}/pj
%dir %{_includedir}/pj/compat
%dir %{_includedir}/pjlib-util
%dir %{_includedir}/pjmedia-audiodev
%dir %{_includedir}/pjmedia-codec
%dir %{_includedir}/pjmedia
%dir %{_includedir}/pjnath
%dir %{_includedir}/pjsip-simple
%dir %{_includedir}/pjsip-ua
%dir %{_includedir}/pjsip
%dir %{_includedir}/pjsua-lib
%{_includedir}/pj++/*.hpp
%{_includedir}/pj/*.h
%{_includedir}/pj/compat/*.h
%{_includedir}/pj/compat/*.in
%{_includedir}/pjlib-util/*.h
%{_includedir}/pjmedia-audiodev/*.h
%{_includedir}/pjmedia-codec/*.h
%{_includedir}/pjmedia-codec/*.in
%{_includedir}/pjmedia/*.h
%{_includedir}/pjmedia/*.in
%{_includedir}/pjnath/*.h
%{_includedir}/pjsip-simple/*.h
%{_includedir}/pjsip-ua/*.h
%{_includedir}/pjsip/*.h
%{_includedir}/pjsip/*.in
%{_includedir}/pjsua-lib/*.h
%{_includedir}/*.h
%{_includedir}/*.hpp
%{_libdir}/pkgconfig/libpjproject.pc


%changelog
* Mon Aug 15 2011 Mario Santagiulaina <fedora@marionline.it> 1.10-2
- Follow the comment of Thomas Spura:
https://bugzilla.redhat.com/show_bug.cgi?id=728302#c1

* Thu Aug 04 2011 Mario Santagiulaina <fedora@marionline.it> 1.10-1
- Initial RPM release
