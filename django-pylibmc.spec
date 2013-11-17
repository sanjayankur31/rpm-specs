%global git_date    20110806
%global git_version b56e74

Name:           django-pylibmc
Version:        0.2.1
Release:        2.%{git_date}git%{git_version}%{?dist}
Summary:        Django cache backend using pylibmc

License:        BSD
URL:            http://github.com/jbalogh/django-pylibmc

# git clone https://github.com/jbalogh/django-pylibmc
# cd django-pylibmc
# git archive --format=tar HEAD | xz  > {name}-{version}.{git_date}git{git_version}.tar.xz
Source0:        %{name}-%{version}.%{git_date}git%{git_version}.tar.xz        
        
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pylibmc
BuildRequires:  Django

%description
Django-pylibmc package provides a memcached cache backend for 
Django using pylibmc. You want to use pylibmc because it's fast.

%prep
%setup -q -cn %{name}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc LICENSE README.rst
%{python_sitelib}/*.egg-info/
%{python_sitelib}/django_pylibmc/



%changelog
* Thu Aug 11 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.2.1-2.20110806gitb56e74
- Resolved file location issue

* Fri Aug 05 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.2.1-1.20110806gitb56e74
- Initial RPM release
