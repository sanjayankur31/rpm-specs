%global scl perl516
%scl_package %scl

%global install_scl 1

Summary: Package that installs %scl
Name: %scl_name
Version: 1
Release: 11%{?dist}
License: GPLv2+
Source1: perl.prov.stack
Source2: perl.req.stack
Source3: perl.attr
Source4: perllib.attr

%if 0%{?install_scl}
Requires: %{scl_prefix}perl
%endif
BuildRequires: scl-utils-build
BuildRequires: iso-codes

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF
%scl_install

perl -pi -e "s/__SCL_NAME__/%{?scl}-perl/" %{SOURCE1}
perl -pi -e "s/__SCL_NAME__/%{?scl}-perl/" %{SOURCE2}

mkdir -p %{buildroot}%{_root_sysconfdir}/rpm/
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config << EOF
%%__perl %%_scl_root/usr/bin/perl
%%__perl_provides /usr/lib/rpm/perl.prov.stack
%%__perl_requires /usr/lib/rpm/perl.req.stack
#%%%perl_bootstrap 1
EOF

mkdir -p %{buildroot}/usr/lib/rpm/
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/rpm/perl.prov.stack
install -m 644 %{SOURCE2} %{buildroot}/usr/lib/rpm/perl.req.stack
mkdir -p %{buildroot}/usr/lib/rpm/fileattrs/
install -m 644 %{SOURCE3} %{buildroot}/usr/lib/rpm/fileattrs/perl.attr
install -m 644 %{SOURCE4} %{buildroot}/usr/lib/rpm/fileattrs/perllib.attr

%files

%files runtime
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config
%attr(0755,root,root) /usr/lib/rpm/perl.req.stack
%attr(0755,root,root) /usr/lib/rpm/perl.prov.stack
/usr/lib/rpm/fileattrs/perl.attr
/usr/lib/rpm/fileattrs/perllib.attr

%changelog
* Mon Jun 17 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-11
- Disable macro perl_bootstrap

* Thu May 23 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-10
- Update definition of MANPATH (rhbz#966388)

* Tue May 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-9
- Do not remove /opt/rh/perl516 to prevent removing of any user data

* Mon May 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-8
- Remove the directory /opt/rh/perl516 after uninstalling rpm (rhbz#956215)

* Sun Apr 28 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-7
- Remove extra colon from path definition

* Thu Apr 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-6
- Update setting of environment variable in the script enable

* Wed Feb  6 2013 Jitka Plesnikova <jplesnik@redhat.com> 1-5
- enable macro perl_bootstrap

* Fri Oct  5 2012 Marcela Mašláňová <mmaslano@redhat.com> 1-4
- update to new version of Perl 5.16
- package perl.{prov,req}.stack as executables

* Mon Jul 23 2012 Marcela Mašláňová <mmaslano@redhat.com> 1-3
- change permission from 700 to 644 on perl.{prov,req}

* Tue Mar  6 2012 Marcela Mašláňová <mmaslano@redhat.com> 1.2
- fix dependency on collection *-runtime

* Tue Dec 06 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.1
- initial packaging of meta perl514 package
