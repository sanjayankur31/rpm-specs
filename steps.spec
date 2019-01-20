# Switch them off if you want
# Best to start with the serial version
%bcond_without mpich
%bcond_without openmpi

Name:           steps
Version:        3.4.1

Release:        1%{?dist}
Summary:        STochastic Engine for Pathway Simulation

License:        GPLv2
URL:            http://steps.sourceforge.net/
Source0:        https://github.com/CNS-OIST/STEPS/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  openblas-devel
# Not yet packaged
BuildRequires:  easyloggingpp-devel
BuildRequires:  gtest-devel
BuildRequires:  petsc-devel
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist Cython}
BuildRequires:  %{py3_dist numpy}


%global _description %{expand:
STEPS is a package for exact stochastic simulation of reaction-diffusion
systems in arbitrarily complex 3D geometries. Our core simulation algorithm is
an implementation of Gillespie's SSA, extended to deal with diffusion of
molecules over the elements of a 3D tetrahedral mesh.

While it was mainly developed for simulating detailed models of neuronal
signaling pathways in dendrites and around synapses, it is a general tool and
can be used for studying any biochemical pathway in which spatial gradients and
morphology are thought to play a role.

STEPS also supports accurate and efficient computational of local membrane
potentials on tetrahedral meshes, with the addition of voltage-gated channels
and currents. Tight integration between the reaction-diffusion calculations and
the tetrahedral mesh potentials allows detailed coupling between molecular
activity and local electrical excitability.

We have implemented STEPS as a set of Python modules, which means STEPS users
can use Python scripts to control all aspects of setting up the model,
generating a mesh, controlling the simulation and generating and analyzing
output. The core computational routines are still implemented as C/C++
extension modules for maximal speed of execution.

STEPS 3.0.0 and above provide early parallel solution for stochastic spatial
reaction-diffusion and electric field simulation.
}

%description
%{_description}

%if %{with openmpi}
%package openmpi
Summary:        %{name} built with openmpi
BuildRequires:  openmpi-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  petsc-openmpi-devel
Requires:       openmpi

%description openmpi
%{_description}
%endif

%if %{with mpich}
%package mpich
Summary:        %{name} built with mpich
BuildRequires:  mpich-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  petsc-mpich-devel
Requires:       mpich

%description mpich
%{_description}

%endif

%prep
# We must create a separate top level directory and then triplicate it so that
# we have two more copies for mpich and openmpi
%autosetup -c -n %{name}-%{version}

# Copy it here for convenience
cp %{name}-%{version}/LICENSE . -v

# Tweaks in the original version before we copy it over
pushd %{name}-%{version}
# Tweaks
popd

%if %{with mpich}
    cp -a %{name}-%{version} %{name}-%{version}-mpich
%endif

%if %{with openmpi}
    cp -a %{name}-%{version} %{name}-%{version}-openmpi
%endif

%build
# Best to use && so that if anything in the chain fails, the build also fails
# straight away
%global do_cmake_config %{expand: \
echo
echo "*** BUILDING %{name}-%{version}$MPI_COMPILE_TYPE ***"
echo
%set_build_flags
pushd %{name}-%{version}$MPI_COMPILE_TYPE  &&
    cmake \\\
        -DCMAKE_C_FLAGS_RELEASE:STRING="-DNDEBUG" \\\
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="-DNDEBUG" \\\
        -DCMAKE_Fortran_FLAGS_RELEASE:STRING="-DNDEBUG" \\\
        -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \\\
        -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \\\
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \\\
        -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \\\
        -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \\\
        -DCMAKE_SKIP_RPATH:BOOL=ON \\\
        -Dwith-mpi:BOOL=$MPI_YES \\\
        -Dwith-gsl:BOOL=ON \\\
        -DCMAKE_INSTALL_PREFIX:PATH=$MPI_HOME \\\
        -DBUILD_SHARED_LIBS:BOOL=ON \\\
%if "%{_lib}" == "lib64"
        -DLIB_SUFFIX=64 &&
%else
        -DLIB_SUFFIX=""  &&
%endif
popd || exit -1;
}

%global do_make_build %{expand: \
    make %{?_smp_mflags} -C %{name}-%{version}$MPI_COMPILE_TYPE || exit -1
}

# Build serial version, dummy arguments
export MPI_COMPILER=serial
export MPI_SUFFIX=""
export MPI_HOME=%{_prefix}
export MPI_BIN=%{_bindir}
export MPI_YES=OFF
%{do_cmake_config}
%{do_make_build}


# Build mpich version
%if %{with mpich}
%{_mpich_load}
export CC=mpicc
export CXX=mpicxx
export FC=mpif90
export F77=mpif77
export MPI_YES=ON
export MPI_COMPILE_TYPE="-mpich"
%{do_cmake_config}
%{do_make_build}

%{_mpich_unload}
%endif

# Build OpenMPI version
%if %{with openmpi}
%{_openmpi_load}
export CC=mpicc
export CXX=mpicxx
export FC=mpif90
export F77=mpif77
export MPI_YES=ON
# Python 3
export MPI_COMPILE_TYPE="-openmpi"
%{do_cmake_config}
%{do_make_build}

%{_openmpi_unload}
%endif

%install
# Install everything
%global do_install %{expand:
echo
echo "*** INSTALLING %{name}-%{version}$MPI_COMPILE_TYPE ***"
echo
    make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" CPPROG="cp -p" -C %{name}-%{version}$MPI_COMPILE_TYPE || exit -1
}

# install serial version
export MPI_SUFFIX=""
export MPI_HOME=%{_prefix}
export MPI_BIN=%{_bindir}
export MPI_YES=OFF
export MPI_COMPILE_TYPE=""
%{do_install}

# Install MPICH version
%if %{with mpich}
%{_mpich_load}
export MPI_COMPILE_TYPE="-mpich"
%{do_install}

# Place in correct mpi libdir
# Tweaks like this may be needed
%if %{_lib} == lib64
    mv -v $RPM_BUILD_ROOT/%{_libdir}/mpich/lib64 $RPM_BUILD_ROOT/$MPI_LIB/
%endif
%{_mpich_unload}
%endif

# Install OpenMPI version
%if %{with openmpi}
%{_openmpi_load}
export MPI_COMPILE_TYPE="-openmpi"
%{do_install}

# Correct location
# May be needed sometimes
%if %{_lib} == lib64
    mv -v $RPM_BUILD_ROOT/%{_libdir}/openmpi/lib64 $RPM_BUILD_ROOT/$MPI_LIB/
%endif
%{_openmpi_unload}
%endif


%files
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/...

%if %{with mpich}
%files mpich
%license LICENSE
# Correct file locations
%{_libdir}/mpich/bin/%{name}
%{_libdir}/mpich/lib/...
%endif

%if %{with openmpi}
%files openmpi
%license LICENSE
# Correct file locations
%{_libdir}/openmpi/bin/%{name}
%{_libdir}/openmpi/lib/..
%endif

%changelog
* Sun Jan 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.4.1-1
- Initial package
