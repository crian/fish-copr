# Fish Shell COPR Builder

Automated Fedora COPR source builds for the **fish shell** with vendored Rust crates.

## Repository Structure

- `fish.spec` — RPM spec file
- `scripts/make-vendor.sh` — Cargo vendor bundling script
- `.copr/Makefile` — COPR "Make SRPM" config
- `.github/workflows/update-fish.yml` — Daily update & release automation

## Installation

```bash
sudo dnf copr enable YOUR_USER/fish
sudo dnf install fish
fish --version
