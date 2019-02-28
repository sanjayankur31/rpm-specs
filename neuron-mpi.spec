# Permit build to succeed even when debug build-id is not found
# Only happens for MPI builds.
# Not yet sure why this is happening---all flags are used correctly in the
# build, but the binaries are linked statically. It probably has something to
# do with how I make nrnmpi separately. Will need some checking
# %%global _missing_build_ids_terminate_build 0


# Stop automatic removal of shebang from neuron makefiles
# %%global __brp_mangle_shebangs_exclude_from ^%%{_bindir}/nrn.*makefile$

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

This package provides NEURON built with MPI support.

Please install the devel packages to compile nmodl files and so on.
}

%global tarname nrn

%bcond_without mpich
%bcond_with openmpi

# fails somehow, disabled by default
%bcond_with metis

# IV uses libtiff from 1995 and threfore has not been packaged yet
%bcond_with iv

Name:       neuron-mpi
Version:    7.5
Release:    4.20181214git%{shortcommit}%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv3+
URL:        http://www.neuron.yale.edu/neuron/
# Using brunomaga's fork which updates neuron to use the current sundials
# Will be merged to neuron main eventually
# https://github.com/neuronsimulator/nrn/issues/113
Source0:    https://github.com/brunomaga/%{tarname}/archive/%{commit}/%{tarname}-%{shortcommit}.tar.gz
# Source0:    https://github.com/neuronsimulator/%%{tarname}/archive/%%{commit}/%%{tarname}-%%{shortcommit}.tar.gz

# Based on brunomega's master branch
Patch0:     0001-Unbundle-Random123.patch
# libstdc++ bundled is from 1988: seems heavily modified. Headers from there
# are not present in the current version
# https://github.com/neuronsimulator/nrn/issues/145
# Upstream changes the soname etc., so this will not conflict with the packaged
# version
# Unbundle readline
Patch1:     0002-Unbundle-readline.patch


# Random123 does not build on these, so neither can NEURON
# https://github.com/neuronsimulator/nrn/issues/114
ExcludeArch:    %{arm} mips64r2 mips32r2 s390 s390x

# Requires the neuron package, tightly linked in version
BuildRequires:  neuron-devel%{?_isa} = %{version}-%{release}
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


%if %{with iv}
BuildRequires:  iv-static iv-devel
%endif

%description
%{desc}

%if %{with mpich}
%package mpich
Summary:    %{name} build with MPICH support.
Requires:   mpich
BuildRequires:  rpm-mpi-hooks
BuildRequires:  mpich-devel
BuildRequires:  sundials-mpich-devel

%description mpich
%{desc}

%package mpich-devel
Summary:    Development files for %{name} built with MPICH
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}

%description mpich-devel
Headers and development shared libraries for the %{name} package built with
MPICH support.

%package static-mpich
Summary:    Static libraries for %{name} built with MPICH
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}

%description static-mpich
Static libraries for %{name} built with MPICH.

%endif # endif mpich

%if %{with openmpi}
%package openmpi
Summary:    %{name} build with OpenMPI support.
Requires:   openmpi
BuildRequires:  rpm-mpi-hooks
BuildRequires:  openmpi-devel
BuildRequires:  sundials-openmpi-devel

%description openmpi
%{desc}

%package openmpi-devel
Summary:    Development files for %{name} built with OpenMPI
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-devel
Headers and development shared libraries for the %{name} package built with
OpenMPI support.

%package static-openmpi
Summary:    Static libraries for %{name} built with OpenMPI
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}

%description static-openmpi
Static libraries for %{name} built with OpenMPI.

%endif # endif openmpi

%prep
# Rather around about way?
# 1. Create a new directory and unpack but do not apply patches (they need to
# be applied inside the extracted source directory)
%autosetup -c -n %{tarname}-%{commit} -N

# 2. Enter extracted sources and apply patches
%autosetup -n %{tarname}-%{commit}/%{tarname}-%{commit} -D -T -S git -p1

# 3. Further tweaks in the extracted source directory
# Use -S patch to prevent it from trying to gitify the directory again
%autosetup -T -D -n %{tarname}-%{commit} -N -S patch

# General tweaks to sources before copying it over
pushd %{tarname}-%{commit}
# Remove executable perms from source files
find src -type f -executable ! -name "*.sh" | xargs chmod -x

# Remove bundled Random123
rm -rf src/Random123
rm -rf src/readline

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
popd # out of bin

popd # out of extracted source


%if %{with mpich}
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-mpich
%endif

%if %{with openmpi}
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-openmpi
%endif

%build
export SUNDIALS_SYSTEM_INSTALL="yes"
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

%global do_build %{expand:
echo "*** Building %{tarname}-%{commit}$MPI_COMPILE_TYPE ***"
pushd %{tarname}-%{commit}$MPI_COMPILE_TYPE

./build.sh || exit -1

# use rpm provided ones
# for i in config.guess config.sub; do
    # /usr/bin/cp -fv /usr/lib/rpm/redhat/$(basename $i) $i
# done

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
--build=%{_build} --host=%{_host} \\\
%{iv_flags} %{metis_flags} --with-gnu-ld

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Generate required header for MPI builds
%if %{with mpich} || %{with openmpi}
pushd src/nrnmpi
    sh mkdynam.sh
popd
%endif

%make_build

popd
}

# No serial build

# MPICH
%if %{with mpich}
%{_mpich_load}
export MPI_COMPILE_TYPE="-mpich"
export MPI_OPTIONS="--with-paranrn=dynamic --with-mpi --with-multisend"
%{do_build}
%{_mpich_unload}
%endif # with mpich

# OpenMPI
%if %{with openmpi}
%{_openmpi_load}
export MPI_COMPILE_TYPE="-openmpi"
export MPI_OPTIONS="--with-paranrn=dynamic --with-mpi --with-multisend"
%{do_build}
%{_openmpi_unload}
%endif # with openmpi

%install
%global do_install %{expand:
echo "*** Installing %{tarname}-%{commit}$MPI_COMPILE_TYPE ***"
%make_install -C %{tarname}-%{commit}$MPI_COMPILE_TYPE
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

# No serial install

# MPICH
%if %{with mpich}
%{_mpich_load}
export MPI_COMPILE_TYPE="-mpich"
%{do_install}
%{modify_for_mpi}
%{_mpich_unload}
%endif # with mpich

# OpenMPI
%if %{with openmpi}
%{_openmpi_load}
export MPI_COMPILE_TYPE="-openmpi"
%{do_install}
%{modify_for_mpi}
%{_openmpi_unload}
%endif # with openmpi

# Post install clean up
# Remove stray object files
# Probably worth a PR
# Must be done at end, otherwise it deletes object files required for other builds
find . $RPM_BUILD_ROOT/%{_libdir}/ -name "*.o" -exec rm -f '{}' \;

%ldconfig_scriptlets

# The makefiles do not have shebangs
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

%files mpich-devel
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

%if %{with openmpi}
%files openmpi
%license Copyright
%doc README.md
# Binaries, makefiles, scripts
%{_libdir}/openmpi/bin/bbswork_openmpi.sh
%{_libdir}/openmpi/bin/hel2mos1_openmpi.sh
%{_libdir}/openmpi/bin/ivoc_openmpi
%{_libdir}/openmpi/bin/memacs_openmpi
%{_libdir}/openmpi/bin/mkthreadsafe_openmpi
%{_libdir}/openmpi/bin/modlunit_openmpi
%{_libdir}/openmpi/bin/mos2nrn_openmpi
%{_libdir}/openmpi/bin/mos2nrn2_openmpi.sh
%{_libdir}/openmpi/bin/neurondemo_openmpi
%{_libdir}/openmpi/bin/nocmodl_openmpi
%{_libdir}/openmpi/bin/nrndiagnose_openmpi.sh
%{_libdir}/openmpi/bin/nrngui_openmpi
%{_libdir}/openmpi/bin/nrniv_openmpi
%{_libdir}/openmpi/bin/nrniv_makefile_openmpi
%{_libdir}/openmpi/bin/nrnivmodl_openmpi
%{_libdir}/openmpi/bin/nrnmech_makefile_openmpi
%{_libdir}/openmpi/bin/nrnoc_openmpi
%{_libdir}/openmpi/bin/nrnoc_makefile_openmpi
%{_libdir}/openmpi/bin/nrnocmodl_openmpi
%{_libdir}/openmpi/bin/oc_openmpi
%{_libdir}/openmpi/bin/sortspike_openmpi
# Libraries
%{_libdir}/openmpi/lib/libivoc.so.0.0.0
%{_libdir}/openmpi/lib/libivoc.so.0
%{_libdir}/openmpi/lib/libmemacs.so.0.0.0
%{_libdir}/openmpi/lib/libmemacs.so.0
%{_libdir}/openmpi/lib/libmeschach.so.0.0.0
%{_libdir}/openmpi/lib/libmeschach.so.0
%{_libdir}/openmpi/lib/libneuron_gnu.so.0.0.0
%{_libdir}/openmpi/lib/libneuron_gnu.so.0
%{_libdir}/openmpi/lib/libnrniv.so.0.0.0
%{_libdir}/openmpi/lib/libnrniv.so.0
%{_libdir}/openmpi/lib/libnrnmpi.so.0.0.0
%{_libdir}/openmpi/lib/libnrnmpi.so.0
%{_libdir}/openmpi/lib/libnrnoc.so.0.0.0
%{_libdir}/openmpi/lib/libnrnoc.so.0
%{_libdir}/openmpi/lib/liboc.so.0.0.0
%{_libdir}/openmpi/lib/liboc.so.0
%{_libdir}/openmpi/lib/libocxt.so.0.0.0
%{_libdir}/openmpi/lib/libocxt.so.0
%{_libdir}/openmpi/lib/libsparse13.so.0.0.0
%{_libdir}/openmpi/lib/libsparse13.so.0
%{_libdir}/openmpi/lib/libscopmath.so.0
%{_libdir}/openmpi/lib/libscopmath.so.0.0.0
%{_libdir}/openmpi/lib/libivos.so.0
%{_libdir}/openmpi/lib/libivos.so.0.0.0

%dir %{_libdir}/openmpi/share/%{tarname}
%{_libdir}/openmpi/share/%{tarname}/lib

%files openmpi-devel
%license Copyright
%doc README.md
%{_includedir}/openmpi-%{_arch}/%{tarname}
%{_libdir}/openmpi/lib/libivoc.so
%{_libdir}/openmpi/lib/libmemacs.so
%{_libdir}/openmpi/lib/libmeschach.so
%{_libdir}/openmpi/lib/libneuron_gnu.so
%{_libdir}/openmpi/lib/libnrniv.so
%{_libdir}/openmpi/lib/libnrnmpi.so
%{_libdir}/openmpi/lib/libnrnoc.so
%{_libdir}/openmpi/lib/liboc.so
%{_libdir}/openmpi/lib/libocxt.so
%{_libdir}/openmpi/lib/libsparse13.so
%{_libdir}/openmpi/lib/libscopmath.so
%{_libdir}/openmpi/lib/libivos.so

# should this be here?!
%{_libdir}/openmpi/lib/nrnconf.h

# Do we need the static libraries?
%files static-openmpi
%license Copyright
%doc README.md
%{_libdir}/openmpi/lib/libivoc.la
%{_libdir}/openmpi/lib/libmemacs.la
%{_libdir}/openmpi/lib/libmeschach.la
%{_libdir}/openmpi/lib/libneuron_gnu.la
%{_libdir}/openmpi/lib/libnrniv.la
%{_libdir}/openmpi/lib/libnrnmpi.la
%{_libdir}/openmpi/lib/libnrnoc.la
%{_libdir}/openmpi/lib/liboc.la
%{_libdir}/openmpi/lib/libocxt.la
%{_libdir}/openmpi/lib/libsparse13.la
%{_libdir}/openmpi/lib/libscopmath.la
%{_libdir}/openmpi/lib/libivos.la

%endif # with openmpi


%changelog
* Thu Feb 28 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-4.20181214git5687519
- Initial build
