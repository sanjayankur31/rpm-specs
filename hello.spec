Name:           hello
Version:        2.8
Release:        1%{?dist}
Summary:        GNU hello world package

License:        GPLv3+
URL:            https://www.gnu.org/software/%{name}/
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

#BuildRequires:  
#Requires:       

%description
The GNU hello world package

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

%find_lang %{name}

%files -f %{name}.lang
%doc README README-release THANKS AUTHORS COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%{_infodir}/dir
%{_infodir}/%{name}.*



%changelog
* Thu Apr 24 2014 Ankur Sinha <sanjay.ankur@gmail.com> - 2.8-1
- Initial rpm build
