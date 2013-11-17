Name:		fedora-freemedia-tool
Version:	0.2
Release:	1%{?dist}
Summary:	A tool for Fedora free-media contributors

License:	GPLv3
URL:		https://gitorious.org/fedora-freemedia-tool
Source0:	%{name}-%{version}alpha.tar.gz

BuildRequires:	sqlite-devel ImageMagick-c++-devel curlpp-devel

%description
The tool aims to make it more convenient for Fedora free-media contributors to
get their tickets from the on-line trac and print out free-media envelops.


%prep
%setup -q -n %{name}-%{version}alpha


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc COPYING TODO NEWS AUTHORS
%{_bindir}/ffmtool
%{_mandir}/man1/ffmtool.1*
%{_datadir}/%{name}/



%changelog
* Thu Feb 16 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.2-1
- initial rpmbuild

