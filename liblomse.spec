Name:           liblomse
Version:        0.14.0
Release:        1%{?dist}
Summary:        A free library to render and edit music scores

License:        BSD
URL:            https://launchpad.net/lomse
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}.tar.gz

# Remove bundled agg references
Patch0:         %{name}-cmake.patch

BuildRequires:  cmake freetype-devel boost-devel zlib-devel libpng-devel
BuildRequires:  unittest-cpp-devel agg-devel

%description
Lomse is a project designed to provide software developers with a library to
add capabilities to any program for rendering, editing and playing back music
scores.

Lomse library hopes to boundle all stuff needed for rendering, editing and
playing back scores, and to be simple enough for newbie programmers but
sophisticated enough to create great applications for musicians. It is written
in C++ and it is free open source and platform independent. It is based on the
experience gained developing the LenMus Phonascus program. Lomse stands for
"LenMus Open Music Score Edition Library".

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
rm -rf src/agg
%patch0 -p0

# Fix agg includes
sed -i-backup 's|#include "agg_|#include "agg2/agg_|' src/render/lomse_font_freetype.cpp src/render/lomse_screen_drawer.cpp include/*.h
sed -i-backup 's|#include <ft2build.h>|#include "ft2build.h"|' include/lomse_font_freetype.h


%build
%cmake -G "Unix Makefiles" -DFREETYPE_INCLUDE_DIRS=%{_includedir}/freetype2/freetype . 
#make %{?_smp_mflags}
make


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc
%{_libdir}/*.so.*

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Wed Feb 12 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.14.0-1
- Initial rpm build

* Wed Feb 12 2014 Ankur Sinha <sanjay.ankur@gmail.com>
- 
