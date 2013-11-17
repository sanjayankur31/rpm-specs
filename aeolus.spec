
Summary:       A synthesized pipe organ for ALSA/JACK
Name:          aeolus
Version:       0.8.4
Release:       4%{?dist}
License:       GPLv2+
Group:         Applications/Multimedia
URL:           http://kokkinizita.linuxaudio.org/
Source0:       http://kokkinizita.linuxaudio.org/linuxaudio/downloads/%{name}-%{version}.tar.bz2
# submitted upstream
Source1:       %{name}.desktop
Source2:       %{name}.png
# sample config files
Source3:       http://kokkinizita.linuxaudio.org/linuxaudio/downloads/stops-0.3.0.tar.bz2
Patch0:        %{name}-%{version}-fsf.patch
# add soname to private lib in LD path
Patch1:        %{name}-%{version}-soname.patch

BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: clthreads-devel
BuildRequires: clalsadrv-devel
BuildRequires: clxclient-devel
BuildRequires: libXft-devel
BuildRequires: desktop-file-utils
BuildRequires: readline-devel

%description
%{name} is a synthesized (i.e. not sampled) pipe organ emulator that 
should be good enough to make an organist enjoy playing it. It is a 
software synthesizer optimized for this job, with possibly hundreds 
of controls for each stop, that enable the user to "voice" his 
instrument. Main features of the default instrument: three manuals and 
one pedal, five different temperaments, variable tuning, IDI control 
of course, stereo, surround or Ambisonics output, flexible audio 
controls including a large church reverb.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
sed -i -e 's|-O3|%{optflags} |' -e 's|-ffast-math||' \
       -e 's|$(LDFLAGS)|$(LDFLAGS) -ldl|g' \
       -e 's|/sbin/ldconfig|# /sbin/ldconfig|g' \
    source/Makefile

tar -xvf %{SOURCE3}

%build
cd source
make PREFIX=%{_prefix} %{?_smp_mflags}

%install
cd source
make DESTDIR=%{buildroot} PREFIX=%{_prefix} LIBDIR=%{_lib}\
     install

mkdir %{buildroot}%{_datadir}
mkdir %{buildroot}%{_datadir}/%{name}
mkdir %{buildroot}%{_datadir}/%{name}/stops
cd ../stops-0.3.0
mv * %{buildroot}%{_datadir}/%{name}/stops/
cd ..

/sbin/ldconfig -n %{buildroot}%{_libdir}

# make sure they are readable
find %{buildroot}%{_datadir}/%{name}/stops -type f -exec chmod 644 {} \;

# .desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install  \
   --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE2}  \
    %{buildroot}%{_datadir}/pixmaps/%{name}.png

# set reasonable default startup options:
# jack driver, point to stops, store presets in user home directory
mkdir -p %{buildroot}%{_sysconfdir}
cat << EOF > %{buildroot}%{_sysconfdir}/%{name}.conf
# Aeolus default options
-J -S %{_datadir}/%{name}/stops -u
EOF

%files
%doc AUTHORS COPYING
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_libdir}/%{name}*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Wed Jul 04 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.8.4-4
- Patch FSF address

* Mon Mar 19 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.8.4-3
- Updated license and build requires

* Wed Oct 26 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.8.4-2
- Packaged according to Fedora guidelines

* Wed Oct 26 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.8.4-1
- initial build, copied from CCRMA source


