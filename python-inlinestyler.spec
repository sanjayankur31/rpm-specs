%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global module_name inlinestyler
Name:           python-%{module_name}
Version:        0.1.7
Release:        1%{?dist}
Summary:        Inlines external CSS into HTML elements

License:        BSD
URL:            https://pypi.python.org/pypi/%{module_name}/%{version}
Source0:        https://pypi.python.org/packages/source/i/%{module_name}/%{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools

Requires:       python-cssutils python-lxml

%description
inlinestyler is an easy way to locally inline CSS into an HTML email message.

%prep
%setup -q -n %{module_name}-%{version}
rm -rf %{module_name}.egg-info

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc AUTHORS CHANGELOG LICENSE README.rst
%{python2_sitelib}/%{module_name}-%{version}-py?.?.egg-info/
%{python2_sitelib}/%{module_name}


%changelog
* Tue May 06 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.7-1
- Updated description
- Corrected python directory macros
- Initial rpm build
