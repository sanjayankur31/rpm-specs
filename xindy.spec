Name:           xindy
Version:        2.5.1
Release:        1%{?dist}
Summary:        Index generator for structured documents like LaTeX or SGML
License:        GPLv2
Url:            http://xindy.sf.net/

Source:         http://mirrors.ctan.org/indexing/xindy/base/xindy-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  clisp
BuildRequires:  flex-devel
BuildRequires:  texlive-latex-bin-bin
BuildRequires:  xz
BuildRequires:  texlive-ec
BuildRequires:  texlive-cm
BuildRequires:  texlive-cyrillic
Requires:       texlive-latex
Requires:       texlive-a4wide
Requires:       texlive-greek-fontenc
Requires:       texlive-cyrillic
Requires:       texlive-cbfonts
Requires:       texlive-babel-greek
Requires:       texlive-lh
Requires:       clisp


%description
xindy is an index processor that can be used to generate book-like
indexes for arbitrary document-preparation systems. This includes
systems such as TeX and LaTeX, the roff-family, SGML/XML-based
systems (e.g. HTML) that process some kind of text and generate
indexing information. The kernel system is not fixed to any specific
system, but can be configured to work together with such systems.

In comparison to other index processors xindy has several powerful
features that make it an ideal framework for describing and
generating complex indices, addressing especially international
indexing.


%prep
%autosetup

%build
%configure
# parallel make doesn't work---LaTeX no like it!
make

%install
%make_install

%files
%{_bindir}/tex2xindy
%{_bindir}/texindy
%{_bindir}/xindy
%{_libdir}/%{name}
%{_mandir}/man1/*xindy*


%changelog
* Wed May 29 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.5.1-1
- Take over from Attila's dead review

* Mon Oct 26 2015 Attila Zsolt Sajo <sajozsattila@gmail.com> - 2.5.1-1
- Initial package
