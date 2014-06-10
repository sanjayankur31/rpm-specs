%global commit 4464fb0db62602276df27ed241cef3020f8c8fc9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python-catkin_tools
Version:        0.1.0
Release:        1%{?dist}
Summary:        Command line tools for working with catkin

Group:          Development/Tools
License:        ASL 2.0
URL:            http://catkin-tools.readthedocs.org
Source0:        https://github.com/catkin/catkin_tools/archive/%{commit}/catkin_tools-%{commit}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-argparse
BuildRequires:  python-catkin_pkg
BuildRequires:  python-mock
BuildRequires:  python-nose
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  PyYAML
Requires:       python-argparse
Requires:       python-catkin_pkg
Requires:       python-setuptools
Requires:       PyYAML

%description
Provides command line tools for working with catkin

%prep
%setup -qn catkin_tools-%{commit}

%build
%{__python2} setup.py build
make -C docs html man
rm -f docs/_build/html/.buildinfo

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
install -d %{buildroot}%{_mandir}/man1
install -m0644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/

# Removed the installed test
rm -rf %{buildroot}%{python2_sitelib}/tests

%check
nosetests -w tests

%files
%doc LICENSE README.md docs/_build/html
%{python2_sitelib}/catkin_tools
%{python2_sitelib}/catkin_tools-%{version}-py?.?.egg-info
%{_bindir}/catkin
%{_mandir}/man1/*.1.gz

%changelog
* Mon Jun  9 2014 Scott K Logan <logans@cottsay.net> - 0.1.0-1
- Initial package
