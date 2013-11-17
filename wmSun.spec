Name:           wmSun
Version:        1.03
Release:        4%{?dist}
Summary:        Rise/Set time of Sun in a dockapp

Group:          User Interface/X
License:        GPLv2+
# Original homepage is down, use the pool at dockapps.org instead.
URL:            http://www.dockapps.org/file.php/id/16
Source0:        http://www.dockapps.org/download.php/id/23/%{name}-%{version}.tar.gz
BuildRequires:  libXext-devel
BuildRequires:  libXpm-devel

%description
Rise/Set time of Sun in a WindowMaker dockapp.

%prep
%setup -q


%build
cd ./%{name}
make clean
make COPTS='%{optflags}' %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install -p -m 0755 ./%{name}/%{name} -t $RPM_BUILD_ROOT%{_bindir}
install -p -m 0644 ./%{name}/%{name}.1 -t $RPM_BUILD_ROOT%{_mandir}/man1/



%files
%defattr(-,root,root,-)
%doc BUGS COPYING TODO ./%{name}/README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*



%changelog

* Fri Jul 01 2011 Mario Blättermann <mariobl@fedoraproject.org> 1.03-4
- Tweaked "make" call to get a real debug package
- Removed initial cleaning of buildroot in %%install

* Thu Jun 30 2011 Mario Blättermann <mariobl@fedoraproject.org> 1.03-3
- Removed -s switch from install section to don't strip the binary
- Dropped %%clean section
- Dropped BuildRoot definition

* Tue May 31 2011 Mario Blättermann <mariobl@fedoraproject.org> 1.03-2
- Replaced %{buildroot} with $RPM_BUILD_ROOT

* Sat Apr 30 2011 Mario Blättermann <mariobl@fedoraproject.org> 1.03-1
- initial version
