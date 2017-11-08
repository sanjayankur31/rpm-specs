# We can't remove libtiff - it's a really old version which doesn't seem to be
# compatible with the version we have in Fedora

%global tarversion 19
%global hg_revision 23
Name:       iv
Version:    3.2b.hines18
Release:    3.hg%{hg_revision}%{?dist}
Summary:    NEURON graphical interface


# src/* LGPLv2+
# autotools stuff is GPLv2+
License:    LGPLv2+ and GPLv2+
URL:        http://www.neuron.yale.edu/neuron/
# the tar keeps getting a version bump, but the configure.in script doesn't.
Source0:    %{name}-hg%{hg_revision}.tar.gz
# Format security corrections
Patch0:     %{name}-%{tarversion}-format-security.patch

BuildRequires:  xorg-x11-server-devel chrpath libtiff-devel imake
BuildRequires:  libX11-devel automake autoconf libtool libXext-devel

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

#%package static
#Summary:    Static libraries for %{name}
#Requires: %{name}%{?_isa} = %{version}-%{release}

#%description static
#Static libraries for %{name}

%prep
%setup -q -n %{name}
%patch0
#Remove executable perms from source files
find . -name "*.cpp" -exec chmod -x '{}' \;
find . -name "*.c" -exec chmod -x '{}' \;
find . -name "*.h" -exec chmod -x '{}' \;
find . -name "*.bm" -exec chmod -x '{}' \;
find . -name "*.la" -exec rm -f '{}' \;
chmod -x README Copyright

%build
./build.sh
%configure --with-x CXXFLAGS="$CXXFLAGS -std=c++98"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

rm -fv %{buildroot}/%{_libdir}/*.la
chrpath --delete %{buildroot}%{_bindir}/i*

# Don't need to install these - nothing else uses them
rm -rf %{buildroot}/%{_includedir}/TIFF

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license Copyright
%doc README 
%{_bindir}/i*
%{_libdir}/*.so.*
%dir %{_datadir}/app-defaults
%{_datadir}/app-defaults/Idemo
%{_datadir}/app-defaults/InterViews
%{_datadir}/app-defaults/Doc

%files devel
%{_includedir}/Dispatch/
%{_includedir}/IV-2_6/
%{_includedir}/IV-X11/
%{_includedir}/IV-look/
%{_includedir}/InterViews/
%{_includedir}/OS/
%{_includedir}/*.h
%{_libdir}/*.so

#%files static
#%{_libdir}/*.la
#

%changelog
* Mon May 2 2016 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.2b.hines18-3.hg23
- https://bugzilla.redhat.com/show_bug.cgi?id=1150441
- Update as per review comments
- Fix licensing
- Add comment explaining libtiff inclusion
- Remove static library
- only use buildroot
- build from latest hg sources

* Fri Jul 31 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.2b.hines18-2
- New tar release, but no version bump

* Wed Oct 08 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.2b.hines18-1
- New build

* Tue Feb 18 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.2b.hines18-1
- Initial rpm build
