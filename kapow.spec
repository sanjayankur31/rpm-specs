Name:           kapow
Version:        1.4.4.1
Release:        1%{?dist}
Summary:        A punch clock program

License:        GPLv3+
URL:            http://gottcode.org/%{name}

Source0:        http://gottcode.org/%{name}/%{name}-%{version}-src.tar.bz2

# Pull request: https://github.com/gottcode/kapow/pull/33
Source1:        %{name}.appdata.xml

BuildRequires:  qt5-qtbase-devel desktop-file-utils

%description
Kapow is a punch clock program designed to easily keep track of your hours,
whether you're working on one project or many. Simply clock in and out with the
Start/Stop button. If you make a mistake in your hours, you can go back and
edit any of the entries by double-clicking on the session in question. Kapow
also allows you to easily keep track of the hours since you last billed a
client, by providing a helpful "Billed" check box--the totals will reflect your
work after the last billed session. 

%prep
%setup -q

# Request qmake to not strip the binary
sed -i.backup '/QT += network/ a\
QMAKE_STRIP = echo' %{name}.pro

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"

qmake-qt5 %{name}.pro PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot} 

mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata/
cp -v %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/appdata/

%find_lang %{name} --with-qt

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc COPYING CREDITS ChangeLog README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%dir %{_datadir}/appdata/
%{_datadir}/appdata/%{name}.appdata.xml

%{_datadir}/icons/hicolor/*/apps/%{name}.*

%{_datadir}/pixmaps/%{name}.xpm

# Find lang doesn't find these two files, so I place them manually
%{_datadir}/%{name}/translations/qt_it.qm
%{_datadir}/%{name}/translations/qt_nl.qm
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/translations

%changelog
* Tue Oct 22 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.4.4.1-1
- Correct directory ownership
- Correct ld flags
- https://bugzilla.redhat.com/show_bug.cgi?id=979767#c8

* Mon Oct 21 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.4.4.1-1
- Update as per https://bugzilla.redhat.com/show_bug.cgi?id=979767#c6
- Remove comments 
- Own datadir/name directory
- Own icon directories
- Add an appdata file

* Sun Jun 30 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.4.4.1-1
- Initial build
- Cosmetic changes #979767
