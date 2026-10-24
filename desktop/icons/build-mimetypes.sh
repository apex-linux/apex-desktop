#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Renders TEMPLATE for every icon in TYPES, in its KINDS colour, into OUTDIR/Apex: with its
# label as paths from 33 px up, and without a label at list sizes, as board 28 draws it.

set -euo pipefail

(($# == 4)) || { echo "usage: build-mimetypes.sh OUTDIR TEMPLATE KINDS TYPES" >&2; exit 2; }
out=$1/Apex template=$2 kinds=$3 types=$4

# Inkscape falls back to any sans without a word, which would change every label.
family=$(fc-match -f '%{family}' 'Adwaita Sans:weight=205')
[[ $family == "Adwaita Sans" ]] || {
    echo "build-mimetypes.sh: fc-match gives '$family' for Adwaita Sans ExtraBold (Fedora: adwaita-sans-fonts)" >&2
    exit 1
}

declare -A colour
while read -r kind hex; do
    [[ -n $kind && $kind != \#* ]] && colour[$kind]=$hex
done <"$kinds"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$out/32x32/mimetypes" "$out/32x32@2x/mimetypes" "$out/scalable/mimetypes"
actions=
while read -r name kind label; do
    [[ -n $name && $name != \#* ]] || continue
    [[ -n ${colour[$kind]:-} ]] || { echo "build-mimetypes.sh: $name: no colour for kind '$kind'" >&2; exit 1; }
    sed -e "s/@COLOR@/${colour[$kind]}/" -e '/id="label"/d' "$template" >"$out/32x32/mimetypes/$name.svg"
    cp "$out/32x32/mimetypes/$name.svg" "$out/32x32@2x/mimetypes/$name.svg"
    if [[ $label == - ]]; then
        cp "$out/32x32/mimetypes/$name.svg" "$out/scalable/mimetypes/$name.svg"
    else
        sed -e "s/@COLOR@/${colour[$kind]}/" -e "s/@LABEL@/$label/" "$template" >"$tmp/$name.svg"
        actions+="file-open:$tmp/$name.svg;export-text-to-path;export-plain-svg;"
        actions+="export-filename:$out/scalable/mimetypes/$name.svg;export-do;file-close;"
    fi
done <"$types"
# One Inkscape process for every label: starting it once per icon takes minutes.
[[ -z $actions ]] || inkscape --actions="$actions" >/dev/null 2>"$tmp/inkscape.log" || {
    cat "$tmp/inkscape.log" >&2
    exit 1
}
if grep -l '<text' "$out/scalable/mimetypes/"*.svg; then
    echo "build-mimetypes.sh: the labels above kept their text" >&2
    exit 1
fi
