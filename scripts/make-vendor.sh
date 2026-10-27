#!/usr/bin/env bash
# Creates fish-<version>-vendor.tar.xz
# from the official fish release tarball.
#
# Usage:     scripts/make-vendor.sh 4.9.3 [output-dir]
# Requires:  cargo (>= 1.85), curl, tar, xz
set -euo pipefail

version="${1:?Usage: $0 <fish-version> [output-dir]}"
outdir="$(realpath "${2:-.}")"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

cd "$work"
curl -fsSL -o src.tar.xz \
  "https://github.com/fish-shell/fish-shell/releases/download/${version}/fish-${version}.tar.xz"
tar -xf src.tar.xz
src="$work/fish-${version}"

mkdir -p "$work/out/.cargo"
cd "$work/out"
{
  cat "$src/.cargo/config.toml"
  echo
  cargo vendor --locked --manifest-path "$src/Cargo.toml"
} > .cargo/config.toml

mkdir -p "$outdir"
tar --sort=name --owner=0 --group=0 --numeric-owner --mtime='@0' \
    -cJf "$outdir/fish-${version}-vendor.tar.xz" vendor .cargo

echo "Done: $outdir/fish-${version}-vendor.tar.xz"
sha256sum "$outdir/fish-${version}-vendor.tar.xz"
