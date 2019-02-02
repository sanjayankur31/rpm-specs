%global tarname calc

Name:       calcium-calculator
Version:    7.9.4
Release:    1%{?dist}
Summary:    The Calcium Calculator

License:    GPLv3+
URL:        https://web.njit.edu/~matveev/calc.html
Source0:    https://web.njit.edu/~matveev/calc/versions/calc_unix_%{version}.tgz

BuildRequires:  gcc-c++

%description
CalC ("Calcium Calculator") is a free (GNU copyleft) modeling tool for
simulating intracellular calcium diffusion and buffering. CalC solves
continuous reaction-diffusion PDEs describing the entry of calcium into a
volume through point-like channels, and its diffusion, buffering and binding to
calcium receptors. 


%prep
%autosetup -n %{version}


%build
make %{?_smp_mflags}


%install
%make_install


%files
%doc README.txt

%changelog
* Sat Feb 02 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.9.4-1
- Initial package
