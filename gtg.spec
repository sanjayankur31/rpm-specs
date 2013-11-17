%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define gtg_milestone 0.3

Name:           gtg
Version:        0.3.bzr1301
Release:        1%{?dist}
Summary:        Personal organizer for the GNOME desktop

Group:          Applications/Productivity
License:        GPLv3+
URL:            http://gtg.fritalk.com
BuildArch:      noarch
Source0:        http://launchpad.net/%{name}/%{gtg_milestone}/%{version}/+download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch1:         gtg-desktop.patch

BuildRequires:  python-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  pyxdg
Requires:       pygtk2 pygtk2-libglade python-configobj pyxdg pycairo gnome-python2-gnome
Requires:       python-liblarch >= 2.1.0
Requires:       python-liblarch_gtk
Requires:       dbus-python

%description
Getting Things GNOME! (GTG) is a personal organizer for the GNOME desktop
environment inspired by the Getting Things Done (GTD) methodology. GTG is
designed with flexibility, adaptability, and ease of use in mind so it can be
used as more than just GTD software.


%prep
%setup -q -n %{name}
%patch1 -p1 -b .desktop
sed -i -e "s|#!/usr/bin/env python||" GTG/gtg.py


%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/GTG/plugins/geolocalized_tasks
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/GTG/plugins/geolocalized-tasks.gtg-plugin
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

%find_lang %{name} --with-gnome


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG LICENSE README
%{_bindir}/gtg
%{_bindir}/gtcli
%{_bindir}/gtg_new_task
%{_datadir}/dbus-1/services/org.gnome.GTG.service
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/icons/hicolor/*/apps/backend_*
%{_datadir}/icons/hicolor/*/actions/%{name}*
%{_datadir}/icons/hicolor/*/categories/%{name}*
%{_datadir}/icons/hicolor/*/categories/search*
%{_datadir}/icons/hicolor/*/categories/item*
%{_datadir}/icons/hicolor/*/emblems/%{name}*
%{_datadir}/icons/hicolor/svg/%{name}*
%{_datadir}/icons/ubuntu-mono*/*/apps/%{name}*
%{python_sitelib}/*
%{_mandir}/man1/*.1.gz


%changelog
* Thu Jun 06 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.bzr1301-1
- Try out trunk!

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov  9 2012 Yanko Kaneti <yaneti@declera.com> 0.3-2
- Add missing requires on python-liblarch(_gtk)

* Fri Nov  9 2012 Yanko Kaneti <yaneti@declera.com> 0.3-1
- New upstream release - 0.3

* Wed Jul 18 2012 Yanko Kaneti <yaneti@declera.com> 0.2.4-8
- Add patch for crash bug 841179 (lp bug 744294)

* Thu Jun 14 2012 Yanko Kaneti <yaneti@declera.com> 0.2.4-7
- Remove the geolocalized_tasks plugin which uses pyclutter,
  which uses gtk3. Bug #817841

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 10 2010 Yanko Kaneti <yaneti@declera.com> 0.2.4-2
- Avoid "RuntimeError: not holding the import lock" with recent pythons, from upstream
- Alternative X test, avoiding the xorg-x11-utils dependency
- Requires dbus-python

* Sun Apr 11 2010 Yanko Kaneti <yaneti@declera.com> 0.2.4-1
- New bugfix release from upstream

* Mon Mar  4 2010 Yanko Kaneti <yaneti@declera.com> 0.2.3-1
- "A bit of polishing." - from upstream

* Mon Mar  1 2010 Yanko Kaneti <yaneti@declera.com> 0.2.2-1
- New upstream release.
  http://gtg.fritalk.com/post/2010/03/01/Getting-Things-GNOME!-0.2.2-(Protector)-release-is-out!

* Fri Feb 19 2010 Yanko Kaneti <yaneti@declera.com> 0.2.1-3
- Fixup the last fixup. Again preventing crash on startup.

* Sun Feb 14 2010 Yanko Kaneti <yaneti@declera.com> 0.2.1-2
- Pull upstream fix for bug 565224. Prevents crash on startup

* Sun Jan 31 2010 Yanko Kaneti <yaneti@declera.com> 0.2.1-1
- Upstream bugfix release

* Sun Jan 31 2010 Yanko Kaneti <yaneti@declera.com> 0.2-3
- Pull an upstream fix for missing tomboy.ui - bug 560316

* Mon Dec 14 2009 Yanko Kaneti <yaneti@declera.com> 0.2-2
- 0.2 final.
  http://gtg.fritalk.com/post/2009/12/10/The-new-Getting-Things-GNOME!-0.2-Gorignak-has-landed!

* Thu Dec  3 2009 Yanko Kaneti <yaneti@declera.com> 0.1.9-1
- 0.2 beta.
  http://gtg.fritalk.com/post/2009/12/02/Getting-Things-GNOME!-0.1.9-is-out!
- Remove some no longer necessary patching
- BR: pyxdg

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Yanko Kaneti <yaneti@declera.com> 0.1.2-3
- Use %%{__python} instead of python

* Mon Jul 13 2009 Yanko Kaneti <yaneti@declera.com> 0.1.2-2
- Implement review feedback
  https://bugzilla.redhat.com/show_bug.cgi?id=510994#c1

* Mon Jul 13 2009 Yanko Kaneti <yaneti@declera.com> 0.1.2-1
- Initial packaging
