%global projectname     freemedforms
%global releasetarname   freemedformsfullsources


Name:           freemedforms
Version:        0.7.5
Release:        6%{?dist}
Summary:        The freemedforms application suite metapackage

License:        GPLv3+ and LGPLv2
URL:            http://www.%{name}.com
Source0:        http://freemedforms.googlecode.com/files/%{releasetarname}-%{version}.tgz
Source1:        %{name}.1


# the config option doesn't appear to work. It still produces a libquazip.so
Patch0:         %{name}-%{version}-remove-quazip.patch
# patch command line parser to try fix segfault
Patch1:         %{name}-%{version}-commandline-parser.patch

BuildRequires:  qt-devel libXext-devel qt-mysql 
BuildRequires:  desktop-file-utils
BuildRequires:  quazip-devel libzip-devel
BuildRequires:  minizip-devel 
BuildRequires:  zlib-devel 

# pull in emr
Requires:       %{projectname}-emr%{?_isa} >= %{version}-%{release}
# pull in freediams
Requires:       freediams%{?_isa} >= %{version}-%{release}

# filter provides and requires. The so files are private plugins
%{?filter_setup:
%filter_provides_in %{_libdir}/%{name}/
%filter_provides_in %{_libdir}/%{projectname}-common/
%filter_requires_in %{_libdir}/%{name}/
%filter_requires_in %{_libdir}/%{projectname}-common/

%filter_from_requires /libUtils/d ; /libExtensionSystem/d ; /libTranslationUtils/d ; /libAggregation/d

%filter_setup
}
%description
FreeMedForms aims to be a open Electronic Medical Record Manager.
FreeMedForms is also a lot of derivatives sub-project, which are
just standalone compilation of FreeMedForms plugins.

This project is a free and open source project. A community grows up
around it. FreeMedForms and derivatives is released under the terms
of the new BSD License. Some parts of the code are LGPL v2.1.

FreeMedForms and Derivatives are coded in C++/Qt4.4.3 at least.
FreeMedForms and Derivatives are available for :
- MacOs X universal
- Linux : Ubuntu, Debian, OpenSuse, standalone binary
- FreeBSD : need compilation of SVN trunk (please contact author)
- Windows

This is a meta package that pulls in the EMR freediams and freeaccounts


%package emr
Summary:    The freemedforms EMR
# noarch requires
Requires:   %{projectname}-emr-data >= %{version}-%{release}
Requires:   %{projectname}-common-resources >= %{version}-%{release}

Requires:   %{projectname}-common-libs%{?_isa} >= %{version}-%{release}

# Obsolete previous packages since we've split into new subpackage scheme
Obsoletes:      %{name} < 0.5.9-0.7.alpha1
Obsoletes:      %{name}-devel < 0.5.9-0.7.alpha1

%description emr
The freemedforms main EMR

Please install the freemedforms-emr-docs-en,fr 
or the freemedforms-emr-translations packages if required

%package emr-data
Summary:    Architecture independant data used by the freemedforms EMR
BuildArch:  noarch

%description emr-data
This package contains the data packs, images and other architecture independant 
data used by the freemedforms EMR

%package emr-docs-en
Summary:    English documentation for the freemedforms EMR
BuildArch:  noarch

%description emr-docs-en
This package contains HTML documentation in English for the freemedforms EMR

%package emr-docs-fr
Summary:    French documentation for the freemedforms EMR
BuildArch:  noarch

%description emr-docs-fr
This package contains HTML documentation in French for the freemedforms EMR

%package common-translations
Summary:    Translation files for the freemedforms EMR
BuildArch:  noarch

%description common-translations
This package contains translation files for the freemedforms suite.
Languages contained are: English, Frence and Deutsch

%package common-libs
Summary:    Common files utilized by the freemedforms suite

%description common-libs
These are files that are shared between the applications of the freemedforms
suite, such as freemedforms, freediams, freeaccount, freeicd, freepad,
freetoolbox.

All applications of the suite should require this package when they are
packaged for Fedora instead of re-generating these files. See the freediams
package for hints on how to do this.

%package common-resources
Summary:    Common resources used by the frreemedforms suite
BuildArch:  noarch

%description common-resources
This package contains textfiles that are shared between the applications of the
freemedforms suite such as freemedforms, freediams, freeaccount, freeicd,
freepad, freetoolbox

All applications of the suite should require this package when they are
packaged for Fedora instead of re-generating these files. See the freediams
package for hints on how to do this.


%prep
%setup -q
%patch0 -p1 -b .removes_bundled_quazip_req
%patch1 -p0 -b .patches_command_line

# contrib/quazip is the location of the bundled quazip library
# delete everything other than the modified global.h and global.cpp files
find ./contrib/  ! -name "global.*" ! -name "exporter.h" -exec rm -fv '{}' \;

# correct include : could've used a patch too I guess
sed -i 's|#include <quazip/quazip/quazipfile.h>|#include <quazip/quazipfile.h>|' plugins/saverestoreplugin/saverestorepage.cpp

# correct end of file rpmlint error
sed -i 's/\r//' README.txt COPYING.txt

%build
export PATH=$PATH:/usr/%{_lib}/qt4/bin/

lrelease global_resources/translations/*.ts 
qmake %{name}.pro -r -config release "CONFIG+=LINUX_INTEGRATED" "CONFIG+=dontbuildquazip" "INSTALL_ROOT_PATH=$RPM_BUILD_ROOT%{_prefix}" "LOWERED_APPNAME=%{name}" "LIBRARY_BASENAME=%{_lib}"
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
install -p -m 0644 %{SOURCE1} -t $RPM_BUILD_ROOT/%{_mandir}/man1/

chmod -v 0755 $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.so*
chmod -v 0755 $RPM_BUILD_ROOT/%{_libdir}/%{name}-common/*.so*
chmod -v 0755 $RPM_BUILD_ROOT/%{_bindir}/%{name}
# internal libraries, let rpath be
#chrpath --delete $RPM_BUILD_ROOT/%{_libdir}/FreeMedForms/*.so*
#chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/FreeMedForms

# fix up desktop file
sed -r -i "s/Categories=Office;MedicalSoftware/Categories=Office;/" ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
sed -r -i "/Version/d" ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
# validate desktop file
desktop-file-validate \
${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop


# remove packagehelpers part
rm -fvr $RPM_BUILD_ROOT/%{_datadir}/%{name}/package_helpers/

%files
%doc COPYING.txt README.txt

%files emr
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*pluginspec
%dir %{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg
%{_mandir}/man1/%{name}.*
%{_docdir}/%{projectname}-project/%{name}/

%files emr-data
%{_datadir}/%{name}/forms/
%{_datadir}/%{name}/profiles/

%files emr-docs-en
%{_docdir}/%{projectname}-project/%{name}/en/

%files emr-docs-fr
%{_docdir}/%{projectname}-project/%{name}/fr/

%files common-translations
%{_datadir}/%{name}/translations/

%files common-libs
%dir %{_libdir}/%{projectname}-common
%{_libdir}/%{projectname}-common/*so.*
%{_libdir}/%{projectname}-common/*so

%files common-resources
%dir %{_docdir}/%{projectname}-project/
%{_datadir}/%{projectname}/textfiles/
%{_datadir}/%{name}/sql/
%{_datadir}/%{name}/datapacks/
%{_datadir}/%{name}/pixmap/

%changelog
* Thu Jun 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-6
- Some more reorganizing of files in packages:
- the sql, datapacks, pixmaps are common components for the entire suite

* Thu Jun 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-5
- Bump spec for ownership changes

* Thu Jun 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-4
- Added freediams
- Split another subpackage for common-resources
- Added projectname macro to use in project common files

* Thu Jun 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-3
- Try patch upstream suggested
- Add obsoletes to maintain upgrade path

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-2
- Split to subpackages to make it easier to install suite applications
- Split arch indep packages

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-1
- Update to 0.7.5

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.4-1
- Update to 0.7.4

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.9-0.6.alpha1
- Filter requires!

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.9-0.5.alpha1
- Remove stray requires on -devel package (removed)

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.9-0.4.alpha1
- Filter provides

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.9-0.3.alpha1
- Remove devel package since so files are privately used plug-ins
- rhbz#742396

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-0.2.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.9-0.1alpha1
- Let rpath be
- Corrections as Eric suggested at https://bugzilla.redhat.com/show_bug.cgi?id=707002#c2

* Sat May 28 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.9-0.1alpha1
- Used chrpath to remove rpath additions
- Initial rpm build
- Based on the spec used for OpenSUSE maintained by Sascha Manns.

