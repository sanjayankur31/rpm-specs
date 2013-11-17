# Does not support py3 yet
%global with_python3 0
%global commit_id 87c7ac3

Name:           pybrain
Version:        0.3.1
Release:        2%{?dist}
Summary:        The python machine learning library

License:        BSD
URL:            http://%{name}.org/pages/home

# wget --content-disposition https://github.com/pybrain/pybrain/tarball/0.3.1
# pybrain-pybrain-0.3.1-0-g87c7ac3.tar.gz
# O.3.2 tarball seems unavailable. Issue filed
# https://github.com/pybrain/pybrain/issues/88
Source0:        %{name}-%{name}-%{version}-0-g%{commit_id}.tar.gz
Patch0:         %{name}-Pillow.patch
# http://github.com/pybrain/pybrain/pull/84
Patch1:         %{name}-test_nearoptimal.patch

BuildArch:      noarch
BuildRequires:  python2-devel scipy
BuildRequires:  python-setuptools
BuildRequires:  python-matplotlib


# https://github.com/pybrain/pybrain/wiki/Dependencies
Requires:       python-matplotlib
Requires:       libsvm
Requires:       python-imaging
Requires:       python-rlglue
Requires:       PyOpenGL PyOpenGL-Tk
Requires:       tkinter
Requires:       scons
Requires:       pycdf
Requires:       pyODE

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-scipy
BuildRequires:  python3-setuptools
%endif # if with_python3


%description
PyBrain is a modular Machine Learning Library for Python. Its goal is to offer
flexible, easy-to-use yet still powerful algorithms for Machine Learning Tasks
and a variety of predefined environments to test and compare your algorithms.

PyBrain is short for Python-Based Reinforcement Learning, Artificial
Intelligence and Neural Network Library. In fact, we came up with the name
first and later reverse-engineered this quite descriptive "Backronym". 

%if 0%{?with_python3}
%package -n python3-pybrain
Summary:        The python machine learning library
Group:          Applications/System
Requires:       python3-matplotlib

%description -n python3-pybrain
PyBrain is a modular Machine Learning Library for Python. Its goal is to offer
flexible, easy-to-use yet still powerful algorithms for Machine Learning Tasks
and a variety of predefined environments to test and compare your algorithms.

PyBrain is short for Python-Based Reinforcement Learning, Artificial
Intelligence and Neural Network Library. In fact, we came up with the name
first and later reverse-engineered this quite descriptive "Backronym". 

%endif # with_python3

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
PyBrain is a modular Machine Learning Library for Python. Its goal is to offer
flexible, easy-to-use yet still powerful algorithms for Machine Learning Tasks
and a variety of predefined environments to test and compare your algorithms.

PyBrain is short for Python-Based Reinforcement Learning, Artificial
Intelligence and Neural Network Library. In fact, we came up with the name
first and later reverse-engineered this quite descriptive "Backronym". 

%prep
%setup -q -n %{name}-%{name}-%{commit_id}
%patch0 -p1 -b pillow
%patch1 -p0 -b TEST1

# Test fails
# sed -iTEST 's/1.4142135623730949/1.414213562373095/' pybrain/tests/unittests/supervised/knn/lsh/test_nearoptimal.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%build
%{__python} setup.py build


%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

rm -fr docs/html/.buildinfo docs/sphinx/_static/.gitignore

for lib in $RPM_BUILD_ROOT%{python_sitelib}/%{name}/tests/{runtests,optimizationtest}.py; do
 sed '1{\@^#! /usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

 
%files
%doc acknowledgements.txt LICENSE
%{python_sitelib}/%{name}/
%{python_sitelib}/PyBrain-%{version}-py?.?.egg-info/

%if 0%{?with_python3}
%files -n python3-pybrain
%doc acknowledgements.txt LICENSE
%{python3_sitelib}/%{name}/
%{python3_sitelib}/PyBrain-%{version}-py?.?.egg-info/
%endif # with_python3

%files doc
%doc acknowledgements.txt LICENSE docs/ examples/

%changelog
* Mon Mar 25 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.1-2
- Correct issues in rhbz# 923035
- run tests
- doc separate package
- add requires
- remove arch specific spec bits

* Tue Mar 19 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.1-1
- Initial rpmbuild

