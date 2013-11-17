Name:           django-celery
Version:        2.2.4
Release:        1%{?dist}
Summary:        Django Celery Integration
Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/%{name}
Source0:        http://pypi.python.org/packages/source/d/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools-devel python-devel
Requires:       Django python-celery

%description
django-celery provides Celery integration for Django; Using the Django ORM and 
cache backend for storing results, autodiscovery of task modules for 
applications listed in INSTALLED_APPS, and more.

Celery is a task queue/job queue based on distributed message passing. It is 
focused on real-time operation, but supports scheduling as well.

The execution units, called tasks, are executed concurrently on a single or more
worker servers. Tasks can execute asynchronously (in the background) or 
synchronously (wait until ready).

%prep
%setup -q 
rm -rf docs/.templates
rm -rf docs/.static*
%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%files 
%defattr(-,root,root,-)
%doc LICENSE FAQ README AUTHORS THANKS TODO Changelog docs/
%{_bindir}/djcelerymon
%{python_sitelib}/djcelery/
%{python_sitelib}/django_celery*.egg-info

%changelog
* Thu Apr 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 2.2.4-1
- initial spec
