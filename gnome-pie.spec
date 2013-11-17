Name:           gnome-pie
Version:        0.2
Release:        1%{?dist}
Summary:        A visual application launcher for Gnome

License:        GPLv3
URL:            http://%{name}.simonschneegans.de/
Source0:        http://cloud.github.com/downloads/Simmesimme/Gnome-Pie/Gnome-Pie-%{version}.tar.gz
Patch0:         Gnome-Pie-link-glib-DSO.patch

BuildRequires:  vala-devel
BuildRequires:  pkgconfig(gee-1.0)
BuildRequires:  libxml2-devel
BuildRequires:  gtk2-devel
BuildRequires:  cairo-devel
BuildRequires:  cmake
BuildRequires:  unique-devel
BuildRequires:  vala-devel
BuildRequires:  libXtst-devel
BuildRequires:  gnome-menus-devel      

Requires(post):  info
Requires(preun): info

%description
Gnome-Pie is a circular application launcher for Linux. It is made of
several pies, each consisting of multiple slices. The user presses a 
key stroke which opens the desired pie. By activating one of its slices,
applications may be launched, key presses may be simulated or files can 
be opened.

%prep
%setup -q -n Gnome-Pie
%patch0 -b p0backup

%build
cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_LDFLAGS=-lgthread
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/README
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/de/LC_MESSAGES/gnomepie.mo
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/pt-br/LC_MESSAGES/gnomepie.mo

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc README AUTHORS COPYING
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/*

%changelog
* Sat Oct 22 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.2-1
- Initial version of the package
