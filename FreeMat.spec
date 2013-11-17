%global svn_rev 4218
%global date_check_out 20110731
Name:           FreeMat
Version:        4.1
Release:        0.2.%{date_check_out}svn%{svn_rev}%{?dist}
Summary:        An environment for rapid engineering, scientific prototyping and data processing
License:        GPLv2+
URL:            http://freemat.sourceforge.net/index.html

# svn export -r 4218 https://freemat.svn.sourceforge.net/svnroot/freemat/trunk/FreeMat FreeMat
# tar -cvzf FreeMat-%{version}.tar.gz FreeMat/
Source0:        %{name}-%{date_check_out}.tar.gz

# https://sourceforge.net/tracker/?func=detail&aid=2026594&group_id=91526&atid=597448
# From the tracker
Source1:        %{name}.desktop

# https://sourceforge.net/tracker/?func=detail&aid=2026590&group_id=91526&atid=597448
# Man page
Source2:        FreeMat.1

# Correct install directory
# Place blas.ini in correct location
Patch0:         0001-%{name}-%{version}-CMakeLists.patch

BuildRequires:  fftw-devel
BuildRequires:  cmake
BuildRequires:  qt-creator
BuildRequires:  blas-devel
BuildRequires:  llvm-devel
BuildRequires:  boost-devel
BuildRequires:  ncurses-devel readline-devel
BuildRequires:  volpack-devel
BuildRequires:  levmar-devel
BuildRequires:  suitesparse-devel
BuildRequires:  portaudio-devel
BuildRequires:  lapack-devel
BuildRequires:  zlib-devel
BuildRequires:  pcre-devel
BuildRequires:  flex
BuildRequires:  libffi-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  clang-devel
BuildRequires:  vtk-devel
BuildRequires:  desktop-file-utils
BuildRequires:  qt-webkit-devel
BuildRequires:  libxml2-devel
BuildRequires:  arpack-devel
BuildRequires:  atlas-devel

# When the include dir bug is fixed
# https://sourceforge.net/tracker/?func=detail&aid=3384982&group_id=91526&atid=597446
# BuildRequires:  InsightToolkit-devel

Requires:   %{name}-data = %{version}-%{release}

%description
FreeMat is a free environment for rapid engineering,
scientific prototyping and data processing.

%package doc
BuildArch:  noarch
Summary:    Documentation for %{name}
Requires:   %{name} = %{version}-%{release}

%description doc
The package contains documentation files related to %{name}.

%package data
BuildArch:  noarch
Summary:    Data files related to %{name}
Requires:   %{name} = %{version}-%{release}

%description data
This package contains data files for %{name}.

%prep
%setup -q -n %{name}

############################ Patches ###############################
%patch0 -b.orig

########################### Fix header #############################
sed -i '24 a\
#include <GL/glu.h>' libs/libGraphics/GLRenderEngine.cpp

sed -i "s/lm\.h/levmar\.h/" libs/libFN/OptFun.cpp

########## Fix library names, since we are using fedora ones #######
sed -i \
-e "s/arpack_c/arpack/" \
-e "s/lapack_c/lapack/" \
src/CMakeLists.txt

#-e "s/blasref/blas/" \
#-e "s/dynblas//" \

#################### remove bundled libraries #######################

# libDynBlas does not appear to be a bundled library

# Modified, the fedora blas does not make the cut
# rm -rf libs/libMath/libBLAS_C
# sed -i "/libBLAS_C/d" libs/libMath/CMakeLists.txt

rm -rf dependencies
rm -rf libs/thirdparty/

rm -rf libs/libFN/levmar-2.3
sed -i "/ADD_SUBDIRECTORY/d" libs/libFN/CMakeLists.txt

rm -rf libs/libMath/libARPACK_C
sed -i "/libARPACK_C/d" libs/libMath/CMakeLists.txt

rm -rf libs/libMath/libLAPACK_C
sed -i "/libLAPACK_C/d" libs/libMath/CMakeLists.txt

############## Correct permissions ##################################
chmod a-x libs/libFN/Interp2D.cpp


############# Modify the blas.ini file just a tad bit as per upstream
# suggestions
sed -i "s/libblas.so/libcblas.so/" tools/blas.ini


%build
# libffi does not install headers to includedir
# The naming of the sonames are too generic. Link statically to binary
%cmake -DFORCE_SYSTEM_LIBS=ON \
-DFFI_INCLUDE_DIR:PATH=%{_libdir}/libffi-3.0.9/include/ \
-DBUILD_SHARED_LIBS=OFF \
-DUSE_VTK=ON  .
# -DUSE_ITK=ON : fails to build with missing header. Wait for fix
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Install the desktop file
desktop-file-install                                    \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
%{SOURCE1}

# Install the man page
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install -p -m 0644 %{SOURCE2} -t $RPM_BUILD_ROOT%{_mandir}/man1/

# Move docs to correct location
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}/
mv $RPM_BUILD_ROOT/%{_datadir}/%{name}/help/* $RPM_BUILD_ROOT/%{_docdir}/%{name}/
rmdir $RPM_BUILD_ROOT/%{_datadir}/%{name}/help

# correct line endings
sed -i 's/\r//' $RPM_BUILD_ROOT/%{_docdir}/FreeMat/text/*.mdc
# sed -i 's/\r//' $RPM_BUILD_ROOT/%{_datadir}/FreeMat-4.1/toolbox/general/license.m
# mv -v $RPM_BUILD_ROOT/%{_datadir}/FreeMat-4.1/help $RPM_BUILD_ROOT/%{_docdir}/FreeMat-4.1/


# No tests are present


%files
%doc COPYING ChangeLog
%{_bindir}/%{name}
%{_mandir}/man1/FreeMat.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/blas.ini

%files data
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/toolbox/

%files doc
%{_docdir}/%{name}/


%changelog
* Fri Aug 19 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.1-0.2.20110731svn4128
- Make doc package noarch
- Make data package noarch
- Modify blas.ini: Upstream says it's better to use cblas

* Tue Aug 02 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.1-0.1.20110731svn4218
- Correct versioning
- Add a man page
- Add a desktop file
- Correct build
- Remove bundles

* Sun Jul 31 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110731-0.1.svn4218
- Update to latest svn release

* Mon Jul 11 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110620-0.3.svn4185
- fix up BRs
- fix up description 
- fix versioning
- split the package

* Fri Jul 01 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110620-0.2svn4185
- Make corrections as per #715180

* Sat Jun 18 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20110620-0.1svn4185
- initial rpm build
