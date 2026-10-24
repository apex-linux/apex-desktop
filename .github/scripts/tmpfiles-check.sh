#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Applies desktop/tmpfiles/apex-desktop.conf to an empty root and to one whose global
# Flatpak override already exists, and checks what each ends up with.

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

require systemd-tmpfiles mktemp
conf="$APEX_ROOT/desktop/tmpfiles/apex-desktop.conf"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

fails=0
fail() {
    printf 'FAIL: %s\n' "$*" >&2
    fails=$((fails + 1))
}

override=var/lib/flatpak/overrides/global
expected=$'[Context]\nfilesystems=xdg-config/gtk-4.0:ro;'

mkdir "$tmp/empty"
systemd-tmpfiles --create --root="$tmp/empty" "$conf"
[[ $(<"$tmp/empty/$override") == "$expected" ]] ||
    fail "on an empty /var the override is '$(<"$tmp/empty/$override")'"
[[ $(stat -c %a "$tmp/empty/$override") == 644 ]] || fail "the override is not 0644"

mkdir -p "$tmp/admin/${override%/*}"
printf '[Context]\nsockets=x11;\n' >"$tmp/admin/$override"
systemd-tmpfiles --create --root="$tmp/admin" "$conf"
[[ $(<"$tmp/admin/$override") == $'[Context]\nsockets=x11;' ]] ||
    fail "an existing override was changed to '$(<"$tmp/admin/$override")'"

((fails == 0)) || exit 1
log "tmpfiles-check.sh: the Flatpak override is created when missing and left alone when present"
