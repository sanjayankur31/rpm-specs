# NOTE: The Patch2 source file and some of the cmake flags are copied from http://packages.debian.org/source/squeeze/vxl

Name:		vxl	
Version:	1.14.0	
Release:	1%{?dist}
Summary:	C++ Libraries for Computer Vision Research and Implementation
Group:		Development/Libraries
License:	BSD
URL:		http://vxl.sourceforge.net/
Source0:	http://sourceforge.net/projects/vxl/files/vxl/1.14/vxl-1.14.0.zip
Source2:	https://vxl.svn.sourceforge.net/svnroot/vxl/trunk/core/vxl_copyright.h
Patch1:		0001-Added-include-path-for-geotiff.patch
Patch2:		0002-Added-soname-info-for-core-libraries.patch
Patch3:		0003-Use-system-rply.patch
Patch4:		0004-Added-more-soname.patch
Patch5:		0005-Do-not-build-OUL.patch
Patch6:		0006-BUG-rplyConfig.cmake-has-wrong-include-path.patch
Patch7:		0007-Arguments-of-ply_open-and-create-changed.-Thanks-to-.patch
Patch8:		0008-Install-vpgl-as-some-libraries-need-it.-Thanks-to-Th.patch
Patch9:		0009-Reverted-an-incompatible-API-changes-which-breaks-IT.patch
Patch10:	0010-Do-not-include-doxygen.cmake-in-UseVXL.patch
Patch11:	0011-More-sonames.patch
Patch12:	0012-Bumped-up-version-to-1.14.patch
Patch13:	0013-Use-system-FindEXPAT.patch
Patch14:	0014-Do-not-use-bundled-minizip.patch
Patch15:	0015-Install-more-targets.patch

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake >= 2.6.3
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libgeotiff-devel
BuildRequires:	texi2html
BuildRequires:	rply-devel
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	shapelib-devel
BuildRequires:	minizip-devel
BuildRequires:	dcmtk-devel

%description
VXL (the Vision-something-Libraries) is a collection of C++ libraries designed
for computer vision research and implementation. It was created from TargetJr
and the IUE with the aim of making a light, fast and consistent system. 
VXL is written in ANSI/ISO C++ and is designed to be portable over many
platforms.


%prep
%setup -q

cp %{SOURCE2} .

#Remove bundled library (let's use FEDORA's ones)
for l in jpeg png zlib tiff geotiff mpeg2 rply dcmtk
do
	find v3p/$l -type f ! -name 'CMakeLists.txt' -execdir rm {} +
done

find contrib/brl/b3p/shapelib -type f ! -name 'CMakeLists.txt' -execdir rm {} +
find contrib/brl/b3p/minizip -type f ! -name 'CMakeLists.txt' -execdir rm {} +

# v3p/mpeg2 lib in fedora is not enough to build the target. Moreover it is in rpmfusion repo
# v3p/netlib dependency not removed because of heavily modifications


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
	-DBUILD_OXL:BOOL=ON \
	-DBUILD_BRL=ON \
	-DBUILD_CORE_GEOMETRY:BOOL=ON \
	-DBUILD_CORE_IMAGING:BOOL=ON \
	-DBUILD_CORE_NUMERICS:BOOL=ON \
	-DBUILD_CORE_PROBABILITY:BOOL=OFF \
	-DBUILD_CORE_SERIALISATION:BOOL=ON \
	-DBUILD_CORE_UTILITIES:BOOL=ON \
	-DBUILD_CORE_VIDEO:BOOL=ON \
	-DBUILD_EXAMPLES:BOOL=OFF \
	-DBUILD_TESTING:BOOL=OFF \
	-DBUILD_DOCUMENTATION:BOOL=ON \
	-DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo" .

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#mkdir -p "${RPM_BUILD_ROOT}%{_docdir}/%{name}/"
#cp -r doc/* "${RPM_BUILD_ROOT}%{_docdir}/%{name}/"

%clean
rm -rf $RPM_BUILD_ROOT

%check
ctest .

%files
%defattr(-,root,root,-)
%doc vxl_copyright.h
%{_libdir}/*.so.*
%{_bindir}/*
%{_datadir}/%{name}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%package	doc
Summary:	Documentation for VXL library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description doc

You should install this package if you would like to
have all the documentation

%files doc
%defattr(-,root,root)
%doc %{_docdir}/*

%package	devel
Summary:	Headers for VXL library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel

You should install this package if you would like to
develop code based on VXL.

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}/
%{_includedir}/%{name}/*
%{_libdir}/*.so

%changelog
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

* Sat Feb 19 2010 Mario Ceresa mrceresa fedoraproject org vxl 1.13.0-1%{?dist}
- Initial RPM Release

