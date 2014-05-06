%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global module_name taskreport
Name:           python-%{module_name}
Version:        1.2.1
Release:        1%{?dist}
Summary:        Automatic reporting tool for Taskwarrior

License:        GPLv3+
URL:            https://pypi.python.org/pypi/%{module_name}/%{version}
Source0:        https://pypi.python.org/packages/source/t/%{module_name}/%{module_name}-%{version}.tar.gz

# Stop setup.py from installing docs to datadir
# Remove install_requires which distutils doesn't support. I'll add another
# requires anyway.
Patch0:         %{module_name}-%{version}-setup-py.patch

BuildArch:      noarch
BuildRequires:  python2-devel
Requires:       task python-inlinestyler python-jinja2

%description
Taskreport is a simple tool to generate HTML reports from your Taskwarrior task
list and send them by email.

The list of features includes:

- generating an HTML report containing the sections defined in the
  configuration file.
- sending the report to one or more email addresses (using the SMTP credentials
  defined in the configuration file).
- outputting the report to a local file.
- customizing the generated HTML with a template (using the Jinja template
  engine).
- in-lining the CSS inside the HTML so that email clients which do not support
  external CSS can render the report gracefully.


%prep
%setup -q -n %{module_name}-%{version}
%patch0 -p0


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%{_bindir}/%{module_name}
%doc data/* CHANGES.txt LICENSE.txt README.txt
%{python2_sitelib}/%{module_name}-%{version}-py?.?.egg-info


%changelog
* Tue May 06 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.2.1-1
- Corrected python directory macros
- Corrected requires to python-jinna2
- Initial rpm build
