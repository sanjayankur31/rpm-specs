Name:           libccd
Version:        1.3
Release:        3%{?dist}
Summary:        Library for collision detection between convex shapes

License:        BSD
URL:            http://libccd.danfis.cz
Source0:        http://libccd.danfis.cz/files/%{name}-%{version}.tar.gz
# This patch integrates all of the test programs that are present in
# the testsuites folder into CMake, via CTest.  Not yet submitted
# upstream
Patch0:         %{name}-1.3-ctest.patch
# This patch changes the ccd.pc file to point to the correct include
# directory.  Not yet submitted upstream
Patch1:         %{name}-1.3-fixpkgconfig.patch


BuildRequires:  cmake
# These are required for executing the test suite
BuildRequires:  python
BuildRequires:  valgrind

%description
libccd implements variation on Gilbert-Johnson-Keerthi (GJK) algorithm + 
Expand Polytope Algorithm (EPA). It also implements Minkowski Portal 
Refinement (MPR, a.k.a. XenoCollide) algorithm as published in Game 
Programming Gems 7.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
# Use the correct upstream version
sed -i 's|\"1.2\")|\"1.3\")|' CMakeLists.txt

%build
mkdir build
pushd build
%cmake -DBUILD_TESTS=ON -DCMAKE_BUILD_TYPE=None ..
popd
make -C build %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make -C build install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%check
make -C build test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc BSD-LICENSE README
%{_libdir}/*.so.*

%files devel
%doc doc/jgt98convex.pdf
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue May 29 2012 Rich Mattes <richmattes@gmail.com> - 1.3-3
- Fixed pkgconfig file to point to correct include dir

* Sat May 26 2012 Rich Mattes <richmattes@gmail.com> - 1.3-2
- Convert test suite to CTest

* Fri May 25 2012 Rich Mattes <richmattes@gmail.com> - 1.3-1
- Update to release 1.3
- Remove upstreamed soname patch

* Sun May 06 2012 Rich Mattes <richmattes@gmail.com> - 1.2-3
- Removed -static subpackage.

* Mon Apr 30 2012 Rich Mattes <richmattes@gmail.com> - 1.2-2
- Update soname patch to match upstream implementation 

* Fri Apr 27 2012 Rich Mattes <richmattes@gmail.com> - 1.2-1
- Initial package
