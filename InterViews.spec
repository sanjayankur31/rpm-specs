Name:       InterViews
Version:    17
Release:    1%{?dist}
Summary:    NEURON graphical interface

License:    GPLv2+ and GPLv3+
URL:        http://www.neuron.yale.edu/neuron/
Source0:    http://www.neuron.yale.edu/ftp/neuron/versions/v7.2/iv-17.tar.gz

BuildRequires:  xorg-x11-server-devel chrpath
#Requires:    

%description
NEURON graphical interface

%package devel
Summary:    Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and development shared libraries for the %{name} package


%prep
%setup -q -n iv-%{version}
chmod -x README Copyright


%build
%configure --with-pic --enable-shared=yes --enable-static=no --disable-rpath
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove static libraries
rm -fv %{buildroot}/%{_libdir}/*.la
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

%changelog
* Sun Mar 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 17-1
- Initial rpm build


