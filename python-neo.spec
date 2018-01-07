%global srcname     neo

Name:       python-%{srcname}
Version:    0.5.2
Release:    1%{?dist}
Summary:    Represent electrophysiology data in Python

License:    BSD
URL:        http://neuralensemble.org/neo/
Source0:    https://files.pythonhosted.org/packages/source/n/%{srcname}/%{srcname}-%{version}.tar.gz


BuildArch:      noarch

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
checks for dimensional consistency and automatic unit conversion.

%package -n python2-%{srcname}
Summary:        %{sum}
BuildRequires:  python2-devel python-setuptools numpy python-sphinx
BuildRequires:  numpy python-quantities
Requires:       numpy python-quantities

Recommends:   python2-scipy python2-h5py python2-igor
# Not in fedora yet, to be updated as these are added
# Recommends:   python2-klusta python2-nixio python2-stfio

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
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
checks for dimensional consistency and automatic unit conversion.


%package -n python3-%{srcname}
Summary:        %{sum}
BuildRequires:  python3-devel python3-setuptools python3-numpy
BuildRequires:  python3-numpy python3-quantities
Requires:       python3-numpy python3-quantities
Recommends:   python3-scipy python3-h5py python3-igor
# Not in fedora yet, to be updated as these are added
# Recommends:   python3-klusta python3-nixio python3-stfio
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
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
checks for dimensional consistency and automatic unit conversion.

%package doc
Summary:    Documentation for python-neo

%description doc
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
%autosetup -n %{srcname}-%{version}
# stray backup file?
rm -fv neo/io/nwbio_BACKUP_4246.py
rm -rf neo.egg-info

%build
%py2_build
%py3_build

pushd doc
    PYTHONPATH="$PYTHONPATH:../build/lib/" make html
    rm build/html/.buildinfo -f
    sed -i 's/\r$//' build/html/objects.inv
    iconv -f iso8859-1 -t utf-8 build/html/objects.inv > build/html/objects.inv.conv && mv -f build/html/objects.inv.conv build/html/objects.inv
popd

%install
%py2_install
%py3_install

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{srcname}
%license LICENSE.txt
%{python2_sitelib}/%{srcname}-%{version}-py?.?.egg-info
%{python2_sitelib}/%{srcname}/

%files -n python3-%{srcname}
%license LICENSE.txt
%{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info
%{python3_sitelib}/%{srcname}/

%files doc
%license LICENSE.txt
%doc README.rst examples doc/build/html

%changelog
* Sun Jan 07 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.2-1
- Update to latest upstream release
- update requires and recommends

* Mon Jun 26 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.1-1
- Update to latest upstream release

* Wed Feb 01 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.4.1-1
- Update to latest upstream release

* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.3-1
- Initial rpmbuild
