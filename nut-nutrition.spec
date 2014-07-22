# For the record. Upstream said that this software was written before Network
# UPS tools and they started writing it without checking if a software with the
# name "nut" already existed. Network UPS tools should ideally be renamed, as a
# result. However, since when it comes to Fedora, the UPS tools got here first,
# I'm modifying nut to nut-nutrition instead to save everyone the trouble.
# Upstream has quite correctly said that he isn't going to change the name
# globally.

%global binaryname      nut
Name:           nut-nutrition
Version:        19.2
Release:        1%{?dist}
Summary:        A nutritional Software

## couldn't find a group!!?!
Group:          Applications/Text
License:        GPLv2+
URL:            http://nut.sourceforge.net/ 
Source0:        http://downloads.sourceforge.net/%{binaryname}/%{binaryname}-%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}.appdata.xml

# Fixes to make file and readme
Patch0:         nut-19.2-Makefile.patch

BuildRequires:  fltk-devel desktop-file-utils

%description
NUT allows you to record what you eat and analyze your meals for
nutrient composition. The database included is the USDA Nutrient
Database for Standard Reference, Release 22.


%prep
%setup -q -n %{binaryname}-%{version}
%patch0 
mv nut.1 nut-nutrition.1 -v
rm -rfv fltk/


%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Desktop file
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata/
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -p -m 644 nuticon.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps/nuticon.xpm

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/
install -p -m 644  nuticon.png $RPM_BUILD_ROOT%{_datadir}/icons/

%post
/bin/touch --no-create %{_datadir}/icons/ &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/ &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/ &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/ &>/dev/null || :


%files
%doc LICENSE README CREDITS
%{_bindir}/%{binaryname}*
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}.1.*
%{_datadir}/applications/*.desktop
%dir %{_datadir}/appdata/
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/pixmaps/nuticon.xpm
%{_datadir}/icons/nuticon.png

%changelog
* Mon Jul 21 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 19.2-1
- Add icons
- rhbz #615508

* Sun Jul 20 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 19.2-1
- Updated to latest upstream version

* Fri Feb 25 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 15.7-3
- Changed spec name

* Sat Jul 17 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 15.7-2
- corrected spec to include Food Data files

* Sat Jul 17 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 15.7-1
- initial package build
