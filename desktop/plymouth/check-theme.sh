#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Checks THEMES/apex and THEMES/apex-twostep as build.sh writes them and the spec installs
# them: the keyfiles, every image the script loads at 1x and @2x, and the two-step images.

set -euo pipefail

(($# == 1)) || { echo "usage: check-theme.sh THEMES" >&2; exit 2; }
themes=$1
fails=0
fail() {
    echo "check-theme.sh: $*" >&2
    fails=$((fails + 1))
}

# KEY=value of a group in a keyfile, empty when absent.
value() {
    awk -v group="[$2]" -v key="$3" '
        /^\[/ { in_group = ($0 == group); next }
        in_group && index($0, key "=") == 1 { print substr($0, length(key) + 2); exit }
    ' "$1"
}

# Width and height from the PNG's IHDR chunk.
png_size() {
    local b
    read -ra b <<<"$(od -An -tu1 -j16 -N8 "$1")"
    echo "$(((b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3])) $(((b[4] << 24) + (b[5] << 16) + (b[6] << 8) + b[7]))"
}

is_png() {
    [[ -f $1 && $(od -An -tx1 -N8 "$1" | tr -d ' \n') == 89504e470d0a1a0a ]]
}

check_keyfile() {
    local name=$1 module=$2 file="$themes/$1/$1.plymouth" dir
    [[ -f $file ]] || { fail "$file is missing"; return; }
    [[ -n $(value "$file" "Plymouth Theme" Name) ]] || fail "$file: no Name"
    [[ $(value "$file" "Plymouth Theme" ModuleName) == "$module" ]] || fail "$file: ModuleName is not $module"
    dir=$(value "$file" "$module" ImageDir)
    [[ $dir == "/usr/share/plymouth/themes/$name" ]] || fail "$file: ImageDir '$dir' is not /usr/share/plymouth/themes/$name"
}

check_keyfile apex script
script=$(value "$themes/apex/apex.plymouth" script ScriptFile)
[[ $script == /usr/share/plymouth/themes/apex/apex.script ]] || fail "apex.plymouth: ScriptFile is '$script'"
[[ -f $themes/apex/apex.script ]] || fail "apex/apex.script is missing"

mapfile -t assets < <(grep -o 'asset("[^"]*")' "$themes/apex/apex.script" | sed 's/asset("\(.*\)")/\1/' | sort -u)
((${#assets[@]} > 0)) || fail "apex.script loads no asset()"
for a in "${assets[@]}"; do
    one="$themes/apex/$a.png" two="$themes/apex/$a@2x.png"
    is_png "$one" || { fail "$one is missing or not a PNG"; continue; }
    is_png "$two" || { fail "$two is missing or not a PNG"; continue; }
    read -r w h <<<"$(png_size "$one")"
    read -r w2 h2 <<<"$(png_size "$two")"
    ((w2 == 2 * w && h2 == 2 * h)) || fail "$a@2x.png is ${w2}x$h2, not twice $a.png's ${w}x$h"
done
read -r w h <<<"$(png_size "$themes/apex/bar-fill.png")"
((w == 160 && h == 3)) || fail "bar-fill.png is ${w}x$h, not board 01's 160x3"

check_keyfile apex-twostep two-step
for n in watermark entry bullet lock; do
    is_png "$themes/apex-twostep/$n.png" || fail "apex-twostep/$n.png is missing or not a PNG"
done
file="$themes/apex-twostep/apex-twostep.plymouth"
[[ $(value "$file" boot-up UseProgressBar) == true ]] || fail "$file: the boot has no progress bar"
# Both themes are drawn for DeviceScale=1: device-size images, bar and text.
[[ $(value "$file" two-step ProgressBarWidth)x$(value "$file" two-step ProgressBarHeight) == 320x6 ]] ||
    fail "$file: the bar is not board 01's 160x3 at @2x"
[[ $(png_size "$themes/apex-twostep/watermark.png") == "$(png_size "$themes/apex/wordmark@2x.png")" ]] ||
    fail "apex-twostep/watermark.png is not the @2x wordmark"
for f in "$themes/apex/apex.plymouth:script" "$file:two-step"; do
    [[ $(value "${f%:*}" "${f##*:}" MonospaceFont) == "monospace 20" ]] ||
        fail "${f%:*}: MonospaceFont is not 'monospace 20', the Esc view's DeviceScale=2 size"
done

((fails == 0)) || exit 1
echo "check-theme.sh: apex (${#assets[@]} images at 1x and @2x) and apex-twostep pass"
