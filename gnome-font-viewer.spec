Name:		gnome-font-viewer
Version:	3.3.2.1
Release:	2%{?dist}
Summary:	Utility for previewing fonts for GNOME

License:	GPLv2
#No URL for the package specifically, as of now
URL:		http://www.gnome.org/gnome-3/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-font-viewer/3.3/gnome-font-viewer-3.3.2.1.tar.xz

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	gtk3-devel
BuildRequires:	GConf2-devel
BuildRequires:	desktop-file-utils

#Requires:   

%description
Use gnome-font-viewer, the Font Viewer, to preview fonts and display 
information about a specified font. You can use the Font Viewer to display the 
name, style, type, size, version, and copyright of the font.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

desktop-file-install --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%files -f %{name}.lang
%doc ABOUT-NLS COPYING NEWS

%{_bindir}/%{name}
%{_bindir}/gnome-thumbnail-font
%{_datadir}/applications/%{name}.desktop
%{_datadir}/thumbnailers/%{name}.thumbnailer


%changelog
* Tue Dec 06 2011 Anuj More <anujmorex@gmail.com> - 3.3.2.1-2
- made some formating changes in the spec file

* Fri Nov 18 2011 Anuj More <anujmorex@gmail.com> - 3.3.2.1-1
- rebuilt

