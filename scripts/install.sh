#!/bin/bash
#
# Installs apex-desktop under <destdir>/usr. apex-image depends on this
# contract: nothing is written outside <destdir>/usr. Needs only bash,
# coreutils, python3 and glib-compile-schemas, which the image build stage
# has.

set -euo pipefail

readonly UUID="apex@apex-linux.github.io"

usage() {
  echo "usage: install.sh <destdir>" >&2
  exit 2
}

# Runs the token generator with the standard library only.
generate() {
  local root="$1" destdir="$2"
  python3 -I -c '
import sys
sys.path.insert(0, sys.argv[1])
from apex_desktop.entrypoints import generate
sys.exit(generate.main(sys.argv[2:]))
' "${root}/src" "${root}/design" "${destdir}"
}

# Copies the extension's code next to its generated stylesheets and
# compiles its settings schema in place.
install_extension() {
  local root="$1" destdir="$2" file
  local target="${destdir}/usr/share/gnome-shell/extensions/${UUID}"
  for file in "${root}/extension/${UUID}"/*; do
    install -D -m 0644 "${file}" "${target}/${file##*/}"
  done
  glib-compile-schemas --strict "${target}/schemas"
}

main() {
  if [[ $# -ne 1 || -z "$1" ]]; then
    usage
  fi
  local destdir="$1"
  local root
  root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

  generate "${root}" "${destdir}"
  install_extension "${root}" "${destdir}"
  install -D -m 0644 "${root}/LICENSE" \
    "${destdir}/usr/share/licenses/apex-desktop/LICENSE"
}

main "$@"
