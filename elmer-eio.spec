# elmer needs eio etc to be build *before* it can be built
# therefore packaging these separately, and not as subpackages
%global svn_rev 5280
%global check_out_date 20110807
Name:           elmer-eio
Version:        0
Release:        0.1.%{check_out_date}.svn%{svn_rev}%{?dist}
Summary:        Open Source Finite Element Software for Multiphysical Problems

License:        GPLv2+
URL:            http://www.csc.fi/english/pages/elmer

# svn export -r 5280 https://elmerfem.svn.sourceforge.net/svnroot/elmerfem/trunk/eio elmer-eio
# tar -cvzf elmer-eio-20110807.tar.gz elmer-eio/
Source0:        %{name}-%{check_out_date}.tar.gz
BuildRequires:  libgfortran compat-libgfortran-41 gcc-gfortran getdata-fortran
BuildRequires:  libgfortran-static mingw32-gcc-gfortran patchy-gfortran paw-gfortran


%description
Elmer is an open source multiphysical simulation software 
developed by CSC - IT Center for Science (CSC). Elmer development 
was started 1995 in collaboration with Finnish Universities, 
research institutes and industry.

Elmer includes physical models of fluid dynamics, structural 
mechanics, electromagnetics, heat transfer and acoustics, for 
example. These are described by partial differential equations 
which Elmer solves by the Finite Element Method (FEM).

%package devel
Requires:     %{name} = %{version}-%{release}
Summary:      Files required for development using %{name}
Provides:     %{name}-static = %{version}-%{release}

%description devel
This package contains the headers and libraries that can be used
to link applications to %{name}

%prep
%setup -q -n %{name}

%build
%configure 
make %{?_smp_flags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_docdir}/eio/
install -p -m 0644 GPL-2 TODO -t $RPM_BUILD_ROOT/%{_docdir}/eio/

%files
%defattr(-,root,root,-)
%{_docdir}/eio/

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_includedir}/*

%changelog
* Sun Aug 07 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1.20110807.svn5280
- Corrected versioning
- Checking out only the required module, instead of the elmerfem full svn

* Sat Jun 18 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110623-0.1svn5244
- initial rpm build
