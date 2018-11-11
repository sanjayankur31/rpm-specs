%global commit 4650e7c0f1dd8beb79bfa8674979b178f4d56630
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global desc %{expand \
NEURON is a simulation environment for modeling individual neurons and networks
of neurons. It provides tools for conveniently building, managing, and using
models in a way that is numerically sound and computationally efficient. It is
particularly well-suited to problems that are closely linked to experimental
data, especially those that involve cells with complex anatomical and
biophysical properties.

This is currently built without GUI (iv) support.
}

%global tarname nrn
%global with_py2 0

%global with_mpich 0
%global with_openmpi 0

# fails somehow
%global with_metis 0

Name:       neuron
Version:    7.5
Release:    1.git%{shortcommit}%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv2+
URL:        http://www.neuron.yale.edu/neuron/
Source0:    https://github.com/neuronsimulator/%{tarname}/archive/%{commit}/%{tarname}-%{shortcommit}.tar.gz
Source1:    neuron-nrnversion.h
Patch0:     0001-Unbundle-Random123.patch
Patch1:     0002-Disable-nrnpy-build-install-during-make-install.patch


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

# Currently bundles sundials. WIP
# https://github.com/neuronsimulator/nrn/issues/113
# BuildRequires:  sundials-devel

# Not building with iv yet
# BuildRequires:  iv-static iv-devel

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

%if %{with_py2}
%package -n python2-%{name}
Summary:    Python2 bindings for NEURON
BuildRequires:  %{py2_dist Cython}
BuildRequires:  python2-devel

%description -n python2-%{name}
%{desc}

This package contains the Python2 bindings for NEURON.
%endif

%package -n python3-%{name}
Summary:    Python bindings for NEURON
BuildRequires:  %{py3_dist Cython}
BuildRequires:  python3-devel

%description -n python3-%{name}
%{desc}

This package contains the Python3 bindings for NEURON.

%prep
%autosetup -c -n %{tarname}-%{commit} -N

pushd %{tarname}-%{commit}
    %autopatch -p1
    # Install the version file so that we dont let the build script do it
    cp -v %{SOURCE1} src/nrnoc/nrnversion.h
    sed -i '/git2nrnversion_h.sh/ d' build.sh
popd

# py3 build directories do not have a suffix, py2 ones have -py2
%if %{with_py2}
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-py2
%endif

%if %{with_mpich}
%if %{with_py2}
    cp -a %{tarname}-%{commit}-py2 %{tarname}-%{commit}-mpich-py2
%endif
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-mpich
%endif

%if %{with_openmpi}
%if %{with_py2}
    cp -a %{tarname}-%{commit}-py2 %{tarname}-%{commit}-openmpi-py2
%endif
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-openmpi
%endif

%build
%global do_build %{expand:
echo "*** Building %{tarname}-%{commit}$MPI_COMPILE_TYPE ***"
pushd %{tarname}-%{commit}$MPI_COMPILE_TYPE
./build.sh &&
%configure --without-iv \\\
%if %{with_metis} \
--with-metis  \\\
%endif \
--with-x \\\
%if %{with_mpich} || %{with_openmpi} \
--with-paranrn=dynamic \\\
--with-mpi --with-multisend \\\
%endif \
--with-nrnpython=dynamic --with-pyexe=$MPI_PYTHON 

%make_build

pushd src/nrnpython
CFLAGS="%{optflags}" $MPI_PYTHON setup.py build
popd
popd
}

# Serial py3 build
export MPI_COMPILE_TYPE=""
export MPI_PYTHON=%{__python3}
%{do_build}

%install
%global do_install %{expand:
echo "*** Installing %{tarname}-%{commit}$MPI_COMPILE_TYPE ***"
pushd %{tarname}-%{commit}$MPI_COMPILE_TYPE
%make_install

pushd src/nrnpython
$MPI_PYTHON setup.py install
popd

popd
}

# Serial py3 build
export MPI_COMPILE_TYPE=""
export MPI_PYTHON=%{__python3}
%{do_install}


%ldconfig_scriptlets

%files
%doc
# %{_bindir}/*
# %{_datadir}/%{name}
# %{_libdir}/*.so.*

%files devel
# %{_includedir}/%{name}/
# %{_libdir}/*.so
# %{_libdir}/nrnconf.h

# Do we need the static libraries?
%files static
# %{_libdir}/*.la

%if %{with_py2}
%files -n python2-%{name}
# %{python2_sitearch}/neuron/
# %{python2_sitearch}/NEURON-%{version}-py?.?.egg-info
%endif

%files -n python3-%{name}
# %{python3_sitearch}/neuron/
# %{python3_sitearch}/NEURON-%{version}-py?.?.egg-info

%changelog
* Sun Nov 11 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-1.git4650e7c
- Update to latest git snapshot
