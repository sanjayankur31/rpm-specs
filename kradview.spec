Name:           kradview
Version:        1.1.0
Release:        5%{?dist}
Summary:        An image viewer oriented to images obtained by X-Ray machines

License:        GPLv3+
URL:            http://www.orcero.org/irbis/%{name}/
Source0:        http://www.orcero.org/irbis/%{name}/%{name}-%{version}.tgz

BuildRequires:  doxygen libX11-devel libXt-devel libXext-devel zlib-devel
BuildRequires:  qt-devel libpng-devel libjpeg-turbo-devel
BuildRequires:  kdelibs3-devel arts-devel
BuildRequires:  desktop-file-utils

%description
%{name} is an image viewer oriented to images obtained by X-Ray machines.

It was developed by David Santo Orcero during his work on his Ph.D.

%prep
%setup -q

# Get rid of build error
sed -i -e 's/QImage::QImage/QImage/g' src/panel2d.cpp

# Tweak the desktop file
sed -i 's/\(Terminal=\)0/\1false/' src/%{name}.desktop
sed -i 's/%%m//' src/%{name}.desktop
sed -i '/Encoding/d' src/%{name}.desktop
sed -i '/Terminal/ a\
Categories=Graphics;' src/%{name}.desktop
sed -i '/Comment\[/d' src/%{name}.desktop
sed -i 's/\(Comment=\)/\1An image viewer oriented to images obtained by X-Ray machines/' src/%{name}.desktop
sed -i '/Name\[/d' src/%{name}.desktop
sed -i '/DocPath/d' src/%{name}.desktop

# Correct permissions
chmod a-x COPYING ChangeLog AUTHORS NEWS TODO README

# Convert to utf-8
for file in README TODO; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

# Correct permissions
chmod a-x src/*

%build
%configure --disable-rpath --disable-static --with-arts
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install                                    \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
$RPM_BUILD_ROOT%{_datadir}/applnk/Utilities/%{name}.desktop

rm  -fv $RPM_BUILD_ROOT/%{_datadir}/applnk/Utilities/%{name}.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc COPYING AUTHORS ChangeLog NEWS TODO README
%{_bindir}/%{name}
%{_bindir}/%{name}_client
%{_datadir}/apps/%{name}/
%{_docdir}/HTML/en/%{name}/
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Sun Jul 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.0-5
- Improve desktop file
- Removed extra documentation

* Tue Jul 12 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.0-4
- correct encoding
- remove executable perms
- correct documentation dir

* Mon Jul 11 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.0-3
- remove desktop file in applnk
- remove defattr line
- corrected description
- corrected desktop entry
- add more documentation

* Thu Jun 30 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.0-2
- correct URL
- correct desktop file

* Fri Jun 03 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.0-1
- Initial rpm build
