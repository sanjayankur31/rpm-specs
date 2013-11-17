%global with_python3 1
%global module_name wstool

Name:           python-%{module_name}
Version:        0.0.3
Release:        1%{?dist}
Summary:        Tool for managing a workspace of multiple heterogeneous SCM repositories

License:        BSD
URL:            http://www.ros.org/wiki/%{module_name}
# wget --content-disposition https://github.com/vcstools/wstool/archive/0.0.3.tar.gz
Source0:        %{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools

%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%endif # if with_python3

Requires:       python-vcstools
Requires:       python-rosinstall
Requires:       python-dateutil

%description
wstool provides commands to manage several local SCM repositories (supports
git, mercurial, subversion, bazaar) based on a single workspace definition file
(.rosinstall).

wstool replaces the rosws tool for catkin workspaces. As catkin workspaces
create their own setup file and environment, wstool is reduced to version
control functions only. So wstool does not have a "regenerate" command, and
does not allow adding non-version controlled elements to workspaces. In all
other respects, it behaves the same as rosws.

%if 0%{?with_python3}
%package -n python3-wstool
Summary:        Tool for managing a workspace of multiple heterogeneous SCM repositories
Requires:       python-vcstools
Requires:       python-rosinstall
Requires:       python3-dateutil

%description -n python3-wstool
wstool provides commands to manage several local SCM repositories (supports
git, mercurial, subversion, bazaar) based on a single workspace definition file
(.rosinstall).

wstool replaces the rosws tool for catkin workspaces. As catkin workspaces
create their own setup file and environment, wstool is reduced to version
control functions only. So wstool does not have a "regenerate" command, and
does not allow adding non-version controlled elements to workspaces. In all
other respects, it behaves the same as rosws.
%endif # with_python3

%prep
%setup -q -n %{module_name}-%{version}


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
mv -v build/scripts-3.3/wstool build/scripts-3.3/python3-wstool
popd
%endif # with_python3

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3 

%files
%doc LICENSE README.rst doc/changelog.rst
%{_bindir}/%{module_name}
%{python_sitelib}/%{module_name}/
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info/

%if 0%{?with_python3}
%files -n python3-wstool
%doc LICENSE README.rst doc/changelog.rst
%{_bindir}/python3-%{module_name}
%{python3_sitelib}/%{module_name}/
%{python3_sitelib}/%{module_name}-%{version}-py?.?.egg-info/
%endif # with_python3

%changelog
* Mon Aug 26 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.0.3-1
- Rename python3 bin script

* Sun Aug 25 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.0.3-1
- Update source to github source
- Add py3 support

* Sat Mar 16 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.0.3-1
- Initial rpmbuild

