%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}
%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"] ')}
Name:           mood-track
Version:        0
Release:        0.0.1RC1%{?dist}
Summary:        Keep track of things that effect mood and behavior

License:        GPLv3+
URL:            http://sourceforge.net/projects/mood-track/
Source0:        http://downloads.sourceforge.net/mood-track/moodtrack-0.0.1RC1.tar.gz

BuildRequires:  rubygem-echoe
Requires:       ruby(abi) = 1.8

%description
MoodTrack keeps track of medications administered, medication 
changes, user defined observations, notes and events that affect 
mood and behavior.

%prep
%setup -q -n moodtrack


%build
Rake %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT


%files
%doc



%changelog
* Fri Jun 24 2011 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.0.1RC1
- initial rpm build
