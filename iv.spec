%global tarversion 19
Name:       iv
Version:    3.2b.hines18
Release:    3%{?dist}
Summary:    NEURON graphical interface

License:    GPLv2+ and GPLv3+
URL:        http://www.neuron.yale.edu/neuron/
# the tar keeps getting a version bump, but the configure.in script doesn't.
Source0:    http://www.neuron.yale.edu/ftp/neuron/versions/v7.5/%{name}-%{tarversion}.tar.gz

BuildRequires:  xorg-x11-server-devel
BuildRequires:  chrpath
BuildRequires:  libtiff-devel
BuildRequires:  imake
BuildRequires:  gcc-c++

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
%{autosetup} -n %{name}-%{tarversion}
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
#%%make_build
make

%install
%make_install

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
* Sun Aug 26 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 3.2b.hines18-3
- Include g++ BR
- Remove included patch
- Use autosetup

* Fri Jul 31 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.2b.hines18-2
- New tar release, but no version bump

* Wed Oct 08 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.2b.hines18-1
- New build

* Tue Feb 18 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.2b.hines18-1
- Initial rpm build
