%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif


%global debug_package %{nil}
%global title RabbitVCS

Name:           rabbitvcs
Version:        0.15.3
Release:        1%{?dist}
Summary:        Graphical user interface to version control systems
Group:          Development/Tools

License:        GPLv2+
URL:            http://www.rabbitvcs.org/
Source0:        http://rabbitvcs.googlecode.com/files/%{name}-%{version}.tar.bz2

BuildRequires:  pygtk2-devel >= 2.12
BuildRequires:  python2-devel

%description
RabbitVCS is a set of graphical tools written to provide simple
and straightforward access to the version control systems you use.

%package core
Summary:        Core package of RabbitVCS
Group:          Development/Tools

Requires:       dbus-python
Requires:       meld
Requires:       pygtk2-libglade
Requires:       pygtk2
Requires:       pysvn
Requires:       python-dulwich
Requires:       python-configobj
Requires:       subversion
Requires:       hicolor-icon-theme

Obsoletes:      rabbitvcs <= 0.13.1
Obsoletes:      rabbitvcs-git
Obsoletes:      rabbitvcs-svn

BuildArch:      noarch

%description core
Contains packages shared between the RabbitVCS extensions.

%package nautilus
Summary:        Nautilus extension for RabbitVCS
Group:          Development/Tools
Requires:       rabbitvcs-core = %{version}-%{release}
Requires:       nautilus
Requires:       nautilus-python >= 0.7.0
Requires:       dbus-python

#RabbitVCS is the new name for NautilusSVN. 
Provides:       nautilussvn = %{version}-%{release}
Obsoletes:      nautilussvn < 0.13

%description nautilus
RabbitVCS is a set of graphical tools written to provide simple and 
straightforward access to the version control systems you use. This is the 
extension for the Nautilus file manager.

%package thunar
Summary:        Thunar extension for RabbitVCS
Group:          Development/Tools
Requires:       rabbitvcs-core = %{version}-%{release}
Requires:       thunar >= 0.4.0
Requires:       thunarx-python >= 0.2.0
Requires:       dbus-python >= 0.80

%description thunar
An extension for Thunar to allow better integration with the 
Subversion source control system.

%package gedit
Summary:        Gedit extension for RabbitVCS
Group:          Development/Tools
Requires:       rabbitvcs-core = %{version}-%{release}
Requires:       gedit

%description gedit
RabbitVCS is a set of graphical tools written to provide simple and 
straightforward access to the version control systems you use. This is the 
extension for gedit text editor

%package cli
Summary:        CLI extension for RabbitVCS
Group:          Development/Tools
Requires:       rabbitvcs-core = %{version}-%{release}
BuildArch:      noarch

%description cli
RabbitVCS is a set of graphical tools written to provide simple and 
straightforward access to the version control systems you use. This is the 
extension for command line interface.

%prep
%setup -q

%build
%{__python2} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

# Installing Nautilus extension
mkdir -p $RPM_BUILD_ROOT%{_datadir}/nautilus-python/extensions/
cp clients/nautilus-3.0/%{title}.py $RPM_BUILD_ROOT%{_datadir}/nautilus-python/extensions/%{title}.py

# Installing Thunar Extension
mkdir -p $RPM_BUILD_ROOT%{_libdir}/thunarx-2/python/
cp clients/thunar/%{title}.py $RPM_BUILD_ROOT%{_libdir}/thunarx-2/python/%{title}.py

# Installing Gedit Extension
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gedit/plugins/
cp clients/gedit/%{name}-plugin.py $RPM_BUILD_ROOT%{_libdir}/gedit/plugins/%{name}-plugin.py
cp clients/gedit/%{name}-gedit3.plugin $RPM_BUILD_ROOT%{_libdir}/gedit/plugins/%{name}-gedit3.plugin

# Installing CLI Extension
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp clients/cli/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}

%find_lang %{title}

%post core
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun core
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans core
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{title}.lang core
%doc AUTHORS COPYING MAINTAINERS
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/16x16/actions/rabbitvcs-push.png
%{_datadir}/icons/hicolor/scalable/*/*.svg
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info

%files nautilus
%{_datadir}/nautilus-python/extensions/%{title}.py*

%files thunar
%{_libdir}/thunarx-2/python/%{title}.py*

%files gedit
%{_libdir}/gedit/plugins/%{name}-plugin.py*
%{_libdir}/gedit/plugins/%{name}-gedit3.plugin

%files cli
%{_bindir}/%{name}

%changelog
* Thu Dec 05 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.15.3-1
- Update to latest release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.15.0.5-1
- Updated to 0.15.0.5, BZ 760682.
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- tar.gz → tar.bz2
- Adjusted the paths for Gnome 3
- Re-added Group, Jon Ciesla limburgher@gmail.com

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 21 2011 Juan Rodriguez <nushio@fedoraproject.org> - 0.14.2.1-3
- Adds a dependency to python-dulwich so the git plugin can work
- Removes rabbitvcs-git and rabbitvcs-svn

* Tue Sep 13 2011 Juan Rodriguez <nushio@fedoraproject.org> - 0.14.2.1-2
- Removes Nautilus dependency on rabbitvcs-core

* Tue Sep 13 2011 Juan Rodriguez <nushio@fedoraproject.org> - 0.14.2.1-1
- Updated package to 0.14.2.1
- Added Thunar Plugin

* Mon Feb 14 2011 Juan Rodriguez <nushio@fedoraproject.org> - 0.14.1.1-1
- Updated Package to 0.14.1.1
- Lots of speed improvements. 
- Git and SVN support separated and are now optional
- Changelog for 0.14.1.1: http://blog.rabbitvcs.org/archives/284
- Changelog for 0.14.1: http://blog.rabbitvcs.org/archives/280
- Changelog for 0.14: http://blog.rabbitvcs.org/archives/277

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.13.3-2
- Rebuild for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jun 16 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13.3-1
- Fixes a *lot* of bugs
- No longer forces English as the language
- Gedit plugin should work now

* Sun Jun 6 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13.2.1-2
- Fixes the package creation

* Sun Jun 6 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13.2.1-1
- Fixes a crash left by a debug flag.

* Mon May 31 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13.2-1
- Updated to version 0.13.2.

* Thu May 27 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13.1-3
- Now obsoletes rabbitvcs
- Fixes svg permission ownage

* Wed May 26 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13.1-2
- rabbitvcs-core is now noarch
- rabbitvcs-cli is now noarch

* Wed Apr 28 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13.1-1
- Rebased to 13.1

* Fri Mar 19 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13-2
- The split packages are now bundled into a single tarball. 
- Changed some requires versions. 
- Thunar and NautilusOld packages are no longer being provided. 
- Updated Python macros to the newly approved ones
- Changed URL, Summary and Descriptions for all packages / subpackages
- Package is no longer noarch

* Thu Feb 11 2010 Juan Rodriguez <nushio@fedoraproject.org> - 0.13-1
- Updated RabbitVCS to 0.13
- Split packages for nautilus, nautilus-old, thunar, gedit and cli
- Requires nautilus-python >= 0.5.2 so 64bit users can use rabbitvcs. 

* Tue Dec 17 2009 Juan Rodriguez <nushio@fedoraproject.org> - 0.12.1-2
- Cleaned up Icon Script
- Added AUTHORS, COPYING and MAINTAINERS

* Tue Dec 1 2009 Juan Rodriguez <nushio@fedoraproject.org> - 0.12.1-1
- Updated to RabbitVCS 0.12.1
- Added SSL Client Cert prompt 
- Updated "previous log message" UI behaviour
- Updated locale detection
- Improvements for packaging scripts

* Sat Oct 3 2009 Juan Rodriguez <nushio@fedoraproject.org> - 0.12-1
- Renamed from NautilusSVN to RabbitVCS to match upstream. 
- Calls gtk-update-icon-cache to regenerate the icon cache
