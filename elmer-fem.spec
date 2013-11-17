# elmer needs matc etc to be build *before* it can be built
# therefore packaging these separately, and not as subpackages
%global svn_rev 5280
%global check_out_date 20110807
Name:           elmer-fem
Summary:        Open Source Finite Element Software for Multiphysical Problems
Version:        0
Release:        0.1.%{check_out_date}.svn%{svn_rev}%{?dist}

License:        GPLv2+
URL:            http://www.csc.fi/english/pages/elmer

# svn export -r 5280 https://elmerfem.svn.sourceforge.net/svnroot/elmerfem/trunk/fem elmer-fem
# tar -cvzf elmer-fem-20110807.tar.gz elmer-fem/
Source0:        %{name}-%{check_out_date}.tar.gz
BuildRequires:  libgfortran compat-libgfortran-41 gcc-gfortran getdata-fortran
BuildRequires:  libgfortran-static mingw32-gcc-gfortran patchy-gfortran paw-gfortran
BuildRequires:  blas-devel elmer-matc-devel lapack-devel suitesparse-devel arpack-devel
BuildRequires:  elmer-eio-devel elmer-hutiter-devel
# without openmpi : default configuration
Provides:       elmer
Requires:       elmer-elmergrid
Requires:       elmer-matc
Requires:       elmer-eio
Requires:       elmer-hutiter
Requires:       elmer-meshgen2d

%description
Elmer is an open source multiphysical simulation software 
developed by CSC - IT Center for Science (CSC). Elmer development 
was started 1995 in collaboration with Finnish Universities, 
research institutes and industry.

Elmer includes physical models of fluid dynamics, structural 
mechanics, electromagnetics, heat transfer and acoustics, for 
example. These are described by partial differential equations 
which Elmer solves by the Finite Element Method (FEM).

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}

%build
%configure --without-metis --with-eiof="%{_libdir}/libeiof.a" --disable-static --disable-rpath
# it segfaults when I try to use FFLAGS. Output:
# DEBUG: ParticleUtils.f90:1784:0: warning: 'maskperm.offset' may be used uninitialized in this function [-Wuninitialized]
# DEBUG: /lib/cpp -DCONTIG=",CONTIGUOUS" -P -traditional-cpp -I. -I/usr/include -DFULL_INDUCTION -DUSE_ARPACK Feti.src > Feti.f90
# DEBUG: gfortran -fPIC -I. -Ibinio -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -Wl,-z,relro -m32 -march=i686  -fasynchronous-unwind-tables -I/usr/lib/gfortran/modules -c Feti.f90
# DEBUG: f951: internal compiler error: Segmentation fault
# DEBUG: Please submit a full bug report,
# DEBUG: with preprocessed source if appropriate.
# DEBUG: See <http://bugzilla.redhat.com/bugzilla> for instructions.

# sed -i "s|\(FCFLAGS = -O -fPIC -I. -Ibinio\)|\1 $FFLAGS|" src/Makefile
# remove the -O so it follows our -O2
# sed -i "s|\(FCFLAGS = \)-O|\1|" src/Makefile
# remove flags one by one to see what's causing the segfault : Unable to find the flag to remove!
# FCFLAGS =  -fPIC -I. -Ibinio -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -Wl,-z,relro -m     32 -march=i686 -mtune=atom -fasynchronous-unwind-tables -I/usr/lib/gfortran/modules
# sed -i "s|\(FCFLAGS =  -fPIC -I. -Ibinio -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -Wl,-z,relro -m32 -march=i686 \)-mtune=atom|\1|" src/Makefile

make %{?_smp_flags}


%install
install -d $RPM_BUILD_ROOT/%{_libdir}/
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_docdir}/fem/
install -p -m 0644 GPL-2 -t $RPM_BUILD_ROOT/%{_docdir}/fem/

install -d \
$RPM_BUILD_ROOT/%{_docdir}/fem/examples/ \
$RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow \
$RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow/Cavity \
$RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow/Doc \
$RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow/SnowFirn \
$RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow/Sources \
$RPM_BUILD_ROOT/%{_docdir}/fem/examples/turing \
$RPM_BUILD_ROOT/%{_docdir}/fem/examples/turing/square \

install -p -m 0644 examples/IceFlow/*.* -t $RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow 
install -p -m 0644 examples/IceFlow/Cavity/*.* -t $RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow/Cavity/ 
install -p -m 0644 examples/IceFlow/Doc/*.* -t $RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow/Doc/ 
install -p -m 0644 examples/IceFlow/SnowFirn/*.* -t $RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow/SnowFirn/ 
install -p -m 0644 examples/IceFlow/Sources/*.* -t $RPM_BUILD_ROOT/%{_docdir}/fem/examples/IceFlow/Sources/ 
install -p -m 0644 examples/turing/*.* -t $RPM_BUILD_ROOT/%{_docdir}/fem/examples/turing/
install -p -m 0644 examples/turing/square/*.* -t $RPM_BUILD_ROOT/%{_docdir}/fem/examples/turing/square/

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/libelmersolver-6.2.so
%{_docdir}/fem/

%files devel
%defattr(-,root,root,-)
%{_datadir}/elmersolver/
%{_libdir}/libelmersolver.so

%changelog
* Sun Aug 07 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1.20110807.svn5280
- Corrected versioning
- Checking out only the required module, instead of the elmerfem full svn

* Sat Jul 02 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110623-0.2svn5244
- remove metis support
- convert to elmer meta package

* Sat Jun 18 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110623-0.1svn5244
- initial rpm build
