Name:           fuelmanager
Version:        0.3.6
Release:        5%{?dist}
Summary:        Manage fuel mileage

Group:          Applications/Productivity
License:        GPLv3+

URL:            http://sourceforge.net/projects/fuelmanager/
Source0:        http://sourceforge.net/projects/fuelmanager/files/fuelmanager-0.3.6.tar.bz2

BuildRequires:  qt-devel
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils

%description
Application that keeps track of four things, miles, gallons, cost, and the \
date of each fill-up.\
It generates monthly and yearly summaries of miles driven, cost of fuel,\
how many gallons, and fuel mileage.\

%prep
%setup -q

%build

qmake-qt4 fuelmanager.pro PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=%{buildroot} 

desktop-file-install --dir=%{buildroot}%{_datadir}/applications  %{name}.desktop

for s in 16 22 24 32 48 256; do
    %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} %{name}.png %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
done

%post
update-desktop-database &> /dev/null || :

/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/fuelmanager
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/applications/*.*

%changelog
* Thu Jun 23 2011 Charles Amey kc8hfi@gmail.com - 0.3.6-5
- Built for Release 0.3.6-5

* Sat Jun 11 2011 Charles Amey kc8hfi@gmail.com - 0.3.4-3
- Built for Release 0.3.4

* Thu Jun 09 2011 Charles Amey kc8hfi@gmail.com - 0.3.3-1
- Built for Release 0.3.3
