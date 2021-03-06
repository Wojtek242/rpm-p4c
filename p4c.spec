%global _hardened_build 1

%define build_timestamp %(date +"%Y%m%d")
%define git_commit 01b63cb3d5a78b416c1ca6bc867fe3882929f794
%define git_commit_short %(echo %{git_commit} | head -c 14)

# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
Summary:       Reference compiler for the P4 programming language.
Name:          p4c
Epoch:         1
Version:       0.0.0
Release:       0.1.%{build_timestamp}git%{git_commit_short}%{?dist}
License:       ASL 2.0
URL:           https://github.com/p4lang/p4c
Source0:       https://github.com/p4lang/p4c/archive/%{git_commit}.tar.gz#/p4c-git.tar.gz
Source1:       check-and-update.sh

BuildRequires: bison
BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: flex
BuildRequires: gc-devel
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gmp-devel
BuildRequires: protobuf-devel

Requires:      boost-iostreams
Requires:      gc
Requires:      cpp
Requires:      protobuf

Provides:      p4c(bin) = %{epoch}:%{version}-%{release}
Provides:      p4c-bm2-psa(bin) = %{epoch}:%{version}-%{release}
Provides:      p4c-bm2-ss(bin) = %{epoch}:%{version}-%{release}
Provides:      p4c-dpdk(bin) = %{epoch}:%{version}-%{release}
Provides:      p4c-ebpf(bin) = %{epoch}:%{version}-%{release}
Provides:      p4c-graphs(bin) = %{epoch}:%{version}-%{release}
Provides:      p4c-ubpf(bin) = %{epoch}:%{version}-%{release}
Provides:      p4test(bin) = %{epoch}:%{version}-%{release}

%description
p4c is a reference compiler for the P4 programming language.

%prep
rm -rf %{name}-%{git_commit}
git clone %{url}.git %{name}-%{git_commit}
cd %{name}-%{git_commit}
git checkout %{git_commit}
git submodule update --init --recursive
cd ..
rm -f %{_topdir}/SOURCES/%{name}-git.tar.gz
tar -czf %{_topdir}/SOURCES/%{name}-git.tar.gz %{name}-%{git_commit}

%autosetup -n %{name}-%{git_commit}

%build
%set_build_flags
mkdir -p build
cd build
cmake .. \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DENABLE_BMV2=ON \
      -DENABLE_EBPF=ON \
      -DENABLE_P4C_GRAPHS=ON \
      -DENABLE_P4TEST=ON \
      -DENABLE_DOCS=ON \
      -DENABLE_GC=ON \
      -DENABLE_GTESTS=ON \
      -DENABLE_PROTOBUF_STATIC=OFF
%make_build

%install
cd build
%make_install

%files
%{_bindir}/p4c
%{_bindir}/p4c-bm2-psa
%{_bindir}/p4c-bm2-ss
%{_bindir}/p4c-dpdk
%{_bindir}/p4c-ebpf
%{_bindir}/p4c-graphs
%{_bindir}/p4c-ubpf
%{_bindir}/p4test
%{_datadir}/p4c

%changelog
* Sat Mar 06 2021 Wojciech Kozlowski <wk@wojciechkozlowski.eu> 1:0.0.0-0.1
- Initial spec file
