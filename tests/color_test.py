"""Tests the colour maths the generator and the contrast checks share."""

import unittest

from apex_desktop.kernel import color


class ParseTest(unittest.TestCase):

    def test_parses_token_forms(self) -> None:
        self.assertEqual(color.parse("#fff"), color.Color(255, 255, 255))
        self.assertEqual(color.parse("#3584e4"), color.Color(53, 132, 228))
        self.assertEqual(
            color.parse("rgba(0,0,10,.09)"), color.Color(0, 0, 10, 0.09)
        )
        self.assertEqual(color.parse("rgb(1, 2, 3)"), color.Color(1, 2, 3))

    def test_rejects_other_forms(self) -> None:
        for text in ("blue", "#12345", "hsl(0, 0%, 0%)", ""):
            with self.subTest(text):
                with self.assertRaises(color.ColorError):
                    color.parse(text)

    def test_css_round_trips(self) -> None:
        self.assertEqual(color.parse("#3584e4").css(), "#3584e4")
        self.assertEqual(
            color.parse("rgba(0,0,10,.09)").css(), "rgba(0, 0, 10, 0.09)"
        )


class MixTest(unittest.TestCase):

    def test_matches_css_color_mix(self) -> None:
        # color-mix(in srgb, #3584e4 75%, #000), the canvas's --accent-strong.
        strong = color.mix(color.parse("#3584e4"), color.parse("#000"), 0.75)
        self.assertEqual(strong.css(), "#2863ab")

    def test_weight_bounds(self) -> None:
        with self.assertRaises(color.ColorError):
            color.mix(color.parse("#fff"), color.parse("#000"), 1.5)


class ContrastTest(unittest.TestCase):

    def test_extremes(self) -> None:
        white, black = color.parse("#fff"), color.parse("#000")
        self.assertAlmostEqual(color.contrast(black, white), 21.0)
        self.assertAlmostEqual(color.contrast(white, white), 1.0)

    def test_composites_translucent_text(self) -> None:
        # system/README.md: --dim on --win is 4.67 in light.
        ratio = color.contrast(
            color.parse("rgba(29,29,33,.62)"), color.parse("#fafafb")
        )
        self.assertAlmostEqual(ratio, 4.67, places=2)

    def test_needs_opaque_background(self) -> None:
        with self.assertRaises(color.ColorError):
            color.contrast(color.parse("#000"), color.parse("rgba(0,0,0,.5)"))


if __name__ == "__main__":
    unittest.main()
