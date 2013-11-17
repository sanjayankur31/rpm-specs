Name:           metis
Version:        4.0.3
Release:        1%{?dist}
Summary:        A set of serial programs for partitioning graphs, partitioning finite element meshes, and producing fill reducing orderings for sparse matrices

License:        MIT
URL:            http://glaros.dtc.umn.edu/gkhome/views/%{name}
Source0:        http://glaros.dtc.umn.edu/gkhome/fetch/sw/%{name}/%{name}-%{version}.tar.gz

#BuildRequires:  
#Requires:       

%description
METIS's key features are the following:

Provides high quality partitions!
Experiments on a large number of graphs arising in various domains 
including finite element methods, linear programming, VLSI, and 
transportation show that METIS produces partitions that are 
consistently better than those produced by other widely used 
algorithms. The partitions produced by METIS are consistently 
10% to 50% better than those produced by spectral partitioning 
algorithms.

It is extremely fast!
Experiments on a wide range of graphs has shown that METIS is one 
to two orders of magnitude faster than other widely used 
partitioning algorithms. Graphs with over 1,000,000 vertices can be 
partitioned in 256 parts in a few seconds on current generation 
workstations and PCs.

Produces low fill orderings!
The fill-reducing orderings produced by METIS are significantly 
better than those produced by other widely used algorithms 
including multiple minimum degree. For many classes of problems 
arising in scientific computations and linear programming, METIS 
is able to reduce the storage and computational requirements of 
sparse matrix factorization, by up to an order of magnitude. 
Moreover, unlike multiple minimum degree, the elimination trees 
produced by METIS are suitable for parallel direct factorization. 
Furthermore, METIS is able to compute these orderings very fast. 
Matrices with over 200,000 rows can be reordered in just a few 
seconds on current generation workstations and PCs. 

%package devel
Requires:     %{name} = %{version}-%{release}
Summary:      Files required for development using %{name}
Provides:     %{name}-static = %{version}-%{release}

%description devel
This package contains the headers and libraries that can be used
to link applications to %{name}

%prep
%setup -q

%build
make %{?_smp_mflags} OPTFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_bindir}
install -p -m 0755 graphchk kmetis mesh2dual mesh2nodal oemetis onmetis partdmesh partnmesh pmetis -t $RPM_BUILD_ROOT/%{_bindir}
install -p -m 0755 Graphs/mtest -t $RPM_BUILD_ROOT/%{_bindir}/

install -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/Graphs/
install -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/Doc/
install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}/Graphs/
install -p -m 0644 Graphs/*.* -t $RPM_BUILD_ROOT/%{_datadir}/%{name}/Graphs/
install -p -m 0644 Graphs/0README -t $RPM_BUILD_ROOT/%{_docdir}/%{name}/Graphs/
install -p -m 0644 Doc/* -t $RPM_BUILD_ROOT/%{_docdir}/%{name}/Doc/
install -p -m 0644 VERSION LICENSE FILES CHANGES -t $RPM_BUILD_ROOT/%{_docdir}/%{name}/

install -d $RPM_BUILD_ROOT/%{_libdir}/
install -p -m 0644 libmetis.a -t $RPM_BUILD_ROOT/%{_libdir}/

install -d $RPM_BUILD_ROOT/%{_includedir}/%{name}
install -p -m 0644 Lib/*.h -t $RPM_BUILD_ROOT/%{_includedir}/%{name}/

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{name}/
%{_docdir}/%{name}/

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_includedir}/%{name}/

%changelog
* Wed Jun 22 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.0.3-1
- initial rpm build
