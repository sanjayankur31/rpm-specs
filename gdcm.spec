# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:		gdcm
Version:	2.0.17
Release:	4%{?dist}
Summary:	Grassroots DiCoM is a C++ library to parse DICOM medical files
Group:		Development/Libraries
License:	BSD
URL:		http://sourceforge.net/apps/mediawiki/gdcm/index.php?title=Main_Page
Source0:	http://sourceforge.net/projects/gdcm/files/gdcm%202.x/GDCM%202.0.17/gdcm-2.0.17.tar.bz2
#Source1:	http://downloads.sourceforge.net/project/gdcm/gdcmData/gdcmData/gdcmData.tar.bz2
Source2:	FindCharLS.cmake
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# There is a bug in doxygen preventing compilation on:
ExcludeArch:	ppc ppc64

Patch1: gdcm-2.0.14-inplacebuild.patch
Patch2:	gdcm-2.0.14-usecopyright.patch
Patch3: gdcm-2.0.16-fix_ptrdiff.patch
Patch4: gdcm-2.0.16-fix-decode.patch
Patch5: gdcm-2.0.16-JlsParameters.patch
Patch6: gdcm-2.0.17-install2libarch.patch
Patch7: gdcm-2.0.17-use_openjpeg_1x.patch
Patch8: gdcm-2.0.17-use_system_charls
Patch9: gdcm-2.0.16-remove-stdafx.patch
Patch10: gdcm-2.0.17-no_versioned_dir.patch

BuildRequires:	cmake >= 2.6.0
BuildRequires:	openssl-devel
BuildRequires:	libuuid-devel
BuildRequires:	expat-devel
BuildRequires:	openjpeg-devel
BuildRequires:	poppler-devel
BuildRequires:	mesa-libOSMesa-devel
BuildRequires:	fontconfig-devel
BuildRequires:	doxygen
BuildRequires:	CharLS-devel >= 1.0
BuildRequires:	texlive-latex
BuildRequires:	graphviz
BuildRequires:	python2-devel
BuildRequires:	swig
BuildRequires:	vtk-devel
BuildRequires:	postgresql-devel
BuildRequires:	mysql-devel
BuildRequires:	libogg-devel
BuildRequires:	libtheora-devel
BuildRequires:	gl2ps-devel
BuildRequires:	mysql-libs


%description
GDCM implements the dicom base standard part 5 that concentrates on image file
format. Hence GDCM supports the following formats:
- ACR-NEMA version 1 and 2 (huffman compression is not supported),
- DICOM version 3.0, including various encodings of JPEG - lossless & lossy-, 
RLE, J2K, deflated, JPEG-LS (very experimental) (MPEG2 compression is not 
supported)
- Papyrus V2 and V3 file headers should be readable, 

%package	devel
Summary:	Libraries and headers for GDCM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel

You should install the gdcm-devel package if you would like to
compile applications based on gdcm

%package	python
Summary:	Python binding for GDCM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description python

You should install the gdcm-python package if you would like to
used this library with python



%prep
%setup -q
%patch1
%patch2
%patch3 -p 2
%patch4 -p 1
%patch5 -p 1
%patch6 -p 1
%patch7 -p 1
%patch8 -p 1
%patch9 -p 1
%patch10 -p 1

# Remove bundled utilities (we use Fedora's ones)

rm -rf Utilities/gdcmexpat
rm -rf Utilities/gdcmopenjpeg
rm -rf Utilities/gdcmzlib
rm -rf Utilities/gdcmuuid
rm -rf Utilities/gdcmcharls

# Remove bundled utilities (we don't use them)
rm -rf Utilities/gdcmmd5
rm -rf Utilities/getopt
rm -rf Utilities/pvrg
rm -rf Utilities/rle
rm -rf Utilities/wxWidgets

cp %{SOURCE2} CMake/

%build
%cmake	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DCMAKE_SKIP_RPATH:BOOL=YES \
	-DGDCM_BUILD_TESTING=OFF \
	-DGDCM_BUILD_EXAMPLES:BOOL=ON \
	-DGDCM_DOCUMENTATION:BOOL=ON \
	-DGDCM_PDF_DOCUMENTATION:BOOL=ON \
	-DGDCM_WRAP_PYTHON:BOOL=ON \
	-DGDCM_WRAP_JAVA=OFF \
	-DGDCM_BUILD_SHARED_LIBS:BOOL=ON \
	-DGDCM_BUILD_APPLICATIONS:BOOL=ON \
	-DCMAKE_BUILD_TYPE:STRING="Release" \
	-DGDCM_USE_VTK:BOOL=ON \
	-DGDCM_USE_SYSTEM_EXPAT=ON \
	-DGDCM_USE_SYSTEM_OPENJPEG=ON \
	-DGDCM_USE_SYSTEM_ZLIB=ON \
	-DGDCM_USE_SYSTEM_UUID=ON \
	-DGDCM_USE_SYSTEM_LJPEG=OFF \
	-DGDCM_USE_SYSTEM_OPENSSL=ON \
	-DGDCM_USE_JPEGLS=ON \
	-DGDCM_USE_SYSTEM_JPEGLS=ON \
	-DGDCM_USE_SYSTEM_POPPLER=ON . 

#Cannot build wrap_java:	
#	-DGDCM_VTK_JAVA_JAR:PATH=/usr/share/java/vtk.jar no found! 
#	yum provides */vtk.jar -> No results found

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{python_sitelib}/
mv $RPM_BUILD_ROOT%{_libdir}/gdcm.py $RPM_BUILD_ROOT%{python_sitelib}/
mv $RPM_BUILD_ROOT%{_libdir}/gdcmswig.py $RPM_BUILD_ROOT%{python_sitelib}/
mv $RPM_BUILD_ROOT%{_libdir}/_gdcmswig.so $RPM_BUILD_ROOT%{python_sitelib}/
mv $RPM_BUILD_ROOT%{_libdir}/vtkgdcm.py $RPM_BUILD_ROOT%{python_sitelib}/

## Rearranging directory layout and removing version from dir
mv $RPM_BUILD_ROOT%{_libdir}/gdcm/*.cmake $RPM_BUILD_ROOT%{_datadir}/gdcm/
rmdir $RPM_BUILD_ROOT%{_libdir}/gdcm

## Cleaning Example dir from cmake cache files + remove 0-lenght files
find %{_builddir}/%{?buildsubdir}/Examples -depth -name CMakeFiles | xargs rm -rf
find %{_builddir}/%{?buildsubdir}/Examples -depth -size 0 | xargs rm -rf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc %{_mandir}/man1/*.1*
%doc AUTHORS Copyright.txt README.Copyright.txt README.txt
%dir %{_datadir}/gdcm/
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/gdcm/XML

%check
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/bin
ctest .

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files devel
%defattr(-,root,root)
%dir %{_includedir}/gdcm/
%doc Examples
%{_includedir}/gdcm/*
%{_libdir}/*.so
%{_datadir}/gdcm/*.cmake

%files python
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 2.0.17-4
- Rebuild (poppler-0.17.0)

* Wed Apr 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> - 2.0.17-3
- Bump release

* Sun Mar 27 2011 Mario Ceresa mrceresa gmailcom - 2.0.17-2
- Fixed BR mysql-libs

* Sat Mar 19 2011 Mario Ceresa mrceresa gmailcom - 2.0.17-1
- Updated to version 2.0.17

* Thu Mar 17 2011 Marek Kasik <mkasik@redhat.com> - 2.0.16-17
- Fix BuildRequires

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 2.0.16-16
- Rebuild (poppler-0.16.3)

* Sun Feb 20 2011 Orion Poplawski <orion@cora.nwra.com> - 2.0.16-15
- Rebuild for new vtk with fixed sonames

* Mon Feb 14 2011 Mario Ceresa <mrceresa@gmail.com> - 2.0.16-13
- Adapted to new version of CharLS lib (v 1.0)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 02 2011 Mario Ceresa <mrceresa@gmail.com> - 2.0.16-11
- Removed python bindings because they fail to build with gcc 4.6

* Mon Feb 02 2011 Mario Ceresa <mrceresa@gmail.com> - 2.0.16-10
- Added patch to fix upstream bug #3169784

* Sun Jan 02 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.0.16-11
- rebuild (poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.0.16-8
- rebuild (poppler)

* Mon Nov 22 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-7
- Fixed bug 655738

* Tue Nov 19 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-6
- Enabled VTK support

* Tue Oct 19 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-5
- Filtered out private python extension lib
- Added documentation

* Tue Oct 19 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-4
- Changed directory ownership

* Fri Oct 15 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-3
- Rearranged directory layout to remove version in dir names

* Sat Sep 18 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-2
- Added ExcludeArch for ppc and ppc64 because of a bug in doxygen
see https://bugzilla.redhat.com/show_bug.cgi?id=566725#c9

* Sat Sep 18 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.16-1
- Updated to release 2.0.16
- Removed patch "stack_namespace" and "poppler_breaks_api" because
already included upstream
- Added swig and texlive-pdflatex to BuildRequires
- Moved python files to a separate package

* Sun Apr 11 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14-5
- Fixed some issues pointed out by Martin Gieseking. In details:
- BR to build documentation (tex + graphviz)
- Changed man page inclusion
- Fixed changelog format
- Removed VTK support because cmake 2.8 is needed to recognize vtk 5.4!
- Fixed python support

* Thu Mar 25 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14-4
- Added VTK support
- Added python support

* Mon Mar 21 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14-3
- Added BuildRequires fontconfig-devel
- Fixed lib /lib64 issue with base CMakeLists.txt

* Mon Mar 15 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14-2
- Added BuildRequires CharLS-devel

* Wed Feb 17 2010 Mario Ceresa <mrceresa@gmail.com> 2.0.14
- Initial RPM Release

