Name:		vxl	
Version:	1.18.0	
Release:	1%{?dist}
Summary:	C++ Libraries for Computer Vision Research and Implementation
License:	BSD
URL:		https://sf.net/projects/vxl/
# Need to remove the non-free lena image from the sources
# tar xf vxl-1.18.0.tar.gz
# rm -rf vxl-1.18.0/contrib/prip/vdtop/tests/lena.org.pgm 
# tar cfz vxl-1.18.0-clean.tar.gz vxl-1.18.0/
#Source0:   https://github.com/vxl/vxl/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}-clean.tar.gz
# Fedora has a distribution-specific include dir
Patch1:		0001-Added-include-path-for-geotiff.patch
Patch2:		0002-Added-soname-info-for-core-libraries.patch
# Use system rply and don't use mpeg2
Patch3:		0003-Use-system-rply.patch
Patch4:		0004-Added-more-soname.patch
Patch5:		0005-Do-not-build-OUL.patch
Patch6:		0006-BUG-rplyConfig.cmake-has-wrong-include-path.patch
Patch7:		0007-Arguments-of-ply_open-and-create-changed.-Thanks-to-.patch
Patch8:		0008-More-sonames.patch
Patch9:		0009-Bumped-up-version-to-1.14.patch
#TODO: Refers to contrib and is therefore not correct
Patch10:	0010-Use-system-FindEXPAT.patch
Patch11:	0011-Do-not-use-bundled-minizip.patch
Patch12:	0012-Added-Coin3D-Submitted-by-Volker-Frohlich.patch
Patch13:	0013-Added-SIMVoleon-Submitted-by-Volker-Frohlich.patch
Patch14:	0014-Added-additional-search-path-for-xerces-Submitted-by.patch
Patch15:	0015-Manage-KL-library-Submitted-by-Volker-Frohlich.patch
Patch16:	0016-Manage-KL-library-2-2-Submitted-by-Volker-Frohlich.patch
Patch17:	0017-Add-sonames-to-vpgl-lib.patch
Patch18:	0018-Added-sonames-to-vgui-vidl-vpdl-Qv-libs.patch
Patch19:	0019-Removed-box2m-which-requires-OpenCL-libraries.patch
Patch20:	0020-Included-missing-vcl_cstdio.h-header.patch
Patch21:	0021-Use-expatpp.h-which-is-provided-by-fedora-repos.patch
Patch22:	0022-Include-missing-vcl_cstdio.h-header.patch
Patch23:	0023-Remove-volm-because-of-error-in-function-prototype.patch
Patch24:	0024-Added-missing-sonames-for-mvl2-and-vepl1.patch
Patch25:	0025-Legacy-def1-r35963.patch
Patch26:	0026-Legacy-def2-r36001.patch

Patch50:        vxl-0.17.0-gcc5.diff
Patch51:	vxl-1.17.0-gcc6.patch

Patch100:	%{name}-1.17.0-secondary.patch

#KL is used in an "UNMAINTAINED_LIBRARY", vgel is only built on request

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:	cmake 
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	Coin2-devel
BuildRequires:	dcmtk-devel
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	expatpp-devel
BuildRequires:	freeglut-devel
BuildRequires:	klt-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libXmu-devel 
BuildRequires:	libXi-devel
BuildRequires:	libjpeg-devel
%ifnarch s390 s390x
BuildRequires:	libdc1394-devel
%endif
BuildRequires:	libgeotiff-devel
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	minizip-compat-devel
BuildRequires:	rply-devel
BuildRequires:	SIMVoleon-devel
BuildRequires:	shapelib-devel
BuildRequires:	texi2html
BuildRequires:	xerces-c-devel
BuildRequires:	zlib-devel

#GUI needs wx, a desktop file and an icon

%description
VXL (the Vision-something-Libraries) is a collection of C++ libraries designed
for computer vision research and implementation. It was created from TargetJr
and the IUE with the aim of making a light, fast and consistent system. 
VXL is written in ANSI/ISO C++ and is designed to be portable over many
platforms.


%package	doc
Summary:	Documentation for VXL library
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc

You should install this package if you would like to
have all the documentation

%package	devel
Summary:	Headers and development libraries for VXL
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel

You should install this package if you would like to
develop code based on VXL.

%prep
%autosetup -N

#Remove bundled library (let's use FEDORA's ones)
# v3p/netlib (made by f2c) dependency not removed because of heavily modifications
# QV is a Silicon Graphics' VRML parser from the 90s. Now unmantained.
for l in jpeg png zlib tiff geotiff rply dcmtk bzlib
do
	find v3p/$l -type f ! -name 'CMakeLists.txt' -execdir rm {} +
done

find contrib/brl/b3p/shapelib -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/minizip -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/expat -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/gel/vgel/kl -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/expatpp -type f ! -name 'CMakeLists.txt' -execdir rm {} +

# v3p/mpeg2 lib in fedora is not enough to build the target. Moreover it is in rpmfusion repo

#TODO: Various
#vxl-devel.x86_64: E: invalid-soname /usr/lib64/libvvid.so libvvid.so

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch50 -p1
%patch51 -p1 -b .gcc6
%patch100 -p1 -b .secondary


#Fix lib / lib64 problem during install:
find . -name CMakeLists.txt -exec sed -i "s/INSTALL_TARGETS([ ]*\/lib/INSTALL_TARGETS(\/lib\$\{LIB_SUFFIX\}/;" {} +

# Fix executable permissions on source file
find . -name "*.h" | xargs chmod ugo-x
find . -name "*.cxx" | xargs chmod ugo-x
find . -name "*.txx" | xargs chmod ugo-x

%build
%cmake -DCMAKE_VERBOSE_MAKEFILE=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DVXL_FORCE_B3P_EXPAT:BOOL=OFF \
	-DVXL_FORCE_V3P_DCMTK:BOOL=OFF \
	-DVXL_FORCE_V3P_GEOTIFF:BOOL=OFF \
	-DVXL_USING_NATIVE_KL=ON \
	-DVXL_FORCE_V3P_JPEG:BOOL=OFF \
	-DVXL_FORCE_V3P_MPEG2:BOOL=OFF \
	-DVXL_FORCE_V3P_PNG:BOOL=OFF \
	-DVXL_FORCE_V3P_TIFF:BOOL=OFF \
	-DVXL_FORCE_V3P_ZLIB:BOOL=OFF \
	-DVXL_FORCE_V3P_RPLY:BOOL=OFF \
	-DVXL_USING_NATIVE_ZLIB=ON \
	-DVXL_USING_NATIVE_JPEG=ON \
	-DVXL_USING_NATIVE_PNG=ON \
	-DVXL_USING_NATIVE_TIFF=ON \
	-DVXL_USING_NATIVE_GEOTIFF=ON \
	-DVXL_USING_NATIVE_EXPAT=ON \
	-DVXL_USING_NATIVE_SHAPELIB=ON \
	-DVXL_USING_NATIVE_BZLIB2=ON \
	-DBUILD_VGUI=OFF \
	-DBUILD_BGUI3D=OFF \
	-DBUILD_OXL:BOOL=ON \
	-DBUILD_BRL=OFF \
	-DBUILD_CORE_GEOMETRY:BOOL=ON \
	-DBUILD_CORE_IMAGING:BOOL=ON \
	-DBUILD_CORE_NUMERICS:BOOL=ON \
	-DBUILD_CORE_PROBABILITY:BOOL=ON \
	-DBUILD_CORE_SERIALISATION:BOOL=ON \
	-DBUILD_CORE_UTILITIES:BOOL=ON \
	-DBUILD_CORE_VIDEO:BOOL=ON \
	-DBUILD_EXAMPLES:BOOL=OFF \
	-DBUILD_TESTING:BOOL=OFF \
	-DBUILD_DOCUMENTATION:BOOL=ON \
	-DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo" \
	-DCMAKE_CXX_FLAGS:STRING="$RPM_OPT_FLAGS -fpermissive" \
	-DPYTHON_LIBRARY=/usr/lib64/libpython2.7.so \
	-DVNL_CONFIG_LEGACY_METHODS=ON .

# Why is expat stated, but not shapelib?
# DCMDK Cmake -- Included in bundle, but why?
#BUILD_VGUI? NO, it depends on box2m which in turns relies on OPENCL which is not available in FEDORA
#wxwidgets seems to be found
#Multiple versions of QT found please set DESIRED_QT_VERSION
#TODO: Xerces for brl
#TODO: Testing?
#BR: coin2, coin3 (coin3d) brl, bbas

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%check
ctest .

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc core/vxl_copyright.h
%{_libdir}/*.so.*
%{_bindir}/*
#%{_datadir}/%{name}/

%files devel
%{_datadir}/%{name}
%{_includedir}/%{name}
%{_libdir}/*.so

%files doc
%doc %{_docdir}/*




%changelog
* Tue Aug 28 2018 Patrik Novotný <panovotn@redhat.com> - 1.17.0-28
- change requires to minizip-compat(-devel), rhbz#1609830, rhbz#1615381

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 1.17.0-26
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 25 2016 Tom Callaway <spot@fedoraproject.org> - 1.17.0-20
- remove non-free lena image file from source tarball (bz1310388)
- fix FTBFS (bz1303695, bz1308234)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 16 2015 Sebastian Pölsterl <sebp@k-d-w.org> - 1.17.0-17
- Rebuilt using hardened build flags: https://fedoraproject.org/wiki/Changes/Harden_All_Packages

* Mon Feb 16 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.17.0-16
- Add vxl-0.17.0-gcc5.diff (Work-around GCC-5.0.0 FTBFS RHBZ#1192886).
- Fix bogus %%changelog date.

* Mon Aug 25 2014 Devrim Gündüz <devrim@gunduz.org> - 1.17.0-15
- Rebuilt for libgeotiff 

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-11
- Applied upstream patches (25, 26) to ensure compatibility with ITK

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.17.0-9
- rebuild due to "jpeg8-ABI" feature drop

* Wed Dec 05 2012 Dan Horák <dan[at]danny.cz> - 1.17.0-8
- fix build on non-x86 arches

* Sun Nov 25 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-7%{?dist}
- Changed source0 path to point to vxl 1.17
- Added missing sonames

* Fri Nov 02 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-6%{?dist}
- Patched to build BRL
- Updated to last version

* Mon Oct 29 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-5%{?dist}
- Removed expatpp bundled library and added corresponding BR
- Removed bundled bzip


* Thu Oct 18 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-4%{?dist}
- Fixed missing oxl_vrml lib
- Turn on compilation of BRL

* Sun Oct 14 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-3%{?dist}
- More fixes from Volker's post https://bugzilla.redhat.com/show_bug.cgi?id=567086#c42
- 

* Wed Oct 10 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-2%{?dist}
- Added patches 12-16 from https://bugzilla.redhat.com/show_bug.cgi?id=567086#c42
- Minor rework of the spec file as pointed out by Volker in the previous link

* Wed Oct 10 2012 Mario Ceresa mrceresa fedoraproject org vxl 1.17.0-1%{?dist}
- Updated to new version
- Reworked patches to the new version
- Disabled BRL because it gives a compilation error

* Fri May 27 2011 Mario Ceresa mrceresa fedoraproject org vxl 1.14.0-1%{?dist}
- Updated to new version
- Added BR doxygen (thanks to Ankur for noticing it)
- Changed patch naming schema
- Work around a rply related bug (patches 3-6)
- Thanks to Thomas Bouffon for patch 7-8
- Patches 9-10 address http://www.itk.org/pipermail/insight-users/2010-July/037418.html
- Fixed 70 missing sonames in patch 11
- Removed bundled expact, shapelib, minizip, dcmtk
- Force brl build
- Use system shipped FindEXPAT


* Tue Mar 23 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-4%{?dist}
- sed patch to add ${LIB_SUFFIX} to all lib install target
- Added soname version info to vil vil_algo lib

* Sun Mar 21 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-3%{?dist}
- Applied patch to build against newly packaged rply

* Tue Mar 2 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-2%{?dist}
- Applied patch from debian distribution to force the generation of versioned lib

* Fri Feb 19 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-1%{?dist}
- Initial RPM Release

