# Shell: window switcher and edge tiling

## Summary

Two window-management surfaces:

*   **15 Window switcher** (`AltTab.dc.html`): the Alt+Tab popup, a glass
    panel of app icons centred on the screen over a Text Editor window. It has
    no `scene` tweak; `dark` defaults to `true` and the selected index starts
    at 1 (Terminal). Clicking an icon selects it.
*   **22 Edge tiling** (`Tiling.dc.html`): a Files window being dragged, with
    a Terminal already tiled to the right half and an accent preview of where
    Files will land. Tweak `target`: `left half` (default) or `maximize`.

The Text Editor window behind the switcher shows SPEC.md section 2.6
"Glass" (`AltTab.dc.html:117-142`). Its values are already recorded in
tokens.json under `glass`; this spec does not cover the editor or its
content.

## Upstream mapping

| Element | Upstream component | Confidence |
| --- | --- | --- |
| Switcher popup | GNOME Shell `js/ui/altTab.js` `AppSwitcherPopup`, built on `js/ui/switcherPopup.js` `SwitcherPopup` and `SwitcherList` | High |
| Switcher items | `altTab.js` `AppIcon` inside `AppSwitcher` | High |
| Per-app window list (Alt+\` or arrow down) | `altTab.js` `ThumbnailSwitcher` | High (not drawn) |
| Edge tiling behaviour | Mutter edge tiling (`org.gnome.mutter edge-tiling`), half-tile and maximise on drag | High |
| Tile preview | GNOME Shell `js/ui/windowManager.js` `TilePreview` (style class `tile-preview`), shown on Mutter's `show-tile-preview` request | High |
| Tiled window look (square, no shadow) | Mutter tiled state plus libadwaita's tiled window styling | High |

## Layout and measurements

All values are logical px on the 1440x900 artboard (device px = 2x).

### Window switcher

| Property | Value | Source |
| --- | --- | --- |
| Position | Centred on the monitor (`left:50%; top:50%; translate(-50%,-50%)`), `z-index:30` | `AltTab.dc.html:77` |
| Box | Column, `align-items:center`, `gap:10px`, padding 14, radius 26 (`panel`) | same |
| Glass | `--panel` fill, `blur(30px) saturate(180%)` | same |
| Shadow | `panel`: `var(--shadow), inset 0 0 0 1px var(--panel-border)` | same |
| Icon row | Row, `gap:6px` | `AltTab.dc.html:78` |
| Item | 120x116, radius 16 (`lg`), column, centred, `gap:8px`; selected fill `--btn-h`, others transparent | `AltTab.dc.html:111` |
| Icon | 84x84 full-colour app icon | `AltTab.dc.html:81` |
| Window dots | Row 4 tall, `gap:4px`; one 4x4 radius-2 `--fg` dot at opacity .7 per open window | `AltTab.dc.html:82` |
| Caption | One label under the row: selected app's name, 13.5px/600, `padding-bottom:2px` | `AltTab.dc.html:86` |

Derived size with five apps: 652 px wide (5 x 120 + 4 x 6 + 2 x 14) and
about 172 px tall (14 + 116 + 10 + caption 18 + 14). The caption height
depends on Inter's line height at 13.5 px.

Drawn list, in most-recently-used order (`AltTab.dc.html:97-103`):

| Index | App | Windows |
| --- | --- | --- |
| 0 | Text Editor | 1 |
| 1 (selected) | Terminal | 2 |
| 2 | Web | 1 |
| 3 | Files | 1 |
| 4 | Settings | 1 |

The bar behind it reads "Text Editor" (focused app) and "Sun Oct 11"
"14:26" with no unread dot. The dock shows running dots for Files, Web, Text
Editor, Terminal and Settings, matching the switcher list.

### Edge tiling

#### Tile preview

| Property | Left half | Maximize | Source |
| --- | --- | --- | --- |
| Rect | x 6, y 38, 708x856 | x 6, y 38, 1428x856 | `Tiling.dc.html:129` |
| Inset | 6 px inside the work area on every side; for the half, 6 px short of the centre line (right edge at 714) | 6 px inside the work area | derived |
| Radius | 14 on all four corners | same | same |
| Fill | `color-mix(in srgb, var(--accent) 16%, transparent)` | same | `Tiling.dc.html:130` |
| Ring | `inset 0 0 0 2px color-mix(in srgb, var(--accent) 70%, transparent)` | same | `Tiling.dc.html:132` |
| Glass | `blur(20px) saturate(160%)` behind the fill | same | `Tiling.dc.html:131` |
| Motion | `transition: width .3s cubic-bezier(.2,.8,.2,1)` (`standard`, `slow`) | same | `Tiling.dc.html:133` |
| Stacking | Above tiled windows, below the dragged window (`z-index:4` vs 5) | same | |

The work area here is the monitor minus the 32 px top bar; the dock is not
drawn and reserves nothing.

#### Windows in the scene

| Window | Left half | Maximize |
| --- | --- | --- |
| Files, being dragged | 660x480 at x -120, y 250 (partly off the left edge); radius 14, `--win`, shadow `window` | 660x480 at x 400, y 32 |
| Pointer (22x26 arrow, hotspot at +2,+2) | at x 2, y 262 (hotspot 4, 264): on the left edge | at x 600, y 34 (hotspot 602, 36): 4 px below the bar |
| Terminal, tiled right | x 720, y 32, 720x868; square; `--term-bg`; `0 0 0 1px var(--border)` hairline, no drop shadow | same |

The terminal header is 47 px with the centred title at 14px/700. The Files
window content (sidebar, path bar, folder grid) belongs to `files.md`.

## States

### Window switcher

Drawn:

*   Open, Terminal selected (initial state).
*   Any item selected by click; the caption follows the selection.
*   Dark (default) and light theme; accent tweak has no visible effect.

Needed, not drawn:

*   Alt+Tab opens with the previous app selected; repeated Tab advances;
    Shift+Tab goes back; releasing Alt activates the selected app's most
    recent window; Escape cancels.
*   Arrow keys and pointer hover change the selection (stock).
*   Per-app window list: Alt+\` or arrow down on a multi-window app (Terminal
    here) opens window thumbnails. Its style is not drawn.
*   Window switcher (`switch-windows`, Alt+Esc or a custom binding) if Apex
    enables it.
*   Overflow when apps do not fit the monitor width (stock shrinks icons, then
    scrolls).
*   Popup delay: stock shows the popup only after a short delay so a quick
    Alt+Tab switches without flashing it. Keep it.
*   Apps on other workspaces: stock `current-workspace-only` setting.
*   An app with more than about five windows: how many dots?

### Edge tiling

Drawn (`target` tweak):

*   `left half`: pointer on the left edge, preview fills the left half minus
    the 6 px inset.
*   `maximize`: pointer at the top, preview fills the work area minus the
    inset; the window is drawn at the top edge.

Needed, not drawn:

*   Right half (mirror of left half; the drawn Terminal is its result).
*   Preview hiding when the pointer leaves the edge zone (fade or shrink).
*   The window snapping into place on release, and the reverse (dragging a
    tiled or maximised window off the edge restores its previous size).
*   Keyboard tiling: Super+Left, Super+Right, Super+Up, Super+Down (stock).
*   Tiled pair resizing (stock GNOME resizes the neighbour together).
*   "Drag to Top Edge to Maximize" off (a switch in
    `ApexDesktop.dc.html`): the top edge does nothing, side edges still tile.
*   Quarter tiling: not drawn; stock GNOME has none.
*   Second monitor and the edge between monitors.
*   Reduce Motion and Reduce Transparency: preview without animation and
    without blur.

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour | `--panel`, `--panel-border`, `--btn-h`, `--fg`, `--accent`, `--win`, `--border`, `--term-bg`, `--head` |
| Type | `typography.family.ui`; `ui` 13.5px/600 (caption); `heading` 14px/700 (terminal title) |
| Radius | `panel` 26 (switcher), `lg` 16 (switcher item), `window` 14 (windows, tile preview), `circle` (dots) |
| Shadow | `panel` (switcher), `window` (dragged window) |
| Glass | "Quick Settings, calendar, toast" row, 30/180 `--panel`, radius 120 at scale 2, for the switcher (tokens.json notes the table does not list the switcher). Tile preview 20/160: not in the glass table. |
| Motion | `standard` easing with `slow` 300 ms (tile preview) |

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Switcher placement, padding, radius, selected fill | Theme | `.switcher-popup`, `.switcher-list`, `.item-box` CSS |
| Switcher glass | Patch | `Shell.BlurEffect` on the switcher and the saturation patch |
| 84 px icons | Patch (small) | Stock `AppSwitcher` picks from `[96, 64, 48, 32, 22]` |
| Single caption under the row instead of a label per icon | Patch | Stock `AppIcon` carries its own label |
| Window-count dots instead of the stock arrow | Patch | Stock draws `.switcher-arrow` for multi-window apps |
| MRU order, keyboard behaviour | Stock | |
| Edge tiling to halves and maximise | Stock | Mutter `edge-tiling` |
| Top-edge maximise as its own setting | Patch | Stock `edge-tiling` switches sides and top together |
| Preview fill, ring, all-corner radius 14 | Theme | `.tile-preview` CSS; stock rounds only the corners next to the panel (`tile-preview-left`, `tile-preview-right`, `on-primary`) |
| 6 px inset | Patch (small) | Stock `TilePreview` fills the tile rect exactly |
| Preview blur | Patch | `Shell.BlurEffect` on a moving, resizing actor; blur cannot be cached while it animates |
| 300 ms standard easing | Patch (small) | Stock animates with the window animation time and ease-out-quad |
| Tiled windows square, without shadow | Stock | Mutter tiled state and libadwaita |

Cost: the switcher is a small, contained patch to `altTab.js`. The tile
preview blur is the only expensive item: it re-blurs every frame while the
preview grows. Ship it behind Reduce Transparency and measure it on the
Radeon iGPU before committing.

## Accessibility

*   The switcher list has role `listbox`, accessible name "Switch windows";
    items are `option` with `aria-selected`. Stock Orca announces the
    selected app name; keep that, and add the window count ("Terminal, 2
    windows"), because the dots are visual only.
*   Caption contrast: `--fg` on `--panel` over the wallpaper. Test light and
    dark with both Apex wallpapers and with a bright window behind the panel.
*   The selected fill `--btn-h` is the only selection cue, and it is a faint
    tint over the panel (well under 3:1). Add a 2 px `focusRing`
    (`inset 0 0 0 2px var(--accent)`) when High Contrast is on.
*   The tile preview is decorative (`aria-hidden`). Announce the result
    ("Tiled left", "Maximised") through the window's state change.
*   The preview's accent ring at 70 % mix must stay at least 3:1 against the
    wallpaper for every accent; yellow `#c88800` on the light wallpaper is
    the weakest. Test it.
*   Reduced motion: no preview growth animation; the preview appears at its
    final size.

## Acceptance criteria

1.  Alt+Tab shows the switcher centred on the primary monitor (stock), with
    radius 26, padding 14 and a `--panel` glass fill.
2.  Each app occupies a 120x116 tile with an 84 px icon; tiles are 6 px
    apart.
3.  The selected tile has a `--btn-h` fill with radius 16; no other tile has
    a fill.
4.  Under each icon, one 4x4 dot shows per open window of that app (two for
    a Terminal with two windows).
5.  A single caption with the selected app's name, 13.5px/600, sits 10 px
    below the tile row and updates on every selection change.
6.  On first Alt+Tab the previously used app is selected; releasing Alt
    focuses it; Escape closes the switcher without changing focus.
7.  With five apps, the switcher measures 652 px wide.
8.  Dragging a window until the pointer touches the left or right monitor
    edge shows an accent preview covering that half of the work area minus
    6 px on every side, with radius 14 on all corners.
9.  Dragging a window to the top edge shows a preview covering the work
    area minus 6 px on every side; with "Drag to Top Edge to Maximize" off,
    no preview shows at the top.
10. The preview fill is the accent at 16 % and its ring is 2 px of the
    accent at 70 %; changing the accent recolours it.
11. The preview reaches its final size in 300 ms with the standard easing.
12. Releasing the window over a half preview tiles it to exactly half the
    work area (720 px wide on a 1440-wide layout, below the 32 px bar),
    square, with a 1 px `--border` hairline and no drop shadow.
13. With Reduce Transparency on, the preview has no blur; with Reduce Motion
    on, it does not animate.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here. Ranked by how much
they block engineering.

1.  Tiling draws no dock (`Tiling.dc.html` has no `<nav>`), with no window
    maximised. Does the dock hide for tiled windows, or is it just omitted?
    See `shell-top-bar-and-dock.md`, question 2.
2.  Is the tile preview blur wanted, given its cost? The SPEC glass table
    (`AltTab.dc.html:119-128`) does not list it.
3.  The 6 px inset makes the preview smaller than the tiled result (708 vs
    720 px). Confirm this is intended, not a hint of tiling gaps.
4.  The maximise scene puts the pointer hotspot at y=36, below the 32 px bar
    (`Tiling.dc.html:143`). Mutter's maximise zone is at the very top edge.
    Keep the stock zone?
5.  Per-app window thumbnails (Alt+\`) and the window switcher are not
    drawn. Style them like the app switcher?
6.  Dot count limit for apps with many windows.
7.  Old-spec text in `Tiling.dc.html`: terminal title and prompt
    "apex@fedora" (lines 45, 47, 58), image versions "45.20261008.131",
    "45.20261010.133", "45.20261001.124" (lines 51-55), the drive label "Apex
    Fedora" and "588 GB free of 1 TB" (lines 74, 76), and the folder
    "apex-fedora" (line 125). In `AltTab.dc.html:47` the editor path reads
    "~/apex-fedora/design". None is a requirement.
