Name:       Random123
Version:    1.08
Release:    3%{?dist}
Summary:    Library of random number generators

License:    BSD
URL:        http://www.deshawresearch.com/resources_random123.html
Source0:    http://www.deshawresearch.com/downloads/download_random123.cgi/%{name}-%{version}.tar.gz

BuildRequires:  doxygen
BuildArch:      noarch

%description
Random123 is a library of "counter-based" random number generators (CBRNGs), in
which the Nth random number can be obtained by applying a stateless mixing
function to N instead of the conventional approach of using N iterations of a
stateful transformation. CBRNGs were originally developed for use in MD
applications on Anton, but they are ideal for a wide range of applications on
modern multi-core CPUs, GPUs, clusters, and special-purpose hardware. Three
families of non-cryptographic CBRNGs are described in a paper presented at the
SC11 conference: ARS (based on the Advanced Encryption System (AES)), Threefry
(based on the Threefish encryption function), and Philox (based on integer
multiplication). They all satisfy rigorous statistical testing (passing
BigCrush in TestU01), vectorize and parallelize well (each generator can
produce at least 264 independent streams), have long periods (the period of
each stream is at least 2128), require little or no memory or state, and have
excellent performance (a few clock cycles per byte of random output). The
Random123 library can be used with CPU (C and C++) and GPU (CUDA and OpenCL)
applications.

%package devel
Summary:   Development files for %{name}
Provides:  %{name} = %{version}-%{release}

%description devel
Random123 is a library of "counter-based" random number generators (CBRNGs), in
which the Nth random number can be obtained by applying a stateless mixing
function to N instead of the conventional approach of using N iterations of a
stateful transformation. CBRNGs were originally developed for use in MD
applications on Anton, but they are ideal for a wide range of applications on
modern multi-core CPUs, GPUs, clusters, and special-purpose hardware. Three
families of non-cryptographic CBRNGs are described in a paper presented at the
SC11 conference: ARS (based on the Advanced Encryption System (AES)), Threefry
(based on the Threefish encryption function), and Philox (based on integer
multiplication). They all satisfy rigorous statistical testing (passing
BigCrush in TestU01), vectorize and parallelize well (each generator can
produce at least 264 independent streams), have long periods (the period of
each stream is at least 2128), require little or no memory or state, and have
excellent performance (a few clock cycles per byte of random output). The
Random123 library can be used with CPU (C and C++) and GPU (CUDA and OpenCL)
applications.

%package doc
Summary:    Documentation for %{name}.

%description doc
Documentation for %{name}

Random123 is a library of "counter-based" random number generators (CBRNGs), in
which the Nth random number can be obtained by applying a stateless mixing
function to N instead of the conventional approach of using N iterations of a
stateful transformation. CBRNGs were originally developed for use in MD
applications on Anton, but they are ideal for a wide range of applications on
modern multi-core CPUs, GPUs, clusters, and special-purpose hardware. Three
families of non-cryptographic CBRNGs are described in a paper presented at the
SC11 conference: ARS (based on the Advanced Encryption System (AES)), Threefry
(based on the Threefish encryption function), and Philox (based on integer
multiplication). They all satisfy rigorous statistical testing (passing
BigCrush in TestU01), vectorize and parallelize well (each generator can
produce at least 264 independent streams), have long periods (the period of
each stream is at least 2128), require little or no memory or state, and have
excellent performance (a few clock cycles per byte of random output). The
Random123 library can be used with CPU (C and C++) and GPU (CUDA and OpenCL)
applications.

%prep
%setup -q


%build
# Header only library
pushd docs
    doxygen Doxyfile
popd

# Wrong file end of line encoding
sed -i 's/\r$//' examples/BUILDVC11.BAT
sed -i 's/\r$//' examples/BUILDVC.BAT

%install
mkdir -p -m 0755 $RPM_BUILD_ROOT/%{_includedir}/%{name}/
cp -a include/Random123/*  $RPM_BUILD_ROOT/%{_includedir}/%{name}/

%files devel
%license LICENSE
%{_includedir}/%{name}/

%files doc
%doc examples

%changelog
* Tue Aug 04 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.08-3
- Update as per reviewer comments in rhbz 1150445

* Fri Jul 31 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.08-2
- Fix doc build errors.

* Wed Jan 08 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.08-1
- Initial rpm build


