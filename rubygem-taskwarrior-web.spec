%global app_root %{_datadir}/%{name}

Name:           rubygem-taskwarrior-web
Version:        1.1.11
Release:        1%{?dist}
Summary:        A web interface for Taskwarrior


License:        ASL 2.0
URL:            http://theunraveler.github.com/taskwarrior-web
Source0:        https://rubygems.org/downloads/taskwarrior-web-1.1.11.gem

BuildArch:      noarch
BuildRequires:  ruby ruby-devel
Requires:       ruby(abi) = 1.8
Requires:       ruby(sinatra)
Requires:       ruby(activesupport)
Requires:       ruby(json)
Requires:       ruby(parseconfig)
Requires:       ruby(vegas)

# Not in repos
Requires:       ruby(rack-flash3)

#Under review: 1062049
Requires:       ruby(rinku)

Requires:       ruby(versionomy)
Requires:       ruby(sinatra-simple-navigation)

%description
A web interface for the Taskwarrior todo application. Because being a neckbeard
is only fun sometimes.


%prep
gem unpack -V %{SOURCE0}
%setup -q -D -T -n %{name}-%{version}

%build
mkdir -p %{buildroot}%{app_root}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{_bindir}
cp -r * %{buildroot}%{app_root}
find %{buildroot}%{app_root}/lib -type f | xargs chmod -x
chmod 0755 %{buildroot}%{app_root}/bin/task-web
rdoc --op %{buildroot}%{_defaultdocdir}/%{name}

%install
rm -rf $RPM_BUILD_ROOT

 
%check


%files
%doc
# For noarch packages: ruby_sitelib
#%{ruby_sitelib}/*
# For arch-specific packages: ruby_sitearch
#%{ruby_sitearch}/*


%changelog
* Fri Aug 01 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.1.11-1
- Initial rpmbuild
