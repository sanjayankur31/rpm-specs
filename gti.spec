Name:           gti
Version:        1.2
Release:        1%{?dist}
Summary:        Just a silly git launcher inspired by sl

License:        
URL:            
Source0:        

BuildRequires:  
Requires:       

%description


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc



%changelog
* Wed Jul 30 2014 Ankur Sinha <sanjay.ankur@gmail.com>
- 
