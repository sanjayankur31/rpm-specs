Name: dcmtk
Summary: Offis DICOM Toolkit (DCMTK)
Version: 3.6.4
Release: 3%{?dist}
License: BSD
Source0: ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk364/dcmtk-3.6.4.tar.gz
URL: http://dicom.offis.de/dcmtk.php.en

Patch0:     0001-3.6.4-Use-system-CharLS-include.patch
Patch1:     0002-3.6.4-Add-FindCharLS.patch
Patch2:     0003-3.6.4-Find-and-include-CharLS.patch
Patch3:     0004-3.6.4-Use-cmake-suggested-locations-for-CharLS.patch
Patch4:     0005-3.6.4-Correct-CharLS-API-call.patch
Patch5:     0006-3.6.4-Remove-reference-to-bundled-CharLS.patch
Patch6:     0007-3.6.4-Update-JLS_ERROR-to-jpegls_error-in-CharLS-usa.patch
Patch7:     0008-3.6.4-correct-JpegLsReadHeader-arguments.patch
Patch8:     0009-3.6.4-update-JlsParameters-for-new-CharLS.patch
Patch9:     0010-3.6.4-correct-JpegLsDecode-arguments-for-CharLS-2.patch
Patch10:    0011-3.6.4-update-ilv-for-new-CharLS.patch
Patch11:    0012-3.6.4-Correct-extra-include-for-CharLS.patch
Patch12:    0013-3.6.4-Update-errors-to-use-enum-class-in-CharLS-2.patch
Patch13:    0014-3.6.4-define-BYTE-for-CharLS.patch
Patch14:    0015-3.6.4-Update-colorTransformation-for-CharLS-2.patch
Patch15:    0016-3.6.4-Update-JpegLsEncode-for-CharLS-2.patch



BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: git-core
BuildRequires: cmake
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libxml2-devel
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: zlib-devel
BuildRequires: CharLS-devel >= 2.0.0
BuildRequires: doxygen

%description
DCMTK is a collection of libraries and applications implementing large
parts the DICOM standard. It includes software for examining,
constructing and converting DICOM image files, handling offline media,
sending and receiving images over a network connection, as well as
demonstrative image storage and worklist servers. DCMTK is is written
in a mixture of ANSI C and C++.  It comes in complete source code and
is made available as "open source" software. This package includes
multiple fixes taken from the "patched DCMTK" project.

Install DCMTK if you are working with DICOM format medical image files.

%package devel
Summary: Development Libraries and Headers for dcmtk
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: CharLS-devel%{?_isa}
Requires: libpng-devel%{?_isa}
Requires: libtiff-devel%{?_isa}

%description devel
Development Libraries and Headers for dcmtk.  You only need to install
this if you are developing programs that use the dcmtk libraries.

%prep
%autosetup -n %{name}-%{version} -p1 -S git

# Remove bundled libraries
rm -rf dcmjpls/libcharls/

# Fix permissions
find . -type f -name "*.h" -exec chmod 0644 '{}' \;
find . -type f -name "*.cc" -exec chmod 0644 '{}' \;

%build
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
export LDFLAGS="%{__global_ldflags} -fPIC"
%cmake -DCMAKE_BUILD_TYPE:STRING="Release" \
 -DDCMTK_INSTALL_LIBDIR=%{_lib} \
 -DDCMTK_INSTALL_CMKDIR=%{_lib}/cmake/%{name} \
 -DCMAKE_INSTALL_DOCDIR:PATH=%{_pkgdocdir} \
 -DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
 -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir}/man1 \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
 -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
 -DCMAKE_INSTALL_DATADIR:PATH=share \
 -DBUILD_APPS:BOOL=ON \
 -DBUILD_SHARED_LIBS:BOOL=ON \
 -DBUILD_SINGLE_SHARED_LIBRARY:BOOL=OFF \
 -DDCMTK_WITH_OPENSSL:BOOL=ON \
 -DDCMTK_WITH_PNG:BOOL=ON \
 -DDCMTK_WITH_PRIVATE_TAGS:BOOL=ON \
 -DDCMTK_WITH_TIFF:BOOL=ON \
 -DDCMTK_WITH_XML:BOOL=ON \
 -DDCMTK_WITH_CHARLS=ON \
 -DDCMTK_WITH_ZLIB:BOOL=ON \
 -DDCMTK_ENABLE_CXX11:BOOL=ON .
%make_build

%install
%make_install

# Remove zero-lenght file
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/wlistdb/OFFIS/lockfile

%ldconfig_scriptlets

%check
ctest %{?_smp_mflags} .

%files
%license COPYRIGHT
%{_pkgdocdir}/
%{_bindir}/*
%{_libdir}/*.so.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/dcmpstat.cfg
%config(noreplace) %{_sysconfdir}/%{name}/dcmqrscp.cfg
%config(noreplace) %{_sysconfdir}/%{name}/printers.cfg
%config(noreplace) %{_sysconfdir}/%{name}/storescp.cfg
%config(noreplace) %{_sysconfdir}/%{name}/storescu.cfg
%config(noreplace) %{_sysconfdir}/%{name}/filelog.cfg
%config(noreplace) %{_sysconfdir}/%{name}/logger.cfg
%{_datadir}/%{name}/
%{_mandir}/man1/*

%files devel
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/cmake/%{name}/

%changelog
* Sun Jul 28 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.4-3
- Update to use CharLS v2

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 09 2019 Antonio Trande <sagitterATfedoraproject.org> - 3.6.4-1
- Release 3.6.4
- Use %%_pkgdocdir
- Active modern C++ support
- Enable tests

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6.2-2
- Switch to %%ldconfig_scriptlets

* Sun Dec 10 2017 Jens Lody <fedora@jenslody.de> - 3.6.2-1
- Update to 3.6.2, fixes rhbz #1440439.
- Do not use deprecated tcp-wrappers, fixes rhbz #1518760.

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 3.6.1-8
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.6.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Dec 15 2014 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 3.6.1-1
- Upgraded to new upstream version.
- Various fixes to the specfile
- Fixes CVE-2013-6825 dcmtk: possible privilege escalation if setuid() fails

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 3.6.0-16
- General spec cleanup
- Move libs into _lib and remove ldd config file
- Fixes versioned doc dir as per BZ993719
- Bump up release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 3.6.0-14
- Added more requires to devel package as per BZ922937
- Added _isa to explicit requires

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 01 2012 Jon Ciesla <limburgher@gmail.com> - 3.6.0-12
- FTBFS, BZ 819236.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-10
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.6.0-8
- Rebuild for new libpng

* Thu Oct 20 2011 Dan Horák <dan[at]danny.cz> 3.6.0-7
- skip the EOL conversion step, files are correct (FTBFS due a change in dos2unix)

* Wed Oct 19 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-6
- Added explicit require for CharLS-devel as requested in #745277

* Wed Apr 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-5
- Fixed dir ownership

* Wed Apr 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-4
- Added doxygen BR

* Tue Mar 22 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-3
- Fixed soname generation for residual modules

* Mon Mar 21 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-2
- Fixed shared library generation
- Fixed patch schema numbering

* Sun Mar 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-1
- Removed bundled charls
- Rebased on public dcmtk git repository

* Thu Feb 3 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.1-1.20110203git
- Updated to new version
- Added patch to fix shared lib generation

* Tue Oct 19 2010 Mario Ceresa <mrceresa@fedoraproject.org> 3.5.4-4
- Adding soname's to generated lib

* Mon Mar 15 2010 Andy Loening <loening@alum dot mit dot edu> 3.5.4-3
- updates for packaging with fedora core
- multiple fixes/enhancements from pdcmtk version 48

* Sat Jan 02 2010 Andy Loening <loening@ alum dot mit dot edu> 3.5.4-2
- tlslayer.cc patch for openssl 1.0

* Thu Feb 02 2006 Andy Loening <loening @ alum dot mit dot edu> 3.5.4-1
- initial build
