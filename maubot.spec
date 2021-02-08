# Created by pyp2rpm-3.3.5
%global pypi_name maubot
%{?python_enable_dependency_generator}

Name:           %{pypi_name}
Version:        0.1.0
Release:        1%{?dist}
Summary:        A plugin-based Matrix bot system

License:        None
URL:            https://github.com/maubot/maubot
Source0:        %{pypi_source}
Source1:        maubot.service

Patch0:         config.patch
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  systemd-rpm-macros

Requires:       systemd

#Manually include the end-to-end dependencies.
Requires:       libolm-python3
Requires:       python3-unpaddedbase64
%py_provides    mautrix-facebook+e2be
Requires:       python3-crypto
%global __requires_exclude ^.*pycryptodome.*$

%description
A plugin-based [Matrix]() bot system written in Python.

%{?python_extras_subpkg:%python_extras_subpkg -n %{name} -i %{python3_sitelib}/*.egg-info postgres}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
A plugin-based [Matrix]() bot system written in Python.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

mkdir -p %{buildroot}%{_datadir}/%{pypi_name}
mv %{buildroot}/usr/alembic.ini %{buildroot}%{_datadir}/%{pypi_name}/
mv %{buildroot}/usr/alembic %{buildroot}%{_datadir}/%{pypi_name}/

mkdir -p %{buildroot}%{_datadir}/%{pypi_name}/plugin
mkdir -p %{buildroot}%{_datadir}/%{pypi_name}/crypto

mkdir -p %{buildroot}%{_sysconfdir}/%{pypi_name}
mv %{buildroot}/usr/example-config.yaml %{buildroot}%{_sysconfdir}/%{pypi_name}/config.yaml

install -p -D -T -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/maubot.service

%post
%systemd_post mautrix-facebook.service

%preun
%systemd_preun mautrix-facebook.service

%postun
%systemd_postun_with_restart mautrix-facebook.service

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%{_datadir}/%{pypi_name}
%dir %{_sysconfdir}/%{pypi_name}
%config(noreplace) %{_sysconfdir}/%{pypi_name}/config.yaml

%{_bindir}/mbc

%{_unitdir}/maubot.service


%changelog
* Sun Feb 07 2021 Alex Manning <git@alex-m.co.uk> - 0.1.0-1
- Initial package.
