"""Outlines the Apex Symbolic masters into the shipped icon files.

Reads design/icons/apex-symbolic.json and writes icons/Apex/symbolic/: one
filled-outline SVG per drawing, and a relative symlink for every other name
with the same drawing. Uses picosvg (skia-pathops) to turn strokes into
fills and union overlapping strokes per layer, so it runs at development
time and the result is committed; a test checks it is up to date.

Exit status: 0 on success, 1 on an unusable glyph, 2 on a usage error.
"""

import argparse
from collections.abc import Sequence
import json
import pathlib
import shutil
import sys
from xml.etree import ElementTree

from picosvg import svg as picosvg

from apex_desktop.generators import icons
from apex_desktop.kernel import tokens as tokens_lib

_NS = "{http://www.w3.org/2000/svg}"
_DIGITS = 3


def outline(master: str) -> str:
    """Returns a master with its strokes converted to filled outlines.

    The result holds only `<svg>` and `<path>` elements; inactive layers
    keep their opacity, and fills are left for GTK and St to recolour.
    """
    # picosvg ships type hints but leaves fromstring unannotated.
    svg = picosvg.SVG.fromstring(master)  # type: ignore[no-untyped-call]
    pico = svg.topicosvg(ndigits=_DIGITS)
    root = ElementTree.fromstring(pico.tostring())
    lines = []
    for path in root.iter(f"{_NS}path"):
        opacity = path.get("opacity")
        attribute = f' opacity="{opacity}"' if opacity else ""
        lines.append(f'  <path{attribute} d="{path.get("d")}"/>\n')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"'
        ' width="16" height="16">\n'
        f"{''.join(lines)}</svg>\n"
    )


def build(
    glyph_table: pathlib.Path, tokens_file: pathlib.Path, out: pathlib.Path
) -> int:
    """Writes the outlined theme into out and returns the file count."""
    tokens = tokens_lib.Tokens.load(tokens_file)
    glyphs = json.loads(glyph_table.read_text(encoding="utf-8"))["glyphs"]
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    count = 0
    for name, aliases in icons.drawings(glyphs).items():
        target = f"{name}-symbolic.svg"
        text = outline(icons.master(glyphs[name], tokens))
        (out / target).write_text(text, encoding="utf-8")
        for alias in aliases:
            (out / f"{alias}-symbolic.svg").symlink_to(target)
        count += 1 + len(aliases)
    return count


def main(argv: Sequence[str] | None = None) -> int:
    """Parses arguments and builds the theme."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--glyphs",
        type=pathlib.Path,
        default=pathlib.Path("design/icons/apex-symbolic.json"),
    )
    parser.add_argument(
        "--tokens",
        type=pathlib.Path,
        default=pathlib.Path("design/system/tokens.json"),
    )
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=pathlib.Path("icons") / icons.THEME / icons.SYMBOLIC_DIR,
    )
    args = parser.parse_args(argv)
    try:
        build(args.glyphs, args.tokens, args.out)
    except (OSError, ValueError, KeyError) as error:
        print(f"build_icons: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
