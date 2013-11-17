Name:           gnumed
Version:        0.9.9
Release:        4%{?dist}
Summary:        The %{name} client

License:        GPLv2
URL:            http://wiki.%{name}.de
Source0:        http://www.%{name}.de/downloads/client/0.9/%{name}-client.0.9.9.tgz
Source2:        readme.GNUmed
# Email with upstream's response to License query
Source3:        GNUmedLicense.README

BuildRequires:  desktop-file-utils
BuildRequires:  python-devel

BuildArch:      noarch

# Python requires
Requires:  python
Requires:  python-psycopg2 >= 2.0.10
Requires:  wxPython >= 2.6.3

# Required to use the software properly
Requires:  file
Requires:  java
Requires:  xsane

# Recommended
Requires:  texlive


%description
This is the GNUmed Electronic Medical Record. 
Its purpose is to enable doctors to keep a medically sound record 
on their patients' health. Currently it is not fully featured. The 
features provided are, however, tested, in use, and considered 
stable. This package does NOT yet provide functionality for billing 
and stock keeping.

While the GNUmed team has taken the utmost care to make sure the 
medical records are safe at all times you still need to make sure 
you are taking appropriate steps to backup the medical data to a 
safe place at appropriate intervals. Do test your backup and 
disaster recovery procedures, too !

Protect your data! GNUmed itself comes without any warranty 
whatsoever. You have been warned.

Homepage: http://gnumed.org/

This package contains the wxpython client. 

Authors:
--------
    Sebastian Hilbert <sebastian.hilbert@gmx.net>
    Karsten Hilbert <karsten.hilbert@gmx.net>
    GNUmed team


%package docs
Summary:    Documentation for %{name}
BuildArch:  noarch

%description docs
The documentation for %{name}

%prep
%setup -q -n %{name}-client.%{version}

%build
# Nothing here

%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
cp client/connectors/gm_ctl_client.conf $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/gm_ctl_client.conf
cp client/doc/%{name}.conf.example $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}.conf
cp client/etc/%{name}/%{name}-client.conf.example $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/%{name}-client.conf
cp %{SOURCE2} .
cp %{SOURCE3} .

mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp client/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/bitmaps
cp  -av client/bitmaps/*.png $RPM_BUILD_ROOT%{_datadir}/%{name}/bitmaps/

# Locale files
for i in "fr" "de" "es" "it" "nb" "nl" "pl" "pt_BR" "ru"; do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/"$i"/LC_MESSAGES/
    cp client/po/"$i"-%{name}.mo $RPM_BUILD_ROOT%{_datadir}/locale/"$i"/LC_MESSAGES/%{name}.mo
done
%find_lang %{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp client/bitmaps/%{name}.xpm $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.xpm

mkdir -p -m 755  $RPM_BUILD_ROOT%{python_sitelib}/Gnumed/business
cp -r client/business $RPM_BUILD_ROOT%{python_sitelib}/Gnumed

mkdir -p -m 755 $RPM_BUILD_ROOT%{python_sitelib}/Gnumed/exporters
cp -r client/exporters $RPM_BUILD_ROOT%{python_sitelib}/Gnumed

mkdir -p -m 755 $RPM_BUILD_ROOT/%{python_sitelib}/Gnumed/wxGladeWidgets
# Remove shebang
sed -i "/\/usr\/bin\/env/d" client/wxGladeWidgets/*
cp -r client/wxGladeWidgets  $RPM_BUILD_ROOT%{python_sitelib}/Gnumed

mkdir -p -m 755 $RPM_BUILD_ROOT/%{python_sitelib}/Gnumed/wxpython/gui
cp -r client/wxpython $RPM_BUILD_ROOT%{python_sitelib}/Gnumed
cp -r client/wxpython/gui $RPM_BUILD_ROOT%{python_sitelib}/Gnumed/wxpython

sed -i "/\/usr\/bin\/env/d" client/%{name}.py
cp -r client/%{name}.py $RPM_BUILD_ROOT%{python_sitelib}/Gnumed

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/
cp client/%{name}-client.desktop $RPM_BUILD_ROOT%{_datadir}/applications/
cp client/bitmaps/%{name}logo.png $RPM_BUILD_ROOT%{_datadir}/icons/%{name}logo.png

desktop-file-install \
    --vendor='' \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    $RPM_BUILD_ROOT%{_datadir}/applications/%{name}-client.desktop

# pycommon
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}/Gnumed/pycommon
cp -r client/pycommon $RPM_BUILD_ROOT%{python_sitelib}/Gnumed
cp -r client/__init__.py $RPM_BUILD_ROOT%{python_sitelib}/Gnumed

# Docs
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-client/user-manual
cp -r client/doc/user-manual/* $RPM_BUILD_ROOT%{_docdir}/%{name}-client/user-manual

# Man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
cp client/doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# Extra binaries
install -p -m 0755 external-tools/gm-print_doc -t $RPM_BUILD_ROOT/%{_bindir}/
install -p -m 0755 external-tools/gm-download_data -t $RPM_BUILD_ROOT/%{_bindir}/

# Wrapper 
cat << EOF > gm_ctl_client
#!/bin/bash
python client/connectors/gm_ctl_client.py --conf-file=%{_sysconfdir}/%{name}/gm_ctl_client.conf
EOF
install -p -m 0755 gm_ctl_client -t $RPM_BUILD_ROOT/%{_bindir}/

%files -f %{name}.lang
%doc readme.GNUmed client/CHANGELOG client/GnuPublicLicense.txt GNUmedLicense.README
%{_bindir}/%{name}
%{_bindir}/gm-print_doc
%{_bindir}/gm_ctl_client
%{_bindir}/gm-download_data
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_datadir}/%{name}/
%{_datadir}/pixmaps/gnumed.xpm
%{_datadir}/icons/%{name}logo.png
%{_datadir}/applications/%{name}-client.desktop
%{python_sitelib}/Gnumed/
%{_mandir}/man1/gm_ctl_client.1*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/gm-print_doc.1*

%files docs
%{_docdir}/%{name}-client/user-manual

%changelog
* Mon Aug 15 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.9-4
- Improve the Requires
- Mailed upstream requesting update of the FSF address
- Added a wrapper
- Added more binaries. Refer for file list:
- http://packages.debian.org/sid/all/gnumed-client/filelist

* Sat Aug 13 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.9-3
- Include upstream's email clarifying the license
- Added a for loop to handle locale files

* Tue Aug 09 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.9-2
- Remove doc dependency
- Put man pages in correct sub packages
- Merge subpackages, modularity isn't really required here, let docs be.
- Correct license

* Fri Aug 07 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.9.9-1
- Initial rpmbuild
- Based on Paul Grinberg's spec for the rpm on the official website.
