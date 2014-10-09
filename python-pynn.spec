%global upstream_name   PyNN
%global module_name     pynn
%global with_python3 1
%global commit  c435db1528aa8478d41927e073d34a0319b6927e
%global short_commit    %(c=%{commit}; echo ${c:0:7})

Name:           python-%{module_name}
Version:        0.8
Release:        0.2.git%{short_commit}%{?dist}
Summary:        Simulator-independent specification of neuronal network models

License:        CeCILL 
URL:            http://neuralensemble.org/PyNN/
# wget --content-discomposition https://github.com/NeuralEnsemble/PyNN/archive/0.8beta1.tar.gz
#Source0:        https://pypi.python.org/packages/source/P/%{upstream_name}/%{upstream_name}-%{version}.tar.gz

# From git checkout
# git clone git@github.com:NeuralEnsemble/PyNN.git
# git archive --format=tar.gz --prefix=PyNN-0.8-c435db1/ --output=PyNN-0.8-c435db1.tar.gz master
Source0:        %{upstream_name}-%{version}-%{short_commit}.tar.gz

# submitted upstream: https://github.com/NeuralEnsemble/PyNN/pull/327
Patch0:         0001-Corrected-some-exception-constructs-to-py3.patch
Patch1:         0002-Some-more-corrections.patch
Patch2:         0003-Corrected-some-print-statements-for-py3.patch
Patch3:         0004-Convert-tabs-to-spaces.patch
Patch4:         0005-Fixed-tab-messed-up-indentation.-Corrected.patch

BuildRequires:  python2-devel python-setuptools python-nose numpy
BuildRequires:  python-mock python-lazyarray python-neo
BuildRequires:  nrn-devel
Requires:       python-mock python-lazyarray python-neo numpy
Requires:       python-nrn

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools python3-nose python3-numpy
BuildRequires:  python3-mock python3-lazyarray python3-neo
BuildRequires:  nrn-devel
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
Requires:       python3-mock python3-lazyarray python3-neo python3-numpy

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
%setup -q -n %{upstream_name}-%{version}-%{short_commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
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
%{python2_sitelib}/%{upstream_name}-%{version}beta1-py?.?.egg-info
%{python2_sitelib}/pyNN/

%if 0%{?with_python3}
%files -n python3-pynn
%{python3_sitelib}/%{upstream_name}-%{version}beta1-py?.?.egg-info
%{python3_sitelib}/pyNN/
%doc AUTHORS LICENSE changelog README
%endif

%changelog
* Thu Oct 09 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8-0.2.git435db1
- Add NEURON as BR to build it's extensions

* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8-0.1.gitc435db1
- Adds py3 support

* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8-0.1.beta1
- Update to 0.8beta1

* Tue Oct 07 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.7.5-1
- Initial rpmbuild
- py3 will be supported in the new release
- disabled tests for the time being - need to package up NEURON, NEST and
  friends.
