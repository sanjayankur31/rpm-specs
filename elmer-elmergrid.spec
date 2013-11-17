# elmer needs matc etc to be build *before* it can be built
# therefore packaging these separately, and not as subpackages
%global svn_rev 5280
%global check_out_date 20110807
Name:           elmer-elmergrid
Summary:        Open Source Finite Element Software for Multiphysical Problems
Version:        0
Release:        0.1.%{check_out_date}.svn%{svn_rev}%{?dist}

License:        GPLv2+
URL:            http://www.csc.fi/english/pages/elmer

# svn export -r 5280 https://elmerfem.svn.sourceforge.net/svnroot/elmerfem/trunk/elmergrid elmer-elmergrid
# tar -cvzf elmer-elmergrid-20110807.tar.gz elmer-elmergrid/
Source0:        %{name}-%{check_out_date}.tar.gz
Patch0:         0001-%{name}-add-conditional-metis.patch
BuildRequires:  libgfortran compat-libgfortran-41 
BuildRequires:  gcc-gfortran getdata-fortran
BuildRequires:  libgfortran-static mingw32-gcc-gfortran 
BuildRequires:  patchy-gfortran paw-gfortran
BuildRequires:  blas-devel elmer-matc-devel


%description
Elmer is an open source multiphysical simulation software 
developed by CSC - IT Center for Science (CSC). Elmer development 
was started 1995 in collaboration with Finnish Universities, 
research institutes and industry.

Elmer includes physical models of fluid dynamics, structural 
mechanics, electromagnetics, heat transfer and acoustics, for 
example. These are described by partial differential equations 
which Elmer solves by the Finite Element Method (FEM).

%prep
%setup -q -n %{name}

# A small patch to remove any requirement of metis
cd src/
%patch0 -b.orig
cd ..

# to print alternate text when metis is called
sed -i "s/\(PARTMETIS\) 1/\1 0/" ./src/femelmer.h

# permission check
chmod a-x src/*.h src/*.c

%build
%configure --with-metis=no --with-matc="%{_libdir}/libmatc.a"
# even after configure, it still looks for metis
sed -i "s/-lmetis//" Makefile src/Makefile

make %{?_smp_flags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_docdir}/elmergrid/doc/tests/
cp -rv --preserve=timestamps tests/* $RPM_BUILD_ROOT/%{_docdir}/elmergrid/doc/tests/
# keeps failing! WHY?!?
# chmod -vR 0644 $RPM_BUILD_ROOT/%{_docdir}/tests/*
install -p -m 0644 GPL-2 -t $RPM_BUILD_ROOT/%{_docdir}/elmergrid/

%files
%defattr(-,root,root,-)
%{_bindir}/ElmerGrid
%{_docdir}/elmergrid/

%changelog
* Sun Aug 07 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1.20110807.svn5280
- Corrected versioning
- Checking out only the required module, instead of the elmerfem full svn

* Sat Jul 02 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110623-0.2svn5244
- remove metis support

* Sat Jun 18 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110623-0.1svn5244
- initial rpm build
