# Does not yet support neuron which is not packaged yet

# Not noarch since it depends on arch versions of NEST/Brian and so on

# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# Since nest-config varies for these environments
# Does not affect brian, which is MPI free
%bcond_with mpich
%bcond_with openmpi

# Tests
%bcond_with tests

# Currently doesn't build: issue filed upstream
# https://github.com/NeuralEnsemble/PyNN/issues/611
%bcond_with nest

# Neuron has not yet been packaged
%bcond_with neuron

%bcond_with docs

%global pypi_name PyNN
%global mod_name pyNN

%global desc %{expand: \
PyNN (pronounced ‘pine’) is a simulator-independent language for building
neuronal network models.

In other words, you can write the code for a model once, using the PyNN API and
the Python programming language, and then run it without modification on any
simulator that PyNN supports (currently NEURON, NEST and Brian) and on a number
of neuromorphic hardware systems.

The PyNN API aims to support modelling at a high-level of abstraction
(populations of neurons, layers, columns and the connections between them)
while still allowing access to the details of individual neurons and synapses
when required. PyNN provides a library of standard neuron, synapse and synaptic
plasticity models, which have been verified to work the same on the different
supported simulators. PyNN also provides a set of commonly-used connectivity
algorithms (e.g. all-to-all, random, distance-dependent, small-world) but makes
it easy to provide your own connectivity in a simulator-independent way.

Even if you don’t wish to run simulations on multiple simulators, you may
benefit from writing your simulation code using PyNN’s powerful, high-level
interface. In this case, you can use any neuron or synapse model supported by
your simulator, and are not restricted to the standard models.

Documentation: http://neuralensemble.org/docs/PyNN/
Mailing list: https://groups.google.com/forum/?fromgroups#!forum/neuralensemble

This package supports the NEST and Brian simulators.}

Name:           python-%{pypi_name}
Version:        0.9.2
Release:        1%{?dist}
Summary:        A package for simulator-independent specification of neuronal network models

License:        CeCILL
URL:            http://neuralensemble.org/%{pypi_name}/
Source0:        %pypi_source %{pypi_name}
Patch0:         %{pypi_name}-0.9.2-disable-extensions.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gsl-devel

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  nest
BuildRequires:  nest-headers
Recommends:     %{py2_dist nest}
Recommends:     %{py2_dist brain}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  nest
BuildRequires:  nest-headers
Recommends:     %{py3_dist nest}
Recommends:     %{py3_dist brain}
%if %{with docs}
BuildRequires:  %{py3_dist sphinx}
%endif
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{desc}

%package doc
Summary:        %{summary}
BuildArch:      noarch

%description doc
Documentation for %{name}.

%if %{with mpich}
%if %{with py2}
%package -n python2-%{pypi_name}-mpich
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  nest-mpich
BuildRequires:  nest-mpich-headers
Requires:       %{py2_dist mpi4py-mpich}
Recommends:     %{py2_dist nest-mpich}
Recommends:     %{py2_dist brain}
%{?python_provide:%python_provide python2-%{pypi_name}-mpich}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}-mpich
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  nest-mpich
BuildRequires:  nest-mpich-headers
Requires:       %{py3_dist mpi4py-mpich}
Recommends:     %{py3_dist nest-mpich}
Recommends:     %{py3_dist brain}
%{?python_provide:%python_provide python3-%{pypi_name}-mpich}

%description -n python3-%{pypi_name}-mpich
%{desc}
%endif

%if %{with openmpi}
%if %{with py2}
%package -n python2-%{pypi_name}-openmpi
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  nest-openmpi
BuildRequires:  nest-openmpi-headers
Requires:       %{py2_dist mpi4py-openmpi}
Recommends:     %{py2_dist nest-openmpi}
Recommends:     %{py2_dist brain}
%{?python_provide:%python_provide python2-%{pypi_name}-openmpi}

%description -n python2-%{pypi_name}
%{desc}
%endif

%package -n python3-%{pypi_name}-openmpi
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  nest-openmpi
BuildRequires:  nest-openmpi-headers
Requires:       %{py3_dist mpi4py-openmpi}
Recommends:     %{py3_dist nest-openmpi}
Recommends:     %{py3_dist brain}
%{?python_provide:%python_provide python3-%{pypi_name}-openmpi}

%description -n python3-%{pypi_name}-openmpi
%{desc}
%endif


%prep
# Different copies for mpich and openmpi and serial
%autosetup -c -n %{pypi_name}-%{version} -N
rm -rf %{pypi_name}-%{version}/%{pypi_name}.egg-info

cp %{pypi_name}-%{version}/README.rst .
cp %{pypi_name}-%{version}/LICENSE .
cp %{pypi_name}-%{version}/AUTHORS .
cp %{pypi_name}-%{version}/changelog .

pushd %{pypi_name}-%{version}
%autopatch -p0
popd

%if %{with mpich}
cp -r %{pypi_name}-%{version} %{pypi_name}-%{version}-mpich
%endif

%if %{with openmpi}
cp -r %{pypi_name}-%{version} %{pypi_name}-%{version}-openmpi
%endif

%build
%global build_pynn %{expand: \
pushd %{pypi_name}-%{version}$PKG_VARIANT
    %py3_build

%if %{with neuron}
    pushd %{mod_name}/neuron/nmodl || exit 1
        %{set_build_flags}
        $MPI_BIN/nrnivmodl
    popd
%endif

%if %{with nest}
    pushd %{mod_name}/nest/extensions || exit 1
        %{set_build_flags}
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
            -DCMAKE_INSTALL_PREFIX:PATH=$MPI_HOME \\\
            -DBUILD_SHARED_LIBS:BOOL=ON \\\
            -Dwith-nest=$MPI_BIN/nest-config \\\
%if "%{_lib}" == "lib64"
            -DLIB_SUFFIX=64  .
%else
            -DLIB_SUFFIX="" .
%endif
        %make_build
    popd
%endif

    %if %{with py2}
        %py2_build
    %endif
popd
}

# serial
PKG_VARIANT=""
MPI_HOME=%{_prefix}
MPI_BIN=%{_bindir}
%{build_pynn}

%if %{with docs}
# Generate docs
pushd %{pypi_name}-%{version}
    sphinx-build-3 doc html
    rm -rf html/.doctrees
    rm -rf html/.buildinfo
popd
%endif

popd

%if %{with mpich}
%{_mpich_load}
NEST_LOC=$MPI_BIN
PKG_VARIANT="-mpich"
%{build_pynn}

%{_mpich_unload}
%endif

%if %{with openmpi}
%{_openmpi_load}
NEST_LOC=$MPI_BIN
PKG_VARIANT="-openmpi"
%{build_pynn}

%{_openmpi_unload}
%endif

%install
%global install_pynn %{expand: \
pushd %{pypi_name}-%{version}$PKG_VARIANT
    %{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT --install-lib=$MPI3_SITEARCH

    pushd %{mod_name}/nest/_build
        %make_install
    popd

    %if %{with py2}
        %{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT --install-lib=$MPI2_SITEARCH
    %endif
popd
}

PKG_VARIANT=""
MPI3_SITEARCH=%{python3_sitearch}
MPI2_SITEARCH=%{python2_sitearch}
%{install_pynn}

%if %{with mpich}
%{_mpich_load}

PKG_VARIANT="-mpich"
MPI3_SITEARCH=$MPI_PYTHON3_SITEARCH
MPI2_SITEARCH=$MPI_PYTHON2_SITEARCH
%{install_pynn}

%{_mpich_unload}
%endif

%if %{with openmpi}
%{_openmpi_load}

PKG_VARIANT="-openmpi"
MPI3_SITEARCH=$MPI_PYTHON3_SITEARCH
MPI2_SITEARCH=$MPI_PYTHON2_SITEARCH
%{install_pynn}

%{_openmpi_unload}
%endif

%check
%if %{with tests}
pushd %{pypi_name}-%{version}
    %{__python3} setup.py test

%if %{with py2}
    %{__python2} setup.py test
%endif
popd

%if %{with mpich}
%{_mpich_load}
pushd %{pypi_name}-%{version}-%{mpich}
    %{__python3} setup.py test

%if %{with py2}
    %{__python2} setup.py test
%endif
popd
%{_mpich_unload}
%endif

%if %{with openmpi}
%{_openmpi_load}
pushd %{pypi_name}-%{version}-%{openmpi}
    %{__python3} setup.py test

%if %{with py2}
    %{__python2} setup.py test
%endif
popd
%{_openmpi_unload}
%endif
%endif


%if %{with py2}
%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst AUTHORS changelog
# %{python2_sitearch}/%{mod_name}-%{version}-py2.?.egg-info
# %{python2_sitearch}/%{mod_name}
%endif

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst AUTHORS changelog
# %{python3_sitearch}/%{mod_name}-%{version}-py3.?.egg-info
# %{python3_sitearch}/%{mod_name}

%files doc
%license LICENSE
%doc %{pypi_name}-%{version}/examples
%if %{with docs}
%doc %{pypi_name}-%{version}/html
%endif

%if %{with mpich}
%if %{with py2}
%files -n python2-%{pypi_name}-mpich
%license LICENSE
%doc README.rst AUTHORS changelog
# %{python2_sitearch}/mpich/%{mod_name}-%{version}-py2.?.egg-info
# %{python2_sitearch}/mpich/%{mod_name}
%endif

%files -n python3-%{pypi_name}-mpich
%license LICENSE
%doc README.rst AUTHORS changelog
# %{python3_sitearch}/mpich/%{mod_name}-%{version}-py3.?.egg-info
# %{python3_sitearch}/mpich/%{mod_name}
%endif

%if %{with openmpi}
%if %{with py2}
%files -n python2-%{pypi_name}-openmpi
%license LICENSE
%doc README.rst AUTHORS changelog
# %{python2_sitearch}/openmpi/%{mod_name}-%{version}-py2.?.egg-info
# %{python2_sitearch}/openmpi/%{mod_name}
%endif

%files -n python3-%{pypi_name}-openmpi
%license LICENSE
%doc README.rst AUTHORS changelog
# %{python3_sitearch}/openmpi/%{mod_name}-%{version}-py3.?.egg-info
# %{python3_sitearch}/openmpi/%{mod_name}
%endif


%changelog
* Sun Nov 25 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.2-1
- Initial build
