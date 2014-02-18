Name:       nrn
Version:    7.3
Release:    1%{?dist}
Summary:    A flexible and powerful simulator of neurons and networks

License:    GPLv2+
URL:        http://www.neuron.yale.edu/neuron/
Source0:    http://www.neuron.yale.edu/ftp/neuron/versions/v7.3/nrn-7.3.tar.gz

# HACK! HACK! HACK!
# I don't know how else to fix it.
Patch0:     %{name}-%{version}-config.patch
Patch1:     %{name}-%{version}-src-makefile.patch

BuildRequires:  ncurses-devel iv-static iv-devel readline-devel
BuildRequires:  Random123-devel Cython
#BuildRequires:  java-1.8.0-openjdk-devel 
BuildRequires:  python2-devel 
BuildRequires:  libX11-devel

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

%prep
%setup -q
%patch0
%patch1
# cannot remove gnu, looks like a customized version.  I cant find the headers
# or declarations yet. The code headers have a 1988 copyright!
rm -fr src/Random123 src/e_editor src/mswin src/readline

# e_editor is replaced by ed
sed -ibackup "s|../e_editor/hoc_ed|/usr/bin/ed|" src/nrnoc/Makefile.am src/nrnoc/Makefile.in
# Line 986
sed -ibackup "s|\$(HOC_E_DEP)$||" src/nrnoc/Makefile.am src/nrnoc/Makefile.in
sed -i 's|IV_LIBDIR="$IV_DIR"/"$host_cpu"/lib|IV_LIBDIR="%{_libdir}"|' configure
sed -i 's|IV_LIBDIR="$IV_DIR"/"$host_cpu"/lib|IV_LIBDIR="%{_libdir}"|' configure
sed -i 's|IV_INCLUDE=-I$IV_DIR/include|IV_INCLUDE=-I%{_includedir}|' configure

%build
%configure --with-x --without-nrnpython --without-nrnjava --with-pic --enable-shared=yes --enable-static=no --disable-rpath --with-iv
make %{?_smp_mflags}

# Py build doesn't work too well
#pushd src/nrnpython
#    CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
#popd


%install
make install DESTDIR=%{buildroot}

#pushd src/nrnpython
#    %{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
#popd

# Remove random object files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.o

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



%changelog
* Tue Feb 18 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 7.3-1
- Initial rpmbuild


