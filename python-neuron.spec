# Python bindings for NEURON
# Are build in post-installation hooks, so they must be built after NEURON has
# been built.

%global commit 56875193411d552eea7d4cbfe09458f3c4f76613
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global desc %{expand: \
NEURON is a simulation environment for modeling individual neurons and networks
of neurons. It provides tools for conveniently building, managing, and using
models in a way that is numerically sound and computationally efficient. It is
particularly well-suited to problems that are closely linked to experimental
data, especially those that involve cells with complex anatomical and
biophysical properties.

This package provides the Python bindings for NEURON.
}

%global tarname nrn

# fails somehow, disabled by default
%bcond_with metis

# IV uses libtiff from 1995 and threfore has not been packaged yet
%bcond_with iv


%global srcname neuron

%global desc %{expand: \
Add a description here.}

Name:       python-%{srcname}
Version:    7.5
Release:    5.20181214git%{shortcommit}%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv3+
URL:        http://www.neuron.yale.edu/neuron/
# Using brunomaga's fork which updates neuron to use the current sundials
# Will be merged to neuron main eventually
# https://github.com/neuronsimulator/nrn/issues/113
Source0:    https://github.com/brunomaga/%{tarname}/archive/%{commit}/%{tarname}-%{shortcommit}.tar.gz
# Source0:    https://github.com/neuronsimulator/%%{tarname}/archive/%%{commit}/%%{tarname}-%%{shortcommit}.tar.gz

# Based on brunomega's master branch
Patch0:     0001-Unbundle-Random123.patch
# libstdc++ bundled is from 1988: seems heavily modified. Headers from there
# are not present in the current version
# https://github.com/neuronsimulator/nrn/issues/145
# Upstream changes the soname etc., so this will not conflict with the packaged
# version
# Unbundle readline
Patch1:     0002-Unbundle-readline.patch

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
BuildRequires:  git
%if %{with iv}
BuildRequires:  iv-static iv-devel
%endif
BuildRequires:  libX11-devel
BuildRequires:  libtool
%if %{with metis}
BuildRequires:  metis-devel
%endif
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  Random123-devel
BuildRequires:  sundials-devel

# Tightly linked to the neuron build
BuildRequires: %{srcname}-devel
# BuildRequires: %{srcname}-devel%{?_isa} = %{version}-%{release}

%{?python_enable_dependency_generator}

%description
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%prep
%autosetup -n %{tarname}-%{commit} -p1 -S git

# Disable mswin bit
sed -i 's/mswin//g'  src/Makefile.am

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
export SUNDIALS_SYSTEM_INSTALL="yes"
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

%configure %{iv_flags} %{metis_flags} --with-gnu-ld --with-nrnpython-only --with-pyexe=%{__python3} --disable-cygwin

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool && \
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install
# Installs it even when we're not providing nrnpy
rm -fv $RPM_BUILD_ROOT/%{_bindir}/*nrnpy* -f
# Remove installed libtool copy
rm -fv $RPM_BUILD_ROOT/%{_datadir}/%{tarname}/libtool

# Post install clean up
# Remove stray object files
# Probably worth a PR
# Must be done at end, otherwise it deletes object files required for other builds
find . $RPM_BUILD_ROOT/%{_libdir}/ -name "*.o" -exec rm -f '{}' \;
# Remove libtool archives
find . $RPM_BUILD_ROOT/%{_libdir}/ -name "*.la" -exec rm -f '{}' \;

# Still needed on F28?
%ldconfig_scriptlets

%files -n python3-%{srcname}
# %license COPYING
# %doc README.rst
# %{python3_sitelib}/%{srcname}-%{version}-py3.?.egg-info
# %{python3_sitelib}/%{srcname}


%changelog
* Sat Mar 02 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-5.20181214git5687519
- initial build
