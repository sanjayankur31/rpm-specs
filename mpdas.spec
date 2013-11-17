Name:			mpdas
Version:		0.3.0
Release:		2%{?dist}
Summary:		An MPD audioscrobbling client

Group:			Applications/Text
License:		BSD
URL:			http://50hz.ws/%{name}/
Source0:		http://50hz.ws/%{name}/%{name}-%{version}.tar.bz2
# fix a minor glitch in the man page
Patch0:			mpdas-man.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libmpd-devel libcurl-devel
Provides:		bundled(md5-deutsch)

%description
mpdas is a MPD AudioScrobbler client supporting the 2.0 protocol 
specs. It is written in C++ and uses libmpd to retrieve the song 
data from MPD and libcurl to post it to Last.fm


%prep
%setup -q
%patch0 


%build
export CONFIG="%{_sysconfdir}" PREFIX="$RPM_BUILD_ROOT%{_prefix}" MANPREFIX="$RPM_BUILD_ROOT%{_mandir}" CXXFLAGS+="$RPM_OPT_FLAGS"
make 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix} $RPM_BUILD_ROOT%{_mandir}/man1/ $RPM_BUILD_ROOT%{_sysconfdir} $RPM_BUILD_ROOT%{_bindir}

# Manually install them
install -m 0755 mpdas $RPM_BUILD_ROOT%{_bindir}/mpdas
rm mpdas -f
install -m 0644 mpdas.1 $RPM_BUILD_ROOT%{_mandir}/man1/mpdas.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README mpdasrc.example ChangeLog
%{_mandir}/man1/mpdas.1*
%{_bindir}/mpdas

%changelog
* Thu Apr 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.0-2
- Changed make flags

* Mon Mar 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org>-  0.3.0-2
- Added virtual requires for md5-deutshc

* Sat Feb 26 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.0-2
- add a patch to fix a minor glitch in the man page

* Sat Feb 26 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.0-1
- Initial rpm build
