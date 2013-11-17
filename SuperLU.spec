Name:           SuperLU
Version:        4.1
Release:        1%{?dist}
Summary:        A library for the direct solution of systems of linear equations

License:        BSD
URL:            http://crd.lbl.gov/~xiaoye/SuperLU/
Source0:        http://crd.lbl.gov/~xiaoye/SuperLU/superlu_4.1.tar.gz
Patch0:         %{name}-generate-shared-objects.patch
 
BuildRequires:  blas-devel f2c lapack-devel

%description
SuperLU is a general purpose library for the direct solution of large, sparse,
nonsymmetric systems of linear equations on high performance machines. The
library is written in C and is callable from either C or Fortran. The library
routines will perform an LU decomposition with partial pivoting and triangular
system solves through forward and back substitution. The LU factorization
routines can handle non-square matrices but the triangular solves are performed
only for square matrices. The matrix columns may be preordered (before
factorization) either through library or user supplied routines. This
preordering for sparsity is completely separate from the factorization. Working
precision iterative refinement subroutines are provided for improved backward
stability. Routines are also provided to equilibrate the system, estimate the
condition number, calculate the relative backward error, and estimate error
bounds for the refined solutions. 


%prep
%setup -q -n %{name}_%{version}
#%patch0 -p1 -b .generate-shared-objects

rm -rvf CBLAS
# start fixing the makefile inc
sed -i\
    -e "s:\(BLASLIB 	=\) -L/usr/lib \(-lblas\):\1 -L%{_libdir}/ -llapack -lf2c \2:"\
    -e "s:\(CFLAGS       =\) -DPRNTlevel=0 -O3:\1 %{optflags} -fPIC:"\
    -e "s:\(FORTRAN	     =\) g77:\1 gfortran:"\
    -e "s:\(LOADOPTS     =\):\1 %{optflags} -I%{_libdir}/gfortran/modules:"\
#    -e "s:\(LIBDIR =\):\1 $RPM_BUILD_ROOT%{_libdir}:"\
    -e "s:\(FFLAGS       =\) -O2:\1 %{optflags} -I%{_libdir}/gfortran/modules:" make.inc

# fix it up
sed -i "s:csh:sh:g" INSTALL/Makefile
sed -i "s:#! /bin/csh:#!/bin/sh:" INSTALL/install.csh
sed -i "s:set ofile = install.out:ofile=\"install.out\":" INSTALL/install.csh
mv -v INSTALL/install.csh INSTALL/install.sh

%build
make -j1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc



%changelog
* Mon Jul 11 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> -4.1-1
- initial rpm build
