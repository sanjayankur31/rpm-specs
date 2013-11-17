%global with_python3 0
%global snapdate 2010-03-22
%global tarname PyODE-snapshot-%{snapdate}

Name:           pyode
Version:        1.2.0
Release:        4%{?dist}
Summary:        Open-source Python bindings for The Open Dynamics Engine
Group:          Development/Libraries

License:        BSD or LGPLv2+
URL:            http://pyode.sourceforge.net/

# https://downloads.sourceforge.net/project/pyode/pyode/snapshot-2010-03-22/PyODE-snapshot-2010-03-22.tar.gz
Source0:        http://downloads.sourceforge.net/%{name}/%{name}/snapshot-%{snapdate}/%{tarname}.tar.gz 

# http://comments.gmane.org/gmane.comp.python.pyode.user/174
Patch0:         0001-pyode-%{snapdate}-fix-test-segfault.patch

# Fix rounding-error test failures on Fedora 17-20 (but not el6!)
Patch1:         0002-pyode-%{snapdate}-use-almost-equal-assert.patch

BuildRequires:  python2-devel python-setuptools
BuildRequires:  ode-devel
BuildRequires:  Pyrex

Requires:       ode

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

%description
A set of open-source Python bindings for The Open Dynamics Engine, an
open-source physics engine. PyODE also includes an XODE parser.

%if 0%{?with_python3}
%package -n python3-pyode
Group:          Applications/System
Summary:        Open-source Python bindings for The Open Dynamics Engine

%description -n python3-pyode
A set of open-source Python bindings for The Open Dynamics Engine, an
open-source physics engine. PyODE also includes an XODE parser.

%endif # with_python3

%prep
%setup -q -n %{tarname}

# Fix wrong end of line file encoding error
sed -i 's/\r//' examples/tutorial3.py 

%patch0 -p1 -b-gc-patch
%patch1 -p0 -b-assert-amlost-equal-patch

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
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

chmod 0755 $RPM_BUILD_ROOT/%{python_sitearch}/ode.so

%check
export PYTHONPATH=build/lib.linux-%{_target_cpu}-%{python_version}
%{__python} tests/test_xode.py


%files
%doc AUTHORS ChangeLog LICENSE LICENSE-BSD README examples
%{python_sitearch}/PyODE-%{version}-py?.?.egg-info
%{python_sitearch}/xode/
%{python_sitearch}/ode.so


%if 0%{?with_python3}
%files -n python3-pyode
%doc AUTHORS ChangeLog LICENSE LICENSE-BSD README examples
%{python3_sitelib}/%{name}/
%endif # with_python3

%changelog
* Fri Apr 26 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2.0-4
- Add another patch to use almost equal assertion
- Fix wrong end of line file encoding rpmlint error
- Remove pyrex from requires

* Thu Apr 25 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2.0-3
- Update as per reviewer comments: 
- https://bugzilla.redhat.com/show_bug.cgi?id=927611
- Add patch to fix tests
- Add group tag for epel
- add documentation

* Mon Apr 15 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2.0-2
- Update as per comments in rhbz
- https://bugzilla.redhat.com/show_bug.cgi?id=927611
- Changed URL
- Added phony check section for readability
- Few more cosmetic changes

* Tue Mar 26 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2.0-1
- Initial rpmbuild

