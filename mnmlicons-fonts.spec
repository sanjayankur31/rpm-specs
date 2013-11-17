%global fontname mnmlicons
%global fontconf 69-%{fontname}.conf

Name:       %{fontname}-fonts
Version:    1.1
Release:    1%{?dist}
Summary:    Perkins Less Web Framework webfonts

Group:      User Interface/X
License:    MIT
URL:        http://code.google.com/p/perkins-less/
Source0:    http://perkins-less.googlecode.com/files/perkins-%{version}.zip
Source1:    %{name}-fontconfig.conf
BuildArch:  noarch

BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem

%description
Fonts from the deprecated old version of the Perkins Less web framework.


%prep
%setup -qc


%build


%install
install -m 0644 -pD stylesheets/perkins/mnmlicons/mnmliconsv21-webfont.ttf \
    %{buildroot}%{_fontdir}/mnmlicons.ttf

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}


%_font_pkg -f %{fontconf} *.ttf

%doc LICENSE


%changelog
* Wed May 19 2013 Alec Leamas <leamas@nowhere.net> - 1.1-1
* Review remarks: change priority, fix .conf file

* Wed May 08 2013 Alec Leamas <leamas@nowhere.net> - 1.1-1
- Only package ttf font

* Tue Apr 24 2013 Alec Leamas <leamas@nowhere.net> - 1.1-1
- Initial release
