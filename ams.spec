# ams does not give debug info by default
#%%define debug_package %%{nil}

Summary:  Alsa Modular Synth, a realtime modular synthesizer
Name:     ams
Version:  2.0.1
Release:  5%{?dist}
URL:      http://alsamodular.sourceforge.net
Source0:  http://downloads.sourceforge.net/project/alsamodular/alsamodular/2.0.1/%{name}-%{version}.tar.bz2
Source1:  ams.desktop
Patch0:   ams-2.0.1-link.patch
License:  GPLv2+
Group:    Applications/Multimedia

Requires: ladspa-cmt-plugins 
Requires: ladspa-swh-plugins 
Requires: ladspa-vco-plugins 
Requires: ladspa-rev-plugins 
Requires: ladspa-mcp-plugins

BuildRequires: desktop-file-utils alsa-lib-devel clalsadrv-devel
BuildRequires: jack-audio-connection-kit-devel ladspa-devel
BuildRequires: fftw2-devel
BuildRequires: qt-devel
# rebuild configure and makefiles for patch0
BuildRequires: libtool automake autoconf

%description
AlsaModularSynth is a realtime modular synthesizer and effect
processor. It features MIDI controlled modular software synthesis,
realtime effect processing with capture, full control of all synthesis
and effect parameters via MIDI, integrated LADSPA Browser with search
capability and JACK Support.

NOTE: Example files are in /usr/share/ams

%prep
%setup -q
%patch0 -p1
for i in `ls demos/*.ams` ; do 
  iconv -f iso8859-1 -t utf-8 $i > $i.conv && mv -f $i.conv $i;
done;
for i in AUTHORS THANKS; do 
  iconv -f iso8859-1 -t utf-8 $i > $i.conv && mv -f $i.conv $i;
done;

%build
aclocal && automake && autoconf
%configure --with-ladspa-path=%{_libdir}/ladspa
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
chmod 755 %{buildroot}%{_bindir}/%{name}

# desktop categories
BASE="Application AudioVideo Audio"
XTRA="X-MIDI X-Jack X-Synthesis Midi"

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications    \
  `for c in ${BASE} ${XTRA} ; do echo "--add-category $c " ; done` \
  %{SOURCE1}

%files
%doc AUTHORS NEWS README COPYING THANKS ChangeLog demos instruments tutorial
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}*
%{_datadir}/pixmaps/%{name}*

%changelog
* Mon Oct 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 2.0.1-5
- Imported from CCRMA

* Tue Jun  8 2010 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 2.0.1-4
- picked up changes from ams srpm created by Simon Lewis with fixes
  by Niels Mayer, bumped release to 4

* Wed May 19 2010 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 2.0.1-1
- updated to 2.0.1, add patch to link against libdl on fc13

* Tue Nov 24 2009 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 2.0.0-1
- updated to 2.0.0, build process now uses configure and make

* Tue Jul 15 2008 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.8-0.2.rc2
- updated qt3-devel build dependency for fc9

* Tue Oct  9 2007 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.8-0.2.rc2
- adjusted desktop categories

* Tue May  8 2007 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.8-0.1.rc2
- updated to rc2, use qmake to define the Makefile

* Mon Apr 30 2007 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.8-0.1.rc1
- updated to 1.8.8-rc1 release

* Tue Dec  5 2006 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.7-6
- added proper require incantations for the specific ladspa plugins 
  needed

* Thu Nov 30 2006 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.7-5
- explicitly require all LADSPA plugins used by the examples and demos,
  and add filter.so (fil plugins). 

* Tue Nov 28 2006 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.7-5
- set LADSPA_PATH to lib64 for x86_64

* Fri Nov 24 2006 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.7-5
- spec file tweaks, changed requirements for fc6 build (ladspa plugin
  packages now have the "ladspa-" prefix), removed old requires
- use separate desktop file

* Mon Jul  3 2006 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.7-4
- added missing swh-plugins requirement (thanks to Michael Tiemann
  for finding this problem)

* Sat May 13 2006 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.7-3
- added explicit requires for the LADSPA plugins all demos need
- added Planet CCRMA categories

* Fri Mar 31 2006 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 
- proper fc5 build dependencies

* Fri Dec 24 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.7-2
- use rpm optimization flags

* Mon Dec 20 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 
- spec file cleanup

* Fri Aug 24 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.7-1
- updated to 1.8.7
- added clalsadrv-devel build requirement

* Fri Jul 23 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.6-1
- updated to 1.8.6

* Tue Jul  6 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.5-1
- updated to 1.8.5

* Thu May 13 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.2-1
- updated to 1.8.2

* Thu Apr 29 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.8.0-1
- updated to 1.8.0

* Tue Mar  2 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.7.6-1
- updated to 1.7.6

* Sun Feb 29 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.7.5-1
- updated to 1.7.5

* Wed Jan 21 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.7.2-1
- updated to 1.7.2

* Wed Dec 17 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.7.1-1
- updated to 1.7.1

* Wed Nov 11 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.6.0-1
- spec file tweaks
- add patch0 to enable old alsa api

* Tue Nov  4 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.6.0-1
- updated to 1.6.0

* Thu Aug 28 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.12-1
- updated to 1.5.12
- adjusted name of makefile, minor doc file list changes

* Mon Aug 18 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.11-1
- updated to 1.5.11, added version tags

* Sat Jul 26 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.10-1
- updated to 1.5.10

* Wed May 21 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.9-1
- updated to 1.5.9

* Tue May 20 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.8b-3
- rebuild for newer version qt (3.1.1), added explicit dependency

* Tue Apr  8 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.8b-2
- rebuilt for newer version of fftw

* Sat Apr  5 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.8b-1
- added support for qt 3.1

* Wed Apr  2 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.8b-1
- updated to 1.5.8b
- rebuild for jack 0.66.3, added explicit requires for it

* Tue Dec 31 2002 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.5-1
- updated to 1.5.5, added menu entry, updated description

* Mon Dec  9 2002 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.4-2
- added patch to synth.cpp (lockups)

* Wed Dec 04 2002 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.4
- updated to 1.5.4

* Tue Nov 12 2002 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.3c-1
- updated to 1.5.3c

* Mon Nov 11 2002 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 1.5.3b-1
- updated to 1.5.3b

* Fri Oct 11 2002 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>
- Initial build.
