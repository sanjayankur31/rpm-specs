Name:           detex
Version:        2.8
Release:        2%{?dist}
Summary:        A program to remove TeX constructs from a text file

Group:          Applications/Text
License:        NCSA
URL:            http://www.cs.purdue.edu/homes/trinkle/detex/
Source0:        http://www.cs.purdue.edu/homes/trinkle/detex/%{name}-%{version}.tar

BuildRequires:  flex flex-static

%description
DeTex is a program to remove TeX constructs from a text file.  It recognizes
the \input command.

This program assumes it is dealing with LaTeX input if it sees the string
"\begin{document}" in the text.  It recognizes the \include and \includeonly
commands.


%prep
%setup -q

# To convert the man page from 1L to 1
sed -i "s/1L/1/" detex.1l
# For proper debuginfo generation
sed -i "/rm -f xxx\.l/d" Makefile
sed -i "s/mv lex\.yy\.c detex\.c/cp lex\.yy\.c detex\.c/" Makefile


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -DNO_MALLOC_DECL"

%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 755 detex $RPM_BUILD_ROOT%{_bindir}/detex
install -Dpm 644 detex.1l $RPM_BUILD_ROOT%{_mandir}/man1/detex.1

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%doc COPYRIGHT README

%changelog
* Thu Apr 28 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.8-2
- Added *comments*

* Sat Apr 16 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.8-2
- removed patch
- renamed man page to .1 instead of .1l
- corrected compilation flags
- Review ticket #682666

* Tue Dec 28 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.8-2
- correct debuginfo error

* Tue Dec 28 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.8-1
- initial RPM build
