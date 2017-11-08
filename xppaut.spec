Name:           xppaut
Version:        7.0
Release:        1%{?dist}
Summary:        The differential equations tool

License:        GPLv2
URL:            http://www.math.pitt.edu/~bard/xpp/xpp.html
Source0:        http://www.math.pitt.edu/~bard/bardware/xppaut_latest.tar.gz
Source1:        http://www.math.pitt.edu/~bard/bardware/xpp_doc.pdf
Patch0:         0001-Makefile-fix.patch
Patch1:         0002-Build-fix1.patch
Patch2:         0003-xppaut-buildfix2.patch
Patch3:         0004-Makefile-fix-2.patch
Patch4:         0005-Use-system-cvode.h.patch

BuildRequires:  libX11-devel sundials-devel
#Requires:       

%description
XPP (XPPAUT is another name) is a tool for solving

    - differential equations,
    - difference equations,
    - delay equations,
    - functional equations,
    - boundary value problems, and
    - stochastic equations.

It evolved from a chapter written by John Rinzel and me on the qualitative
theory of nerve membranes and eventually became a commercial product for MSDOS
computers called PHASEPLANE. It is now available as a program running under X11
and Windows.

The code brings together a number of useful algorithms and is extremely
portable. All the graphics and interface are written completely in Xlib which
explains the somewhat idiosyncratic and primitive widgets interface.

XPP contains the code for the popular bifurcation program, AUTO . Thus, you can
switch back and forth between XPP and AUTO, using the values of one program in
the other and vice-versa. I have put a ``friendly'' face on AUTO as well. You
do not need to know much about it to play around with it.

XPP has the capabilities for handling up to 590 differential equations.

    - There areover a dozen solvers including several for stiff systems, a
      solver for integral equations and a symplectic solver.
    - Up to 10 graphics windows can be visible at once and a variety of color
      combinations is supported.
    - PostScript output is supported as well as GIF and animater GIF movies
    - Post processing is easy and includes the ability to make histograms, FFTs
      and applying functions to columns of your data.
    - Equilibria and linear stability as well as one-dimensional invariant sets
      can be computed.
    - Nullclines and flow fields aid in the qualitative understanding of
      two-dimensional models.
    - Poincare maps and equations on cylinders and tori are also supported.
    - Some useful averaging theory tricks and various methods for dealing with
      coupled oscillators are included primarily because that is what I do for
      a living.
    - Equations with Dirac delta functions are allowable.
    - I have added an animation package that allows you to create animated
      versions of your simulations, such as a little pendulum moving back and
      forth or lamprey swimming. See toys! for examples.
    - There is a curve-fitter based on the Marquardt-Levenberg algorithm which
      lets you fit data points to the solutions to dynamical systems.
    - It is possible to automatically generate ``movies'' of three-dimensional
      views of attractors or parametric changes in the attractor as some
      parameters vary.
    - Dynamically link to external subroutines 

%prep
%setup -q -c
# remove cvode stuff that sundials already contains
rm -f cvode_band.h  cvode_bandpre.h  cvode_bbdpre.h  cvode_dense.h \
cvode_diag.h  cvode_direct.h  cvode.h  cvode_impl.h  cvode_lapack.h \
cvode_sparse.h  cvode_spbcgs.h  cvode_spgmr.h  cvode_spils.h  cvode_sptfqmr.h \
cvodes_band.h  cvodes_bandpre.h  cvodes_bbdpre.h  cvodes_dense.h  cvodes_diag.h \
cvodes_direct.h  cvodes.h  cvodes_impl.h  cvodes_lapack.h  cvodes_sparse.h \
cvodes_spbcgs.h  cvodes_spgmr.h  cvodes_spils.h  cvodes_sptfqmr.h

# why does the source have so files?
find . -name "*.so" -exec rm -f '{}' \;
find . -name "*~" -exec rm -f '{}' \;
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
export CFLAGS="%{optflags} -fPIC -D_XOPEN_SOURCE=600 -DNON_UNIX_STDIO -DAUTO -DCVODE_YES"
export CXXFLAGS="%{optflags} -fPIC -D_XOPEN_SOURCE=600 -DNON_UNIX_STDIO -DAUTO -DCVODE_YES"
export LDFLAGS="${LDFLAGS:--Wl,-z,relro }"
#make %{?_smp_mflags} MANDIR=%{_mandir}/man1/ BINDIR=%{_bindir} DOCDIR=%{_docdir}/%{name} LIBDIR=%{_libdir} xppaut mkmkavi xpplib
make MANDIR=%{_mandir}/man1/ BINDIR=%{_bindir} DOCDIR=%{_docdir}/%{name} LIBDIR=%{_libdir} xppaut mkmkavi xpplib
rm -f odesol2.o


%install
%make_install MANDIR=%{_mandir}/man1/ BINDIR=%{_bindir} %DOCDIR=%{_docdir}/%{name} LIBDIR=%{_libdir}



%files
%license LICENSE
%{_bindir}/%{name}
%{_docdir}/%{name}
%{_mandir}/man1/%{name}*

%changelog
* Fri Jul 31 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 7.0-1
- Initial build
