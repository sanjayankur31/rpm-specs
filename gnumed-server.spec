Name:		gnumed-server
Version:	14.8
Release:	1%{?dist}
Summary:	The GNUmed back end server
Group:		Applications/Productivity	
License:	GPLv2+ or GPLv1
URL:		http://wiki.gnumed.de/
Source0:	http://www.gnumed.de/downloads/server/v14/%{name}.%{version}.tgz
Source1:	http://www.gnu.org/licenses/gpl-1.0.txt	
Patch0:		gnumed-server-correct-dir.patch
BuildArch:  noarch

Requires: python
Requires: python-psycopg2
Requires: mailx
Requires: bzip2
Requires: gnupg2
Requires: openssl
Requires: postgresql
Requires: postgresql-client
Requires: postgresql-filedump
Requires: rsync
Requires: mx

%description
The GNUmed project builds an open source Electronic Medical Record. 
It is developed by a handful of medical doctors and programmers from 
all over the world. It can be useful to anyone documenting the health 
of patients, including but not limited to doctors, physical therapists, 
occupational therapists.

%prep
%setup -q -n gnumed-server.%{version}

#Patch GM_SERVER_DIR path
#-GM_SERVER_DIR="/var/lib/gnumed/server/bootstrap"
#+GM_SERVER_DIR="/usr/lib/gnumed-server/server/bootstrap"
%patch0 -p1

%build

%install
pushd server

#Copy to /sharedstatedir/gnumed-server/
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
cp -p -r bootstrap %{buildroot}%{_sharedstatedir}/%{name}
cp -p -r pycommon %{buildroot}%{_sharedstatedir}/%{name}
cp -p -r sql %{buildroot}%{_sharedstatedir}/%{name}
cp __init__.py %{buildroot}%{_sharedstatedir}/%{name}
echo "%{version}" > %{buildroot}%{_sharedstatedir}/%{name}/version.txt

# silcence bootstrap process by setting interactive to 'no' and set 'gm-dbo' as default password
for conffile in `find %{buildroot}/%{_sharedstatedir}/%{name}/bootstrap -maxdepth 1 -type f -name \*.conf` ; do \
   sed -i 's/^\(interactive[[:space:]]*=[[:space:]]*\)yes/\1no/' "$conffile" ; \
   sed -i 's/^\(password[[:space:]]*=[[:space:]]*\)/\1 gm-dbo/' "$conffile" ; \
done


#copy config files to /etc
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
for conf in `ls etc/gnumed/*.conf.example`; 
    do mv $conf `echo $conf|sed 's/.example//'`; 
done
cp -p -r etc/gnumed/*.conf %{buildroot}%{_sysconfdir}/%{name}

#create .gz files and copy them to mandir
mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_mandir}/man1/

for man in `ls doc/*.*`; \
    do gzip $man; \
done
cp -p doc/*.8.gz %{buildroot}%{_mandir}/man8
cp -p doc/*.1.gz %{buildroot}%{_mandir}/man1


#remove .sh extensions
#copy all scripts to bin dir
mkdir -p %{buildroot}%{_bindir}
rename ".sh" "" *.sh
cp gm-* %{buildroot}%{_bindir}


#copy all docs to default doc dir
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}
cp -p doc/README %{buildroot}%{_defaultdocdir}/%{name}
cp -r -p doc/schema %{buildroot}%{_defaultdocdir}/%{name}
cp -p GnuPublicLicense.txt %{buildroot}%{_defaultdocdir}/%{name}

popd  


%files
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/%{name}/
%{_sharedstatedir}/%{name}/
%{_bindir}/gm-*
%{_mandir}/man8/gm-*
%{_mandir}/man1/gm-*
%config(noreplace) %{_sysconfdir}/%{name}/

%changelog

* Sun May 29 2011 - Susmit Shannigrahi <susmit@fedoraproject.org> - 14.8-1
- New upstream release.
- Correcting spec based on review.

* Sun Feb 27 2011 - Susmit Shannigrahi <susmit@fedoraproject.org> - 14.7-1
- New upstream release
- Added mx as dependency
- Fixing file permission for bindir, mandir

* Sun Feb 27 2011 - Susmit Shannigrahi <susmit@fedoraproject.org> - 14.6-2
- Whole lot of fixes the spec file.

* Wed Jan 12 2011 - Susmit Shannigrahi <susmit@fedoraproject.org> - 14.6-1
- New upstream release.

* Sun Jan 02 2011 - Susmit Shannigrahi <susmit@fedoraproject.org> - 14.5-1
- Initial packaging based on Sebastian Hilbert's unofficial package for F13.
 
