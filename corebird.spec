Name:			corebird
Version:		0.4
Release:		0%{?dist}
Summary:		Native GTK Twitter client
License:		GPLv3+
URL:			http://corebird.baedert.org/
Source0:		https://github.com/baedert/corebird/archive/corebird-0.4.tar.gz
BuildRequires:		gtk3-devel >= 3.9
BuildRequires:		glib2-devel >= 2.38
BuildRequires:		rest-devel
BuildRequires:		json-glib-devel
BuildRequires:		libnotify-devel
BuildRequires:		sqlite-devel
BuildRequires:		libsoup-devel
BuildRequires:		vala-devel
BuildRequires:		cmake
BuildRequires:		librsvg2-tools
BuildRequires:		desktop-file-utils
BuildRequires:		libgee-devel
Requires:		fontawesome-fonts

%description
Native GTK Twitter client for the Linux desktop.

%prep
%setup

%build
%{cmake} .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# in separate package
rm -rf %{buildroot}%{_datadir}/fonts

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc COPYING README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/glib-2.0/schemas/org.baedert.%{name}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Mon Nov 04 2013 Ryan Lerch <ryanlerch@fedoraproject.org> - 0.4-0
- initial package
