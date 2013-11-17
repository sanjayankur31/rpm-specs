Name:           libtpcimgio
Version:        1.5.10
Release:        3%{?dist}
Summary:        Turku PET Centre for image file input and output procedures

License:        LGPLv2+
URL:            http://www.turkupetcentre.net/software/libdoc/%{name}/index.html
Source0:        http://www.turkupetcentre.net/software/libsrc/%{name}_1_5_10_src.zip
Patch0:         %{name}-add-header.patch
BuildRequires:  libtpcmisc-devel
BuildRequires:  doxygen dos2unix
BuildRequires:  graphviz


%description
The libtpcimgio library is a collection of commonly used C files 
in Turku PET Centre for image file input and output procedures. 
Libtpcimgio library supports Analyze 7.5, Ecat 6.x, Ecat 7.x and 
partly interfile formats.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}
%patch0 -p1
sed -i "/^CFLAGS/d" Makefile

# Fix encodings and line endings.
dos2unix -k History Readme TODO
iconv -f ISO_8859-1 -t utf8 -o History.new History && mv -f History.new History


%build
# c99 standard since they use declarations in the for loops
# includedirs since it doesn't find them on their own
# the _XOPEN_SOURCE for timezone declaration
# undefine STRICT_ANSI since c99 sets it, and it conflicts with the strings.h declaration

export CFLAGS="%{optflags} -std=c99 -Iinclude/ -I%{_includedir}/libtpcmisc/ -D_XOPEN_SOURCE -U__STRICT_ANSI__"
export CXXFLAGS="%{optflags}"
make %{?_smp_mflags}

# Build doxygen documentation
mkdir doc
( cat Doxyfile ; echo "OUTPUT_DIRECTORY=./doc" ) | doxygen -


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
install -d $RPM_BUILD_ROOT%{_bindir}

install -p -m 0755 %{name} -t $RPM_BUILD_ROOT%{_bindir}/
install -p -m 0644 %{name}.a -t $RPM_BUILD_ROOT%{_libdir}/
install -p -m 0644 include/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/

%files
%doc History Readme TODO
%{_bindir}/%{name}

%files devel
%doc doc/%{name}/*
%{_libdir}/%{name}.a
%{_includedir}/*

%changelog
* Mon Aug 01 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5.10-3
- Add graphviz to BR

* Sun Jul 31 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5.10-2
- Changes that Richard made:
- Add more documentation
- Fix line endings and encoding
- Add architecture specific requires
- https://bugzilla.redhat.com/show_bug.cgi?id=714327#c1

* Fri Jun 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.5.10-1
- initial rpm build
