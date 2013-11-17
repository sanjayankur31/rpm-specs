Name:           openemr
Version:        4.0.0
Release:        2%{?dist}
Summary:        Practice management, EMR, prescription writing and medical billing application

License:        GPLv2+
URL:            http://www.oemr.org/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz 

BuildArch:      noarch
Requires:       httpd php mysql
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Major features of OpenEMR

    Free (Free Libre Open Source Software)
    Open Source
    Multilanguage Support
    Free Upgrades
    Free online support
    Electronic Billing (includes Medicare)
    Document management
    Integrated practice management
    E-Prescribing
    Insurance tracking (3 insurances)
    Easy to customize
    Easy Installation (Thank You! Brady Miller and Obinna Amalu.)
    Voice recognition ready (MS Windows Operating Systems)
    Web based (Secure access with SSL certificates)
    Integration with external general accounting program SQL-Ledger
    Built in Scheduler
    Multi-facility capable
    Prescriptions by printed script, fax or email

%prep
%setup -q
rm -rf contrib/util/ubuntu_package_scripts
rm -rf phpmyadmin
rm -rf library/adldap
rm -rf library/adodb


find ./ -name "*.sql" -exec chmod a-x '{}' \;
find ./ -name "*.php" -exec chmod a-x '{}' \;
find ./ -name "*.inc" -exec chmod a-x '{}' \;
find ./ -name "*.jpg" -exec chmod a-x '{}' \;
find ./ -name "*.xsl" -exec chmod a-x '{}' \;
find ./ -name "*.xml" -exec chmod a-x '{}' \;
find ./ -name "*.txt" -exec chmod a-x '{}' \;
find ./ -name "*.html" -exec chmod a-x '{}' \;
find ./ -name "*.js" -exec chmod a-x '{}' \;
find ./ -name "*.pl" -exec chmod a+x '{}' \;
find ./ -name "*.sh" -exec chmod a+x '{}' \;
chmod a+x contrib/util/installScripts/cvsDemoMisc/refresh
chmod a+x contrib/util/installScripts/cvsDemoInstall
chmod a+x contrib/util/installScripts/cvsDemoMisc/StartupDeveloperAppliance2
chmod a+x gacl/soap/clients/python_client.py
# Current directory. Why isn't the find command working on these?
chmod a-x *.php *.js *.html *.xml
chmod a-x admin.php

sed -i "s:/opt/local/bin/perl:/usr/bin/perl:" contrib/util/undelete_from_log/convert_logcomments.pl



%build
# Nothing

%install

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/
for i in "accounting" "ccr" "contrib" "controllers" "custom" "gacl" "images" \
"includes" "interface" "library" "modules" "phpmyadmin" "sites" \
"sql" "templates" "Tests" "Documentation" ; do 
    cp -a "$i" $RPM_BUILD_ROOT%{_datadir}/%{name}/"$i"
    install -p *.php *.html *.xml *.js -t $RPM_BUILD_ROOT%{_datadir}/%{name}/
done

%files
%doc INSTALL README license.txt
%{_datadir}/%{name}/

%changelog
* Tue Aug 16 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.0.0-2
- Remove bundled software

* Sun Aug 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 4.0.0-1
- Initial rpm build
