Name:           gnote
Version:        3.7.3
Release:        5%{?dist}
Summary:        Note-taking application
Group:          User Interface/Desktops
License:        GPLv3+
URL:            http://live.gnome.org/Gnote
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gnote/3.7/%{name}-%{version}.tar.xz

# Built in mock but failed on koji with this error:
# /usr/bin/ld: note: '__pthread_key_create@@GLIBC_2.2.5' is defined in DSO
# /lib64/libpthread.so.0 so try adding it to the linker command line
# 
# Added -lpthread
Patch0:         gnote-3.7.3-dso-pthread.patch

BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gtkmm30-devel
BuildRequires:  gtkspell3-devel
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  libsecret-devel
BuildRequires:  libuuid-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  pcre-devel


%description
Gnote is a desktop note-taking application which is simple and easy to use.
It lets you organize your notes intelligently by allowing you to easily link
ideas together with Wiki style interconnects. It is a port of Tomboy to C++ 
and consumes fewer resources.

%prep
%setup -q
%patch0

%build
%configure --disable-static --with-gnu-ld
V=1 make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# A missing semi colon
sed -i 's/\(Keywords\[sl\]=.*$\)/\1;/' %{buildroot}%{_datadir}/applications/gnote.desktop

desktop-file-validate %{buildroot}%{_datadir}/applications/gnote.desktop

find %{buildroot} -type f -name "*.la" -delete

%find_lang %{name} --with-gnome

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/sbin/ldconfig

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc COPYING README TODO NEWS AUTHORS
%{_bindir}/gnote
%{_mandir}/man1/gnote.1.gz
%{_datadir}/applications/gnote.desktop
%{_datadir}/gnote/
%{_datadir}/icons/hicolor/*/apps/gnote.png
%{_datadir}/icons/hicolor/scalable/apps/gnote.svg
%{_prefix}/%{_lib}/gnote/
%{_prefix}/%{_lib}/libgnote*
%{_datadir}/dbus-1/services/org.gnome.Gnote.service
%{_datadir}/glib-2.0/schemas/org.gnome.gnote.gschema.xml

%changelog
* Thu Mar 07 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.7.3-5
- Update patch, retry build

* Tue Mar 05 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.7.3-4
- Spec bump, update patch, retry build

* Tue Mar 05 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.7.3-3
- Spec bump

* Tue Mar 05 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.7.3-2
- Add patch for missing -lpthread that broke koji build

* Tue Mar 05 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.7.3-1
- Update to 3.7.3 rhbz#917584
- Add gtkspell3 to BR for spell check support

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.7.2-1
- Update to latest: 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.0-1
- Update to 3.7.0

* Wed Sep 26 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0
- Use desktop-file-validate

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul  8 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.1-1
- update to 0.9.1
- http://ftp.gnome.org/pub/GNOME/sources/gnote/0.9/gnote-0.9.1.news

* Thu Mar 29 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 0.9.0-1
- update to 0.9.0
- https://mail.gnome.org/archives/gnote-list/2012-March/msg00000.html

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 0.8.2-3
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.8.2-1
- update to 0.8.2
- https://mail.gnome.org/archives/gnote-list/2011-December/msg00001.html

* Sun Oct 24 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.8.0-2
- Update scriplets for gsettings schema and icon cache. Fixes rhbz#743580
- Drop obsolete dependency on Gconf and dbus-c++-devel
- Update build requires to gtkmm30-devel instead of gtkmm24-devel
- Fix source url

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Tue Aug 02 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.5-1
- New upstream release
- http://mail.gnome.org/archives/gnote-list/2011-July/msg00001.html
- Drop all patches since they are now upstream

* Sun May 01 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.4-1
- New upstream bug fix release
- http://mail.gnome.org/archives/gnote-list/2011-April/msg00011.html
- Drop couple of no longer needed patches

* Sun Apr 17 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.3-9
- Rebuilt for Boost soname bump
- Added rarian-compat as build requires

* Thu Feb 10 2011 Bastien Nocera <bnocera@redhat.com> 0.7.3-8
- Make sure that gnote shows up on first launch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb  6 2011 Michel Salim <salimma@fedoraproject.org> - 0.7.3-6
- Rebuild for Boost 1.46

* Thu Feb 03 2011 Bastien Nocera <bnocera@redhat.com> 0.7.3-5
- Disable panel applet
- Rebuild against newer GTK+
- Add patch from Petr Machata <pmachata@redhat.com> to fix the build

* Fri Dec 17 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.3-4
- Add the patch

* Fri Dec 17 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.3-3
- Fix gnote losing add-in status when running as app
- Resolves rhbz#654562

* Sat Nov 06 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.3-2
- Explicit build requires on libxslt-devel

* Sat Nov 06 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.3-1
- New upstream bug fix release with translation updates
- http://mail.gnome.org/archives/gnote-list/2010-November/msg00002.html
- Drop backported patch

* Fri Jul 30 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.2-2
- Rebuild for Boost 1.44
- Drop the clean section

* Fri Mar 12 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.2-1
- Ability to search for phrases, prompt while renaming notes, bug fixes
- Add a patch from upstream master to replace deprecated macros 
- Drop upstreamed patch to fix dso linking
- http://mail.gnome.org/archives/gnote-list/2010-March/msg00010.html

* Tue Feb 16 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.1-3
- Fix implicit DSO linking (thanks to Ankur Sinha)
- Fixes bz#564774

* Wed Jan 20 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.1-2
- Rebuild for new Boost soname bump

* Tue Jan 05 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.1-1
- Mostly minor bug fixes
- http://mail.gnome.org/archives/gnote-list/2010-January/msg00004.html

* Fri Jan 01 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.0-1
- Add a Note of the Day addin, addins can be disabled now
- http://mail.gnome.org/archives/gnote-list/2009-December/msg00013.html

* Tue Dec 29 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.3-3
- Upstream patches adding a fix for Bugzilla add-in and other minor bug fixes

* Tue Dec 22 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.3-2
- Several patches from upstream for additional translations
- Gnote now confirm to XDG specification

* Tue Dec 01 2009 Bastien Nocera <bnocera@redhat.com> 0.6.3-1
- Update to 0.6.3

* Thu Aug 13 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.2-1
- Very minor bug fixes
- http://mail.gnome.org/archives/gnote-list/2009-August/msg00006.html

* Sat Aug 01 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.1-1
- D-Bus support enabled, many new features and bug fixes
- http://mail.gnome.org/archives/gnote-list/2009-July/msg00016.html
- 0.6.0 skipped due to applet breakage fixed in this release
- http://mail.gnome.org/archives/gnote-list/2009-July/msg00020.html

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.3-1
- Few minor bug fixes
- http://mail.gnome.org/archives/gnote-list/2009-July/msg00002.html

* Sat Jul 04 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.2-2
- Build requires libuuid-devel instead of e2fsprogs-devel

* Sat Jul 04 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.2-1
- New upstream bug fix release
- http://mail.gnome.org/archives/gnote-list/2009-July/msg00000.html

* Thu Jun 25 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.1-1
- Fixes a regression and some bugs
- http://mail.gnome.org/archives/gnote-list/2009-June/msg00002.html

* Wed Jun 17 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.0-1
- Adds the ability to import Tomboy notes on first run 
- http://mail.gnome.org/archives/gnote-list/2009-June/msg00000.html
 
* Thu May 28 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.4.0-1
- Many minor bug fixes from new upstream release
  http://www.figuiere.net/hub/blog/?2009/05/27/670-gnote-040

* Wed May 06 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.3.1-1
- new upstream release. Fixes rhbz #498739. Fix #499227

* Fri May 01 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.3.0-1
- new upstream release. Includes applet and more plugins.

* Fri Apr 24 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.0-2
- enable spell checker

* Thu Apr 23 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.0-1
- new upstream release

* Thu Apr 16 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.2-2
- Add BR on gnome-doc-utils

* Wed Apr 15 2009 Jesse Keating <jkeating@redhat.com> - 0.1.2-1
- Update to 0.1.2 to fix many upstream bugs
  http://www.figuiere.net/hub/blog/?2009/04/15/660-gnote-012

* Fri Apr 10 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-4
- Drop a unnecessary require, BR and fix summary

* Wed Apr 08 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-3
- Fix review issues

* Wed Apr 08 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-2
- include pre script for gconf schema

* Wed Apr 08 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.1-1
- Initial spec file

