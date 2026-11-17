"""Tests that the imported design sources are safe to publish and build."""

import json
import pathlib
import re
import unittest

from apex_desktop.kernel import svg

_DESIGN = pathlib.Path(__file__).resolve().parent.parent / "design"
_ASSETS = _DESIGN / "canvas" / "assets"


class DesignTest(unittest.TestCase):

    def test_tokens_parse(self) -> None:
        tokens = json.loads(
            (_DESIGN / "system" / "tokens.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(tokens["accent"]["options"]), 9)

    def test_shipped_assets_are_sanitised(self) -> None:
        shipped = sorted(_ASSETS.glob("*.svg"))
        self.assertEqual(
            [path.name for path in shipped],
            ["facets-dark.svg", "facets-light.svg"],
        )
        for path in shipped:
            with self.subTest(path.name):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(svg.sanitize(text), text)

    def test_no_private_canvas_address(self) -> None:
        pattern = re.compile(r"claude\.ai/artifact/")
        for path in _DESIGN.rglob("*"):
            if path.is_file():
                with self.subTest(str(path.relative_to(_DESIGN))):
                    text = path.read_text(encoding="utf-8")
                    self.assertIsNone(pattern.search(text))


if __name__ == "__main__":
    unittest.main()
