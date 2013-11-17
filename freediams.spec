%global projectname     freemedforms
%global releasetarname   freemedformsfullsources


Name:           freediams
Version:        0.7.5
Release:        5%{?dist}
Summary:        The pharmaceutical prescription assistant

License:        GPLv3+ and LGPLv2
URL:            http://www.%{projectname}.com
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

# Use already generated libs from freemedforms-common
BuildRequires:  %{projectname}-common-libs

# Require the common subpackage that contains files shared by the suite's
# applications
Requires:       %{projectname}-common-libs%{?_isa} >= %{version}-%{release}
Requires:       %{projectname}-common-resources >= %{version}-%{release}

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
FreeDiams prescriber is the result of FreeMedForms prescriber plugins built
into a standalone application. FreeDiams is a multi-platform (MacOS, Linux,
FreeBSD, Windows), free and open source released under the GPLv3 license.

It is mainly developed by medical doctors and is intended for use by these same
professionals. It can be used alone to prescribe and / or test drug
interactions within a prescription. It can be linked to any application thanks
to its command line parameters.

FreeDiams can manage multiple drugs databases. Some drugs databases are already
available:

    French (sources: AFSSAPS)
    Canadian (sources: HCDPD)
    USA (sources: FDA)
    South African (sources: AEPI)

The interactions database (source: AFSSAPS) give access to many informations:

    interactions by themselves
    risk level
    nature of the risk
    management of the interaction

This is part of the freemedforms suite of applications


%package docs-en
Summary:    English documentation for freediams
BuildArch:  noarch

%description docs-en
This package contains HTML documentation in English for freediams

%package docs-fr
Summary:    French documentation for freediams
BuildArch:  noarch

%description docs-fr
This package contains HTML documentation in French for freediams

%prep
%setup -q -n %{projectname}-%{version}
%patch0 -p1 -b .removes_bundled_quazip_req
%patch1 -p0 -b .patches_command_line

# contrib/quazip is the location of the bundled quazip library
# delete everything other than the modified global.h and global.cpp files
find ./contrib/  ! -name "global.*" ! -name "exporter.h" -exec rm -fv '{}' \;

# Make use of already built libraries from freemedforms
# This will need to be done for all applications in the suite
sed -i 's|\(LIBS \*= -L$${BUILD_PLUGIN_PATH} -L$${BUILD_LIB_PATH}\)|\1 -L%{_libdir}/%{projectname}-common/|' buildspecs/config.pri

# correct include : could've used a patch too I guess
sed -i 's|#include <quazip/quazip/quazipfile.h>|#include <quazip/quazipfile.h>|' plugins/saverestoreplugin/saverestorepage.cpp

# correct end of file rpmlint error
sed -i 's/\r//' README.txt COPYING.txt


%build
export PATH=$PATH:/usr/%{_lib}/qt4/bin/

lrelease global_resources/translations/*.ts 
qmake %{name}.pro -r -config release "CONFIG+=LINUX_INTEGRATED" "CONFIG+=dontbuildquazip" "CONFIG+=dontbuildlibs" "CONFIG+=dontinstallresources" "CONFIG+=dontinstalllibs"  "INSTALL_ROOT_PATH=$RPM_BUILD_ROOT%{_prefix}" "LOWERED_APPNAME=%{name}" "LIBRARY_BASENAME=%{_lib}"
#qmake %{name}.pro -r -config debug "CONFIG+=LINUX_INTEGRATED" "CONFIG+=dontbuildquazip" "CONFIG+=dontinstallresources" "CONFIG+=dontinstalllibs"  "INSTALL_ROOT_PATH=$RPM_BUILD_ROOT%{_prefix}" "LOWERED_APPNAME=%{name}" "LIBRARY_BASENAME=%{_lib}"
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
install -p -m 0644 %{SOURCE1} -t $RPM_BUILD_ROOT/%{_mandir}/man1/

chmod -v 0755 $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.so*
chmod -v 0755 $RPM_BUILD_ROOT/%{_bindir}/%{name}

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
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg
%{_mandir}/man1/%{name}.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*pluginspec
%dir %{_docdir}/%{projectname}-project/%{name}/

%files docs-en
%{_docdir}/%{projectname}-project/%{name}/en/

%files docs-fr
%{_docdir}/%{projectname}-project/%{name}/fr/

%changelog
* Thu Jun 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-5
- Added a patch to fix segfaulting

* Thu Jun 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-4
- Cleaned spec, removed superflous commands and comments
- added requires on common resources

* Thu Jun 28 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-3
- specbump to bring it up to speed with freemedforms

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-2
- Update patch

* Wed Jun 27 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-1
- Initial rebuild with 0.7.5
