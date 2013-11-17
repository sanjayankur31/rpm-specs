Name:           deja-dup
Version:        23.2
Release:        1%{?dist}
Summary:        Simple backup tool and frontend for duplicity

Group:          Applications/Archiving
License:        GPLv3+
URL:            https://launchpad.net/deja-dup
Source0:        https://launchpad.net/deja-dup/24/%{version}/+download/%{name}-%{version}.tar.xz

# configure.ac lists libpeas-1.0, not libpeas >= 1.0. Corrected the configure
# script for this
#Patch0:         deja-dup-23.2-libpeas-require.patch

BuildRequires:  gettext desktop-file-utils intltool scrollkeeper
BuildRequires:  yelp-tools pango-devel cairo-devel vala-devel
BuildRequires:  libtool glib2-devel libnotify-devel
BuildRequires:  nautilus-devel libgnome-keyring-devel
BuildRequires:  gtk3-devel itstool
BuildRequires:  libpeas-devel >= 1.0
Requires:       duplicity >= 0.6.08 
Requires:       python-cloudfiles
Requires(post): /usr/bin/gtk-update-icon-cache
Requires(postun): /usr/bin/gtk-update-icon-cache

%description
Déjà Dup is a simple backup tool. It hides the complexity of doing backups the
'right way' (encrypted, off-site, and regular) and uses duplicity as the
backend.

Features: 
 • Support for local, remote, or cloud backup locations (Amazon S3 or Rackspace)
 • Securely encrypts and compresses your data
 • Incrementally backs up, letting you restore from any particular backup
 • Schedules regular backups
 • Integrates well into your GNOME desktop

%prep
%setup -q
#%patch0 -b.orig

%build
%configure --disable-static --with-nautilus --with-gnu-ld
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/nautilus/extensions-3.0/*.la

desktop-file-validate %{buildroot}/%{_datadir}/applications/deja-dup.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/deja-dup-preferences.desktop
desktop-file-validate %{buildroot}/%{_sysconfdir}/xdg/autostart/deja-dup-monitor.desktop

%find_lang %{name} --with-gnome

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc COPYING NEWS
%{_bindir}/deja-dup
%{_bindir}/deja-dup-preferences
%{_datadir}/applications/deja-dup-preferences.desktop
%{_mandir}/man1/deja-dup-preferences.1.gz
%{_mandir}/man1/deja-dup.1.gz
%{_mandir}/*/man1/deja-dup-preferences.1.gz
%{_mandir}/*/man1/deja-dup.1.gz
%{_datadir}/GConf/gsettings/deja-dup.convert
%{_datadir}/glib-2.0/schemas/org.gnome.DejaDup.gschema.xml
%{_sysconfdir}/xdg/autostart/deja-dup-monitor.desktop
%{_libdir}/nautilus/extensions-3.0/libdeja-dup.so
%{_libexecdir}/deja-dup/
%{_datadir}/applications/deja-dup.desktop
%{_datadir}/deja-dup/
%{_datadir}/icons/hicolor/*/apps/deja-dup.png
%{_datadir}/icons/hicolor/scalable/apps/deja-dup-symbolic.svg
%{_datadir}/icons/hicolor/scalable/devices/deja-dup-cloud.svg
%{_datadir}/help/*/deja-dup/

%changelog
* Sun Jun 17 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 23.2-1
- Update to 23.2
- Add libpeas as BR
- Add patch for libpeas

* Fri Jun  1 2012 Ville Skyttä <ville.skytta@iki.fi> - 20.2-3
- Own %%{_libexecdir}/deja-dup and %%{_datadir}/deja-dup dirs.

* Wed Mar 21 2012 Tom Callaway <spot@fedoraproject.org> - 20.2-2
- fix BuildRequires

* Wed Mar 21 2012 Richard Hughes <rhughes@redhat.com> - 20.2-1
- Update to 20.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 20.1-1
- New upstream release
- https://launchpad.net/deja-dup/+announcement/9065
- http://bazaar.launchpad.net/~deja-dup-hackers/deja-dup/20/view/1210/NEWS
- Fixes rhbz#748223
- validate deja-dup-monitor.desktop

* Tue Aug 23 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 19.90-1
- New upstream release
- https://launchpad.net/deja-dup/+announcement/8826
- http://bazaar.launchpad.net/~deja-dup-hackers/deja-dup/20/view/1141/NEWS
- Drop no longer needed build requires on po4a and unique-devel

* Sun Aug 07 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 19.5-1
- New upstream release
- Validate the preferences desktop file. Upstream bug reported by me lp:822312
- Drop BR on libxml2-python since itstool was fixed by me to add that dep

* Sun Aug 07 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 19.4-1
- New upstream release
- https://launchpad.net/deja-dup/+announcement/8715
- Upstream dropped Ubuntu specific icons per my bug report
- Dropped build requires on control-center-devel.  no longer exists
- Added build requires on itstool and libxml2-python
- Changed build requires from gnome-doc-utils to yelp-tools
- Add versioned requires on duplicity as per offlist mail from upstream
- Validate the primary desktop file
- Drop GConf entirely

* Sun Jun 26 2011 Jitesh Shah <jitesh.1337@gmail.com> - 19.3-1
- New upstream release (Mostly bugfixes and a couple of layout changes)
- https://launchpad.net/deja-dup/20/19.3
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/20/view/head:/NEWS

* Tue Jun 14 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 19.2.2-1
- New upstream release
- https://launchpad.net/deja-dup/20/19.2
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/20/view/head:/NEWS
- Drop build dependency on unique3-devel. No longer needed

* Mon May 09 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 19.1-1
- New upstream release
- Drop defattr since recent rpm makes it redundant 
- Add control-center-devel as build requires
- Update gsettings scriptlets to match latest guidelines
- Drop obsolete and invalid configuration options

* Sat Apr 16 2011 Chris Smart <csmart@fedoraproject.org> - 18.1.1-1
- Update to latest upstream release, which will "actually work with NetworkManager 0.9"
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/18/revision/888

* Wed Apr 13 2011 Chris Smart <csmart@fedoraproject.org> - 18.1-1
- Update to latest upstream release, 18.1
- https://launchpad.net/deja-dup/18/18.1

* Sat Apr 09 2011 Chris Smart <csmart@fedoraproject.org> - 18.0-1
- Update to latest upstream release, 18.0
- https://launchpad.net/deja-dup/18/18.0

* Wed Apr 06 2011 Dan Williams <dcbw@redhat.com> - 17.92-3
- Really fix for NM 0.9

* Wed Apr 05 2011 Dan Williams <dcbw@redhat.com> - 17.92-2
- Update for NetworkManager 0.9

* Sun Mar 27 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 17.92-1
- Update to latest upstream release
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/trunk/revision/863

* Tue Mar 17 2011 Chris Smart <csmart@fedoraproject.org> - 17.91-1
- Update to latest upstream release
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/trunk/revision/854

* Tue Mar 05 2011 Chris Smart <csmart@fedoraproject.org> - 17.90-1
- Update to latest upstream release
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/trunk/revision/838

* Tue Feb 15 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 17.6-3
- Rebuild against new GTK

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 17.6-2
- Rebuild against newer gtk

* Fri Feb 11 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 17.6-2
- Update build requirements

* Fri Feb 11 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 17.6-1
- Update to latest upstream release
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/trunk/revision/827
- Drop no longer needed nautilus extension related patch
- Enable GTK3 and Nautilus support unconditionally

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 17.5-1
- Update to 17.5

* Sat Jan 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 17.4-3
- Dir ownership fixes.

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 17.4-2
- Rebuild against new GTK+

* Tue Dec 28 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 17.4-1
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/trunk/annotate/761/NEWS
- Reorganize the backup location preferences to be more intuitive
- New Chinese (simplified) translation and other translation updates

* Fri Dec 04 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 17.3-1
- https://launchpad.net/deja-dup/+announcement/7341
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/trunk/revision/753#NEWS
- drop no longer needed libnotify patch

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 17.2-1
- Update to 17.2

* Fri Nov 12 2010 Adam Williamson <awilliam@redhat.com> - 17.1-1
- bump to 17.1
- adjust for use of gsettings
- add notify.patch to fix build against new libnotify

* Sun Jun 06 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 15.3-2
- Drop the dependency on yelp

* Sun Jun 06 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 15.3-1
- Several bug fixes including a potential data loss fix

* Sat May 08 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 15.1-1
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/trunk/revision/646#NEWS
- Reorganize help documentation to use new mallard format
- Change terminology for 'backup' verb to 'back up'
- Many new and updated translations
 
* Sat May 01 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 14.1-1
- https://launchpad.net/deja-dup/+announcement/5730
- Fix critical bugs preventing backup to external disks and restore single dir

* Sun Apr 18 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 14.0.3-1
- https://launchpad.net/deja-dup/+announcement/5630
- fix restoring to a non-empty directory

* Mon Apr 12 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 14.0.2-1
- https://launchpad.net/deja-dup/+announcement/5544
- drop the clean section

* Thu Apr 01 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 14.0-1
- new upstream release
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/14/annotate/head:/NEWS
- Gconf schema installation. Fixes rhbz #577004

* Mon Mar 20 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 13.92-1
- new upstream release
- https://launchpad.net/deja-dup/+announcement/5313

* Mon Mar 01 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 13.91-1
- new upstream release
- Fix review issues

* Tue Dec 22 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 13.4-1
- new upstream release
- http://bazaar.launchpad.net/~deja-dup-team/deja-dup/trunk/revision/557#NEWS

* Tue Dec 08 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 13.3-1
- new upstream release

* Tue Nov 23 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 11.1-1
- Initial spec
