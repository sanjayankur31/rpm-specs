%global module_name pykalman
%global with_python3    1

Name:           python-%{module_name}
Version:        0.9.5
Release:        1%{?dist}
Summary:        Kalman Filter, Smoother, and EM algorithm

License:        BSD
URL:            http://%{module_name}.github.com/
Source0:        https://pypi.python.org/packages/source/p/%{module_name}/%{module_name}-0.9.5.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-nose numpy python-sphinx scipy

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-nose python3-numpy python3-sphinx
BuildRequires:  python3-scipy
%endif

%description
Kalman Filter, Smoother, and EM Algorithm for Python

%if 0%{?with_python3}
%package -n python3-%{module_name}
Summary:    Kalman Filter, Smoother, and EM Algorithm

%description -n python3-%{module_name}
Kalman Filter, Smoother, and EM Algorithm for Python
%endif

%prep
%setup -q -n %{module_name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check
nosetests %{module_name}/tests/

%if 0%{?with_python3}
pushd %{py3dir}
nosetests-3.4 %{module_name}/tests/
popd
%endif # with_python3
 
%files
%{python_sitelib}/%{module_name}/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{module_name}
%{python3_sitelib}/%{module_name}/
%{python3_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Tue Aug 26 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.5-1
- Initial rpm build
