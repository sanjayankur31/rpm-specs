Name:     perl-IO-Termios
Version:  0.03
Release:  1%{?dist}
Summary:  Supply termios(3) methods to IO::Handle objects

Group:    Development/Libraries
License:  GPL+ or Artistic
URL:      http://search.cpan.org/~pevans/IO-Termios-%{version}/
Source0:  http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/IO-Termios-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
BuildRequires: perl(ExtUtils::MakeMaker)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This class extends the generic IO::Handle object class by providing methods 
which access the system's terminal control termios(3) operations.

%prep
%setup -q -n IO-Termios-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} ';' 2>/dev/null
chmod -R u+w $RPM_BUILD_ROOT/*



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{perl_vendorlib}/IO/
%{_mandir}/man3/*.3pm*

%changelog
* Fri Dec 20 2013 Charles Amey <kc8hfi@gmail.com> - 0.03-1
- Initial build
