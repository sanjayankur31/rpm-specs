Name:           gitg
Version:        0.3.2
Release:        1%{?dist}
Summary:        GTK+ graphical interface for the git revision control system

Group:          Development/Tools
License:        GPLv2+
URL:            http://trac.novowork.com/gitg
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.2/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  dbus-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk3-devel
BuildRequires:  gtksourceview3-devel
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  intltool
BuildRequires:  libgit2-glib-devel
BuildRequires:  libgee-devel
BuildRequires:  json-glib-devel
BuildRequires:  webkitgtk3-devel
BuildRequires:  gobject-introspection-devel

Requires:       %{name}-libs = %{version}-%{release}
Requires:       git
Requires:       gsettings-desktop-schemas

%description
gitg is a GitX clone for GNOME/gtk+. It aims at being a small, fast and
convenient tool to visualize git history and actions that benefit from a
graphical presentation.

%package libs
Summary:        Backend Library for gitg
License:        GPLv2+
Group:          Development/Libraries

%description libs
libgitg is a GObject based library that provides an easy access to git methods
through GObject based methods

%package devel
Summary:        Development files for %{name}
License:        GPLv2+
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}
# FIXME: Provides should be dropped when F15 is EOL
Provides:       gitg-libgitg-devel%{?_isa} = %{version}-%{release}
Obsoletes:      gitg-libgitg-devel < 0.2.2-2

%description devel
This package contains development files for %{name}.

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

desktop-file-install                                       \
  --vendor=""                                              \
  --delete-original                                        \
  --dir=$RPM_BUILD_ROOT%{_datadir}/applications            \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database >&/dev/null || :
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
update-desktop-database >&/dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README ChangeLog

%{_bindir}/gitg
%{_datadir}/gitg
%{_mandir}/man1/gitg.1*

%{_datadir}/icons/hicolor/*/apps/gitg.*

%{_datadir}/glib-2.0/schemas/org.gnome.gitg.gschema.xml

%{_datadir}/applications/gitg.desktop


%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libgitg-*.so.*


%files devel
%defattr(-,root,root,-)
%{_libdir}/libgitg-*.so
%{_libdir}/pkgconfig/libgitg-1.0.pc

%{_includedir}/libgitg-1.0

%changelog
* Tue Jan 21 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.2-1
- Update to latest upstream release
- Dropped F15 provides
- Added some new BRs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 05 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 0.2.7-1
- update to 0.2.7

* Thu Mar 28 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 0.2.6-1
- update to 0.2.6

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 0.2.5-6
- Rebuilt for gtksourceview3 soname bump

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 0.2.5-3
- Silence rpm scriptlet output

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 04 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 0.2.5-1
- update to 0.2.5

* Thu Jul 21 2011 James Bowes <jbowes@redhat.com> 0.2.3-1
- update to 0.2.3

* Fri Apr 22 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.2-3
- Fix Obsoletes/Provides

* Thu Apr 21 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.2-2
- Remove libtool archive and static library
- Rename libgitg(-devel) package to follow naming guidelines

* Fri Apr 01 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 0.2.2-1
- update to 0.2.2

* Tue Feb 08 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 0.2.0-1
- update to 0.2.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Apr 13 2010 James Bowes <jbowes@redhat.com> 0.0.6-3
- update icon cache

* Tue Apr 13 2010 James Bowes <jbowes@redhat.com> 0.0.6-2
- Remove pixmaps dir

* Tue Apr 13 2010 James Bowes <jbowes@redhat.com> 0.0.6-1
- Update to 0.0.6

* Tue Sep 15 2009 James Bowes <jbowes@redhat.com> 0.0.5-1
- Update to 0.0.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 02 2009 James Bowes <jbowes@redhat.com> 0.0.3-1
- Initial packaging for Fedora.

