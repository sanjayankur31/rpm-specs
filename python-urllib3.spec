%if 0%{?fedora}
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global srcname urllib3

Name:           python-%{srcname}
Version:        1.5
Release:        3%{?dist}
Summary:        Python HTTP library with thread-safe connection pooling and file post

License:        MIT
URL:            http://urllib3.readthedocs.org/
Source0:        http://pypi.python.org/packages/source/u/%{srcname}/%{srcname}-%{version}.tar.gz
# Patch to change default behaviour to check SSL certs for validity
# https://bugzilla.redhat.com/show_bug.cgi?id=855320
Patch0:         python-urllib3-default-ssl-cert-validate.patch
### TODO: Send this to upstream urllib3
# make all imports of things in packages try system copies first
Patch1:         python-urllib3-unbundle.patch
### TODO: Send this upstream
# Compatibility with python-2.6's unittest
Patch2:         python-urllib3-py2.6-compat.patch
# Remove logging-clear-handlers from setup.cfg because it's not available in RHEL6's nose
Patch100:       python-urllib3-old-nose-compat.patch

BuildArch:      noarch

Requires:       ca-certificates
Requires:       python-six

### TODO: In review https://bugzilla.redhat.com/show_bug.cgi?id=885013
# Requires: python-backports-ssl_match_hostname
%if 0%{?rhel} <= 6
BuildRequires:  python-ordereddict
Requires:       python-ordereddict
%endif

BuildRequires:  python2-devel
# For unittests
BuildRequires:  python-nose
BuildRequires:  python-six
BuildRequires:  python-tornado

%if 0%{?with_python3}
BuildRequires:  python3-devel
# For unittests
BuildRequires:  python3-nose
BuildRequires:  python3-six
BuildRequires:  python3-tornado
%endif # with_python3

%description
Python HTTP module with connection pooling and file POST abilities.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Requires:       ca-certificates
Requires:       python3-six
# Note: Will not run with python3 < 3.2 (unless python3-backports-ssl_match_hostname is created)
Summary:        Python3 HTTP library with thread-safe connection pooling and file post
%description -n python3-%{srcname}
Python3 HTTP module with connection pooling and file POST abilities.
%endif # with_python3


%prep
%setup -q -n %{srcname}-%{version}

### TODO: unbundle everything in packages/:
# Need:
# ssl_match_hostname https://bugzilla.redhat.com/show_bug.cgi?id=885013
# rm -rf urllib3/packages/
rm -rf urllib3/packages/six*
rm -rf urllib3/packages/ordered_dict*

%patch0 -p1
%patch1 -p1
%if 0%{?rhel} && 0%{?rhel} <= 6
%patch100 -p1
%patch2 -p1
%endif

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python_sitelib}/dummyserver

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

# dummyserver is part of the unittest framework
rm -rf %{buildroot}%{python3_sitelib}/dummyserver
popd
%endif # with_python3

%check
nosetests

%if 0%{?with_python3}
pushd %{py3dir}
nosetests-%{python3_version}
popd
%endif # with_python3

%files
%doc CHANGES.rst LICENSE.txt README.rst CONTRIBUTORS.txt
# For noarch packages: sitelib
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc LICENSE.txt
# For noarch packages: sitelib
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 1.5-3
- Renamed patches to python-urllib3-*
- Fixed ssl check patch to use the correct cert path for Fedora.
- Included dependency on ca-certificates
- Cosmetic indentation changes to the .spec file.

* Tue Feb  5 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-2
- python3-tornado BR and run all unittests on python3

* Mon Feb 04 2013 Toshio Kuratomi <toshio@fedoraproject.org> 1.5-1
- Initial fedora build.

