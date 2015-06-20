Name:           cronometer
Version:        0.9.9
Release:        1%{?dist}
Summary:        

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
* Sun Jul 20 2014 Ankur Sinha <sanjay.ankur@gmail.com>
- 
