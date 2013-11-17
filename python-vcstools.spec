%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global realname vcstools
Name:           python-%{realname}
Version:        0.1.29
Release:        1%{?dist}
Summary:        Version Control System tools for Python

License:        BSD
URL:            https://pypi.python.org/pypi/%{reanname}
Source0:        https://pypi.python.org/packages/source/v/%{realname}/%{realname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
BuildRequires:  python-sphinx


%description
The vcstools module provides a Python API for interacting with different 
version control systems (VCS/SCMs). The VcsClient class provides an API 
for seamless interacting with Git, Mercurial (Hg), Bzr and SVN. The focus 
of the API is manipulating on-disk checkouts of source-controlled trees. 
Its main use is to support the rosinstall tool.

%prep
%setup -q -n %{realname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%doc
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-*.egg-info

%changelog
* Sat Mar 16 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.29-1
- Update to latest

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.26-2.20130102gitd41568f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Rich Mattes <richmattes@gmail.com> - 0.1.26-1.20130102gitd41568f
- Update to release 0.1.26

* Fri Oct 26 2012 Rich Mattes <richmattes@gmail.com> - 0.1.24-1.20121026gitba30262
- Update to release 0.1.24

* Mon Aug 28 2012 Rich Mattes <richmattes@gmail.com> - 0.1.21-1.20120828hg0fba0588
- Update to release 0.1.21

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.17-4.20120606hg6205f4fc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Rich Mattes <richmattes@gmail.com> - 0.1.17-3.20120606hg6205f4fc
- Added el6 support
- Enabled unit tests

* Wed Jun 06 2012 Rich Mattes <richmattes@gmail.com> - 0.1.17-2.20120606hg6205f4fc
- Update package release to include hg checkout info
- Remove el5 specific RPM_BUILD_ROOT removal from install section

* Tue Jun 05 2012 Rich Mattes <richmattes@gmail.com> - 0.1.17-1
- Update to release 0.1.17

* Wed Apr 25 2012 Rich Mattes <richmattes@gmail.com> - 0.1.4-1
- Initial package
