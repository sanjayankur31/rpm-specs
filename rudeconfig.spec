Name:           rudeconfig
Version:        5.0.5
Release:        10%{?dist}
Summary:        Library (C++ API) for reading and writing configuration/.ini files
License:        GPLv2+
URL:            http://www.rudeserver.com/config
Source0:        http://www.rudeserver.com/config/download/%{name}-%{version}.tar.bz2

BuildRequires: gcc-c++

%description
%{name} is a library that allows applications to read, modify 
and create configuration/.ini files.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
%{name} is a library that allows applications to read, modify
and create configuration/.ini files. The %{name}-devel package
contains libraries, header files, and documentation needed
to develop C++ applications using %{name}.

%prep
%autosetup

%build
%configure --disable-static
%make_build

%install
%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS README NEWS ChangeLog
%{_libdir}/librudeconfig.so.3
%{_libdir}/librudeconfig.so.3.2.1

%files devel
%dir %{_includedir}/rude
%{_includedir}/rude/config.h
%{_libdir}/librudeconfig.so
%{_mandir}/man3/*

%changelog
* Sat Oct 20 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 5.0.5-10
- Unretire
