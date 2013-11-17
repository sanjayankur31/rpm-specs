%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
    %{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
    %{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
    %endif

Name:           memaker
Version:        20100110
Release:        1%{?dist}
Summary:        An avatar creator

Group:          Amusements/Graphics
License:        GPLv3+
URL:            https://launchpad.net/memaker 

# tar created from a bzr 
#
# bzr branch lp:memaker && tar -czvf memaker-20100110-bzr.tar.gz memaker
Source0:        %{name}-%{version}-bzr.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

#BuildRequires:  gettext
BuildRequires:  python2-devel python-distutils-extra redhat-lsb intltool
BuildRequires:  desktop-file-utils
Requires:       gnome-python2-rsvg notify-python numpy python-imaging 

%description
MeMaker gives users a wide variety of images that, when placed 
together, create an avatar. This avatar is intended to represent 
the way that this person is in some way. The goal of the project 
is to have enough images that anyone can create an image that 
they feel would closely represent them without having to use a photo
in the image itself.

%prep
%setup -q -n %{name}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

# not copied by setup script
cp -av data/labels $RPM_BUILD_ROOT/%{_datadir}/%{name}/

# icons and desktop files
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/scalable/apps/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/

desktop-file-install                                    \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
./build/share/applications/%{name}.desktop

cp -av data/icons/scalable/apps/%{name}.svg $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/scalable/apps/
cp -av data/icons/48x48/apps/%{name}.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/

for lib in $RPM_BUILD_ROOT%{python_sitelib}/MeMaker/*.py; do
 sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

for lib in $RPM_BUILD_ROOT%{python_sitelib}/MeMaker/utils/*.py; do
 sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

for lib in $RPM_BUILD_ROOT%{python_sitelib}/MeMaker/view/*.py; do
 sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

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
%doc AUTHORS COPYING README TODO
%{_datadir}/%{name}/
%{_bindir}/%{name}
%{python_sitelib}/MeMaker/
%{python_sitelib}/%{name}-?.?-py?.?.egg-info
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/applications/%{name}.desktop 


%changelog
* Mon May 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20100110-1
- Correcting the directory ownership
- #608319
- replaced "memaker" with name macro 
- changed cp -v to cp -av to preserve timestamps
- update to upstream dev 

* Tue Jun 22 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5-1
- initial rpm build
