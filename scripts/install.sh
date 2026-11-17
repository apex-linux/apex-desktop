#!/bin/bash
#
# Installs apex-desktop under <destdir>/usr. apex-image depends on this
# contract: nothing is written outside <destdir>/usr. Needs only bash,
# coreutils and python3, which is all the image build stage has.

set -euo pipefail

usage() {
  echo "usage: install.sh <destdir>" >&2
  exit 2
}

main() {
  if [[ $# -ne 1 || -z "$1" ]]; then
    usage
  fi
  local destdir="$1"
  local root
  root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

  install -D -m 0644 "${root}/LICENSE" \
    "${destdir}/usr/share/licenses/apex-desktop/LICENSE"
}

main "$@"
