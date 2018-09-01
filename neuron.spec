%global tarname nrn
Name:       neuron
Version:    7.5
Release:    1%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv2+
URL:        http://www.neuron.yale.edu/neuron/
Source0:    https://neuron.yale.edu/ftp/neuron/versions/v%{version}/%{tarname}-%{version}.tar.gz

# HACK! HACK! HACK!
# I don't know how else to fix it.
# Patch0:     %{name}-%{version}-config.patch
# Patch1:     %{name}-%{version}-src-makefile.patch
# Patch2:     %{name}-%{version}-nrnpython.patch
# Patch3:     %{name}-%{version}-python-installroot.patch
# Patch4:     %{name}-%{version}-python-installroot-neuronmusic.patch
# Patch5:     %{name}-%{version}-python-installroot-setup-neuronmusic.patch
# Patch6:     %{name}-%{version}-homedir.patch
# Patch7:     %{name}-%{version}-python-makefile.patch
# Patch8:     %{name}-%{version}-nrnunits.patch
# Patch9:     %{name}-%{version}-bin-files.patch

BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  Random123-devel 
BuildRequires:  python2-Cython
BuildRequires:  python2-devel
BuildRequires:  libX11-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  python3-Cython

# BuildRequires:  java-1.8.0-openjdk-devel
# Not building with iv yet
# BuildRequires:  iv-static iv-devel

# Is pvm packaged properly? Everything appears to be in /usr/share..
# Cannot be used in this state
#BuildRequires:  pvm
#Requires:

%description
NEURON is a simulation environment for modeling individual neurons and networks
of neurons. It provides tools for conveniently building, managing, and using
models in a way that is numerically sound and computationally efficient. It is
particularly well-suited to problems that are closely linked to experimental
data, especially those that involve cells with complex anatomical and
biophysical properties.

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

%package -n python-%{name}
Summary:    Python bindings for NEURON

%description -n python-%{name}
This package contains the Python2 bindings for NEURON.

%package -n python3-%{name}
Summary:    Python bindings for NEURON

%description -n python3-%{name}
This package contains the Python3 bindings for NEURON.

%prep
%setup -q -n %{tarname}-%{version}

# %patch0
# %patch1
# %patch2
# %patch3
# %patch4
# %patch5
# %patch6
# %patch7
# %patch8
# %patch9

# Way too much work patching them individually
#sed -i "s|pkgdatadir = \$(datadir)/@PACKAGE@|pkgdatadir = \$(datadir)/@PACKAGE@-@PACKAGE_VERSION@/|" Makefile.in
# find ./share/lib/hoc/ -name "Makefile.in" -execdir sed -i "s|neuronhomedir = \$(prefix)/share/@PACKAGE@/lib|neuronhomedir = \$(prefix)/share/@PACKAGE@/|" '{}' \;
# sed -i -e "s|nrndir = \$(prefix)/share/@PACKAGE@/lib|nrndir = \$(prefix)/share/@PACKAGE@|" share/lib/hoc/chanbild/Makefile.in
# find ./share/lib/auditscripts/ -name "Makefile.in" -execdir sed -i "s|neuronhomedir = \$(prefix)/share/@PACKAGE@/lib|neuronhomedir = \$(prefix)/share/@PACKAGE@/|" '{}' \;
# find ./share/demo -name "Makefile.in" -execdir sed -i "s|thisdir = \$(prefix)/share/@PACKAGE@/demo|thisdir = \$(prefix)/share/@PACKAGE@/demo|" '{}' \;
# find ./share/examples/ -name "Makefile.in" -execdir sed -i "s|thisdir = \$(prefix)/share/@PACKAGE@/examples/|thisdir = \$(prefix)/share/@PACKAGE@/examples/|" '{}' \;
# cannot remove gnu, looks like a customized version.  I cant find the headers
# or declarations yet. The code headers have a 1988 copyright!
rm -fr src/Random123 src/e_editor src/readline

# e_editor is replaced by ed
sed -ibackup "s|../e_editor/hoc_ed|/usr/bin/ed|" src/nrnoc/Makefile.am src/nrnoc/Makefile.in
# Line 986
sed -ibackup "s|\$(HOC_E_DEP)$||" src/nrnoc/Makefile.am src/nrnoc/Makefile.in
# sed -i 's|IV_LIBDIR="$IV_DIR"/"$host_cpu"/lib|IV_LIBDIR="%{_libdir}"|' configure
# sed -i 's|IV_LIBDIR="$IV_DIR"/"$host_cpu"/lib|IV_LIBDIR="%{_libdir}"|' configure
# sed -i 's|IV_INCLUDE=-I$IV_DIR/include|IV_INCLUDE=-I%{_includedir}|' configure

# Doesn't live in /usr/share/nrn/lib any more
# sed -i 's|lib/cleanup|cleanup|' src/oc/hoc.c

# spurious executable perm
find . -name "*.c" -execdir chmod -x '{}' \;
find . -name "*.h" -execdir chmod -x '{}' \;
find . -name "*.cpp" -execdir chmod -x '{}' \;

# for python3 build---must build twice, very hard to uncouple to python build from the build system
cd ..
cp -r %{tarname}-%{version} %{tarname}-%{version}-py3

%build
cd ../

pushd %{tarname}-%{version}
    %configure --with-x --with-nrnpython=%{__python2} --with-numpy --without-nrnjava --with-pic --enable-shared=yes --enable-static=no --disable-rpath --without-iv --disable-pysetup
    make
    pushd src/nrnpython
        CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build
    popd
popd
pushd %{tarname}-%{version}-py3
    %configure --with-x --with-nrnpython=%{__python3} --with-numpy --without-nrnjava --with-pic --enable-shared=yes --enable-static=no --disable-rpath --without-iv --disable-pysetup
    make
    pushd src/nrnpython
        CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
    popd
popd


%install
pushd %{tarname}-%{version}
    make install DESTDIR=$RPM_BUILD_ROOT

    pushd src/nrnpython
        %{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
    popd

    # Remove random object files
    rm -f $RPM_BUILD_ROOT/%{_libdir}/*.o
popd
pushd %{tarname}-%{version}-py3
    make install DESTDIR=$RPM_BUILD_ROOT

    pushd src/nrnpython
        %{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
    popd

    # Remove random object files
    rm -f $RPM_BUILD_ROOT/%{_libdir}/*.o
popd

%check
# Wants a built SO not sure how to proceed
#pushd share/lib/python/neuron/tests
#    PYTHONPATH=$RPM_BUILD_ROOT/%{python2_sitearch}/ %{__python} test_all.py
#popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc
%{_bindir}/*
%{_datadir}/%{name}
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/nrnconf.h

# Do we need the static libraries?
%files static
%{_libdir}/*.la

%files -n python-%{name}
%{python2_sitearch}/neuron/
%{python2_sitearch}/NEURON-%{version}-py?.?.egg-info

%files -n python3-%{name}
%{python3_sitearch}/neuron/
%{python3_sitearch}/NEURON-%{version}-py?.?.egg-info

%changelog
* Sun Aug 26 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-1
- Update to new version
- WIP

* Wed Oct 08 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 7.3-1
- Lots of patches/fixes to get it to build as per FHS
- Managed to build py bindings
- Not had the patience to build java yet

* Tue Feb 18 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 7.3-1
- Initial rpmbuild


