Name:		fpaste
Version:	0.3.7.2
Release:	1%{?dist}
Summary:	A simple tool for pasting info onto sticky notes instances
BuildArch:	noarch
Group:		Applications/Internet
License:	GPLv3+
URL:		https://fedorahosted.org/fpaste/
Source0:	https://fedorahosted.org/released/fpaste/fpaste-%{version}.tar.gz

%description
It is often useful to be able to easily paste text to the Fedora
Pastebin at http://paste.fedoraproject.org and this simple script 
will do that and return the resulting URL so that people may 
examine the output. This can hopefully help folks who are for 
some reason stuck without X, working remotely, or any other 
reason they may be unable to paste something into the pastebin

%prep
%setup -q 

%build
#nothing required

%install
mkdir -p %{buildroot}%{_bindir}
make install BINDIR=%{buildroot}%{_bindir} MANDIR=%{buildroot}%{_mandir}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%doc CHANGELOG COPYING README TODO
%{_mandir}/man1/fpaste.1.gz

%changelog
* Tue Apr 15 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.7.2-1
- Update to latest upstream release
- Get rid of all patches. They've been merged upstream.

* Fri Apr 04 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.7.1-12
- Update man page

* Thu Jan 23 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.7.1-11
- Another patch to handle server errors

* Thu Jan 23 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.7.1-10
- new patches
- correct syntax options
- correct expiry options
- remove description option
- better kde/plasma detection
- Correct return code of paste method
- Enable nick and password options

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.7.1-8
- Correct url patch
- Update summary

* Wed Apr 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.7.1-7
- Multiple patchs
- URL shortner
- Private option
- Default private on
- Option to use another pastebin
- Rectified summary

* Fri Mar 01 2013 Athmane Madjoudj <athmane@fedoraproject.org> 0.3.7.1-6
- Add a patch to make private url default and use expire option.

* Fri Feb 01 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.7.1-5
- Update patch to point to fedora fpaste production environment

* Fri Oct 19 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.3.7.1-4
- Patch: remove smolt data
- Patch: point to fedora staging sticky notes server
- THIS UPDATE DOES NOT GO TO STABLE. TESTING ONLY.
- Will go to stable when the fedora sticky notes moves to production

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 06 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.7.1-2
- spec bump for gcc 4.7 rebuild

* Sun Oct 16 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.7.1-1
- update to new upstream release
- drop dependency on xsel (#743311)

* Wed Aug 24 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.7-1
- Update to latest upstream release

* Thu Apr 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.6-1
- Update to new upstream release
- Pastes which exceed the server's size limit now error more gracefully
- stdin and clipboard descriptions now default to showing a small text summary of the form "beginning ... middle ... end". 
- sysinfo improvements

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.5-1
- New maintenance release
- --sysinfo: detect running and installed Desktop Environment(s)
- --sysinfo: Show filesystem type in df -hT output
- --sysinfo: Smolt fixed, GL and other additions. by Francois Cami
- --sysinfo: Optimized: rpm -qa --list --nodigest --nosignature. by Dave Riches

* Mon Aug 24 2009 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.4-1
- New release
- Validate paste size and content as non-binary before sending; user is prompted Y/N to override for huge pastes or binary content.
- Added options --printonly and --confirm to show or ask user before sending
- --sysinfo updated: Added blkid, top CPU hogs, top memory hogs, X errors,h/w virtualization, 64-bit capable, and last few reboot/runlevel changes
- Workaround to read user input from raw_input following sys.stdin EOF
- Guess language syntax from common file extension(s)
- --help usage compacted and grouped
- Check that 'xsel' is installed for clipboard input support; silent fail on output
- Use 'fpaste/x.x.x' User-agent header
- bug fixes
* Fri Aug 21 2009 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.3-2
- Added xsel in requires
* Fri Aug 21 2009 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.3-1
- new package release
- Proper urllib2 error handling
- Catches Ctrl-C while waiting for stdin to show a usage reminder rather than a traceback
- Typos fixed, and more TODO
- Added --sysinfo option to gather and pastebin basic system information
- Added options to read text from (xsel) clipboard and write resultant URL to clipboard
* Thu Aug 13 2009 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.2-2
- Corrected source0 field
* Thu Aug 13 2009 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.2-1
- New tar 
- Man page included in tar
* Wed Aug 12 2009 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.1-2
- Review request begins : #516698
- Removed buildroot declaration and removal from install section in accordance with new guidelines
- Aligned description properly
* Tue Aug 11 2009 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.1-1
- Initial rpm build
