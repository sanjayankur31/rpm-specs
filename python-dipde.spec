# https://fedoraproject.org/wiki/Packaging:DistTag?rd=Packaging/DistTag#Conditionals
# http://rpm.org/user_doc/conditional_builds.html
%if 0%{?fedora} >= 30
# disabled by default
%bcond_with py2
%else
%bcond_without py2
%endif

# Enabled by default
# If the package needs to download data for the test which cannot be done in
# koji, these can be disabled in koji by using `bcond_with` instead, but the
# tests must be validated in mock with network enabled like so:
# mock -r fedora-rawhide-x86_64 rebuild <srpm> --enable-network --rpmbuild-opts="--with tests"
%bcond_without tests

%global srcname dipde

%global desc %{expand: \
DiPDE (dipde) is a simulation platform for numerically solving the time
evolution of coupled networks of neuronal populations. Instead of solving the
subthreshold dynamics of individual model leaky-integrate-and-fire (LIF)
neurons, dipde models the voltage distribution of a population of neurons with
a single population density equation. In this way, dipde can facilitate the
fast exploration of mesoscale (population-level) network topologies, where
large populations of neurons are treated as homogeneous with random fine-scale
connectivity.

The population density approach in computational neuroscience seeks to
understand the statistical evolution of a large population of homogeneous
neurons. Beginning with the work of Knight and Sirovich [1] (see also [2]), the
approach typically formulates a partial integro-differential equation for the
evolution of the voltage probability distribution receiving synaptic activity,
and under the influence of neural dynamics. Neuronal dynamics typically follow
from the assumption of a leaky integrate-and fire model. We implement a
numerical scheme for computing the time evolution of the master equation for
populations of leaky integrate-and-fire neurons with shot-noise synapses (for a
similar approach, see [3]).

DiPDE is developed by the Modeling, Analysis and Theory group at the Allen
Institute, with contributions from Nicholas Cain, Ram Iyer, Vilas Menon,
Michael Buice, Tim Fliss, Keith Godfrey, David Feng, and Stefan Mihalas.

[1] Knight, N.W., Manin, D., & Sirovich, L. (1996) Dynamical models of
interacting neuron populations in visual cortex. Symposium on Robotics and
Cybernetics; Computational Engineering in Systems Application: 1–5.

[2] Omurtag, A., Knight, B.W., & Sirovich, L. (2000) On the Simulation of Large
Populations of Neurons. Journal of Computational Neuroscience 8: 51–63.

[3] de Kamps M. (2003) A simple and stable numerical solution for the
population density equation. Neural Computation 15: 2129–2146.

[4] Potjans T.C., & Diesmann, M. (2014) The cell-type specific cortical
microcircuit: relating structure and activity in a full-scale spiking network
model. Cerebral Cortex 24: 785–806.

[5] Cain, N., Iyer, R., Koch, C., & Mihalas, S. (2015) The computational
properties of a simplified cortical column model. In Preparation.

[6] Cain, N., Fliss, T., Menon, V., Iyer, R., Koch, C., & Mihalas, S. (2014)
Simulations of the statistics of firing activity of neuronal populations in the
entire mouse brain. Program No. 160.02/GG10. 2013 Neuroscience Meeting Planner.
Washington, DC: Society for Neuroscience, 2014. Online.

[7] Iyer, R., Menon, V., Buice, M., Koch, C., & Mihalas, S. (2013). The
Influence of Synaptic Weight Distribution on Neuronal Population Dynamics. PLoS
Computational Biology, 9(10), e1003248. doi:10.1371/journal.pcbi.1003248

[8] Iyer, R., Cain, N., & Mihalas, S. (2014). Dynamics of excitatory-inhibitory
neuronal networks with exponential synaptic weight . Cosyne Abstracts 2014,
Salt Lake City USA.}


%global commit cdf1325f77f575af75a5ab1401b484bc5c0ae1d8
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Name:           python-%{srcname}
Version:        0.1.0
Release:        1.20190202.git%{shortcommit}%{?dist}
Summary:        Numerical solver for coupled population density equations

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
License:        GPLv3+
URL:            http://alleninstitute.github.io/dipde
Source0:        https://github.com/AllenInstitute/%{srcname}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz


BuildArch:      noarch

%{?python_enable_dependency_generator}

%description
%{desc}

%if %{with py2}
%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist numpy}
BuildRequires:  %{py2_dist scipy}
BuildRequires:  %{py2_dist matplotlib}
BuildRequires:  %{py2_dist sympy}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{desc}
%endif

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist sympy}
%if %{with tests}
BuildRequires:  %{py3_dist pytest}
%endif
# For documentation
BuildRequires:  %{py3_dist sphinx}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{commit}

# We'll regenerate the docs
rm -rf doc/build

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%build
%py3_build

%if %{with py2}
%py2_build
%endif

# pushd doc
    # make SPHINXBUILD=sphinx-build-3 html
    # rm -rf _build/html/.doctrees
    # rm -rf _build/html/.buildinfo
# popd

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
# If, however, we're installing separate executables for python2 and python3,
# the order needs to be reversed so the unversioned executable is the python2 one.
%if %{with py2}
%py2_install
%endif

%py3_install

%check
%if %{with tests}
%if %{with py2}
%{__python2} setup.py test
%endif
%{__python3} setup.py test
%endif

%if %{with py2}
%files -n python2-%{srcname}
%license COPYING
%doc README.rst
%{python2_sitelib}/%{srcname}-%{version}-py2.?.egg-info
%{python2_sitelib}/%{srcname}
%endif

%files -n python3-%{srcname}
%license COPYING
%doc README.rst
%{python3_sitelib}/%{srcname}-%{version}-py3.?.egg-info
%{python3_sitelib}/%{srcname}

%files doc
%license COPYING
# %doc doc/_build/html

%changelog
* Sat Feb 02 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.0-1.20190202.gitcdf1325
- Initial rpm build
