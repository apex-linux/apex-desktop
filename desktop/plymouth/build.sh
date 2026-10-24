#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Lays out both themes in OUTDIR/apex and OUTDIR/apex-twostep: each SVG rendered with
# rsvg-convert, at 1x and @2x for apex and at @2x under two-step's names for apex-twostep.

set -euo pipefail

(($# >= 2)) || { echo "usage: build.sh OUTDIR SVG..." >&2; exit 2; }
src=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
out=$1
shift

# rsvg-convert falls back to any sans without a word, which would change the wordmark.
family=$(fc-match -f '%{family}' 'Adwaita Sans:weight=205')
[[ $family == "Adwaita Sans" ]] || {
    echo "build.sh: fc-match gives '$family' for Adwaita Sans ExtraBold (Fedora: adwaita-sans-fonts)" >&2
    exit 1
}

mkdir -p "$out/apex" "$out/apex-twostep"
install -m0644 "$src/apex/apex.plymouth" "$src/apex/apex.script" "$out/apex/"
for f in "$@"; do
    n=${f##*/}
    n=${n%.svg}
    rsvg-convert --zoom 1 -o "$out/apex/$n.png" "$f"
    rsvg-convert --zoom 2 -o "$out/apex/$n@2x.png" "$f"
done

install -m0644 "$src/apex-twostep/apex-twostep.plymouth" "$out/apex-twostep/"
for pair in watermark:wordmark entry:field bullet:bullet; do
    install -m0644 "$out/apex/${pair#*:}@2x.png" "$out/apex-twostep/${pair%%:*}.png"
done
# two-step fails its passphrase dialog without a lock.png; the Apex field has no lock.
rsvg-convert -o "$out/apex-twostep/lock.png" <<<'<svg xmlns="http://www.w3.org/2000/svg" width="1" height="76"/>'
