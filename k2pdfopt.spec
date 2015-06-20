Name:           k2pdfopt
Version:        2.31
Release:        1%{?dist}
Summary:        optimizes PDF/DJVU files for mobile e-readers

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
* Tue Jan  6 2015 Ankur Sinha <sanjay.ankur@gmail.com>
- 
