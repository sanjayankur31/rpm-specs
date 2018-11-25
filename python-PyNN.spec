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
# Also no brian mpich/openmpi sub packages for this reason
%bcond_with mpich
%bcond_with openmpi

# Tests
%bcond_with tests

# nest extensions don't build: issue filed upstream
# https://github.com/NeuralEnsemble/PyNN/issues/611
%bcond_with nestext

# Neuron has not yet been packaged
%bcond_with neuronext

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

%if %{with nestext}
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gsl-devel
%endif


# If neither nest nor neuron are being built, this is a noarch package
%if !%{with nestext} && !%{with neuronext}
BuildArch:      noarch
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

%if %{with py2}
%package -n python2-%{pypi_name}-common
Summary:        %{summary}
BuildArch:      noarch
BuildRequires:  python2-devel

%description -n python2-%{pypi_name}-common
Common files for python2-%{pypi_name}.

%{?python_provide:%python_provide python2-%{pypi_name}-common}

%package -n python2-%{pypi_name}-nest
Summary:        %{summary}
BuildRequires:  nest
BuildRequires:  nest-headers
Requires:     %{py2_dist nest}
Requires:     python2-%{pypi_name}-common

%description -n python2-%{pypi_name}-nest
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python2-%{pypi_name}-nest}

%package -n python2-%{pypi_name}-neuron
Summary:        %{summary}
%if %{with neuronext}
BuildRequires:  neuron
%endif
Requires:     %{py2_dist neuron}
Requires:     python2-%{pypi_name}-common

%description -n python2-%{pypi_name}-neuron
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python2-%{pypi_name}-neuron}

%package -n python2-%{pypi_name}-brian
Summary:      %{summary}
BuildArch:      noarch
Requires:     %{py2_dist brian}
Requires:     python2-%{pypi_name}-common

%description -n python2-%{pypi_name}-brian
%{pypi_name} files for the Brian simulator.

%{?python_provide:%python_provide python2-%{pypi_name}-brian}

%package -n python2-%{pypi_name}-nineml
Summary:      %{summary}
BuildArch:      noarch
Requires:     %{py2_dist nineml}
Requires:     python2-%{pypi_name}-common

%description -n python2-%{pypi_name}-nineml
%{pypi_name} files for NineML.

%{?python_provide:%python_provide python2-%{pypi_name}-nineml}
%endif # py2

%package -n python3-%{pypi_name}-common
Summary:        %{summary}
BuildArch:      noarch
BuildRequires:  python3-devel

%description -n python3-%{pypi_name}-common
Common files for python3-%{pypi_name}.

%{?python_provide:%python_provide python3-%{pypi_name}-common}

%package -n python3-%{pypi_name}-nest
Summary:        %{summary}
BuildRequires:  nest
BuildRequires:  nest-headers
Requires:     %{py3_dist nest}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-nest
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-nest}

%package -n python3-%{pypi_name}-neuron
Summary:        %{summary}
%if %{with neuronext}
BuildRequires:  neuron
%endif
Requires:     %{py3_dist neuron}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-neuron
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-neuron}

%package -n python3-%{pypi_name}-brian
Summary:      %{summary}
BuildArch:      noarch
Requires:     %{py3_dist brian}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-brian
%{pypi_name} files for the Brian simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-brian}

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
%if %{with py2}
%package -n python2-%{pypi_name}-nest-mpich
Summary:        %{summary}
BuildRequires:  nest-mpich
BuildRequires:  nest-mpich-headers
Requires:     %{py2_dist nest-mpich}
Requires:     python2-%{pypi_name}-common

%description -n python2-%{pypi_name}-nest-mpich
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python2-%{pypi_name}-nest-mpich}

%package -n python2-%{pypi_name}-neuron-mpich
Summary:        %{summary}
%if %{with neuronext}
BuildRequires:  neuron
%endif
Requires:     %{py2_dist neuron}
Requires:     python2-%{pypi_name}-common

%description -n python2-%{pypi_name}-neuron-mpich
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python2-%{pypi_name}-neuron-mpich}

%endif # py2


%package -n python3-%{pypi_name}-nest-mpich
Summary:        %{summary}
BuildRequires:  nest-mpich
BuildRequires:  nest-mpich-headers
Requires:     %{py3_dist nest-mpich}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-nest-mpich
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-nest-mpich}

%package -n python3-%{pypi_name}-neuron-mpich
Summary:        %{summary}
%if %{with neuronext}
BuildRequires:  neuron
%endif
Requires:     %{py3_dist neuron}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-neuron-mpich
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-neuron-mpich}

%endif # mpich

# openmpi
%if %{with openmpi}
%if %{with py2}
%package -n python2-%{pypi_name}-nest-openmpi
Summary:        %{summary}
BuildRequires:  nest-openmpi
BuildRequires:  nest-openmpi-headers
Requires:     %{py2_dist nest-openmpi}
Requires:     python2-%{pypi_name}-common

%description -n python2-%{pypi_name}-nest-openmpi
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python2-%{pypi_name}-nest-openmpi}

%package -n python2-%{pypi_name}-neuron-openmpi
Summary:        %{summary}
%if %{with neuronext}
BuildRequires:  neuron
%endif
Requires:     %{py2_dist neuron}
Requires:     python2-%{pypi_name}-common

%description -n python2-%{pypi_name}-neuron-openmpi
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python2-%{pypi_name}-neuron-openmpi}

%endif # py2


%package -n python3-%{pypi_name}-nest-openmpi
Summary:        %{summary}
BuildRequires:  nest-openmpi
BuildRequires:  nest-openmpi-headers
Requires:     %{py3_dist nest-openmpi}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-nest-openmpi
%{pypi_name} files for the NEST simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-nest-openmpi}

%package -n python3-%{pypi_name}-neuron-openmpi
Summary:        %{summary}
%if %{with neuronext}
BuildRequires:  neuron
%endif
Requires:     %{py3_dist neuron}
Requires:     python3-%{pypi_name}-common

%description -n python3-%{pypi_name}-neuron-openmpi
%{pypi_name} files for the NEURON simulator.

%{?python_provide:%python_provide python3-%{pypi_name}-neuron-openmpi}

%endif # openmpi

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

%if %{with neuronext}
    pushd %{mod_name}/neuron/nmodl || exit 1
        %{set_build_flags}
        $MPI_BIN/nrnivmodl
    popd
%endif

%if %{with nestext}
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

%if %{with nestext}
    pushd %{mod_name}/nest/extensions || exit 1
        %make_install
    popd
%endif

    %if %{with py2}
        %{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT --install-lib=$MPI2_SITEARCH
    %endif
popd
}

PKG_VARIANT=""
MPI3_SITEARCH=%{python3_sitelib}
MPI2_SITEARCH=%{python2_sitelib}
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


%files doc
%license LICENSE
%doc %{pypi_name}-%{version}/examples
%if %{with docs}
%doc %{pypi_name}-%{version}/html
%endif

%if %{with py2}
%files -n python2-%{pypi_name}-common
%license LICENSE
%doc README.rst AUTHORS changelog
%{python2_sitelib}/%{pypi_name}-%{version}-py3.?.egg-info
%dir %{python2_sitelib}/%{mod_name}
%{python2_sitelib}/%{mod_name}/*py
%{python2_sitelib}/%{mod_name}/common
%{python2_sitelib}/%{mod_name}/descriptions
%{python2_sitelib}/%{mod_name}/utility
%{python2_sitelib}/%{mod_name}/standardmodels
%{python2_sitelib}/%{mod_name}/recording
%{python2_sitelib}/%{mod_name}/mock
%{python2_sitelib}/%{mod_name}/neuroml
%{python2_sitelib}/%{mod_name}/__pycache__

%files -n python2-%{pypi_name}-nest
%{python2_sitelib}/%{mod_name}/nest
%if %{with nestext}
# extensions go here
%endif

%files -n python2-%{pypi_name}-neuron
%{python2_sitelib}/%{mod_name}/neuron
%if %{with neuronext}
# nmodl bits go here
%endif

%files -n python2-%{pypi_name}-brian
%{python2_sitelib}/%{mod_name}/brian

%files -n python2-%{pypi_name}-nineml
%{python2_sitelib}/%{mod_name}/nineml

%endif #py2

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

%files -n python3-%{pypi_name}-nest
%{python3_sitelib}/%{mod_name}/nest
%if %{with nestext}
# nest extensions go here
%endif # nest

%files -n python3-%{pypi_name}-neuron
%{python3_sitelib}/%{mod_name}/neuron
%if %{with neuronext}
# nmodl things go here
%endif # neuron

%files -n python3-%{pypi_name}-brian
%{python3_sitelib}/%{mod_name}/brian

%files -n python3-%{pypi_name}-nineml
%{python3_sitelib}/%{mod_name}/nineml

# mpich
%if %{with mpich}
%if %{with py2}
%files -n python2-%{pypi_name}-nest
%if %{with nestext}
# nest extensions go here
%endif # nest

%files -n python2-%{pypi_name}-neuron
%if %{with neuronext}
# nmodl extensions go here
%endif # neuron

%endif # py2

%files -n python3-%{pypi_name}-nest
%if %{with nestext}
# nest extensions go here
%endif # nest

%files -n python3-%{pypi_name}-neuron
%if %{with neuronext}
# nmodl bits go here
%endif # neuron

%endif # mpich

# openmpi
%if %{with openmpi}
%if %{with py2}
%files -n python2-%{pypi_name}-nest
%if %{with nestext}
# nest extensions go here
%endif # nest

%files -n python2-%{pypi_name}-neuron
%if %{with neuronext}
# nmodl bits go here
%endif # neuron

%endif # py2

%files -n python3-%{pypi_name}-nest
%if %{with nestext}
# nest extensions go here
%endif # nest

%files -n python3-%{pypi_name}-neuron
%if %{with neuronext}
# nmodl bits go here
%endif # neuron

%endif # openmpi

%changelog
* Sun Nov 25 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.2-1
- Initial build
