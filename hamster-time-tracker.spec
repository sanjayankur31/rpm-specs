Name:        hamster-time-tracker
Version:    1.03.3
Release:    1%{?dist}
Summary:    The Linux time tracker

License:    GPLv3+
URL:        http://projecthamster.wordpress.com/
# wget --content-disposition https://github.com/projecthamster/hamster/archive/%{name}-%{version}.tar.gz
Source0:    hamster-%{name}-%{version}.tar.gz
Source1:    %{name}.appdata.xml

# Move service files to bindir rather than libdir
# Stop gschema building etc.
# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#GConf
Patch0:     %{name}-1.03.3-file-locations.patch

# Correct service files to point to BINDIR rather than LIBDIR
Patch1:     %{name}-1.03.3-service-dbus1.patch
Patch2:     %{name}-1.03.3-service-dbus2.patch

BuildArch:  noarch
BuildRequires:    desktop-file-utils
BuildRequires:    gettext intltool
BuildRequires:    glib2-devel dbus-glib
BuildRequires:    docbook-utils gnome-doc-utils libxslt
Requires:         dbus
Requires:         hicolor-icon-theme
Requires:         bash-completion

BuildRequires: GConf2
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2


%description
Project Hamster is time tracking for individuals. It helps you to keep track on
how much time you have spent during the day on activities you choose to track. 

Whenever you change from doing one task to other, you change your current
activity in Hamster. After a while you can see how many hours you have spent on
what. Maybe print it out, or export to some suitable format, if time reporting
is a request of your employee. 

%prep
%setup -q -n hamster-%{name}-%{version}
%patch0 
%patch1 
%patch2 

# remove shebang
sed -ibackup '1d' src/hamster/today.py

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LINKFLAGS="-Wl,-z,relro"

./waf configure -vv --prefix=%{_prefix} --datadir=%{_datadir} 
./waf build -vv %{?_smp_mflags}


%install
./waf install --destdir=%{buildroot}

mkdir -p %{buildroot}/%{_datadir}/appdata/
cp %{SOURCE1} %{buildroot}/%{_datadir}/appdata/  -v

%find_lang %{name} --with-gnome

desktop-file-validate %{buildroot}/%{_datadir}/applications/hamster*desktop

%pre
%gconf_schema_prepare %{name}
%gconf_schema_obsolete %{name}

%post
%gconf_schema_upgrade %{name}
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%preun
%gconf_schema_remove %{name}

%files -f %{name}.lang
%doc AUTHORS COPYING MAINTAINERS NEWS 
%{_bindir}/hamster*
%{python_sitelib}/hamster
%{_datadir}/%{name}/
%{_datadir}/dbus-1/services/*hamster*.service
%{_sysconfdir}/bash_completion.d/hamster.bash
%{_sysconfdir}/gconf/schemas/hamster-time-tracker.schemas
%{_datadir}/applications/hamster*desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/appdata/%{name}.appdata.xml



%changelog
* Sat Nov 30 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-1
- Initial rpm build

