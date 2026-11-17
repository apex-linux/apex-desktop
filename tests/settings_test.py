"""Tests the default settings and the wallpaper list."""

import pathlib
import unittest
from xml.etree import ElementTree

from apex_desktop.generators import settings
from apex_desktop.kernel import svg
from apex_desktop.kernel import tokens as tokens_lib

_TOKENS = pathlib.Path(__file__).resolve().parent.parent / (
    "design/system/tokens.json"
)


class SettingsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.tokens = tokens_lib.Tokens.load(_TOKENS)

    def test_override_sets_the_wallpaper_pair(self) -> None:
        text = settings.override(self.tokens)
        self.assertIn(
            "picture-uri='file:///usr/share/backgrounds/apex/facets-l.svg'",
            text,
        )
        self.assertIn(
            "picture-uri-dark="
            "'file:///usr/share/backgrounds/apex/facets-d.svg'",
            text,
        )
        self.assertIn("primary-color='#e8ebf0'", text)
        self.assertIn("enabled-extensions=['apex@apex-linux.github.io']", text)

    def test_override_asks_for_the_light_shell(self) -> None:
        # 'default' gives a dark Shell on GNOME 51; the artboards are light.
        self.assertIn(
            "color-scheme='prefer-light'", settings.override(self.tokens)
        )

    def test_wallpaper_chooser_order(self) -> None:
        root = ElementTree.fromstring(
            settings.background_properties(self.tokens).split("\n", 2)[2]
        )
        names = [entry.findtext("name") for entry in root]
        self.assertEqual(
            names, ["Facets", "Slate", "Sage", "Sand", "Mist", "Ink"]
        )

    def test_solid_wallpapers_are_flat_and_clean(self) -> None:
        files = settings.solid_wallpapers(self.tokens)
        self.assertEqual(len(files), 5)
        self.assertIn('fill="#4d5868"', files["slate.svg"])
        for name, text in files.items():
            with self.subTest(name):
                self.assertEqual(
                    svg.sanitize(text), svg.sanitize(svg.sanitize(text))
                )

    def test_schema_defaults_to_solid(self) -> None:
        root = ElementTree.fromstring(settings.schema().split("\n", 2)[2])
        key = root.find("schema/key[@name='translucent-surfaces']")
        assert key is not None
        self.assertEqual(key.findtext("default"), "false")


if __name__ == "__main__":
    unittest.main()
