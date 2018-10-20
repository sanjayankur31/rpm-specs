# MUSIC depends on MPI for communication, so a non-MPI version is not being
# built.
# https://github.com/INCF/MUSIC/issues/55

# Since the main package is now empty, instead of using a -common sub package
# for the noarch files, I'll just use the main package.

# TODO: unbundle rudeconfig

%global commit a77e57878158b36401c0977702c1386ba01db118
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global with_mpich 1
%global with_openmpi 1
%global with_py2 0

%global lname music

%global _description \
MUSIC is an API allowing large scale neuron simulators using MPI internally to \
exchange data during runtime.  MUSIC provides mechanisms to transfer massive \
amounts of event information and continuous values from one parallel \
application to another.  Special care has been taken to ensure that existing \
simulators can be adapted to MUSIC.  In particular, MUSIC handles data transfer \
between applications that use different time steps and different data \
allocation strategies. \
\
This is the MUSIC pilot implementation. \
\
The two most important components built from this software distribution is the \
music library `libmusic.a' and the music utility `music'.  A MUSIC-aware \
simulator links against the C++ library and can be launched using mpirun \
together with the music utility as described below.  MUSIC can also be used \
from a C program using the API in music-c.h. \
\
MUSIC is distributed under the GNU General Public License v3.


Name:           MUSIC
Version:        0
Release:        1.20181020git%{shortcommit}%{?dist}
Summary:        MUSIC, the MUltiSimulation Coordinator

License:        GPLv3+
URL:            https://github.com/INCF/%{name}/
Source0:        https://github.com/INCF/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  python3-Cython
BuildRequires:  freeglut-devel

%if %{with_py2}
BuildRequires:  python2-devel
BuildRequires:  python2-Cython
%endif

BuildArch:      noarch

%description
%{_description}


%if %{with_openmpi}
%package openmpi
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
Requires:       %{name} = %{version}-%{release}
%description openmpi
%{_description}

%package openmpi-devel
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
Requires:       %{name} = %{version}-%{release}
%description openmpi-devel
%{_description}

%package -n python3-%{name}-openmpi
Summary:        Python3 support for %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  python3-mpi4py-openmpi
Requires:       python3-mpi4py-openmpi
Requires:       openmpi
Requires:       %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-openmpi}

%description -n python3-%{name}-openmpi
%{_description}

%if %{with_py2}
%package -n python2-%{name}-openmpi
Summary:        Python2 support for %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  python2-mpi4py-openmpi
Requires:       python2-mpi4py-openmpi
Requires:       openmpi
Requires:       %{name} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-openmpi}

%description -n python2-%{name}-openmpi
%{_description}
%endif
%endif


%if %{with_mpich}
%package mpich
Summary:        %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich
Requires:       %{name}-common = %{version}-%{release}

%description mpich
%{_description}

%package mpich-devel
Summary:        %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich
Requires:       %{name}-common = %{version}-%{release}

%description mpich-devel
%{_description}

%package -n python3-%{name}-mpich
Summary:        Python3 support for %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  python3-mpi4py-mpich
Requires:       python3-mpi4py-mpich
Requires:       mpich
Requires:       %{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-mpich}

%description -n python3-%{name}-mpich
%{_description}

%if %{with_py2}
%package -n python2-%{name}-mpich
Summary:        Python2 support for %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  python2-mpi4py-mpich
Requires:       python2-mpi4py-mpich
Requires:       mpich
Requires:       %{name}-common = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}-mpich}

%description -n python2-%{name}-mpich
%{_description}
%endif
%endif

%prep
%autosetup -c -n %{name}-%{commit}

cp %{name}-%{commit}/LICENSE .
cp %{name}-%{commit}/README .

%if %{with_py2}
    cp -a %{name}-%{commit} %{name}-%{commit}-py2
%endif

%if %{with_mpich}
    %if %{with_py2}
        cp -a %{name}-%{commit} %{name}-%{commit}-mpich-py2
    %endif
    cp -a %{name}-%{commit} %{name}-%{commit}-mpich
%endif

%if %{with_openmpi}
    %if %{with_py2}
        cp -a %{name}-%{commit} %{name}-%{commit}-openmpi-py2
    %endif
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
%if %{with_mpich}
%{_mpich_load}
MPI_CXX="mpicxx"
MPI_VARIANT="mpich"

%if %{with_py2}
MPI_COMPILE_TYPE="-mpich-py2"
PYTHON_BIN="%{__python2}"
%{do_build}
%endif


MPI_COMPILE_TYPE="-mpich"
PYTHON_VERSION=3
PYTHON_BIN="%{__python3}"
%{do_build}

%{_mpich_unload}
%endif

# Openmpi
%if %{with_openmpi}
%{_openmpi_load}
MPI_VARIANT="ompi"
MPI_CXX="mpicxx"

%if %{with_py2}
MPI_COMPILE_TYPE="-openmpi-py2"
PYTHON_VERSION=2
PYTHON_BIN="%{__python2}"
%{do_build}
%endif


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
%if %{with_mpich}
%{_mpich_load}
%if %{with_py2}
MPI_COMPILE_TYPE="-mpich-py2"
%{do_install}
%endif


MPI_COMPILE_TYPE="-mpich"
%{do_install}
%{_mpich_unload}
%endif

# Openmpi
%if %{with_openmpi}
%{_openmpi_load}
%if %{with_py2}
MPI_COMPILE_TYPE="-openmpi-py2"
%{do_install}
%endif


MPI_COMPILE_TYPE="-openmpi"
%{do_install}
%{_openmpi_unload}
%endif

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets


%files
%license LICENSE
%doc README

%if %{with_mpich}
%files mpich
%{_libdir}/mpich/bin/%{lname}
%{_libdir}/mpich/bin/%{lname}_tests.sh
%{_libdir}/mpich/bin/%{lname}run
%{_libdir}/mpich/lib/libmusic-c.so.1
%{_libdir}/mpich/lib/libmusic-c.so.1.0.0

%files mpich-devel
%{_includedir}/mpich*/%{name}
%{_includedir}/mpich*/%{name}*.*
%{_includedir}/mpich*/predict_rank-c.h
%{_libdir}/mpich/lib/libmusic-c.so

%files -n python3-%{name}-mpich
# %{_libdir}/mpich/lib/%{name}.so.*

%if %{with_py2}
%files -n python2-%{name}-mpich
# %{_libdir}/mpich/lib/libpy2neurosim*.so.*
# %{_libdir}/mpich/lib/libpyneurosim*.so.*
%endif
%endif

%if %{with_openmpi}
%files openmpi
# %{_libdir}/openmpi/lib/%{name}.so.*

%files openmpi-devel
# %{_includedir}/openmpi*/neurosim
# %{_libdir}/openmpi/lib/*.so

%files -n python3-%{name}-openmpi
# %{_libdir}/openmpi/lib/libpy3neurosim*.so.*

%if %{with_py2}
%files -n python2-%{name}-openmpi
# %{_libdir}/openmpi/lib/libpy2neurosim*.so.*
# %{_libdir}/openmpi/lib/libpyneurosim*.so.*
%endif
%endif

%changelog
* Sat Oct 20 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-1.20181020gita77e5787
- Remove non MPI packages
- Use macros
- Put common files into separate sub package
- Correct autosetup usage
- Initial build
