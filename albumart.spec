Name:           albumart
Version:        1.6.6
Release:        1%{?dist}
Summary:        Album Cover Art Downloader

License:        GPLv2+
URL:            http://www.unrealvoodoo.org/hiteck/projects/%{name}/
Source0:        http://www.unrealvoodoo.org/hiteck/projects/%{name}/dist/%{name}-%{version}.tar.gz

# Some desktop file fixes
# Fixes for the binary file. Some paths are hardcoded :(
Patch0:         albumart-desktop-file-binary.patch

BuildArch:      noarch
BuildRequires:  python2-devel PyQt desktop-file-utils
Requires:       PyQt

%description
A program that will semi-automatically download album cover images for your
music collection. All you have to do is point it at the root of your music
directory and for each directory, the program will download a set of
corresponding (well, best guess) album covers from the Internet, from which you
can choose one that suits your fancy.

See how the program works from a flash demonstration video.

Note that due to the latest changes in Amazon's Product Advertising API, Album
Cover Art Downloader is unable to download any images from Amazon for the time
being. 

%package konqueror
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   kde-baseapps
Summary:    Service menu additon for %{name}

%description konqueror
Konqueror service menu for %{name}


%prep
%setup -q
%patch0 -p2


%build
%{__python2} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT 

# The build system always installs to lib for some reason.
# Tried the various options, but they don't work as required
mkdir -p -m 0755 $RPM_BUILD_ROOT/%{python2_sitelib}/%{name}
mv $RPM_BUILD_ROOT/usr/lib/%{name}/* $RPM_BUILD_ROOT/%{python2_sitelib}/%{name}/

desktop-file-validate --warn-kde $RPM_BUILD_ROOT/%{_datadir}/applnk/Multimedia/%{name}.desktop

# Unable to fix this. Will ask a kde person :)
# desktop-file-validate --warn-kde $RPM_BUILD_ROOT/%{_datadir}/apps/konqueror/servicemenus/albumart_set_cover_image.desktop

chmod -x $RPM_BUILD_ROOT/%{python2_sitelib}/albumart/yahoo/search/webservices.py
chmod -x $RPM_BUILD_ROOT/%{python2_sitelib}/albumart/yahoo/search/domparsers.py
chmod -x $RPM_BUILD_ROOT/%{python2_sitelib}/albumart/process.py

sed -i 's/\r//' $RPM_BUILD_ROOT/%{python2_sitelib}/albumart/process.py
sed -i 's/\r//' $RPM_BUILD_ROOT/%{python2_sitelib}/albumart/event.py
sed -i 's/\r//' $RPM_BUILD_ROOT/%{python2_sitelib}/albumart/albumart.py


pushd $RPM_BUILD_ROOT/%{python2_sitelib}/albumart/
    sed '1{\@^#!/usr/bin/python@d}'  albumart.py > albumart.py.new &&
    touch -r albumart.py albumart.py.new &&
    mv albumart.py.new albumart.py
popd

mkdir -p  $RPM_BUILD_ROOT/%{_mandir}/man1/
cp debian/albumart-qt.1 $RPM_BUILD_ROOT/%{_mandir}/man1/
 
%files
%{_bindir}/%{name}-qt
%{_docdir}/%{name}/
%{_datadir}/applnk/Multimedia/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}*

%{python2_sitelib}/%{name}-%{version}-py?.?.egg-info
%{python2_sitelib}/%{name}/

%files konqueror
%{_datadir}/apps/konqueror/servicemenus/albumart_set_cover_image.desktop


%changelog
* Fri Nov 22 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.6.6-1
- python -> python2
- Add man page
- Add konqueror subpackage
- Update license to GPLv2+

* Wed Feb 27 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.6.6-1
- initial rpm build

