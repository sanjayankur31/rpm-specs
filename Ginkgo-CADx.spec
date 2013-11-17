Name:           Ginkgo-CADx
Version:        2.5.2.0
Release:        1%{?dist}
Summary:        An extensible multi-platform Open Source Medical Imaging software

License:        GPLv3
URL:            http://ginkgo-cadx.com/en/
Source0:        http://downloads.sourceforge.net/%{name}/ginkgocadx-%{version}.tgz


Patch0:         0002-ginkgo-cadx-wxtreeitem.patch
Patch1:         0003-ginkgo-cadx-cmakelist-dcmtk.patch

BuildRequires:  vtk-devel InsightToolkit-devel 
BuildRequires:  libX11-devel libXext-devel 
BuildRequires:  libxml2-devel openssl-devel
BuildRequires:  cmake 
BuildRequires:  wxPython-devel wxGTK-devel mingw32-wxWidgets
BuildRequires:  dcmtk-devel
BuildRequires:  vxl-devel
BuildRequires:  sqlite-devel
BuildRequires:  tcp_wrappers-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils

%description
* Multiplatform (Windows, Linux, MacOS) and portable (no installation required).
* Easy and customizable interface throught profiles.
* Full featured DICOM Image Visualization.

  -  Complete tool set (measure, markers, text, ...).
  -  Multiple modalities support (Neurological, Radiological, Dermathological,
Ophthalmological, UltraSound, Endoscopy, Electrocardiogram ...)

* Dicomization support from JPEG, PNG, GIF and TIFF.
* Full EMH integration support: HL7 standard, XML-RPC and IHE compliant 
workflows.
* PACS Workstation (C-FIND, C-GET, C-MOVE, C-STORE...)
* 3D reconstruction (volume and surface reconstruction)
* Extensible through custom Extensions. 

%package devel
Requires:   %{name} = %{version}-%{release}
Summary:    Development files for %{name}

%description devel
This package contains shared objects for %{name}

%prep
%setup -q -n ginkgocadx-%{version}
%patch0 -b .orig
%patch1 -b .orig

# Correct build error
sed -i "s/ptrdiff_t/std::ptrdiff_t/" src/cadxcore/api/icontrato.h

%build
pushd src/
mkdir build
pushd build

%cmake ../ -DCMAKE_BUILD_TYPE=Release -DUSE_PATCHED_LIBS:BOOL=FALSE \
-DUSE_CUSTOM_WX:BOOL=FALSE -DUSE_CUSTOM_VTK:BOOL=FALSE \
-DUSE_CUSTOM_ITK:BOOL=FALSE -DUSE_CUSTOM_DCMTK:BOOL=FALSE \
-DCUSTOM_PACKAGE:BOOL=FALSE

make %{?_smp_mflags}

popd
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd src/build/
    make install DESTDIR=$RPM_BUILD_ROOT
popd

# Install man page
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
install -p -m 0644 man/ginkgocadx.1 -t $RPM_BUILD_ROOT/%{_mandir}/man1/

# Install desktop file
desktop-file-install                                    \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
ginkgocadx.desktop

# Find lang doesn't find the translations
# Please ignore rpmlint warnings

# Correct line ending
sed -i 's/\r//' License.txt

%files
%doc doc/* License.txt TODO.txt
%{_mandir}/man1/*
%{_bindir}/ginkgocadx
%dir %{_libdir}/ginkgocadx/
%{_libdir}/ginkgocadx/*.so.*
%dir %{_libdir}/ginkgocadx/Plugins/
%{_libdir}/ginkgocadx/Plugins/*.so.*
%{_datadir}/applications/ginkgocadx.desktop
%{_datadir}/ginkgocadx/

%files devel
%{_libdir}/ginkgocadx/*.so
%{_libdir}/ginkgocadx/Plugins/*.so


%changelog
* Sat Jul 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.5.2.0-1
- initial rpm build
