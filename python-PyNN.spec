# Note that since it builds nest extensions, this package is NOT noarch

# There does not seem to be a way to install py2 and py3 versions in parallel,
# especially because of the nest exteionsions. So we only provide py3
# https://github.com/NeuralEnsemble/PyNN/issues/615

# Since nest-config varies for these environments
# Does not affect brian, which is MPI free
# Also no brian mpich/openmpi sub packages for this reason
%bcond_without mpich
%bcond_with openmpi

# Tests
%bcond_with tests

# With nest extensions
# https://github.com/NeuralEnsemble/PyNN/issues/615
# Are nest extensions python version independent?
# NEST doesn't do 32bit, so
# Will be fixed in next NEST release
%ifarch armv7hl || %ifarch i686
%bcond_with nest
# without the nest bits, no compilation, no debuginfo
# I don't think we can make the package noarch, can we?
%global debug_package %{nil}
%else
%bcond_without nest
%endif

# Disabled until NEURON is packaged
%bcond_with neuron

# We packaged brian2, the newest version, but PyNN works only with brian1
# http://neuralensemble.org/docs/PyNN/installation.html?highlight=brian#installing-brian
# brian v1 is python2 only, so we cannot support it until PyNN is updated to support brian2.
%bcond_with brian

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
Version:        0.9.3
Release:        1%{?dist}
Summary:        A package for simulator-independent specification of neuronal network models

License:        CeCILL
URL:            http://neuralensemble.org/%{pypi_name}/
Source0:        %pypi_source %{pypi_name}
# Disable pynn's way of building extensions
# We do it ourselves
Patch0:         %{pypi_name}-0.9.3-disable-extensions-build.patch

%if %{with nest}
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gsl-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  libtool-ltdl-devel
%endif


%if %{with mpich} || %{with openmpi}
BuildRequires:  rpm-mpi-hooks
%endif

%if %{with mpich}
BuildRequires:  mpich-devel
%endif

%if %{with openmpi}
BuildRequires:  openmpi-devel
%endif

%{?python_enable_dependency_generator}

%description
%{desc}

%package doc
Summary:        %{summary}
BuildArch:      noarch
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist jinja2}

%description doc
Documentation for %{name}.

%package -n python3-%{pypi_name}-common
Summary:        %{summary}
BuildArch:      noarch
BuildRequires:  python3-devel

%description -n python3-%{pypi_name}-common
Common files for python3-%{pypi_name}.

%{?python_provide:%python_provide python3-%{pypi_name}-common}

%if %{with nest}
%package -n python3-%{pypi_name}-nest
Summary:        %{summary}
BuildRequires:  nest
BuildRequires:  nest-headers
BuildRequires:  libneurosim-devel
Requires:     %{py3_dist pynest}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-nest
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-nest}

%package -n python3-%{pypi_name}-nest-devel
Summary:        %{summary}

%description -n python3-%{pypi_name}-nest-devel
Development %{pypi_name} files for the NEST simulator.
%endif

%if %{with neuron}
%package -n python3-%{pypi_name}-neuron
Summary:        %{summary}
BuildRequires:  neuron
Requires:     %{py3_dist neuron}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-neuron
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-neuron}
%endif

%if %{with brian}
%package -n python3-%{pypi_name}-brian
Summary:      %{summary}
BuildArch:      noarch
Requires:     %{py3_dist brian2}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-brian
%{pypi_name} files for the Brian simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-brian}
%endif

%package -n python3-%{pypi_name}-nineml
Summary:      %{summary}
BuildArch:      noarch
Requires:     %{py3_dist nineml}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-nineml
%{pypi_name} files for NineML.

%{?python_provide:%python_provide python3-%{pypi_name}-nineml}

# mpich
%if %{with mpich}
%if %{with nest}
%package -n python3-%{pypi_name}-nest-mpich
Summary:        %{summary}
BuildRequires:  nest-mpich
BuildRequires:  nest-mpich-headers
BuildRequires:  libneurosim-mpich-devel
Requires:     python3-nest-mpich
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-nest-mpich
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-nest-mpich}

%package -n python3-%{pypi_name}-nest-devel-mpich
Summary:        %{summary}

%description -n python3-%{pypi_name}-nest-devel-mpich
Development %{pypi_name} files for the NEST simulator.
%endif

%if %{with neuron}
%package -n python3-%{pypi_name}-neuron-mpich
Summary:        %{summary}
BuildRequires:  neuron
Requires:     %{py3_dist neuron}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-neuron-mpich
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-neuron-mpich}
%endif

%endif # mpich

# openmpi
%if %{with openmpi}
%if %{with nest}
%package -n python3-%{pypi_name}-nest-openmpi
Summary:        %{summary}
BuildRequires:  nest-openmpi
BuildRequires:  nest-openmpi-headers
BuildRequires:  libneurosim-openmpi-devel
Requires:     python3-nest-openmpi
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-nest-openmpi
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-nest-openmpi}

%package -n python3-%{pypi_name}-nest-devel-openmpi
Summary:        %{summary}

%description -n python3-%{pypi_name}-nest-devel-openmpi
Development %{pypi_name} files for the NEST simulator.
%endif

%if %{with neuron}
%package -n python3-%{pypi_name}-neuron-openmpi
Summary:        %{summary}
BuildRequires:  neuron
Requires:     %{py3_dist neuron}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-neuron-openmpi
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-neuron-openmpi}
%endif

%endif # openmpi

%prep
# Different copies for mpich and openmpi and serial
%autosetup -c -n %{pypi_name}-%{version} -N
rm -rfv %{pypi_name}-%{version}/%{mod_name}.egg-info

cp %{pypi_name}-%{version}/README.rst .
cp %{pypi_name}-%{version}/LICENSE .
cp %{pypi_name}-%{version}/AUTHORS .
cp %{pypi_name}-%{version}/changelog .

# We'll be able to drop these soon as the different packages are made available
# Remove nest bits
%if !%{with nest}
sed -i "s/'pyNN.nest.standardmodels',//" %{pypi_name}-%{version}/setup.py
sed -i "s/'pyNN.nest',//" %{pypi_name}-%{version}/setup.py
sed -i '/nest\/extensions/ d' %{pypi_name}-%{version}/setup.py
rm %{pypi_name}-%{version}/pyNN/nest -rf
%endif

# Remove neuron bits
%if !%{with neuron}
sed -i "s/'pyNN.neuron.standardmodels',//" %{pypi_name}-%{version}/setup.py
sed -i "s/'pyNN.neuron',//" %{pypi_name}-%{version}/setup.py
sed -i "s|'neuron/nmodl.*,$||" %{pypi_name}-%{version}/setup.py
rm -rf %{pypi_name}-%{version}/pyNN/neuron
%endif

# Remove brian bits
%if !%{with brian}
sed -i "s/'pyNN.brian.standardmodels',//" %{pypi_name}-%{version}/setup.py
sed -i "s/'pyNN.brian',//" %{pypi_name}-%{version}/setup.py
rm %{pypi_name}-%{version}/pyNN/brian -rf
%endif


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

%if %{with nest}
    pushd %{mod_name}/nest/extensions || exit 1
        %make_install
    popd
%endif

popd
}

PKG_VARIANT=""
MPI3_SITEARCH=%{python3_sitelib}
%{install_pynn}

%if %{with mpich}
%{_mpich_load}

PKG_VARIANT="-mpich"
MPI3_SITEARCH=$MPI_PYTHON3_SITEARCH
%{install_pynn}

%{_mpich_unload}
%endif # mpich end

%if %{with openmpi}
%{_openmpi_load}

PKG_VARIANT="-openmpi"
MPI3_SITEARCH=$MPI_PYTHON3_SITEARCH
%{install_pynn}

%{_openmpi_unload}
%endif # openmpi end

%check
%if %{with tests}
pushd %{pypi_name}-%{version}
    %{__python3} setup.py test
popd

%if %{with mpich}
%{_mpich_load}
pushd %{pypi_name}-%{version}-%{mpich}
    %{__python3} setup.py test
popd
%{_mpich_unload}
%endif # mpich end

%if %{with openmpi}
%{_openmpi_load}
pushd %{pypi_name}-%{version}-%{openmpi}
    %{__python3} setup.py test
popd
%{_openmpi_unload}
%endif # openmpi start

%endif # tests end


%files doc
%license LICENSE
%doc %{pypi_name}-%{version}/examples
%if %{with docs}
%doc %{pypi_name}-%{version}/html
%endif

%files -n python3-%{pypi_name}-common
%license LICENSE
%doc README.rst AUTHORS changelog
%{python3_sitelib}/%{pypi_name}-%{version}-py3.?.egg-info
%dir %{python3_sitelib}/%{mod_name}
%{python3_sitelib}/%{mod_name}/*py
%{python3_sitelib}/%{mod_name}/common
%{python3_sitelib}/%{mod_name}/descriptions
%{python3_sitelib}/%{mod_name}/utility
%{python3_sitelib}/%{mod_name}/standardmodels
%{python3_sitelib}/%{mod_name}/recording
%{python3_sitelib}/%{mod_name}/neuroml
%{python3_sitelib}/%{mod_name}/mock
%{python3_sitelib}/%{mod_name}/__pycache__

%if %{with nest}
%files -n python3-%{pypi_name}-nest
%dir %{python3_sitelib}/%{mod_name}/nest
%{python3_sitelib}/%{mod_name}/nest/*py
%{python3_sitelib}/%{mod_name}/nest/standardmodels
%{python3_sitelib}/%{mod_name}/nest/__pycache__
%{_libdir}/nest/pynn_extensions.so
%{_libdir}/nest/libpynn_extensions.so
%{_datadir}/nest/sli/pynn_extensions-init.sli

%files -n python3-%{pypi_name}-nest-devel
%{_includedir}/pynn_extensions.h
%{python3_sitelib}/%{mod_name}/nest/extensions
%endif # nest

%if %{with neuron}
%files -n python3-%{pypi_name}-neuron
%{python3_sitelib}/%{mod_name}/neuron
# nmodl things go here
%endif # neuron

%if %{with brian}
%files -n python3-%{pypi_name}-brian
%{python3_sitelib}/%{mod_name}/brian
%endif

%files -n python3-%{pypi_name}-nineml
%{python3_sitelib}/%{mod_name}/nineml

# mpich
%if %{with mpich}
%if %{with nest}
%files -n python3-%{pypi_name}-nest-mpich
# nest extensions go here
%endif # nest

%if %{with neuron}
%files -n python3-%{pypi_name}-neuron-mpich
# nmodl bits go here
%endif # neuron

%endif # mpich

# openmpi
%if %{with openmpi}
%if %{with nest}
%files -n python3-%{pypi_name}-nest-openmpi
# nest extensions go here
%endif # nest

%if %{with neuron}
%files -n python3-%{pypi_name}-neuron-openmpi
# nmodl bits go here
%endif # neuron

%endif # openmpi

%changelog
* Thu Dec 06 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.3-1
- Initial build
