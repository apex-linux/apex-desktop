"""Colours as the design tokens write them, and the WCAG contrast maths.

The tokens use `#rrggbb` and `rgba(r,g,b,a)`. Everything here is pure, so
the generator and the tests share one implementation of mixing,
compositing and contrast.
"""

import dataclasses
import re

_HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
_RGBA = re.compile(
    r"^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)"
    r"\s*(?:,\s*([\d.]+)\s*)?\)$"
)


class ColorError(ValueError):
    """Raised when a string is not a colour the tokens can contain."""


@dataclasses.dataclass(frozen=True)
class Color:
    """An sRGB colour with channels from 0 to 255 and alpha from 0 to 1."""

    red: float
    green: float
    blue: float
    alpha: float = 1.0

    def css(self) -> str:
        """Returns the colour as `#rrggbb`, or `rgba()` when translucent."""
        channels = [round(c) for c in (self.red, self.green, self.blue)]
        if self.alpha >= 1.0:
            return "#" + "".join(f"{c:02x}" for c in channels)
        alpha = f"{self.alpha:.3f}".rstrip("0").rstrip(".")
        red, green, blue = channels
        return f"rgba({red}, {green}, {blue}, {alpha})"

    def with_alpha(self, alpha: float) -> "Color":
        """Returns the same colour at another alpha."""
        return dataclasses.replace(self, alpha=alpha)

    def over(self, background: "Color") -> "Color":
        """Composites this colour over an opaque background."""
        if background.alpha < 1.0:
            raise ColorError("the background of a composite must be opaque")
        a = self.alpha
        return Color(
            self.red * a + background.red * (1 - a),
            self.green * a + background.green * (1 - a),
            self.blue * a + background.blue * (1 - a),
        )


def parse(text: str) -> Color:
    """Parses `#rgb`, `#rrggbb`, `rgb()` or `rgba()`.

    Args:
        text: the colour as the tokens write it.

    Returns:
        The colour.

    Raises:
        ColorError: text is not one of those forms.
    """
    text = text.strip()
    if match := _HEX.match(text):
        digits = match.group(1)
        if len(digits) == 3:
            digits = "".join(d * 2 for d in digits)
        return Color(
            int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)
        )
    if match := _RGBA.match(text):
        red, green, blue, alpha = match.groups()
        return Color(
            float(red),
            float(green),
            float(blue),
            1.0 if alpha is None else float(alpha),
        )
    raise ColorError(f"not a colour: {text!r}")


def mix(first: Color, second: Color, weight: float) -> Color:
    """Mixes two colours like CSS `color-mix(in srgb, first weight, second)`.

    It is also what GNOME Shell's `st-mix(first, second, weight)` computes.

    Args:
        first: the colour that gets `weight`.
        second: the colour that gets `1 - weight`.
        weight: from 0 to 1.

    Returns:
        The mixed colour, with mixed alpha.
    """
    if not 0.0 <= weight <= 1.0:
        raise ColorError(f"mix weight out of range: {weight}")
    alpha = first.alpha * weight + second.alpha * (1 - weight)
    if alpha == 0:
        return Color(0, 0, 0, 0)

    def channel(a: float, b: float) -> float:
        premultiplied = a * first.alpha * weight + b * second.alpha * (
            1 - weight
        )
        return premultiplied / alpha

    return Color(
        channel(first.red, second.red),
        channel(first.green, second.green),
        channel(first.blue, second.blue),
        alpha,
    )


def _linear(channel: float) -> float:
    value = channel / 255
    if value <= 0.04045:
        return value / 12.92
    return float(((value + 0.055) / 1.055) ** 2.4)


def luminance(color: Color) -> float:
    """Returns the WCAG relative luminance of an opaque colour."""
    if color.alpha < 1.0:
        raise ColorError("luminance needs an opaque colour; composite first")
    return (
        0.2126 * _linear(color.red)
        + 0.7152 * _linear(color.green)
        + 0.0722 * _linear(color.blue)
    )


def contrast(foreground: Color, background: Color) -> float:
    """Returns the WCAG 2 contrast ratio of foreground on background.

    A translucent foreground is composited over the background first, as it
    renders. The background must be opaque.
    """
    if foreground.alpha < 1.0:
        foreground = foreground.over(background)
    lighter, darker = sorted(
        (luminance(foreground), luminance(background)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)
