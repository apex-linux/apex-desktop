#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Guesses the content type of board 27's files, and of common ones, as Files does, and
# looks its icon up with GTK 4 in Apex: the file colour of its kind, labelled from 41 px up.

import os
import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk  # noqa: E402

SAMPLES = {
    "doc": ["Apex Fedora — Spec.odt", "Keyboard Shortcuts.odt", "letter.docx", "old.doc", "note.rtf"],
    "sheet": ["Design Tokens.ods", "budget.xlsx", "old.xls", "export.csv"],
    "md": ["HIG Notes.md", "README.md", "notes.txt"],
    "pdf": ["Invoice-2026-09.pdf"],
    "iso": ["Fedora-Workstation-Live-45.iso", "disk.img"],
    "archive": ["adwaita-icons-src.tar.xz", "inter-4.1.zip", "jetbrains-mono-2.304.zip",
                "a.tar.gz", "a.gz", "a.tar", "a.7z", "a.zst", "a.tar.zst", "a.xz"],
    "audio": ["Rain on Glass.flac", "Night Drive.opus", "Focus Loop.ogg", "a.mp3", "a.wav"],
    "video": ["Boot Animation v3.webm", "Overview Transition.mp4", "a.mkv"],
    "code": ["stylesheet.scss", "metadata.json", "extension.js", "Makefile", "a.css", "a.html",
             "a.py", "a3.py", "a.c", "a.h", "a.rs", "a.sh", "a.xml"],
    "image": ["mockup-2880x1800.png", "icon-grid.png", "a.jpg", "a.svg", "a.webp", "a.gif"],
    "file": ["apex.plymouth", "blob.bin"],
}


def table(path):
    return [line.split() for line in open(path) if line.strip() and not line.startswith("#")]


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: mimetypes-check.py THEMES")
    themes = os.path.abspath(sys.argv[1])
    src = os.path.join(os.path.dirname(__file__), "../../desktop/icons/mimetypes")
    colour = dict(table(os.path.join(src, "kinds")))
    names = {row[0] for row in table(os.path.join(src, "types"))}
    fails = []

    gio_names = set()
    for content_type in Gio.content_types_get_registered():
        gio_names.update(Gio.content_type_get_icon(content_type).get_names())
    fails += [f"{n} is no icon name GIO gives any content type" for n in sorted(names - gio_names)]

    icon_theme = Gtk.IconTheme()
    icon_theme.set_search_path([themes, "/usr/share/icons"])
    icon_theme.set_theme_name("Apex")
    for kind, files in SAMPLES.items():
        for name in files:
            content_type, _ = Gio.content_type_guess(name, None)
            gicon = Gio.content_type_get_icon(content_type)
            for size, scale, subdirs in [(24, 1, ["32x32"]), (24, 2, ["32x32", "32x32@2x"]), (64, 1, ["scalable"]),
                                         (64, 2, ["scalable"])]:
                icon = icon_theme.lookup_by_gicon(gicon, size, scale, Gtk.TextDirection.NONE, 0)
                path = icon.get_file().get_path() if icon.get_file() else ""
                if os.path.dirname(path) not in [os.path.join(themes, "Apex", d, "mimetypes") for d in subdirs]:
                    fails.append(f"{name} ({content_type}) at {size}@{scale}: {path or 'nothing'}")
                elif colour[kind] not in open(path).read():
                    fails.append(f"{name} ({content_type}): {path} is not {kind}'s {colour[kind]}")

    for fail in fails:
        print("FAIL:", fail, file=sys.stderr)
    if fails:
        sys.exit(1)
    count = sum(len(files) for files in SAMPLES.values())
    print(f"mimetypes-check.py: {count} files of {len(SAMPLES)} kinds resolve to Apex in their colour")


main()
