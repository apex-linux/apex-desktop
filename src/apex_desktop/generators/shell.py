"""Generates the GNOME Shell stylesheet from the design tokens.

The stylesheet ships inside the Apex Shell extension as
`stylesheet-light.css` and `stylesheet-dark.css`; the Shell loads the one
that matches the colour scheme. Every rule is scoped under `.apex-shell`,
a class the extension puts on the stage's UI group, so it outranks the
stock theme without `!important` and disappears when the extension is off.

Glass surfaces ship solid. The `.apex-glass` class, which the extension
adds when the `translucent-surfaces` setting is on, swaps in the
translucent tints. Live blur behind them waits for OQ-03.

St differs from browser CSS in ways the tokens do not: it draws one box
shadow per element, and has no `color-mix()`. An inset hairline therefore
becomes a 1 px border, and accent mixes become `st-mix()`, which St
evaluates at run time against the user's accent colour.
"""

import dataclasses
import re

from apex_desktop.kernel import color
from apex_desktop.kernel import tokens as tokens_lib

Scheme = tokens_lib.Scheme

ROOT = ".apex-shell"
GLASS = ".apex-glass"

# The shell artboards draw secondary text at .72 instead of the apps' .62
# (OQ-24); this artboard is the one about the top bar and dock.
SHELL_ARTBOARD = "Desktop.dc.html"

ACCENT = "-st-accent-color"
ACCENT_FG = "-st-accent-fg-color"

_MIX = re.compile(
    r"^color-mix\(in srgb, var\(--accent\) (\d+)%,"
    r" (#[0-9a-fA-F]{3,6}|transparent)\)$"
)
_TRANSPARENT = color.Color(0, 0, 0, 0)


@dataclasses.dataclass(frozen=True)
class AccentMix:
    """An accent-derived colour, as a fraction of the accent and a partner.

    St evaluates it per user accent; the tests evaluate it for all nine.
    """

    weight: float
    partner: color.Color

    def st(self) -> str:
        """Returns the St CSS expression."""
        if self.partner == _TRANSPARENT:
            return f"st-transparentize({ACCENT}, {1 - self.weight:.2f})"
        return (
            f"st-mix({ACCENT}, {self.partner.css()}, "
            f"{round(self.weight * 100)}%)"
        )

    def resolve(self, accent: color.Color) -> color.Color:
        """Returns the colour for one accent."""
        return color.mix(accent, self.partner, self.weight)


def derived(tokens: tokens_lib.Tokens, name: str) -> AccentMix:
    """Reads a derived accent such as `--accent-tint` from the tokens."""
    formula = tokens.accent_derived(name)
    match = _MIX.match(formula)
    if match is None:
        raise tokens_lib.TokenError(f"unsupported {name} {formula!r}")
    weight, partner = int(match.group(1)) / 100, match.group(2)
    if partner == "transparent":
        return AccentMix(weight, _TRANSPARENT)
    return AccentMix(weight, color.parse(partner))


def accent_strong(tokens: tokens_lib.Tokens) -> AccentMix:
    """Reads `--accent-strong`, the fill under white text (OQ-31)."""
    return derived(tokens, "--accent-strong")


def focus_ring(tokens: tokens_lib.Tokens, scheme: Scheme) -> AccentMix | None:
    """Returns the focus ring colour: None means the plain accent.

    Light surfaces take `--accent-strong`, because the plain accent misses
    3:1 for Yellow there. Dark surfaces take the plain accent, which misses
    3:1 only for Purple; that case is tracked by OQ-31.
    """
    if scheme is Scheme.LIGHT:
        return accent_strong(tokens)
    return None


def _first_layer(shadow: str) -> str:
    """Returns the first layer of a comma-separated shadow list."""
    depth = 0
    for index, char in enumerate(shadow):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            return shadow[:index].strip()
    return shadow.strip()


def _layers(shadow: str) -> list[str]:
    layers = []
    rest = shadow
    while rest:
        layer = _first_layer(rest)
        layers.append(layer)
        rest = rest[len(layer) :].lstrip(" ,")
    return layers


@dataclasses.dataclass(frozen=True)
class _Palette:  # pylint: disable=too-many-instance-attributes
    """The resolved values for one scheme: one field per colour role."""

    fg: str
    dim: str
    border: str
    btn: str
    btn_h: str
    bar_glass: str
    bar_solid: str
    bar_fg: str
    bar_hover: str
    dock: str
    dock_border: str
    dock_sep: str
    dock_shadow: str
    panel: str
    panel_solid: str
    panel_border: str
    shadow: str
    card: str
    card_border: str
    msg_card: str
    pill: str
    pill_border: str
    running_dot: str
    recording: str
    privacy: str
    pill_ink: str
    accent_strong: str
    focus: str


def _palette(tokens: tokens_lib.Tokens, scheme: Scheme) -> _Palette:
    def role(name: str) -> str:
        return tokens.color(name, scheme).css()

    dock_shadow = [
        layer
        for layer in _layers(tokens.shadow("dock", scheme))
        if not layer.startswith("inset")
    ]
    ring = focus_ring(tokens, scheme)
    return _Palette(
        fg=role("--fg"),
        dim=tokens.color("--dim", scheme, SHELL_ARTBOARD).css(),
        border=role("--border"),
        btn=role("--btn"),
        btn_h=role("--btn-h"),
        bar_glass=role("--bar"),
        bar_solid=role("--bar-solid"),
        bar_fg=role("--bar-fg"),
        bar_hover=role("--bar-hover"),
        dock=role("--dock"),
        dock_border=role("--dock-border"),
        dock_sep=role("--dock-sep"),
        dock_shadow=dock_shadow[0],
        panel=role("--panel"),
        panel_solid=role("--panel-solid"),
        panel_border=role("--panel-border"),
        shadow=_first_layer(tokens.role("--shadow", scheme)),
        card=role("--card"),
        card_border=role("--card-border"),
        msg_card=role("--msg-card"),
        pill=role("--pill"),
        pill_border=role("--pill-border"),
        # The dot is --fg at .7 opacity (Desktop.dc.html:130).
        running_dot=tokens.color("--fg", scheme).with_alpha(0.7).css(),
        recording=role("--recording"),
        privacy=role("--privacy"),
        pill_ink=role("--pill-ink"),
        accent_strong=accent_strong(tokens).st(),
        focus=ACCENT if ring is None else ring.st(),
    )


Rule = tuple[str, dict[str, str]]


def _scope(selector: str) -> str:
    parts = [part.strip() for part in selector.split(",")]
    return ",\n".join(
        f"{ROOT}{part}" if part.startswith(GLASS) else f"{ROOT} {part}"
        for part in parts
    )


def _render(rules: list[Rule]) -> str:
    blocks = []
    for selector, declarations in rules:
        body = "".join(
            f"  {name}: {value};\n" for name, value in declarations.items()
        )
        blocks.append(f"{_scope(selector)} {{\n{body}}}\n")
    return "\n".join(blocks)


def _type(tokens: tokens_lib.Tokens, size: str, weight: str) -> dict[str, str]:
    return {
        "font-size": tokens.font_size(size),
        "font-weight": str(tokens.font_weight(weight)),
    }


def _focus(p: _Palette) -> dict[str, str]:
    return {"box-shadow": f"inset 0 0 0 2px {p.focus}"}


def _top_bar(t: tokens_lib.Tokens, p: _Palette) -> list[Rule]:
    pill = t.radius("pill-bar")
    height = t.fixed("topBarHeight")
    button = t.fixed("topBarButtonHeight")
    inset = f"{(int(height[:-2]) - int(button[:-2])) // 2}px"
    return [
        (
            "#panel",
            {
                "height": height,
                "padding": t.fixed("topBarPadding"),
                "background-color": p.bar_solid,
                "color": p.bar_fg,
                "box-shadow": "none",
                "transition-duration": t.duration("slow"),
                **_type(t, "ui", "semibold"),
            },
        ),
        (
            "#panel .panel-button, #panel .panel-button.clock-display",
            {
                "border": f"{inset} solid transparent",
                "border-radius": "999px",
                "color": p.bar_fg,
                "font-weight": str(t.font_weight("semibold")),
                "transition-duration": t.duration("fast"),
            },
        ),
        (
            "#panel .panel-button:hover, #panel .panel-button:focus",
            {"box-shadow": f"inset 0 0 0 100px {p.bar_hover}"},
        ),
        (
            "#panel .panel-button:active, #panel .panel-button:checked",
            {"box-shadow": f"inset 0 0 0 100px {p.btn_h}"},
        ),
        (
            "#panel .panel-button.clock-display .clock",
            {"border-radius": pill, "border": "0"},
        ),
        (
            "#panel .panel-button.clock-display:hover .clock,"
            " #panel .panel-button.clock-display:focus .clock,"
            " #panel .panel-button.clock-display:active .clock,"
            " #panel .panel-button.clock-display:checked .clock",
            {"box-shadow": "none"},
        ),
        (
            "#panel .panel-button.clock-display",
            {"font-weight": str(t.font_weight("bold"))},
        ),
        (
            "#panel .panel-button#panelActivities .workspace-dot",
            {
                "min-width": "7px",
                "min-height": "7px",
                "border-radius": t.radius("xs"),
                "background-color": p.bar_fg,
            },
        ),
        (
            "#panel .panel-button .system-status-icon",
            {"icon-size": "16px"},
        ),
        # The stock theme paints these pills with an inset shadow inside the
        # transparent border; so does this one, in every state.
        (
            "#panel .panel-button.screen-recording-indicator,"
            " #panel .panel-button.screen-recording-indicator:hover,"
            " #panel .panel-button.screen-recording-indicator:focus,"
            " #panel .panel-button.screen-recording-indicator:active",
            {
                "background-color": "transparent",
                "box-shadow": f"inset 0 0 0 100px {p.recording}",
                "color": p.pill_ink,
                **_type(t, "small-plus", "bold"),
            },
        ),
        (
            "#panel .panel-button.screen-sharing-indicator,"
            " #panel .panel-button.screen-sharing-indicator:hover,"
            " #panel .panel-button.screen-sharing-indicator:focus,"
            " #panel .panel-button.screen-sharing-indicator:active",
            {
                "background-color": "transparent",
                "box-shadow": f"inset 0 0 0 100px {p.privacy}",
                "color": p.pill_ink,
            },
        ),
        (f"{GLASS} #panel", {"background-color": p.bar_glass}),
    ]


def _menus(t: tokens_lib.Tokens, p: _Palette) -> list[Rule]:
    return [
        (".popup-menu-boxpointer", {"-arrow-base": "0", "-arrow-rise": "6px"}),
        (
            ".popup-menu-content",
            {
                "padding": "6px",
                "background-color": p.panel_solid,
                "color": p.fg,
                "border-radius": t.radius("window"),
                "border": f"1px solid {p.panel_border}",
                "box-shadow": p.shadow,
            },
        ),
        (
            ".popup-menu-item",
            {
                "min-height": "34px",
                "padding": "0 12px",
                "spacing": "10px",
                "border-radius": "9px",
                **_type(t, "ui", "medium"),
            },
        ),
        (
            ".popup-menu-item:hover, .popup-menu-item:focus",
            {"background-color": p.btn_h, "color": p.fg},
        ),
        (
            ".popup-separator-menu-item .popup-separator-menu-item-separator",
            {"background-color": p.border, "margin": "5px 10px"},
        ),
        (
            ".toggle-switch",
            {"width": "46px", "background": p.btn_h},
        ),
        (
            ".toggle-switch .handle",
            {"margin": "2px", "width": "22px", "height": "22px"},
        ),
        (".toggle-switch:checked", {"background": ACCENT}),
    ]


def _quick_settings(t: tokens_lib.Tokens, p: _Palette) -> list[Rule]:
    return [
        (
            ".quick-settings",
            {"padding": "14px", "border-radius": t.radius("panel")},
        ),
        (
            ".quick-settings-grid",
            {"spacing-rows": "10px", "spacing-columns": "10px"},
        ),
        (
            ".quick-toggle, .quick-toggle-has-menu",
            {"min-height": "54px", "border-radius": "999px"},
        ),
        (
            ".quick-toggle, .quick-toggle-has-menu .quick-toggle-menu-button",
            {"background-color": p.btn, "color": p.fg},
        ),
        (
            ".quick-toggle:hover,"
            " .quick-toggle-has-menu .quick-toggle-menu-button:hover",
            {"background-color": p.btn_h},
        ),
        (
            ".quick-toggle:checked,"
            " .quick-toggle-has-menu .quick-toggle-menu-button:checked",
            {"background-color": p.accent_strong, "color": ACCENT_FG},
        ),
        (".quick-toggle:focus", _focus(p)),
        (".quick-toggle .quick-toggle-title", _type(t, "body", "bold")),
        (
            ".quick-toggle .quick-toggle-subtitle",
            {"font-size": t.font_size("caption")},
        ),
        (
            ".quick-settings .icon-button",
            {"padding": "10px", "background-color": p.btn, "color": p.fg},
        ),
        (
            ".slider",
            {
                "-barlevel-height": "6px",
                "-barlevel-background-color": p.btn_h,
                "-barlevel-active-background-color": ACCENT,
                "-slider-handle-radius": "10px",
            },
        ),
        (
            ".quick-toggle-menu",
            {
                "border-radius": t.radius("card-lg"),
                "background-color": p.card,
                "border": f"1px solid {p.card_border}",
                "color": p.fg,
            },
        ),
        (
            ".quick-toggle-menu .header .icon.active",
            {"background-color": ACCENT},
        ),
    ]


def _calendar(t: tokens_lib.Tokens, p: _Palette) -> list[Rule]:
    card = t.radius("card-lg")
    return [
        (".datemenu-popover", {"border-radius": t.radius("panel")}),
        (
            ".message",
            {
                "border-radius": card,
                "background-color": p.msg_card,
                "border": f"1px solid {p.card_border}",
                "color": p.fg,
                "box-shadow": "none",
            },
        ),
        (".message .message-header", {"color": p.dim}),
        (".message .message-title", _type(t, "ui", "bold")),
        (
            ".calendar",
            {
                "border-radius": card,
                "background-color": p.card,
                "border": f"1px solid {p.card_border}",
                "color": p.fg,
            },
        ),
        (
            ".calendar .calendar-day",
            {"border-radius": card, "font-size": t.font_size("body")},
        ),
        (
            ".calendar .calendar-day.calendar-today",
            {
                "background-color": p.accent_strong,
                "color": ACCENT_FG,
                "font-weight": str(t.font_weight("bold")),
            },
        ),
        (
            ".events-button, .world-clocks-button, .weather-button",
            {
                "border-radius": t.radius("window"),
                "background-color": p.card,
                "border": f"1px solid {p.card_border}",
                "color": p.fg,
            },
        ),
        (
            ".message-list-controls .message-list-clear-button",
            {"background-color": p.btn, "color": p.fg},
        ),
    ]


def _transients(t: tokens_lib.Tokens, p: _Palette) -> list[Rule]:
    panel = {
        "background-color": p.panel_solid,
        "color": p.fg,
        "border": f"1px solid {p.panel_border}",
        "box-shadow": p.shadow,
    }
    return [
        (
            ".notification-banner",
            {"width": "460px", "border-radius": t.radius("lg"), **panel},
        ),
        (
            ".osd-window",
            {
                "border-radius": t.radius("toast"),
                "padding": "0 18px",
                "min-height": "40px",
                "spacing": "12px",
                **_type(t, "ui", "semibold"),
                **panel,
            },
        ),
        (".osd-window StIcon", {"icon-size": "16px"}),
        (
            ".osd-window .level",
            {
                "min-width": "180px",
                "-barlevel-height": "6px",
                "-barlevel-background-color": p.btn_h,
                "-barlevel-active-background-color": ACCENT,
            },
        ),
        (
            ".switcher-list",
            {"padding": "14px", "border-radius": t.radius("panel"), **panel},
        ),
        (
            ".switcher-list .item-box",
            {"border-radius": t.radius("lg"), "color": p.fg},
        ),
        (
            ".switcher-list .item-box:selected,"
            " .switcher-list .item-box:highlighted",
            {"background-color": p.btn_h, "color": p.fg},
        ),
        (
            ".dash-label",
            {
                "border-radius": "13px",
                "padding": "4px 10px",
                **_type(t, "small-plus", "semibold"),
                **panel,
            },
        ),
        (
            ".tile-preview, .tile-preview.tile-preview-left.on-primary,"
            " .tile-preview.tile-preview-right.on-primary,"
            " .tile-preview.tile-preview-left.tile-preview-right.on-primary",
            {
                "background-color": derived(t, "--accent-tint").st(),
                "border": f"2px solid {derived(t, '--accent-ring').st()}",
                "border-radius": t.radius("window"),
            },
        ),
        (
            f"{GLASS} .notification-banner, {GLASS} .osd-window,"
            f" {GLASS} .switcher-list",
            {"background-color": p.panel},
        ),
    ]


def _dialogs(t: tokens_lib.Tokens, p: _Palette) -> list[Rule]:
    return [
        (
            ".modal-dialog",
            {
                "background-color": p.panel_solid,
                "color": p.fg,
                "border-radius": t.radius("panel"),
                "border": f"1px solid {p.panel_border}",
                "box-shadow": p.shadow,
                "padding": "28px 28px 22px",
                "spacing": "18px",
            },
        ),
        (
            ".modal-dialog .message-dialog-title",
            {"letter-spacing": "-0.2px", **_type(t, "title-3", "bold")},
        ),
        (
            ".modal-dialog .message-dialog-description",
            {"color": p.dim, "font-size": t.font_size("ui")},
        ),
        (
            ".modal-dialog .modal-dialog-button-box .modal-dialog-button",
            {
                "min-height": "36px",
                "padding": "0 12px",
                "border-radius": t.radius("card-lg"),
                "background-color": p.btn,
                "color": p.fg,
                **_type(t, "body", "semibold"),
            },
        ),
        (
            ".modal-dialog .modal-dialog-button-box .modal-dialog-button:hover",
            {"background-color": p.btn_h},
        ),
        (
            ".modal-dialog .modal-dialog-button-box .modal-dialog-button:focus",
            _focus(p),
        ),
        (
            ".modal-dialog .modal-dialog-button-box"
            " .modal-dialog-button.default",
            {"background-color": p.accent_strong, "color": ACCENT_FG},
        ),
    ]


def _dock(t: tokens_lib.Tokens, p: _Palette) -> list[Rule]:
    return [
        (
            "#apexDock .dash-background",
            {
                "background-color": p.panel_solid,
                "border": f"1px solid {p.dock_border}",
                "border-radius": t.radius("dock"),
                "box-shadow": p.dock_shadow,
                "padding": t.fixed("dockPadding"),
            },
        ),
        (
            "#apexDock .dash-separator",
            {
                "width": "1px",
                "height": "40px",
                "margin": "0 4px 8px",
                "background-color": p.dock_sep,
            },
        ),
        (
            "#apexDock .app-grid-running-dot",
            {
                "width": "4px",
                "height": "4px",
                "border-radius": "2px",
                "background-color": p.running_dot,
            },
        ),
        (f"{GLASS} #apexDock .dash-background", {"background-color": p.dock}),
    ]


def _overview(t: tokens_lib.Tokens, p: _Palette) -> list[Rule]:
    return [
        (
            ".search-entry",
            {
                "border-radius": "999px",
                "background-color": p.pill,
                "border": f"1px solid {p.pill_border}",
                "color": p.fg,
            },
        ),
        (".search-entry:focus", _focus(p)),
        (
            ".unlock-dialog-clock-time",
            {
                "font-size": t.font_size("display-1"),
                "font-weight": str(t.font_weight("heavy")),
                "letter-spacing": "-4px",
            },
        ),
        (
            ".unlock-dialog-clock-date",
            {"font-size": t.font_size("title-2")},
        ),
    ]


def stylesheet(tokens: tokens_lib.Tokens, scheme: Scheme) -> str:
    """Returns the Shell stylesheet for one colour scheme."""
    p = _palette(tokens, scheme)
    features = tokens.font_features().replace("'", '"')
    root = f"{ROOT} {{\n  font-feature-settings: {features};\n}}\n"
    rules = (
        _top_bar(tokens, p)
        + _menus(tokens, p)
        + _quick_settings(tokens, p)
        + _calendar(tokens, p)
        + _transients(tokens, p)
        + _dialogs(tokens, p)
        + _dock(tokens, p)
        + _overview(tokens, p)
    )
    header = (
        "/* Generated by apex_desktop.generators.shell from"
        f" design/system/tokens.json ({scheme.value}). Do not edit. */\n\n"
    )
    return header + root + "\n" + _render(rules)
