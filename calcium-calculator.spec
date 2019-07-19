%global tarname calc

Name:       calcium-calculator
Version:    7.9.5
Release:    1%{?dist}
Summary:    The Calcium Calculator

License:    GPLv3+
URL:        https://web.njit.edu/~matveev/calc.html
Source0:    https://web.njit.edu/~matveev/calc/versions/calc_unix_%{version}.tgz
Patch0:     0002-Fix-invalid-conversion-from-char-to-char.patch
Patch1:     0003-Include-build-flags.patch
Patch2:     0004-Fix-format-security-issues.patch

BuildRequires:  gcc-c++
BuildRequires:  git-core

%description
CalC ("Calcium Calculator") is a free (GNU copyleft) modeling tool for
simulating intracellular calcium diffusion and buffering. CalC solves
continuous reaction-diffusion PDEs describing the entry of calcium into a
volume through point-like channels, and its diffusion, buffering and binding to
calcium receptors.


%prep
%autosetup -c -n %{name}-%{version} -S git

sed -i 's/\r$//' README.txt
# Remove executable bits
chmod 0644 README.txt

find . -name "*" -type f -exec chmod 0644 '{}' \;
find . -name "*" -type f -exec sed -i 's/\r$//' '{}' \;

%build
%{set_build_flags}
%make_build

%install
install -p -m 755 -D -t $RPM_BUILD_ROOT/%{_bindir} calc

%files
%doc README.txt examples
%{_bindir}/calc

%changelog
* Fri Jul 19 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 7.9.5-1
- Initial package
