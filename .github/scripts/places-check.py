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
SET_BY_APEX_FOLDER_ICONS_SH = ["folder-screenshots"]
DRAWN += SET_BY_APEX_FOLDER_ICONS_SH
# The dock's bin, in no accent: every theme finds Apex's through Inherits=.
NEUTRAL = ["user-trash", "user-trash-full"]
LIST = [(16, 1), (24, 1), (32, 1), (16, 2), (24, 2), (32, 2)]
GRID = [(48, 1), (64, 1), (96, 1), (256, 1), (48, 2), (64, 2), (96, 2)]
EMBLEMLESS_DIRS = ["32x32", "32x32@2x"]


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
            for (size, scale), subdirs in [(s, EMBLEMLESS_DIRS) for s in LIST] + \
                                          [(s, ["scalable"]) for s in GRID]:
                wants = [os.path.join(themes, theme, d, "places", name + ".svg") for d in subdirs]
                got = lookup(theme, name, size, scale)
                if got not in wants:
                    fails.append(f"{theme} {name} at {size}@{scale}: {got or 'nothing'}, not {' or '.join(wants)}")
                elif colour not in open(got).read():
                    fails.append(f"{got} does not use {colour}")
                elif subdirs != ["scalable"] and 'scale(1.245)"/>' not in open(got).read():
                    fails.append(f"{got} has an emblem at a list size")
        for name in NEUTRAL:
            for (size, scale), subdir in [(s, "32x32") for s in LIST] + [(s, "scalable") for s in GRID]:
                got = lookup(theme, name, size, scale)
                if os.path.dirname(os.path.dirname(got)) not in [os.path.join(themes, "Apex", d) for d in
                                                                 (subdir, subdir + "@2x")]:
                    fails.append(f"{theme} {name} at {size}@{scale}: {got or 'nothing'}, not Apex's")

    for fail in fails:
        print("FAIL:", fail, file=sys.stderr)
    if fails:
        sys.exit(1)
    print(f"places-check.py: {len(DRAWN)} folder names and {len(NEUTRAL)} neutral ones resolve to Apex in all "
          f"{len(accents) + 1} themes")


main()
