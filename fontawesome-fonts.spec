%global fontname fontawesome
%global fontconf 60-%{fontname}.conf

Name:		%{fontname}-fonts
Version:	4.0.3
Release:	0%{?dist}
Summary:	Iconic font set
License:	OFL
URL:		http://fortawesome.io/
Source0:	http://fontawesome.io/assets/font-awesome-4.0.3.zip
Source1:	%{name}-fontconfig.conf
BuildArch:	noarch
BuildRequires:	fontpackages-devel
Requires:	fontpackages-filesystem

%description 
Font Awesome gives you scalable vector icons that can instantly be 
customized — size, color, drop shadow, and anything that can be done with the 
power of CSS.

%package web
Requires:	%{fontname}-fonts = %{version}-%{release}
Summary:	Web files for fontawesome

%description web
Web files for fontawesome.

%prep
%setup -q -n font-awesome-%{version}

%build
# Nothing to do here.

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p fonts/*.ttf fonts/*.otf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
		%{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
		%{buildroot}%{_fontconfig_templatedir}/%{fontconf}

ln -s %{_fontconfig_templatedir}/%{fontconf} \
		%{buildroot}%{_fontconfig_confdir}/%{fontconf}

mkdir -p %{buildroot}%{_datadir}/font-awesome-%{version}/
cp -a css less scss %{buildroot}%{_datadir}/font-awesome-%{version}/

%_font_pkg -f %{fontconf} *.ttf *.otf


%files web
%{_datadir}/font-awesome-%{version}/

%changelog
* Mon Nov 04 2013 Ryan Lerch <ryanlerch@fedoraproject.org> - 4.0.3-0
- initial package based off spot's package
