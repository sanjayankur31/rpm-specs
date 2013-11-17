Name:           o-palm
Version:        4.0.0
Release:        1%{?dist}
Summary:        A coupler for all the applications built upon existing independent models

License:        LGPLv3+
URL:            http://www.cerfacs.fr/globc/PALM_WEB/index.html
Source0:        http://www.cerfacs.fr/globc/PALM_WEB/EN/BECOMEAUSER/download/%{name}4_0_0.tgz
Source1:        %{name}-user-guide-en.pdf
Source2:        %{name}-user-guide-fr.pdf
# add some includes, make changes to Makefile.in
Patch0:         o-palm-make-fixes.patch

BuildRequires:  doxygen blas-devel lapack-devel
BuildRequires:  mpich2-devel flex

%description
The most useful PALM features for such applications are:

- The graphical user interface, making the set-up of a coupled 
application very simple, even with many coupled models.
- The independent interfaces, allowing the use of existing models 
with very few changes, no matter what the other coupled entities are.
- The management of parallel communications, making the coupling 
of parallel models almost automatic.
- The dynamic coupling capabilities, allowing more flexible 
coupling strategies.
- The explicit time reference for the exchanged fields, allowing 
the coupling of iterative models with different time steps.
- The predefined algebra toolbox, allowing field manipulations, 
conversions and interpolations on the fly.
- The debugging, performances analysis and run time monitoring 
tools, simplifying the set-up, the tuning and the control of 
coupled applications.

%package devel
Requires:      %{name} = %{version}-%{release}
Summary:       Development files related to %{name}

%description devel
This package contains files required to develop applications 
linked to %{name}

%package doc
Summary:      Documentation for %{name}

%description doc
This package contains documentation for the %{name} package

%prep
%setup -q -c -n %{name}
%patch0

%build
# make steplang
pushd PrePALM_MP/STEPLANG
    export CFLAGS="%{optflags}"
    export CXXFLAGS="%{optflags}"
    export FFLAGS="%{optflags} -I%{_libdir}/gfortran/modules"
    # Hoping to override these, the configure file won't work for us
    %ifarch x86_64
        find . -name "Makefile" -execdir sed -i -e "s|-I/usr/lib/mpich2//include|-I%{_includedir}/mpich2-x86_64/|" -e "s|\(ARCH=\).*|\1x86_64|" '{}' \;
        find . -name "Makefile" -execdir sed -i -e "s|\(CFLAGS=\).*|\1%{optflags}|" -e "s|\(FFLAGS=\).*|\1%{optflags} -I%{_includedir}/gfortran/modules|"'{}' \;
        export MPICHLIBPATH="-L%{_libdir}/mpich2/lib/"
        export MPICHLIBS="-lmpichf -lmpich -lgm"
    # not needed when using mpich2
    # export OPENMPIINC="%{_includedir}/openmpi-x86_64/"
    # export OPENMPILIBPATH="-L%{_libdir}/openmpi/lib"
    %endif
    %ifarch %{ix86}
        find . -name "Makefile" -execdir sed -i "s|-I/usr/lib/mpich2//include|-I%{_includedir}/mpich2-i386/|"  -e "s|\(ARCH=\).*|\1i386|" '{}' \;
        find . -name "Makefile" -execdir sed -i -e "s|\(CFLAGS=\)-I/usr/local/include|\1%{optflags}|" -e "s|\(FFLAGS=\).*|\1%{optflags} -I%{_includedir}/gfortran/modules|"'{}' \;
        export MPICHLIBPATH="-L%{_libdir}/mpich2/lib/"
        export MPICHLIBS="-lmpichf -lmpich -lgm"
    # not needed when using mpich2
    # export OPENMPIINC="%{_includedir}/openmpi-i386/"
    # export OPENMPILIBPATH="-L%{_libdir}/openmpi/lib"
    %endif
    make -j1
popd

# build PALM_MP
pushd PALM_MP
   # Hoping to override these, the configure file won't work for us
    %ifarch x86_64
        %configure --with-openmpi=%{_libdir}/openmpi/  --with-mpich=%{_libdir}/mpich2/ --with-fortran_main=MAIN --with-fortran_underscore --with-shared-lib --enable-64bits
        find . -name "Makefile" -execdir sed -i "s|-I/usr/lib/mpich2//include|-I%{_includedir}/mpich2-x86_64/|" '{}' \;
        find . -name "Makefile" -execdir sed -i -e "s|\(CFLAGS=\).*|\1%{optflags}|" -e "s|\(FFLAGS=\).*|\1%{optflags} -I%{_includedir}/gfortran/modules|" '{}' \;
        export MPICHLIBPATH="-L%{_libdir}/mpich2/lib/"
        export MPICHLIBS="-lmpichf -lmpich -lgm"
    # not needed when using mpich2
    # export OPENMPIINC="%{_includedir}/openmpi-x86_64/"
    # export OPENMPILIBPATH="-L%{_libdir}/openmpi/lib"
    %endif
    %ifarch %{ix86}
        %configure --with-openmpi=%{_libdir}/openmpi/  --with-mpich=%{_libdir}/mpich2/ --with-fortran_main=MAIN --with-fortran_underscore --with-shared-lib
        find . -name "Makefile" -execdir sed -i "s|-I/usr/lib/mpich2//include|-I%{_includedir}/mpich2-i386/|" '{}' \;
        find . -name "Makefile" -execdir sed -i -e "s|\(CFLAGS=\).*|\1%{optflags}|" -e "s|\(FFLAGS=\).*|\1%{optflags} -I%{_includedir}/gfortran/modules|" '{}' \;
        export MPICHLIBPATH="-L%{_libdir}/mpich2/lib/"
        export MPICHLIBS="-lmpichf -lmpich -lgm"
    # not needed when using mpich2
    # export OPENMPIINC="%{_includedir}/openmpi-i386/"
    # export OPENMPILIBPATH="-L%{_libdir}/openmpi/lib"
    %endif
    make -j1
popd

%install
# install the PALM_MP
pushd PALM_MP
    make install DESTDIR=$RPM_BUILD_ROOT
popd

# remove .a files
rm -fv $RPM_BUILD_ROOT/%{_libdir}/*.a

# permissions
find PrePALM_MP/ -type f  -name "*.txt" -execdir chmod -v a-x '{}' \;
find PrePALM_MP/ -type f  -name "*.doc" -execdir chmod -v a-x '{}' \;

# remove extra files
rm -vf $RPM_BUILD_ROOT/%{_prefix}/config/*
rmdir -v $RPM_BUILD_ROOT/%{_prefix}/config/

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
install -p -m 0644 $RPM_BUILD_ROOT%{_includedir}/*.* -t $RPM_BUILD_ROOT%{_includedir}/%{name}/
rm -vf $RPM_BUILD_ROOT%{_includedir}/*.*

# correct permissions
chmod a-x $RPM_BUILD_ROOT%{_libdir}/*

install -d $RPM_BUILD_ROOT/%{_bindir}
install -p -m 0755 PrePALM_MP/STEPLANG/steplang.sh $RPM_BUILD_ROOT/%{_bindir}/steplang

install -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/STEPLANG
cp -av PrePALM_MP/STEPLANG/DOC $RPM_BUILD_ROOT/%{_docdir}/%{name}/STEPLANG/
cp -av PrePALM_MP/STEPLANG/EXAMPLES $RPM_BUILD_ROOT/%{_docdir}/%{name}/STEPLANG/

install -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/PrePALM_MP/
cp -av PrePALM_MP/DOC $RPM_BUILD_ROOT/%{_docdir}/%{name}/PrePALM_MP/
cp -av PrePALM_MP/TEMPLATES $RPM_BUILD_ROOT/%{_docdir}/%{name}/PrePALM_MP/
# remove executables from the docs, and scripts in the docs
find PrePALM_MP/training/ -type f -execdir chmod -v a-x '{}' \;
cp -av PrePALM_MP/training $RPM_BUILD_ROOT/%{_docdir}/%{name}/PrePALM_MP/
install -p -m 0644 PrePALM_MP/modif_pour_ppmp_avec_tclsh.txt PrePALM_MP/doc_idcards.txt -t $RPM_BUILD_ROOT/%{_docdir}/%{name}/PrePALM_MP/

install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}/PrePALM_MP/
install -p -m 0755 PrePALM_MP/*.tcl -t $RPM_BUILD_ROOT/%{_datadir}/%{name}/PrePALM_MP/
install -p -m 0644 PrePALM_MP/prepalm_MP.vtp -t $RPM_BUILD_ROOT/%{_datadir}/%{name}/PrePALM_MP/
cp -av PrePALM_MP/IMAGES $RPM_BUILD_ROOT/%{_datadir}/%{name}/PrePALM_MP/
cp -av PrePALM_MP/ALGEBRA $RPM_BUILD_ROOT/%{_datadir}/%{name}/PrePALM_MP/

# install steplang
install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}/PrePALM_MP/STEPLANG/
install -p -m 0644 PrePALM_MP/STEPLANG/steplang-i386 -t $RPM_BUILD_ROOT/%{_datadir}/%{name}/PrePALM_MP/STEPLANG/

pushd $RPM_BUILD_ROOT/%{_docdir}/o-palm/PrePALM_MP/training/session_5/corrige/
    iconv -f iso8859-1 -t utf-8 vecteur_print.ok > vecteur_print.ok.conv && mv -f vecteur_print.ok.conv vecteur_print.ok
popd
pushd $RPM_BUILD_ROOT/%{_docdir}/o-palm/PrePALM_MP/training/chapter_17/unit_tcl/
    iconv -f iso8859-1 -t utf-8 palm.i > palm.i.conv && mv -f palm.i.conv palm.i
popd
pushd $RPM_BUILD_ROOT/%{_docdir}/o-palm/PrePALM_MP/training/chapter_17/unit_python/
    iconv -f iso8859-1 -t utf-8 palm.i > palm.i.conv && mv -f palm.i.conv palm.i
popd
pushd $RPM_BUILD_ROOT/%{_docdir}/o-palm/PrePALM_MP/training/chapter_17/unit_perl/
    iconv -f iso8859-1 -t utf-8 palm.i > palm.i.conv && mv -f palm.i.conv palm.i
popd
pushd $RPM_BUILD_ROOT/%{_docdir}/o-palm/PrePALM_MP/
    iconv -f iso8859-1 -t utf-8 modif_pour_ppmp_avec_tclsh.txt > modif_pour_ppmp_avec_tclsh.txt.conv && mv -f modif_pour_ppmp_avec_tclsh.txt.conv modif_pour_ppmp_avec_tclsh.txt
popd
pushd $RPM_BUILD_ROOT/%{_datadir}/o-palm/PrePALM_MP/ALGEBRA/Interpolation/Geophysic/DSCRIP_lib/
    chmod -v a-x *.F90
popd

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/
cat << EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/prepalm_mp.sh
function prepalm {
    export PREPALMMPDIR=
    $PREPALMMPDIR/prepalm_MP.tcl $∗ &
}
EOF

%files
%defattr(-,root,root,-)
%doc PrePALM_MP/lgpl.txt
%{_bindir}/steplang
%config(noreplace) %{_sysconfdir}/profile.d/prepalm_mp.sh
%{_datadir}/%{name}/

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/*.o
%{_includedir}/%{name}

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}/


%changelog
* Thu Jun 16 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.0.0-1
- Initial rpm build
