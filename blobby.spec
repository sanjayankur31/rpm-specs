%global svn_rev 1541
Name:           blobby
Version:        1.0
Release:        1svn%{svn_rev}%{?dist}
Summary:        Volley-ball game
Group:          Amusements/Games
License:        GPLv2+
URL:            http://blobby.sourceforge.net
# Version 1 is broken. Upstream suggested I use the svn checkout.
#Source0:        http://downloads.sourceforge.net/%{name}/%{name}2-linux-%{version}.tar.gz
# svn export -r 1541  svn://svn.code.sf.net/p/blobby/code/trunk blobby-1.0svn1541
# tar -cvzf blobby-1.0svn1541.tar.gz blobby-1.0svn1541/
Source0:        %{name}-%{version}svn%{svn_rev}.tar.gz
Source1:        blobby.desktop
Source2:        blobby.appdata.xml

BuildRequires:  SDL2-devel, physfs-devel, zlib-devel, cmake, boost-devel, zip
BuildRequires:  ImageMagick, desktop-file-utils, hicolor-icon-theme
BuildRequires:  pkgconfig

%description
Blobby Volley is one of the most popular freeware games.
Blobby Volley 2 is the continuation of this lovely game.

%prep
%setup -q -n %{name}-%{version}svn%{svn_rev}

# Updated to SDL2 but still looks for SDL also? Why!
sed -ibackup '/find_package(SDL REQUIRED)/d' src/CMakeLists.txt

%build
%cmake .
make %{?_smp_mflags}

%install
%make_install

# Icon
# unzip -o -j data/gfx.zip gfx/ball01.bmp
convert -size 48x48 -transparent black data/Icon.bmp blobby.png
install -p -m 644 -D blobby.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/blobby.png

# Desktop file
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata/
install -p -m 644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/appdata/blobby.appdata.xml

%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%files
%doc AUTHORS README ChangeLog COPYING TODO
%{_bindir}/*
%{_datadir}/blobby
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/applications/*.desktop
%dir %{_datadir}/appdata/
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Tue Sep 16 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.0-1svn1541
- Update to lastest available code

* Mon Aug 18 2014 Richard Hughes <richard@hughsie.com> - 1.0-0.11.rc4
- Add a one line summary to the desktop file so that the application appears
  in GNOME Software and Apper.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.10.rc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.9.rc4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 1.0-0.8.rc4
- Rebuild for boost 1.55.0

* Tue Dec 03 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0-0.7.rc4
- Update to rc4
- Add appdata file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 1.0-0.5.rc3
- Rebuild for boost 1.54.0

* Wed Feb 13 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.0-0.4.rc3
- update to 1.0rc3
- drop obsolete gcc patch
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- use make_install macro

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 21 2012 Tom Callaway <spot@fedoraproject.org> - 1.0-0.1.rc1
- update to 1.0rc1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9c-3
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec  9 2011 Tom Callaway <spot@fedoraproject.org> - 0.9c-1
- 0.9c

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 23 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9b-1
- new release

* Sun Mar 07 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8-3.20100306svn
- made corrections to spec : release field

* Sun Mar 07 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8-2.20100306svn
- made corrections to spec : release field

* Sun Mar 07 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8-0.1.20100306svn
- cleaned up spec
- corrected desktop file
- corrected svn versioning

* Sat Mar 06 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20100306-1
- Update version

* Fri Feb 19 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.6-0.14.a
- Fix lpthread issue for FTBFS implicit DSO linkage 564611

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-0.13.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.11.a
- add ARM patch, thanks to Kedar Sovani

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-0.11.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.10.a
- update Summary to comply with the guidelines

* Thu Jun 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.9.a
- fix build with gcc 4.3 (patch1)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6-0.8.a
- Autorebuild for GCC 4.3

* Sun Oct 07 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.7.a
- detect OpenGL using opengl-games-utils

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.6.a
- fix license tag again: if no version is specified, any version can be
  chosen (see http://fedoraproject.org/wiki/Licensing)

* Sat Aug 25 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.5.a
- rebuild for BuildID
- fix license tag

* Sun Jan 14 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.4.a
- patch configure instead of configure.in

* Sun Jan 14 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.3.a
- patch it to obey RPM_OPT_FLAGS

* Sun Jan 14 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.2.a
- add dependency on hicolor-icon-theme (#222547)
- removed the "Application" category from the desktop file

* Fri Jan 12 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.6-0.1.a
- initial package
