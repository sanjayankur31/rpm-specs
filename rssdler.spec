Name:           rssdler
Version:        0.4.2
Release:        2%{?dist}
Summary:        Downloads enclosures and other objects linked to from various types of RSS feeds

Group:          Applications/Text
License:        GPLv2
URL:            http://code.google.com/p/rssdler/
Source0:        http://rssdler.googlecode.com/files/rssdler-%{version}.tar.gz
Source1:        gpl-2.0.txt
Source2:        rssdler-example-config.txt
BuildArch:      noarch

BuildRequires:  python2-devel python-setuptools python-feedparser
Requires:       python-feedparser python-mechanize

%description
A utility to automatically download enclosures and other objects 
linked to from various types of RSS feeds. 
videocasts, and torrents.

Features include:
- filtering using regular expressions and/or file size
- global, feed, and filter based download locations
- can run in the background (at least on GNU/Linux) like a daemon
- various logging and verbosity levels
- support for sites protected with cookies (LWP/MSIE/Mozilla/Safari/Firefox3)
- global and feed scan times
- respects 'ttl' tag in feeds that have them
- call custom functions after a download or after a scan of the feed 
(episode advancement!)
- generates an RSS feed of what it has downloaded.

Because it is written in Python, it is highly cross-platform compatible. 
It tries to be memory efficient, with reports of it functioning on 
consumer routers. Minimal external dependencies help keep that a reality. 
It became popular when people started using it in conjunction with 
rTorrent for torrent broadcatching.

%prep
%setup -q -n %{name}042


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT 
install %{SOURCE1} ./
install %{SOURCE2} ./
chmod a-x rssdler-example-config.txt
chmod a-x gpl-2.0.txt

pushd $RPM_BUILD_ROOT%{python_sitelib}
sed '/\/usr\/bin\/env/d' rssdler.py > rssdler.py.new &&
touch -r rssdler.py rssdler.py.new &&
mv rssdler.py.new rssdler.py
popd

%files
%defattr(-,root,root,-)
%doc README gpl-2.0.txt rssdler-example-config.txt
%{_bindir}/%{name}
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info
%{python_sitelib}/%{name}.py
%{python_sitelib}/%{name}.py?

%changelog
* Wed May 25 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-2
- Remove buildroot tag and clean section
- added an example config in docs

* Fri Feb 18 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.2-1
- initial RPM build
