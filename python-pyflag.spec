%global src_name pyflag
Name:           python-pyflag
Version:        0.85
Release:        2%{?dist}
Summary:        Forensic and Log Analysis GUI

License:        GPLv2+
URL:            http://www.pyflag.net
Source0:        http://sourceforge.net/projects/pyflag/files/pyflag/0.85/pyflag-0.85.tar.bz2


BuildRequires:  python-devel MySQL-python python-imaging pexpect pynetsnmp libextractor-devel libpcap-devel zlib-devel file-libs mysql-server mysql libtool swig clamav-lib file-devel


%description
This application is designed to assist IT security professionals with
analyzing log files, tcpdump files and hard disk images for forensic
evidence.It performs data analysis using a MYSQL database.

%package devel
Summary: Libraries for Pyflag
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The package %{src_name}-devel contains the static libraries needed for Pyflag Development

%prep
%setup -q -n %{src_name}-%{version}

%build 
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#Adding Shebang
sed -i -e '1i#!/usr/bin/python' $RPM_BUILD_ROOT/%{_bindir}/conf.py

pushd $RPM_BUILD_ROOT
#permissions for executable files
for file in ./%{python_sitelib}/%{src_name}/{jpeg_carver,Tester,regkey_load,FlagHTTPServer,mspst,FlagGTKServer,examine,pdf_carver,pyclamd,zip_carver}.py; do
   chmod a+x $file
done
for file in ./%{_datarootdir}/%{src_name}/utilities/{EventLogTool,indexer,compare,export_index_hits,incremental_load,nsrl_load,whois_load,raid_guess}.py; do
   chmod a+x $file
done
for file in ./%{_datarootdir}/%{src_name}/utilities/{whois_load,regkeys_load,update_version}.sh; do
   chmod a+x $file
done
chmod a+x ./%{python_sitelib}/%{src_name}/FileFormats/libole2.py
popd

# remove static libraries
find $RPM_BUILD_ROOT -name "*.a" -execdir rm -fv '{}' \;
find $RPM_BUILD_ROOT -name "*.la" -execdir rm -fv '{}' \;

%files
%doc COPYING README TODO
%{python_sitearch}/%{src_name}
#%{python_sitelib}/%{src_name}
#%{_bindir}/*
%{_libdir}/%{src_name}/*.so.*
%{_datarootdir}/%{src_name}/*
%{_mandir}/man1/*

%files devel
%{_libdir}/%{src_name}/*.so

%changelog
* Thu Dec 01 2011 Soumya Kanti Chakraborty <soumya@fedoraproject.org> - 0.85-2
- Fixed Make issues for 64 bit machines.
* Thu Nov 24 2011 Soumya Kanti Chakraborty <soumya@fedoraproject.org> - 0.85-1
- initial release
