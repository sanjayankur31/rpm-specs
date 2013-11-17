Name:           rutorrent
Version:        3.5
Release:        1%{?dist}
Summary:        Yet another web front end for rTorrent

License:        GPLv3
URL:            http://code.google.com/p/rutorrent/
Source0:        http://rutorrent.googlecode.com/files/rutorrent-3.5.tar.gz
#Separate packages for plugins would be better
#Source1:        http://rutorrent.googlecode.com/files/plugins-3.5.tar.gz
# Apache configuration file
Source2:        %{name}.conf
Patch0:         %{name}-%{version}-config.patch
BuildArch:      noarch

Requires:       rtorrent mod_scgi
Requires:       php
Requires:       /usr/bin/id
Requires:       /usr/bin/curl
Requires:       /usr/bin/gzip
Requires:       /usr/bin/stat
Requires:       /usr/bin/php

%description
ruTorrent is a front-end for the popular Bittorrent client rTorrent.
Main features:

    Lightweight server side, so it can be installed on old and low-end servers
and even on some SOHO routers
    Extensible - there are several plugins and everybody can create his own one
    Nice look ;) 

%prep
%setup -q -n %{name}
%patch0 -p1

#tar -xvf %{SOURCE1}


## %build
# Nothing to build


%install
# Main datadir
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}

# configdir
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/
cp -rv conf/* $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/
rm -rf conf

mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_lib}/%{name}
mv -v php/test.sh $RPM_BUILD_ROOT/%{_prefix}/%{_lib}/%{name}

mkdir -p $RPM_BUILD_ROOT/%{_sharedstatedir}/%{name}/
mv -v share/* $RPM_BUILD_ROOT/%{_sharedstatedir}/%{name}/
rm -rf share

pushd $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/
    ln -sv ../../../%{_sharedstatedir}/%{name}/ share
    ln -sv ../../../%{_sysconfdir}/%{name} conf
popd

cp -prv * $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}

pushd $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/php/
    ln -sv ../../../..%{_prefix}/%{_lib}/%{name}/test.sh test.sh
popd

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/

%files
%config %dir %{_sysconfdir}/%{name}
%attr(644,root,apache)%config %dir %{_sysconfdir}/%{name}/users/
%attr(644,root,apache)%config(noreplace)%{_sysconfdir}/%{name}/*.php
%attr(644,root,apache)%config(noreplace)%{_sysconfdir}/%{name}/*.ini

# Everyone has access to this directory
%attr(755, apache, apache) %{_sharedstatedir}/%{name}/

%config(noreplace)%{_sysconfdir}/httpd/conf.d/%{name}.conf

%dir %{_datadir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}/conf
%{_datadir}/%{name}-%{version}/share  
%{_datadir}/%{name}-%{version}/css  
%{_datadir}/%{name}-%{version}/favicon.ico  
%{_datadir}/%{name}-%{version}/index.html
%{_datadir}/%{name}-%{version}/js
%{_datadir}/%{name}-%{version}/lang
%{_datadir}/%{name}-%{version}/php  
%{_datadir}/%{name}-%{version}/images
# Own this directory, but let future packages place plugins in there
%dir %{_datadir}/%{name}-%{version}/plugins

# Test.sh
%{_prefix}/%{_lib}/%{name}/

%changelog
* Sun Sep 29 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.5-1
- Initial rpm build

