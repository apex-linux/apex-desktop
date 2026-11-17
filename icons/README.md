# Apex icon theme

`Apex/symbolic/` holds Apex Symbolic, the 289 symbolic glyphs drawn on the
canvas contact sheets 31 to 31d, as filled outlines. GTK and GNOME Shell
recolour a symbolic icon by forcing its fill, so the stroked drawings are
outlined before they ship. Names that share a drawing are symlinks.

These files are build output. Edit the source, then rebuild:

1.  `design/icons/apex-symbolic.json` is the glyph table, extracted from
    the sheets. The design owner changes the sheets; `just icons` extracts
    the table again and rebuilds this folder.
2.  The stroke width, caps, joins and inactive opacity come from
    `design/system/tokens.json` (`icon`).

`just test` fails if this folder is not what the table and tokens produce.

The theme inherits from Adwaita and hicolor, so undrawn symbolic names come
from Adwaita and app icons from each app. Full-colour app icons (Colloid)
are not part of it until OQ-16 is settled; see
[design/canvas/assets/README.md](../design/canvas/assets/README.md).

The drawings are Apex's own and share this repository's licence.
