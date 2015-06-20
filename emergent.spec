%global svn_revision    7375

Name:		emergent
Version:	6.3.2
Release:	1.20140622svn%{svn_revision}%{?dist}
Summary:	Neural network simulator

Group:		Development/Libraries
License:	GPLv3+ and BSD and LGPLv2.1+
URL:		http://grey.colorado.edu/emergent
# svn checkout svn checkout --username anonymous --password emergent http://grey.colorado.edu/svn/emergent/emergent/trunk emergent
Source0:	%{name}-svn-%{svn_revision}.tar.xz

BuildRequires:	cmake qt-devel qtwebkit-devel Coin2-devel
#Requires:	

%description
emergent is a comprehensive, full-featured deep neural network simulator that
enables the creation and analysis of complex, sophisticated models of the brain
in the world. The software differs from other tools (e.g., Matlab, python) in
providing a full-featured GUI for constructing, visualizing, and interacting
with the neural models (in a 3D display), so that people with little to no
programming experience can use it effectively. This is important for teaching
applications. It also supports the workflow of professional neural network
researchers, with a powerful scripting language system called css (not the
other css), which uses the familiar C++ syntax, including python/matlab like
Matrix extensions. Programs also have a full GUI that also allows novices to
automate network training & testing, and construction of the input environment,
while simultaneously supporting the expert with a text-based editor interface.
Full interactive debugging and error-checking facilities are provided. Model
outputs can be analyzed using DataTable data processing operations (filtering,
grouping, sorting, dimensionality reduction, etc). The same DataTable
functionality is used for presenting inputs to the networks, and it is
straightforward to write programs to generate any sort of input (interactively
or statically) for the networks. In addition, the 3D GUI also features a
complete Newtonian physics simulator, allowing you to create rich robotics
simulations, including a biophysically realistic human arm with 12 muscles, and
realistic visual processing of images (which can come from virtual cameras in
the virtual environment, or from the real world) according to principles of
early visual processing. As a direct descendant of PDP (1986) and PDP++ (1999),
emergent has been in development for decades, and has been used in hundreds of
scientific publications from a variety of different labs. Detailed models of
the hippocampus, prefrontal cortex, basal ganglia, visual cortex, cerebellum,
and other brain areas are available (and described in our textbook). A large
number of classic neural network algorithms and variants are supported,
including Backpropagation, Constraint Satisfaction, Self Organizing, and the
Leabra algorithm which incorporates many of the most important features from
each of these algorithms, in a biologically consistent manner. In addition, the
symbolic / subsymbolic ACT-R architecture is now supported as well. 

%prep
%setup -q -n %{name}


%build
%cmake -DCOIN_LIBRARY=%{buildroot}/%{_libdir}/ -DCOIN_INCLUDE_DIR=%{buildroot}/%{_includedir}/Coin2/
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc Changelog* COPYING* AUTHORS doc/*



%changelog
* Sun Jun 22 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 6.3.2-1svn
- Initial build


