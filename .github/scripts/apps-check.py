#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Looks each app icon desktop/icons/apps draws, and its -symbolic name, up with GTK 4's own icon
# theme in Apex and each Apex-<accent>: Apex's drawing must win over Colloid's and the app's own.

import filecmp
import os
import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402

SIZES = [(16, 1), (24, 1), (32, 1), (48, 1), (64, 1), (128, 1), (256, 1), (16, 2), (32, 2), (64, 2)]


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: apps-check.py THEMES")
    themes = os.path.abspath(sys.argv[1])
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../desktop/icons")
    apps = sorted(f[:-4] for f in os.listdir(os.path.join(here, "apps")) if f.endswith(".svg"))
    accents = [line.split()[0] for line in open(os.path.join(here, "accents"))
               if line.strip() and not line.startswith("#")]
    fails = []

    def lookup(theme, name, size, scale):
        icon_theme = Gtk.IconTheme()
        icon_theme.set_search_path([themes, "/usr/share/icons"])
        icon_theme.set_theme_name(theme)
        icon = icon_theme.lookup_icon(name, None, size, scale, Gtk.TextDirection.NONE, 0)
        return icon.get_file().get_path() if icon.get_file() else ""

    for theme in ["Apex"] + ["Apex-" + a for a in accents]:
        for name in apps:
            want = os.path.join(themes, "Apex", "scalable", "apps", name + ".svg")
            wants_symbolic = os.path.join(themes, "Apex", "symbolic", name + "-symbolic.svg")
            for size, scale in SIZES:
                got = lookup(theme, name, size, scale)
                if got != want:
                    fails.append(f"{theme} {name} at {size}@{scale}: {got or 'nothing'}, not {want}")
                elif not filecmp.cmp(got, os.path.join(here, "apps", name + ".svg"), shallow=False):
                    fails.append(f"{got} is not desktop/icons/apps/{name}.svg")
                got = lookup(theme, name + "-symbolic", size, scale)
                if got != wants_symbolic:
                    fails.append(f"{theme} {name}-symbolic at {size}@{scale}: {got or 'nothing'}, "
                                 f"not {wants_symbolic}")

    for fail in fails:
        print("FAIL:", fail, file=sys.stderr)
    if fails:
        sys.exit(1)
    print(f"apps-check.py: {' '.join(apps)} and the -symbolic names resolve to Apex in all "
          f"{len(accents) + 1} themes")


main()
