%global _description %{expand:
libb64 is a library of ANSI C routines for fast encoding/decoding data into and
from a base64-encoded format. C++ wrappers are included, as well as the source
code for standalone encoding and decoding executables.

Base64 uses a subset of displayable ASCII characters, and is therefore a useful
encoding for storing binary data in a text file, such as XML, or sending binary
data over text-only email.}


Name:           libb64
Version:        1.2
Release:        1%{?dist}
Summary:        A library for fast encoding/decoding data into and from a base64-encoded format

License:        Public Domain
URL:            http://libb64.sourceforge.net/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.src.zip


BuildRequires: gcc-c++

%description
%{_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Upstream only provides a static library
Provides:      %{name}-static = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup


%build
export "CFLAGS=%{optflags}"
export "CXXFLAGS=%{optflags}"
export "LDFLAGS=%{build_ldflags}"
%make_build


%install
# Upstream doesn't provide any install bits in the Makefile
# static lib
install -D -m 0644 -p src/libb64.a $RPM_BUILD_ROOT/%{_libdir}/libb64.a
# binary
install -D -m 0755 -p base64/base64 $RPM_BUILD_ROOT/%{_bindir}/base64
# headers
install -D -m 0644 -p -t $RPM_BUILD_ROOT/%{_includedir}/b64/  include/b64/*

# Only static, so we don't need ldconfig scriptlets

%files
%license LICENSE
%doc AUTHORS README TODO
%{_bindir}/base64


%files devel
%license LICENSE
%{_includedir}/b64
%{_libdir}/libb64.a

%changelog
* Sat Nov 03 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.2-1
- Initial build
