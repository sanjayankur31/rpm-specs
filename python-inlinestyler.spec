# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global module_name inlinestyler
Name:           python-%{module_name}
Version:        0.1.7
Release:        1%{?dist}
Summary:        Inlines external CSS into HTML elements

License:        BSD
URL:            https://pypi.python.org/pypi/%{module_name}/%{version}
Source0:        https://pypi.python.org/packages/source/i/%{module_name}/%{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools

Requires:       python-cssutils python-lxml

%description
inlinestyler is an easy way to locally inline CSS into an HTML email message.

Styling HTML email is a black art. CSS works, but only when it's been placed
inline on the individual elements (and even then, not always) - which makes
development frustrating, and iteration slow.

The general solution is to use an in-lining service, which takes a message with
the CSS placed externally, and rewrites it so that all CSS is applied to the
individual elements. The most widely used of these services - and as far as I
can tell, the one that powers CampaignMonitor - is Premailer. It's a great
service, and the guys behind it put a lot of work into keeping it up to date
with the most recent discoveries in what works and what doesn't.

inlinestyler takes (most) of the functionality of Premailer, and makes it
available locally, accessible without having call a remote service.

%prep
%setup -q -n %{module_name}-%{version}
rm -rf %{module_name}.egg-info

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc AUTHORS CHANGELOG LICENSE README.rst
%{python_sitelib}/%{module_name}-%{version}-py?.?.egg-info/
%{python_sitelib}/%{module_name}


%changelog
* Mon May 05 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.1.7-1
- Initial rpm build
- 
