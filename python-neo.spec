%global module_name     neo
%global with_python3 1

Name:       python-%{module_name}
Version:    0.3.3
Release:    1%{?dist}
Summary:    Represent electrophysiology data in Python

License:    BSD
URL:        http://neuralensemble.org/neo/
Source0:    https://pypi.python.org/packages/source/n/%{module_name}/%{module_name}-%{version}.tar.gz

BuildRequires:  python2-devel python-setuptools numpy python-sphinx
BuildRequires:  python-quantities
Requires:       numpy python-quantities
BuildArch:      noarch

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools python3-numpy 
BuildRequires:  python3-quantities
Requires:       python3-numpy python3-quantities
%endif # if with_python3

%description
Neo is a package for representing electrophysiology data in Python, together
with support for reading a wide range of neurophysiology file formats,
including Spike2, NeuroExplorer, AlphaOmega, Axon, Blackrock, Plexon, Tdt, and
support for writing to a subset of these formats plus non-proprietary formats
including HDF5.

The goal of Neo is to improve interoperability between Python tools for
analyzing, visualizing and generating electrophysiology data (such as
OpenElectrophy, NeuroTools, G-node, Helmholtz, PyNN) by providing a common,
shared object model. In order to be as lightweight a dependency as possible,
Neo is deliberately limited to represention of data, with no functions for data
analysis or visualization.

Neo implements a hierarchical data model well adapted to intracellular and
extracellular electrophysiology and EEG data with support for multi-electrodes
(for example tetrodes). Neo's data objects build on the quantities_ package,
which in turn builds on NumPy by adding support for physical dimensions. Thus
neo objects behave just like normal NumPy arrays, but with additional metadata,
checks for dimensional consistency and automatic unit conversion.%if

0%{?with_python3}
%package -n python3-%{module_name}
Summary:    A lazily-evaluated numerical array class

%description -n python3-%{module_name}
Neo is a package for representing electrophysiology data in Python, together
with support for reading a wide range of neurophysiology file formats,
including Spike2, NeuroExplorer, AlphaOmega, Axon, Blackrock, Plexon, Tdt, and
support for writing to a subset of these formats plus non-proprietary formats
including HDF5.

The goal of Neo is to improve interoperability between Python tools for
analyzing, visualizing and generating electrophysiology data (such as
OpenElectrophy, NeuroTools, G-node, Helmholtz, PyNN) by providing a common,
shared object model. In order to be as lightweight a dependency as possible,
Neo is deliberately limited to represention of data, with no functions for data
analysis or visualization.

Neo implements a hierarchical data model well adapted to intracellular and
extracellular electrophysiology and EEG data with support for multi-electrodes
(for example tetrodes). Neo's data objects build on the quantities_ package,
which in turn builds on NumPy by adding support for physical dimensions. Thus
neo objects behave just like normal NumPy arrays, but with additional metadata,
checks for dimensional consistency and automatic unit conversion.%if

%prep
%setup -q -n %{module_name}-%{version}
rm -rf neo.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3 

%check
%{__python2} setup.py test
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3 

%files
%doc README.rst examples
%{python2_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{python2_sitelib}/%{module_name}/

%if 0%{?with_python3}
%files -n python3-%{module_name}
%doc README.rst examples
%{python3_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{python3_sitelib}/%{module_name}/
%endif

%changelog
* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.3-1
- Initial rpmbuild
