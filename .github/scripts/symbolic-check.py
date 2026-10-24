#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Looks every name of desktop/icons/expected-symbolic.txt up with GTK 4's own icon theme in
# Apex, and counts which theme of its Inherits= chain draws it. A name nothing draws fails.

import argparse
import os
from collections import Counter

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("names", help="expected-symbolic.txt: NAME<TAB>PACKAGES lines; # and @ lines are skipped")
    parser.add_argument("themes", help="the directory that holds the built Apex theme")
    parser.add_argument("--search", action="append", default=[],
                        help="a further icon directory, after THEMES (default: /usr/share/icons)")
    parser.add_argument("--fallbacks", action="store_true",
                        help="list each name Apex does not draw, with the theme that does")
    args = parser.parse_args()
    search = [os.path.abspath(args.themes)] + [os.path.abspath(s) for s in args.search or ["/usr/share/icons"]]

    icon_theme = Gtk.IconTheme()
    icon_theme.set_search_path(search)
    icon_theme.set_theme_name("Apex")

    entries = [line.rstrip("\n").split("\t") for line in open(args.names)
               if line.strip() and not line.startswith(("#", "@"))]
    counts, fallbacks, missing = Counter(), [], []
    for name, *packages in entries:
        icon = icon_theme.lookup_icon(name, None, 16, 1, Gtk.TextDirection.NONE, 0)
        gfile = icon.get_file()
        path = (gfile.get_path() or gfile.get_uri()) if gfile else ""
        if os.path.basename(path) not in (name + ".svg", name + ".png", name + ".symbolic.png"):
            missing.append(f"{name}\t{' '.join(packages)}")
            continue
        root = next((s for s in search if path.startswith(s + "/")), None)
        theme = path[len(root) + 1:].split("/")[0] if root else "resource"
        counts[theme] += 1
        if theme != "Apex":
            fallbacks.append(f"{theme}\t{name}\t{' '.join(packages)}")

    if args.fallbacks:
        print("\n".join(sorted(fallbacks)))
    summary = ", ".join(f"{n} from {t}" for t, n in counts.most_common())
    print(f"symbolic-check.py: {len(entries)} names: {summary or 'none resolve'}")
    if missing:
        print(f"symbolic-check.py: {len(missing)} names resolve nowhere:", *missing, sep="\n  ")
        raise SystemExit(1)


main()
