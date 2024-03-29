%global __requires_exclude libcrucible\\.so

Name:           bees
Version:        0.7.2
Release:        1%{?dist}
Summary:        Best-Effort Extent-Same, a btrfs dedup agent

License:        GPLv3
URL:            https://github.com/Zygo/bees
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libbtrfsutil)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  systemd

# https://github.com/Zygo/bees/commit/7933ccb660de3f4b5cd8d2ac2af00d4d4e6acdf3
# Now libcrucible is statically linked to the binary
# so now main package should replace libcrucible
Obsoletes: libcrucible-%{name} <= %{version}-%{release}

%description
bees is a block-oriented userspace deduplication agent designed for large btrfs
filesystems. It is an offline dedupe combined with an incremental data scan
capability to minimize time data spends on disk from write to dedupe.


%prep
%autosetup -p1

sed -i "s|CCFLAGS = .*||" makeflags

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


%changelog
* Fri Oct 14 2022 ElXreno <elxreno@gmail.com> - 0.7.2-1
- Update to version 0.7.2

* Thu Oct 14 2021 ElXreno <elxreno@gmail.com> - 0.7-1
- Update to version 0.7

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
