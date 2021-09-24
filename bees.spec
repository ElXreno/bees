%global __requires_exclude libcrucible\\.so

%global debug_package %{nil}

Name:           bees
Version:        0.6.5
Release:        2%{?dist}
Summary:        Best-Effort Extent-Same, a btrfs dedup agent

License:        GPLv3
URL:            https://github.com/Zygo/bees
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Not really required
BuildRequires:  discount
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libbtrfsutil)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  systemd

Requires:       libcrucible-%{name}%{?_isa}

%description
bees is a block-oriented userspace deduplication agent designed for large btrfs
filesystems. It is an offline dedupe combined with an incremental data scan
capability to minimize time data spends on disk from write to dedupe.

# libcrucible from bees
%package -n     libcrucible-%{name}
Summary:        crucible library for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n libcrucible-%{name}
crucible library for %{name}.


%prep
%autosetup -p1

# Right now default build flags brokes bees, possibly LTO issue
# sed -i "s|CCFLAGS  =.*|CCFLAGS = -I../include -D_FILE_OFFSET_BITS=64 %%{build_cxxflags}|" makeflags

cat <<EOF > localconf
BEES_VERSION=v%{version}
LIBDIR=%{_lib}
EOF


%build
%make_build


%install
%make_install


%post
%systemd_post 'beesd@*.service'


%preun
%systemd_preun 'beesd@*.service'


%postun
%systemd_postun_with_restart 'beesd@*.service'


%files
%license COPYING
%doc README.md
%{_sbindir}/beesd
%{_libdir}/%{name}/%{name}
%{_unitdir}/beesd@.service
%config %{_sysconfdir}/%{name}/beesd.conf.sample

%files -n   libcrucible-%{name}
%{_libdir}/libcrucible.so


%changelog
* Fri Sep 24 2021 ElXreno <elxreno@gmail.com> - 0.6.5-2
- rebuilt

* Sun Mar 21 2021 ElXreno <elxreno@gmail.com> - 0.6.5-1
- Update to version 0.6.5

* Sun Mar 21 2021 ElXreno <elxreno@gmail.com> - 0.6.4-2
- rebuilt

* Sat Feb 13 2021 ElXreno <elxreno@gmail.com> - 0.6.4-1
- Update, little rewrite spec file

* Tue Nov 24 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 2020-10-10-1
- Update version

* Fri Jan 24 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl> - 2019.11.28-2
- rebuilt

* Fri Jan 24 2020 Piotr Rogowski <piotr.rogowski@creativestyle.pl>
- 
