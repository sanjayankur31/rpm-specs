# This is a serial build of NEURON without Python or other bindings.
# Both the MPI builds and Python bindings require NEURON to be already
# installed in the system---they are build as post-installation hooks. So, we
# first package a serial version of NEURON and then package those separately
# after using this package as a BR

%global commit 56875193411d552eea7d4cbfe09458f3c4f76613
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global desc %{expand: \
NEURON is a simulation environment for modeling individual neurons and networks
of neurons. It provides tools for conveniently building, managing, and using
models in a way that is numerically sound and computationally efficient. It is
particularly well-suited to problems that are closely linked to experimental
data, especially those that involve cells with complex anatomical and
biophysical properties.

This package is currently built without GUI (iv) support.
It does not include MPI support.

Please install the %{name}-devel package to compile nmodl files and so on.
}

%global tarname nrn

# fails somehow, disabled by default
%bcond_with metis

# IV uses libtiff from 1995 and threfore has not been packaged yet
%bcond_with iv

Name:       neuron
Version:    7.5
Release:    2.20181214git%{shortcommit}%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv2+
URL:        http://www.neuron.yale.edu/neuron/
# Using brunomaga's fork which updates neuron to use the current sundials
# Will be merged to neuron main eventually
# https://github.com/neuronsimulator/nrn/issues/113
Source0:    https://github.com/brunomaga/%{tarname}/archive/%{commit}/%{tarname}-%{shortcommit}.tar.gz
# Source0:    https://github.com/neuronsimulator/%%{tarname}/archive/%%{commit}/%%{tarname}-%%{shortcommit}.tar.gz

# Based on brunomega's master branch
Patch0:     0001-Unbundle-Random123.patch

# Random123 does not build on these, so neither can NEURON
# https://github.com/neuronsimulator/nrn/issues/114
ExcludeArch:    %{arm} mips64r2 mips32r2 s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  bison-devel
BuildRequires:  flex
BuildRequires:  flex-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
%if %{with iv}
BuildRequires:  iv-static iv-devel
%endif
BuildRequires:  libX11-devel
BuildRequires:  libtool
%if %{with metis}
BuildRequires:  metis-devel
%endif
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  Random123-devel
BuildRequires:  sundials-devel

%description
%{desc}

%package devel
Summary:    Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and development shared libraries for the %{name} package

%package static
Summary:    Static libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description static
Static libraries for %{name}

%package doc
Summary:    Documentation for %{name}
BuildArch:  noarch

%description doc
Documentation for %{name}


%prep
%autosetup -n %{tarname}-%{commit} -p1 -S git

rm -rf src/Random123

# Stop build file from generating version header
sed -i '/git2nrnversion_h.sh/ d' build.sh

# Create version file ourselves
export TIMESTAMP=$(date +%Y-%m-%d)
export COMMIT=%{shortcommit}
cat > src/nrnoc/nrnversion.h << EOF
#define GIT_DATE "$TIMESTAMP"
#define GIT_BRANCH "master"
#define GIT_CHANGESET "$COMMIT"
#define GIT_DESCRIBE "Neuron built for Fedora"
EOF

# Use system libtool instead of a local copy that neuron tries to install
pushd bin
    for f in *_makefile.in
    do
        sed -i 's|\(LIBTOOL.*=.*\)$(pkgdatadir)\(.*\)|\1$(bindir)\2|' $f
    done
popd

%build
export SUNDIALS_SYSTEM_INSTALL="yes"
./build.sh

%if !%{with iv}
%global iv_flags  --without-iv --with-x
%else
%global iv_flags " "
%endif

%if %{with metis}
%global metis_flags --with-metis
%else
%global metis_flags " "
%endif

%configure %{iv_flags} %{metis_flags} --with-gnu-ld

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool && \
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install
# Installs it even when we're not providing nrnpy
rm -fv $RPM_BUILD_ROOT/%{_bindir}/*nrnpy* -f
# Remove installed libtool copy
rm -fv $RPM_BUILD_ROOT/%{_datadir}/%{tarname}/libtool

# Post install clean up
# Remove stray object files
# Probably worth a PR
# Must be done at end, otherwise it deletes object files required for other builds
find . $RPM_BUILD_ROOT/%{_libdir}/ -name "*.o" -exec rm -f '{}' \;

# Still needed on F28?
%ldconfig_scriptlets

# The makefiles do not have shebangs
%files
%license Copyright
%doc README.md
# Binaries, scripts and makefiles
%{_bindir}/bbswork.sh
%{_bindir}/hel2mos1.sh
%{_bindir}/ivoc
%{_bindir}/memacs
%{_bindir}/mkthreadsafe
%{_bindir}/modlunit
%{_bindir}/mos2nrn
%{_bindir}/mos2nrn2.sh
%{_bindir}/neurondemo
%{_bindir}/nocmodl
%{_bindir}/nrndiagnose.sh
%{_bindir}/nrngui
%{_bindir}/nrniv
%{_bindir}/nrniv_makefile
%{_bindir}/nrnivmodl
%{_bindir}/nrnmech_makefile
%{_bindir}/nrnoc
%{_bindir}/nrnoc_makefile
%{_bindir}/nrnocmodl
%{_bindir}/oc
%{_bindir}/sortspike
# Libs
%{_libdir}/libivoc.so.0.0.0
%{_libdir}/libivoc.so.0
%{_libdir}/libmemacs.so.0.0.0
%{_libdir}/libmemacs.so.0
%{_libdir}/libmeschach.so.0.0.0
%{_libdir}/libmeschach.so.0
%{_libdir}/libneuron_gnu.so.0.0.0
%{_libdir}/libneuron_gnu.so.0
%{_libdir}/libnrniv.so.0.0.0
%{_libdir}/libnrniv.so.0
%{_libdir}/libnrnmpi.so.0.0.0
%{_libdir}/libnrnmpi.so.0
%{_libdir}/libnrnoc.so.0.0.0
%{_libdir}/libnrnoc.so.0
%{_libdir}/liboc.so.0.0.0
%{_libdir}/liboc.so.0
%{_libdir}/libocxt.so.0.0.0
%{_libdir}/libocxt.so.0
%{_libdir}/libsparse13.so.0.0.0
%{_libdir}/libsparse13.so.0
%{_libdir}/libscopmath.so.0
%{_libdir}/libscopmath.so.0.0.0
%{_libdir}/libivos.so.0
%{_libdir}/libivos.so.0.0.0
# other hoc files and data
%dir %{_datadir}/%{tarname}
%{_datadir}/%{tarname}/lib

%files devel
%license Copyright
%doc README.md
%{_includedir}/%{tarname}
%{_libdir}/libivoc.so
%{_libdir}/libmemacs.so
%{_libdir}/libmeschach.so
%{_libdir}/libneuron_gnu.so
%{_libdir}/libnrniv.so
%{_libdir}/libnrnmpi.so
%{_libdir}/libnrnoc.so
%{_libdir}/liboc.so
%{_libdir}/libocxt.so
%{_libdir}/libsparse13.so
%{_libdir}/libscopmath.so
%{_libdir}/libivos.so

# should this be here?!
%{_libdir}/nrnconf.h

# Do we need the static libraries?
%files static
%license Copyright
%doc README.md
%{_libdir}/libivoc.la
%{_libdir}/libmemacs.la
%{_libdir}/libmeschach.la
%{_libdir}/libneuron_gnu.la
%{_libdir}/libnrniv.la
%{_libdir}/libnrnmpi.la
%{_libdir}/libnrnoc.la
%{_libdir}/liboc.la
%{_libdir}/libocxt.la
%{_libdir}/libsparse13.la
%{_libdir}/libscopmath.la
%{_libdir}/libivos.la

%files doc
%license Copyright
%doc README.md
%{_datadir}/%{tarname}/examples
%{_datadir}/%{tarname}/demo

%changelog
* Sun Jan 06 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-2.20181214git5687519
- Put each BR on different line
- Remove unneeded comment
- Re-do random123 patch to only modify autotools files
- Remove random123 in prep

* Fri Dec 28 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-1.20181214git5687519
- Update to latest git snapshot that uses current sundials
- Build without MPI
