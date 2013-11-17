%global commit 421f879c6478ec23ea4e398fb47f8a621ff784e6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Name:           odeint
Version:        2.2
Release:        3%{?dist}
Summary:        A C++ library for numerically solving Ordinary Differential Equations

License:        Boost
URL:            http://headmyshoulder.github.com/%{name}-v2/index.html

# Upstream gives release tarballs
Source0:        https://github.com/headmyshoulder/%{name}-v2/archive/%{commit}/%{name}-v2-%{version}.tar.gz

BuildArch:      noarch


%description
%{summary}

%package devel
Summary:    A C++ library for numerically solving Ordinary Differential Equations
# For the headers that odeint includes
# Checked a few files, hopefully this has all of the required headers
Requires:   boost-devel
Provides:   %{name}-static = %{version}-%{release}

%description devel
Odeint is a modern C++ library for numerically solving Ordinary Differential
Equations. It is developed in a generic way using Template Metaprogramming
which leads to extraordinary high flexibility at top performance. The numerical
algorithms are implemented independently of the underlying arithmetic. This
results in an incredible applicability of the library, especially in
non-standard environments. For example, odeint supports matrix types, arbitrary
precision arithmetic and even can be easily run on CUDA GPUs - check the
Highlights to learn more.

Moreover, odeint provides a comfortable easy-to-use interface allowing for a
quick and efficient implementation of numerical simulations. Visit the
impressively clear 30 lines Lorenz example.

Odeint was accepted in Boost 1.53 and this package will be obsoleted when the
Fedora boost libraries are updated.

%package doc
Summary:    Documentation for %{name}
Requires:    %{name}-devel = %{version}-%{release}
%description doc
%{summary}

%prep
%setup -qn %{name}-v2-%{commit}


%build
# Nothing to build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_includedir}/boost/numeric/
cp -prv boost/numeric/* $RPM_BUILD_ROOT/%{_includedir}/boost/numeric/

# Docs
# Skip tests and performance etc
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/
cp -prv libs/numeric/odeint/* $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/

%files devel
%doc README CHANGELOG
%{_includedir}/boost/numeric/odeint.hpp
%{_includedir}/boost/numeric/odeint/

%files doc
%{_docdir}/%{name}-%{version}/

%changelog
* Sun May 05 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 2.2-3
- Make doc package require devel
- Change sourceURL

* Fri May 03 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 2.2-2
- Update package as per review requirements
- Remove extra stuff from main package
- Rename docs to doc
- Correct spelling error
- Add static requires to devel
- Could not remove requires from main package since adding a dep on -devel in
  doc gives the rpm lint "devel dependency" error.

* Sun Jan 27 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 2.2-1
- Add boost requires
- Shorten description
- Correct source url, versioning
- Initial rpmbuild

