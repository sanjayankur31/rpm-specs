%global wikindxdir %{_datadir}/wikindx-

Name:           wikindx
Version:        4.2.1
Release:        1%{?dist}
Summary:        Virtual research environment/On-line bibliography manager

License:        GPLv2+
URL:            http://%{name}.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}%{version}.zip
Source1:        %{name}.conf
Source2:        %{name}-README.fedora

# Point to fedora adodb
Patch0:         %{name}-use-fedora-adodb.patch

Buildarch:      noarch

Requires:       mariadb-server php php-adodb httpd php-mysql

%description
WIKINDX...

* can manage all my bibliographic data allowing me to search through 
    them with an accuracy and speed that cannot be duplicated with 
    index cards.
* enables me to store unlimited quotes, paraphrases and thoughts 
    and to efficiently cross-reference them in a searchable database.
* is free, stable and open source allowing me to cast off the 
    shackles of commercial, licensed software.
* supports non-English multi-byte character sets.
* runs on all major operating systems (*NIX, OsX, Windows).
* runs not only on a desktop computer but also on a web server so 
    I can access my bibliography from any networked point or share my 
    bibliography with my research team.
* allows multiple attachments for each bibliographic resource.
* can export my bibliography in various bibliographic styles 
    (APA, Chicago, IEEE for example).
* allows me to edit or create bibliographic styles through a graphical 
    interface.
* integrates a WYSIWYG word processor with easy importation of quotes etc. 
    so that at long last I can write an article, from draft through to 
    publication with automatic citation formatting, entirely within the 
    one software.
* at the click of a mouse button will reformat my article to another 
    citation style whether that style uses footnotes, endnotes or in-text 
    citation.
* can import and export other bibliographic formats including 
    BibTeX or Endnote format.
* supports multiple users.

WIKINDX is all this and more.

%prep
%setup -q -n %{name}4
%patch0 -p1

# Set config file to file in /etc/
#sed -ibackup 's|\(include_once("\)\(config.php");\)|\1%{_sysconfdir}/%{name}/\2|' core/startup/FACTORY.php

#sed -ibackup 's|// \(public $WIKINDX_ATTACHMENTS_DIR = "\)D:\attachments\(";\)|\1 %{_localstatedir}/lib/%{name}/attachments"\2|' config.php.dist
#sed -ibackup 's|// \(public $WIKINDX_FILES_DIR = "\)D:\files\(";\)|\1 %{_localstatedir}/lib/%{name}/files"\2|' config.php.dist

# Corrent end of line
sed -i 's/\r$//' docs/*.txt
sed -i 's/\r$//' *.txt

# encoding
pushd docs/manual/js/prettify/
    for file in *.js
    do
        iconv -f iso8859-1 -t utf-8 "$file" > "$file"".conv" && mv -f "$file"".conv" "$file"
    done
popd

# spurious executable bits
chmod -x core/tiny_mce/plugins/wikindxSpecialChars/*.{htm,php}
sed -i 's/\r$//' core/tiny_mce/plugins/wikindxSpecialChars/*.htm
sed -i 's/\r$//' core/tiny_mce/plugins/wikindxSpecialChars/*.php
find . -name "*.tpl" -exec sed -i 's/\r$//' '{}' \;


#php-adodb is available in the repos
rm -rvf core/sql/adodb*
rm -rvf core/sql/datadict
rm -rvf core/sql/xsl
rm -rvf core/sql/license.txt
rm -rvf core/sql/*.so
rm -rvf core/sql/toexport.inc.php


%build
# Nothing to build

%install
# Move config to correct location
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mv config.php.dist $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/config.php

# Move worker folders
mkdir -p -m0755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/
mv attachments $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/ -v
mv files $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/ -v
mv styles $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/ -v
mv templates $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/ -v
mv languages $RPM_BUILD_ROOT/%{_localstatedir}/lib/%{name}/ -v

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr * $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
cp -pr %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d

cp -pr %SOURCE2 .


rm -frv $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/docs/
rm -fv $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/*.txt


# Make symlinks
pushd $RPM_BUILD_ROOT/%{_datadir}/%{name}-%{version}/
    ln -sv ../../../%{_localstatedir}/lib/%{name}/attachments/ attachments
    ln -sv ../../../%{_localstatedir}/lib/%{name}/files/ files
    ln -sv ../../../%{_localstatedir}/lib/%{name}/styles/ styles
    ln -sv ../../../%{_localstatedir}/lib/%{name}/templates/ templates
    ln -sv ../../../%{_localstatedir}/lib/%{name}/languages/ languages
    ln -sv ../../../%{_sysconfdir}/%{name}/config.php config.php
popd

%files
%doc READMEFIRST.txt README_PHPDOC.txt CHANGELOG.txt %{name}-README.fedora
%doc docs/*
%attr(0644,root,apache)%config(noreplace) %{_sysconfdir}/%{name}/config.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %{_sysconfdir}/%{name}

%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/attachments/
%{_localstatedir}/lib/%{name}/attachments/ATTACHMENTS
%{_localstatedir}/lib/%{name}/attachments/index.html

%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/files/
%{_localstatedir}/lib/%{name}/files/FILES
%{_localstatedir}/lib/%{name}/files/index.html

# styles
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/CACHE
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography
%{_localstatedir}/lib/%{name}/styles/index.html
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography/apa
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography/britishmedicaljournal
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography/chicago
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography/harvard
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography/ieee
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography/mla
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography/turabian
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/styles/bibliography/wikindx
%attr(0775, root, apache) %{_localstatedir}/lib/%{name}/styles/bibliography/*/*.xml
%{_localstatedir}/lib/%{name}/styles/bibliography/*/README.txt

# ANY NEW ENTRIES INTO BIBLIOGRAPHY MUST BE WRITABLE BY APACHE. READ
# INSTALL.TXT!

# Templates
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/templates
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/templates/default
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/templates/simpleBlue
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/templates/bryophyta
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/templates/verticalOrange
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/templates/enluminure
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/templates/compiled_templates
%attr(0775, root, apache) %{_localstatedir}/lib/%{name}/templates/*/description.txt
%{_localstatedir}/lib/%{name}/templates/*/*.tpl
%{_localstatedir}/lib/%{name}/templates/*/*.js
%{_localstatedir}/lib/%{name}/templates/*/*.css
%{_localstatedir}/lib/%{name}/templates/*/icons
%{_localstatedir}/lib/%{name}/templates/*/images
%{_localstatedir}/lib/%{name}/templates/index.html
%{_localstatedir}/lib/%{name}/templates/enluminure/readme.txt

# languages
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/languages
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/languages/en
%attr(0775, root, apache) %dir %{_localstatedir}/lib/%{name}/languages/reference
%attr(0775, root, apache) %{_localstatedir}/lib/%{name}/languages/reference/*.php
%attr(0775, root, apache) %{_localstatedir}/lib/%{name}/languages/en/*.txt
%attr(0775, root, apache) %{_localstatedir}/lib/%{name}/languages/index.html
%{_localstatedir}/lib/%{name}/languages/en/*.php

# The symlinks!
%{_datadir}/%{name}-%{version}/attachments
%{_datadir}/%{name}-%{version}/files
%{_datadir}/%{name}-%{version}/styles
%{_datadir}/%{name}-%{version}/templates
%{_datadir}/%{name}-%{version}/languages

# The other stuff
%dir %{_datadir}/%{name}-%{version}/
%{_datadir}/%{name}-%{version}/core/  
%{_datadir}/%{name}-%{version}/sqlschema/  
%{_datadir}/%{name}-%{version}/*.php
%{_datadir}/%{name}-%{version}/*.xml

# Own plugins directory, but let other packages place the files in here
%dir %{_datadir}/%{name}-%{version}/plugins/  
%{_datadir}/%{name}-%{version}/plugins/index.html


%changelog
* Mon Sep 30 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.2.1-1
- Update spec

* Tue Mar 12 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 4.1.9-1
- Update to 4.1.9
- Update spec as per guidelines

* Sat Feb 16 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.8.2-1
- Update requires
- Initial rpm build

