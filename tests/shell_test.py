"""Tests the Shell stylesheet generator: tokens in, CSS out."""

import copy
import json
import pathlib
import re
import unittest

from apex_desktop.generators import shell
from apex_desktop.kernel import color
from apex_desktop.kernel import tokens as tokens_lib

Scheme = tokens_lib.Scheme

_TOKENS = pathlib.Path(__file__).resolve().parent.parent / (
    "design/system/tokens.json"
)
_LITERAL = re.compile(r"#[0-9a-fA-F]{3,6}\b|rgba?\([^)]*\)")

# Accent and surface pairs where a 2 px ring misses 3:1. Tracked as OQ-31;
# the test fails if the set changes, so a fix or a regression is noticed.
_KNOWN_RING_FAILURES = {("purple", Scheme.DARK)}


def _data() -> dict[str, object]:
    return dict(json.loads(_TOKENS.read_text(encoding="utf-8")))


def _block(css: str, selector: str) -> dict[str, str]:
    """Returns the declarations of the rule with exactly this selector."""
    body = css.split(f"\n{selector} {{\n", 1)[1].split("\n}", 1)[0]
    return dict(
        line.strip().rstrip(";").split(": ", 1) for line in body.splitlines()
    )


def _rgb(text: str) -> tuple[int, int, int]:
    parsed = color.parse(text)
    return (round(parsed.red), round(parsed.green), round(parsed.blue))


def _token_rgbs(data: object) -> set[tuple[int, int, int]]:
    """Returns the RGB of every colour written anywhere in the tokens."""
    found: set[tuple[int, int, int]] = set()
    text = json.dumps(data)
    for literal in _LITERAL.findall(text):
        try:
            found.add(_rgb(literal))
        except color.ColorError:
            pass
    return found


class StylesheetTest(unittest.TestCase):

    def setUp(self) -> None:
        self.tokens = tokens_lib.Tokens.load(_TOKENS)

    def test_every_colour_comes_from_the_tokens(self) -> None:
        allowed = _token_rgbs(_data())
        for scheme in Scheme:
            css = shell.stylesheet(self.tokens, scheme)
            for literal in _LITERAL.findall(css):
                with self.subTest(scheme=scheme.value, literal=literal):
                    self.assertIn(_rgb(literal), allowed)

    def test_a_token_change_reaches_the_css(self) -> None:
        data = _data()
        changed = copy.deepcopy(data)
        role = changed["color"]["shell"]["--panel-solid"]  # type: ignore
        role["light"]["value"] = "#123456"
        css = shell.stylesheet(tokens_lib.Tokens(changed), Scheme.LIGHT)
        self.assertIn("background-color: #123456;", css)
        self.assertNotIn("#123456", shell.stylesheet(self.tokens, Scheme.LIGHT))

    def test_rules_are_scoped(self) -> None:
        css = shell.stylesheet(self.tokens, Scheme.LIGHT)
        for line in css.splitlines():
            if line.endswith("{") or line.endswith(","):
                with self.subTest(line):
                    self.assertTrue(line.startswith(shell.ROOT), line)

    def test_shell_surfaces_are_solid_unless_glass(self) -> None:
        css = shell.stylesheet(self.tokens, Scheme.DARK)
        solid = self.tokens.color("--bar-solid", Scheme.DARK).css()
        glass = self.tokens.color("--bar", Scheme.DARK).css()
        self.assertIn(".apex-shell #panel {\n  height: 32px;", css)
        self.assertIn(f"background-color: {solid};", css)
        self.assertIn(
            ".apex-shell.apex-glass #panel {\n" f"  background-color: {glass};",
            css,
        )

    def test_extension_actors_are_styled(self) -> None:
        css = shell.stylesheet(self.tokens, Scheme.LIGHT)
        for name in (
            ".apex-activities-diamond",
            ".apex-activities-box",
            ".apex-focus-label",
            ".apex-shell.apex-glass #panel.apex-solid-bar",
            "#apexDock .dash-background",
        ):
            with self.subTest(name):
                self.assertIn(name, css)

    def test_measurements_from_the_top_bar_spec(self) -> None:
        css = shell.stylesheet(self.tokens, Scheme.LIGHT)
        # 32 px bar with 24 px buttons leaves a 4 px border on each side.
        self.assertIn("border: 4px solid transparent;", css)
        self.assertIn("padding: 0 8px;", css)
        self.assertIn("font-size: 13.5px;", css)

    def test_dock_height_matches_the_spec(self) -> None:
        # shell-top-bar-and-dock.md: height is icon + 16, 70 px at medium,
        # 10 px above the edge with no stock margin under the background.
        css = shell.stylesheet(self.tokens, Scheme.LIGHT)
        background = _block(css, ".apex-shell #apexDock .dash-background")
        top, _, bottom = (
            int(v.removesuffix("px")) for v in background["padding"].split()
        )
        border = 2 * shell.DOCK_BORDER
        self.assertEqual(top + 54 + bottom + border, 70)
        self.assertEqual(background["margin-bottom"], "0")
        tile = _block(
            css,
            ".apex-shell #apexDock .dash-item-container .overview-tile,\n"
            ".apex-shell #apexDock .dash-item-container .show-apps",
        )
        tile_top, _, tile_bottom = (
            int(v.removesuffix("px")) for v in tile["padding"].split()
        )
        self.assertEqual(tile_top + 54 + tile_bottom, 70)
        self.assertEqual(tile_top, 5)

    def test_dock_glyphs_take_the_dock_ink(self) -> None:
        for scheme in Scheme:
            with self.subTest(scheme.name):
                css = shell.stylesheet(self.tokens, scheme)
                fg = self.tokens.role("--fg", scheme)
                self.assertIn(
                    "#apexDock .dash-item-container .show-apps:hover"
                    " .overview-icon",
                    css,
                )
                self.assertIn(f"color: {color.parse(fg).css()};", css)

    def test_calendar_days_have_no_fill(self) -> None:
        css = shell.stylesheet(self.tokens, Scheme.LIGHT)
        self.assertIn(
            ".apex-shell .calendar .calendar-day,\n"
            ".apex-shell .calendar .calendar-day-heading,\n",
            css,
        )
        selected = _block(css, ".apex-shell .calendar .calendar-day:selected")
        self.assertEqual(selected["background-color"], "transparent")
        self.assertEqual(
            selected["box-shadow"], "inset 0 0 0 2px -st-accent-color"
        )

    def test_out_of_month_days_keep_the_date_menu_faint(self) -> None:
        css = shell.stylesheet(self.tokens, Scheme.LIGHT)
        other = _block(
            css, ".apex-shell .calendar .calendar-day.calendar-other-month"
        )
        self.assertEqual(other["color"], "rgba(29, 29, 33, 0.64)")
        today = _block(
            css, ".apex-shell .calendar .calendar-day.calendar-today"
        )
        self.assertEqual(today["box-shadow"], "none")

    def test_accent_strong_comes_from_the_derived_token(self) -> None:
        strong = shell.accent_strong(self.tokens)
        self.assertEqual(strong.st(), "st-mix(-st-accent-color, #000000, 75%)")
        self.assertIn(strong.st(), shell.stylesheet(self.tokens, Scheme.LIGHT))


class ContrastRulesTest(unittest.TestCase):
    """The contrast rules in system/README.md and the shell specs."""

    def setUp(self) -> None:
        self.tokens = tokens_lib.Tokens.load(_TOKENS)

    def _ratio(self, fg: color.Color, bg: color.Color) -> float:
        return color.contrast(fg, bg)

    def test_text_on_solid_shell_surfaces(self) -> None:
        for scheme in Scheme:
            panel = self.tokens.color("--panel-solid", scheme)
            solid_bar = self.tokens.color("--bar-solid", scheme)
            dim = self.tokens.color("--dim", scheme, shell.SHELL_ARTBOARD)
            pairs = {
                "fg on panel": (self.tokens.color("--fg", scheme), panel),
                "dim on panel": (dim, panel),
                "bar-fg on bar": (
                    self.tokens.color("--bar-fg", scheme),
                    solid_bar,
                ),
            }
            for name, (fg, bg) in pairs.items():
                with self.subTest(scheme=scheme.value, pair=name):
                    self.assertGreaterEqual(self._ratio(fg, bg), 4.5)

    def test_indicator_pills(self) -> None:
        # shell-top-bar-and-dock.md: pill ink reaches 4.5:1 in both themes.
        for scheme in Scheme:
            ink = self.tokens.color("--pill-ink", scheme)
            for fill in ("--recording", "--privacy"):
                with self.subTest(f"{scheme.value} {fill}"):
                    bg = self.tokens.color(fill, scheme)
                    self.assertGreaterEqual(self._ratio(ink, bg), 4.5)

    def test_white_text_on_accent_fills(self) -> None:
        # Rule 3 and OQ-31: small white text sits on --accent-strong.
        white = color.parse("#ffffff")
        strong = shell.accent_strong(self.tokens)
        for accent in self.tokens.accents():
            with self.subTest(accent.name):
                fill = strong.resolve(accent.color)
                self.assertGreaterEqual(self._ratio(white, fill), 4.5)

    def test_focus_rings_reach_three_to_one(self) -> None:
        failures = set()
        for scheme in Scheme:
            panel = self.tokens.color("--panel-solid", scheme)
            ring = shell.focus_ring(self.tokens, scheme)
            for accent in self.tokens.accents():
                shown = (
                    accent.color if ring is None else ring.resolve(accent.color)
                )
                if self._ratio(shown, panel) < 3.0:
                    failures.add((accent.name, scheme))
        self.assertEqual(failures, _KNOWN_RING_FAILURES)


if __name__ == "__main__":
    unittest.main()
