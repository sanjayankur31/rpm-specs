Name:           OpenImageIO
Version:        0.10.0
Release:        2%{?dist}
Summary:        Library for reading and writing images

Group:          Development/Libraries
License:        BSD
URL:            https://sites.google.com/site/openimageio/home

Source0:        https://download.github.com/%{name}-oiio-Release-%{version}-12-g8055b0f.tar.gz
Patch0:         OpenImageIO-0.10.0-git_backports.patch
Patch1:         OpenImageIO-0.10.0-atomic_test_fix.patch
Patch2:         OpenImageIO-0.10.0-use_system_tbb.patch

BuildRequires:  boost-devel glew-devel qt-devel OpenEXR-devel ilmbase-devel
BuildRequires:  python2-devel txt2man
BuildRequires:  libpng libtiff-devel
BuildRequires:  zlib-devel jasper-devel
BuildRequires:  pugixml-devel
# Field3D support is not considered stable at this time and no package
# currently exists for Fedora. Re-enable when fixed.
#BuildRequires:  hdf5-devel Field3D-devel


%description
OpenImageIO is a library for reading and writing images, and a bunch of related
classes, utilities, and applications. Main features include:
- Extremely simple but powerful ImageInput and ImageOutput APIs for reading and
  writing 2D images that is format agnostic.
- Format plugins for TIFF, JPEG/JFIF, OpenEXR, PNG, HDR/RGBE, Targa, JPEG-2000,
  DPX, Cineon, FITS, BMP, ICO, RMan Zfile, Softimage PIC, DDS, SGI,
  PNM/PPM/PGM/PBM, Field3d.
- An ImageCache class that transparently manages a cache so that it can access
  truly vast amounts of image data.
- A really nice image viewer, iv, also based on OpenImageIO classes (and so 
  will work with any formats for which plugins are available).

%package devel
Summary:        Documentation for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for package %{name}


%prep
%setup -q -n %{name}-oiio-8055b0f
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Remove bundled pugixml
rm -f src/include/pugixml.hpp \
      src/include/pugiconfig.hpp \
      src/libutil/pugixml.cpp \

rm -rf src/include/tbb


%build
mkdir -p build
pushd build
%cmake -DCMAKE_SKIP_RPATH:BOOL=TRUE \
       -DINCLUDE_INSTALL_DIR:PATH=/usr/include/%{name} \
       -DPYLIB_INSTALL_DIR:PATH=%{python_sitearch} \
       -DINSTALL_DOCS:BOOL=OFF \
       -DUSE_EXTERNAL_PUGIXML:BOOL=TRUE \
       -DUSE_TBB:BOOL=OFF \
       ../src

make %{?_smp_mflags}


%install
pushd build
make DESTDIR=%{buildroot} install

# Move man pages to the right directory
mkdir -p %{buildroot}%{_mandir}/man1
cp -a doc/*.1 %{buildroot}%{_mandir}/man1


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE
%{_bindir}/*
%{_libdir}/libOpenImageIO.so.*
%{python_sitearch}/OpenImageIO.so
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc src/doc/*.pdf
%{_libdir}/libOpenImageIO.so
%{_includedir}/*

%changelog
* Mon Jul 18 2011 Richard Shaw <hobbes1069@gmail.com> - 0.10.0-2
- Disabled use of the TBB library.
- Moved headers to named directory.

* Tue Jul 05 2011 Richard Shaw <hobbes1069@gmail.com> - 0.10.0-1
- Inital Release.
