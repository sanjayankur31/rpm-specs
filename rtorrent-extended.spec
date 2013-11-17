%global     svn_rev 1986
Name:           rtorrent-extended
Version:        0.9.2
Release:        0.1svn%{svn_rev}%{?dist}
Summary:        rtorrent with some extensions

License:        GPLv2+
URL:            http://code.google.com/p/pyroscope/wiki/RtorrentExtended
Source0:        http://libtorrent.rakshasa.no/downloads/rtorrent-%{version}.tar.gz
# svn co -r 1986 http://pyroscope.googlecode.com/svn/trunk/pyrocore/docs/rtorrent-extended
# tar -cvzf rtorrent-extended.tar.gz rtorrent-extended/
Source1:        rtorrent-extended.tar.gz
Patch0:         rtorrent-0.13.1-FTBFS-rtorrentrc.patch

BuildRequires:  curl-devel
BuildRequires: libstdc++-devel
BuildRequires: libsigc++20-devel
BuildRequires: libtorrent-devel
BuildRequires: ncurses-devel
BuildRequires: pkgconfig
BuildRequires: xmlrpc-c-devel

%description
A BitTorrent client using libtorrent, which on high-bandwidth connections is 
able to seed at 3 times the speed of the official client. Using
ncurses its ideal for use with screen or dtach. It supports 
saving of sessions and allows the user to add and remove torrents and scanning
of directories for torrent files to seed and/or download.

The extended patches add quite a few features that make rtorrent easier to use. 


%prep
%setup -q
# http://libtorrent.rakshasa.no/ticket/2326
# http://libtorrent.rakshasa.no/ticket/2327
%patch0 -p1 -b .fallocate-rtorrentrc


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc



%changelog
