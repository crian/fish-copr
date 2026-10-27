# Source build of fish with vendored Rust crates (for COPR).

# GitHub repository where the vendor tarball is located as a release asset
%global vendor_repo crian/fish-copr

# Do not build debuginfo package
%global debug_package %{nil}

# Test suite is disabled by default
%bcond_with tests

Name:           fish
Version:        4.9.3
Release:        1%{?dist}
Summary:        Friendly interactive shell
License:        GPL-2.0-only AND LGPL-2.0-or-later AND MIT AND PSF-2.0 AND (Apache-2.0 OR MIT) AND (Unlicense OR MIT) AND WTFPL AND Zlib
URL:            https://fishshell.com
Source0:        https://github.com/fish-shell/fish-shell/releases/download/%{version}/fish-%{version}.tar.xz
Source1:        https://github.com/%{vendor_repo}/releases/download/v%{version}/fish-%{version}-vendor.tar.xz

BuildRequires:  cargo >= 1.85
BuildRequires:  rust >= 1.85
BuildRequires:  rust-srpm-macros
BuildRequires:  cmake >= 3.15
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  pcre2-devel
BuildRequires:  pkgconfig
BuildRequires:  man-db
BuildRequires:  /usr/bin/sphinx-build
%if %{with tests}
BuildRequires:  python3
BuildRequires:  python3-pexpect
BuildRequires:  procps-ng
BuildRequires:  glibc-langpack-en
%endif

Requires:       ncurses-term
Recommends:     man-db
Recommends:     man-pages
Recommends:     groff-base
Recommends:     python3

%description
fish is a fully-equipped command line shell (like bash or zsh) that is
smart and user-friendly. fish supports powerful features like syntax
highlighting, autosuggestions, and tab completions that just work, with
nothing to learn or configure.

%prep
%autosetup -n fish-%{version}
tar -xf %{SOURCE1}
find share -type f -name '*.py' -exec sed -i -e '1{s@^#!.*@#!/usr/bin/python3@}' {} +

%build
export CARGO_NET_OFFLINE=true
export RUSTFLAGS="%{build_rustflags}"

%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DWITH_DOCS=ON \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_INSTALL_DOCDIR=%{_docdir}/fish
%cmake_build

%install
%cmake_install
sed -i 's^/usr/local/^/usr/^g' %{buildroot}%{_datadir}/pkgconfig/fish.pc

%check
%if %{with tests}
export CI=1
%cmake_build --target fish_run_tests
%endif

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/fish" > %{_sysconfdir}/shells
    echo "/bin/fish" >> %{_sysconfdir}/shells
  else
    grep -q "^%{_bindir}/fish$" %{_sysconfdir}/shells || echo "%{_bindir}/fish" >> %{_sysconfdir}/shells
    grep -q "^/bin/fish$" %{_sysconfdir}/shells || echo "/bin/fish" >> %{_sysconfdir}/shells
  fi
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -i '\!^%{_bindir}/fish$!d' %{_sysconfdir}/shells
  sed -i '\!^/bin/fish$!d' %{_sysconfdir}/shells
fi

%files
%license COPYING
%{_bindir}/fish
%{_bindir}/fish_indent
%{_bindir}/fish_key_reader
%{_mandir}/man1/*.1*
%config(noreplace) %{_sysconfdir}/fish/
%{_datadir}/fish/
%{_datadir}/pkgconfig/fish.pc
%{_docdir}/fish/

%changelog
* Tue Oct 27 2026 fish-copr crian <crian84@gmail.com> - 4.9.3-1
- First COPR package: fish 4.9.3 from sources with vendored crates
