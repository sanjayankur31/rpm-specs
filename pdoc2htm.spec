Name:           pdoc2htm
Version:        1.3.0
Release:        1%{?dist}
Summary:        Convert the information text, printed by command-line programs, to XHTML 1.0 format.

License:        LGPLv2.1+
URL:            http://www.turkupetcentre.net/software/show.php?program=%{name}
Source0:        http://www.turkupetcentre.net/software/src/%{name}_1_3_0.zip

%description
Convert the information text, printed by command-line programs,
to XHTML 1.0 format.


%prep
%setup -q -n %{name}


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc


%changelog
* Fri Jun 17 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.0-1
- initial rpm build
