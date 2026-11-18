"""Lists the Adwaita full-colour icons that the Apex theme must carry.

GTK 4 looks an icon up theme by theme, and in each theme tries every name
the icon carries, symbolic variants included (GThemedIcon adds them). A
name Apex draws as `X-symbolic` therefore hides Adwaita's full-colour `X`:
Files asks for "folder" and gets the Apex folder glyph. Apex carries those
full-colour files as links into Adwaita, so the lookup stops at them.

Reads an Adwaita icon directory and icons/Apex/symbolic/, and writes
icons/adwaita-full-colour.txt: one Adwaita-relative path per line, for
every full-colour file under scalable/ or 16x16/ whose name Apex draws.
AdwaitaLegacy is not listed: its old full-colour action icons give way to
the Apex glyphs, as they do to Adwaita's own symbolic icons.

Exit status: 0 on success, 2 on a usage error.
"""

import argparse
from collections.abc import Sequence
import pathlib
import sys

from apex_desktop.generators import icons

_ROOT = pathlib.Path(__file__).resolve().parents[3]
_SUFFIX = "-symbolic.svg"


def full_colour(adwaita: pathlib.Path, apex: pathlib.Path) -> list[str]:
    """Returns the Adwaita-relative paths Apex must link to, sorted."""
    drawn = {
        path.name.removesuffix(_SUFFIX)
        for path in apex.iterdir()
        if path.name.endswith(_SUFFIX)
    }
    found = []
    for size in icons.FULL_COLOUR_SIZES:
        for path in sorted((adwaita / size).glob("*/*")):
            if path.stem in drawn and path.suffix in (".svg", ".png"):
                found.append(str(path.relative_to(adwaita)))
    return sorted(found)


def main(argv: Sequence[str] | None = None) -> int:
    """Parses arguments and writes the list."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "adwaita", type=pathlib.Path, help="an installed Adwaita theme"
    )
    args = parser.parse_args(argv)
    if not (args.adwaita / "index.theme").is_file():
        parser.error(f"{args.adwaita} is not an icon theme")
    paths = full_colour(
        args.adwaita, _ROOT / "icons" / icons.THEME / "symbolic"
    )
    (_ROOT / icons.FULL_COLOUR_LIST).write_text(
        icons.FULL_COLOUR_HEADER + "".join(f"{p}\n" for p in paths),
        encoding="utf-8",
    )
    print(f"{len(paths)} full-colour files", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
