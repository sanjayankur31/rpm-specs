Name:       lifeograph
Version:    0.11.1
Release:    2%{?dist}
Summary:    A diary program

License:    GPLv3+
URL:        http://%{name}.wikidot.com/start
Source0:    https://launchpad.net/%{name}/trunk/%{version}/+download/%{name}-%{version}.tar.gz
# Correct desktop file to add semi colons to a few fields
Patch0:     %{name}-%{version}-desktop-file.patch
# Convert flag commands to append rather than replace
Patch1:     %{name}-%{version}-wscript.patch

BuildRequires:  waf gtkmm30-devel enchant-devel libgcrypt-devel intltool
BuildRequires:  desktop-file-utils

%description
Lifeograph is a diary program to take personal notes on life. It has all
essential functionality expected in a diary program and strives to have
a clean and streamlined user interface.


%prep
%setup -q
%patch0
%patch1


%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LINKFLAGS="-Wl,-z,relro"

./waf configure -vv --prefix=%{_prefix} --datadir=%{_datadir} 
./waf build -vv %{?_smp_mflags}


%install
./waf install --destdir=%{buildroot}

%find_lang %{name}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Sat Jun 15 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.11.1-2
- Replace sed with patch
- Update desktop database
- Bug# 973868

* Thu Jun 13 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.11.1-1
- Initial rpmbuild
