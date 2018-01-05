%global commit0 c3bcb1d9ba6ab244c2004e2b73fad3de40b77b2d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global srcname qutebrowser

Name:       %{srcname}
Version:    1.0.4
Release:    20180105git%{shortcommit0}%{?dist}
Summary:    A keyboard-driven, vim-like browser based on PyQt5 and QtWebEngine

License:    GPLv3
URL:        http://www.qutebrowser.org
Source0:    https://github.com/qutebrowser/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildArch:  noarch
BuildRequires:  python3-devel
BuildRequires:  asciidoc
BuildRequires:  desktop-file-utils
Requires:   qt5-qtbase
Requires:   qt5-qtdeclarative
Requires:   python3-setuptools
Requires:   python3-qt5
Requires:   python3-qt5-webengine
Requires:   python3-jinja2
Requires:   python3-pygments
Requires:   python3-PyYAML
Requires:   python3-pyPEG2
Requires:   python3-attrs
Requires:   ((qt5-qtwebengine and python3-qt5-webengine) or (qt5-qtwebkit and python3-qt5-webkit))
Recommends: (qt5-qtwebengine and python3-qt5-webengine)
Recommends: (qt5-qtwebkit and python3-qt5-webkit)
Recommends: python3-cssutils


%description
qutebrowser is a keyboard-focused browser with a minimal GUI. It’s based on
Python, PyQt5 and QtWebEngine and free software, licensed under the GPL.
It was inspired by other browsers/addons like dwb and Vimperator/Pentadactyl.


%prep
%autosetup -n %{srcname}-%{commit0}


%build
# Compile the man page
a2x -f manpage doc/qutebrowser.1.asciidoc
# Compile docs, only release tars have them
# temporary fix
sed -i '82,86 d' doc/contributing.asciidoc
python3 scripts/asciidoc2html.py

# Find all *.py files and if their first line is exactly '#!/usr/bin/env python3'
# then replace it with '#!/usr/bin/python3' (if it's the 1st line).
find . -type f -iname "*.py" -exec sed -i '1s_^#!/usr/bin/env python3$_#!/usr/bin/python3_' {} +

%py3_build


%install
%py3_install

# install .desktop file
desktop-file-install \
    --add-category="Network" \
    --delete-original \
    --dir=%{buildroot}%{_datadir}/applications \
    misc/%{srcname}.desktop

# Install man page
install -Dm644 doc/%{srcname}.1 -t %{buildroot}%{_mandir}/man1

# Install icons
install -Dm644 icons/qutebrowser.svg \
    -t "%{buildroot}%{_datadir}/icons/hicolor/scalable/apps"
for i in 16 24 32 48 64 128 256 512; do
    install -Dm644 "icons/qutebrowser-${i}x${i}.png" \
        "%{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/qutebrowser.png"
done

# Set __main__.py as executable
chmod 755 %{buildroot}%{python3_sitelib}/%{srcname}/__main__.py

# Remove zero-length files:
# https://fedoraproject.org/wiki/Packaging_tricks#Zero_length_files
find %{buildroot} -size 0 -delete


%post
# Update the icon cache:
# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Icon_Cache
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

# Update the desktop database:
# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#desktop-database
/usr/bin/update-desktop-database &> /dev/null || :


%postun
# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Icon_Cache
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#desktop-database
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Icon_Cache
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license LICENSE
%doc README.asciidoc doc/changelog.asciidoc qutebrowser/html/doc
%{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info
%{python3_sitelib}/%{srcname}
%{_bindir}/%{srcname}
%{_datadir}/applications/%{srcname}.desktop
%{_mandir}/man1/%{srcname}.1*
%{_datadir}/icons/hicolor/scalable/apps/%{srcname}.svg
%{_datadir}/icons/hicolor/16x16/apps/%{srcname}.png
%{_datadir}/icons/hicolor/24x24/apps/%{srcname}.png
%{_datadir}/icons/hicolor/32x32/apps/%{srcname}.png
%{_datadir}/icons/hicolor/48x48/apps/%{srcname}.png
%{_datadir}/icons/hicolor/64x64/apps/%{srcname}.png
%{_datadir}/icons/hicolor/128x128/apps/%{srcname}.png
%{_datadir}/icons/hicolor/256x256/apps/%{srcname}.png
%{_datadir}/icons/hicolor/512x512/apps/%{srcname}.png


%changelog
* Fri Jan 05 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.0.4-20180105gitc3bcb1d9
- Build latest git commit

* Fri Dec 15 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.0.4-20171215gite65c0dd8
- Build new git commit

* Tue Nov 28 2017 Timothée Floure <timothee.floure@fnux.ch> - 1.0.4-1
- Rebase to 1.0.4

* Tue Nov 14 2017 Timothée Floure <timothee.floure@fnux.ch> - 1.0.3-2
- Fix typos in some (weak) Qt dependencies

* Tue Nov 07 2017 Timothée Floure <timothee.floure@fnux.ch> - 1.0.3-1
- Rebase to 1.0.3
- Fix dependency issue for architectures unsupported by qt5-qtwebengine

* Fri Oct 20 2017 Timothée Floure <timothee.floure@fnux.ch> - 1.0.2-1
- Rebase to 1.0.2
- Remove the deprecated Group tag
- Add the python3-attrs dependency
- Adapt the descriptions and dependencies to the QtWebEngine backend (new default)
- Doc tag: do not package the PKG-INFO file anymore
- Doc tag: package the full HTML documentation instead of sparse asciidoc files

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 14 2017 Tomas Orsava <torsava@redhat.com> - 0.10.1-1
- Rebased to 0.10.1

* Mon Feb 27 2017 Tomas Orsava <torsava@redhat.com> - 0.10.0-1
- Rebased to 0.10.0
- Updated Source URL

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Tomas Orsava <torsava@redhat.com> - 0.9.1-1
- Rebased to 0.9.1

* Mon Jan 02 2017 Tomas Orsava <torsava@redhat.com> - 0.9.0-1
- Rebased to 0.9.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.8.4-2
- Rebuild for Python 3.6

* Fri Aug 05 2016 Tomas Orsava <torsava@redhat.com> - 0.8.2-1
- New upstream release 0.8.2

* Thu Jul 28 2016 Tomas Orsava <torsava@redhat.com> - 0.8.1-1
- Rebased onto a new upstream version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 13 2016 Tomas Orsava <torsava@redhat.com> - 0.7.0-1
- Updated to a new version
- Removed soft dependency on `colorama` as it is no longer needed

* Fri May 06 2016 Tomas Orsava <torsava@redhat.com> - 0.6.2-1
- Updated to a new upstream version.
- Remover patches specific to the version 0.6.1

* Wed Apr 27 2016 Tomas Orsava <torsava@redhat.com> - 0.6.1-2
- Added 3 upstream patches from the mailing list to help with PyQT crashes
  until 0.6.2 comes out.

* Tue Apr 12 2016 Tomas Orsava <torsava@redhat.com> - 0.6.1-1
- Updated to a new upstream version.
- Simplified the sed command that replaces shebangs.
- Fixed issue with python3-qt5-webkit not being provided by python-qt5 in f23.

* Wed Mar 02 2016 Rex Dieter <rdieter@fedoraproject.org> 0.5.1-2
- Requires: python3-qt5-webkit

* Mon Feb 22 2016 Tomas Orsava <torsava@redhat.com> - 0.5.1-1
- Let there be package.

