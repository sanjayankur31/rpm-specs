%global svn_rev 6405
Name:           opendental
Version:        7.5
Release:        0.1svn%{svn_rev}%{?dist}
Summary:        Open Source Practice Management

License:        GPL+
URL:            http://www.opendental.com/index.html

# svn export https://70.90.133.65:23793/svn/opendental/opendental7.5 opendental7.5
# tar -xvzf opendental7.5.tar.gz opendental7.5/
Source0:        %{name}%{version}.tar.gz

BuildRequires:  nant-devel mono-devel monodevelop mono-nunit-devel

%description
asdsad

%prep
%setup -q -n %{name}%{version}


%build
mdtool build --buildfile:OpenDental5_6.sln LINUX DISABLE_MICROSOFT_OFFICE


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc



%changelog
* Thu Jun 23 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.5-1
- intial rpm build
