%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Name:           darkclient
Version:        0.1
Release:        3%{?dist}
Summary:        A command line tool for the darkroom service

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/kushaldas/%{name}
Source0:        http://kushal.fedorapeople.org/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-setuptools python2-devel


%description
A command line tool which produces machine parse-able output from darkroom
service of GNU Buildids.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1  --skip-build --root $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{name}
%config(noreplace)     %{_sysconfdir}/%{name}.conf
%{python_sitelib}/%{name}-%{version}*.egg-info



%changelog
* Wed Apr 04 2011 Kushal Das <kushal@fedoraproject.org> 0.1-3
- Using more macros

* Tue Apr 03 2011 Kushal Das <kushal@fedoraproject.org> 0.1-2
- Added BR and macro name change

* Tue Apr 03 2011 Kushal Das <kushal@fedoraproject.org> 0.1-1
- v0.1 release

