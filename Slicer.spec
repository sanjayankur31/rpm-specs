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
# For their build, but we won't use them.
BuildRequires: subversion git-core
# Everything under the Superbuild directory.
BuildRequires: vtk-devel InsightToolkit-devel dcmtk-devel
BuildRequires: curl-devel zlib-devel jsoncpp-devel libarchive-devel
BuildRequires: openssl-devel openigtlink-devel pcre-devel rapidjson-devel
BuildRequires: swig itcl-devel tcl-devel teem-devel tk-devel ctk-devel
# Only seems to support python2 at the moment
# I'd think a lot of these are Requires, rather than BRs, but I'm leaving them
# here for the time being
BuildRequires: python2-devel python2-gitdb python2-smmap
BuildRequires: %{py2_dist numpy appdirs chardet couchdb}
BuildRequires: %{py2_dist GitPython nose packaging pip pydicom}
BuildRequires: %{py2_dist PyGithub pyparsing setuptools six wheel scipy}

# Not yet in Fedora
# https://github.com/Slicer/ParameterSerializer
# https://github.com/commontk/qRestAPI
# https://github.com/SimpleITK/SimpleITK
# https://github.com/Slicer/SlicerExecutionModel
# https://github.com/commontk/AppLauncher -> is this required?

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
    %cmake \
    -DLICER_USE_SYSTEM_QT:BOOL=1 \
    -DLICER_USE_SYSTEM_python:BOOL=1 \
    -DLICER_USE_SYSTEM_bzip2:BOOL=1 \
    -DSLICER_USE_SYSTEM_CTKAPPLAUNCHER:BOOL=1 \
    -DSLICER_USE_SYSTEM_CTKAppLauncherLib:BOOL=1 \
    -DSLICER_USE_SYSTEM_CTK:BOOL=1 \
    -DSLICER_USE_SYSTEM_CTKResEdit:BOOL=1 \
    -DSLICER_USE_SYSTEM_curl:BOOL=1 \
    -DSLICER_USE_SYSTEM_DCMTK:BOOL=1 \
    -DSLICER_USE_SYSTEM_incrTcl:BOOL=1 \
    -DSLICER_USE_SYSTEM_ITKv4:BOOL=1 \
    -DSLICER_USE_SYSTEM_JsonCpp:BOOL=1 \
    -DSLICER_USE_SYSTEM_LibArchive:BOOL=1 \
    -DSLICER_USE_SYSTEM_NUMPY:BOOL=1 \
    -DSLICER_USE_SYSTEM_OpenIGTLink:BOOL=1 \
    -DSLICER_USE_SYSTEM_OpenSSL:BOOL=1 \
    -DSLICER_USE_SYSTEM_ParameterSerializer:BOOL=1 \
    -DSLICER_USE_SYSTEM_PCRE:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-appdirs:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-chardet:BOOL=1 \
    -DSLICER_USE_SYSTEM_python:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-couchdb:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-gitdb:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-GitPython:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-nose:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-packaging:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-pip:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-pydicom:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-PyGithub:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-pyparsing:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-setuptools:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-six:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-smmap:BOOL=1 \
    -DSLICER_USE_SYSTEM_python-wheel:BOOL=1 \
    -DSLICER_USE_SYSTEM_qRestAPI:BOOL=1 \
    -DSLICER_USE_SYSTEM_RapidJSON:BOOL=1 \
    -DSLICER_USE_SYSTEM_SciPy:BOOL=1 \
    -DSLICER_USE_SYSTEM_SimpleITK:BOOL=1 \
    -DSLICER_USE_SYSTEM_SlicerExecutionModel:BOOL=1 \
    -DSLICER_USE_SYSTEM_Swig:BOOL=1 \
    -DSLICER_USE_SYSTEM_tcl:BOOL=1 \
    -DSLICER_USE_SYSTEM_teem:BOOL=1 \
    -DSLICER_USE_SYSTEM_tk:BOOL=1 \
    -DSLICER_USE_SYSTEM_VTKv9:BOOL=1 \
    -DSLICER_USE_SYSTEM_zlib:BOOL=1 \
    ..
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
- Add all the BRs from Superbuild
- Initial build
