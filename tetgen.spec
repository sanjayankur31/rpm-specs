Name:           tetgen
Version:        1.4.3
Release:        2%{?dist}
Summary:        A Quality Tetrahedral Mesh Generator and a 3D Delaunay Triangulator

License:        MIT
URL:            http://tetgen.berlios.de
Source0:        http://tetgen.berlios.de/files/%{name}%{version}.tar.gz
Source1:        %{name}-manual.pdf

%description
TetGen is a program to generate tetrahedral meshes of any 
3D polyhedral domains. TetGen generates exact constrained 
Delaunay tetrahedralizations, boundary conforming Delaunay 
meshes, and Voronoi partitions.

TetGen provides various features to generate good quality and 
adaptive tetrahedral meshes suitable for numerical methods, such 
as finite element or finite volume methods. For more information 
of TetGen, please take a look at a list of features.

TetGen is written in C++. It can be compiled into either a 
standalone program invoked from command-line or a library for 
linking with other programs. All major operating systems, 
e.g. Unix/Linux, MacOS, Windows, etc, are supported.

%prep
%setup -q -n %{name}%{version}
sed -i "/CXXFLAGS = -g/d" makefile
sed -i "s/\(PREDCXXFLAGS = -O0\)/\1 %{optflags}/" makefile
sed -i "s/\(PREDCXXFLAGS = -O0\) -O2/\1/" makefile
install -p -m 0644 %{SOURCE1} -t .

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
make %{?_smp_mflags}

%install
install -d $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 %{name} -t $RPM_BUILD_ROOT%{_bindir}/

%files
%doc README LICENSE example.poly %{name}-manual.pdf
%{_bindir}/%{name}

%changelog
* Wed Jun 29 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.3-2
- included documentation
- added a hack to make all files use optflags

* Tue Jun 28 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.3-1
- correct spec to use our optflags

* Sat Jun 18 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.3-1
- initial rpm build
