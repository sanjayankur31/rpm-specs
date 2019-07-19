# MUSIC depends on MPI for communication, so a non-MPI version is not being
# built.
# https://github.com/INCF/MUSIC/issues/55


%global commit a78a8e2c90b07274db94265db75c320dbb01f9fb
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# For debugging
%bcond_without mpich
%bcond_without openmpi

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
Version:        1.1.15
Release:        2.20190717git%{shortcommit}%{?dist}
Summary:        The MUltiSimulation Coordinator

License:        GPLv3+
URL:            https://github.com/INCF/%{name}/
Source0:        https://github.com/INCF/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:         0001-Enable-testsuite-and-extras-for-mpich2.patch

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  freeglut-devel
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  patch
BuildRequires:  python3-devel
BuildRequires:  python3-Cython
# Currently bundles a modified version of rudeconfig which cannot be unbundled
# until MUSIC upstream sends their changes upstream to rudeconfig.
# https://github.com/INCF/MUSIC/issues/56
# BuildRequires:  rudeconfig-devel

%description %_description

%if %{with mpich}
%package mpich
Summary:        %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description mpich %_description

%package mpich-devel
Summary:        %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
Requires:       mpich
Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}

%description mpich-devel
Development files for %{name} built with MPICH.

%package -n python3-%{name}-mpich
Summary:        Python3 support for %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  python3-mpi4py-mpich
Requires:       python3-mpi4py-mpich
Requires:       mpich
Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-mpich}

%description -n python3-%{name}-mpich %_description
%endif

%if %{with openmpi}
%package openmpi
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description openmpi %_description

%package openmpi-devel
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
Requires:       openmpi
Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-devel
Development files for %{name} built with MPICH.

%package -n python3-%{name}-openmpi
Summary:        Python3 support for %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  python3-mpi4py-openmpi
Requires:       python3-mpi4py-openmpi
Requires:       openmpi
Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}-openmpi}

%description -n python3-%{name}-openmpi %_description
%endif

%prep
%autosetup -c -n %{name}-%{commit} -N
# Unable to use autosetup directly because we need three copies of the source
# in here now
# Apply patches
pushd %{name}-%{commit}
%patch -p1 -P 0
# on Fedora, we have mpichversion, not mpich2version
sed -i 's|mpich2version|mpichversion|' configure.ac
popd

cp %{name}-%{commit}/LICENSE .
cp %{name}-%{commit}/README .

%if %{with mpich}
    cp -a %{name}-%{commit} %{name}-%{commit}-mpich
%endif

%if %{with openmpi}
    cp -a %{name}-%{commit} %{name}-%{commit}-openmpi
%endif

%build

%global do_build %{expand:
echo "** BUILDING $MPI_COMPILE_TYPE **"
pushd %{name}-%{commit}$MPI_COMPILE_TYPE
./autogen.sh &&
%{set_build_flags}
MPI_CXXFLAGS="$CXXFLAGS $(pkg-config --cflags $MPI_VARIANT)"
MPI_CFLAGS="$CFLAGS $(pkg-config --cflags $MPI_VARIANT)"
MPI_LDFLAGS="$LDFLAGS $(pkg-config --libs $MPI_VARIANT)"
./configure MPI_CXXFLAGS="$MPI_CXXFLAGS" MPI_CFLAGS="$MPI_CFLAGS" MPI_LDFLAGS="$MPI_LDFLAGS" PYTHON="$PYTHON_BIN" \\\
--disable-static \\\
--prefix=$MPI_HOME \\\
--libdir=$MPI_LIB \\\
--includedir=$MPI_INCLUDE \\\
--bindir=$MPI_BIN \\\
--mandir=$MPI_MAN &&
%make_build &&
popd
}


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
MPI_VARIANT="ompi-cxx"

MPI_COMPILE_TYPE="-openmpi"
PYTHON_VERSION=3
PYTHON_BIN="%{__python3}"
%{do_build}
%{_openmpi_unload}
%endif

%install
%global do_install %{expand:
%make_install -C %{name}-%{commit}$MPI_COMPILE_TYPE
mv $RPM_BUILD_ROOT/$MPI_HOME/lib/%{lname}-%{version}/* $RPM_BUILD_ROOT/$MPI_BIN/ -v && rm -vrf $RPM_BUILD_ROOT/$MPI_HOME/lib/%{lname}-%{version}
for f in contsink eventcounter eventgenerator eventlogger eventselect eventsink eventsource messagesource music viewevents waveconsumer waveproducer clocksource constsource contdelay eventdelay launchtest multiport musicrun test_ag
do
    if [ -e  "$RPM_BUILD_ROOT/$MPI_BIN/$f" ]; then
        echo "Renaming $f"
        mv "$RPM_BUILD_ROOT/$MPI_BIN/$f" "$RPM_BUILD_ROOT/$MPI_BIN/$f$MPI_SUFFIX" -v
    fi
done
# One separately
mv "$RPM_BUILD_ROOT/$MPI_BIN/music_tests.sh" "$RPM_BUILD_ROOT/$MPI_BIN/music_tests$MPI_SUFFIX.sh" -v
}


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
%{_libdir}/mpich/bin/contsink_mpich
%{_libdir}/mpich/bin/eventcounter_mpich
%{_libdir}/mpich/bin/eventgenerator_mpich
%{_libdir}/mpich/bin/eventlogger_mpich
%{_libdir}/mpich/bin/eventselect_mpich
%{_libdir}/mpich/bin/eventsink_mpich
%{_libdir}/mpich/bin/eventsource_mpich
%{_libdir}/mpich/bin/messagesource_mpich
%{_libdir}/mpich/bin/music_mpich
%{_libdir}/mpich/bin/viewevents_mpich
%{_libdir}/mpich/bin/waveconsumer_mpich
%{_libdir}/mpich/bin/waveproducer_mpich
%{_libdir}/mpich/bin/constsource_mpich
%{_libdir}/mpich/bin/clocksource_mpich
%{_libdir}/mpich/bin/contdelay_mpich
%{_libdir}/mpich/bin/eventdelay_mpich
%{_libdir}/mpich/bin/launchtest_mpich
%{_libdir}/mpich/bin/multiport_mpich
%{_libdir}/mpich/bin/music_tests_mpich.sh
%{_libdir}/mpich/bin/musicrun_mpich
%{_libdir}/mpich/bin/test_ag_mpich
%{_libdir}/mpich/lib/libmusic.so.1
%{_libdir}/mpich/lib/libmusic-c.so.1
%{_libdir}/mpich/lib/libmusic.so.1.0.0
%{_libdir}/mpich/lib/libmusic-c.so.1.0.0
%{_libdir}/mpich/share/%{lname}*
%{_mandir}/mpich-%{_arch}/man1/*

%files mpich-devel
%{_includedir}/mpich*/%{lname}
%{_includedir}/mpich*/%{lname}*.*
%{_includedir}/mpich*/predict_rank-c.h
%{_libdir}/mpich/lib/libmusic.so
%{_libdir}/mpich/lib/libmusic-c.so

%files -n python3-%{name}-mpich
%{_libdir}/mpich/lib/python%{python3_version}/site-packages/%{lname}
%{_libdir}/mpich/%{_lib}/python%{python3_version}/site-packages/%{lname}
%{_libdir}/mpich/%{_lib}/python%{python3_version}/site-packages/%{lname}-%{version}-py%{python3_version}.egg-info
%endif

%if %{with openmpi}
%files openmpi
%{_libdir}/openmpi/bin/contsink_openmpi
%{_libdir}/openmpi/bin/eventcounter_openmpi
%{_libdir}/openmpi/bin/eventgenerator_openmpi
%{_libdir}/openmpi/bin/eventlogger_openmpi
%{_libdir}/openmpi/bin/eventselect_openmpi
%{_libdir}/openmpi/bin/eventsink_openmpi
%{_libdir}/openmpi/bin/eventsource_openmpi
%{_libdir}/openmpi/bin/messagesource_openmpi
%{_libdir}/openmpi/bin/music_openmpi
%{_libdir}/openmpi/bin/viewevents_openmpi
%{_libdir}/openmpi/bin/waveconsumer_openmpi
%{_libdir}/openmpi/bin/waveproducer_openmpi
%{_libdir}/openmpi/bin/constsource_openmpi
%{_libdir}/openmpi/bin/clocksource_openmpi
%{_libdir}/openmpi/bin/contdelay_openmpi
%{_libdir}/openmpi/bin/eventdelay_openmpi
%{_libdir}/openmpi/bin/launchtest_openmpi
%{_libdir}/openmpi/bin/multiport_openmpi
%{_libdir}/openmpi/bin/music_tests_openmpi.sh
%{_libdir}/openmpi/bin/musicrun_openmpi
%{_libdir}/openmpi/bin/test_ag_openmpi
%{_libdir}/openmpi/lib/libmusic.so.1
%{_libdir}/openmpi/lib/libmusic-c.so.1
%{_libdir}/openmpi/lib/libmusic.so.1.0.0
%{_libdir}/openmpi/lib/libmusic-c.so.1.0.0
%{_libdir}/openmpi/share/%{lname}*
%{_mandir}/openmpi-%{_arch}/man1/*

%files openmpi-devel
%{_includedir}/openmpi*/%{lname}
%{_includedir}/openmpi*/%{lname}*.*
%{_includedir}/openmpi*/predict_rank-c.h
%{_libdir}/openmpi/lib/libmusic.so
%{_libdir}/openmpi/lib/libmusic-c.so

%files -n python3-%{name}-openmpi
%{_libdir}/openmpi/lib/python%{python3_version}/site-packages/%{lname}
%{_libdir}/openmpi/%{_lib}/python%{python3_version}/site-packages/%{lname}
%{_libdir}/openmpi/%{_lib}/python%{python3_version}/site-packages/%{lname}-%{version}-py%{python3_version}.egg-info
%endif

%changelog
* Wed Jul 17 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.1.15-2.20190717gita78a8e2
- Bundle rudeconfig
- Remove python 2 subpackage

* Sat Oct 20 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-1.20181020gita77e5787
- Depend on packaged rudeconfig
- Remove non MPI packages
- Use macros
- Put common files into separate sub package
- Correct autosetup usage
- Initial build
