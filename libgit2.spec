%global commit 43cb8b32428b1b29994874349ec22eb5372e152c

Name: libgit2
Version: 0.20.0
Release: 1%{?dist}
Summary: A C implementation of the Git core methods as a library

License: GPLv2 with exceptions
URL: http://libgit2.github.com/
Source0: https://github.com/%{name}/%{name}/archive/%{commit}/%{name}-%{version}.tar.gz

# Use system libxdiff
Patch0: libgit2-0.20.0-system-libxdiff.patch

# Add htonl() and friends declarations on non-x86 arches
Patch1: libgit2-0.19.0-non-x86.patch

BuildRequires: cmake >= 2.6
BuildRequires: http-parser-devel
BuildRequires: libxdiff-devel
BuildRequires: openssl-devel
BuildRequires: python
BuildRequires: zlib-devel

%description
libgit2 is a portable, pure C implementation of the Git core methods 
provided as a re-entrant linkable library with a solid API, allowing
you to write native speed custom Git applications in any language
with bindings.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
# Remove VCS files from examples
find examples -name ".gitignore" -delete

# Apply patches
%patch0 -p1 -b .system-libxdiff
%patch1 -p1 -b .non-x86

# Fix pkgconfig generation
sed -i 's|@CMAKE_INSTALL_PREFIX@/||' libgit2.pc.in

# Don't test network
sed -i 's/ionline/xonline/' CMakeLists.txt

# Remove bundled libraries
rm -rf deps
rm -rf src/xdiff


%build
%cmake .
make %{_smp_mflags}


%check
ctest -V


%install
make install DESTDIR=%{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc README.md COPYING AUTHORS
%{_libdir}/libgit2.so.*


%files devel
%doc docs examples
%{_libdir}/libgit2.so
%{_libdir}/pkgconfig/libgit2.pc
%{_includedir}/git2*


%changelog
* Sun Nov 24 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 0.20.0-1
- 0.20.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 25 2013 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.19.0-1
- 0.19.0

* Wed Jun 19 2013 Dan Horák <dan[at]danny.cz> - 0.18.0-5
- Add htonl() and friends declarations on non-x86 arches
- Rebuilt with fixed libxdiff for big endian arches

* Thu May 30 2013 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.18.0-4
- Update the http-parser patch
- Skip tests that require network connectivity

* Thu May 30 2013 Tom Callaway <spot@fedoraproject.org> - 0.18.0-3
- use system libxdiff instead of bundled copy

* Fri May 24 2013 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.18.0-2
- Remove unnecessary CMake build flags
- Fix the pkgconfig file

* Thu May 02 2013 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.18.0-1
- Update to version 0.18.0
- Unbundle the http-parser library

* Fri Oct 19 2012 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.17.0-2
- Use make for building and installation
- Specify minimum CMake version
- Remove useless OpenSSL build dependency
- Move development documentation to the -devel package
- Add code examples to the -devel package

* Thu Oct 18 2012 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.17.0-1
- Initial package.
