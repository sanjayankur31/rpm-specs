%global soname libopennl.so

Name:           OpenNL
Version:        3.2.1
Release:        5%{?dist}
Summary:        A library for solving sparse linear systems

License:        BSD
URL:            http://alice.loria.fr/index.php/software/4-library/23-opennl.html
Source0:        https://gforge.inria.fr/frs/download.php/27459/OpenNL3.2.zip

# Changes the soname from libnl.so to libopennl.so
Patch0:         OpenNL-3.2.1-library_soname.patch

BuildRequires:  cmake


%description
OpenNL (Open Numerical Library) is a library for solving sparse linear systems,
especially designed for the Computer Graphics community. The goal for OpenNL is
to be as small as possible, while offering the subset of functionalities
required by this application field. The Makefiles of OpenNL can generate a
single .c + .h file, very easy to integrate in other projects. The distribution
includes an implementation of our Least Squares Conformal Maps parameterization
method.

New version: OpenNL 3.2.1, includes support for CUDA and Fermi architecture
(Concurrent Number Cruncher and Nathan Bell's ELL formats)


OpenNL offers the following set of functionalities:

    Efficient sparse matrix data structure (for non-symmetric and symmetric
matrices)
    Iterative builder for sparse linear system
    Iterative builder for sparse least-squares problems
    Iterative solvers: conjugate gradient, BICGStab, GMRES
    Preconditionners: Jacobi, SSOR
    Iterative solver on the GPU (Concurrent Number Cruncher and Nathan Bell's
ELL)
    Sparse direct solvers: OpenNL can be linked with SuperLU
    Simple demo program with LSCM (Least Squares Conformal Maps)

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the %{name} shared library that one can link against.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1

%build
mkdir -p build/linux-Release
cd build/linux-Release
%cmake -DCMAKE_BUILD_TYPE:STRING=Release ../../

make %{?_smp_mflags}


%install
# Install library
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/
install -p -m 0755  build/linux-Release/binaries/lib/libopennl.so.%{version} \
$RPM_BUILD_ROOT/%{_libdir}/

find  build/linux-Release/binaries/lib -type l -exec cp -a '{}' \
$RPM_BUILD_ROOT/%{_libdir}/ \;

# Correct encoding
pushd examples
    sed -i 's/\r//' make_test.bat
popd

# Install includes
install -d $RPM_BUILD_ROOT/%{_includedir}/NL/
cp -av src/NL/nl.h $RPM_BUILD_ROOT/%{_includedir}/
find src/NL/ -name "*.h" ! -name "nl.h" -execdir cp -av '{}' $RPM_BUILD_ROOT/%{_includedir}/NL/ \;

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc doc/*
%{_libdir}/%soname.*

%files devel
%doc examples
%{_libdir}/%soname
%{_includedir}/*

%changelog
* Sat Jul 16 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.2.1-5
- fix doc macro usage

* Fri Jul 15 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.2.1-4
- Modify install section

* Thu Jul 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.2.1-3
- add version macros to soname etc.

* Thu Jul 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.2.1-2
- add patch to correct libname and versioning (courtesy of Richard Shaw)

* Tue Jul 12 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.2.1-1
- initial rpmbuild

