%global fontname anka-coder
%global fontconf 65-%{fontname}


%global common_desc \
The Anka/Coder family is a mono spaced, courier-width (60% of height; em size \
2048x1229) font that contains characters from 437, 866, 1251, 1252 and some \
other code pages and can be used for source code, terminal windows etc. \
There are 3 font sets (regular. italic, bold, bold-italic each): 1. \
Anka/Coder (em size 2048x1229) 2. Anka/Coder Condensed (condensed by \
12.5%; em size 2048x1075) 3. Anka/Coder Narrow (condensed by 25%; em \
size 2048x922)

Name:           %{fontname}-fonts
Version:        1.100
Release:        1%{?dist}
Summary:        A mono spaced, courier-width font

License:        OFL
URL:            http://code.google.com/p/anka-coder-fonts/

# Generated from an hg clone since sfd sources were available
# hg clone https://code.google.com/p/anka-coder-fonts/
# tar -cvzf anka-coder-fonts-20130409-hg.tar.gz --exclude="\.hg" anka-coder-fonts/
Source0:        anka-coder-fonts-20130409-hg.tar.gz
Source1:        %{name}-norm.conf
Source2:        %{name}-condensed.conf
Source3:        %{name}-narrow.conf

BuildArch:      noarch
BuildRequires:  fontpackages-devel
BuildRequires:  fontforge
Requires:       fontpackages-filesystem

%description
%common_desc

%package common
Summary:        Common files of %{name}
Requires:       fontpackages-filesystem

%description common
%common_desc

This package consists of files used by other %{name} packages.


%package -n %{fontname}-norm-fonts
Summary:        Normal version of %{name}
Requires:       %{name}-common = %{version}-%{release}

%description -n %{fontname}-norm-fonts
%common_desc

"Anka/Coder Norm" simply supplements the family. 


%_font_pkg -n norm -f %{fontconf}-norm.conf AnkaCoder-*.ttf
%doc AnkaCoder-{b,bi,r,i}-sample.pdf

# Repeat for every font family ➅
%package -n %{fontname}-condensed-fonts
Summary:        Condensed version of %{name}
Requires:       %{name}-common = %{version}-%{release}

%description -n %{fontname}-condensed-fonts
%common_desc

"Anka/Coder Condensed" can be used for both printing and screen 
viewing of source code, also as for displaying terminal windows.


%_font_pkg -n condensed -f %{fontconf}-condensed.conf AnkaCoder-C87*.ttf
%doc AnkaCoder-C87-{b,bi,r,i}-sample.pdf

%package -n %{fontname}-narrow-fonts
Summary:        Narrow version of %{name}
Requires:       %{name}-common = %{version}-%{release}

%description -n %{fontname}-narrow-fonts
%common_desc

"Anka/Coder Narrow" was developed for printing of source code; it \
is too tight for screen resolution.

%_font_pkg -n narrow -f %{fontconf}-narrow.conf AnkaCoder-C75*.ttf
%doc AnkaCoder-C75-{b,bi,r,i}-sample.pdf


%prep
%setup -q -n %{name}

%build
for family in "AnkaCoder" "AnkaCoder Condensed" "AnkaCoder Narrow"
do
pushd "$family"
fontforge -lang=ff -script "-" *.sfd <<EOF
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
mv *.ttf ../ -v
mv *.pdf ../ -v
popd
done

sed -i 's/\r//' AnkaCoder/OFL.txt

%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}

install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-norm.conf

install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-condensed.conf

install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-narrow.conf

for fconf in %{fontconf}-norm.conf \
             %{fontconf}-condensed.conf \
             %{fontconf}-narrow.conf ; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done


%clean
rm -fr %{buildroot}


%files common
%defattr(0644,root,root,0755)
%doc AnkaCoder/OFL.txt


%changelog
* Tue Apr 09 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.100-1
- Initial rpmbuild

