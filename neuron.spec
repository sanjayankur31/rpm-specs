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

# disabled for the moment
%bcond_with mpich
%bcond_with openmpi

# fails somehow, disabled by default
%bcond_with metis

Name:       neuron
Version:    7.5
Release:    1.git%{shortcommit}%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv2+
URL:        http://www.neuron.yale.edu/neuron/
Source0:    https://github.com/neuronsimulator/%{tarname}/archive/%{commit}/%{tarname}-%{shortcommit}.tar.gz
Source1:    neuron-nrnversion.h
Patch0:     0001-Unbundle-Random123.patch

# Random123 does not build on these, so neither can NEURON
# https://github.com/neuronsimulator/nrn/issues/114
ExcludeArch:    %{arm} mips64r2 mips32r2 s390 s390x

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

%prep
%autosetup -c -n %{tarname}-%{commit} -N

pushd %{tarname}-%{commit}
    %autopatch -p1
    # Install the version file so that we dont let the build script do it
    cp -v %{SOURCE1} src/nrnoc/nrnversion.h
    sed -i '/git2nrnversion_h.sh/ d' build.sh
popd

%if %{with mpich}
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-mpich
%endif

%if %{with openmpi}
cp -a %{tarname}-%{commit} %{tarname}-%{commit}-openmpi
%endif

%build
%global do_build %{expand:
echo "*** Building %{tarname}-%{commit}$MPI_COMPILE_TYPE ***"
pushd %{tarname}-%{commit}$MPI_COMPILE_TYPE
./build.sh &&
%configure --without-iv \\\
%if %{with metis} \
--with-metis  \\\
%endif \
--with-x \\\
%if %{with mpich} || %{with openmpi} \
--with-paranrn=dynamic \\\
--with-mpi --with-multisend \\\
%endif

%make_build

popd
}

# Serial build
export MPI_COMPILE_TYPE=""
%{do_build}

%install
%global do_install %{expand:
echo "*** Installing %{tarname}-%{commit}$MPI_COMPILE_TYPE ***"
pushd %{tarname}-%{commit}$MPI_COMPILE_TYPE
%make_install

popd
}

export MPI_COMPILE_TYPE=""
%{do_install}

# Remove stray object files
# Probably worth a PR
find . $RPM_BUILD_ROOT/%{_libdir}/ -name "*.o" -exec rm -fv '{}' \;
rm -fv $RPM_BUILD_ROOT/%{_datadir}/%{tarname}/libtool

%ldconfig_scriptlets

%files
%doc
%{_bindir}/bbswork.sh
%{_bindir}/hel2mos1.sh
%{_bindir}/ivoc
%{_bindir}/memacs
%{_bindir}/mkthreadsafe
%{_bindir}/modlunit
%{_bindir}/mos2nrn
%{_bindir}/mos2nrn2.sh
%{_bindir}/neurondemo
%{_bindir}/nocmodl
%{_bindir}/nrndiagnose.sh
%{_bindir}/nrngui
%{_bindir}/nrniv
%{_bindir}/nrniv_makefile
%{_bindir}/nrnivmodl
%{_bindir}/nrnmech_makefile
%{_bindir}/nrnoc
%{_bindir}/nrnoc_makefile
%{_bindir}/nrnocmodl
%{_bindir}/nrnpyenv.sh
%{_bindir}/oc
%{_bindir}/set_nrnpyenv.sh
%{_bindir}/sortspike
%{_libdir}/libivoc.so.0.0.0
%{_libdir}/libivoc.so.0
%{_libdir}/libmemacs.so.0.0.0
%{_libdir}/libmemacs.so.0
%{_libdir}/libmeschach.so.0.0.0
%{_libdir}/libmeschach.so.0
%{_libdir}/libneuron_gnu.so.0.0.0
%{_libdir}/libneuron_gnu.so.0
%{_libdir}/libnrniv.so.0.0.0
%{_libdir}/libnrniv.so.0
%{_libdir}/libnrnmpi.so.0.0.0
%{_libdir}/libnrnmpi.so.0
%{_libdir}/libnrnoc.so.0.0.0
%{_libdir}/libnrnoc.so.0
%{_libdir}/liboc.so.0.0.0
%{_libdir}/liboc.so.0
%{_libdir}/libocxt.so.0.0.0
%{_libdir}/libocxt.so.0
%{_libdir}/libscopath.so.0.0.0
%{_libdir}/libscopath.so.0
%{_libdir}/libsparse13.so.0.0.0
%{_libdir}/libsparse13.so.0
# BUNDLING!
%{_libdir}/libsundials.so.0.0.0
%{_libdir}/libsundials.so.0

%{_datadir}/%{name}/lib

%files devel
%{_includedir}/%{tarname}
%{_libdir}/libivoc.so
%{_libdir}/libmemacs.so
%{_libdir}/libmeschach.so
%{_libdir}/libneuron_gnu.so
%{_libdir}/libnrniv.so
%{_libdir}/libnrnmpi.so
%{_libdir}/libnrnoc.so
%{_libdir}/liboc.so
%{_libdir}/libocxt.so
%{_libdir}/libscopath.so
%{_libdir}/libsparse13.so
# BUNDLING!
%{_libdir}/libsundials.so

# should this be here?!
%{_libdir}/nrnconf.h

# Do we need the static libraries?
%files static
%{_libdir}/libivoc.la
%{_libdir}/libmemacs.la
%{_libdir}/libmeschach.la
%{_libdir}/libneuron_gnu.la
%{_libdir}/libnrniv.la
%{_libdir}/libnrnmpi.la
%{_libdir}/libnrnoc.la
%{_libdir}/liboc.la
%{_libdir}/libocxt.la
%{_libdir}/libscopath.la
%{_libdir}/libsparse13.la
# BUNDLING!
%{_libdir}/libsundials.la


%doc
%{_datadir}/%{name}/examples
%{_datadir}/%{name}/demo

%changelog
* Sun Nov 11 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-1.git4650e7c
- Update to latest git snapshot
