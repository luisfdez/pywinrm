%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%else
%global with_python3 1
%endif

%global srcname pywinrm

Name:      python-%{srcname}
Version:   0.0.3
Release:   1%{?dist}
Summary:   Python library for Windows Remote Management
Source0:   %{name}-%{version}.tar.gz
BuildArch: noarch

Group:     Development/Languages
License:   MIT license
URL:       http://github.com/diyan/pywinrm/

BuildRequires: python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3

Requires: python-xmltodict
Requires: python-isodate

%description
Python library for Windows Remote Management

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:   Python library for Windows Remote Management

%description -n python3-%{srcname}
Python 3 library for Windows Remote Management
%endif # with_python3

%prep
%setup -q %{name}-%{version} -n %{srcname}-%{version}

rm -rf *.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}


%clean
rm -rf %{buildroot}

%files
%{python2_sitelib}/*

%doc

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc
%{python3_sitelib}/*
%endif

%changelog
