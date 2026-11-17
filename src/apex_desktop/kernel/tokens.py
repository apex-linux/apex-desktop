"""Reads values from the design tokens in `design/system/tokens.json`.

The generator never writes a colour, size or radius of its own: every value
comes through this module, so tokens.json stays the single source.
"""

import dataclasses
import enum
import json
import pathlib
import re
from typing import Any

from apex_desktop.kernel import color as colors

_VAR = re.compile(r"var\((--[a-z0-9-]+)\)")


class Scheme(enum.Enum):
    """The two colour schemes every role has a value for."""

    LIGHT = "light"
    DARK = "dark"


class TokenError(KeyError):
    """Raised when the generator asks for a token tokens.json lacks."""


@dataclasses.dataclass(frozen=True)
class Accent:
    """One of the nine accent colours."""

    name: str
    label: str
    color: colors.Color


class Tokens:
    """Typed access to the parsed tokens.json document."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data
        self._roles: dict[str, dict[str, Any]] = {}
        for group in data["color"].values():
            for role, entry in group.items():
                self._roles[role] = entry

    @classmethod
    def load(cls, path: pathlib.Path) -> "Tokens":
        """Reads a tokens.json file."""
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def role(
        self, name: str, scheme: Scheme, artboard: str | None = None
    ) -> str:
        """Returns a colour role's value as the tokens write it.

        Args:
            name: the role, for example `--panel-solid`.
            scheme: light or dark.
            artboard: when given and that artboard draws a conflicting
                value, return the artboard's value instead of the majority.
                The shell uses this to take the values the shell artboards
                draw, as OQ-24 records for `--dim`.

        Raises:
            TokenError: no such role.
        """
        try:
            entry = self._roles[name][scheme.value]
        except KeyError as error:
            raise TokenError(f"no colour role {name} ({scheme.value})") from (
                error
            )
        if artboard is not None:
            for conflict in entry.get("conflicts", []):
                if artboard in conflict["sources"]:
                    return str(conflict["value"])
        return str(entry["value"])

    def color(
        self, name: str, scheme: Scheme, artboard: str | None = None
    ) -> colors.Color:
        """Returns a colour role parsed into a colour."""
        return colors.parse(self.role(name, scheme, artboard))

    def resolve(self, text: str, scheme: Scheme) -> str:
        """Replaces every `var(--role)` in a token value with its value."""
        for _ in range(4):
            replaced = _VAR.sub(lambda m: self.role(m.group(1), scheme), text)
            if replaced == text:
                return replaced
            text = replaced
        raise TokenError(f"var() nesting too deep in {text!r}")

    def accents(self) -> list[Accent]:
        """Returns the nine accents in picker order."""
        return [
            Accent(
                option["name"], option["label"], colors.parse(option["value"])
            )
            for option in self._data["accent"]["options"]
        ]

    def accent_derived(self, name: str) -> str:
        """Returns a derived accent formula, for example `--accent-strong`."""
        try:
            return str(self._data["accent"]["derived"][name]["value"])
        except KeyError as error:
            raise TokenError(f"no derived accent {name}") from error

    def default_accent(self) -> str:
        """Returns the name of the default accent."""
        return str(self._data["accent"]["default"])

    def radius(self, name: str) -> str:
        """Returns a radius token, for example `26px`."""
        return self._lookup("radius", name)

    def font_size(self, name: str) -> str:
        """Returns a type size token, for example `13.5px`."""
        return self._lookup("typography", "size", name)

    def font_weight(self, name: str) -> int:
        """Returns a weight token, for example 600."""
        return int(self._lookup("typography", "weight", name))

    def font_family(self, name: str) -> list[str]:
        """Returns a font stack, for example the `ui` stack."""
        stack = self._data["typography"]["family"][name]["stack"]
        return [str(family) for family in stack]

    def font_features(self) -> str:
        """Returns the UI font features, for example `'cv05', 'ss03'`."""
        return self._lookup("typography", "features", "ui")

    def fixed(self, name: str) -> Any:
        """Returns a fixed size from `spacing.fixed`."""
        return self._data["spacing"]["fixed"][name]["value"]

    def shadow(self, name: str, scheme: Scheme) -> str:
        """Returns a shadow token with its `var()` references resolved."""
        return self.resolve(self._lookup("shadow", name), scheme)

    def solid_wallpapers(self) -> list[tuple[str, str, colors.Color]]:
        """Returns the solid wallpapers as (name, label, colour), in order."""
        try:
            solids = self._data["wallpaper"]["solid"]
        except KeyError as error:
            raise TokenError("no wallpaper.solid") from error
        return [
            (name, str(entry["label"]), colors.parse(entry["value"]))
            for name, entry in solids.items()
        ]

    def duration(self, name: str) -> str:
        """Returns a motion duration, for example `150ms`."""
        return self._lookup("motion", "duration", name)

    def _lookup(self, *path: str) -> str:
        node: Any = self._data
        try:
            for key in path:
                node = node[key]
            return str(node["value"])
        except (KeyError, TypeError) as error:
            raise TokenError("no token " + ".".join(path)) from error
