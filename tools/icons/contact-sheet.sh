#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

usage() {
    cat >&2 <<'EOF'
contact-sheet.sh ICONS_DIR OUT_DIR

Draws board 31, every Apex Symbolic glyph, as GTK 4 draws it: symbolic recolouring, at
scale 2, light and dark, headless (no display). ICONS_DIR holds the Apex theme: the RPM
payload's usr/share/icons, or /usr/share/icons. For each scene of tools/icons/boards.txt it
writes OUT_DIR/board-31-symbolic-SCENE-light.png and -dark.png, and removes the sheets an
earlier run left there. The same glyphs and fonts give byte-identical PNGs.

Needs python3 with GTK 4 (Fedora: python3-gobject gtk4) and Adwaita Sans
(adwaita-sans-fonts). PYTHON picks the interpreter (default python3).

Exit status: 0 the sheets are written; 1 a glyph is missing or draws nothing, named on
stderr, and no sheet of its scene is written; 2 usage; 3 a dependency is missing.
EOF
    exit 2
}

need() {
    printf 'contact-sheet.sh: %s not found (Fedora: %s)\n' "$1" "$2" >&2
    exit 3
}

main() {
    (($# == 2)) || usage
    local icons=$1 out=$2 here python=${PYTHON:-python3}
    here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
    [[ -f $icons/Apex/index.theme ]] || { printf 'contact-sheet.sh: %s holds no Apex theme\n' "$icons" >&2; exit 2; }

    command -v "$python" >/dev/null || need "$python" python3
    "$python" -c 'import gi; gi.require_version("Gtk", "4.0"); from gi.repository import Gtk' 2>/dev/null ||
        need "GTK 4 for Python" "python3-gobject gtk4"
    command -v fc-match >/dev/null || need fc-match fontconfig
    [[ $(fc-match -f '%{family[0]}' 'Adwaita Sans') == 'Adwaita Sans' ]] || need "Adwaita Sans" adwaita-sans-fonts

    mkdir -p "$out"
    rm -f "$out"/board-31-symbolic-*.png
    "$python" -I "$here/contact-sheet.py" "$icons" "$out" "$here/boards.txt"
}

main "$@"
