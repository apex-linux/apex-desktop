#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Checks DIR's apex-greeter-light.png and apex-greeter-dark.png: PNGs at 2880x1800, the
# laptop's panel, as the spec renders them for gdm's background.

set -euo pipefail

(($# == 1)) || { echo "usage: check-greeter.sh DIR" >&2; exit 2; }
fails=0
for v in light dark; do
    f=$1/apex-greeter-$v.png
    if [[ ! -f $f || $(od -An -tx1 -N8 "$f" | tr -d ' \n') != 89504e470d0a1a0a ]]; then
        echo "check-greeter.sh: $f is missing or not a PNG" >&2
        fails=1
        continue
    fi
    read -ra b <<<"$(od -An -tu1 -j16 -N8 "$f")"
    w=$(((b[0] << 24) + (b[1] << 16) + (b[2] << 8) + b[3]))
    h=$(((b[4] << 24) + (b[5] << 16) + (b[6] << 8) + b[7]))
    ((w == 2880 && h == 1800)) || { echo "check-greeter.sh: $f is ${w}x$h, not 2880x1800" >&2; fails=1; }
done
((fails == 0)) || exit 1
echo "check-greeter.sh: both greeter backgrounds are 2880x1800"
