# Notes:
# It makes use of some icons from
# - crystal
# - nuvola
# that are available in Fedora
#
# [root@ankur ~]# repoquery -i crystal-clear -l | egrep png | wc -l
# 5053
#
# Doesn't make sense to install 5000 icons because this package uses *4*

Name:           GoFigure2
Version:        0.8.2
Release:        1%{?dist}
Summary:        A software for visualizing, processing and analysis of bioimages

License:        BSD
URL:            http://%{name}.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-v%{version}.tar.gz 
Source1:        GoFigure2.desktop

BuildRequires:  cmake 
BuildRequires:  qt-devel qt-doc 
BuildRequires:  mysql-devel 
BuildRequires:  boost-devel
BuildRequires:  vtk-devel 
BuildRequires:  InsightToolkit-devel 
BuildRequires:  vxl-devel 
BuildRequires:  qt-webkit-devel
BuildRequires:  libxml2-devel
BuildRequires:  doxygen 
BuildRequires:  graphviz
BuildRequires:  desktop-file-utils

Requires:       mysql

# Also needs ffmpeg, building without it

%description
%{name} is an open-source, cross-platform application for visualizing,
processing and analysis of multidimensional microscopy data. Users can
visualize, segment and track cells through time, detect cell-division and
ultimately generate lineages.

%package devel
Requires:   %{name} = %{version}-%{release}
Summary:    Development files related to %{name}

%description devel
This package contains the headers and shared libraries related to %{name}

%prep
%setup -q -n %{name}-v%{version}

# Correct spurious exec perm
find Code/ -name "*.h" -execdir chmod a-x '{}' \;

%build
# VTK without ffmpeg, obviously
# I don't think it really builds any documentation
%cmake -DBUILD_DOCUMENTATION=ON -DVTK_USE_FFMPEG_ENCODER=FALSE \
-DGOFIGURE2_INSTALL_LIB_DIR=%{_libdir}/gofigure2 \
-DBUILD_EXAMPLES=ON .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -p -m 0644 UseGoFigure2.cmake -t $RPM_BUILD_ROOT/%{_datadir}/gofigure2/

# Install an icon
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps
install -p Resources/fig/Myapp2.png -T $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/GoFigure2.png

# Desktop file install
desktop-file-install                                    \
--dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
%{SOURCE1}

# Remove the installdox file
rm -fv Documentation/html/installdox

%check
ctest .

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc Documentation/html
%{_bindir}/gofigure
%dir %{_libdir}/gofigure2/
%{_libdir}/gofigure2/*.so.*
%{_docdir}/gofigure2/
%{_datadir}/gofigure2/
%{_datadir}/icons/hicolor/32x32/apps/GoFigure2.png
%{_datadir}/applications/GoFigure2.desktop

%files devel
%{_includedir}/gofigure2/
%{_libdir}/gofigure2/*.so

%changelog
* Thu Jul 28 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8.2-1
- new upstream release

* Sat Jul 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8.1-1
- initial rpmbuild
