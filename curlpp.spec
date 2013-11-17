Name: curlpp
Version: 0.7.3
Release: 7%{?dist}
Summary: A C++ wrapper for libcURL

Group: System Environment/Libraries
License: MIT
URL: http://curlpp.org/
Source0: http://curlpp.googlecode.com/files/curlpp-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: boost-devel
BuildRequires: curl-devel

%description
cURLpp is a C++ wrapper for libcURL.


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: boost-devel
Requires: curl-devel
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

# Convert CRLF line endings to LF in the examples
for file in examples/*.cpp
do
	sed 's/\r//' $file > $file.new && \
	touch -r $file $file.new && \
	mv $file.new $file
done

# remove deps on global.h which in turn pulls in config.h
sed -i '28 d' include/curlpp/Types.hpp  

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
#install -p include/curlpp/config.h %{buildroot}%{_includedir}/curlpp/config.h

# Unwanted library files
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a
# Useless header file
# rm -f %{buildroot}%{_includedir}/curlpp/config.win32*


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING CHANGES
%{_libdir}/libcurlpp.so.*
%{_libdir}/libutilspp.so.*


%files devel
%defattr(-,root,root,-)
%doc examples/*.cpp examples/README doc/guide.pdf
%{_bindir}/curlpp-config
%{_includedir}/curlpp/
%{_includedir}/utilspp/
%{_libdir}/libcurlpp.so
%{_libdir}/libutilspp.so
%{_libdir}/pkgconfig/curlpp.pc



%changelog
* Wed Feb 08 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.7.3-7
- remove config.h dependency

* Fri Jan 27 2012 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.7.3-6
- Added missing configuration header file

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.7.3-4
- Changed libcurl-devel dependency to curl-devel for EPEL5 compatibility

* Tue Jul 19 2011 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.7.3-3
- Removed wildcard for selecting pkgconfig file
- Added trailing slash for directories in file listing
- Added doc/guide.pdf to development documentation

* Tue Jul 19 2011 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.7.3-2
- Added boost-devel, libcurl-devel and pkgconfig as requirements to devel
  subpackage.
- Complete line-ending conversion once all steps are done
- Added default file attributes to devel subpackage
- Added verbosity to file selectors

* Mon Jul 18 2011 Veeti Paananen <veeti.paananen@rojekti.fi> - 0.7.3-1
- Initial package.
