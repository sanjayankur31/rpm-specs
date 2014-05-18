%global modulename SPARQLWrapper
%global with_python3 1

Name:       python-%{modulename}
Summary:    SPARQL Endpoint interface to Python
Version:    1.5.2
Release:    1%{?dist}
Group:      Development/Libraries
License:    W3C and BSD
URL:        https://pypi.python.org/pypi/%{modulename}

Source0:    https://pypi.python.org/packages/source/S/%{modulename}/%{modulename}-%{version}.tar.gz    

BuildArch:         noarch
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-nose
BuildRequires:    python-six

%if 0%{?with_python3}
BuildRequires:    python3-devel
BuildRequires:    python-tools
BuildRequires:    python3-nose
BuildRequires:    python3-six
BuildRequires:    python3-setuptools
%endif

%description
This is a wrapper around a SPARQL service. It helps in creating the query URI
and, possibly, convert the result into a more manageable format.

%if 0%{?with_python3}
%package -n python3-%{modulename}
Summary:    SPARQL Endpoint interface to Python
Group:      Development/Libraries 

%description -n python3-%{modulename}
This is a wrapper around a SPARQL service. It helps in creating the query URI
and, possibly, convert the result into a more manageable format.
%endif


%prep
%setup -q -n %{modulename}-%{version} 

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

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
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

%check
nosetests

%if 0%{?with_python3}
pushd %{py3dir}
nosetests-3.3 build
popd
%endif

%files
%doc AUTHORS.txt ChangeLog.txt LICENSE.txt README.txt
%{python2_sitelib}/%{modulename}-*.egg-info
%{python2_sitelib}/%{modulename}

%if 0%{?with_python3}
%files -n python3-%{modulename}
%doc AUTHORS.txt ChangeLog.txt LICENSE.txt README.txt
%{python3_sitelib}/%{modulename}-*.egg-info
%{python3_sitelib}/%{modulename}
%endif 


%changelog
* Sun Apr 20 2014 Dan Scott <dan@coffeecode.net> - 1.5.2-1
- Initial spec
