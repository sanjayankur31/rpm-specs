Name:           OpenSURF
Version:        0
Release:        0.1.20120412%{?dist}
Summary:        An open implementation of SURF

License:        GPLv1
URL:            http://www.chrisevansdev.com/computer-vision-opensurf.html
Source0:        http://opensurf1.googlecode.com/files/OpenSURFcpp.zip
Source1:        opensurf.pdf
Patch0:         %{name}-Makefile.patch

BuildRequires:  opencv-devel

%description
The task of finding point correspondences between two images of the same scene
or object is an integral part of many machine vision or computer vision
systems. The algorithm aims to find salient regions in images which can be
found under a variety of image transformations. This allows it to form the
basis of many vision based tasks; object recognition, video surveillance,
medical imaging, augmented reality and image retrieval to name a few. 

OpenSURF is an open source implementation of SURF.

%prep
%setup -q -n %{name}cpp
mv Makefile.gcc Makefile
cp %{SOURCE1} ./
%patch0 -p0

%build
export CFLAGS="%{optflags}"
export CPPLAGS="%{optflags}"
export LDFLAGS="-Wl,-z,relro"
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 surf %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_libdir}
install -m 0755 libsurf.so %{buildroot}/%{_libdir}/

%files
%doc opensurf.pdf README.txt
%{_bindir}/surf
%{_libdir}/libsurf.so

%changelog
* Thu Aug 30 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0-0.1.20120412
- initial rpm build

