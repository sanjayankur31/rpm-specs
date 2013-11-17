%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Name:           python-django-authopenid
Version:        1.0.1
Release:        4%{?dist}
Summary:        OpenID authentication application for Django

Group:          Development/Languages
License:        ASL 2.0
# retain old name since that's what it's called in pypy
URL:            http://pypi.python.org/pypi/django-authopenid/
Source0:        http://pypi.python.org/packages/source/d/django-authopenid/django-authopenid-1.0.1.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools python-openid
# Doc build is borked
# BuildRequires:  python-sphinx
Requires:       python-openid
Requires:       python-django python-django-registration

# for the rename request
Provides:       django-authopenid = %{version}-%{release}
Obsoletes:      django-authopenid < 1.0.1-4

%description
Django authentication application with openid using django auth 
contrib. This application allows a user to connect to you website 
with a legacy account (user name/password) or an openid URL.

%prep
%setup -q -n django-authopenid-%{version}
sed -i "/zip_safe = False/d" setup.py
# Remove hidden files
pushd example
    find . -name "._*" -exec rm -fv '{}' \;
    find . -name ".DS_Store" -exec rm -fv '{}' \;
popd
rm django_authopenid/templates/authopenid/._yadis.xrdf

# remove egg-info to ensure that it's built by setup.py
rm -vfr django_authopenid.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Installs a copy in usr/ also!
rm -rvf $RPM_BUILD_ROOT%{_prefix}/django_authopenid

# Correct locations for examples
mv $RPM_BUILD_ROOT%{python_sitelib}/example $RPM_BUILD_ROOT/%{python_sitelib}/django_authopenid
# Correct non-executable-script error
chmod a+x $RPM_BUILD_ROOT%{python_sitelib}/django_authopenid/{example/manage,tests/test_store}.py
# Correct script-without-shebang
chmod a-x $RPM_BUILD_ROOT%{python_sitelib}/django_authopenid/example/templates/base.html

%files
%doc AUTHORS LICENSE NOTICE README THANKS CHANGES.md
%{python_sitelib}/django_authopenid
%{python_sitelib}/django_authopenid-*-py?.?.egg-info

%changelog
* Wed Jul 25 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0.1-4
- Bumpspec to release 4 to ensure clean upgrade path from obsoleted package

* Wed Jul 25 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0.1-2
- Remove egg-info to ensure that setup.py builds it #842633

* Tue Jul 24 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.0.1-1
- Initial build for rename request

