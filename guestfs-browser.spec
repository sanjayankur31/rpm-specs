Name:           guestfs-browser
Version:        0.1.6
Release:        2%{?dist}
Summary:        Guest filesystem browser

Group:          Applications/Emulators
License:        GPLv2+

URL:            http://people.redhat.com/~rjones/guestfs-browser/
Source0:        http://people.redhat.com/~rjones/guestfs-browser/files/guestfs-browser-%{version}.tar.gz
Source1:        %{name}.desktop

BuildRequires:  hivex-devel >= 1.2.4-3
BuildRequires:  libguestfs-devel >= 1.9.11
BuildRequires:  libvirt-devel
BuildRequires:  ocaml
BuildRequires:  ocaml-bitstring-devel
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-camomile-devel >= 0.8.1, ocaml-camomile-data
BuildRequires:  ocaml-extlib-devel
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-hivex-devel
BuildRequires:  ocaml-lablgtk-devel
BuildRequires:  ocaml-libvirt-devel
BuildRequires:  ocaml-libguestfs-devel
BuildRequires:  ocaml-xml-light-devel
BuildRequires:  /usr/bin/pod2man
BuildRequires:  /usr/bin/pod2html
BuildRequires:  desktop-file-utils

Requires:       libguestfs >= 1.9.11
Requires:       /usr/bin/gnome-open
Requires:       /usr/bin/hivexregedit

# Only needed to build the internal documentation.
#BuildRequires:  ocaml-ocamldoc


%description
The Guest Filesystem Browser lets you browse inside the filesystems of
virtual machines and disk images using a simple graphical interface.

This package delivers some of the features of libguestfs and the
guestfish scripting tool to users who don't want to use the command
line.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE1}
desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop


%files
%doc COPYING HACKING README
%{_bindir}/guestfs-browser
%{_mandir}/man1/guestfs-browser.1*
%{_datadir}/applications/%{name}.desktop


%changelog
* Tue Jul 26 2011 Richard W.M. Jones <rjones@redhat.com> - 0.1.6-2
- Fedora review (https://bugzilla.redhat.com/669911#c8)

* Sat Jan 15 2011 Richard W.M. Jones <rjones@redhat.com> - 0.1.6-1
- Initial RPM release.
