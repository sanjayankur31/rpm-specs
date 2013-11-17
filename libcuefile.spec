%global svn_release 475

Name:           libcuefile
Version:        0
Release:        0.1.svn%{svn_release}%{?dist}
Summary:        A stripped down version of cuetools

License:        GPLv2+
URL:            http://www.musepack.net/
Source0:        http://files.musepack.net/source/%{name}_r%{svn_release}.tar.gz

BuildRequires:  cmake
#Requires:       

%description
%{name} is a stripped down version of the original cuetools library. This is
used by the musepack tools.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}_r%{svn_release}

# Correct permissions
find . -name "*.c" -exec chmod 0644 '{}' \;
find . -name "*.h" -exec chmod 0644 '{}' \;
chmod 0644 AUTHORS COPYING README

# Remove quiet build
sed -ibackup '5d' CMakeLists.txt


%build
%cmake .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install 
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
# Remove static lib
rm $RPM_BUILD_ROOT/%{_libdir}/%{name}.a

# Use a different directory. Otherwise, it'll clash with the actual cuetools
# directory
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/%{name}/
cp -v include/cuetools/*.h $RPM_BUILD_ROOT/%{_includedir}/%{name}/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README
%{_libdir}/*.so.*

%files devel
%doc
%{_includedir}/%{name}
%{_libdir}/*.so


%changelog
* Sat Oct 12 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1.svn475
- initial rpm build
