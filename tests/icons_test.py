"""Tests the shipped Apex Symbolic files against apex-symbolic.md."""

import json
import pathlib
import re
import tempfile
import unittest
from xml.etree import ElementTree

from apex_desktop.entrypoints import build_icons
from apex_desktop.generators import icons

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_GLYPHS = _ROOT / "design/icons/apex-symbolic.json"
_TOKENS = _ROOT / "design/system/tokens.json"
_SHIPPED = _ROOT / "icons" / icons.THEME / icons.SYMBOLIC_DIR
_NS = "{http://www.w3.org/2000/svg}"
_NUMBER = re.compile(r"-?\d*\.?\d+")


def _glyphs() -> dict[str, dict[str, str]]:
    return dict(json.loads(_GLYPHS.read_text(encoding="utf-8"))["glyphs"])


class ShippedIconsTest(unittest.TestCase):

    def test_every_drawn_name_ships(self) -> None:
        names = {path.name for path in _SHIPPED.iterdir()}
        expected = {f"{name}-symbolic.svg" for name in _glyphs()}
        self.assertEqual(names, expected)
        self.assertEqual(len(names), 289)

    def test_shared_drawings_are_symlinks(self) -> None:
        links = [path for path in _SHIPPED.iterdir() if path.is_symlink()]
        self.assertEqual(len(links), 289 - 224)
        for link in links:
            with self.subTest(link.name):
                target = pathlib.Path(link.readlink())
                self.assertEqual(target.parent, pathlib.Path("."))
                self.assertTrue((_SHIPPED / target).is_file())

    def test_only_filled_paths(self) -> None:
        glyphs = _glyphs()
        for path in sorted(_SHIPPED.iterdir()):
            if path.is_symlink():
                continue
            name = path.name.removesuffix("-symbolic.svg")
            with self.subTest(path.name):
                root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
                self.assertEqual(root.tag, f"{_NS}svg")
                self.assertEqual(
                    dict(root.attrib),
                    {"viewBox": "0 0 16 16", "width": "16", "height": "16"},
                )
                for child in root:
                    self.assertEqual(child.tag, f"{_NS}path")
                    self.assertLessEqual(set(child.attrib), {"d", "opacity"})
                    opacity = child.get("opacity")
                    if opacity is not None:
                        self.assertAlmostEqual(float(opacity), 0.35)
                        self.assertTrue(glyphs[name]["o"])

    def test_geometry_stays_on_the_canvas(self) -> None:
        # Control points included, so the margin is looser than the 0.5
        # the painted outline keeps.
        for path in _SHIPPED.iterdir():
            if path.is_symlink():
                continue
            text = path.read_text(encoding="utf-8")
            numbers = [float(n) for n in _NUMBER.findall(text.split(">", 1)[1])]
            with self.subTest(path.name):
                self.assertGreaterEqual(min(numbers), 0.25)
                self.assertLessEqual(max(numbers), 15.75)

    def test_shipped_files_match_the_masters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp) / "symbolic"
            build_icons.build(_GLYPHS, _TOKENS, out)
            for path in sorted(_SHIPPED.iterdir()):
                fresh = out / path.name
                with self.subTest(path.name):
                    if path.is_symlink():
                        self.assertEqual(path.readlink(), fresh.readlink())
                    else:
                        self.assertEqual(
                            path.read_text(encoding="utf-8"),
                            fresh.read_text(encoding="utf-8"),
                            "run: just icons",
                        )


class IndexThemeTest(unittest.TestCase):

    def test_chain_and_directories(self) -> None:
        text = icons.index_theme()
        self.assertIn("Name=Apex\n", text)
        self.assertIn("Inherits=Adwaita,hicolor\n", text)
        self.assertIn("Directories=symbolic\n", text)
        self.assertIn("[symbolic]\n", text)

    def test_full_colour_names_are_drawn_by_apex(self) -> None:
        # Only a name Apex draws as -symbolic hides Adwaita's full colour.
        paths = _full_colour()
        self.assertEqual(paths, sorted(set(paths)))
        self.assertIn("scalable/places/folder.svg", paths)
        for path in paths:
            with self.subTest(path):
                size, _, file = path.split("/")
                self.assertIn(size, icons.FULL_COLOUR_SIZES)
                stem = file.rsplit(".", 1)[0]
                self.assertTrue((_SHIPPED / f"{stem}-symbolic.svg").exists())

    def test_full_colour_directories_are_declared(self) -> None:
        text = icons.index_theme(_full_colour())
        self.assertIn("Directories=symbolic,16x16/devices,16x16/emblems,", text)
        self.assertIn(
            "[scalable/places]\nContext=Places\nSize=128\nMinSize=8\n"
            "MaxSize=512\nType=Scalable\n",
            text,
        )
        self.assertIn(
            "[16x16/places]\nContext=Places\nSize=16\nType=Fixed\n", text
        )

    def test_requires_names_every_linked_file(self) -> None:
        paths = _full_colour()
        lines = [
            line
            for line in icons.requires(paths).splitlines()
            if line and not line.startswith("#")
        ]
        self.assertEqual(len(lines), len(paths))
        for line, path in zip(lines, paths):
            self.assertEqual(
                line, f"adwaita-icon-theme /usr/share/icons/Adwaita/{path}"
            )


def _full_colour() -> list[str]:
    return icons.read_full_colour(
        (_ROOT / icons.FULL_COLOUR_LIST).read_text(encoding="utf-8")
    )


if __name__ == "__main__":
    unittest.main()
