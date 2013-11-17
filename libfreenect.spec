%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

Name:           libfreenect
Version:        0.1.2
Release:        2%{?dist}
Summary:        Device driver for the Kinect
License:        GPLv2+ or ASL 2.0
URL:            http://www.openkinect.org/

# No official releases, yet. To reproduce tarball use freenect_generate_tarball.sh:
# Usage: freenect_generate_tarball.sh [GIT TAG]
Source0:        libfreenect-v%{version}.tar.bz2
Source1:        freenect_generate_tarball.sh

BuildRequires:  cmake
BuildRequires:  Cython
BuildRequires:  doxygen
BuildRequires:  freeglut-devel
BuildRequires:  libusb1-devel
BuildRequires:  libGL-devel
BuildRequires:  libXi-devel
BuildRequires:  libXmu-devel
BuildRequires:  numpy
BuildRequires:  opencv-devel
BuildRequires:  python-devel

Requires:       udev

%description
libfreenect is a free and open source library that provides access to the
Kinect device.  Currently, the library supports the RGB webcam, the depth
image, the LED, and the tilt motor.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        static
Summary:        Development files for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    static
The %{name}-static package contains static libraries for
developing applications that use %{name}.

%package        fakenect
Summary:        Library to play back recorded data for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    fakenect
Fakenect consists of a "record" program to save dumps from the kinect sensor 
and a library that can be linked to, providing an interface compatible with 
freenect.  This allows you to save data and repeat for experiments, debug 
problems, share datasets, and experiment with the kinect without having one.

%package        opencv
Summary:        OpenCV bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    opencv
The %{name}-opencv package contains the libfreenect binding
library for OpenCV development.

%package        python
Summary:        Python bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    python
The %{name}-python package contains python bindings for %{name}

%prep
%setup -q -n %{name}
# Get rid of osx and win specific stuff
sed -i 's|get_python_lib(prefix='\''${CMAKE_INSTALL_PREFIX}'\'')|get_python_lib(1)|' wrappers/python/CMakeLists.txt
sed -i 's|/usr/local|/usr|' wrappers/python/setup.py
chmod -x wrappers/cpp/cppview.cpp
sed -i 's|set(CMAKE_C_FLAGS "-Wall")|#set(CMAKE_C_FLAGS "-Wall")|' src/CMakeLists.txt
sed -i 's|set(CMAKE_C_FLAGS "-Wall")|#set(CMAKE_C_FLAGS "-Wall")|' examples/CMakeLists.txt

%build
mkdir build
pushd build
%cmake -DBUILD_AUDIO=ON -DBUILD-CPP=ON -DBUILD_C_SYNC=ON -DBUILD_CV=ON -DBUILD_REDIST_PACKAGE=ON -DBUILD_EXAMPLES=ON -DBUILD_CPACK=OFF -DBUILD_FAKENECT=ON -DBUILD_PYTHON=ON ..
make %{?_smp_mflags} VERBOSE=1
popd

pushd doc
doxygen Doxyfile
popd

%install
rm -rf %{buildroot}
make -C build install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/lib/udev/rules.d
install -p -m 0644 platform/linux/udev/51-kinect.rules %{buildroot}/lib/udev/rules.d
find %{buildroot} -name '*.la' -exec rm -f {} ';'
mv %{buildroot}%{_includedir}/libfreenect.hpp %{buildroot}%{_includedir}/libfreenect/libfreenect.hpp
# These binaries have very vague names.  Renaming them to freenect-* to clarify 
for f in %{buildroot}%{_bindir}/*; do
    mv $f %{buildroot}%{_bindir}/freenect-$(basename $f)
done
mv %{buildroot}%{_bindir}/freenect-fakenect %{buildroot}%{_bindir}/fakenect

mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{_datadir}/fwfetcher.py   %{buildroot}%{_datadir}/%{name}
# Get rid of the hashbang in the fwfetcher song
sed -i "s|#!/usr/bin/env python||" %{buildroot}%{_datadir}/%{name}/fwfetcher.py

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post opencv -p /sbin/ldconfig

%postun opencv -p /sbin/ldconfig

%files
%doc APACHE20 GPL2 README.asciidoc CONTRIB
/lib/udev/rules.d/*
%{_libdir}/libfreenect.so.*
%{_libdir}/libfreenect_sync.so.*
%exclude %{_bindir}/freenect-cvdemo
%exclude %{_bindir}/fakenect
%{_bindir}/freenect-*
%{_datadir}/%{name}

%files opencv
%{_bindir}/freenect-cvdemo
%{_libdir}/libfreenect_cv.so.*

%files devel
%doc doc/html
%doc examples/*.c wrappers/cpp/cppview.cpp
%{_includedir}/libfreenect
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/fakenect/*.so

%files static
%{_libdir}/*.a

%files python
%{python_sitearch}/*.so

%files fakenect
%dir %{_libdir}/fakenect
%{_libdir}/fakenect/*.so.*
%{_bindir}/fakenect

%changelog
* Wed Aug 15 2012 Rich Mattes <richmattes@gmail.com> - 0.1.2-2
- Filtered private python lib provides
- Clarified that freenect_generate_tarball.sh works with a git tag

* Thu Apr 26 2012 Rich Mattes <richmattes@gmail.com> - 0.1.2-1
- Update to git tag 0.1.2
- Create OpenCV wrapper sub-package
- Create fakenect library sub-package

* Tue Mar 24 2011 Rich Mattes <richmattes@gmail.com> - 0-0.3.4a159fgit
- Force cmake to honor rpm optflags
- Change to out-of-tree build

* Tue Mar 24 2011 Rich Mattes <richmattes@gmail.com> - 0-0.2.4a159fgit
- Update to latest snapshot

* Mon Jan 31 2011 Rich Mattes <richmattes@gmail.com> - 0-0.1.687b2da5git
- Initial package

