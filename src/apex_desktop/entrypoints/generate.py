"""Writes every generated desktop file under <destdir>/usr.

scripts/install.sh runs this inside the image build, where only the
standard library is available. It reads design/system/tokens.json and the
cleared design assets, and writes nothing outside <destdir>/usr.

Exit status: 0 on success, 1 when the tokens or an asset are unusable, 2 on
a usage error.
"""

import argparse
from collections.abc import Sequence
import pathlib
import sys

from apex_desktop.generators import gtk
from apex_desktop.generators import settings
from apex_desktop.generators import shell
from apex_desktop.kernel import color
from apex_desktop.kernel import svg
from apex_desktop.kernel import tokens as tokens_lib

_SHARE = pathlib.Path("usr/share")
EXTENSION_DIR = _SHARE / "gnome-shell/extensions" / settings.EXTENSION_UUID


def _write(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def generate(design: pathlib.Path, destdir: pathlib.Path) -> list[str]:
    """Generates the files and returns their paths relative to destdir.

    Args:
        design: the repository's design/ folder.
        destdir: the install root; files go under destdir/usr only.

    Raises:
        tokens_lib.TokenError: a token the generator needs is missing.
        color.ColorError: a token is not a valid colour.
        svg.UnsafeSvgError: a design asset fails sanitising.
    """
    tokens = tokens_lib.Tokens.load(design / "system" / "tokens.json")
    files: dict[pathlib.Path, str] = {}
    for scheme in tokens_lib.Scheme:
        files[EXTENSION_DIR / f"stylesheet-{scheme.value}.css"] = (
            shell.stylesheet(tokens, scheme)
        )
    files[EXTENSION_DIR / "schemas" / f"{settings.SCHEMA_ID}.gschema.xml"] = (
        settings.schema()
    )
    files[_SHARE / "apex-desktop/gtk-4.0/gtk.css"] = gtk.stylesheet(tokens)
    files[_SHARE / "glib-2.0/schemas/zz0-apex.gschema.override"] = (
        settings.override(tokens)
    )
    files[_SHARE / "gnome-background-properties/apex.xml"] = (
        settings.background_properties(tokens)
    )
    assets = design / "canvas" / "assets"
    for installed, source in settings.WALLPAPERS.items():
        text = (assets / source).read_text(encoding="utf-8")
        files[_SHARE / "backgrounds/apex" / installed] = svg.sanitize(text)

    for relative, text in files.items():
        _write(destdir / relative, text)
    return sorted(str(path) for path in files)


def main(argv: Sequence[str] | None = None) -> int:
    """Parses arguments and generates the files."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("design", type=pathlib.Path, help="the design folder")
    parser.add_argument("destdir", type=pathlib.Path, help="the install root")
    args = parser.parse_args(argv)
    try:
        generate(args.design, args.destdir)
    except (
        tokens_lib.TokenError,
        color.ColorError,
        svg.UnsafeSvgError,
        OSError,
    ) as error:
        print(f"generate: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
