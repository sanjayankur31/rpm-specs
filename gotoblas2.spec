Name:           gotoblas2
Version:        1.13
Release:        1%{?dist}
Summary:        GotoBLAS2 uses new algorithms and memory techniques for optimal performance of the BLAS routines

License:        BSD
URL:            http://www.tacc.utexas.edu/tacc-projects/gotoblas2/
# http://cms.tacc.utexas.edu/tacc-projects/gotoblas2/downloads/
# http://cms.tacc.utexas.edu/index.php?eID=tx_nawsecuredl&u=0&file=fileadmin/images/GotoBLAS2-1.13_bsd.tar.gz&t=1308652596&hash=a77e6e44e091ef241ed6d8f16d8dd56e
Source0:        GotoBLAS2-1.13_bsd.tar.gz

BuildRequires:  lapack-devel
#Requires:       

%description
GotoBLAS2 has been released by the Texas Advanced Computing 
Center as open source software under the BSD license. This 
product is no longer under active development by TACC, but 
it is being made available to the community to use, study, 
and extend. GotoBLAS2 uses new algorithms and memory techniques 
for optimal performance of the BLAS routines. The changes 
in this final version target new architecture features in 
microprocessors and interprocessor communication techniques; 
also, NUMA controls enhance multi-threaded execution of BLAS 
routines on node. The library features optimal performance 
on the following platforms:

- Intel Nehalem and Atom systems
- VIA Nanoprocessor 
- AMD Shanghai and Istanbul

The library includes the following features:

- Configurations for a variety of hardware platforms
- Incorporation of features of many ISAs (Instruction Set Architecture)
- Implementation of NUMA controls to assure best process affinity and memory policy
- Dynamic detection of multiple architecture components, which can be included in a single binary (for binary distributions)



%prep
%setup -q -n GotoBLAS2


%build
export CFLAGS="%{optflags}" 
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags} I/%{_libdir}/gfortran/modules" 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc


%changelog
* Mon Jun 20 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.13-1
- intial rpmbuild
