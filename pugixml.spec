Name:           pugixml
Version:        1.0
Release:        1%{?dist}
Summary:        A light-weight C++ XML processing library
Group:          Development/Libraries
License:        MIT
URL:            http://pugixml.org

Source0:        http://pugixml.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:         pugixml-1.0-set_lib_soversion.patch

BuildRequires:  cmake

%description
pugixml is a light-weight C++ XML processing library.
It features:
- DOM-like interface with rich traversal/modification capabilities
- Extremely fast non-validating XML parser which constructs the DOM tree from
  an XML file/buffer
- XPath 1.0 implementation for complex data-driven tree queries
- Full Unicode support with Unicode interface variants and automatic encoding
  conversions


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for package %{name}


%prep
%setup -q -c %{name}-%{version}
%patch0


%build
mkdir -p ./build && pushd build
%cmake ../scripts

make


%install
# Fix encodings
#find ./docs -name '*.cpp' -exec dos2unix -k {} \;i
#find ./docs -name '*.css' -exec dos2unix -k {} \;
#find ./docs -name '*.xml' -exec dos2unix -k {} \;
#find ./ -name '*.txt' -exec dos2unix -k {} \;

mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_datadir}/%{name}/contrib
mkdir -p %{buildroot}%{_libdir}

install -p -m 0644 contrib/* %{buildroot}%{_datadir}/%{name}/contrib/
install -p -m 0644 src/*.hpp %{buildroot}%{_includedir}/
install -p -m 0755  build/*.so.* %{buildroot}%{_libdir}/
mv build/*.so %{buildroot}%{_libdir}/


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc readme.txt
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/*
%{_libdir}/*.so
%{_datadir}/%{name}
%{_includedir}/*.hpp


%changelog
* Fri Jul 08 2011 Richard Shaw <hobbes1069@gmail.com> - 1.0-1
- Initial Release
