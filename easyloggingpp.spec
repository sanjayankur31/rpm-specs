Name:           easyloggingpp
Version:        9.96.7
Release:        1%{?dist}
Summary:        Single header C++ logging library

License:        MIT
URL:            https://zuhd.org/products/easyloggingpp
Source0:        https://github.com/zuhd-org/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
Easylogging++ is single header efficient logging library for C++ applications.
It is extremely powerful, highly extendable and configurable to user's
requirements.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup


%build
%configure --disable-static
%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
# %license add-license-file-here
# %doc add-main-docs-here
# %{_libdir}/*.so.*

%files devel
# %doc add-devel-docs-here
# %{_includedir}/*
# %{_libdir}/*.so


%changelog
* Sun Jan 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 9.96.7-1
- Initial build

