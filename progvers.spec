Name:           progvers
Version:        0.4.1
Release:        1%{?dist}
Summary:        Extracts program version information from executable program files

License:        LGPLv2.1+
URL:            http://www.turkupetcentre.net/software/show.php?program=%{name}
Source0:        http://www.turkupetcentre.net/software/src/%{name}_0_4_1.zip

%description
Program for extracting program version information from an executable
program file into a text file in format:
program_name = xxx 
program_version = x.y.z 
compilation_date = YYYY-MM-DD hh:mm:ss
etc

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
