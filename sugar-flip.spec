Name:           sugar-flip
Version:        1
Release:        3%{?dist}
Summary:        Simple strategic game of flipping coins

Group:          Sugar/Activities
License:        GPLv3+ and MIT
URL:            http://wiki.sugarlabs.org/go/Activities/Flip
Source0:        http://download.sugarlabs.org/sources/honey/Flip/Flip-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  python sugar-toolkit python2-devel
Requires:       sugar

%description
Flip is a simple strategic game where you have to flip coins until 
they are all heads up. Each time you win, the challenge gets more 
difficult. You can play flips with your friends over the net. 

%prep
%setup -q -n Flip-%{version}

%build
%{__python} ./setup.py build

%install
%{__python} ./setup.py install --prefix=%{buildroot}/%{_prefix}
rm %{buildroot}%{sugaractivitydir}Flip.activity/setup.py

%files 
%defattr(-,root,root,-)
%doc COPYING NEWS
%{sugaractivitydir}/Flip.activity/

%changelog
* Fri Mar 30 2012 Kalpa Welivitigoda <callkalpa@gmail.com> - 1-3
- removed setup.py

* Fri Mar 30 2012 Kalpa Welivitigoda <callkalpa@gmail.com> - 1-2
- updated license info
- removed gettext
- added python2-devel
- updated license

* Sun Dec 18 2011 Kalpa Welivitigoda <callkalpa@gmail.com> - 1-1
- initial packaging
