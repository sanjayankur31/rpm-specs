Name:           irssi-libnotify
Version:        0.2.0
Release:        2%{?dist}
Summary:        Use libnotify to alert user to irssi messages

License:        GPLv2
URL:            http://code.google.com/p/%{name}/wiki/
# git clone https://code.google.com/p/irssi-libnotify/
# tar -cvzf irssi-libnotify-20120526.tar.gz irssi-libnotify

Source0:        %{name}-20120526.tar.gz

# Slightly modified for Fedora.
Source1:        irssi-libnotify-README.fedora

BuildArch:      noarch
Requires:       irssi
Requires:       libnotify
Requires:       pygobject3
Requires:       perl(base)
Requires:       perl(Irssi)
Requires:       perl(Irssi::Irc)
Requires:       perl(Net::DBus)
Requires:       perl(HTML::Entities)

%description
This script issues notifications on the desktop to let a GUI user know
something is going on in an Irssi session. The following types of messages
produce notifications:

-    private message
-    highlighted public message
-    DCC request 

Please read the irssi-libnotify-README.fedora file provided to learn usage.

%prep
%setup -q -n %{name}

%build
# remove their copy
rm -fv README.txt

%install
install -d $RPM_BUILD_ROOT%{_datadir}/irssi/scripts
install -m 644 -p notify.pl $RPM_BUILD_ROOT%{_datadir}/irssi/scripts/notify.pl

install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

# install py as a text file. Readme tells user what to do.
install -m 644 -p notify-listener.py $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/notify-listener.txt
install -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%{_fixperms} $RPM_BUILD_ROOT/*

%files
%{_datadir}/irssi/scripts/notify.pl
%doc %{_docdir}/%{name}-%{version}

%changelog
* Sat May 26 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.2.0-2
- Updated as per #825166

* Fri May 25 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.2.0-1
- Initial rpm build

