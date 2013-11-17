# Only creates static libraries! :/

Name:           libtpcmisc
Version:        1.4.8
Release:        3%{?dist}
Summary:        Miscellaneous PET functions

License:        LGPLv2+
URL:            http://www.turkupetcentre.net/software/libdoc/%{name}/index.html
Source0:        http://www.turkupetcentre.net/software/libsrc/%{name}_1_4_8_src.zip

BuildRequires:  doxygen dos2unix graphviz


%description
Former libpet, the common PET C library, has been divided up in 
smaller sub-libraries that each handle a specific task. 
This library includes miscellaneous functions utilized in PET 
data processing.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}
sed -i "/^CFLAGS/d" Makefile

# Fix encodings and line endings.
dos2unix -k History Readme
iconv -f ISO_8859-1 -t utf8 -o History.new History && mv -f History.new History


%build
# c99 standard since they use declarations in the for loops
export CFLAGS="%{optflags} -std=c99"
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
%doc History Readme
%{_bindir}/%{name}

%files devel
%doc doc/%{name}/*
%{_libdir}/%{name}.a
%{_includedir}/*

%changelog
* Mon Aug 01 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.8-3
- Add graphviz to BR

* Sun Jul 31 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.8-2
- Changes that Richard made:
- Add more documentation
- Fix line endings and encoding
- Add architecture specific requires
- https://bugzilla.redhat.com/show_bug.cgi?id=714326#c2

* Fri Jun 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.8-1
- initial rpm build
