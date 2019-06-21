%global _description %{expand:
NEURON is a simulation environment for modeling individual neurons and networks
of neurons. It provides tools for conveniently building, managing, and using
models in a way that is numerically sound and computationally efficient. It is
particularly well-suited to problems that are closely linked to experimental
data, especially those that involve cells with complex anatomical and
biophysical properties.

This package provides the python bindings for neuron.
It does not include MPI support.

Please install the %{name}-devel package to compile nmodl files and so on.
}

%global tarname nrn

# fails somehow, disabled by default
%bcond_with metis

# IV uses libtiff from 1995 and threfore has not been packaged yet
%bcond_with iv

Name:       python-neuron
Version:    7.7.1
Release:    1%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv3+
URL:        http://www.neuron.yale.edu/neuron/
Source0:    https://github.com/neuronsimulator/%{tarname}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:     0001-Unbundle-Random123.patch
# libstdc++ bundled is from 1988: seems heavily modified. Headers from there
# are not present in the current version
# https://github.com/neuronsimulator/nrn/issues/145
# Upstream changes the soname etc., so this will not conflict with the packaged
# version
# Unbundle readline
Patch1:     0002-Unbundle-readline.patch
# Not really needed here, but it's better to build on the neuron sources
# exactly
Patch2:     0003-Install-ivstream-header.patch
# Do not let the Makefile call setup.py in post-install
Patch3:     0004-Disable-python-bits-in-install-exec-hook.patch

# Random123 does not build on these, so neither can NEURON
# https://github.com/neuronsimulator/nrn/issues/114
ExcludeArch:    %{arm} mips64r2 mips32r2 s390 s390x

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  bison-devel
BuildRequires:  flex
BuildRequires:  flex-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git-core
%if %{with iv}
BuildRequires:  iv-static iv-devel
%endif
BuildRequires:  libX11-devel
BuildRequires:  libtool
%if %{with metis}
BuildRequires:  metis-devel
%endif
BuildRequires:  ncurses-devel
# Required by mk_hocusr.py
BuildRequires:  python3
BuildRequires:  readline-devel
BuildRequires:  Random123-devel

# Bundles sundials. WIP
# https://github.com/neuronsimulator/nrn/issues/113
# BuildRequires:  sundials-devel
# Provides: bundled(sundials) = 2.0.1

%description %_description

%prep
%autosetup -n %{tarname}-%{version} -p1 -S git

# Remove executable perms from source files
find src -type f -executable ! -name "*.sh" | xargs chmod -x

# Remove bundled Random123
rm -rf src/Random123
rm -rf src/readline

# Stop build file from generating version header
sed -i '/git2nrnversion_h.sh/ d' build.sh

# Create version file ourselves
export TIMESTAMP=$(date +%Y-%m-%d)
export COMMIT=%{shortcommit}
cat > src/nrnoc/nrnversion.h << EOF
#define GIT_DATE "$TIMESTAMP"
#define GIT_BRANCH "master"
#define GIT_CHANGESET "$COMMIT"
#define GIT_DESCRIBE "Neuron built for Fedora"
EOF

# Use system libtool instead of a local copy that neuron tries to install
pushd bin
    for f in *_makefile.in
    do
        sed -i 's|\(LIBTOOL.*=.*\)$(pkgdatadir)\(.*\)|\1$(bindir)\2|' $f
    done
popd

%build
# Not yet to be used
# export SUNDIALS_SYSTEM_INSTALL="yes"
./build.sh

%if !%{with iv}
%global iv_flags  --without-iv --with-x
%else
%global iv_flags " "
%endif

%if %{with metis}
%global metis_flags --with-metis
%else
%global metis_flags " "
%endif

%configure %{iv_flags} %{metis_flags} \
--with-gnu-ld --disable-rpm-rules \
--without-paranrn --with-nrnpython-only  \
--with-nrnpython=dynamic --with-pyexe=%{__python3}

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool && \
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make -j1 -C src/nrnpython
pushd src/nrnpython
    %py3_build
popd

%install
%make_install -C src/nrnpython
pushd src/nrnpython
    %py3_install
popd


# The makefiles do not have shebangs
%files
%license Copyright

%changelog
* Wed Jun 19 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.7.1-1
- Initial build
