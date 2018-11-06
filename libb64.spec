Name:           libb64
Version:        1.2
Release:        3%{?dist}
Summary:        Tool for fast encoding/decoding data into and from a base64-encoded format

License:        Public Domain
URL:            http://libb64.sourceforge.net/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.src.zip


BuildRequires: gcc-c++

%description
Base64 uses a subset of displayable ASCII characters, and is therefore a useful
encoding for storing binary data in a text file, such as XML, or sending binary
data over text-only email.

libb64 is a library of ANSI C routines for fast encoding/decoding data into and
from a base64-encoded format. C++ wrappers are included, as well as the source
code for standalone encoding and decoding executables.

This package provides the %{name}-b64 binary tool for encoding to and decoding
from the Base64 scheme. Please install the %{name}-devel package to develop
software using %{name}.



%package        devel
Summary:        Development files for %{name}
# Upstream only provides a static library
Provides:      %{name}-static = %{version}-%{release}
# Does not need to require the base package as it is complete itself

%description    devel
The %{name}-devel package contains the library and header files for developing
applications that use %{name}.

%prep
%autosetup

# Remove unneeded flags
sed -i '/-O3/ d' src/Makefile
sed -i '/pedantic/ d' src/Makefile


%build
%set_build_flags
%make_build


%install
# Upstream doesn't provide any install bits in the Makefile
# static lib
install -D -m 0644 -p src/libb64.a $RPM_BUILD_ROOT/%{_libdir}/libb64.a
# binary, rename to prevent conflict with coreutils binary
install -D -m 0755 -p base64/base64 $RPM_BUILD_ROOT/%{_bindir}/libb64-base64
# headers
install -D -m 0644 -p -t $RPM_BUILD_ROOT/%{_includedir}/b64/  include/b64/*

# Only static, so we don't need ldconfig scriptlets

%files
%license LICENSE
%doc AUTHORS README
%{_bindir}/libb64-base64


%files devel
%license LICENSE
%{_includedir}/b64
%{_libdir}/libb64.a

%changelog
* Tue Nov 06 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.2-3
- Improve summary and description to mention that the main package only
  provides the tool.
- Rename binary to prevent conflict
- Improve summary and description
- Prevent addition to compiler flags
- Do not require main package from devel
- Do not use empty TODO file

* Sun Nov 04 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.2-2
- Do not use description macro
- Use easier macro for build flags

* Sat Nov 03 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.2-1
- Initial build
