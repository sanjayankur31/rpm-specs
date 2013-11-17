Name:           FretsOnFire
Version:        1.3.110
Release:        2%{?dist}
Summary:        A game of musical skill and fast fingers

Group:          Amusements/Games
# need to confirm what to put in here
License:        GPLv2 and Bitstream Vera with exceptions
URL:            http://fretsonfire.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        FretsOnFire.desktop
Source2:        FretsOnFire.sh
## Source3:        Songs.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python2-devel python-setuptools gettext
BuildRequires:  desktop-file-utils
Requires:       pygame PyOpenGL python-imaging numpy

%description
Frets on Fire is a game of musical skill and fast fingers. The
aim of the game is to play guitar with the keyboard as accurately
as possible.


%prep
## tar -xvf %{SOURCE3}
%setup -q -n "Frets on Fire-%{version}"

sed -i 's/\r//' readme.txt
sed -i 's/\r//' copying.txt
chmod a-x copying.txt
iconv -f iso8859-1 -t utf-8 copying.txt > copying.txt.conv && mv -f copying.txt.conv copying.txt

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
make translations


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT 
##--install-data %{python_sitelib}/%{name}


mkdir -p $RPM_BUILD_ROOT/%{python_sitelib}/%{name}/src/
mkdir -p $RPM_BUILD_ROOT/%{python_sitelib}/%{name}/data/

# spurious installation directories!
rm -rfv $RPM_BUILD_ROOT%{_prefix}/data
rm -rfv $RPM_BUILD_ROOT%{_prefix}/copying.txt
rm -rfv $RPM_BUILD_ROOT%{_prefix}/readme.txt

# Since the build script is so nicely broken, we do all of this manually
# if you use --install-data, it installs only pngs and gives a runtime error 
# for an svg!

mv -v src/* -t  $RPM_BUILD_ROOT/%{python_sitelib}/%{name}/src/
mv -v data/* -t  $RPM_BUILD_ROOT/%{python_sitelib}/%{name}/data/
## mv -v ../Songs/* $RPM_BUILD_ROOT%{python_sitelib}/%{name}/data/songs/


desktop-file-install %{SOURCE1} --dir=$RPM_BUILD_ROOT%{_datadir}/applications/

install -m 755 -D %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/FretsOnFire
install -D $RPM_BUILD_ROOT%{python_sitelib}/%{name}/data/icon.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/FretsOnFire.png

chmod a-x $RPM_BUILD_ROOT%{python_sitelib}/%{name}/data/songs/killscores.sh

# remove second copy
rm -vf $RPM_BUILD_ROOT%{python_sitelib}/%{name}/readme.txt
rm -vf $RPM_BUILD_ROOT%{python_sitelib}/%{name}/copying.txt
rm -rvf $RPM_BUILD_ROOT%{python_sitelib}/%{name}/data/win32
rm -vf $RPM_BUILD_ROOT%{python_sitelib}/%{name}/data/Makefile

%clean
rm -rf $RPM_BUILD_ROOT

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
%defattr(-,root,root,-)
%doc readme.txt copying.txt todo.txt
%dir %{python_sitelib}/%{name}
%{python_sitelib}/%{name}/src/
%{python_sitelib}/Frets_on_Fire-%{version}-py?.?.egg-info
%dir %{python_sitelib}/%{name}/data/
%{python_sitelib}/%{name}/data/*.*
%{python_sitelib}/%{name}/data/mods
%{python_sitelib}/%{name}/data/songs
%{python_sitelib}/%{name}/data/translations
%{_datadir}/applications/FretsOnFire.desktop
%{_datadir}/icons/hicolor/64x64/apps/FretsOnFire.png
%{_bindir}/%{name}

%changelog
* Fri Jan 07 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.110-2
- updated spec 
- http://bugzilla.rpmfusion.org/show_bug.cgi?id=1594

* Fri Dec 31 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.110-1
- initial rpmbuild
