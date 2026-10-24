#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

usage() {
    cat >&2 <<'EOF'
scan.sh PACKAGES >desktop/icons/expected-symbolic.txt

Lists the *-symbolic icon names that the packages named in PACKAGES request and do not ship
themselves. Run it in fedora:45 with those packages installed. It reads every ELF file,
GResource bundle, JavaScript, GtkBuilder, CSS and Python file each package owns, and the
same kinds of file inside each GResource. Names built at run time are not literals: they
are printed to stderr as templates, and the families Apex knows of are in DYNAMIC.
EOF
    exit 2
}

readonly NAME_RE='(?<![A-Za-z0-9._%$/{}@-])[A-Za-z0-9][A-Za-z0-9._-]*-symbolic(?![A-Za-z0-9_])'
# shellcheck disable=SC2016 # a regular expression, not an expansion
readonly TEMPLATE_RE='[A-Za-z0-9._-]*(%[a-z]|\$\{[^}]{1,40}\})[A-Za-z0-9._%${}-]*-symbolic(?![A-Za-z0-9_])'
readonly ICON_FILE_RE='/icons/(.*/)?[^/]+-symbolic(\.symbolic)?\.(svg|png)$'
readonly TEXT_RE='\.(js|ui|css|py|xml)$'

# Names the shell builds from UPower's, NetworkManager's and its own state, by package.
readonly DYNAMIC=(
    "upower battery-level-{0,10,20,30,40,50,60,70,80,90,100}-symbolic"
    "upower battery-level-{0,10,20,30,40,50,60,70,80,90}-charging-symbolic"
    "upower battery-level-100-charged-symbolic battery-missing-symbolic"
    "gnome-shell network-wireless-signal-{none,weak,ok,good,excellent}-symbolic"
    "gnome-shell network-cellular-signal-{none,weak,ok,good,excellent}-symbolic"
)

is_elf() { [[ $(head -c 4 -- "$1" | od -An -c | tr -d ' ') == '177ELF' ]]; }

# The text of FILE, and of each scannable file inside it when it holds GResources.
contents() {
    local f=$1 r
    cat -- "$f"
    if is_elf "$f" || [[ $f == *.gresource ]]; then
        gresource list "$f" 2>/dev/null | grep -E "$TEXT_RE" | while IFS= read -r r; do
            gresource extract "$f" "$r"
        done || true
    fi
}

# "name<TAB>package" for every name PACKAGE requests, and "-name<TAB>package" for every icon it ships.
scan_package() {
    local pkg=$1 f
    while IFS= read -r f; do
        [[ -f $f && ! -L $f ]] || continue
        if [[ $f =~ $ICON_FILE_RE ]]; then
            f=${f##*/}
            printf -- '-%s\t%s\n' "${f%%.*}" "$pkg"
        elif [[ $f =~ $TEXT_RE || $f == *.gresource ]] || is_elf "$f"; then
            if is_elf "$f" || [[ $f == *.gresource ]]; then
                { gresource list "$f" 2>/dev/null || true; } | { grep -E "$ICON_FILE_RE" || true; } |
                    sed "s|.*/||; s|\..*||; s|^|-|; s|\$|\t$pkg|"
            fi
            contents "$f" >"$TMP/contents"
            { grep -aoP "$TEMPLATE_RE" "$TMP/contents" || true; } | sed "s|^|template $pkg: |" >&2
            { grep -aoP "$NAME_RE" "$TMP/contents" || true; } | sed "s|\$|\t$pkg|"
        fi
    done < <(rpm -ql "$pkg")
}

main() {
    (($# == 1)) || usage
    local -a pkgs
    mapfile -t pkgs < <(sed 's/#.*//; /^[[:space:]]*$/d; s/[[:space:]]//g' "$1")
    rpm -q "${pkgs[@]}" >/dev/null || { echo "scan.sh: install the packages of $1 first" >&2; exit 1; }
    TMP=$(mktemp -d)
    trap 'rm -rf "$TMP"' EXIT

    printf '# Symbolic icons the Fedora 45 shell and apps request and do not ship, from tools/icons/scan.sh\n'
    printf '# %s in fedora:45; each @ line names a package version it read.\n' "$1"
    rpm -q --qf '@%{NAME}-%{VERSION}-%{RELEASE}\n' "${pkgs[@]}" | sort
    local p entry
    {
        for p in "${pkgs[@]}"; do scan_package "$p"; done
        for entry in "${DYNAMIC[@]}"; do
            eval "printf '%s\t${entry%% *}\n' ${entry#* }"
        done
    } | awk -F '\t' '
        /^-/ { shipped[substr($1, 2)] = 1; next }
        { if (!(($1, $2) in seen)) { seen[$1, $2] = 1; by[$1] = by[$1] (by[$1] == "" ? "" : " ") $2 } }
        END { for (n in by) if (!(n in shipped)) print n "\t" by[n] }
    ' | LC_ALL=C sort
}

main "$@"
