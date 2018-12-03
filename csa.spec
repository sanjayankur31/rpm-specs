%global desc %{expand: \
The CSA library provides elementary connection-sets and operators for combining
them. It also provides an iteration interface to such connection-sets enabling
efficient iteration over existing connections with a small memory footprint
also for very large networks. The CSA can be used as a component of neuronal
network simulators or other tools.

See the following reference for more information:

Mikael Djurfeldt (2012) "The Connection-set Algebra---A Novel Formalism for the
Representation of Connectivity Structure in Neuronal Network Models"
Neuroinformatics 10(3), 1539-2791, http://dx.doi.org/10.1007/s12021-012-9146-1}


# Python2 support
%bcond_with py2


Name:       csa
Version:    0.1.8
Release:    1%{?dist}
Summary:    The Python implementation of the Connection-Set Algebra

License:    GPLv3
URL:        https://github.com/INCF/csa
Source0:    https://github.com/INCF/csa/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  libneurosim-devel

BuildRequires:  python2-devel
BuildRequires:  python3-devel

%description
%{desc}


%prep
%autosetup -c %{name}-%{version}

%if %{with py2}
cp -r %{name}-%{version} %{name-version}-py2
%endif

%build
pushd %{name}-%{version}
export PYTHON=%{__python3}
./autogen.sh
%configure
make %{?_smp_mflags}
popd

%if %{with py2}
pushd %{name}-%{version}-py2
export PYTHON=%{__python2}
./autogen.sh
%configure
make %{?_smp_mflags}
popd
%endif


%install
pushd %{name}-%{version}
export PYTHON=%{__python3}
%make_install
popd

%if %{with py2}
export PYTHON=%{__python2}
pushd %{name}-%{version}-py2
%make_install
popd
%endif

%files
%license COPYING
%doc INSTALL NEWS RELEASE AUTHORS ChangeLog



%changelog
* Mon Dec 03 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.8-1
- Initial build
