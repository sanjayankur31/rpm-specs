Name:		byobu
Version:	5.17
Release:	1%{?dist}
Summary:	Light-weight, configurable window manager built upon GNU screen

Group:		Applications/System
License:	GPLv3
URL:		http://launchpad.net/byobu
Source0:	http://code.launchpad.net/byobu/trunk/%{version}/+download/byobu_%{version}.orig.tar.gz
# default windows
Source1:	fedoracommon
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
%if 0%{?rhel}%{?fedora} > 5
Requires:	python >= 2.5
%else
Requires:	python26
%endif

BuildRequires:	gettext, desktop-file-utils, automake
Requires:	screen, newt, gettext

%Description
Byobu is a Japanese term for decorative, multi-panel screens that serve 
as folding room dividers. As an open source project, Byobu is an 
elegant enhancement of the otherwise functional, plain, 
practical GNU Screen. Byobu includes an enhanced profile 
and configuration utilities for the GNU screen window manager, 
such as toggle-able system status notifications.

%prep
%setup -q
# remove swap file
if [ -e "usr/bin/.byobu-status-print.swp" ]; then rm usr/bin/.byobu-status-print.swp
fi
# fix path for lib directory in scripts
for i in `grep -Ri {BYOBU_PREFIX}/lib/ * | awk -F: '{print $1}' | uniq`; do
sed -i "s#{BYOBU_PREFIX}/lib/#{BYOBU_PREFIX}/libexec/#g" $i;
done
for i in `grep -Ri BYOBU_PREFIX/lib/ * | awk -F: '{print $1}' | uniq`; do
sed -i "s#BYOBU_PREFIX/lib/#BYOBU_PREFIX/libexec/#g" $i;
done
# fix path for help file
sed -i "s#DOC=PREFIX+'/share/doc/'+PKG#DOC=PREFIX+'/share/doc/'+PKG+'-%{version}'#g" usr/bin/byobu-config
# set default fedora windows
cp -p %{SOURCE1} usr/share/byobu/windows/common
# fix path from lib to libexec by modified Makefile.am
#sed -i "s#/lib/#/libexec/#g" usr/lib/byobu/Makefile.am
sed -i "s#libdirdir = \$(prefix)/lib/#libdirdir = \$(prefix)/libexec/#g" usr/lib/byobu/Makefile.in usr/lib/byobu/include/Makefile.in

sed -i "1 d" etc/profile.d/Z97-byobu.sh

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" install
# remove doc from make install
rm -rf %{buildroot}%{_docdir}/%{name}

# remove apport which is not available in fedora
rm %{buildroot}%{_libexecdir}/%{name}/apport
sed -i 's#status\[\"apport\"\]=0##g' %{buildroot}%{_bindir}/byobu-config

for po in po/*.po
do
    lang=${po#po/}
    lang=${lang%.po}
    mkdir -p %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/
    msgfmt ${po} -o %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/%{name}.mo
done
desktop-file-install usr/share/applications/%{name}.desktop --dir %{buildroot}%{_datadir}/applications

%find_lang %{name}

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
%doc usr/share/doc/%{name}/help.*.txt
%dir %{_datadir}/%{name}
%dir %{_libexecdir}/%{name}
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}*.1.gz
%{_libexecdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/profile.d/Z97-byobu.sh

%changelog
* Tue Apr 24 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 5.17-1
- Update to current release 5.17

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Jan Klepek <jan.klepek at, gmail.com> - 4.41-1
- update to 4.41

* Mon Aug 1 2011 Jan Klepek <jan.klepek at, gmail.com> - 4.23-1
- update to 4.23

* Sat Jul 23 2011 Jan Klepek <jan.klepek at, gmail.com> - 4.22-2
- updated to 4.22 + various bugfixes

* Sat Jul 23 2011 Jan Klepek <jan.klepek at, gmail.com> - 4.20-1
- new major release

* Sat Jan 8 2011 Jan Klepek <jan.klepek at, gmail.com> - 3.21-1
- new release

* Sat Dec 18 2010 Jan Klepek <jan.klepek at, gmail.com> - 3.20-2
- upgrade to 3.20 + some patches

* Fri Sep 3 2010 Jan Klepek <jan.klepek at, gmail.com> - 3.4-1
- upgraded to 3.4

* Thu Jun 17 2010 Jan Klepek - 2.80-1
- bugfix for BZ#595087, changed default windows selection, removed apport from toggle status notification
- upgraded to 2.80 version

* Sun May 2 2010 Jan Klepek <jan.klepek at, gmail.com> - 2.73-1
- new version released

* Wed Apr 21 2010 Jan Klepek <jan.klepek at, gmail.com> - 2.67-3
- adjusted SHARE path

* Tue Apr 20 2010 Jan Klepek <jan.klepek at, gmail.com> - 2.67-2
- adjusted path for looking for po files and removed duplicate file entry

* Fri Apr 2 2010 Jan Klepek <jan.klepek at, gmail.com> - 2.67-1
- Initial fedora RPM release
