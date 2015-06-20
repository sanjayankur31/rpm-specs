Name:           processing
Version:        2.2.1
Release:        1%{?dist}
Summary:        The Processing Development Environment

License:        
URL:            www.processing.org
Source0:        

BuildRequires:  ant java-1.7.0-openjdk
Requires:       

%description
Processing is a programming language, development environment, and online community.
Since 2001, Processing has promoted software literacy within the visual arts
and visual literacy within technology. Initially created to serve as a software
sketchbook and to teach computer programming fundamentals within a visual
context, Processing evolved into a development tool for professionals. Today,
there are tens of thousands of students, artists, designers, researchers, and
hobbyists who use Processing for learning, prototyping, and production


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc



%changelog
* Fri Aug 15 2014 Ankur Sinha <sanjay.ankur@gmail.com>
- 
