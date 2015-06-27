Name:           scribus
Version:        1.4.5
Release:        2%{?dist}
Summary:        DeskTop Publishing application written in Qt
Group:          Applications/Productivity
License:        GPLv2+
URL:            http://www.scribus.net/
# ./make-free-archive %{version}
SOURCE0:        %{name}-%{version}-free.tar.xz
#Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
#Source1:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz.asc

# Icons from svn checkout
# svn checkout svn://scribus.net/trunk/Scribus
# mkdir scribus-icons/{16x16,32x32,128x128,256x256,512x512,1024x1024}/apps -p
# for i in "16x16" "32x32" "128x128" "256x256" "512x512" "1024x1024"
# do
# cp Scribus/resources/iconsets/artwork/*"$i".png # scribus-icons/"$i"/apps/scribus.png
# done
# tar -cvJf scribus-icons.tar.xz scribus-icons
SOURCE1:        %{name}-icons.tar.xz

Patch1:         %{name}-1.4.4-qreal_double.patch
# fix build with non-free content removed
Patch2:         %{name}-1.4.2-nonfree.patch
# Fix necessary LPPL attribution
Patch3:         %{name}-1.4.5-lppl-fixes.patch

BuildRequires:  cmake
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  lcms2-devel
BuildRequires:  libart_lgpl-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  python-devel
BuildRequires:  python-imaging-devel
BuildRequires:  qt4-devel
BuildRequires:  zlib-devel
BuildRequires:  freetype-devel
BuildRequires:  gnutls-devel
BuildRequires:  cairo-devel
BuildRequires:  hunspell-devel
BuildRequires:  boost-devel
BuildRequires:  podofo-devel
BuildRequires:  hyphen-devel
Requires:       ghostscript
Requires:       python
Requires:       python-imaging
Requires:       tkinter
Requires:       shared-mime-info
Requires:       hicolor-icon-theme
Obsoletes:      %{name}-doc < %{version}-%{release}
Obsoletes:      %{name}-devel < %{version}-%{release}

%filter_provides_in %{_libdir}/%{name}/plugins
%filter_setup


%description
Scribus is an desktop open source page layout program with
the aim of producing commercial grade output in PDF and
Postscript, primarily, though not exclusively for Linux.

While the goals of the program are for ease of use and simple easy to
understand tools, Scribus offers support for professional publishing
features, such as CMYK color, easy PDF creation, Encapsulated Postscript
import/export and creation of color separations.


%prep
%setup -q
cp -v %SOURCE1 .
tar -xvf %{name}-icons.tar.xz

%patch1 -p1 -b .double
%patch2 -p1 -b .nonfree
%patch3 -p1

# recode man page to UTF-8
pushd scribus/manpages
iconv -f ISO8859-2 -t UTF-8 scribus.1.pl > tmp
touch -r scribus.1.pl tmp
mv tmp scribus.1.pl
popd

# fix permissions
chmod a-x scribus/pageitem_latexframe.h

# drop shebang lines from python scripts
for f in scribus/plugins/scriptplugin/{samples,scripts}/*.py
do
    sed '1{/#!\/usr\/bin\/env\|#!\/usr\/bin\/python/d}' $f > $f.new
    touch -r $f $f.new
    mv $f.new $f
done


%build
mkdir build
pushd build
%cmake -DWANT_DISTROBUILD=YES -DWANT_HUNSPELL=YES -DWANT_NOHEADERINSTALL=YES ..

make VERBOSE=1 %{?_smp_mflags}
popd


%install
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd

install -p -D -m0644 ${RPM_BUILD_ROOT}%{_datadir}/scribus/icons/scribus.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/scribus.png
install -p -D -m0644 ${RPM_BUILD_ROOT}%{_datadir}/scribus/icons/scribusdoc.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/x-scribus.png

for iconsize in "16x16" "32x32" "128x128" "256x256" "512x512" "1024x1024"
do
    install -p -D -m0644 %{name}-icons/"$iconsize"/apps/%{name}.png ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/"$iconsize"/apps/%{name}.png
done

find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'

# install the global desktop file
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mimelnk/application/*scribus.desktop
desktop-file-install \
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
    --vendor="fedora"                      \
%endif
    --dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
    scribus.desktop

# remove unwanted stuff
rm -rf ${RPM_BUILD_ROOT}%{_defaultdocdir}/%{name}

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: http://bugs.scribus.net/view.php?id=12708
SentUpstream: 2014-09-18
-->
<application>
  <id type="desktop">scribus.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Scribus is a desktop publishing application that allows you to create posters,
      magazines and books ready to send off to a printing house.
      It supports professional publishing features, such color separations, CMYK and
      spot colors, ICC color management, and versatile PDF creation.
    </p>
    <!-- FIXME: Probably needs another paragraph or two -->
  </description>
  <url type="homepage">http://scribus.net/</url>
  <screenshots>
    <screenshot type="default">http://upload.wikimedia.org/wikipedia/commons/f/f4/Scribus-1.3-Linux.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

%post
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-desktop-database &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

fi

%posttrans
update-desktop-database &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :



%files
%doc AUTHORS ChangeLog COPYING LINKS README
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/appdata/*%{name}.appdata.xml
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/*
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude %{_datadir}/%{name}/samples/*.py[co]
%exclude %{_datadir}/%{name}/scripts/*.py[co]
%{_mandir}/man1/*
%{_mandir}/pl/man1/*
%{_mandir}/de/man1/*


%changelog
* Sat Jun 27 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.4.5-2
- Added icons from 1.5 tree
- Fix changelog entries with incorrect date entries

* Thu May  7 2015 Tom Callaway <spot@fedoraproject.org> 1.4.5-1
- update to 1.4.5
- drop non-free and questionable hyphen dic files (bz 1219415)
- fix necessary LPPL attributions

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1.4.4-7
- Add an AppData file for the software center

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.4.4-6
- Rebuild for boost 1.57.0

* Thu Aug 28 2014 Dan Horák <dan[at]danny.cz> - 1.4.4-5
- switch to Debian patch for the qreal vs double conflict on ARM (fixes #1076885)

* Wed Aug 20 2014 Kevin Fenzi <kevin@scrye.com> - 1.4.4-4
- Rebuild for rpm bug 1131892

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1.4.4-2
- optimize/update scriptlets

* Fri Jun  6 2014 Tom Callaway <spot@fedoraproject.org> - 1.4.4-1
- update to 1.4.4, drop non-free dot files

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.4.3-3
- Rebuild for boost 1.55.0

* Thu Sep 19 2013 Dan Horák <dan[at]danny.cz> - 1.4.3-2
- fix the double patch (#1009979)

* Mon Aug 19 2013 Dan Horák <dan[at]danny.cz> - 1.4.3-1
- update to 1.4.3 (#990030)
- update for unversioned docdir

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 1.4.2-6
- Rebuild for boost 1.54.0

* Mon Feb 25 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4.2-5
- Remove --vendor from desktop-file-install for F19+ https://fedorahosted.org/fesco/ticket/1077

* Wed Jan 30 2013 Dan Horák <dan[at]danny.cz> - 1.4.2-4
- update for Pillow (#896301)

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.4.2-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Jan 18 2013 Dan Horák <dan[at]danny.cz> - 1.4.2-2
- use hunspell to be consistent with the rest of the system

* Tue Jan 15 2013 Dan Horák <dan[at]danny.cz> - 1.4.2-1
- update to 1.4.2
- remove non-free content from source archive (#887221)
- drop doc and devel sub-packages
- switch to lcms2

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.4.1-4
- rebuild against new libjpeg

* Thu Aug  9 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.1-3
- Add patch to fix FTBFS on ARM

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 06 2012 Dan Horák <dan[at]danny.cz> - 1.4.1-1
- update to 1.4.1

* Wed Mar 07 2012 Dan Horák <dan[at]danny.cz> - 1.4.0-5
- fix crash at export as image (rhbz#800765)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Dan Horák <dan[at]danny.cz> - 1.4.0-2
- the swatches/profiles patches were submitted to upstream bugtracker

* Mon Jan 02 2012 Dan Horák <dan[at]danny.cz> - 1.4.0-1.1
- install profiles and swatches to datadir
- use versioned docdir

* Mon Jan 02 2012 Dan Horák <dan[at]danny.cz> - 1.4.0-1
- update to 1.4.0

* Fri Jun 24 2011 Dan Horák <dan@danny.cz> - 1.3.9-6
- fix build with cups 1.5 (#716107)

* Wed May 04 2011 Dan Horák <dan@danny.cz> - 1.3.9-5
- rebuilt against podofo 0.9.1

* Thu Apr 14 2011 Dan Horák <dan@danny.cz> - 1.3.9-4
- rebuilt against podofo 0.9.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Dan Horák <dan[AT]danny.cz> - 1.3.9-2
- run update-desktop-database in scriptlets too (#664318)

* Tue Nov 30 2010 Dan Horák <dan[AT]danny.cz> - 1.3.9-1
- update to 1.3.9
- filter unwanted Provides

* Wed Nov 03 2010 Dan Horák <dan@danny.cz> - 1.3.8-3
- rebuilt against podofo 0.8.4

* Fri Oct 22 2010 Dan Horák <dan@danny.cz> - 1.3.8-2
- rebuilt against podofo 0.8.3

* Mon Aug 16 2010 Dan Horák <dan[AT]danny.cz> - 1.3.8-1
- update to 1.3.8

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Dan Horák <dan[AT]danny.cz> - 1.3.7-4
- fix crash when selecting frame (#604124)

* Tue Jun 15 2010 Dan Horák <dan[AT]danny.cz> - 1.3.7-3
- show icons in shapes menu (#603921)

* Tue Jun 08 2010 Dan Horák <dan[AT]danny.cz> - 1.3.7-2
- rebuilt with podofo 0.8.1

* Tue Jun  1 2010 Dan Horák <dan[AT]danny.cz> - 1.3.7-1
- update to final 1.3.7

* Thu Apr 29 2010 Dan Horák <dan[AT]danny.cz> - 1.3.6-4
- fix build with podofo 0.8.0

* Thu Apr 29 2010 Dan Horák <dan[AT]danny.cz> - 1.3.6-3
- rebuilt for podofo 0.8.0

* Wed Mar 31 2010 Dan Horák <dan[AT]danny.cz> - 1.3.6-2
- added 2 patches for rawhide

* Mon Mar 29 2010 Dan Horák <dan[AT]danny.cz> - 1.3.6-1
- update to final 1.3.6

* Wed Nov 25 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5.1-5
- fixed a crash when closing a hyphenator object (#537677)

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.5.1-4
- rebuilt with new openssl

* Tue Aug 25 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5.1-3
- drop shebang line from python scripts
- don't package precompiled python scripts

* Thu Aug 20 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5.1-1
- update to final 1.3.5.1
- drop the upstreamed "install-headers" patch
- always install doc subpackage (#446148)
- full changelog: http://www.scribus.net/?q=node/193

* Wed Jul 29 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.17.rc3
- don't use parallel build on s390x

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-0.16.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.15.rc3
- update to 1.3.5-rc3
- use system hyphen library (#506074)
- fix update path for the doc subpackage (#512498)
- preserve directories when installing headers (#511800)

* Thu Jun  4 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.14.rc2
- update to 1.3.5-rc2

* Mon May 18 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.13.beta
- rebuilt with podofo enabled

* Wed Apr 22 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.12.beta
- update to 1.3.5.beta
- make docs subpackage noarch
- drop outdated Obsoletes/Provides

* Sun Mar 29 2009 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.11.20090329svn13359
- update to revision 13359
- add aspell-devel and boost-devel as BR
- update release tag to conform to the pre-release versioning guideline

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-0.10.12516svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.4-0.9.12516svn
- rebuild with new openssl

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.5-0.8.12516svn
- Rebuild for Python 2.6

* Tue Dec  2 2008 Dan Horák <dan[AT]danny.cz> - 1.3.5-0.7.12516svn
- fix directory ownership in doc subpackage (#474041)

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.5-0.6.12516svn
- Rebuild for Python 2.6

* Mon Oct 13 2008 Dan Horák <dan[AT]danny.cz> 1.3.5-0.5.12516svn
- install global desktop file instead of KDE-only one (#461124)
- little cleanup

* Fri Sep 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-0.4.12516svn
- new svn snapshot

* Sun Jul 27 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-0.3.12419svn
- new svn snapshot

* Mon Jul 21 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-0.2.12404svn
- svn snapshot

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.4-5
- Autorebuild for GCC 4.3

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 1.3.4-4
- Rebuilt for gcc43

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.4-3
- fix inclusion of python scripts as proposed by Todd Zullinger (#312091)
- fix desktop file

* Thu Aug 23 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.4-2
- rebuild for buildid
- new license tag

* Sat Jun 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.4
- version upgrade

* Mon Dec 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.6-1
- version upgrade

* Sat Nov 11 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.5-1
- version upgrade

* Wed Oct 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.4-1
- version upgrade

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.3-1
- version upgrade (#205962)

* Sun Jun 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.2-2
- bump

* Tue May 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.2-1
- version upgrade

* Sat Apr 22 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3.1-1
- version upgrade

* Tue Mar 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.3-1
- version upgrade
- add BR gnutls-devel

* Sat Mar 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.3.2-1
- upgrade to beta version

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.2.4.1-4
- Rebuild for Fedora Extras 5

* Wed Feb 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.2.4.1-3
- add missing requires python-imaging

* Sat Jan 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.2.4.1-2
- rebuild (#178494)

* Wed Jan 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.2.4.1-1
- version upgrade

* Thu Jul 7 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.2.1-2
- use dist tag for sanity between branches

* Tue Jul 5 2005 P Linnell <mrdocs AT scribus.info> - 1.2.2.1-1
- 1.2.2.1 released to fix crash on open with certain 1.2.1 docs

* Sun Jul 3 2005 P Linnell <mrdocs AT scribus.info> - 1.2.2-0.fc4
- 1.2.2 final

* Tue Jun 28 2005 P Linnell <mrdocs AT scribus.info>- 1.2.2cvs-0
- test build for 1.2.2cvs
- Add freetype2 explicit build requirement
- Add obsoletes. See PACKAGING in the source tarball
- Change the description per PACKAGING
- Bump required python. 2.2 is no longer supported.


* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.2.1-5
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 06 2005 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2.1-3
- Bumped BR on qt-devel to 3.3.

* Thu Feb  3 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.1-2
- Fix x86_64 build and summary.

* Sun Jan 09 2005 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2.1-1
- 1.2.1.

* Sat Dec 04 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2.1-0.1.cvs20041118
- cvs snapshot.

* Thu Nov 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2-0.fdr.3
- Redirect output in post/postun, to avoid failure.

* Wed Nov 10 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 1.2-0.fdr.2
- Mime-type corrections for FC3.
- Dropped redundent BR XFree86-devel.

* Thu Aug 26 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.2-0.fdr.1
- 1.2.
- Dropping old obsoletes/provides (don't know of anyone using them).

* Thu Aug 19 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.2-0.fdr.0.RC1
- 1.2RC1.

* Sat Aug 07 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.7-0.fdr.4
- mime info/icon for .sla files.

* Sat Jul 10 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.7-0.fdr.3
- BuildReq openssl-devel (#1727).

* Thu Jun 10 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.7-0.fdr.2
- Source0 allows direct download (#1727).
- Req tkinter (#1727).

* Sun Jun 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.7-0.fdr.1
- Updated to 1.1.7.
- Re-added _smp_mflags.

* Mon May 24 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.6-0.fdr.3
- Add Application Category to desktop entry.

* Sun Apr 11 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.6-0.fdr.2
- Bump ghostscript Req to 7.07.
- URL scribus.net.

* Tue Apr 06 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.6-0.fdr.1
- Updated to 1.1.6.
- Using upstream desktop entry.

* Sat Feb 14 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.5-0.fdr.1
- Updated to 1.1.5.

* Sun Dec 21 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.4-0.fdr.1
- Updated to 1.1.4.

* Thu Dec 04 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.3-0.fdr.2
- Dropped LDFLAGS="-lm"
- Added --with-pythondir=%%{_prefix}
- Req ghostscript.

* Sun Nov 30 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.3-0.fdr.1
- Updated to 1.1.3.
- Removed _smp_mflags.

* Tue Nov 18 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.2-0.fdr.2
- Req python.
- Provides scribus-scripting.

* Sun Nov 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.2-0.fdr.1
- Updated to 1.1.2.
- Obsoletes scribus-scripting.

* Sat Oct 11 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.1-0.fdr.2
- BuildReq littlecms-devel -> lcms-devel.

* Thu Oct 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.1.1-0.fdr.1
- Updated to 1.1.1.
- BuildReq littlecms-devel.
- BuildReq libart_lgpl-devel.

* Wed Sep 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0.1-0.fdr.1
- Updated to 1.0.1.
- Split off devel package for headers.
- No longer Obsoletes scribus-i18n-en

* Thu Jul 24 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0-0.fdr.3
- desktop entry terminal=0 -> false.

* Tue Jul 15 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0-0.fdr.2
- Added Obsoletes scribus-i18n-en.

* Tue Jul 15 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0-0.fdr.1
- Updated to 1.0.

* Tue Jul 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.0-0.fdr.0.1.rc1
- Updated to 1.0RC1.

* Fri Jun 20 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.11.1-0.fdr.1
- Updated to 0.9.11.1.
- Added obsoletes scribus-svg.

* Sun May 25 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.10-0.fdr.3
- Using make DESTDIR= workaround for plugin issue.
- Removed post/postun ldconfig.
- Removed devel subpackage.

* Mon May 19 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.10-0.fdr.2
- Explicitly set file permission on icon.
- Created devel package.
- Removed .la files.
- Added ChangeLog to Documentation.

* Sun May 18 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.10-0.fdr.1
- Updated to 0.9.10.
- buildroot -> RPM_BUILD_ROOT.

* Sat Apr 26 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.9-0.fdr.3
- Added BuildRequires for cups-devel.

* Thu Apr 24 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.9-0.fdr.2
- Added BuildRequires for libtiff-devel.
- Added line to help package find tiff.

* Sun Apr 20 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.9-0.fdr.1
- Updated to 0.9.9.
- Added line for QT.

* Thu Apr 10 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.8-0.fdr.3.rh90
- Added missing BuildRequires.
- Corrected Group.

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.9.8-0.fdr.2
- Added desktop-file-utils to BuildRequires.
- Changed category to X-Fedora-Extra.
- Added Epoch:0.

* Thu Mar 27 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.9.8-0.fdr.1
- Initial RPM release.
