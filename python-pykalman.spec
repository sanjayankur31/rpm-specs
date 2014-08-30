# Turn off byte compilation because I don't want it to byte compile the
# examples in docs
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global module_name pykalman
%global with_python3    1

%global commit  2aeb4ad80f9dcc4ea182331e33bda7ea4866548e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-%{module_name}
Version:        0.9.5
Release:        1.20140827git%{shortcommit}%{?dist}

Summary:        Kalman Filter, Smoother, and EM algorithm

License:        BSD
URL:            http://%{module_name}.github.com/
Source0:        https://github.com/%{module_name}/%{module_name}/archive/%{commit}/%{module_name}-%{commit}.tar.gz

# https://github.com/pykalman/pykalman/issues/33
# https://github.com/pykalman/pykalman/issues/32

BuildArch:      noarch
BuildRequires:  python2-devel python-nose numpy scipy
BuildRequires:  python-numpydoc python-sphinx 

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-nose python3-numpy
BuildRequires:  python3-scipy

# py3-numpydoc not in Fedora yet. Bug filed:
# https://bugzilla.redhat.com/show_bug.cgi?id=1134171
#BuildRequires:  python3-numpydoc python3-sphinx
%endif

%description
This module implements two algorithms for tracking: the Kalman Filter and
Kalman Smoother. In addition, model parameters which are traditionally
specified by hand can also be learned by the implemented EM algorithm without
any labeled training data.

%package doc
Summary:    Documentation for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description doc
Documentation for %{name}

%if 0%{?with_python3}
%package -n python3-%{module_name}
Summary:    Kalman Filter, Smoother, and EM Algorithm

%description -n python3-%{module_name}
This module implements two algorithms for tracking: the Kalman Filter and
Kalman Smoother. In addition, model parameters which are traditionally
specified by hand can also be learned by the implemented EM algorithm without
any labeled training data.

%package -n python3-%{module_name}-doc
Summary:    Documentation for python3-%{module_name}
Requires:   python3-%{module_name}%{?_isa} = %{version}-%{release}

%description -n python3-%{module_name}-doc
Documentation for python3-%{module_name}
%endif

%prep
%setup -q -n %{module_name}-%{commit}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%build
%{__python2} setup.py build
pushd doc
    make html
    sed -i 's/\r$//' build/html/_static/jquery.js
    rm -fv build/html/.buildinfo
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
#documentation
    pushd doc
        #use py2 at the moment until python3-numpydoc is available
        #sed -ibackup 's/sphinx-build/sphinx-build-3/' Makefile
        make html
        sed -i 's/\r$//' build/html/_static/jquery.js
        rm -fv build/html/.buildinfo
    popd
popd
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT

%py_byte_compile %{__python3} $RPM_BUILD_ROOT/%{python3_sitelib}/%{module_name}/

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/python3-%{module_name}
cp -pr doc/build/html $RPM_BUILD_ROOT/%{_docdir}/python3-%{module_name}
cp -pr examples $RPM_BUILD_ROOT/%{_docdir}/python3-%{module_name}
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%py_byte_compile %{__python2} $RPM_BUILD_ROOT/%{python_sitelib}/%{module_name}/

%check
nosetests %{module_name}/tests/

%if 0%{?with_python3}
pushd %{py3dir}
nosetests-3.4 %{module_name}/tests/
popd
%endif # with_python3
 
%files
%doc COPYING
%{python_sitelib}/%{module_name}/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info

%files doc
%doc doc/build/html examples

%if 0%{?with_python3}
%files -n python3-%{module_name}
%doc COPYING
%{python3_sitelib}/%{module_name}/
%{python3_sitelib}/%{module_name}-%{version}-py?.?.egg-info

%files -n python3-%{module_name}-doc
%{_docdir}/python3-%{module_name}/examples
%{_docdir}/python3-%{module_name}/html
%endif

%changelog
* Sat Aug 30 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.5-1.20140827git2aeb4ad
- Correct SOURCE0
- Move COPYING file to main package from doc subpackage

* Sat Aug 30 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.5-1.20140827git2aeb4ad
- Updated description

* Fri Aug 29 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.5-1.20140827git2aeb4ad
- Updated as per reviewer comments
- Split to different doc sub packages
- Added changelogs

* Tue Aug 26 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.5-1.20140827git2aeb4ad
- update to git code that includes documentation and license

* Tue Aug 26 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.5-1
- Initial rpm build


