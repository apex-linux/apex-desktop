#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

usage() {
    cat >&2 <<'EOF'
check-caches.sh THEME_DIR...

Fails when a theme's icon-theme.cache is invalid, or differs from one built afresh from
the files the theme holds now: a cache built before a later copy or deletion lists icons
that are not there. The spec's %check and make check-data run it.
EOF
    exit 2
}

main() {
    (($# > 0)) || usage
    local tmp theme failed=0
    tmp=$(mktemp -d)
    # shellcheck disable=SC2064 # expand now: $tmp is local and gone when EXIT fires.
    trap "rm -rf '$tmp'" EXIT
    for theme in "$@"; do
        theme=${theme%/}
        if ! gtk-update-icon-cache --validate "$theme" 2>/dev/null; then
            printf 'check-caches: %s/icon-theme.cache is missing or invalid\n' "$theme" >&2
            failed=1
            continue
        fi
        rm -rf "${tmp:?}/theme" && cp -a "$theme" "$tmp/theme"
        gtk-update-icon-cache --force --quiet "$tmp/theme"
        if ! cmp -s "$theme/icon-theme.cache" "$tmp/theme/icon-theme.cache"; then
            printf 'check-caches: %s/icon-theme.cache does not match the theme: build it after the last change\n' "$theme" >&2
            failed=1
        fi
    done
    ((failed == 0)) || exit 1
    printf 'check-caches: %s icon caches are valid and current\n' "$#"
}

main "$@"
