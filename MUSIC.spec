%global commit a77e57878158b36401c0977702c1386ba01db118
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global with_mpich 0
%global with_openmpi 0
%global with_py2 1

%global _description\
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
Release:        0.20181013git%{shortcommit}%{?dist}
Summary:        MUSIC, the MUltiSimulation Coordinator

License:        GPLv3+
URL:            https://github.com/INCF/%{name}/
Source0:        https://github.com/INCF/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  freeglut-devel

%description
%{_description}

%if %{with_py2}
BuildRequires:  python2-devel
%endif


%description
%{_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n python3-%{name}
Summary:        Python3 support for %{name}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
%{_description}

%if %{with_py2}
%package -n python2-%{name}
Summary:        Python2 support for %{name}
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
%{_description}
%endif

%if %{with_openmpi}
%package openmpi
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
Requires:       %{name}-openmpi-common = %{version}-%{release}
%description openmpi
%{_description}

%package openmpi-devel
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
Requires:       %{name}-openmpi-common = %{version}-%{release}
%description openmpi-devel
%{_description}

%package -n python3-%{name}-openmpi
Summary:        Python3 support for %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
%{?python_provide:%python_provide python3-%{name}-openmpi}

%description -n python3-%{name}-openmpi
%{_description}

%if %{with_py2}
%package -n python2-%{name}-openmpi
Summary:        Python2 support for %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
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
Requires:       %{name}-mpich-common = %{version}-%{release}

%description mpich
%{_description}

%package mpich-devel
Summary:        %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich

%description mpich-devel
%{_description}

%package -n python3-%{name}-mpich
Summary:        Python3 support for %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich
%{?python_provide:%python_provide python3-%{name}-mpich}

%description -n python3-%{name}-mpich
%{_description}

%if %{with_py2}
%package -n python2-%{name}-mpich
Summary:        Python2 support for %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich
%{?python_provide:%python_provide python2-%{name}-mpich}

%description -n python2-%{name}-mpich
%{_description}
%endif
%endif

%prep
%autosetup -n %{name}-%{commit}

cd ../
cp -a %{name}-%{commit} %{name}-%{commit}-py3


%if %{with_mpich}
    %if %{with_py2}
        cp -a %{name}-%{commit} %{name}-%{commit}-mpich
    %endif
    cp -a %{name}-%{commit}-py3 %{name}-%{commit}-mpich-py3
%endif

%if %{with_openmpi}
    %if %{with_py2}
        cp -a %{name}-%{commit} %{name}-%{commit}-openmpi
    %endif
    cp -a %{name}-%{commit}-py3 %{name}-%{commit}-openmpi-py3
%endif

%build

%global do_build \
pushd %{name}-%{commit}$MPI_COMPILE_TYPE && \
./autogen.sh && \
export CFLAGS="%{optflags}"  \
export CXXFLAGS="%{optflags}"  \
export LDFLAGS="${LDFLAGS:--Wl,-z,relro -specs=/usr/lib/rpm/redhat/redhat-hardened-ld}"  \
./configure MPI_CXXFLAGS="$FLAGS" MPI_CFLAGS="$FLAGS" MPI_LDFLAGS="$LDFLAGS" \\\
--disable-static \\\
--with-python=$PYTHON_VERSION \\\
--prefix=$MPI_HOME \\\
--libdir=$MPI_LIB \\\
--includedir=$MPI_INCLUDE \\\
--bindir=$MPI_BIN \\\
%if "$MPI_YES" == "no" \
--disable-mpi \\\
%endif \
--mandir=$MPI_MAN && \
%make_build && \
popd || exit -1


cd ../

%if %{with_py2}
MPI_COMPILE_TYPE=""
PYTHON_VERSION=2
MPI_YES="no"
MPI_HOME=%{_prefix}
MPI_LIB=%{_libdir}
MPI_INCLUDE=%{_includedir}
MPI_BIN=%{_bindir}
MPI_MAN=%{_mandir}
MPI_CXX=""
FLAGS="%{optflags}"
%{do_build}
%endif


MPI_COMPILE_TYPE="-py3"
PYTHON_VERSION=3
MPI_YES="no"
MPI_HOME=%{_prefix}
MPI_LIB=%{_libdir}
MPI_INCLUDE=%{_includedir}
MPI_BIN=%{_bindir}
MPI_MAN=%{_mandir}
MPI_CXX=""
FLAGS="%{optflags}"
%{do_build}

# Mpich
%if %{with_mpich}
%{_mpich_load}
%if %{with_py2}
MPI_COMPILE_TYPE="-mpich"
PYTHON_VERSION=2
MPI_YES="yes"
MPI_CXX="mpicxx"
FLAGS=""
%{do_build}
%endif


MPI_COMPILE_TYPE="-mpich-py3"
PYTHON_VERSION=3
MPI_YES="yes"
MPI_CXX="mpicxx"
FLAGS=""
%{do_build}

%{_mpich_unload}
%endif

# Openmpi
%if %{with_openmpi}
%{_openmpi_load}
%if %{with_py2}
MPI_COMPILE_TYPE="-openmpi"
PYTHON_VERSION=2
MPI_YES="yes"
MPI_CXX="mpicxx"
FLAGS=""
%{do_build}
%endif


MPI_COMPILE_TYPE="-openmpi-py3"
PYTHON_VERSION=3
MPI_YES="yes"
MPI_CXX="mpicxx"
FLAGS=""
%{do_build}
%{_openmpi_unload}
%endif

%install
cd ../

%global do_install \
%make_install -C %{name}-%{commit}$MPI_COMPILE_TYPE || exit -1

%if %{with_py2}
MPI_COMPILE_TYPE=""
PYTHON_VERSION=2
%{do_install}
%endif


MPI_COMPILE_TYPE="-py3"
PYTHON_VERSION=3
%{do_install}

# Mpich
%if %{with_mpich}
%{_mpich_load}
%if %{with_py2}
MPI_COMPILE_TYPE="-mpich"
PYTHON_VERSION=2
%{do_install}
%endif


MPI_COMPILE_TYPE="-mpich-py3"
PYTHON_VERSION=3
%{do_install}
%{_mpich_unload}
%endif

# Openmpi
%if %{with_openmpi}
%{_openmpi_load}
%if %{with_py2}
MPI_COMPILE_TYPE="-openmpi"
PYTHON_VERSION=2
%{do_install}
%endif


MPI_COMPILE_TYPE="-openmpi-py3"
PYTHON_VERSION=3
%{do_install}
%{_openmpi_unload}
%endif

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING
%doc README
# %{_libdir}/%{name}.so.*

%files devel
# %{_includedir}/*
# %{_libdir}/*.so

%files -n python3-%{name}
# %{_libdir}/libpy3neurosim*.so.*

%if %{with_py2}
%files -n python2-%{name}
# %{_libdir}/libpy2neurosim*.so.*
# %{_libdir}/libpyneurosim*.so.*
%endif

%if %{with_mpich}
%files mpich
%license COPYING
%doc README
# %{_libdir}/mpich/lib/%{name}.so.*

%files mpich-devel
# %{_includedir}/mpich*/neurosim
# %{_libdir}/mpich/lib/*.so

%files -n python3-%{name}-mpich
# %{_libdir}/mpich/lib/libpy3neurosim*.so.*

%if %{with_py2}
%files -n python2-%{name}-mpich
# %{_libdir}/mpich/lib/libpy2neurosim*.so.*
# %{_libdir}/mpich/lib/libpyneurosim*.so.*
%endif
%endif

%if %{with_openmpi}
%files openmpi
%license COPYING
%doc README
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
* Sat Oct 13 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.20181013.gita77e5787
- Initial build
