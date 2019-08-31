Name:           cpaste
Version:        1.0.0
Release:        2%{?dist}
Summary:        Command line tool to upload things to pastebin.centos.org

License:        GPL
URL:            http://github.com/benapetr/stikkit
Source0:        http://paste.scratchbook.ch/download/%{name}-%{version}.tar.gz
Source1:        default_apikey
Source2:        default_url
Source3:        default_expiry
Source4:        README.CentOS


Patch1:         cpaste-support-private.patch
Patch2:         cpaste-useragent.patch
Patch3:         cpaste-lastargasfilename.patch

BuildRequires:  libcurl-devel cmake

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Command line tool to upload things to the CentOS Project's pastebin service
located at https://pastebin.centos.org.  Will accept input from a named file
piped in via standard input.  Permits the user to specify title; authors name;
expiry time; language/format and mark the paste as private.  May also be used
for any other stikked-based pastebin service.

%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cmake .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}/usr/local/bin/cpaste %{buildroot}%{_bindir}/cpaste
mkdir -p %{buildroot}%{_sysconfdir}/cpaste
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/cpaste/apikey
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/cpaste/url
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/cpaste/expiry

install -m 0644 %{SOURCE4} $RPM_BUILD_DIR/%{name}-%{version}/

%post

%preun

%files
%doc README.md License.txt README.CentOS
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/apikey
%config %{_sysconfdir}/%{name}/url
%config %{_sysconfdir}/%{name}/expiry

%changelog
* Thu Sep 13 2018 Pablo Greco <pablo@fliagreco.com.ar> - 1.0.0-2
- Backport patch from stikkit to support private pastes
- Backport patch from stikkit to change useragent
- Use last invalid arg as filename, no need to use -i to paste a file

* Thu Sep 13 2018 Psychotic Build System <builder@psychotic.ninja> - 1.0.0-1
- Forked from the Psychotic Ninja 'stikkit-1.0.6-7' package and rebased to 1.0.0
- Renamed stikkit->cpaste; stikkit.1->cpaste.1; README.Psychotic->README.CentOS
- Updated README.CentOS
- Updated stikkit.1
- Path references changed from /stikkit/ to /cpaste/
