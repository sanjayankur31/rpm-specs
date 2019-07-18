# MUSIC depends on MPI for communication, so a non-MPI version is not being
# built.
# https://github.com/INCF/MUSIC/issues/55


%global commit a77e57878158b36401c0977702c1386ba01db118
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# For debugging
%bcond_without mpich
%bcond_with openmpi

%global lname music

%global _description %{expand:
MUSIC is an API allowing large scale neuron simulators using MPI internally to
exchange data during runtime.  MUSIC provides mechanisms to transfer massive
amounts of event information and continuous values from one parallel
application to another.  Special care has been taken to ensure that existing
simulators can be adapted to MUSIC.  In particular, MUSIC handles data transfer
between applications that use different time steps and different data
allocation strategies.

This is the MUSIC pilot implementation.

The two most important components built from this software distribution is the
music library `libmusic.a' and the music utility `music'.  A MUSIC-aware
simulator links against the C++ library and can be launched using mpirun
together with the music utility as described below.  MUSIC can also be used
from a C program using the API in music-c.h.

MUSIC is distributed under the GNU General Public License v3.}


Name:           MUSIC
Version:        0
Release:        2.20190717git%{shortcommit}%{?dist}
Summary:        MUSIC, the MUltiSimulation Coordinator

License:        GPLv3+
URL:            https://github.com/INCF/%{name}/
Source0:        https://github.com/INCF/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# https://github.com/INCF/MUSIC/pull/53
Patch0:         0001-Fix-python3-syntax-error.patch

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  freeglut-devel
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  libtool
BuildRequires:  python3-devel
BuildRequires:  python3-Cython
# Currently bundles a modified version of rudeconfig which cannot be unbundled
# until MUSIC upstream sends their changes upstream to rudeconfig.
# https://github.com/INCF/MUSIC/issues/56
# BuildRequires:  rudeconfig-devel

%description %_description


%if %{with openmpi}
%package openmpi
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
Requires:       %{name} = %{version}-%{release}
%description openmpi %_description

%package openmpi-devel
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
Requires:       %{name} = %{version}-%{release}
%description openmpi-devel
Development files for %{name} built with OpenMPI.

%package -n python3-%{name}-openmpi
Summary:        Python3 support for %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  python3-mpi4py-openmpi
Requires:       python3-mpi4py-openmpi
Requires:       openmpi
Requires:       %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-openmpi}

%description -n python3-%{name}-openmpi %_description
%endif


%if %{with mpich}
%package mpich
Summary:        %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich
Requires:       %{name}-common = %{version}-%{release}

%description mpich %_description

%package mpich-devel
Summary:        %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich
Requires:       %{name}-common = %{version}-%{release}

%description mpich-devel
Development files for %{name} built with MPICH.

%package -n python3-%{name}-mpich
Summary:        Python3 support for %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  python3-mpi4py-mpich
Requires:       python3-mpi4py-mpich
Requires:       mpich
Requires:       %{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-mpich}

%description -n python3-%{name}-mpich %_description
%endif

%prep
%autosetup -c -n %{name}-%{commit} -N -S git

cp %{name}-%{commit}/LICENSE .
cp %{name}-%{commit}/README .

# Apply patches
pushd %{name}-%{commit}
    %autopatch
popd

%if %{with mpich}
    cp -a %{name}-%{commit} %{name}-%{commit}-mpich
%endif

%if %{with openmpi}
    cp -a %{name}-%{commit} %{name}-%{commit}-openmpi
%endif

%build

%global do_build \
echo "** BUILDING $MPI_COMPILE_TYPE **" \
pushd %{name}-%{commit}$MPI_COMPILE_TYPE && \
./autogen.sh && \
%{set_build_flags} \
MPI_CXXFLAGS="$CXXFLAGS $(pkg-config --cflags $MPI_VARIANT)" \
MPI_CFLAGS="$CFLAGS $(pkg-config --cflags $MPI_VARIANT)" \
MPI_LDFLAGS="$LDFLAGS -L$MPI_LIB -lmpi" \
./configure MPI_CXXFLAGS="$MPI_CXXFLAGS" MPI_CFLAGS="$MPI_CFLAGS" MPI_LDFLAGS="$MPI_LDFLAGS" PYTHON="$PYTHON_BIN" \\\
--disable-static \\\
--prefix=$MPI_HOME \\\
--libdir=$MPI_LIB \\\
--includedir=$MPI_INCLUDE \\\
--bindir=$MPI_BIN \\\
--mandir=$MPI_MAN && \
%make_build && \
popd || exit -1


# Mpich
%if %{with mpich}
%{_mpich_load}
MPI_CXX="mpicxx"
MPI_VARIANT="mpich"

MPI_COMPILE_TYPE="-mpich"
PYTHON_VERSION=3
PYTHON_BIN="%{__python3}"
%{do_build}

%{_mpich_unload}
%endif

# Openmpi
%if %{with openmpi}
%{_openmpi_load}
MPI_CXX="mpicxx"
MPI_VARIANT="openmpi"

MPI_COMPILE_TYPE="-openmpi"
PYTHON_VERSION=3
PYTHON_BIN="%{__python3}"
%{do_build}
%{_openmpi_unload}
%endif

%install
%global do_install \
%make_install -C %{name}-%{commit}$MPI_COMPILE_TYPE || exit -1

# Mpich
%if %{with mpich}
%{_mpich_load}
MPI_COMPILE_TYPE="-mpich"
%{do_install}
%{_mpich_unload}
%endif

# Openmpi
%if %{with openmpi}
%{_openmpi_load}
MPI_COMPILE_TYPE="-openmpi"
%{do_install}
%{_openmpi_unload}
%endif

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# For F28 etc?
%ldconfig_scriptlets


%files
%license LICENSE
%doc README

%if %{with mpich}
%files mpich
%license LICENSE
%{_libdir}/mpich/bin/%{lname}
%{_libdir}/mpich/bin/%{lname}_tests.sh
%{_libdir}/mpich/bin/%{lname}run
%{_libdir}/mpich/lib/libmusic-c.so.1
%{_libdir}/mpich/lib/libmusic-c.so.1.0.0

%files mpich-devel
%license LICENSE
%{_includedir}/mpich*/%{name}
%{_includedir}/mpich*/%{name}*.*
%{_includedir}/mpich*/predict_rank-c.h
%{_libdir}/mpich/lib/libmusic-c.so

%files -n python3-%{name}-mpich
%license LICENSE
# %{_libdir}/mpich/lib/%{name}.so.*
%endif

%if %{with openmpi}
%files openmpi
%license LICENSE
# %{_libdir}/openmpi/lib/%{name}.so.*

%files openmpi-devel
%license LICENSE
# %{_includedir}/openmpi*/neurosim
# %{_libdir}/openmpi/lib/*.so

%files -n python3-%{name}-openmpi
%license LICENSE
# %{_libdir}/openmpi/lib/libpy3neurosim*.so.*
%endif

%changelog
* Wed Jul 17 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-2.20190717gita77e5787
- Bundle rudeconfig
- Remove python 2 subpackage

* Sat Oct 20 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-1.20181020gita77e5787
- Depend on packaged rudeconfig
- Remove non MPI packages
- Use macros
- Put common files into separate sub package
- Correct autosetup usage
- Initial build
