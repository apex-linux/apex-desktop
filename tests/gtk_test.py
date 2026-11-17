"""Tests the libadwaita style sheet generator."""

import pathlib
import unittest

from apex_desktop.generators import gtk
from apex_desktop.kernel import color
from apex_desktop.kernel import tokens as tokens_lib

Scheme = tokens_lib.Scheme

_TOKENS = pathlib.Path(__file__).resolve().parent.parent / (
    "design/system/tokens.json"
)


class GtkTest(unittest.TestCase):

    def setUp(self) -> None:
        self.tokens = tokens_lib.Tokens.load(_TOKENS)
        self.css = gtk.stylesheet(self.tokens)

    def test_both_schemes(self) -> None:
        light, dark = self.css.split("@media (prefers-color-scheme: dark)")
        self.assertIn("--window-bg-color: #fafafb;", light)
        self.assertIn("--window-bg-color: #242428;", dark)

    def test_window_radius_and_features(self) -> None:
        self.assertIn("--window-radius: 14px;", self.css)
        self.assertIn('font-feature-settings: "cv05", "ss03";', self.css)

    def test_app_text_contrast(self) -> None:
        # system/README.md: --fg and --dim pass 4.5:1 on --win and --side.
        for scheme in Scheme:
            for surface in ("--win", "--side"):
                bg = self.tokens.color(surface, scheme)
                for role in ("--fg", "--dim"):
                    with self.subTest(f"{scheme.value} {role} on {surface}"):
                        ratio = color.contrast(
                            self.tokens.color(role, scheme), bg
                        )
                        self.assertGreaterEqual(ratio, 4.5)


if __name__ == "__main__":
    unittest.main()
