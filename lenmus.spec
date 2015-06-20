Name:           lenmus
Version:        5.3.1
Release:        1%{?dist}
Summary:        A free program for learning music theory

License:        GPLv3+
URL:            https://launchpad.net/lenmus
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}.tar.gz

BuildRequires:  portmidi-devel wxGTK-devel sqlite-devel freetype-devel cmake
#Requires:       

%description
LenMus Phonascus, "the teacher of music", is a free program to help you
in the study of music theory and ear training.

The LenMus Project is an open project, committed to the principles of
Open Source, free education, and open access to information. It has no comercial
purpose. It is an open workbench for working on all areas related to teaching
music, and music representation and management with computers. It aims at
developing publicly available knowledge, methods and algorithms related to all
these areas and at the same time provides free quality software for music
students, amateurs, and teachers.

Please visit the LenMus website (http://www.lenmus.org) for the latest news
about the project or for further details about releases.
%prep
%setup -q


%build
%cmake .
make %{?_smp_mflags}


%install
%make_install


%files
%doc



%changelog
* Wed Feb 12 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 5.3.1-1
- Initial build

* Wed Feb 12 2014 Ankur Sinha <sanjay.ankur@gmail.com>
- 
