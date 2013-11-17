Name:          gnome-music
Summary:       Music player and management application for GNOME
Version:       3.9.90
Release:       2%{?dist}

# The sources are under the GPLv2+ license, except for:
# - the bundled libgd which is LGPLv2+,
# - the gnome-music icon which is CC-BY-SA
#
# Also: https://bugzilla.gnome.org/show_bug.cgi?id=706457
License:       (GPLv2+ with exceptions) and LGPLv2+ and CC-BY-SA
URL:           http://wiki.gnome.org/Apps/Music
Source0:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/3.9/%{name}-%{version}.tar.xz

BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0) >= 1.35.9
BuildRequires: pkgconfig(grilo-0.2) >= 0.2.6
BuildRequires: pkgconfig(gtk+-3.0) >= 3.8.0
BuildRequires: python3-devel

Requires:      gdk-pixbuf2
Requires:      gobject-introspection
Requires:      grilo
Requires:      gstreamer1
Requires:      gstreamer1-plugins-base
Requires:      gtk3
Requires:      pango
Requires:      python3-gobject
Requires:      tracker

# Can't migrate to GDBus, the server-side support is not implemented yet:
#     https://bugzilla.gnome.org/show_bug.cgi?id=656330
Requires:      python3-dbus

# libgd is not meant to be installed as a system-wide shared library.
# It is just a way for GNOME applications to share widgets and other common
# code on an ad-hoc basis.
Provides:      bundled(libgd)
%global __provides_exclude_from ^%{_libdir}/%{name}/libgd\.so$

%description
Music player and management application for GNOME.


%prep
%setup -q


%build
%configure --disable-silent-rules
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p"

find %{buildroot} -name '*.la' -exec rm -f '{}' \;

%find_lang %{name}

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.Music.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_libdir}/%{name}
%{python3_sitelib}/gnomemusic


%changelog
* Wed Aug 21 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 3.9.90-2
- A couple of fixes, based on Ankur's feedback:
  - Fix the upstream URL
  - Fix the license tag
  - Validate the desktop file
  - Make the build verbose

* Wed Aug 21 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 3.9.90-1
- Initial package for Fedora.
