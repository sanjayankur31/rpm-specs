Name:		quarter
Version:	1.0.0
Release:	1%{?dist}
Summary:	Glue library provides integration between Coin2

Group:		Development/Libraries
License:	GPLv2
URL:		https://bitbucket.org/Coin3D/quarter/overview
Source0:	https://bitbucket.org/Coin3D/quarter/get/quarter-1_0_0.tar.gz

BuildRequires:	Coin2-devel qt-devel mesa-libGL-devel

%description
Quarter is a light-weight glue library that provides seamless
integration between Systems in Motions's Coin high-level 3D
visualization library and Trolltech's Qt 2D user interface library.

Qt and Coin is a perfect match since they are both open source, widely
portable and easy to use. Quarter has evolved from Systems in Motion's
own experiences using Coin and Qt together in our applications.

The functionality in Quarter revolves around QuarterWidget, a subclass
of QGLWidget. This widget provides functionality for rendering of Coin
scenegraphs and translation of QEvents into SoEvents. Using this
widget is as easy as using any other QWidget.


%prep
%setup -q -n Coin3D-quarter-e41f230c86f9


%build
%configure --with-qt=true
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc



%changelog

