Name:		pps-tools
Version:	0
Release:	0.2.20100413git74c32c%{?dist}
Summary:	LinuxPPS user-space tools

Group:		System Environment/Base
License:	GPLv2+
URL:		https://github.com/ago/pps-tools

# git clone git://github.com/ago/pps-tools; cd pps-tools
# git archive --prefix=pps-tools/ 74c32c | gzip > pps-tools-20100413git74c32c.tar.gz
Source0:	pps-tools-20100413git74c32c.tar.gz

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
This package includes the LinuxPPS user-space tools.

%package devel
Summary: LinuxPPS PPSAPI header file
Group: Development/System

%description devel
This package includes the header needed to compile PPSAPI (RFC-2783)
applications.

%prep
%setup -q -n %{name}

%build
CFLAGS="$RPM_OPT_FLAGS" make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_includedir}/sys}
install -m755 -t $RPM_BUILD_ROOT%{_bindir} ppsbind ppsfind ppstest ppswatch
install -p -m644 -t $RPM_BUILD_ROOT%{_includedir} timepps.h
ln -s ../timepps.h $RPM_BUILD_ROOT%{_includedir}/sys

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc debian/README debian/copyright
%{_bindir}/pps*

%files devel
%defattr(-,root,root,-)
%{_includedir}/timepps.h
%{_includedir}/sys/timepps.h

%changelog
* Tue Aug 09 2011 Miroslav Lichvar <mlichvar@redhat.com> 0-0.2.20100413git74c32c
- include README and copyright (#692069) 
- provide also <sys/timepps.h>

* Wed Mar 30 2011 Miroslav Lichvar <mlichvar@redhat.com> 0-0.1.20100413git74c32c
- initial release
