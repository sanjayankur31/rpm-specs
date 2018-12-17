# Permit build to succeed even when debug build-id is not found
# Not yet sure why this is happening---all flags are used correctly in the build
# Only happens with MPI binaries, but they're built pretty much in the same way
# as the serial binary too
%global _missing_build_ids_terminate_build 0


# Stop automatic removal of shebang from neuron makefiles
%global __brp_mangle_shebangs_exclude_from ^%{_bindir}/nrn.*makefile$

%global commit 56875193411d552eea7d4cbfe09458f3c4f76613
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global desc %{expand: \
NEURON is a simulation environment for modeling individual neurons and networks
of neurons. It provides tools for conveniently building, managing, and using
models in a way that is numerically sound and computationally efficient. It is
particularly well-suited to problems that are closely linked to experimental
data, especially those that involve cells with complex anatomical and
biophysical properties.

This is currently built without GUI (iv) support.

Please install the %{name}-devel package to compile nmodl files and so on.
}

%global tarname nrn

%bcond_without mpich
%bcond_with openmpi

# fails somehow, disabled by default
%bcond_with metis

# IV uses libtiff from 1995 and threfore has not been packaged yet
%bcond_with iv

Name:       neuron
Version:    7.5
Release:    1.20181214git%{shortcommit}%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv2+
URL:        http://www.neuron.yale.edu/neuron/
# Using brunomaga's fork which updates neuron to use the current sundials
# Will be merged to neuron main eventually
# https://github.com/neuronsimulator/nrn/issues/113
Source0:    https://github.com/brunomaga/%{tarname}/archive/%{commit}/%{tarname}-%{shortcommit}.tar.gz
# Source0:    https://github.com/neuronsimulator/%%{tarname}/archive/%%{commit}/%%{tarname}-%%{shortcommit}.tar.gz

Patch0:     0001-Unbundle-Random123-for-brunomegas-branch.patch

# For mpi versions nrnmpi must be built after oc and nrniv
# Upstream does this by building nrnmpi as a post-install-hook when liboc and
# libnrniv have already been installed in %%{_libdir}, but we want to do it
# during the build, so we do not let the Makefiles' subdirectory system do it.
# We do it ourselves.
Patch1:     0001-Disable-mpi-libnrnmpi-build.patch

# Random123 does not build on these, so neither can NEURON
# https://github.com/neuronsimulator/nrn/issues/114
ExcludeArch:    %{arm} mips64r2 mips32r2 s390 s390x

BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  Random123-devel
BuildRequires:  libX11-devel
BuildRequires:  metis-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf automake libtool
BuildRequires:  git
BuildRequires:  bison bison-devel
BuildRequires:  flex-devel flex
BuildRequires:  sundials-devel

%if %{with iv}
BuildRequires:  iv-static iv-devel
%endif

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

%if %{with mpich}
%package mpich
Summary:    %{name} build with MPICH support.
Requires:   mpich
BuildRequires:  rpm-mpi-hooks
BuildRequires:  mpich-devel
BuildRequires:  sundials-mpich-devel

%description mpich
%{desc}

%package devel-mpich
Summary:    Development files for %{name} built with MPICH
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}

%description devel-mpich
Headers and development shared libraries for the %{name} package built with
MPICH support.

%package static-mpich
Summary:    Static libraries for %{name} built with MPICH
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}

%description static-mpich
Static libraries for %{name} built with MPICH.

%endif


%prep
%autosetup -c -n %{tarname}-%{commit} -N

cp %{tarname}-%{commit}/Copyright . -v
cp %{tarname}-%{commit}/README.md . -v

pushd %{tarname}-%{commit}
    %autopatch -p1

    # Let us tell the system where to find the sundials libraries. It is hard coded.
    sed -i 's|SUNDIALS_LIBDIRNAMES="${prefix}/lib"|SUNDIALS_LIBDIRNAMES="$MPI_LIB"|' configure.ac

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
popd

%if %{with mpich}
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-mpich
# Disable subdir based build of nrnmpi
sed -i "s/nrnmpi//" %{tarname}-%{commit}-mpich/src/Makefile.am
%endif

%if %{with openmpi}
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-openmpi
# Disable subdir based build of nrnmpi
sed -i "s/nrnmpi//" %{tarname}-%{commit}-openmpi/src/Makefile.am
%endif

%build
export SUNDIALS_SYSTEM_INSTALL="yes"
%global do_build %{expand:
echo "*** Building %{tarname}-%{commit}$MPI_COMPILE_TYPE ***"
pushd %{tarname}-%{commit}$MPI_COMPILE_TYPE
./build.sh &&
%{set_build_flags}
./configure \\\
--enable-static=no \\\
--enable-shared=yes \\\
--enable-dependency-tracking \\\
--prefix=$MPI_HOME \\\
--exec-prefix=$MPI_HOME \\\
--bindir=$MPI_BIN \\\
--sbindir=$MPI_HOME/bin/ \\\
--datadir=$MPI_HOME/share/ \\\
--includedir=$MPI_INCLUDE \\\
--libdir=$MPI_LIB \\\
--mandir=$MPI_MAN $MPI_OPTIONS \\\
%if !%{with iv} \
--without-iv --with-x \\\
%endif \
--with-gnu-ld \\\
%if %{with metis} \
--with-metis  \\\
%endif

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool &&
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool &&

# Generate required header for MPI builds
%if %{with mpich} || %{with openmpi}
pushd src/nrnmpi
    sh mkdynam.sh
popd
%endif

%make_build


# For mpi versions nrnmpi must be built after oc and nrniv
# Upstream does this by building nrnmpi as a post-install-hook when liboc and
# libnrniv have already been installed in %%{_libdir}, but we want to do it
# during the build, so we do not let the Makefiles' subdirectory system do it.
# We do it ourselves.
%if %{with mpich} || %{with openmpi}
    %make_build -C src/nrnmpi
%endif

popd
}

# Serial build
export MPI_COMPILE_TYPE=""
export MPI_OPTIONS=""
export MPI_LIB="%{_libdir}"
export MPI_HOME="%{_prefix}"
export MPI_BIN="%{_bindir}"
export MPI_INCLUDE="%{_includedir}"
export MPI_MAN="%{_mandir}"
%{do_build}

# MPICH
%if %{with mpich}
%{_mpich_load}
export MPI_COMPILE_TYPE="-mpich"
export MPI_OPTIONS="--with-paranrn=dynamic --with-mpi --with-multisend"
%{do_build}
%{_mpich_unload}
%endif # with mpich

%install
%global do_install %{expand:
echo "*** Installing %{tarname}-%{commit}$MPI_COMPILE_TYPE ***"
%make_install -C %{tarname}-%{commit}$MPI_COMPILE_TYPE

# Manualy install mpi bits for MPI builds where we've disabled the subdir in the main makefile
%if %{with mpich} || %{with openmpi}
    %make_install -C %{tarname}-%{commit}$MPI_COMPILE_TYPE/src/nrnmpi
%endif
}

%global modify_for_mpi %{expand:
# Remove installed libtool
rm -fv $RPM_BUILD_ROOT/$MPI_HOME/share/%{tarname}/libtool
# Remove docs for MPI packages
rm -rf $RPM_BUILD_ROOT/$MPI_HOME/share/%{tarname}/examples
rm -rf $RPM_BUILD_ROOT/$MPI_HOME/share/%{tarname}/demo
# Remove nrnpy bits
# nrnpython requires neuron to be installed already, so we'll provide that as a
# separate package
pushd $RPM_BUILD_ROOT/$MPI_BIN
    rm -fv *nrnpy*
    # The HAMMER: Replace references to all these files with ones suffixed with
    # $MPI_SUFFIX
    for f in ivoc memacs mkthreadsafe modlunit mos2nrn neurondemo nocmodl nrngui nrniv nrniv_makefile nrnivmodl nrnmech_makefile nrnoc nrnoc_makefile nrnocmodl oc sortspike bbswork.sh hel2mos1.sh mos2nrn2.sh nrndiagnose.sh; do

        for t in ivoc memacs mkthreadsafe modlunit mos2nrn neurondemo nocmodl nrngui nrniv nrniv_makefile nrnivmodl nrnmech_makefile nrnoc nrnoc_makefile nrnocmodl oc sortspike bbswork hel2mos1 mos2nrn2 nrndiagnose; do
            sed -i "s/$t/$t$MPI_SUFFIX/g" $f
        done
    done

    # Rename the files: shell scripts
    for f in bbswork hel2mos1 mos2nrn2 nrndiagnose ; do
        cp -pv $f{,$MPI_SUFFIX}.sh && rm -f $f.sh
    done

    # Other files
    for f in ivoc memacs mkthreadsafe modlunit mos2nrn neurondemo nocmodl nrngui nrniv nrniv_makefile nrnivmodl nrnmech_makefile nrnoc nrnoc_makefile nrnocmodl oc sortspike; do
        # Rename files
        cp -pv $f{,$MPI_SUFFIX} && rm -f $f
    done
popd
}

export MPI_COMPILE_TYPE=""
%{do_install}
# Installs it even when we're not providing nrnpy
rm -fv $RPM_BUILD_ROOT/%{_bindir}/*nrnpy* -f
# Remove installed libtool copy
rm -fv $RPM_BUILD_ROOT/%{_datadir}/%{tarname}/libtool

# MPICH
%if %{with mpich}
%{_mpich_load}
export MPI_COMPILE_TYPE="-mpich"
%{do_install}
%{modify_for_mpi}
%{_mpich_unload}
%endif # with mpich

# Post install clean up
# Remove stray object files
# Probably worth a PR
# Must be done at end, otherwise it deletes object files required for other builds
find . $RPM_BUILD_ROOT/%{_libdir}/ -name "*.o" -exec rm -f '{}' \;

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

%if %{with mpich}
%files mpich
%license Copyright
%doc README.md
# Binaries, makefiles, scripts
%{_libdir}/mpich/bin/bbswork_mpich.sh
%{_libdir}/mpich/bin/hel2mos1_mpich.sh
%{_libdir}/mpich/bin/ivoc_mpich
%{_libdir}/mpich/bin/memacs_mpich
%{_libdir}/mpich/bin/mkthreadsafe_mpich
%{_libdir}/mpich/bin/modlunit_mpich
%{_libdir}/mpich/bin/mos2nrn_mpich
%{_libdir}/mpich/bin/mos2nrn2_mpich.sh
%{_libdir}/mpich/bin/neurondemo_mpich
%{_libdir}/mpich/bin/nocmodl_mpich
%{_libdir}/mpich/bin/nrndiagnose_mpich.sh
%{_libdir}/mpich/bin/nrngui_mpich
%{_libdir}/mpich/bin/nrniv_mpich
%{_libdir}/mpich/bin/nrniv_makefile_mpich
%{_libdir}/mpich/bin/nrnivmodl_mpich
%{_libdir}/mpich/bin/nrnmech_makefile_mpich
%{_libdir}/mpich/bin/nrnoc_mpich
%{_libdir}/mpich/bin/nrnoc_makefile_mpich
%{_libdir}/mpich/bin/nrnocmodl_mpich
%{_libdir}/mpich/bin/oc_mpich
%{_libdir}/mpich/bin/sortspike_mpich
# Libraries
%{_libdir}/mpich/lib/libivoc.so.0.0.0
%{_libdir}/mpich/lib/libivoc.so.0
%{_libdir}/mpich/lib/libmemacs.so.0.0.0
%{_libdir}/mpich/lib/libmemacs.so.0
%{_libdir}/mpich/lib/libmeschach.so.0.0.0
%{_libdir}/mpich/lib/libmeschach.so.0
%{_libdir}/mpich/lib/libneuron_gnu.so.0.0.0
%{_libdir}/mpich/lib/libneuron_gnu.so.0
%{_libdir}/mpich/lib/libnrniv.so.0.0.0
%{_libdir}/mpich/lib/libnrniv.so.0
%{_libdir}/mpich/lib/libnrnmpi.so.0.0.0
%{_libdir}/mpich/lib/libnrnmpi.so.0
%{_libdir}/mpich/lib/libnrnoc.so.0.0.0
%{_libdir}/mpich/lib/libnrnoc.so.0
%{_libdir}/mpich/lib/liboc.so.0.0.0
%{_libdir}/mpich/lib/liboc.so.0
%{_libdir}/mpich/lib/libocxt.so.0.0.0
%{_libdir}/mpich/lib/libocxt.so.0
%{_libdir}/mpich/lib/libsparse13.so.0.0.0
%{_libdir}/mpich/lib/libsparse13.so.0
%{_libdir}/mpich/lib/libscopmath.so.0
%{_libdir}/mpich/lib/libscopmath.so.0.0.0
%{_libdir}/mpich/lib/libivos.so.0
%{_libdir}/mpich/lib/libivos.so.0.0.0

%dir %{_libdir}/mpich/share/%{tarname}
%{_libdir}/mpich/share/%{tarname}/lib

%files devel-mpich
%license Copyright
%doc README.md
%{_includedir}/mpich-%{_arch}/%{tarname}
%{_libdir}/mpich/lib/libivoc.so
%{_libdir}/mpich/lib/libmemacs.so
%{_libdir}/mpich/lib/libmeschach.so
%{_libdir}/mpich/lib/libneuron_gnu.so
%{_libdir}/mpich/lib/libnrniv.so
%{_libdir}/mpich/lib/libnrnmpi.so
%{_libdir}/mpich/lib/libnrnoc.so
%{_libdir}/mpich/lib/liboc.so
%{_libdir}/mpich/lib/libocxt.so
%{_libdir}/mpich/lib/libsparse13.so
%{_libdir}/mpich/lib/libscopmath.so
%{_libdir}/mpich/lib/libivos.so

# should this be here?!
%{_libdir}/mpich/lib/nrnconf.h

# Do we need the static libraries?
%files static-mpich
%license Copyright
%doc README.md
%{_libdir}/mpich/lib/libivoc.la
%{_libdir}/mpich/lib/libmemacs.la
%{_libdir}/mpich/lib/libmeschach.la
%{_libdir}/mpich/lib/libneuron_gnu.la
%{_libdir}/mpich/lib/libnrniv.la
%{_libdir}/mpich/lib/libnrnmpi.la
%{_libdir}/mpich/lib/libnrnoc.la
%{_libdir}/mpich/lib/liboc.la
%{_libdir}/mpich/lib/libocxt.la
%{_libdir}/mpich/lib/libsparse13.la
%{_libdir}/mpich/lib/libscopmath.la
%{_libdir}/mpich/lib/libivos.la

%endif # with mpich

%changelog
* Sun Dec 9 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-1.20181214git5687519
- Update to latest git snapshot that uses current sundials
