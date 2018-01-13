Name:       Slicer
Version:    4.8.1
Release:    1%{?dist}
Summary:    Multi-platform, free open source software for visualization and image computing

%global gittag v%{version}

License:    BSD and Apache and LGPL2
URL:        https://www.slicer.org/
Source0:    https://github.com/%{name}/%{name}/archive/%{gittag}/%{name}-%{version}.tar.gz

# https://www.slicer.org/wiki/Documentation/Nightly/Developers/Build_Instructions#Linux
BuildRequires: cmake qt5-devel gcc-c++ vtk-devel doxygen xorg-x11-server-devel
BuildRequires: libXt-devel mesa-libGL-devel libXrender-devel ncurses-devel
# Why do they need these for building it?
BuildRequires: subversion git-core

%description
3D Slicer is an open source software platform for medical image informatics,
image processing, and three-dimensional visualization. Built over two decades
through support from the National Institutes of Health and a worldwide
developer community, Slicer brings free, powerful cross-platform processing
tools to physicians, researchers, and the general public.

%prep
%autosetup -n %{name}-%{version}

%build

# Fails if one doesn't do this
mkdir build
pushd build
    %cmake -DSlicer_USE_SYSTEM_QT:BOOL=1 ..
    make %{?_smp_mflags}
popd


%install
pushd build
    %make_install
popd


%files
%doc
%license



%changelog
* Fri Jan 12 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.8.1-1
- Initial build
