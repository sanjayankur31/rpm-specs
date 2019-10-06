%global commit 5987de50801d1ce3dedc91307d478594459662d6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global checkout_timestamp  20191005

Name:           cork
Version:        0
Release:        0.1.%{checkout_timestamp}git%{shortcommit}%{?dist}
Summary:        3D Boolean / CSG Library

License:        LGPLv3+ with exceptions
URL:            https://github.com/gilbo/cork
Source0:        https://github.com/gilbo/cork/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:         0001-increase-mesh-data-output-precision-to-avoid-error-i.patch
Patch1:         0002-support-first-and-second-flags-where-first-A-U-A-B-s.patch
Patch2:         0003-allow-users-to-seed-the-RNG-with-a-negative-input-as.patch
Patch3:         0004-use-gcc-g-instead-of-clang.patch
Patch4:         0005-Tweak-makefile-for-fedora.patch


BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  gmp-devel

%description
Surprisingly, most Boolean/CSG libraries available today (early 2013) are not
robust to numerical errors. Floating-point errors often lead to segmentation
faults or produce grossly inaccurate results (e.g. nothing) despite the code
being provided . The few libraries which are robust (e.g. CGAL) require the
user to correctly configure the arithmetic settings to ensure robustness.

Cork is designed with the philosophy that you, the user, don't know and don't
care about esoteric problems with floating point arithmetic. You just want a
Boolean library with a simple interface, that you can rely on... Unfortunately
since Cork is still in ongoing development, this may be more or less true at
the moment. This code should be very usable for a research project, perhaps
slightly less so for use in a product.

Cork was developed by Gilbert Bernstein, a computer scientist who has worked on
robust geometric intersections in various projects since 2007. He's reasonably
confident he knows what he's doing. =D

%package devel
Summary:    Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.


%prep
%autosetup -n %{name}-%{commit} -S git


%build
%{set_build_flags}
%make_build


%install
# Makefile doesn't have an install command, so we do it ourself
install -m 755 -d $RPM_BUILD_ROOT/%{_bindir}/
install -m 755 -t $RPM_BUILD_ROOT/%{_bindir}/ bin/cork
install -m 755 -t $RPM_BUILD_ROOT/%{_bindir}/ bin/off2obj

install -m 755 -d $RPM_BUILD_ROOT/%{_includedir}/
install -m 644 -t $RPM_BUILD_ROOT/%{_includedir}/ include/cork.h

install -m 755 -d $RPM_BUILD_ROOT/%{_libdir}/
install -m 755 -t $RPM_BUILD_ROOT/%{_libdir}/ libcork.so.0.0.0
pushd $RPM_BUILD_ROOT/%{_libdir} || exit -1
    ln -s libcork.so.0.0.0 libcork.so
popd || exit -1

%files
%license COPYRIGHT
%doc README.md
%{_libdir}/libcork.so.0.0.0
%{_libdir}/libcork.so.0
%{_bindir}/{cork,off2obj}

%files devel
%{_includedir}/%{name}.h
%{_libdir}/libcork.so


%changelog
* Sat Oct 05 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1.20191005git5987de5
- Initial package
