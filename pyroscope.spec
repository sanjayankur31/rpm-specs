%global svn_rev 1986
%global svn_co_date 20120525
%global rt-version  0.9.2
%global lt-version  0.13.2

Name:           pyroscope
Version:        0
Release:        0.1.r%{svn_rev}_%{svn_co_date}%{?dist}
Summary:        Python torrent tools, specially to be used with rtorrent

License:        GPLv2+
URL:            http://code.google.com/p/pyroscope/wiki/
# svn checkout -r %{svn_rev} http://%{name}.googlecode.com/svn/trunk/ %{name}-svn-20120525
# tar -cvzf %{name}-svn-%{svn_co_date}.tar.gz %{name}-svn-%{svn_co_date}/
Source0:        %{name}-svn-%{svn_co_date}.tar.gz
Source1:        http://libtorrent.rakshasa.no/downloads/libtorrent-%{lt-version}.tar.gz
Source2:        http://libtorrent.rakshasa.no/downloads/rtorrent-%{rt-version}.tar.gz

#BuildArch:      noarch
BuildRequires:  python-devel python-setuptools
BuildRequires:  curl-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libsigc++20-devel
BuildRequires:  openssl-devel
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig
BuildRequires:  xmlrpc-c-devel

%description
A collection of tools for the BitTorrent protocol and especially the rTorrent
client. It offers the following components:

* CommandLineTools for automation of common tasks, like metafile creation,
and filtering and mass-changing your loaded torrents
* Patches to improve your rTorrent experience, like new commands and canvas
 coloring
* rTorrent extensions like a QueueManager and statistics (work in progress) 
a modern and versatile rTorrent web interface (currently on hold) 


%prep
%setup -q


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc
# For noarch packages: sitelib
%{python_sitelib}/*
# For arch-specific packages: sitearch
%{python_sitearch}/*


%changelog
