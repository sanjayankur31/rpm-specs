# Tests do not pass, and the output isn't clear as to why
%bcond_with tests

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

%if %{with tests}
BuildRequires:  gtest-devel
BuildRequires:  boost-devel
BuildRequires:  qt5-qtbase-devel
%endif

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup
%if %{with tests}
# Remove syslog test
# We dont have syslog any more by default
# https://fedoraproject.org/wiki/Changes/NoDefaultSyslog
rm test/syslog-test.h
sed -i '/syslog-test.h/ d' test/main.cc
%endif


%build
%if %{with tests}
%cmake -Dtest=ON .
%else
%cmake .
%endif

%make_build


%install
%make_install

%if %{with tests}
%check
make test
%endif


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
