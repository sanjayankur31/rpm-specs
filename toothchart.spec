%global debug_package %{nil}
Name:           toothchart
Version:        0.02.0
Release:        0.1beta%{?dist}
Summary:        A PHP script which graphically shows how a baby's primary teeth have erupted

License:        GPLv2
URL:            http://sourceforge.net/projects/toothchart/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-beta-0.02.0.tar.gz
BuildArch:      noarch

Requires:       php

%description
The Baby Tooth chart is a PHP script which graphically shows how a 
baby's primary teeth have erupted - Eventually it'll become a 
POST/PHP-Nuke module. Uses only PHP and static images (i.e. no 
PHP graphics or FLASH, so no extra libraries needed)

%prep
%setup -q -n %{name}

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}/images/
install -p -m 0644  index.php -t $RPM_BUILD_ROOT/%{_datadir}/%{name}/
install -p -m 0644  images/* -t $RPM_BUILD_ROOT/%{_datadir}/%{name}/images/

install -d $RPM_BUILD_ROOT/%{_docdir}/%{name}/
install -p -m 0644 docs/* -t $RPM_BUILD_ROOT/%{_docdir}/%{name}/

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}/
%{_docdir}/%{name}/

%changelog
* Wed Jun 29 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.02.0-0.1beta
- corrected license
- corrected version,release fields
