Name:           pcl
Version:        1.6.0
Release:        3%{?dist}
Summary:        Library for point cloud processing

Group:          System Environment/Libraries
License:        BSD
URL:            http://pointclouds.org/
Source0:        http://www.pointclouds.org/assets/files/1.6.0/PCL-1.6.0-Source-patched-ROS.tar.bz2
#Patch0:         PCL-1.4.0-Source-fedora.patch
#Patch1:         pcl-1.5.1-gcc47.patch
#Patch2:         pcl-1.6-rosintegration-v2.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# For plain building
BuildRequires:  cmake, gcc-c++, boost-devel
# Documentation
BuildRequires:  doxygen, graphviz, python-sphinx
%if ! 0%{?rhel} || 0%{?rhel} >= 6
BuildRequires:  texlive-latex
%else
BuildRequires:  tetex-latex
%endif

# mandatory
BuildRequires:  eigen3-devel, flann-devel, cminpack-devel, vtk-devel, gl2ps-devel
# optional
BuildRequires:  qhull-devel, libusb1-devel, gtest-devel qtwebkit-devel
%ifarch %{ix86} x86_64
BuildRequires:  openni-devel
%endif

%description
The Point Cloud Library (or PCL) is a large scale, open project for point
cloud processing.

The PCL framework contains numerous state-of-the art algorithms including
filtering, feature estimation, surface reconstruction, registration, model
fitting and segmentation. 

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       eigen3-devel, qhull-devel, openni-devel, cminpack-devel, flann-devel, vtk-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tools
Summary:        Point cloud tools and viewers
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    tools
This package contains tools for point cloud file processing and viewers
for point cloud files and live Kinect data.


%package        doc
Summary:        PCL API documentation
Group:          Documentation
%if ! 0%{?rhel} || 0%{?rhel} >= 6
BuildArch:      noarch
%endif

%description    doc
The %{name}-doc package contains API documentation for the Point Cloud
Library.


%prep
%setup -q -n PCL-%{version}-Source
#%patch0 -p2 -b .fedora
#%patch2 -p0 -b .rosintegration

# Just to make it obvious we're not using any of these
rm -rf  3rdparty


%build
source /opt/ros/fuerte/setup.sh

mkdir build
pushd build
%cmake \
  -DCMAKE_BUILD_TYPE=NONE \
  -DOPENNI_INCLUDE_DIR:PATH=/usr/include/ni \
  -DLIB_INSTALL_DIR=$(echo %{_libdir} | sed -e 's|%{_prefix}/||') \
  -DPCL_PKGCONFIG_SUFFIX:STRING="" \
  -DBUILD_documentation=ON \
  -DCMAKE_SKIP_RPATH=ON \
  -DUSE_ROS=ON \
  ..

make -j 2
#%{?_smp_mflags}
make doc
popd

pushd doc/overview
make
popd

pushd doc/tutorials
sed -i "s/, 'sphinxcontrib.doxylink.doxylink'//" content/conf.py
make
popd

pushd doc/advanced
make
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Just a dummy test
rm $RPM_BUILD_ROOT%{_bindir}/timed_trigger_test

#mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name} $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}
mv doc/doxygen/html doc/doxygen/api

popd

mv doc/tutorials/html doc/tutorials/tutorials

for f in $RPM_BUILD_ROOT%{_bindir}/{openni_image,pcd_grabber_viewer,pcd_viewer,openni_viewer,oni_viewer}; do
	mv $f $RPM_BUILD_ROOT%{_bindir}/pcl_$(basename $f)
done
rm $RPM_BUILD_ROOT%{_bindir}/{openni_fast_mesh,openni_ii_normal_estimation,openni_voxel_grid}

mkdir -p $RPM_BUILD_ROOT%{_libdir}/cmake/pcl
mv $RPM_BUILD_ROOT%{_datadir}/%{name}-*/*.cmake $RPM_BUILD_ROOT%{_libdir}/cmake/pcl

# Remove installed documentation, will add with doc tags later
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-1.6

#mv $RPM_BUILD_ROOT%{_libdir}/pcl/*.cmake $RPM_BUILD_ROOT%{_libdir}/cmake/pcl
#rmdir $RPM_BUILD_ROOT%{_libdir}/pcl

# This is required to fix crashes in programs linked against pcl_visualization lib
#sed -i -e 's/vtkWidgets/vtkRendering/' $RPM_BUILD_ROOT%{_libdir}/cmake/pcl/PCLDepends-release.cmake

# At the moment fails due to RPATH problem
# (RPATH not built into test apps as required)
#%check
#cd build
#make test

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS.txt LICENSE.txt
%{_libdir}/*.so.*
%{_datadir}/%{name}-1.6

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/pcl

%files tools
%defattr(-,root,root,-)
%{_bindir}/pcl_*
# There are no .desktop files because the GUI tools are rather examples
# to understand a particular feature of PCL.

%files doc
%defattr(-,root,root,-)
%doc build/doc/doxygen/api
%doc doc/tutorials/tutorials


%changelog
* Thu Mar 21 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.6.0-3
- Add ros patch

* Tue Sep 25 2012 Rich Mattes <richmattes@gmail.com> - 1.6.0-2
- Disabled march=native flag in PCLConfig.cmake

* Mon Aug 06 2012 Rich Mattes <richmattes@gmail.com> - 1.6.0-1
- Update to release 1.6.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Rich Mattes <richmattes@gmail.com> - 1.5.1-3
- Rebuild for new vtk

* Thu Apr 19 2012 Tim Niemueller <tim@niemueller.de> - 1.5.1-2
- Pass proper LIB_INSTALL_DIR, install wrong cmake files otherwise

* Mon Apr 04 2012 Rich Mattes <richmattes@gmail.com> - 1.5.1-1
- Update to release 1.5.1
- Add new patch for gcc-4.7 fixes

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Rich Mattes <richmattes@gmail.com> - 1.4.0-1
- Update to release 1.4.0
- Add patch for gcc-4.7 fixes

* Mon Jan 16 2012 Tim Niemueller <tim@niemueller.de> - 1.3.1-5
- Update patch to fix PCLConfig.cmake

* Sat Jan 14 2012 Rich Mattes <richmattes@gmail.com> - 1.3.1-4
- Rebuild for gcc-4.7 and flann-1.7.1

* Sun Jan 08 2012 Dan Horák <dan[at]danny.cz> - 1.3.1-3
- openni is exclusive for x86

* Fri Dec 23 2011 Tim Niemueller <tim@niemueller.de> - 1.3.1-2
- Make sure documentation is not in main package

* Sat Dec 04 2011 Tim Niemueller <tim@niemueller.de> - 1.3.1-1
- Update to 1.3.1

* Tue Nov 22 2011 Tim Niemueller <tim@niemueller.de> - 1.3.0-1
- Update to 1.3.0

* Tue Oct 22 2011 Tim Niemueller <tim@niemueller.de> - 1.2.0-1
- Update to 1.2.0

* Tue Oct 04 2011 Tim Niemueller <tim@niemueller.de> - 1.1.1-2
- Change vtkWidgets to vtkRendering as import library flags to fix crash
  for binaries compiled with the installed PCL

* Tue Sep 20 2011 Tim Niemueller <tim@niemueller.de> - 1.1.1-1
- Update to 1.1.1

* Wed Jul 27 2011 Tim Niemueller <tim@niemueller.de> - 1.1.0-1
- Update to 1.1.0

* Wed Apr 06 2011 Tim Niemueller <tim@niemueller.de> - 1.0.0-0.1.svn366
- Initial package

