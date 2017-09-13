%global snapshot .svn20170913.r313153
%global srcname lit

%if 0%{?fedora}
%global with_python3 1
%endif

# FIXME: Work around for rhel not having py2_build/py2_install macro.
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}}

Name: python-%{srcname}
Version: 0.6.0dev
Release: 1%{?snapshot}%{?dist}
BuildArch: noarch

License: NCSA
Group: Development/Languages
Summary: Tool for executing llvm test suites
URL: https://pypi.python.org/pypi/lit
# svn checkout http://llvm.org/svn/llvm-project/llvm/trunk/utils/lit
# cd lit
# python setup.py sdist --formats=gztar
Source0: lit-%{version}.tar.gz

BuildRequires: python2-devel
BuildRequires: python-setuptools
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif

%description
lit is a tool used by the LLVM project for executing its test suites.

%package -n python2-lit
Summary: LLVM lit test runner for Python 2
Group: Development/Languages

%if 0%{?with_python3}
%package -n python3-lit
Summary: LLVM lit test runner for Python 3
Group: Development/Languages
%endif

%description -n python2-lit
lit is a tool used by the LLVM project for executing its test suites.

%if 0%{?with_python3}
%description -n python3-lit
lit is a tool used by the LLVM project for executing its test suites.
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Strip out #!/usr/bin/env python
sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{python2_sitelib}/%{srcname}/*.py
%if 0%{?with_python3}
sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{python3_sitelib}/%{srcname}/*.py
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
# FIXME: Tests fail with python3
#{__python3} setup.py test
%endif

%clean
rm -rf %{buildroot}

%files -n python2-%{srcname}
%doc README.txt
%{python2_sitelib}/*
%if %{undefined with_python3}
%{_bindir}/lit
%endif

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.txt
%{python3_sitelib}/*
%{_bindir}/lit
%endif

%changelog
* Wed Sep 13 2017 Jajauma's Packages <jajauma@yandex.ru> - 0.6.0dev-1.svn20170913.r313153
- Update to latest svn snapshot

* Tue Aug 22 2017 Jajauma's Packages <jajauma@yandex.ru> - 0.5.0-3
- Skip python3 on RHEL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 09 2017 Tom Stellard <tstellar@redhat.com> - 0.5.0-1
- Initial version
