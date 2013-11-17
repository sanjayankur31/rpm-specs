Name:		xword
Version:	1.0
Release:	2%{?dist}
Summary:	Reads and writes crossword puzzles in the Across Lite file format


Group:		Amusements/Games
License:	BSD
URL:		http://x-word.org/
Source0:	http://x-word.org/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.xml
Source3:	%{name}.1

BuildRequires:	desktop-file-utils
Requires:	pygtk2 gnome-python2-gnomeprint 
BuildArch:	noarch 

%description
Xword is a GTK program that works well for doing crossword puzzles in the
Across Lite file format used by The New York Times and others. As well as a
clock, it supports printing. It also auto-saves puzzles as you solve them so
that you can return to partially completed puzzles.


%prep
%setup -q


sed -i -e "s|HOME_PATH = os\.path\.dirname(sys\.argv\[0\])|HOME_PATH = '%{_datadir}/%{name}-%{version}'|g" xword


%build
#nothing to build



%install

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_bindir}/
install -d $RPM_BUILD_ROOT%{_mandir}/man1/

install -p -m 755 xword $RPM_BUILD_ROOT%{_bindir}/

install -p -m 644 layout-rtb.png $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -p -m 644 crossword-solve.png $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -p -m 644 crossword-clock.png $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -p -m 644 crossword-check.png $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -p -m 644 crossword-check-all.png $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}


#man page
install -p -m 644 %SOURCE3 $RPM_BUILD_ROOT%{_mandir}/man1

#icon install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps
cp -p crossword-solve.png					\
	$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps/xword.png



#desktop file
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications %SOURCE1

#mime file
install -d $RPM_BUILD_ROOT%{_datadir}/mime/packages
install -p -m 644 %SOURCE2 $RPM_BUILD_ROOT%{_datadir}/mime/packages/

%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :


%clean


%files
%doc LICENSE
%{_datadir}/%{name}-%{version}
%{_datadir}/icons/hicolor/24x24/apps/xword.png
%{_datadir}/applications/%{name}.desktop
%{_bindir}/*
%{_datadir}/mime/packages/*
%{_mandir}/man1/*



%changelog
* Wed Oct 31 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0-2
- Update as per review #871629

* Mon Oct 29 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0-1
- Initial rpm spec based on Alex's spec at rhbz# 470155
- Compressed Alex's changelog below
- Addressed the comments in the review by Mamoru Tasaka 
  <mtasaka ioa.s.u-tokyo.ac.jp>. Warning on python 2.6 will
  be addressed later. 
- Added LICENSE to %%doc
- Fix a silly error involving $RPM_BUILD_ROOT.
- Initial import.
