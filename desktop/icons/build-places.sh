#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Renders TEMPLATE for every folder in EMBLEMS and every accent in ACCENTS: the blue set
# into OUTDIR/Apex, and each accent's set, with its index.theme, into OUTDIR/Apex-<accent>.

set -euo pipefail

(($# >= 4)) || { echo "usage: build-places.sh OUTDIR TEMPLATE EMBLEMS ACCENTS [NEUTRAL...]" >&2; exit 2; }
src=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
out=$1 template=$2 emblems=$3 accents=$4
shift 4

# Board 27's tab is color-mix(in srgb, accent 68%, #000).
darken() {
    local hex=${1#\#} c v rgb=
    for c in 0 2 4; do
        v=$((16#${hex:c:2} * 68))
        printf -v rgb '%s%02x' "$rgb" $(((v + 50) / 100))
    done
    echo "#$rgb"
}

# The glyph's shapes in white, at the emblem's 1.5 stroke: board 27 draws emblems so.
emblem() {
    sed -n '/<svg[ >]/,/<\/svg>/p' "$src/symbolic/$1.svg" | sed '1d;$d' |
        sed -e 's/currentColor/#ffffff/g' -e 's/stroke-width="1.75"/stroke-width="1.5"/g'
}

folder() {
    local front=$1 glyph=$2 back
    back=$(darken "$front")
    sed -e "s/@FRONT@/$front/" -e "s/@BACK@/$back/" "$template" |
        if [[ $glyph == - ]]; then
            cat
        else
            awk -v emblem="$(emblem "$glyph")" '
                /<g id="emblem"/ { sub(/\/>$/, ">"); print; print emblem; print "  </g>"; next }
                { print }'
        fi
}

places() {
    local theme=$1 front=$2 name glyph
    mkdir -p "$theme/32x32/places" "$theme/32x32@2x/places" "$theme/scalable/places"
    while read -r name glyph; do
        [[ -n $name && $name != \#* ]] || continue
        folder "$front" "$glyph" >"$theme/scalable/places/$name.svg"
        [[ $name == folder ]] && continue
        # List sizes draw the folder without its emblem, as board 28's list view does.
        ln -sf folder.svg "$theme/32x32/places/$name.svg"
        ln -sf folder.svg "$theme/32x32@2x/places/$name.svg"
    done <"$emblems"
    folder "$front" - >"$theme/32x32/places/folder.svg"
    cp "$theme/32x32/places/folder.svg" "$theme/32x32@2x/places/folder.svg"
    # Nautilus's search provider names inode-directory first, so it must not reach Adwaita's.
    for dir in 32x32 32x32@2x scalable; do
        mkdir -p "$theme/$dir/mimetypes"
        cp "$theme/$dir/places/folder.svg" "$theme/$dir/mimetypes/inode-directory.svg"
    done
}

index() {
    cat <<EOF
[Icon Theme]
Name=$1
Comment=$2
Inherits=$3
Directories=32x32/places,32x32@2x/places,scalable/places,32x32/mimetypes,32x32@2x/mimetypes,scalable/mimetypes

[32x32/places]
Context=Places
Size=32
Threshold=8
Type=Threshold

[32x32@2x/places]
Context=Places
Size=32
Scale=2
Threshold=8
Type=Threshold

[scalable/places]
Context=Places
Size=64
MinSize=33
MaxSize=512
Type=Scalable

[32x32/mimetypes]
Context=MimeTypes
Size=32
Threshold=8
Type=Threshold

[32x32@2x/mimetypes]
Context=MimeTypes
Size=32
Scale=2
Threshold=8
Type=Threshold

[scalable/mimetypes]
Context=MimeTypes
Size=64
MinSize=33
MaxSize=512
Type=Scalable
EOF
}

blue=
while read -r accent color; do
    [[ -n $accent && $accent != \#* ]] || continue
    [[ $accent == blue ]] && blue=$color
    places "$out/Apex-$accent" "$color"
    index "Apex ${accent^}" "Apex with $accent folders" Apex >"$out/Apex-$accent/index.theme"
done <"$accents"
[[ -n $blue ]] || { echo "build-places.sh: accents has no blue, the default" >&2; exit 1; }
places "$out/Apex" "$blue"
# A NEUTRAL icon is the same in every theme, so it goes into Apex alone, which they inherit.
for icon in "$@"; do
    for dir in 32x32 32x32@2x scalable; do
        install -m0644 "$icon" "$out/Apex/$dir/places/${icon##*/}"
    done
done
