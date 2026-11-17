"""Extracts the Apex Symbolic glyphs from the four canvas contact sheets.

Each sheet's script holds `const GL = [[group, [[id, label, d, f, o], ...]],
...]`. The literal is read with a small tokenizer, never evaluated, because
canvas files are untrusted. The result, design/icons/apex-symbolic.json,
is the source of truth for the icon build (apex-symbolic.md, open question
3). A developer tool; the image build never runs it.

Exit status: 0 on success, 1 when the sheets disagree or cannot be read,
2 on a usage error.
"""

import argparse
from collections.abc import Iterator, Sequence
import json
import pathlib
import re
import sys
from typing import Any

# Sheet artboard -> board number, in the order the spec lists them.
SHEETS = {
    "Glyphs.dc.html": "31",
    "GlyphFamilies.dc.html": "31b",
    "GlyphActions.dc.html": "31c",
    "GlyphMore.dc.html": "31d",
}

_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_PATH = re.compile(r"^[MmLlHhVvCcSsQqTtAaZz0-9.,\s+-]*$")
_TOKEN = re.compile(
    r"""\s*(?:(\[)|(\])|(,)|'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)")"""
)


class SheetError(ValueError):
    """Raised when a sheet's glyph list is missing or malformed."""


def _tokens(text: str) -> Iterator[tuple[str, str]]:
    position = 0
    while position < len(text):
        match = _TOKEN.match(text, position)
        if match is None:
            if text[position:].strip() == "":
                return
            raise SheetError(f"unexpected text at {text[position:][:20]!r}")
        position = match.end()
        opening, closing, comma, single, double = match.groups()
        if opening:
            yield "[", ""
        elif closing:
            yield "]", ""
        elif comma:
            yield ",", ""
        else:
            raw = single if single is not None else double
            yield "str", re.sub(r"\\(.)", r"\1", raw)


def _parse(tokens: list[tuple[str, str]], at: int) -> tuple[Any, int]:
    """Parses one string or array starting at token index `at`."""
    kind, value = tokens[at]
    if kind == "str":
        return value, at + 1
    if kind != "[":
        raise SheetError(f"expected a value, got {kind!r}")
    items: list[Any] = []
    at += 1
    while tokens[at][0] != "]":
        item, at = _parse(tokens, at)
        items.append(item)
        if tokens[at][0] == ",":
            at += 1
    return items, at + 1


def glyph_list(html: str) -> list[Any]:
    """Returns the parsed `GL` literal of one sheet."""
    start = html.find("const GL = [")
    if start < 0:
        raise SheetError("no `const GL = [` in the sheet")
    start = html.index("[", start)
    end = html.find("\n    ];", start)
    if end < 0:
        raise SheetError("the GL literal does not end")
    literal = html[start : end + len("\n    ]")]
    try:
        result, _ = _parse(list(_tokens(literal)), 0)
    except IndexError as error:
        raise SheetError("the GL literal is truncated") from error
    return list(result)


def extract(project: pathlib.Path) -> dict[str, Any]:
    """Reads the four sheets and returns the glyph table.

    Raises:
        SheetError: a sheet is malformed, or one name has two drawings.
    """
    glyphs: dict[str, dict[str, str]] = {}
    for sheet, board in SHEETS.items():
        html = (project / sheet).read_text(encoding="utf-8")
        for group, items in glyph_list(html):
            for name, label, d, f, o in items:
                if not _NAME.match(name):
                    raise SheetError(f"bad icon name {name!r}")
                for path in (d, f, o):
                    if not _PATH.match(path):
                        raise SheetError(f"bad path data in {name}")
                entry = {"d": d, "f": f, "o": o}
                if name in glyphs:
                    old = {k: glyphs[name][k] for k in ("d", "f", "o")}
                    if old != entry:
                        raise SheetError(f"{name} has two different drawings")
                    continue
                glyphs[name] = {
                    "board": board,
                    "group": group,
                    "label": label,
                    **entry,
                }
    return {
        "source": "Apex Symbolic contact sheets 31, 31b, 31c and 31d",
        "glyphs": dict(sorted(glyphs.items())),
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Parses arguments and writes the glyph table."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "project", type=pathlib.Path, help="the canvas project folder"
    )
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=pathlib.Path("design/icons/apex-symbolic.json"),
    )
    args = parser.parse_args(argv)
    try:
        table = extract(args.project)
    except (SheetError, OSError, ValueError) as error:
        print(f"extract_glyphs: {error}", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(table, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
