%global upstream_name   PyNN
%global module_name     pynn
%global with_python3 0

Name:           python-%{module_name}
Version:        0.7.5
Release:        1%{?dist}
Summary:        Simulator-independent specification of neuronal network models

License:        CeCILL 
URL:            http://neuralensemble.org/PyNN/
Source0:        https://pypi.python.org/packages/source/P/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools python-nose numpy
BuildRequires:  python-mock python-lazyarray python-neo
Requires:       python-mock python-lazyarray python-neo numpy

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools python3-nose python3-numpy
BuildRequires:  python3-mock python3-lazyarray python3-neo
Requires:       python3-mock python3-lazyarray python3-neo python3-numpy
%endif # if with_python3

%description
A Python package for simulator-independent specification of neuronal network
models

In other words, you can write the code for a model once, using the PyNN API and
the Python programming language, and then run it without modification on any
simulator that PyNN supports (currently NEURON, NEST, PCSIM and Brian).

The API has two parts, a low-level, procedural API (functions create(),
connect(), set(), record(), record_v()), and a high-level, object-oriented API
(classes Population and Projection, which have methods like set(), record(),
setWeights(), etc.).

The low-level API is good for small networks, and perhaps gives more
flexibility. The high-level API is good for hiding the details and the
book-keeping, allowing you to concentrate on the overall structure of your
model.

The other thing that is required to write a model once and run it on multiple
simulators is standard cell and synapse models. PyNN translates standard
cell-model names and parameter names into simulator-specific names, e.g.
standard model IF_curr_alpha is iaf_neuron in NEST and StandardIF in NEURON,
while SpikeSourcePoisson is a poisson_generator in NEST and a NetStim in
NEURON.

Even if you don't wish to run simulations on multiple simulators, you may
benefit from writing your simulation code using PyNN's powerful, high-level
interface. In this case, you can use any neuron or synapse model supported by
your simulator, and are not restricted to the standard models.

PyNN is a work in progress, but is already being used for several large-scale
simulation projects.

%if 0%{?with_python3}
%package -n python3-%{module_name}
Summary:        Simulator-independent specification of neuronal network models

%description -n python3-%{module_name}
A Python package for simulator-independent specification of neuronal network
models

In other words, you can write the code for a model once, using the PyNN API and
the Python programming language, and then run it without modification on any
simulator that PyNN supports (currently NEURON, NEST, PCSIM and Brian).

The API has two parts, a low-level, procedural API (functions create(),
connect(), set(), record(), record_v()), and a high-level, object-oriented API
(classes Population and Projection, which have methods like set(), record(),
setWeights(), etc.).

The low-level API is good for small networks, and perhaps gives more
flexibility. The high-level API is good for hiding the details and the
book-keeping, allowing you to concentrate on the overall structure of your
model.

The other thing that is required to write a model once and run it on multiple
simulators is standard cell and synapse models. PyNN translates standard
cell-model names and parameter names into simulator-specific names, e.g.
standard model IF_curr_alpha is iaf_neuron in NEST and StandardIF in NEURON,
while SpikeSourcePoisson is a poisson_generator in NEST and a NetStim in
NEURON.

Even if you don't wish to run simulations on multiple simulators, you may
benefit from writing your simulation code using PyNN's powerful, high-level
interface. In this case, you can use any neuron or synapse model supported by
your simulator, and are not restricted to the standard models.

PyNN is a work in progress, but is already being used for several large-scale
simulation projects.
%endif # with_python3

%prep
%setup -q -n %{upstream_name}-%{version}

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
#PYTHONPATH=$RPM_BUILD_ROOT/%{python2_sitelib}/ nosetests -w test/unittests -c test/unittests/setup.cfg

#%if 0%{?with_python3}
#nosetests-3.4 test
#%endif
 
%files
%doc AUTHORS LICENSE changelog README
%{python2_sitelib}/%{upstream_name}-%{version}-py?.?.egg-info
%{python2_sitelib}/pyNN/

%if 0%{?with_python3}
%files -n python3-pynn
%endif

%changelog
* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.5-1
- Initial rpmbuild
- py3 will be supported in the new release
- disabled tests for the time being - need to package up NEURON, NEST and
  friends.
