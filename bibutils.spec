Name:           bibutils
Version:        4.15
Release:        4%{?dist}
Summary:        Bibliography conversion tools
# manpage is GPLv2 though source files only state GPL
License:        GPL+ and GPLv2
URL:            http://sourceforge.net/p/bibutils/home/Bibutils/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}_src.tgz

BuildRequires:  tcsh
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
Patch1:         bibutils-lib-symlink.patch
Patch2:         bibutils-bin-cflags.patch
Patch3:         bibutils-fix-docbook-tag.patch

%description
The bibutils package converts between various bibliography
formats using a common MODS-format XML intermediate.


%package libs
Summary:        Bibutils library
License:        GPL+

%description libs
Bibutils library.


%package devel
Summary:        Development files for bibutils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
License:        GPL+

%description devel
Bibutils development files.

%prep
%setup -q -n %{name}_%{version}
%patch1 -p1 -b .orig
%patch2 -p1 -b .orig
%patch3 -p1 -b .orig


%build
./configure --install-dir %{buildroot}%{_bindir} --install-lib %{buildroot}%{_libdir} --dynamic
export CFLAGS="-I../lib %{optflags}"
make -C lib
make -C bin

xsltproc -o bibutils.1 --nonet %{_datadir}/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl bibutils.dbk


%install
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}
make install

mkdir -p %{buildroot}%{_includedir}/%{name}
cp -p lib/*.h %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_libdir}/pkgconfig 
cp -p lib/%{name}.pc %{buildroot}%{_libdir}/pkgconfig
sed -i -e 's!\\!!g' -e 's!libdir=${prefix}/lib!libdir=%{_libdir}!' -e 's!${includedir}!${includedir}/%{name}!' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
mkdir -p %{buildroot}%{_mandir}/man1
cp -p %{name}.1 %{buildroot}%{_mandir}/man1

for i in $(cd %{buildroot}%{_bindir}; ls *); do
  ln -s bibutils.1 %{buildroot}%{_mandir}/man1/$i.1
done


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc Copying ChangeLog
%{_bindir}/*
%{_mandir}/man1/*.1*


%files libs
%{_libdir}/libbibutils.so.*


%files devel
%{_includedir}/%{name}
%{_libdir}/libbibutils.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Oct  4 2012 Jens Petersen <petersen@redhat.com> - 4.15-4
- tcsh provides csh so no need to patch configure for tcsh
- change license to GPL+ for the code and GPLv2 for the manpage

* Tue Oct  2 2012 Jens Petersen <petersen@redhat.com> - 4.15-3
- improve summary and description (#861922)
- build and install docbook manpage which is GPLv2+ (#861922)
- use _isa (#861922)

* Tue Oct  2 2012 Jens Petersen <petersen@redhat.com> - 4.15-2
- BR tcsh

* Mon Oct  1 2012 Jens Petersen <petersen@redhat.com> - 4.15-1
- initial packaging
