#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Looks every folder icon name GLib 2.90 gives Files up with GTK 4's own icon theme, in
# Apex and in each Apex-<accent>, at list and grid sizes and at scale 1 and 2.

import os
import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402

# gio/glocalfileinfo.c get_icon_name(), and "folder", inode/directory's generic icon.
DRAWN = ["folder", "user-home", "user-desktop", "folder-documents", "folder-download",
         "folder-music", "folder-pictures", "folder-projects", "folder-publicshare",
         "folder-templates", "folder-videos"]
# Files shows these too, but boards 27 to 29 do not draw them: they stay Adwaita's.
UNDRAWN = ["folder-remote", "user-trash", "user-trash-full"]
LIST = [(16, 1), (24, 1), (32, 1), (16, 2), (24, 2), (32, 2)]
GRID = [(48, 1), (64, 1), (96, 1), (256, 1), (48, 2), (64, 2), (96, 2)]


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: places-check.py THEMES")
    themes = os.path.abspath(sys.argv[1])
    accents = dict(line.split() for line in open(os.path.join(os.path.dirname(__file__),
                   "../../desktop/icons/accents")) if line.strip() and not line.startswith("#"))
    fails = []

    def lookup(theme, name, size, scale):
        icon_theme = Gtk.IconTheme()
        icon_theme.set_search_path([themes, "/usr/share/icons"])
        icon_theme.set_theme_name(theme)
        icon = icon_theme.lookup_icon(name, None, size, scale, Gtk.TextDirection.NONE, 0)
        return icon.get_file().get_path() if icon.get_file() else ""

    for theme, colour in [("Apex", accents["blue"])] + [("Apex-" + a, c) for a, c in accents.items()]:
        for name in DRAWN:
            # Either list directory will do: both hold the folder without its emblem.
            for (size, scale), subdirs in [(s, ["32x32", "32x32@2x"]) for s in LIST] + \
                                          [(s, ["scalable"]) for s in GRID]:
                wants = [os.path.join(themes, theme, d, "places", name + ".svg") for d in subdirs]
                got = lookup(theme, name, size, scale)
                if got not in wants:
                    fails.append(f"{theme} {name} at {size}@{scale}: {got or 'nothing'}, not {' or '.join(wants)}")
                elif colour not in open(got).read():
                    fails.append(f"{got} does not use {colour}")
                elif subdirs != ["scalable"] and 'scale(1.245)"/>' not in open(got).read():
                    fails.append(f"{got} has an emblem at a list size")
    for name in UNDRAWN:
        print(f"places-check.py: {name} resolves to {lookup('Apex-red', name, 64, 1) or 'nothing'}")

    for fail in fails:
        print("FAIL:", fail, file=sys.stderr)
    if fails:
        sys.exit(1)
    print(f"places-check.py: {len(DRAWN)} folder names resolve to Apex in all {len(accents) + 1} themes")


main()
