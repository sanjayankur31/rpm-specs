%global    fontname    hiran-perizia
%global    fontconf    60-%{fontname}.conf

Name:        %{fontname}-fonts
Version:    0.1.0
Release:    1%{?dist}
Summary:    English asymmetric font

Group:        User Interface/X
License:    GPLv3+ with exceptions
# alas! returns a 404 : http://hiran.in/fontprojects
URL:        http://hiran.in/blog/thanks-perizia-is-now-a-font
Source0:    http://hiran.in/content/fonts/perizia/src/perizia010.sfd
Source1:    %{name}-fontconfig.conf
Source2:    GPL-3.0.txt

BuildArch:    noarch
BuildRequires:    fontforge,fontpackages-devel
Requires:    fontpackages-filesystem

%description
perizia is an asymmetric English font.

%prep
%setup -c -T
install -m 644 -p %{SOURCE2} .

%build
fontforge -lang=ff -script "-" %{SOURCE0} <<EOF
i = 1 
while ( i < \$argc )
  Open (\$argv[i], 1)
  Generate (\$fontname + ".ttf")
  PrintSetup (5) 
  PrintFont (0, 0, "", \$fontname + "-sample.pdf")
  Close()
  i++ 
endloop
EOF

%install
rm -fr %{buildroot}


install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
%{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}

%_font_pkg -f %{fontconf} *.ttf

%doc *.pdf

%changelog
* Thu May 26 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.0-1
- Corrected fontconfig file
- Corrected name
- Corrected version
- Corrected prep section
- Corrected license
- Corrected files section

* Thu Mar 31 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20081017-2
- Updated spec : Added foundry name and corrected URL
- #457709

* Mon Mar 14 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 20081017-1
- initial rpm build
