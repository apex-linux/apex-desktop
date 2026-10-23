#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

# Inkscape offsets strokes to a fixed tolerance in user units: coarse on a 16-unit canvas.
readonly SCALE=100

usage() {
    cat >&2 <<'EOF'
fill-strokes.sh SOURCE.svg OUT.svg

Turns the strokes of an Apex Symbolic glyph, drawn on a 16 px viewBox, into filled paths
with Inkscape, which GTK and St can recolour. The spec's %build and make check-data run it.
EOF
    exit 2
}

main() {
    (($# == 2)) || usage
    local src=$1 out=$2
    grep -q 'viewBox="0 0 16 16"' "$src" || { printf 'fill-strokes: %s has no viewBox="0 0 16 16"\n' "$src" >&2; exit 1; }

    local tmp
    tmp=$(mktemp -d)
    # shellcheck disable=SC2064 # expand now: $tmp is local and gone when EXIT fires.
    trap "rm -rf '$tmp'" EXIT

    awk -v k="$SCALE" '{ s = s $0 "\n" } END {
        i = index(s, "<svg"); j = i + index(substr(s, i), ">")
        body = substr(s, j); e = 0
        for (p = index(body, "</svg>"); p; p = index(substr(body, e + 1), "</svg>")) e += p
        printf "%s<g transform=\"scale(%s)\">%s</g>%s", substr(s, 1, j - 1), k, substr(body, 1, e - 1), substr(body, e)
    }' "$src" >"$tmp/in.svg"

    # Each ungroup moves a group's transform and stroke onto its children: the scale, then two levels of the glyph's own groups.
    inkscape --actions="select-all:all;selection-ungroup;select-all:all;selection-ungroup;select-all:all;selection-ungroup;select-all:all;object-stroke-to-path;export-plain-svg;export-filename:$tmp/out.svg;export-do" \
        "$tmp/in.svg"

    sed "s/viewBox=\"0 0 16 16\"/viewBox=\"0 0 $((16 * SCALE)) $((16 * SCALE))\"/" "$tmp/out.svg" >"$tmp/scaled.svg"
    grep -q "viewBox=\"0 0 $((16 * SCALE)) $((16 * SCALE))\"" "$tmp/scaled.svg" ||
        { printf 'fill-strokes: Inkscape changed the viewBox of %s\n' "$src" >&2; exit 1; }
    mv "$tmp/scaled.svg" "$out"
}

main "$@"
