#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Runs plymouthd on its X11 renderer in Xvfb, a 2880x1800 screen like the laptop's, at
# DeviceScale 2 and 1, and checks pixels of the frames it saves to OUTDIR.

set -euo pipefail

usage() {
    cat >&2 <<'EOF'
usage: plymouth-preview.sh THEMES OUTDIR

THEMES holds apex/ and apex-twostep/ as build.sh writes them. Root in a throwaway
container only: the themes go to /run/plymouth/themes, where plymouthd looks first.
Needs plymouthd and the X11 renderer (Fedora: plymouth-plugin-script,
plymouth-plugin-two-step, plymouth-devel), Xvfb, xwd, xdotool and netpbm-progs.
EOF
    exit 2
}

(($# == 2)) || usage
themes=$(cd "$1" && pwd)
mkdir -p "$2"
out=$(cd "$2" && pwd)
[[ $EUID -eq 0 && ( -e /.dockerenv || -e /run/.containerenv ) ]] || usage

fails=0
fail() {
    echo "plymouth-preview.sh: FAIL: $*" >&2
    fails=$((fails + 1))
}

# The screen is 2880x1800 device pixels at both scales; design pixel (x, y) is device (2x, 2y).
rgb() {
    pamcut -left "$2" -top "$3" -width 1 -height 1 "$out/$1.ppm" | pamtopnm -plain | tail -n 1 | xargs
}

expect() {
    local frame=$1 x=$2 y=$3 what=$4 test=$5 r g b
    read -r r g b <<<"$(rgb "$frame" "$x" "$y")"
    ((test)) || fail "$frame: ($x, $y) should be $what, is rgb($r, $g, $b)"
}

# The brightest pixel of a box, to see that the art drew there without pinning font rendering.
brightest() {
    pamcut -left "$2" -top "$3" -width "$4" -height "$5" "$out/$1.ppm" | ppmtopgm | pamsumm -max -brief
}

shot() {
    sleep 1
    xwd -root -silent -display "$DISPLAY" | xwdtopnm 2>/dev/null >"$out/$1.ppm"
    pnmtopng "$out/$1.ppm" >"$out/$1.png"
}

run() {
    local theme=$1 scale=$2 mode=$3 tag="$1-scale$2"
    rm -rf /run/plymouth/themes
    mkdir -p /run/plymouth/themes
    cp -r "$themes/$theme" /run/plymouth/themes/
    sed -i 's|/usr/share/plymouth/themes/|/run/plymouth/themes/|' "/run/plymouth/themes/$theme/$theme.plymouth"

    Xvfb :87 -screen 0 2880x1800x24 -nolisten tcp >"$out/$tag-xvfb.log" 2>&1 &
    local xvfb=$!
    export DISPLAY=:87
    for _ in $(seq 50); do xwd -root -silent >/dev/null 2>&1 && break; sleep 0.1; done
    PLYMOUTH_FORCE_SCALE=$scale plymouthd --no-daemon --mode="$mode" --no-boot-log \
        --debug-file="$out/$tag-plymouthd.log" --ignore-serial-consoles --graphical-boot \
        --kernel-command-line="rhgb plymouth.ignore-serial-consoles plymouth.splash=$theme" \
        2>"$out/$tag-stderr.log" &
    local ply=$!
    for _ in $(seq 50); do plymouth --ping && break; sleep 0.1; done
    plymouth show-splash
    if [[ $mode == updates ]]; then
        plymouth system-update --progress=58
    fi
    shot "$tag-splash"
    plymouth ask-for-password --prompt="Please enter passphrase for disk apex-root" >/dev/null &
    shot "$tag-ask"
    xdotool type --delay 30 secret
    shot "$tag-typed"
    xdotool key Return
    wait $!
    plymouth ask-for-password --prompt="Please enter passphrase for disk apex-root" >/dev/null &
    shot "$tag-wrong"
    xdotool type --delay 30 x
    xdotool key Return
    wait $!
    plymouth quit
    wait "$ply" || true
    kill "$xvfb"
    wait "$xvfb" 2>/dev/null || true
    grep -q 'script.*parse error\|Parser error' "$out/$tag-plymouthd.log" && fail "$tag: the script does not parse"
    return 0
}

for scale in 2 1; do
    run apex "$scale" updates
    t="apex-scale$scale"
    expect "$t-splash" 20 20 black 'r + g + b == 0'
    (($(brightest "$t-splash" 1296 816 288 82) > 240)) || fail "$t-splash: no wordmark"
    expect "$t-splash" 1320 981 "the bar's fill" 'r > 240 && g > 240 && b > 240'
    expect "$t-splash" 1580 981 "the bar's track" 'r > 25 && r < 45 && g > 25 && g < 45'
    expect "$t-ask" 1640 1016 "the field" 'r > 38 && r < 54 && g > 38 && g < 54'
    (($(brightest "$t-ask" 1220 1000 300 30) > 120)) || fail "$t-ask: no placeholder"
    (($(brightest "$t-ask" 1240 1082 400 30) > 120)) || fail "$t-ask: no hint"
    expect "$t-typed" 1228 1016 "the first bullet" 'r > 200'
    expect "$t-wrong" 1440 980 "the error ring" 'r > 200 && g < 170 && b < 170'
done

run apex-twostep 2 boot
t=apex-twostep-scale2
expect "$t-splash" 20 20 black 'r + g + b == 0'
(($(brightest "$t-splash" 1296 816 288 82) > 240)) || fail "$t-splash: no wordmark"
(($(brightest "$t-ask" 1190 1000 500 40) > 38)) || fail "$t-ask: no field"

((fails == 0)) || exit 1
echo "plymouth-preview.sh: frames in $out"
