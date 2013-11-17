Name:           vcsh
Version:        1.20130909
Release:        2%{?dist}
Summary:        Version Control System for $HOME
Group:          Development/Tools

License:        GPLv2+
URL:            https://github.com/RichiH/vcsh
Source0:        https://github.com/RichiH/vcsh/archive/v%{version}.tar.gz
Patch0:         vcsh.make_install.patch

BuildArch:      noarch
BuildRequires:  rubygem-ronn
Requires:       git


%description
vcsh allows you to have several git repositories, all maintaining their working
trees in $HOME without clobbering each other. That, in turn, means you can have
one repository per config set (zsh, vim, ssh, etc), picking and choosing which
configs you want to use on which machine.


%prep
%setup -q
%patch0


%build
make %{?_smp_mflags} all=manpages


%install
%{make_install} all=manpages docdir=%{_pkgdocdir}


%files
%defattr(-, root, root, -)
%doc LICENSE CONTRIBUTORS changelog
%{_bindir}/%{name}
%{_mandir}/man*/%{name}*
%{_datadir}/zsh/

#%if 0%{?fedora} >= 20
#%{_pkgdocdir}/*
#%endif


%changelog
* Sat Oct 19 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 1.20130909-2
- Added the _docdir in the files listing
- Removed unnecessary `rm -rf %{buildroot}' in clean and install

* Sat Oct 12 2013 Dridi Boukelmoune <dridi.boukelmoune@gmail.com> - 1.20130909-1
- Initial package
