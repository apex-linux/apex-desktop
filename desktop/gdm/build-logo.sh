#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Renders TEMPLATE, board 12's footer, into OUT with its text as paths: the Apex wordmark
# over "Built on Fedora Linux VERSION · GNOME", centred as the board's flex column centres them.

set -euo pipefail

(($# == 3)) || { echo "usage: build-logo.sh OUT TEMPLATE VERSION" >&2; exit 2; }
out=$1 template=$2 version=$3
[[ $version =~ ^[0-9]+$ ]] || { echo "build-logo.sh: VERSION '$version' is not a Fedora release" >&2; exit 2; }

family=$(fc-match -f '%{family}' 'Adwaita Sans:weight=205')
[[ $family == "Adwaita Sans" ]] || {
    echo "build-logo.sh: fc-match gives '$family' for Adwaita Sans ExtraBold (Fedora: adwaita-sans-fonts)" >&2
    exit 1
}

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# id x y width height, from Inkscape's ink boxes.
query() {
    inkscape --query-all "$1" 2>/dev/null | awk -F, -v id="$2" '$1 == id { print $2 + $4, $4 }'
}

fill() {
    sed -e "s/@WIDTH@/$1/g" -e "s/@WORDMARK_X@/$2/" -e "s/@CENTER@/$3/" -e "s/@VERSION@/$version/" "$template"
}

# CSS centres the row by advances: "Apex"'s, tracking included, is ApexApex's right edge less Apex's.
name=$(grep -o '<text id="name"[^>]*>' "$template")
printf '<svg xmlns="http://www.w3.org/2000/svg">%s\n%s</svg>\n' \
    "${name/id=\"name\"/id=\"one\"}Apex</text>" "${name/id=\"name\"/id=\"two\"}ApexApex</text>" >"$tmp/probe.svg"
read -r one_right _ < <(query "$tmp/probe.svg" one)
read -r two_right _ < <(query "$tmp/probe.svg" two)
row=$(awk -v a="$one_right" -v b="$two_right" 'BEGIN { print 26 + (b - a) }')

fill 400 0 200 >"$tmp/measure.svg"
read -r _ credit_width < <(query "$tmp/measure.svg" credit)
width=$(awk -v r="$row" -v c="$credit_width" 'BEGIN { w = (r > c ? r : c) + 2; print (w == int(w) ? w : int(w) + 1) }')
wordmark_x=$(awk -v w="$width" -v r="$row" 'BEGIN { printf "%.3f", (w - r) / 2 }')

fill "$width" "$wordmark_x" "$(awk -v w="$width" 'BEGIN { print w / 2 }')" >"$tmp/logo.svg"
inkscape "$tmp/logo.svg" --export-text-to-path --export-plain-svg --export-filename="$out" \
    >/dev/null 2>"$tmp/inkscape.log" || { cat "$tmp/inkscape.log" >&2; exit 1; }
if grep -q '<text' "$out"; then
    echo "build-logo.sh: $out kept its text" >&2
    exit 1
fi
