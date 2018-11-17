# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2 0
%endif

# disabled to begin with
%bcond_with tests

%global desc %{expand: \
Stimfit is a free, fast and simple program for viewing and analyzing
electrophysiological data. It features an embedded Python shell that allows you
to extend the program functionality by using numerical libraries such as NumPy
and SciPy. A standalone Python module for file i/o that does not depend on the
graphical user interface is also available.

Please cite the following publication when you use Stimfit for your research:

Guzman SJ, Schlögl A, Schmidt-Hieber C (2014) Stimfit: quantifying
electrophysiological data with Python. Front Neuroinform 
doi:10.3389/fninf.2014.00016}


Name:           stimfit
Version:        0.15.8
Release:        1%{?dist}
Summary:        Program and tools for viewing and analyzing electrophysiological data

License:        MIT
URL:            https://github.com/neurodroid/%{name}
Source0:        https://github.com/neurodroid/%{name}/archive/v%{version}windows/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
# Not yet packaged
# BuildRequires:  biosig4c++-devel
BuildRequires:  hdf5-devel

%description
%{desc}

%if %{with py2}
%package -n python2-%{name}
Summary:        %{summary}
BuildRequires:  python2-devel
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
%{desc}
%endif

%package -n python3-%{name}
Summary:        %{summary}
BuildRequires:  python3-devel
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
%{desc}


%prep
%autosetup -n -c %{name}-%{version}
%if %{with py2}
cp -r %{name}-%{version}windows %{name}-%{version}windows-py2
%endif

%build
pushd %{name}-%{version}windows
    ./autogen.sh
    export PYTHON_VERSION=%{python3_version}
    %configure --enable-python --with-biosig
    %{make_build}
popd

%if %{with py2}
pushd %{name}-%{version}windows-py2
    ./autogen.sh
    export PYTHON_VERSION=%{python3_version}
    %configure --enable-python --with-biosig
popd
%endif
%install
pushd %{name}-%{version}windows
    %{make_install}
popd

%if %{with py2}
pushd %{name}-%{version}windows-py2
    %{make_install}
popd
%endif

%check

%files
%license COPYING
%doc README.md NEWS AUTHORS ChangeLog BUGS


%if %{with py2}
%files -n python2-%{name}
%license COPYING
# %{python2_sitelib}/*
%endif

%files -n python3-%{name}
%license COPYING
# %{python3_sitelib}/*
%{_bindir}/sample-exec

%changelog
* Sat Nov 17 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.15.8-1
- Initial build
