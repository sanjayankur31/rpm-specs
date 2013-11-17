%global snapshot_date 20111028
%global snapshot_revision 638
Name:           transgui
Version:        3.1
Release:        3.%{snapshot_date}svn%{snapshot_revision}%{?dist}
Summary:        An App to remotely control a Transmission Bit-Torrent client  

Group:          Applications/Internet
License:        GPLv2+
URL:            https://code.google.com/p/transmisson-remote-gui/
#clone and tarred : svn export -r%%{snapshot_revision} http://transmisson-remote-gui.googlecode.com/svn/trunk/ transgui-%%{version}
#tar -cvzf transgui-%%{version}svn%%{snapshot_revision}.tar.gz transgui-%%{version}
Source0:        %{name}-%{version}svn%{snapshot_revision}.tar.gz
Source1:        %{name}.desktop


BuildRequires:  fpc
BuildRequires:  desktop-file-utils
BuildRequires:  lazarus
BuildRequires:  prelink

%description
Transmission Remote GUI is a feature rich cross platform front-end to remotely
control a Transmission Bit-Torrent client daemon via its RPC protocol. It is 
faster and has more functionality than the built-in Transmission web interface.

%prep
%setup -q


%build
make %{?_smp_mflags}
execstack -c %{name}

%install
install -pd $RPM_BUILD_ROOT/%{_bindir}
install -p %{name} $RPM_BUILD_ROOT/%{_bindir}

#menu-entries
install -pdm 755 $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}
install -pd $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp -p %{name}.png $RPM_BUILD_ROOT%{_datadir}/pixmaps


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%doc readme.txt LICENSE.txt rpc-spec.txt VERSION.txt


%changelog
* Tue Oct 28 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 3.1-3.20111028svn638
- Updated to new revision

* Tue Apr 12 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 3.1-2.20110410svn604
- Fix Snapshot issue

* Sun Apr 10 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 3.1-1.20110410svn604
- Initial version of the package
