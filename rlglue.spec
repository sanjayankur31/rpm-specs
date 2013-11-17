Name:           rlglue
Version:        3.04
Release:        1%{?dist}
Summary:        Reinforcement Learning Glue

License:        ASL 2.0
URL:            http://glue.rl-community.org/wiki/Main_Page
Source0:        http://rl-glue-ext.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  chrpath
#Requires:       

%description
RL-Glue (Reinforcement Learning Glue) provides a standard interface that allows
you to connect reinforcement learning agents, environments, and experiment
programs together, even if they are written in different languages. 


%package devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Development files for %{name}


%description devel
RL-Glue (Reinforcement Learning Glue) provides a standard interface that allows
you to connect reinforcement learning agents, environments, and experiment
programs together, even if they are written in different languages. 




%package doc
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Summary:        Documentation for %{name}

%description doc
RL-Glue (Reinforcement Learning Glue) provides a standard interface that allows
you to connect reinforcement learning agents, environments, and experiment
programs together, even if they are written in different languages. 


%prep
%setup -q
# Remove script. Docs already built
rm -fv docs/makeDocs.bash
rm -fv docs/html/images.idx


%build
%configure --disable-rpath --with-gnu-ld --with-pic --enable-static=no
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}



%install
rm -rf $RPM_BUILD_ROOT
%make_install

find $RPM_BUILD_ROOT/%{_libdir}/ -name "*.la" -exec rm -fv '{}' \;
find $RPM_BUILD_ROOT/%{_libdir}/ -name "*.a" -exec rm -fv '{}' \;

chrpath --delete $RPM_BUILD_ROOT%{_bindir}/rl_glue
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/librlgluenetdev-0:0:0.so.0.0.0


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc LICENSE-2.0.txt README.txt ChangeLog
%{_bindir}/rl_glue
%{_libdir}/librlglue-3:0:0.so*
%{_libdir}/librlgluenetdev-0:0:0.so*
%{_libdir}/librlutils-3:0:0.so*
%{_mandir}/man1/rl_glue.*


%files devel
%{_includedir}/%{name}/
%{_libdir}/librlglue.so
%{_libdir}/librlgluenetdev.so
%{_libdir}/librlutils.so


%files doc
%doc docs examples


%changelog
* Mon Mar 25 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 3.04-1
- Initial rpmbuild

