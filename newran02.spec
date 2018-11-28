# Upstream never made a release
Name:       newran02
Version:    0
Release:    0.1%{?dist}
Summary:    A random number generator library

License:    Public Domain
URL:        http://www.robertnz.net/index.html
Source0:    http://www.robertnz.net/ftp/newran02.tar.gz

BuildRequires:  gcc-c++

%description
This is a C++ library for generating sequences of random numbers from a wide
variety of distributions. It is particularly appropriate for the situation
where one requires sequences of identically distributed random numbers since
the set up time for each type of distribution is relatively long but it is
efficient when generating each new random number. The library includes classes
for generating random numbers from a number of distributions and is easily
extended to be able to generate random numbers from almost any of the standard
distributions.

Comments and bug reports to robert at statsresearch.co.nz [replace at by
you-know-what].

For updates and notes see http://www.robertnz.net.

There are no restrictions on the use of newran except that I take no liability
for any problems that may arise from its use.

I welcome its distribution as part of low cost CD-ROM collections.

You can use it in your commercial projects. However, if you distribute the
source, please make it clear which parts are mine and that they are available
essentially for free over the Internet.


%prep
%autosetup -c -n %{name}


%build
%{set_build_flags}
make %{?_smp_mflags}


%install
%make_install


%files
%doc



%changelog
* Wed Nov 28 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0-0.1
- Initial build
