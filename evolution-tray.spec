Name:           evolution-tray
Version:        0.0.8
Release:        1%{?dist}
Summary:        Tray plugin for evolution

License:        GPLv2+
URL:            http://gnome.eu.org/index.php/Evolution_Tray
Source0:        http://gnome.eu.org/%{name}-%{version}.tar.gz
Patch0:         0001-evolution-tray-fedora-gconf-client-header.patch

BuildRequires:  libnotify-devel GConf2-devel intltool evolution-devel
# Requires:       

%description


%prep
%setup -q
## %patch0

# Add the gconf includedir to the path. Configure doesn't seem to pick her up
sed -ibackup 's|\(^INCLUDES =\)|\1 -I/usr/include/gconf/2/ |' src/Makefile.in


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc



%changelog
* Wed Mar 13 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.0.8-1
- Initial rpmbuild

