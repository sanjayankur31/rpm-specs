Name:           ledgersmb
Version:        1.2.24
Release:        1%{?dist}
Summary:        Financial accounting program

License:        GPLv2+
URL:            http://www.ledgersmb.org/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        001-README.fedora
BuildArch:      noarch

BuildRequires:  perl-devel perl
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(Locale::Maketext::Lexicon), texlive-latex, httpd, postgresql, perl(DBD::Pg)
Requires:  perl(DBI), perl(version), perl(Smart::Comments), perl(MIME::Lite), perl(Class::Std)
Requires:  perl(AppConfig::Std), %{?perl_default_filter}


%description
LedgerSMB is a double-entry accounting system written in perl.
LedgerSMB is a fork of sql-ledger offering better security and data integrity,
and many advanced features.

This package does not work in SELinux restricted mode.


%prep
%setup -q -n %{name}
cp %{SOURCE1} .

find . -name "*.po" -exec chmod a-x '{}' \;
find . -name "*.png" -exec chmod a-x '{}' \;
find . -name "*.pm" -exec chmod a-x '{}' \;
find . -name "*.html" -exec chmod a-x '{}' \;
find . -name "*.tex" -exec chmod a-x '{}' \;
find . -name "*.eps" -exec chmod a-x '{}' \;
find . -name "*.txt" -exec chmod a-x '{}' \;
find . -name "*.css" -exec chmod a-x '{}' \;
find . -name "*.orig" -exec rm -f '{}' \;
chmod a+x utils/notify_short/config.pl utils/cli/ledgersmb_cli.pl \
utils/notify_short/listener.pl upgrade-templates.pl
chmod a-x bin/*.pl


%build
cat << TAK > rpm-ledgersmb-httpd.conf
Alias /ledgersmb/doc/LedgerSMB-manual.pdf %{_docdir}/%{name}-%{version}/LedgerSMB-manual.pdf
<Files %{_docdir}/%{name}-%{version}/LedgerSMB-manual.pdf>
</Files>

TAK

perl -p -e "s,/some/path/to/ledgersmb,%{_datadir}/%{name},g" ledgersmb-httpd.conf >> rpm-ledgersmb-httpd.conf


%install
mkdir -p -m0755 $RPM_BUILD_ROOT%{_datadir}/%{name} # /usr/lib/ledgersmb - readonly code and cgi directory
mkdir -p -m0755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name} # /etc/ledgersmb - configs
mkdir -p -m0755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name} # /var/lib/ledgersmb - data files, modified by cgi
mkdir -p -m0755 $RPM_BUILD_ROOT%{_localstatedir}/spool/%{name} # /var/spool/ledgersmb - spool files, modified by cgi

# the conf, placed in etc, symlinked back in place
mv ledgersmb.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/ledgersmb/ledgersmb.conf
ln -s ../../..%{_sysconfdir}/ledgersmb/ledgersmb.conf \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/ledgersmb.conf

# install relevant parts in data/cgi directory
cp -rp *.pl favicon.ico index.html ledger-smb.eps ledger-smb.gif ledger-smb.png ledger-smb_small.png menu.ini \
  bin LedgerSMB sql utils locale drivers \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/locale/legacy

# css - written to by cgi
mkdir -p -m0755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/css
ln -s ../../..%{_localstatedir}/lib/%{name}/css \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/css
cp -rp css/* \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/css

# templates - written to by cgi
mkdir -p -m0755 $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/templates
ln -s ../../..%{_localstatedir}/lib/%{name}/templates \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/templates
cp -rp templates/* \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/templates

# spool - written to by cgi
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/spool/%{name}
ln -s ../../..%{_localstatedir}/spool/%{name} \
  $RPM_BUILD_ROOT%{_datadir}/%{name}/spool

# apache config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 rpm-ledgersmb-httpd.conf \
  $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/ledgersmb.conf

chmod a-x $RPM_BUILD_ROOT/%{_datadir}/%{name}/sql/*.sql
chmod a-x $RPM_BUILD_ROOT/%{_datadir}/%{name}/sql/legacy/*.sql


%files
%doc doc/{COPYRIGHT,faq.html,LedgerSMB-manual.pdf,README,release_notes} 001-README.fedora
%doc BUGS Changelog CONTRIBUTORS INSTALL LICENSE README.translations TODO UPGRADE
%{_datadir}/%{name}
%attr(-, apache, apache) %config(noreplace) %{_localstatedir}/lib/%{name}
%attr(-, apache, apache) %dir %{_localstatedir}/spool/%{name}
%attr(0755, root, apache) %dir %{_sysconfdir}/%{name}
%attr(0644, root, apache) %config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf



%changelog
* Tue Jul 19 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.2.24-1
- Initial rpm build
- Based on Rakesh Pandit's spec for review ticket 604005
