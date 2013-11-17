Name:           vmtk
Version:        1.0.1
Release:        1%{?dist}
Summary:        The Vascular Modeling Toolkit

License:        BSD
URL:            http://www.%{name}.org/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

### Patch0:         vmtk-0.9.0-use_system_nl.patch

BuildRequires:  vtk-devel 
BuildRequires:  python-devel 
BuildRequires:  cmake 
BuildRequires:  InsightToolkit-devel 
BuildRequires:  OpenNL-devel
BuildRequires:  tcl-devel
BuildRequires:  vxl-devel
BuildRequires:  tk-devel

# Requires vtk-devel for libVPIC.so (BZ#705885)
Requires:       vtk-devel

%description
== Segmentation of vascular segments (or other anatomical structures) from 
medical images:

    Gradient-based 3D level sets segmentation. A new gradient computation
modality based on upwind finite differences allows the segmentation of small
(down to 1.2 pixels/diameter) vessels.
    Interactive level sets initialization based on the Fast Marching Method.
This includes a brand new method for selecting a vascular segment comprised
between two points automatically ignoring side branches, no parameters involved.
Segmenting a complex vascular tract comes down to selecting the endpoints of a
branch, letting level sets by attracted to gradient peaks with the sole
advection term turned on, repeating the operation for all the branches and
merging everything in a single model. 

== Geometric analysis and surface data processing of 3D models of blood vessels
(and tubular objects in general)((The key algorithms have been published on
medical imaging journals. You can find a complete reference to publications at
David Steinman's and Luca Antiga's homepages)):

    Compute centerlines and maximal inscribed sphere radius of branching tubular
structures given their polygonal surface representation
    Split surface models into their constitutive branches based on centerline
geometry
    Compute centerline-based geometric quantities (such as bifurcation angles,
planarity, symmetry, branch curvature, tortuosity) and surface-based geometric
quantities (such as distance to centerlines, surface curvature, deviation from
tangency to maximal inscribed spheres)
    Robustly map branches to a rectangular parametric space
    Generate rectangular patches based on the parametric mapping for statistical
analysis of geometric and CFD data over populations. 

== Scripts, I/O tools and simple algorithms to easily work with 
images and meshes:

    Read and write a number of image, surface and volume mesh formats. Includes
a DICOM series reader with auto-flipping capabilities, Netgen mesh format
reader, libMesh xda mesh format writer, Tetgen mesh generator wrapper, FIDAP
FDNEUT mesh format reader and writer and a Newtetr input file generator
    Display images and meshes
    Incapsulate several VTK classes and make them available as pipeable scripts
(e.g. Marching Cubes, surface smoothing, clipping, normal computation,
connectivity, subdivision, distance between surfaces, ICP registration)
    Add cylindrical extensions to surface model boundaries as a preprocessing
step for CFD simulations.
    Generate boundary layers of prismatic elements with varying thickness for
CFD 

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains headers and libraries required to develop applications
using %{name}.


%prep
%setup -q
### %patch0 -p1
## Remove bundled software
rm -rvf vtkVmtk/Utilities/{Doxygen,OpenNL,Stellar_1.0,tetgen1.4.3}

rm -rvf vtkVmtk/Utilities/OpenNL vtkVmtk/Utilities/Doxygen
sed -i "/Doxygen/d" vtkVmtk/Utilities/CMakeLists.txt
sed -i "/OpenNL/d" vtkVmtk/Utilities/CMakeLists.txt
sed -i "/OpenNL/d" vtkVmtk/Utilities/CMakeLists.txt
sed -i "/Utilities\/OpenNL/d" vtkVmtk/DifferentialGeometry/CMakeLists.txt

find . -name "vtkvmtkITKImageWriter.*" -execdir chmod -v  a-x '{}' \;
find . -name  "vtkvmtkITKArchetypeImageSeriesScalarReader.*" -execdir chmod -v a-x '{}' \;


%build
%cmake -DVTK_VMTK_BUILD_TETGEN:BOOL=OFF \
       -DVMTK_WITH_LIBRARY_VERSION:BOOL=ON \
       -DUSE_EXTERN_OPENNL:BOOL=ON \
       -DUSE_SYSTEM_ITK:BOOL=ON \
       ./

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove shebangs as these should not be executable
find $RPM_BUILD_ROOT/usr/lib/vmtk/vmtk -name "*.py" -perm 644 -execdir sed -i "/#\!\/usr\/bin\/env python/d" '{}' \;

# Install is not multilib compatible
%ifarch x86_64 ppc64
  mv $RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{_libdir}
%endif

# Install python files to the correct location
mkdir -p $RPM_BUILD_ROOT%{python_sitearch}/%{name}
mv $RPM_BUILD_ROOT%{_libdir}/vmtk/vmtk/* $RPM_BUILD_ROOT%{python_sitearch}/vmtk/
rm -rf $RPM_BUILD_ROOT%{_libdir}/vmtk/vmtk


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc Copyright.txt TODO.txt
%{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so.*
%{python_sitearch}/%{name}
%exclude %{python_sitearch}/%{name}/libvtkvmtkCommonPython.so

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}/*.so
%{python_sitearch}/%{name}/libvtkvmtkCommonPython.so


%changelog
* Mon Jan 14 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0.1-1
- Update upstream URL
- Update to latest version

* Thu Jul 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.0-2
- Correct some permissions to remove rpmlint errors

* Sun Jul 10 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.0-1
- initial rpm build
