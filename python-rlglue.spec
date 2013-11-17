%global with_python3 0
%global module_name rlglue

Name:           python-%{module_name}
Version:        2.02
Release:        1%{?dist}
Summary:        Python codec for %{module_name}

License:        ASL 2.0
URL:            http://glue.rl-community.org/wiki/Python_Codec
Source0:        https://pypi.python.org/packages/source/r/%{module_name}/%{module_name}-%{version}.tar.gz
Source1:        PythonCodec.pdf

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       rlglue numpy

%if 0%{?with_python3}
BuildRequires:  python3-devel 
#BuildRequires:  python3-setuptools
%endif # if with_python3

%description
Python RL-Glue Codec, a software library that provides socket-compatibility
with the RL-Glue Reinforcement Learning software library.

%if 0%{?with_python3}
%package -n python3-%{module_name}
Summary:        Python codec for %{module_name}

%description -n python3-%{module_name}

%endif # with_python3

%prep
%setup -q -n %{module_name}-%{version}
cp %{SOURCE1} .

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
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3
 
%files
%doc PythonCodec.pdf
%{python_sitelib}/%{module_name}/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{module_name}
%endif # with_python3

%changelog
* Tue Mar 26 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 2.02-1
- Initial rpmbuild

