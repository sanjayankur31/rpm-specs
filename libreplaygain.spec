%global svn_release 475

Name:           libreplaygain
Version:        0
Release:        0.1.20110810svn%{svn_release}%{?dist}
Summary:        Gain analysis library from musepack

License:        LGPLv2+
URL:            http://www.musepack.net/index.php
Source0:        http://files.musepack.net/source/%{name}_r%{svn_release}.tar.gz

BuildRequires:  cmake

%description
Gain analysis library used by Musepack utilities and libraries


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}_r%{svn_release}

# Correct permissions and end of line
chmod 0644 include/replaygain/*.h src/gain_analysis.c
sed -ibackup 's/\r$//' include/replaygain/*.h src/gain_analysis.c

# Don't let it override the compiler flags
# Don't make the build quiet
sed '5,9d' -ibackup CMakeLists.txt


%build
%cmake .
make %{?_smp_mflags}


%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
# Remove static lib
rm $RPM_BUILD_ROOT/%{_libdir}/%{name}.a

mkdir -p $RPM_BUILD_ROOT/%{_includedir}/replaygain/
cp -v include/replaygain/*.h $RPM_BUILD_ROOT/%{_includedir}/replaygain/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/replaygain
%{_libdir}/*.so


%changelog
* Sat Oct 19 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1.20110810svn475
- Update as per review: #1018541
- Update version
- Remove unrequired portions
- File inclusions
- Initial rpmbuild

