%define alphatag rc5
Name:           parcellite
Version:        1.0.2
Release:        0.1.%{alphatag}%{?dist}
Summary:        A lightweight GTK+ clipboard manager

Group:          User Interface/Desktops
License:        GPLv3+
URL:            http://parcellite.sourceforge.net/
Source0:        http://downloads.sourceforge.net/parcellite/parcellite-%{version}%{alphatag}.tar.gz
Patch0:         parcellite-0.9.2-de.po.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.10.0 
BuildRequires:  desktop-file-utils, intltool >= 0.23

%description
Parcellite is a stripped down, basic-features-only clipboard manager with a 
small memory footprint for those who like simplicity.

In GNOME and Xfce the clipboard manager will be started automatically. For 
other desktops or window managers you should also install a panel with a 
system tray or notification area if you want to use this package.


%prep
%setup -q -n parcellite-%{version}%{alphatag}
%patch0 -p1 -b .orig


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
%find_lang %{name}

desktop-file-install --vendor="fedora"                     \
  --delete-original                                        \
  --remove-category=Application                            \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

desktop-file-install                                       \
  --delete-original                                        \
  --add-category=TrayIcon                                  \
  --dir=${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart/     \
  ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart/%{name}-startup.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README NEWS
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{name}-startup.desktop
%{_bindir}/%{name}
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_mandir}/man1/%{name}.1.*


%changelog
* Sun Feb 19 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.0.2-0.1.rc5
- Version bump (new upstream author, different versioning scheme)
- Extending the patch to fix DSO linking (#565054)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.9.2-4
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.2-2
- Add patch to fix DSO linking (#565054)

* Fri Jan 01 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 18 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1
- Remove both patches as all fixes got upstreamed

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.9-1
- Update to 0.9
- Fix Control+Click behaviour
- Small corrections to German translation

* Sat Apr 19 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.8-1
- Update to 0.8

* Sat Apr 19 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.7-2
- No longer require lxpanel
- Preserve timestamps during install
- Include NEWS in doc

* Sat Apr 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.7-1
- Initial Fedora RPM
