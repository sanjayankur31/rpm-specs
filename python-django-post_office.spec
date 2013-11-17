# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global app_name django-post_office
Name:           python-%{app_name}
Version:        0.3.1
Release:        2%{?dist}
Summary:        Allows you to log email activities and send mail asynchronously
Group:          Applications/Internet


License:        MIT
URL:            https://pypi.python.org/pypi/%{app_name}
Source0:        https://pypi.python.org/packages/source/d/%{app_name}/%{app_name}-0.3.1.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools
# For tests
BuildRequires:  python-django
Requires:       python-django

%description
Django Post Office is a simple app that allows you to send email asynchronously
in Django. Supports HTML email, database backed templates and logging.

``post_office`` is implemented as a Django ``EmailBackend`` so you don't need
to change any of your code to start sending email asynchronously.


%prep
%setup -q -n %{app_name}-%{version}

#remove bundled egg info
rm -rf django_post_office.egg-info


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%check
%{__python} post_office/tests/runtests.py

 
%files
%doc README.rst AUTHORS.rst LICENSE.txt
%{python_sitelib}/post_office/
%{python_sitelib}/django_post_office-%{version}-py?.?.egg-info/


%changelog
* Fri May 03 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.1-2
- Update spec as per review: 959172
- Run tests
- add python-django as requires
- remove bundled egg info

* Fri May 03 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.1-1
- Initial rpm build

