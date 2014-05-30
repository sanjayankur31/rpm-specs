%{!?python2_sitelib: %global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global module_name stopforumspam

Name:           python-django-%{module_name}
Version:        1.4.1
Release:        1%{?dist}
Summary:        Django middleware for blocking IPs listed in stopforumspam.com

License:        BSD
URL:            https://pypi.python.org/pypi/stopforumspam/
Source0:        https://pypi.python.org/packages/source/s/stopforumspam/stopforumspam-1.4.1.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools

Requires:       python-django

%description
Tired of comment spam, form spam and dumb crawlers? A django application that
provides middleware for blocking IPs listed in stopforumspam.com's database. A
simple management command is provided for updating the database:

    manage.py sfsupdate [--force]

Using this command, all IPs are stored in Django models. Using django-admin,
it's possible to add your own extra IP addresses on a permanent database.

%prep
%setup -q -n %{module_name}-%{version}
rm -frv stopforumspam.egg-info


%build
%{__python2} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc README.md
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%{python_sitelib}/%{module_name}


%changelog
* Fri May 30 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.4.1-1
- Initial rpm build


