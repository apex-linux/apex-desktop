#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Draws board 31's contact sheets with GTK 4's own symbolic recolouring, headless, at scale 2.
# contact-sheet.sh checks the dependencies and runs it; its usage is the contract.

import os
import sys

import gi

for namespace, version in [("Gdk", "4.0"), ("Graphene", "1.0"), ("Gsk", "4.0"), ("Gtk", "4.0"),
                           ("Pango", "1.0"), ("PangoCairo", "1.0")]:
    gi.require_version(namespace, version)
from gi.repository import Gdk, Graphene, Gsk, Gtk, Pango, PangoCairo  # noqa: E402

BOARD = "31"
BOARD_SLUG = "symbolic"
SCALE = 2
GLYPH = 16
COLUMNS = 7
CELL_W, CELL_H, PAD, TITLE_H = 168, 56, 16, 40
# libadwaita's window background and foreground.
STYLES = {"light": ("#fafafb", "rgba(0,0,6,0.8)"), "dark": ("#222226", "#ffffff")}
FONT = "Adwaita Sans"


def rgba(spec):
    colour = Gdk.RGBA()
    colour.parse(spec)
    return colour


def rect(x, y, w, h):
    r = Graphene.Rect()
    r.init(x, y, w, h)
    return r


def point(x, y):
    p = Graphene.Point()
    p.init(x, y)
    return p


def layout(text, size, width=None):
    lay = Pango.Layout.new(PangoCairo.FontMap.get_default().create_context())
    lay.set_font_description(Pango.FontDescription.from_string(f"{FONT} {size}"))
    lay.set_text(text, -1)
    if width:
        lay.set_width(width * Pango.SCALE)
        lay.set_alignment(Pango.Alignment.CENTER)
        lay.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
    return lay


def render(renderer, node, w, h):
    return renderer.render_texture(node, rect(0, 0, w * SCALE, h * SCALE))


def glyph_is_empty(renderer, paintable, fg):
    snapshot = Gtk.Snapshot()
    snapshot.scale(SCALE, SCALE)
    paintable.snapshot_symbolic(snapshot, GLYPH, GLYPH, [fg])
    node = snapshot.to_node()
    if node is None:
        return True
    downloader = Gdk.TextureDownloader.new(render(renderer, node, GLYPH, GLYPH))
    downloader.set_format(Gdk.MemoryFormat.R8G8B8A8)
    data, _ = downloader.download_bytes()
    return not any(data.get_data()[3::4])


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: contact-sheet.py ICONS_DIR OUT_DIR BOARDS_FILE")
    icons, out, boards = (os.path.abspath(a) for a in sys.argv[1:])
    scenes = {}
    for line in open(boards):
        if line.strip() and not line.startswith("#"):
            scene, name = line.split()
            scenes.setdefault(scene, []).append(name)

    theme = Gtk.IconTheme()
    theme.set_search_path([icons])
    theme.set_theme_name("Apex")
    renderer = Gsk.CairoRenderer()
    renderer.realize(None)
    failures = []
    os.makedirs(out, exist_ok=True)

    for scene, names in scenes.items():
        paintables, failed = [], len(failures)
        for name in names:
            want = os.path.join(icons, "Apex", "symbolic", f"{name}-symbolic.svg")
            paintable = theme.lookup_icon(f"{name}-symbolic", None, GLYPH, SCALE, Gtk.TextDirection.NONE, 0)
            gfile = paintable.get_file()
            if not gfile or gfile.get_path() != want:
                failures.append(f"{scene} {name}: missing, no {want}")
            elif glyph_is_empty(renderer, paintable, rgba("#000")):
                failures.append(f"{scene} {name}: empty, {want} draws nothing")
            paintables.append(paintable)
        if len(failures) > failed:
            continue
        for style, (bg_spec, fg_spec) in STYLES.items():
            bg, fg = rgba(bg_spec), rgba(fg_spec)
            rows = -(-len(names) // COLUMNS)
            w, h = 2 * PAD + COLUMNS * CELL_W, 2 * PAD + TITLE_H + rows * CELL_H
            snapshot = Gtk.Snapshot()
            snapshot.scale(SCALE, SCALE)
            snapshot.append_color(bg, rect(0, 0, w, h))
            title = f"Board {BOARD} · Apex Symbolic · {scene} · {len(names)} glyphs · {style}"
            snapshot.save()
            snapshot.translate(point(PAD, PAD))
            snapshot.append_layout(layout(title, 11), fg)
            snapshot.restore()
            for i, (name, paintable) in enumerate(zip(names, paintables)):
                x = PAD + (i % COLUMNS) * CELL_W
                y = PAD + TITLE_H + (i // COLUMNS) * CELL_H
                snapshot.save()
                snapshot.translate(point(x + (CELL_W - GLYPH) / 2, y + 8))
                paintable.snapshot_symbolic(snapshot, GLYPH, GLYPH, [fg])
                snapshot.restore()
                snapshot.save()
                snapshot.translate(point(x + 4, y + 8 + GLYPH + 6))
                snapshot.append_layout(layout(name, 7, CELL_W - 8), fg)
                snapshot.restore()
            path = os.path.join(out, f"board-{BOARD}-{BOARD_SLUG}-{scene}-{style}.png")
            render(renderer, snapshot.to_node(), w, h).save_to_png(path)
            print(f"contact-sheet.py: {path}: {len(names)} glyphs")

    renderer.unrealize()
    if failures:
        print(f"contact-sheet.py: {len(failures)} glyphs fail:", *failures, sep="\n  ", file=sys.stderr)
        sys.exit(1)


main()
