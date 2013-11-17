# To make packaging a little simple

%global binaryname      nut
Name:           nut-nutrition
Version:        15.7
Release:        3%{?dist}
Summary:        A nutritional Software

## couldn't find a group!!?!
Group:          Applications/Text
License:        GPLv2+
URL:            http://nut.sourceforge.net/ 
Source0:        http://downloads.sourceforge.net/%{binaryname}/%{binaryname}-%{version}.tar.gz
Patch0:         nut-Makefile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
NUT allows you to record what you eat and analyze your meals for
nutrient composition. The database included is the USDA Nutrient
Database for Standard Reference, Release 22.


%prep
%setup -q -n %{binaryname}-%{version}
%patch0 


%build
# change the FOODDIR location
%{__sed} -i "s|\/usr\/local\/lib\/nut|\%{_prefix}\/share\/%{binaryname}|" Makefile 
export CFLAGS="%{optflags}"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_bindir}
install -d $RPM_BUILD_ROOT/%{_mandir}/man1/
install -d $RPM_BUILD_ROOT/%{_datadir}/%{binaryname}/
install -p -m 0755 %{binaryname} $RPM_BUILD_ROOT/%{_bindir}/%{binaryname}
install -p %{binaryname}.1 $RPM_BUILD_ROOT/%{_mandir}/man1/%{binaryname}.1
cp -pR raw.data/* $RPM_BUILD_ROOT/%{_datadir}/%{binaryname}/

%files
%defattr(-,root,root,-)
%doc LICENSE README CREDITS
%{_bindir}/%{binaryname}
%{_datadir}/%{binaryname}/
%{_mandir}/man1/%{binaryname}.1.*

%changelog
* Fri Feb 25 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 15.7-3
- Changed spec name

* Sat Jul 17 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 15.7-2
- corrected spec to include Food Data files

* Sat Jul 17 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 15.7-1
- initial package build
