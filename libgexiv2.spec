Name:           libgexiv2
Version:        0.5.0
Release:        3%{?dist}
Summary:        Gexiv2 is a GObject-based wrapper around the Exiv2 library

Group:          System Environment/Libraries
License:        GPLv2
URL:            http://trac.yorba.org/wiki/gexiv2 
Source0:        http://yorba.org/download/gexiv2/0.5/%{name}-%{version}.tar.xz


BuildRequires:  exiv2-devel gobject-introspection-devel libtool

%description
libgexiv2 is a GObject-based wrapper around the Exiv2 library. 
It makes the basic features of Exiv2 available to GNOME applications.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       vala

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
CFLAGS="%{optflags}"; export CFLAGS
CXXFLAGS="%{optflags}"; export CXXFLAGS
FFLAGS="%{optflags} -I/usr/lib64/gfortran/modules"; export FFLAGS
LDFLAGS="-Wl,-z,relro"; export LDFLAGS

# it is not an autotool generated configure script
./configure --release --enable-introspection --prefix=/usr
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT LIB=%{_lib}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING MAINTAINERS 
%{_libdir}/libgexiv2.so.*

%files devel
%{_includedir}/gexiv2/
%{_libdir}/libgexiv2.so
%{_libdir}/pkgconfig/gexiv2.pc
%{_datadir}/vala/vapi/gexiv2.vapi

%{_datadir}/gir-1.0/GExiv2-0.4.gir
%{_libdir}/girepository-1.0/GExiv2-0.4.typelib


%changelog
* Mon Mar 11 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.0-3
- Enable introspection for py support
- add new files for introspection

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 06 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.0-1
- Update to 0.5.0
- rhbz#890402

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.4.1-2
- rebuild (exiv2)

* Tue Apr 03 2012 Kalev Lember <kalevlember@gmail.com> - 0.4.1-1
- Update to 0.4.1

* Thu Feb 23 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.91-1
- Update to 0.3.91
- rhbz #796278
- remove patches

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.2.2-3
- rebuild (exiv2)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.2.2-1
- 0.2.2
- exiv2-0.21 patch

* Tue Aug 24 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.0-1
- update to latest upstream release

* Sun Aug 08 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.90-1
- update to latest upstream release

* Tue Jul 13 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.0-1
- update to latest upstream release

* Mon Jun 14 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.91-2
- changed file section so package owns the directory containing headers too

* Fri Jun 11 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.91-1
- updated to latest release
- removed patch - it was included in this release

* Sat Jun 05 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-5
- changed configure macro as per bug report comment

* Sat Jun 05 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-4
- changed configure portion
- added Requires:  vala for devel
- made the file section more precise
- bugzilla #599097 
- changed patch to include a default LIB setting

* Fri Jun 04 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-3
- patched makefile

* Thu Jun 03 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-2
- some fixes in spec
- moved *.vapi to devel
- removed INSTALL from doc
- added comment to yorba ticket link
- corrected typo in description

* Wed Jun 02 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-1
- initial rpmbuild
