%global tarname mpDris2
# For F<20
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           mpdris2
Version:        0.4
Release:        1%{?dist}
Summary:        Provide MPRIS 2 support to mpd

License:        GPLv3+
URL:            https://github.com/eonpatapon/%{tarname}
Source0:        http://mpdris2.patapon.info/latest/%{tarname}-%{version}.tar.gz

# Add another category entry
# Add line to make it appear in control center (in current git repo)
# Sent upstream: https://github.com/eonpatapon/mpDris2/pull/47
Patch0:         000-%{tarname}-0.4-desktop-file.patch
BuildArch:      noarch

BuildRequires:  gettext intltool desktop-file-utils
# Will pull in python
# Have I missed anything?
Requires:       dbus-python python-mpd pygobject2

%description
mpDris2 provides MPRIS 2 support to mpd (Music Player Daemon).

mpDris2 is run in the user session and monitors a local or distant 
mpd server


%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p0


%build
%configure --docdir=%{_pkgdocdir}

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

#%if 0%{?fedora} < 20
#rm -frv $RPM_BUILD_ROOT/%{_docdir}/

desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/%{tarname}.desktop

%find_lang %{tarname}

%files -f %{tarname}.lang
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{tarname}.desktop
%doc AUTHORS COPYING README
%{_bindir}/%{tarname}
%{_datadir}/applications/%{tarname}.desktop
%{_datadir}/dbus-1/services/org.mpris.MediaPlayer2.mpd.service
%{_pkgdocdir}/%{tarname}.conf

%changelog
* Thu Aug 22 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.4-1
- License updated to GPLv3+

* Wed Aug 21 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.4-1
- Mark files as doc

* Fri Jun 21 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.4-1
- #912048
- Use find_lang
- Rename to lowercase
- Patch desktop file
- Mark autostart file as config

* Sun Feb 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.4-1
- Initial rpmbuild
