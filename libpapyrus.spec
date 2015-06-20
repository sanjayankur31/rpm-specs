Name:		libpapyrus
Version:	0.13.3
Release:	1%{?dist}
Summary:	C++ Cairo scenegraph library

License:	GPLv3+ and LGPLv3+
URL:		http://libpapyrus.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/papyrus-%{version}.tar.bz2

BuildRequires:	gtkmm24-devel cairomm-devel

%description
Papyrus uses cairomm, and thus cairo, to perform rendering of a 2-D
scenegraph into a cairo context.Thus, papyrus scenegraphs can be rendered
on-screen (such as X11 windows) as well as PDF documents, PNG images, SVG
documents and any other surface cairo supports ( Microsoft Windows surfaces,
Quartz surfaces, postscript, OpenGL to name a few more).

Examples of papyrus rendering scenegraphs into PNG images can be found
throughout this documentation. The example images of papyrus drawables were all
created by the papyrus example programs.

A key feature of papyrus is the ability to create customized shapes through
inheritance, and papyrus is designed to allow multiple points at which this can
occur such as:

- Inherit from Renderable if you want complete control over the drawing
process.  
- Inherit from Drawable and reimplement the pure virtual method
Drawable::draw if you want control over the drawing process, but want to
leverage concepts such as the Viewbox.  
- Inherit from Shape and reimplement the
pure virtual method Shape::draw_shape and/or the virtual method
Shape::draw_outline if all you need to do is customize the cairo drawing path.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc



%changelog
* Tue Sep 09 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.13.3-1
- Initial build


