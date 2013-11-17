# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           indimpc
Version:        0
Release:        0.1.20120415.git%{?dist}
Summary:        A minimalist MPD client with support for the gnome-shell and multimedia keys

# TODO
License:        BSD
URL:            https://github.com/fmoralesc/%{name}
# Git hub has a redirect
# To download, in a browser goto: https://github.com/fmoralesc/indimpc/tarball/gnome-shell
# chmod 0644 <downloaded file>
Source0:        fmoralesc-%{name}-969e9e2.tar.gz
Source1:        indimpc.sh
Source2:        README.fedora

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
Requires:       notify-python
Requires:       dbus-python
Requires:       python-mpd
Requires:       python-keybinder
Requires:       ncmpcpp

%description
This is a minimalist MPD client with support for the gnome-shell indication
system and multimedia keys. It is easily configurable and can launch a more
featured client when needed.

It depends on:

    python-dbus (dbus-python in some systems)
    python-notify
    python-mpd
    python-keybinder (not needed if using Gnome)

For its normal operation, indimpc requires a notifications daemon, hopefully
with support for action-icons, body-markup and persistence (gnome-shell is
recommended). If there is no instance of gnome-settings-daemon running, it will
fallback to python-keybinder to grab the multimedia keys.

Please look at the README.fedora file provided with this package.

%prep
%setup -q -n fmoralesc-%{name}-969e9e2

mv %{SOURCE2} ./

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{python_sitelib}/%{name}/
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m 0755 -t $RPM_BUILD_ROOT/%{python_sitelib}/%{name}/ %{name}.py
install -m 0755 -T %{SOURCE1} $RPM_BUILD_ROOT/%{_bindir}/%{name}


desktop-file-install                                    \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
%{name}.desktop

%files
%doc README.md %{name}.rc ChangeLog LICENSE README.fedora
# For noarch packages: sitelib
%{python_sitelib}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop


%changelog
* Sun Apr 15 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0-0.1.20120415.git
- Update to latest git head. 
- Bugfix

* Fri Apr 13 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0-2.20111209.git
- correct requires

* Sun Mar 11 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-1.20111209.git
- Add requires on ncmpc++
- Added a README.fedora file
- Added comment on how to obtain the source tar

* Fri Dec 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.20111209.git
- Update to current git. Author added ChangeLog and License information

* Wed Dec 07 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.20111207.git
- Initial rpm build
