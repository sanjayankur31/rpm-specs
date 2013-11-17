%global     svn_release 1526
%global     co_date     20111204
Name:           OpenNero
Version:        0
Release:        0.1.20111204svn%{svn_release}%{?dist}
Summary:        Game platform for Artificial Intelligence research and education

License:        zlib/libpng and BSD and GPLv2+ and MIT 
URL:            http://code.google.com/p/opennero/
# svn checkout http://opennero.googlecode.com/svn/trunk OpenNero-%{co_date}svn
# tar -cvzf OpenNero-%{co_date}svn.tar.gz OpenNero-%{co_date}svn
Source0:        %{name}-%{co_date}svn.tar.gz

BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  libX11-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  zlib-devel 

BuildRequires:  python-devel
BuildRequires:  python-matplotlib
BuildRequires:  wxPython
BuildRequires:  irrlicht-devel



%description
OpenNERO is an open source software platform designed for research and education
in Artificial Intelligence. The project is based on the Neuro-Evolving Robotic
Operatives (NERO) game developed by graduate and undergraduate students at the
Neural Networks Research Group and Department of Computer Science at the
University of Texas at Austin.

In particular, OpenNERO has been used to implement several demos and exercises
for Russell and Norvig's textbook Artificial Intelligence: A Modern Approach.
These demos and exercises illustrate AI methods such as brute-force search,
heuristic search, scripting, reinforcement learning, and evolutionary
computation, and AI problems such as maze running, vacuuming, and robotic
battle. The methods and problems are implemented in several different
environments (or "mods"), as described below.

More environments, problems, and methods, as well as demos and exercises
illustrating them, will be added in the future. The current ones are intended to
serve as a starting point on which new ones can be built, by us, but also by the
community at large. If you have questions or would like to contribute, check out
the OpenNERO Google Group. 


%prep
%setup -q -n %{name}-%{co_date}svn


%build
%cmake .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc README.txt COPYING.txt



%changelog
* Sun Dec 04 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1.20111204svn1526
- Initial rpm build
