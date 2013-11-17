# Note: devel package does not contain any headers. Do I need to add them?
# .so files are shared libraries, I need to call /sbin/ldconfig, but where? In a
# post section for the devel package?
# Schemas handling also needs to be looked at.
Name:           aeskulap
Version:        0.2.2
Release:        0.5beta1%{?dist}
Summary:        A full open source replacement for commercially available DICOM viewers

License:        LGPLv2+
URL:            http://aeskulap.nongnu.org

Source0:        http://www.bms-austria.com/~pipelka/aeskulap/%{name}-%{version}-beta1.tar.gz
Source1:        %{name}-tutorials.pdf
# applied all the patches from the debian package
# svn export svn://svn.debian.org/svn/debian-med/trunk/packages/aeskulap/trunk/ aeskulap-debian
Patch0:         %{name}-circular-svg.patch
Patch2:         %{name}-DcmElement.patch
Patch3:         %{name}-desktop.patch
Patch4:         %{name}-findAndCopyElement.patch
Patch5:         %{name}-gcc.patch
Patch6:         %{name}-i18n.patch
# This is used to update the configure.in before running autoreconf to update the autotoolization. 
Patch7:         %{name}-configure.patch
Patch8:         %{name}-oflog.patch
Patch9:         %{name}-patientNames.patch

BuildRequires:   dcmtk-devel
BuildRequires:   intltool libpng-devel libjpeg-turbo-devel
BuildRequires:   libtiff-devel gtkmm24-devel libglademm24-devel 
BuildRequires:   gconfmm26-devel libtool
BuildRequires:   openssl-devel
BuildRequires:   gettext-devel
BuildRequires:   tcp_wrappers-devel
BuildRequires:   desktop-file-utils
BuildRequires:   GConf2
Requires(pre):   GConf2
Requires(post):  GConf2
Requires(preun): GConf2

%description
Aeskulap is able to load a series of special images stored in the
DICOM format for review. Additionally Aeskulap is able to query
and fetch DICOM images from archive nodes (also called PACS) over
the network.

The goal of this project is to create a full open source replacement
for commercially available DICOM viewers.

Aeskulap is based on gtkmm, glademm and gconfmm and designed to run
under Linux. Ports of these packages are available for different
platforms. It should be quite easy to port Aeskulap to any platform
were these packages are available.

%prep
%setup -q -n %{name}-%{version}-beta1
# configure.in patch
%patch7 -p1
# otherwise it fails
touch ./NEWS
autoreconf -if

# apply patches
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1

# remove bundled copy of dcmtk!
rm -rvf dcmtk

# remove header : Debian used a patch for this
sed -ri "/dcmtk\/dcmdata\/dcdebug\.h/d" ./imagepool/poolfindassociation.cpp ./imagepool/poolmoveassociation.cpp

%build
# point her to the correct lib version depending on the arch
sed -i 's/lib -ldcmjpeg/%{_lib}\/dcmtk -ldcmjpeg/' configure configure.in

%configure --disable-static --disable-schemas-install
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT

install -p -m 0644 %{SOURCE1} -t .

desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

# remove .la files. Is this sufficient?
find $RPM_BUILD_ROOT -name "*.la" -exec rm -fv '{}' \;

%find_lang %{name}

%pre
%gconf_schema_prepare %{name}

%post
%gconf_schema_upgrade %{name}
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%preun
%gconf_schema_remove %{name}

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%doc AUTHORS ABOUT-NLS ChangeLog COPYING README %{name}-tutorials.pdf

%changelog
* Sat Jul 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.2-0.5beta1
- Update scriptlets

* Sat Jul 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.2-0.4beta1
- Update license

* Mon Jul 04 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.2-0.3beta1
- remove autoconf patch and call autoreconf in the spec

* Wed Jun 29 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.2-0.2beta1
- get rid of devel package
- add tutorials as additional documentation
 
* Mon Jun 06 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.2-0.1beta1
- initial rpm build
