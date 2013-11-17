%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Name:           django-authopenid
Version:        1.0.1
Release:        3%{?dist}
Summary:        Openid authentification application for Django

Group:          Development/Languages
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}/
Source0:        http://pypi.python.org/packages/source/d/%{name}/%{name}-1.0.1.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel python-setuptools python-openid
# Doc build is borked
# BuildRequires:  python-sphinx
Requires:       python-openid django-registration

%description
Django authentification application with openid using django auth 
contrib. This application allow a user to connect to you website 
with a legacy account (username/password) or an openid url.

%prep
%setup -q
sed -i "/zip_safe = False/d" setup.py
# Remove hidden files
pushd example
    find . -name "._*" -exec rm -fv '{}' \;
    find . -name ".DS_Store" -exec rm -fv '{}' \;
popd
rm django_authopenid/templates/authopenid/._yadis.xrdf

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
* Fri Jan 06 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.0.1-3
- spec bump for gcc 4.7 rebuild

* Thu Aug 18 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.0.1-2
- use pypi sources

* Wed Aug 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.0.1-1
- repackage to unretire

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.6-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ian Weller <ianweller@gmail.com> 0.9.6-2
- Add patch from I. Vazquez (django-authopenid-0.9.6-keyword.patch)

* Sun Feb 15 2009 Ian Weller <ianweller@gmail.com> 0.9.6-1
- Initial package build
