Name:           easyloggingpp
Version:        9.96.7
Release:        1%{?dist}
Summary:        Single header C++ logging library

License:        MIT
URL:            https://zuhd.org/products/easyloggingpp
Source0:        https://github.com/zuhd-org/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch


%description
Easylogging++ is single header efficient logging library for C++ applications.
It is extremely powerful, highly extendable and configurable to user's
requirements.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  cmake
BuildRequires:  gcc-c++
# For test
BuildRequires:  gtest-devel
BuildRequires:  boost-devel
BuildRequires:  qt5-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup


%build
%cmake -Dtest=ON .
%make_build


%install
%make_install

# %check
# make test
# Tries to write to /var/log/syslog in a test and fails.


%files devel
%license LICENSE
%doc README.md doc/ CHANGELOG.md
%{_includedir}/easylogging++.h
# cc file is required
%{_includedir}/easylogging++.cc
%{_datadir}/pkgconfig/%{name}.pc


%changelog
* Sun Jan 20 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 9.96.7-1
- Initial build
