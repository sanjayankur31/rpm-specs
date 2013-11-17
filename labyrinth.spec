Name:           labyrinth
Version:        0.6
Release:        1%{?dist}
Summary:        A light weight mind mapping tool

License:        GPLv2+
URL:            https://github.com/%{name}-team/%{name}
#Source0:        https://github.com/%{name}-team/%{name}/archive/0.6.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel desktop-file-utils gettext
Requires:       pygtk2 pycairo pyxdg pygobject2

%description
Labyrinth is a lightweight mind-mapping tool, written in Python using Gtk and
Cairo to do the drawing. It is intended to be as light and intuitive as
possible, but still provide a wide range of powerful features.

A mind-map is a diagram used to represent words, ideas, tasks or other items
linked to and arranged radially around a central key word or idea. It is used
to generate, visualize, structure and classify ideas, and as an aid in study,
organization, problem solving, and decision making. (From Wikipedia)

Currently, Labyrinth provides 3 different types of thoughts, or nodes - Text,
Image and Drawing. Text is the basic standard text node. Images allow you to
insert and scale any supported image file (PNG, JPEG, SVG). Drawings are for
those times when you want to illustrate something, but don't want to fire up a
separate drawing program. It allows you to quickly and easily sketch very
simple line diagrams.


%prep
%setup -q

# Remove windows files
rm -rf Windows

# Correct non executable script rpmlint error
sed -ibackup '1 d' %{name}_lib/MMapArea.py
sed -ibackup '1 d' %{name}_lib/TextThought.py


%build
%{__python} setup.py build
# Translations
make -C po

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/16x16/apps
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/22x22/apps
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/24x24/apps
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/scalable/apps
install -m 644 data/%{name}-16.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/16x16/apps/%{name}.png
install -m 644 data/%{name}-22.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/22x22/apps/%{name}.png
install -m 644 data/%{name}-24.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/24x24/apps/%{name}.png
install -m 644 data/%{name}.svg $RPM_BUILD_ROOT/usr/share/icons/hicolor/scalable/apps/%{name}.svg

#Translations
make -C po localedir=$RPM_BUILD_ROOT/%{_datadir}/locale install

desktop-file-install                                    \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
data/%{name}.desktop

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING NEWS README.rst doc/
%{python_sitelib}/%{name}_lib/
%{_bindir}/%{name}
%{python_sitelib}/Labyrinth-%{version}-py?.?.egg-info
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*



%changelog
* Mon Jul 08 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.6-1
- Initial rpm build
- Remove windows files
- RHBZ 982255

