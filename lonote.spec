Name:           lonote
Version:        1.8.7
Release:        1%{?dist}
Summary:        Personal Notebook based on Qt Webkit
# The entire source code is GPLv3 except ./lonote/google_dmp/ which is ASL 2.0
License:        GPLv3 and ASL 2.0
URL:            http://code.google.com/p/lonote
Source0:        http://lonote.googlecode.com/files/%{name}-%{version}.7z

BuildArch:      noarch
BuildRequires:  python3-devel >= 3.1
BuildRequires:  /usr/bin/7z
BuildRequires:  desktop-file-utils
Requires:       python3-PyQt4

%description
LoNote is a Note-Taking software based on Python3 and PyQt4. Each page is
saved in HTML format and the program is actually a WYSIWYG HTML editor
specialized for note-taking convenience.

%prep
# %setup does not support 7z format, so we extract it manually
rm -fr %{name}-%{version}
7z x %{SOURCE0}
cd %{name}-%{version}
# Remove a shebang
sed -i -e '/^#!\//, 1d' lonote/google_dmp/diff_match_patch.py

%build
cd %{name}-%{version}
python3 setup.py build

%install
cd %{name}-%{version}
python3 setup.py install --root=%{buildroot} --skip-build

# Rearrage the documents to conform Fedora convention
rm -r %{buildroot}%{_docdir}/%{name}/doc/{PO_FILE,localization}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
mv %{buildroot}%{_docdir}/%{name}/doc/* %{buildroot}%{_docdir}/%{name}-%{version}
rm -fr %{buildroot}%{_docdir}/%{name}/

# validate the desktop entry file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%files -f %{name}-%{version}/%{name}.lang
%{_docdir}/%{name}-%{version}/
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}-*.egg-info
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*


%changelog
* Wed Oct 24 2012 Robin Lee <cheeselee@fedoraproject.org> - 1.8.7-1
- Update to 1.8.7

* Wed Oct 10 2012 Robin Lee <cheeselee@fedoraproject.org> - 1.8.6-2
- Fix and validate the desktop entry file

* Tue Oct  9 2012 Robin Lee <cheeselee@fedoraproject.org> - 1.8.6-1
- Submit for Fedora
