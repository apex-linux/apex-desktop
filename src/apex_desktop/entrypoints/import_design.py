"""Copies the design sources the build reads from a design folder.

The design owner keeps the canvas export in an untracked `.design/` folder.
This tool copies the documents and the assets cleared for shipping into
`design/`, so a clean clone builds without that folder. It is a developer
tool; the image build never runs it.

Exit status: 0 on success, 1 when an asset fails sanitising, 2 on a usage
error.
"""

import argparse
from collections.abc import Sequence
import pathlib
import re
import sys

from apex_desktop.kernel import svg

# The canvas lives in a private artifact; the public repository names it
# without its address.
_CANVAS_URL = re.compile(r"\(?https://claude\.ai/artifact/[A-Za-z0-9]+\)?")
_CANVAS_NAME = "(the owner's private canvas)"

_DOCUMENTS = (
    "INDEX.md",
    "OPEN-QUESTIONS.md",
    "system/README.md",
    "system/tokens.json",
    "canvas/assets/MANIFEST.md",
)

# Assets cleared for shipping, by blob id. Everything else in the manifest
# is withheld; design/canvas/assets/README.md says why.
_ASSETS = {
    "3d451127dc2b77221bac98465ee1ec99": "facets-light.svg",
    "f607332583898d73d053baf1c0cae872": "facets-dark.svg",
}


def _redact(text: str) -> str:
    return _CANVAS_URL.sub(_CANVAS_NAME, text)


def import_design(source: pathlib.Path, dest: pathlib.Path) -> None:
    """Copies the documents and cleared assets from source into dest.

    Args:
        source: the design folder, laid out as `.design/` is.
        dest: the repository's `design/` folder.

    Raises:
        svg.UnsafeSvgError: a cleared asset fails sanitising.
    """
    documents = list(_DOCUMENTS)
    documents += [
        str(path.relative_to(source))
        for path in sorted((source / "handoff").glob("*.md"))
    ]
    for name in documents:
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        text = (source / name).read_text(encoding="utf-8")
        target.write_text(_redact(text), encoding="utf-8")

    assets = dest / "canvas" / "assets"
    for blob, name in _ASSETS.items():
        text = (source / "canvas" / "assets" / f"{blob}.svg").read_text(
            encoding="utf-8"
        )
        (assets / name).write_text(svg.sanitize(text), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    """Parses arguments and runs the import."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=pathlib.Path, help="the .design folder")
    parser.add_argument(
        "--dest",
        type=pathlib.Path,
        default=pathlib.Path("design"),
        help="where to write (default: design)",
    )
    args = parser.parse_args(argv)
    if not (args.source / "system" / "tokens.json").is_file():
        print(f"{args.source} has no system/tokens.json", file=sys.stderr)
        return 2
    try:
        import_design(args.source, args.dest)
    except svg.UnsafeSvgError as error:
        print(f"import_design: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
