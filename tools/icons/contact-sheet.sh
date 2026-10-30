#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

usage() {
    cat >&2 <<'EOF'
contact-sheet.sh ICONS_DIR OUT_DIR

Draws board 31, every Apex Symbolic glyph, as GTK 4 draws it: symbolic recolouring, at
scale 2, light and dark. GTK needs a display: without DISPLAY or WAYLAND_DISPLAY it runs
its own Xvfb, and stops it when done. ICONS_DIR holds the Apex theme: the RPM
payload's usr/share/icons, or /usr/share/icons. For each scene of tools/icons/boards.txt it
writes OUT_DIR/board-31-symbolic-SCENE-light.png and -dark.png, and removes the sheets an
earlier run left there. The same glyphs and fonts give byte-identical PNGs.

Needs python3 with GTK 4 (Fedora: python3-gobject gtk4 gobject-introspection), Adwaita
Sans (adwaita-sans-fonts), fontconfig, and Xvfb without a display (xorg-x11-server-Xvfb).
PYTHON picks the interpreter (default python3).

Exit status: 0 the sheets are written; 1 a glyph is missing or draws nothing, named on
stderr, and no sheet of its scene is written; 2 usage; 3 a dependency is missing.
EOF
    exit 2
}

need() {
    printf 'contact-sheet.sh: %s not found (Fedora: %s)\n' "$1" "$2" >&2
    exit 3
}

start_xvfb() {
    local fifo
    fifo=$(mktemp -u)
    mkfifo "$fifo"
    Xvfb -displayfd 3 -screen 0 1024x768x24 -nolisten tcp 3>"$fifo" 2>/dev/null &
    XVFB_PID=$!
    trap 'kill "$XVFB_PID" 2>/dev/null' EXIT
    DISPLAY=:$(head -n1 "$fifo")
    rm -f "$fifo"
    [[ $DISPLAY != : ]] || { printf 'contact-sheet.sh: Xvfb did not start\n' >&2; exit 3; }
    export DISPLAY
}

main() {
    (($# == 2)) || usage
    local icons=$1 out=$2 here python=${PYTHON:-python3}
    here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
    [[ -f $icons/Apex/index.theme ]] || { printf 'contact-sheet.sh: %s holds no Apex theme\n' "$icons" >&2; exit 2; }

    command -v "$python" >/dev/null || need "$python" python3
    "$python" -c 'import gi; gi.require_version("Gtk", "4.0"); from gi.repository import Gtk' 2>/dev/null ||
        need "GTK 4 for Python" "python3-gobject gtk4 gobject-introspection"
    command -v fc-match >/dev/null || need fc-match fontconfig
    [[ $(fc-match -f '%{family[0]}' 'Adwaita Sans') == 'Adwaita Sans' ]] || need "Adwaita Sans" adwaita-sans-fonts
    if [[ -z ${DISPLAY:-}${WAYLAND_DISPLAY:-} ]]; then
        command -v Xvfb >/dev/null || need Xvfb xorg-x11-server-Xvfb
        start_xvfb
    fi

    mkdir -p "$out"
    rm -f "$out"/board-31-symbolic-*.png
    "$python" -I "$here/contact-sheet.py" "$icons" "$out" "$here/boards.txt"
}

main "$@"
