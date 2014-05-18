%global commit 19796b19b3f1eff5513e2299cf8dfe918f93eb56
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		openstv
Version:	1.7
Release:	1%{?dist}
Summary:	Single transferable vote and instant runoff voting software

Group:		Applications/Productivity
License:	GPLv2+
URL:		https://github.com/OpenTechStrategies/openstv
Source0:	https://github.com/OpenTechStrategies/openstv/archive/%{commit}/openstv-%{commit}.tar.gz
Source1:	openstv
Source2:	openstv-run-election
Source3:	openstv.1
Source4:	openstv-run-election.1
Source5:	openstv.desktop
Patch0:		openstv-1.7-setup-package-data.patch

BuildArch:	noarch
BuildRequires:	desktop-file-utils
BuildRequires:	icoutils
BuildRequires:	python2-devel
Requires:	hicolor-icon-theme
Requires:	wxPython

%description
OpenSTV is an open-source software for implementing the single transferable
vote and other voting methods such as instant runoff voting, Condorcet voting,
and approval voting. OpenSTV is the only open-source software that implements
the single transferable vote exactly as used by governments, including Scotland
and the City of Cambridge, Massachusetts. These methods have been extensively
verified against other software and/or actual election results.

Organizations can use OpenSTV to implement their own elections. First, the
organization must adopt a voting method. Second, the organization must conduct
the vote, and this will most likely be done with paper ballots. Third, the
ballots must be entered into the OpenSTV program. Finally, you can use OpenSTV
to count the votes and determine the winners of the election.

%prep
%setup -q -n %{name}-%{commit}
sed -i 's:#!/usr/bin/env python:# Run openstv instead:' openstv/OpenSTV.py
sed -i 's:#!/usr/bin/env python:# Run openstv-run-election instead:' openstv/runElection.py
%patch0 -p1
icotool --extract --index=7 openstv/Icons/pie.ico
mv pie_7_48x48x32.png %{name}.png


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --root=%{buildroot}
install -Dpm 0755 %{SOURCE1} %{buildroot}%{_bindir}/openstv
install -pm 0755 %{SOURCE2} %{buildroot}%{_bindir}/openstv-run-election
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_mandir}/man1/openstv.1
install -pm 0644 %{SOURCE4} %{buildroot}%{_mandir}/man1/openstv-run-election.1
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE5}
install -Dpm 0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc CHANGELOG.txt README.md
%{_bindir}/%{name}*
%{python2_sitelib}/%{name}/
%{python2_sitelib}/OpenSTV-%{version}-*.egg-info
%{_mandir}/man1/%{name}*.1.gz
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png



%changelog
* Wed Mar 12 2014 David King <amigadave@amigadave.com> - 1.7-1
- Initial import.
