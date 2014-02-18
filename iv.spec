Name:       iv
Version:    3.2b.hines18
Release:    1%{?dist}
Summary:    NEURON graphical interface

License:    GPLv2+ and GPLv3+
URL:        http://www.neuron.yale.edu/neuron/
Source0:    http://www.neuron.yale.edu/ftp/neuron/versions/v7.3/%{name}-18.tar.gz
#Source0:    ftp://ftp.sgi.com/graphics/interviews/%{version}.tar.Z
# Format security corrections
Patch0:     %{name}-18-format-security.patch

BuildRequires:  xorg-x11-server-devel chrpath libtiff-devel imake
#Requires:    

%description
InterViews is a native C++ toolkit for X Windows developed by Mark Linton and
his team at Stanford University and later Silicon Graphics. The last major
release was InterViews 3.1 in 1993, and included the Unidraw drawing editor
application framework which was the basis of John Vlissides' thesis work at
Stanford. InterViews also has lightweight glyphs with switchable look-and-feel
(Apple monochrome, Motif, OpenLook, and SGI Motif). It has been ported to most
any Unix which runs X11. Other programmers known to have worked on InterViews
include Paul Calder, John Interrante, Steven Tang, and Scott Stanton. 

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
%setup -q -n %{name}-18
%patch0
#Remove executable perms from source files
find . -name "*.cpp" -exec chmod -x '{}' \;
find . -name "*.c" -exec chmod -x '{}' \;
find . -name "*.h" -exec chmod -x '{}' \;
find . -name "*.bm" -exec chmod -x '{}' \;
find . -name "*.la" -exec rm -f '{}' \;
chmod -x README Copyright

#rm -rf include/TIFF
#rm -rf src/lib/TIFF #src/lib/OS



%build
%configure --with-pic --enable-shared=yes --enable-static=no --disable-rpath --with-x
#make %{?_smp_mflags}
make

%install
make install DESTDIR=%{buildroot}

# Cannot remove static libraries. Required by neuron
## rm -fv %{buildroot}/%{_libdir}/*.la
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/i*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README Copyright
%{_bindir}/i*
%{_libdir}/*.so.*
%{_datadir}/app-defaults/Doc
%{_datadir}/app-defaults/Idemo
%{_datadir}/app-defaults/InterViews

%files devel
%{_includedir}/Dispatch/
%{_includedir}/IV-2_6/
%{_includedir}/IV-X11/
%{_includedir}/IV-look/
%{_includedir}/InterViews/
%{_includedir}/OS/
%{_includedir}/TIFF/
%{_includedir}/*.h
%{_libdir}/*.so

%files static
%{_libdir}/*.la

%changelog
* Tue Feb 18 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.2b.hines18-1
- Initial rpm build
