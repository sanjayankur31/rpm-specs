%global debug_package %{nil}
# no binaries to extract debuginfo from
# only static libraries

Name:           UFconfig
Version:        3.6.1
Release:        1%{?dist}
Summary:        Commonly used configuration files for software developed by Tim Davis, CISE, UF

License:        Copyright only
URL:            http://www.cise.ufl.edu/research/sparse/%{name}/
Source0:        http://www.cise.ufl.edu/research/sparse/%{name}/%{name}-3.6.1.tar.gz

#BuildRequires:  
#Requires:       

%description
Commonly used configuration files required for :

  Package  Description
  -------  -----------
  AMD	   approximate minimum degree ordering
  CAMD	   constrained AMD
  COLAMD   column approximate minimum degree ordering
  CCOLAMD  constrained approximate minimum degree ordering
  UMFPACK  sparse LU factorization, with the BLAS
  CXSparse int/long/real/complex version of CSparse
  CHOLMOD  sparse Cholesky factorization, update/downdate
  KLU	   sparse LU factorization, BLAS-free
  BTF	   permutation to block triangular form
  LDL	   concise sparse LDL'
  LPDASA   LP Dual Active Set Algorithm
  SuiteSparseQR     sparse QR factorization

UFconfig is not required by:

  CSparse	a Concise Sparse matrix package
  RBio		read/write files in Rutherford/Boeing format
  UFcollection	tools for managing the UF Sparse Matrix Collection
  LINFACTOR     simple m-file to show how to use LU and CHOL to solve Ax=b
  MESHND        2D and 3D mesh generation and nested dissection ordering
  MATLAB_Tools  misc collection of m-files
  SSMULT        sparse matrix times sparse matrix, for use in MATLAB

%package devel
Summary: Development files for %{name}
Provides: %{name}-static = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description devel
The package contains the static library and includes for %{name}

%prep
%setup -q -n %{name}

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_libdir}
install -d $RPM_BUILD_ROOT/%{_includedir}/%{name}
install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}
make install INSTALL_LIB=$RPM_BUILD_ROOT/%{_libdir}  INSTALL_INCLUDE=$RPM_BUILD_ROOT/%{_includedir}/%{name}/
install -p UFconfig.mk  -t $RPM_BUILD_ROOT/%{_datadir}/%{name}

%files
%doc README.txt
%{_datadir}/%{name}/%{name}.mk

%files devel
%{_libdir}/*
%{_includedir}/%{name}/

%changelog
* Sat Jun 18 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.6.1-1
- initial RPM build
