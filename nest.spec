Name:        nest
Version:     2.4.2
Release:     1%{?dist}
Summary:     the Neural Simulation Tool

License:     GPLv2+
URL:         http://www.nest-initiative.org/Software:About_NEST
Source0:     http://www.nest-simulator.org/download/gplreleases/%{name}-%{version}.tar.gz

BuildRequires:     python2-devel numpy scipy python-matplotlib python-ipython
BuildRequires:  readline-devel
#Requires:

%description
NEST is a simulation software for spiking neural network models, including
large-scale neuronal networks. NEST was initially developed by Markus Diesmann
and Marc-Oliver Gewaltig and is now developed and maintained by the NEST
Initiative.

%package python-nest
Summary:    Python bindings for %{name}

%description python-test
NEST is a simulation software for spiking neural network models, including
large-scale neuronal networks. NEST was initially developed by Markus Diesmann
and Marc-Oliver Gewaltig and is now developed and maintained by the NEST
Initiative.

This package contains python bindings %{name}.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%{_bindir}/nest*
%{_bindir}/sli

%files -n python-%{name}
%{python2_sitearch}/%{name}
%{python2_sitearch}/%{name}
%{python2_sitearch}/PyNEST-%{version}-py?.?.egg-info
%{python2_sitearch}/Topology-%{version}-py?.?.egg-info
%{python2_sitelib}/ConnPlotter-0.7a-py?.?.egg-info
%{python2_sitelib}/ConnPlotter/

%files doc
%{_docdir}/%{name}/




%changelog
* Thu Oct 09 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.4.2-1
- Initial build


