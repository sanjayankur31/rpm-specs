%global _description %{expand: \
A wrapper around Armadillo which provides a Newmat style API.
The current version of armawrap is written against:

- newmat10D
- Armadillo 5.200

Please cite:

Conrad Sanderson.
Armadillo: An Open Source C++ Linear Algebra Library for
Fast Prototyping and Computationally Intensive Experiments.
Technical Report, NICTA, 2010.
}

Name:           armawrap
Version:        0.2.2
Release:        1%{?dist}
Summary:        A wrapper around Armadillo which provides a Newmat style API

License:        ASL and MPLv2.0
URL:            https://git.fmrib.ox.ac.uk/fsl/armawrap
Source0:        https://git.fmrib.ox.ac.uk/fsl/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz
# Disable newmat tests
Patch0:         0001-armawrap-disable-newmat-tests.patch

BuildRequires:  gcc-c++
BuildRequires:  lapack-devel
BuildRequires:  blas-devel
BuildRequires:  armadillo-devel
BuildArch:      noarch

%description
%{_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -S patch -p0
# Remove bundled armadillo
rm -rf armawrap/armadillo_bits armawrap/armadillo-5.200.1

%build

%install
install -p -m 0644 -D -t $RPM_BUILD_ROOT/%{_includedir}/%{name} %{name}/*

%check
pushd tests && ./run_tests.sh && popd


%files devel
%license LICENSE
%doc README.rst CHANGELOG.rst
%{_includedir}/%{name}


%changelog
* Sun Dec 30 2018 Ankur Sinha <sanjay.ankur@gmail.com>
- Initial build
