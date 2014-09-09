%global svn_rev 330
%global checkoutdate    20140909
Name:           gtrainer
Version:        0
Release:        0.%{checkoutdate}svn%{svn_rev}%{?dist}
Summary:        Your personal coach

License:        GPLv2+
URL:            http://kutxa.homeunix.org/gtrainer/index-en.html

# From svn export
# svn export  svn://kutxa.homeunix.org/gtrainer/trunk gtrainer-svn330
# tar -cvzf gtrainer-svn330.tar.gz gtrainer-svn330/
Source0:        %{name}-svn%{svn_rev}.tar.gz

BuildRequires:  gtkmm24-devel libglademm24-devel gconfmm26-devel libxml++-devel
BuildRequires:  libdb4-cxx-devel sqlite-devel gettext
BuildRequires:  automake autoconf libtool gettext-devel intltool
#Requires:       

%description
Gtrainer is a program designed for keeping the training of cross-cycling,
cycling or mountain biking for advanced or beginner levels Its been created for
GNU/Linux. An sports diary.

You can create your own training program and save them, keep a rigorous control
of your daily training (weigh control, kilometers, heart rate, etc)

You can also access daily tips about the training, print the weekly, monthly or
yearly training progress, and so on This program has been designed in Gtkmm24,
C++ and it uses the SQLite, PostgreSQL and MySQL to register the data

%prep
%setup -q -n %{name}-svn%{svn_rev}

iconv -f iso8859-1 -t utf-8 AUTHORS > AUTHORS.conv && mv -f AUTHORS.conv AUTHORS
iconv -f iso8859-1 -t utf-8 README > README.conv && mv -f README.conv README
iconv -f iso8859-1 -t utf-8 COPYING > COPYING.conv && mv -f COPYING.conv COPYING

%build
sed -i 's/dnlelse/dnl else/' configure.in
sed -i 's/dnlfi/dnl fi/' configure.in

sed -i 's/-module//' src/plugins/sampleplugin/Makefile*
sed -i 's/-module//' src/plugins/export2csv/Makefile*

./autogen.sh
%configure
make %{?_smp_mflags}


%install
%make_install

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}/
cp trainer.glade $RPM_BUILD_ROOT/%{_datadir}/%{name}/

rm -fv $RPM_BUILD_ROOT/%{_bindir}/export2csv.la
rm -fv $RPM_BUILD_ROOT/%{_bindir}/sampleplugin.la

%find_lang %{name}


%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%{_datadir}/%{name}/



%changelog
* Tue Sep 09 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.20140909svn330
- Initial rpmbuild
