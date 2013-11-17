#
# spec file for package python-scgi
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           python-scgi
Version:        1.14
Release:        1.4
#
#
BuildRequires:  apache2-devel
BuildRequires:  pcre-devel
BuildRequires:  python-devel
%define	apxs	/usr/sbin/apxs2
%define	apache_libexecdir	%(%{apxs} -q LIBEXECDIR)
%define apache_mmn        %(MMN=$(%{apxs} -q LIBEXECDIR)_MMN; test -x $MMN && $MMN)
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Url:            http://www.mems-exchange.org/software/scgi/
# repacked from http://quixote.python.ca/releases/scgi-%{version}.tar.gz
#
Source:         http://python.ca/scgi/releases/scgi-%{version}.tar.gz
Patch0:         python-scgi-newstyle-classes.patch
Patch1:         python-scgi-1.13_documentation_path.patch
Patch2:         python-scgi-apache24.patch
#
Summary:        Python implementation of the SCGI protocol
License:        SUSE-Python-1.6
Group:          Development/Libraries/Python

%description
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

This package contains the python bindings.

%package -n apache2-mod_scgi
Requires:       %{apache_mmn}
Requires:       apache2
#
Summary:        Apache module named mod_scgi that implements the client side of the protocol
Group:          Development/Libraries/Python

%description -n apache2-mod_scgi
The SCGI protocol is a replacement for the Common Gateway Interface
(CGI) protocol. It is a standard for applications to interface with
HTTP servers. It is similar to FastCGI but is designed to be easier to
implement.

This package contains the apache2 module.

To load mod_python into Apache, run the command "a2enmod scgi" as root.

%prep
%setup -n scgi-%{version}
%patch0 -p1
%patch1
%patch2 -p1

%build
CFLAGS="%{optflags}" \
%{__python} setup.py build
pushd apache2
    %{apxs} -c mod_scgi.c
popd

%install
%{__python} setup.py install --prefix=%{_prefix} --root %{buildroot} --record-rpm %{name}.files
%{__install} -D -m 0755 apache2/.libs/mod_scgi.so  %{buildroot}%{apache_libexecdir}/mod_scgi.so

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.files
%defattr(-,root,root)
%doc README.txt cgi2scgi.c CHANGES.txt LICENSE.txt doc/guide.html cgi2scgi.c

%files -n apache2-mod_scgi
%defattr(-,root,root)
%{apache_libexecdir}/mod_scgi.so
%doc README.txt CHANGES.txt LICENSE.txt README.apache2.txt doc/guide.html

%changelog
* Tue Apr 23 2013 dimstar@opensuse.org
- Update to version 1.14:
  + Improve logic for reaping dead child processes.
  + Properly handle interrupted system calls while doing a restart.
  + Drop GIL when passing file descriptors.
  + Add target to build multi-architecture mod_scgi for Mac OS.
- Rebase python-scgi-newstyle-classes.patch.
- Add python-scgi-apache24.patch: Port to Apache 2.4.
* Wed Jan 25 2012 cfarrell@suse.com
- license update: SUSE-Python-1.6
  License is the old Python license (CNRI on Fedora). Use proprietary
  SUSE-prefix until Python-1.6 is accepted upstream at spdx.org
* Wed Apr 29 2009 mrueckert@suse.de
- update to version 1.13:
  - Send Content-Length provided by client, rather than
    r->remaining.
  - Fix error message typo in passfd.c.
  - Remove duplicated text from Apache error messages.
  - Ensure that PATH_INFO is correct even with mod_rewrite
    mod_rewrite can modify r->path_info.  One way this could happen
    is if the path being served by SCGI exists on the filesystem.
    Ensure that PATH_INFO is correct.  Thanks to David Binger for
    point out the fix.
- add python-scgi-1.13_documentation_path.patch:
  fix path to documentation (bnc#482477)
- include guide.html (bnc#482477)
- move cgi2scgi.c to the main package
* Fri Mar  6 2009 maw@pobox.com
- Add python-scgi-newstyle-classes.patch, converting several
  classes from oldstyle to newstyle.
* Fri Apr 13 2007 mrueckert@suse.de
- update to version 1.12:
  - Provide a new overridable method in SCGIHandler, produce(), as
    a more user-friendly alternative to handle_connection().
    Another new alternative is produce_cgilike() which receives the
    request payload on standard input and is expected to write its
    results to standard output.
    (Jeroen T. Vermeulen <jtv@thaiopensource.org>)
  - Define the CMSG_LEN and CMSG_SPACE macros if the platform
    doesn't provide them. (Neil Schemenauer <nas@arctrix.com>)
  - Add guide.html document.
    (Jeroen T. Vermeulen <jtv@thaiopensource.org>)
* Fri Sep 22 2006 poeml@suse.de
- remove libapr-util1-devel from Buildrequires, since the correct
  one comes with apache2-devel
* Wed Aug 30 2006 mrueckert@suse.de
- Update to version 1.11:
  o Allow SCGIServer to use an open socket if provided by the
    calling procedure. The existing serve() method remains the same.
  o Improve portability of the passfd module (solves at least one
    bug on AMD64 machines).
  o Fix a mod_scgi bug that caused a segfault (due to a NULL pointer
    dereference) with certain configurations.
  o Don't send duplicated headers for SCRIPT_NAME and HTTPS.
- removed apache2-mod_scgi-1.9_apache-2.2.0.patch:
  Patch was applied upstream in 1.10 (only change in 1.10)
- install docs with the apache module too
* Sat Mar  4 2006 aj@suse.de
- updated to reflect python changes due to #149809
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan 16 2006 mrueckert@suse.de
- update the patch so it works with apache 2.0 again
* Sun Jan 15 2006 mrueckert@suse.de
- added apache2-mod_scgi-1.9_apache-2.2.0.patch
* Thu Dec 15 2005 mrueckert@suse.de
- Update to version 1.9
  + removed all patches. they are upstream now.
* Mon Nov 21 2005 mrueckert@suse.de
- Initial package of version 1.8
