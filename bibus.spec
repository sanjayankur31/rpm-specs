%global debug_package %{nil}

Name:           bibus
Version:        1.5.2
Release:        1%{?dist}
Summary:        Bibliographic and reference management software

Group:          Applications/Publishing
License:        GPLv2+
URL:            http://bibus-biblio.sourceforge.net/
Source0:        http://downloads.sourceforge.net/bibus-biblio/%{name}_%{version}.orig.tar.gz

#Patch0:		%{name}-build-1.5.1.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
## temporarily removing noarch to workaround this bug:
##  https://bugzilla.redhat.com/show_bug.cgi?id=438527
## also filed with bibus upstream: 
##  http://sourceforge.net/tracker/index.php?func=detail&aid=1989580&group_id=110943&atid=657832
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
Requires:       wxPython > 2.6
Requires:       MySQL-python
Requires:       libreoffice-writer
Requires:       libreoffice-pyuno


%description
Bibus is a bibliographic database. It uses a MySQL or SQLite database
to store references. It can directly insert references in
LibreOffice and MS Word and generate the bibliographic index.


%prep
%setup -q -n %{name}-%{version}
#%patch0 -p0

## make files UTF-8 
for i in bibMSW.htm eTBlast\ Interface\ to\ Bibus.htm
do
  /usr/bin/iconv -f iso8859-1 -t utf-8 "Docs/html/en/${i}" > "Docs/html/en/${i}.conv" && /bin/mv -f "Docs/html/en/${i}.conv" "Docs/html/en/${i}"
done

## remove all CVS version control files
find . -type d -name CVS -print0 | xargs --null rm -rf

##  fix line endings
##find Docs -type f -exec sed -i 's/\r//' {} 2>/dev/null ';'
find Docs -type f -name '*ml' -exec sed -i 's/\r//' {} 2>/dev/null ';'

## remove she-bang lines in .py files to keep rpmlint happy
find . -type f -name "*.py" -exec sed -i '/^#![ ]*\/usr\/bin\/.*$/ d' {} 2>/dev/null ';'

## restore she-bang line for bibusStart.py
sed -i '1i #!/usr/bin/env python' bibusStart.py

## remove non-standard zh_cn locale directory
rm -r locale/zh_cn

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT/%{_prefix} sysconfdir=$RPM_BUILD_ROOT/etc \
 oopath=%{_libdir}/libreoffice/program/ ooure=%{_libdir}/libreoffice/ure/lib \
 oobasis=%{_libdir}/libreoffice/basis-link/program  install

## fix symlink
rm $RPM_BUILD_ROOT%{_bindir}/bibus
ln -s %{_datadir}/%{name}/bibusStart.py $RPM_BUILD_ROOT%{_bindir}/bibus

## fix location of doc directory to include version
mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name} $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

## also install ScreenShots subdirectory, missed by Makefile
install -d $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/html/ScreenShots/
install -m644 Docs/html/ScreenShots/*.png $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/html/ScreenShots/

## fix bibus.cfg to remove $RPM_BUILD_ROOT
sed -i "s:$RPM_BUILD_ROOT::" $RPM_BUILD_ROOT%{_datadir}/%{name}/bibus.cfg

## fix bibus.cfg to fix documentation location
sed -i "s:doc/bibus:doc/bibus-%{version}:" $RPM_BUILD_ROOT%{_datadir}/%{name}/bibus.cfg

## remove uninstall program, not necessary for RPM package
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/Setup/uninstall.sh

desktop-file-install --vendor="fedora"               \
     --delete-original                               \
     --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
     --remove-category="Application"                 \
     ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%{find_lang} %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}-%{version}
%{_bindir}/bibus
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/48x48/apps/*
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/*


%changelog
* Wed Mar 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.5.2-1
- Update to upstream release

* Wed Feb  8 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.1-7
- Remove python-sqlite2 dep as bibus can use the sqlite3 module from the stdlib

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 30 2010 Caolán McNamara <caolanm@redhat.com> - 1.5.1-4
- rebuild against LibreOffice

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 1.5.1-3
- recompiling .py files against Python 2.7 (rhbz#623278)

* Mon Mar  8 2010 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.1-2
- Disable debuginfo package (#547493)

* Wed Dec  9 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.1-1
- Update to latest upstream (1.5.1)
- Should fix connection problem with newer OpenOffice.org (#545809)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.3.1-2
- Fix paths to openoffice (#479099)

* Mon Dec  1 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.3.1-1
- Updating to new upstream (1.4.3.1)
- Adds support for OpenOffice 3.x
- Add patch to fix broken Makefile and desktop file
- Cleanup .spec

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.4.3-2
- Rebuild for Python 2.6

* Tue Jun 10 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.3-1
- Update to latest upstream (1.4.3)
- Make package arch-specific to allow package to find appropriate location
  for x86_64 (#438527)
- Fix PNG corruption introduced by fixing line-feeds, patch thanks to 
  Nicolas Thierry-Mieg (#448483)
- Add missing images to doc

* Thu Mar 13 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.1-4
- Require python-sqlite2, not sqlite

* Thu Mar 13 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.1-3
- Fix desktop-file-install as per review (#436619)

* Wed Mar 11 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.1-2
- Require sqlite for sqlite backend

* Sat Mar  8 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.4.1-1
- Initial Fedora package

