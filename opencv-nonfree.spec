%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%global tar_name OpenCV
%global indice   a

%global proj_name   opencv
Name:           %{proj_name}-nonfree
Version:        2.4.4
Release:        3%{?dist}
Summary:        Nonfree portions of OpenCV

Group:          Development/Libraries
# This is normal three clause BSD.
License:        BSD
URL:            http://opencv.willowgarage.com/wiki/
Source0:        http://downloads.sourceforge.net/opencvlibrary/%{tar_name}-%{version}%{?indice}.tar.bz2
Source1:        opencv-samples-Makefile
Patch0:         opencv-pkgcmake.patch
Patch1:         opencv-pkgcmake2.patch
#http://code.opencv.org/issues/2720
Patch2:         OpenCV-2.4.4-pillow.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool
BuildRequires:  cmake >= 2.6.3
BuildRequires:  chrpath

#BuildRequires:  eigen2-devel}
BuildRequires:  eigen3-devel
BuildRequires:  gtk2-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
%if 0%{?fedora} >= 1
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
BuildRequires:  libdc1394-devel
%endif
%endif
BuildRequires:  jasper-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libv4l-devel
BuildRequires:  OpenEXR-devel
%ifarch %{ix86} x86_64
BuildRequires:  openni-devel
BuildRequires:  openni-primesense
%endif
%ifarch %{ix86} x86_64 ia64 ppc ppc64
BuildRequires:  tbb-devel
%endif
BuildRequires:  zlib-devel, pkgconfig
BuildRequires:  python-devel
BuildRequires:  numpy, swig >= 1.3.24
BuildRequires:  python-sphinx
BuildRequires:  ffmpeg-devel >= 0.4.9
BuildRequires:  gstreamer-devel gstreamer-plugins-base-devel
BuildRequires:  xine-lib-devel

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.

This package contains the nonfree libraries of opencv


%package devel
Summary:        Nonfree devel portions of %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the nonfree devel libraries of opencv

%prep
%setup -q -n %{proj_name}-%{version}
%patch0 -p1 -b .pkgcmake
%patch1 -p1 -b .pkgcmake2
%patch2 -p1 -b .pillow

# fix dos end of lines
sed -i 's|\r||g'  samples/c/adaptiveskindetector.cpp


%build
mkdir -p build
pushd build
%cmake CMAKE_VERBOSE=1 \
 -DPYTHON_PACKAGES_PATH=%{python_sitearch} \
 -DCMAKE_SKIP_RPATH=ON \
%ifnarch x86_64 ia64
 -DENABLE_SSE=0 \
 -DENABLE_SSE2=0 \
%endif
 %{!?_with_sse3:-DENABLE_SSE3=0} \
 -DCMAKE_BUILD_TYPE=ReleaseWithDebInfo \
 -DBUILD_TEST=1 \
 -DBUILD_opencv_java=0 \
%ifarch %{ix86} x86_64 ia64
 -DWITH_TBB=1 -DTBB_LIB_DIR=%{_libdir} \
%endif
 -DWITH_GSTREAMER=1 \
 -DWITH_FFMPEG=1 \
 -DBUILD_opencv_nonfree=1 \
 -DBUILD_opencv_gpu=1 \
 -DCUDA_TOOLKIT_ROOT_DIR=%{?_cuda_topdir} \
 -DCUDA_VERBOSE_BUILD=1 \
 -DCUDA_PROPAGATE_HOST_FLAGS=0 \
%ifarch %{ix86} x86_64
 -DWITH_OPENNI=ON \
%endif
 -DWITH_XINE=1 \
 -DINSTALL_C_EXAMPLES=1 \
 -DINSTALL_PYTHON_EXAMPLES=1 \
 ..

make VERBOSE=1 %{?_smp_mflags}

popd


%install
rm -rf $RPM_BUILD_ROOT  __devel-doc
pushd build
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" CPPROG="cp -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


rm -f $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/build_all.sh \
      $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/cvsample.dsp \
      $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/cvsample.vcproj \
      $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/facedetect.cmd
install -pm644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/OpenCV/samples/c/GNUmakefile

# remove unnecessary documentation
rm -rf $RPM_BUILD_ROOT%{_datadir}/OpenCV/doc

popd

#Cmake mess
mkdir -p  $RPM_BUILD_ROOT%{_libdir}/cmake/OpenCV
mv $RPM_BUILD_ROOT%{_datadir}/OpenCV/*.cmake \
  $RPM_BUILD_ROOT%{_libdir}/cmake/OpenCV

# remove the non non free parts
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_calib3d.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_contrib.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_core.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_features2d.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_flann.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_highgui.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_imgproc.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_legacy.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_ml.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_objdetect.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_photo.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_stitching.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_ts.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_video.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_videostab.so*
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/libopencv_gpu.so*

# remove headers
rm -rvf $RPM_BUILD_ROOT/%{_includedir}/opencv
rm -rvf $RPM_BUILD_ROOT/%{_includedir}/opencv2

# remove cmake
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/cmake/OpenCV

# remove samples etc
rm -rvf $RPM_BUILD_ROOT/%{_datadir}/OpenCV
rm -rvf $RPM_BUILD_ROOT/%{_datadir}/opencv

# remove binaries
rm -rvf $RPM_BUILD_ROOT/%{_bindir}/opencv*

# remove python stuff
rm -rvf $RPM_BUILD_ROOT/%{python_sitearch}/cv*

# remove packageconfig
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/

%check
# Check fails since we don't support most video
# read/write capability and we don't provide a display
# ARGS=-V increases output verbosity
# Make test is unavailble as of 2.3.1
%if 0
#ifnarch ppc64
pushd build
    LD_LIBRARY_PATH=%{_builddir}/%{tar_name}-%{version}/lib:$LD_LIBARY_PATH make test ARGS=-V || :
popd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/libopencv_nonfree.so.*

%files devel
%{_libdir}/libopencv_nonfree.so

%changelog
* Thu May 09 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 2.4.4-3
- Initial rpm build
