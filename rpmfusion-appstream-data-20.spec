Name:           rpmfusion-appstream-data-20
Version:        1
Release:        1%{?dist}
Summary:        AppStream metadata for RPMFusion

License:        CC0
URL:            http://rpmfusion.org
Source0:        rpmfusion-20.xml.gz
Source1:        rpmfusion-20-icons.tar.gz

BuildRequires:  libappstream-glib
BuildArch:      noarch

#Requires:       

%description
This package provides AppStream metadata for RPMFusion packages

%prep
# NOTHING

%build
#NOTHING

%install
DESTDIR=%{buildroot} appstream-util install %{SOURCE0} %{SOURCE1}

%files
%{_datadir}/app-info/xmls/rpmfusion-20.xml.gz
%{_datadir}/app-info/icons/rpmfusion-20


%changelog
* Thu Aug 14 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1-1
- Initial package
