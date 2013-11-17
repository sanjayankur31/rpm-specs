Name:           evolution-remove-duplicates
Version:        20100104
Release:        1%{?dist}
Summary:        An evolution plugin to remove duplicate messages

Group:          Applications/Internet
License:        GPLv3
URL:            http://gnome.eu.org/cgit/%{name}

# Generated from the git clone
# git clone git://gnome.eu.org/evolution-remove-duplicates
# cd ..
# tar -cjf evolution-remove-duplicates-20100104.tar.bz2  evolution-remove-duplicates/

Source0:        http://gnome.eu.org/cgit/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  evolution-devel intltool gnome-common

%description
A plugin that enables users to remove duplicate messages in Evolution


%prep
%setup -q -n %{name}

%build
./autogen.sh
%configure 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%{_libdir}/evolution/*/plugins/liborg-gnome-remove-duplicates.*
%{_libdir}/evolution/*/plugins/org-gnome-remove-duplicates.*
%{_datadir}/evolution/*/errors/org-gnome-remove-duplicates.error



%changelog
* Tue Jan 04 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20100104-1
- rebuilt to support 2.32 in Fedora 14
