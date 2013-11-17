Name:           prepaid-manager-applet
Version:        0.0.1.1
Release:        1%{?dist}
Summary:        An applet for the GNOME Desktop for GSM mobile prepaid SIM cards

Group:          Applications/Internet
License:        GPLv3
URL:            https://honk.sigxcpu.org/piki/projects/ppm/
Source0:        http://honk.sigxcpu.org/projects/ppm/tarballs/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  gettext gnome-common glib2-devel intltool gnome-doc-utils
BuildRequires:  python2-devel desktop-file-utils
BuildRequires:  dbus-python-devel pygobject2-devel gtk3-devel

Requires:       mobile-broadband-provider-info ModemManager gtk3 
Requires:       dbus-python pygobject2 gtk3

%description
prepaid-manager-applet aims to ease the handling of mobile internet 
connections using GSM mobile prepaid cards on the GNOME Desktop. 
Such a SIM card can either be in a mobile phone used as a modem, 
a USB 3g module (USB surf stick) or used by the built in 3G 
chip set in your laptop/net book.

* It allows you to check the current balance and to top up the credit.
* It uses ModemManager to talk to your GSM chip set.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $%{buildroot}
make install DESTDIR=%{buildroot}
desktop-file-validate %{buildroot}/%{_datadir}/applications/prepaid-manager-applet.desktop
chmod a+x %{buildroot}/%{_datadir}/prepaid-manager-applet/prepaid-manager-applet.py
%find_lang %{name}

%postun
if [ $1 -eq 0 ] ; then
     glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/glib-2.0/schemas/org.gnome.PrepaidManager.gschema.xml

%changelog
* Wed May 25 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.1.1-1
- Updated to first tar release

* Mon Mar 28 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110323-1
- Initial rpm package
