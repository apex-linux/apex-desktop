#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

usage() {
    cat >&2 <<'EOF'
check-theme.sh THEME_DIR [SOURCE_DIR]

Checks an assembled Apex icon theme: index.theme, every SVG and every link. The spec's
%check runs it on the installed theme, make check-data on one built from desktop/icons.
With SOURCE_DIR, the Apex Symbolic sources: each stroke-opacity of NAME.svg must survive
as a fill-opacity or opacity in symbolic/NAME-symbolic.svg.
EOF
    exit 2
}

Q=\"\'

# The distinct values of an opacity property, as attribute or style, normalised by awk.
opacities() {
    { grep -Eo "(^|[^-[:alnum:]])$1[[:space:]]*(=[[:space:]]*[$Q]|:)[[:space:]]*[0-9.]+" "$2" || true; } |
        sed -E 's/.*[^0-9.]//' | awk '{ printf "%g\n", $1 }' | sort -u
}

check_opacity() {
    local src out want have
    for src in "$2"/*.svg; do
        want=$(opacities stroke-opacity "$src")
        [[ -n $want ]] || continue
        out=$1/symbolic/$(basename "$src" .svg)-symbolic.svg
        [[ -f $out ]] || { fail "$out is missing"; continue; }
        have=$(opacities '(fill-)?opacity' "$out")
        [[ -z $(comm -23 <(printf '%s\n' "$want") <(printf '%s\n' "$have")) ]] ||
            fail "$out lost the stroke-opacity of ${src##*/} ($(tr '\n' ' ' <<<"$want"))"
    done
}

fail() {
    printf 'check-theme: %s\n' "$*" >&2
    FAILED=1
}

check_index() {
    local index=$1
    awk -v index_file="$index" '
        function err(m) { printf "check-theme: %s: %s\n", index_file, m > "/dev/stderr"; bad = 1 }
        /^[[:space:]]*(#|$)/ { next }
        /^\[.*\]$/ { group = substr($0, 2, length($0) - 2); groups[group] = 1; if (!first) first = group; next }
        !/=/ { err("not a key=value line: " $0); next }
        {
            key = substr($0, 1, index($0, "=") - 1); value = substr($0, index($0, "=") + 1)
            if (group == "") err("a key before the first group: " key)
            if ((group, key) in kv) err("[" group "] sets " key " twice")
            kv[group, key] = value
        }
        END {
            if (first != "Icon Theme") err("the first group is not [Icon Theme]")
            split("Name Comment Directories", required, " ")
            for (i in required) if (!(("Icon Theme", required[i]) in kv)) err("[Icon Theme] has no " required[i])
            # Apex Symbolic is partial: every other symbolic icon comes from Adwaita.
            if (kv["Icon Theme", "Inherits"] != "Adwaita,hicolor") err("Inherits is not Adwaita,hicolor")
            n = split(kv["Icon Theme", "Directories"], dirs, ",")
            for (i = 1; i <= n; i++) {
                d = dirs[i]
                print d
                if (!(d in groups)) { err("no [" d "] group"); continue }
                if (kv[d, "Size"] !~ /^[1-9][0-9]*$/) err("[" d "] Size is not a positive integer")
                type = ((d, "Type") in kv) ? kv[d, "Type"] : "Threshold"
                if (type !~ /^(Fixed|Scalable|Threshold)$/) err("[" d "] Type is " type)
                if (type == "Scalable" && (kv[d, "MinSize"] !~ /^[1-9][0-9]*$/ || kv[d, "MaxSize"] !~ /^[1-9][0-9]*$/))
                    err("[" d "] is Scalable without integer MinSize and MaxSize")
            }
            exit bad
        }
    ' "$index"
}

main() {
    (($# == 1 || $# == 2)) || usage
    local theme=${1%/}
    command -v xmllint >/dev/null 2>&1 || { printf 'check-theme: xmllint not found (Fedora: libxml2)\n' >&2; exit 1; }
    FAILED=0

    [[ -f $theme/index.theme ]] || { printf 'check-theme: %s/index.theme is missing\n' "$theme" >&2; exit 1; }
    local listed
    listed=$(check_index "$theme/index.theme") || FAILED=1

    local dir
    while IFS= read -r dir; do
        grep -Fxq -- "$dir" <<<"$listed" || fail "$dir holds icons but index.theme does not list it"
    done < <(cd "$theme" && find . -mindepth 2 \( -name '*.svg' -o -name '*.png' \) -printf '%h\n' | sed 's|^\./||' | sort -u)

    local link
    while IFS= read -r link; do
        fail "$link: the link is absolute or dangling"
    done < <(find "$theme" -type l \( -lname '/*' -o -xtype l \))

    find "$theme" -name '*.svg' ! -xtype l -print0 | xargs -0 -r -n 500 xmllint --noout --nonet || fail "an SVG does not parse"

    local misplaced
    misplaced=$(cd "$theme" && find . -name '*-symbolic.svg' ! -path './symbolic/*')
    [[ -z $misplaced ]] || fail "symbolic icons outside symbolic/, where they would shadow Adwaita's: $misplaced"

    local stroked
    # GTK and St recolour fills only, so a stroke in a symbolic icon keeps its drawn colour.
    stroked=$(find "$theme" -name '*-symbolic.svg' -print0 |
        xargs -0 -r grep -EoH "(^|[^-[:alnum:]])stroke[[:space:]]*(=[[:space:]]*[$Q][^$Q]*|:[^;$Q]*)" |
        grep -Ev "(=[[:space:]]*[$Q]|:)[[:space:]]*none[[:space:]]*\$" | cut -d: -f1 | sort -u || true)
    [[ -z $stroked ]] || fail "symbolic icons with a stroke: $stroked"
    (($# == 1)) || check_opacity "$theme" "${2%/}"

    ((FAILED == 0)) || exit 1
    printf 'check-theme: %s: %s SVGs\n' "$theme" "$(find "$theme" -name '*.svg' | wc -l)"
}

main "$@"
