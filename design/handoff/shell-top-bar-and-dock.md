# Shell: top bar, indicators and dock

## Summary

The top bar and the dock are the two permanent shell surfaces of the Apex
desktop. Two artboards draw them:

*   **37 Desktop: dock and top bar** (`Desktop.dc.html`): the bar and the dock
    on the empty desktop and over a maximised window. Tweaks: `scene`
    (`desktop`, `maximised`, `revealed`), `iconSize` (`small`, `medium`,
    `large`), `translucentBar`, `runningIndicators`, `showTrash`, `dark`,
    `accent`.
*   **39 Top bar: indicators** (`Indicators.dc.html`): the right half of the
    bar with app (tray) indicators, their menus, an overflow menu, and the
    system status pills. Tweak `scene`: `everyday`, `in a call`, `recording`,
    `menu`, `overflow`, `everything`.

The same bar and dock appear, unchanged in geometry, in every shell artboard
(AltTab, Tiling, Overview, Launcher, Spotlight). Differences between those
copies are listed under [Open questions](#open-questions).

The maximised Text Editor in `Desktop.dc.html:41-54` shows a roadmap excerpt
("S2a: The dock and the top bar") that describes the intended build
(an `ApexDock` subclass of `Dash`, schema keys). It is data, not a
requirement; this spec cites it only where it explains a drawn behaviour.

## Upstream mapping

| Element | Upstream component | Confidence |
| --- | --- | --- |
| Top bar | GNOME Shell `js/ui/panel.js` `Panel` (`#panel`) | High |
| Activities button with workspace pills | `js/ui/panel.js` `ActivitiesButton` and its workspace dots (GNOME 45+) | High |
| Focused app name | None since GNOME 45 removed `AppMenuButton` from the panel | High |
| Clock and unread dot | `js/ui/dateMenu.js` `DateMenuButton`, `MessagesIndicator` | High |
| Search button | None. New panel button that opens Spotlight (see `shell-overview-launcher-spotlight.md`) | High |
| System menu (Wi-Fi, volume, battery) | `js/ui/panel.js` `QuickSettings` indicators; `js/ui/status/network.js`, `volume.js`, `system.js` | High |
| Recording pill | `js/ui/status/remoteAccess.js` screen-recording indicator | Medium |
| Sharing pill | `js/ui/status/remoteAccess.js` screen-sharing indicator | Medium |
| Camera, microphone, location, remote desktop icons | Privacy indicators in Quick Settings: `status/camera.js` (GNOME 46+), `status/volume.js` input indicator, `status/location.js`, `status/remoteAccess.js` | Medium |
| Unsafe mode icon | Unsafe-mode indicator in the Quick Settings indicator box | Medium |
| Accessibility button | `js/ui/status/accessibility.js` | High |
| Input source button | `js/ui/status/keyboard.js` `InputSourceIndicator` | High |
| App indicators and their menus | Not in GNOME Shell. StatusNotifierItem support comes from the AppIndicator extension (`gnome-shell-extension-appindicator`, packaged in Fedora) | High |
| Overflow "+N" button and menu | Not in GNOME Shell or the AppIndicator extension | High |
| Dock | `js/ui/dash.js` `Dash`, `DashIcon`, `ShowAppsIcon`, made always visible outside the overview. Behaviour matches Dash to Dock (intellihide, Trash, fixed icon size, edge reveal) | High for the base, medium for the route |
| Running dot | `js/ui/appDisplay.js` `AppIcon` running dot (`.app-well-app-running-dot`) | High |
| Hover label | `js/ui/dash.js` `DashItemContainer.showLabel` (`.dash-label`) | High |
| Glass on bar and dock | `Shell.BlurEffect` (`src/shell-blur-effect.c`) on the actor, plus the saturation patch the canvas calls "patch 0003" | High |

Two routes exist for the dock. Ship a fork of Dash to Dock with Apex
defaults and CSS, or write the `ApexDock` subclass of `Dash` that the
roadmap text describes (`Desktop.dc.html:43-50`, "about 800 lines"). Both
need the same behaviours listed below. The owner must pick one.

## Layout and measurements

All values are logical px on the 1440x900 artboard (device px = 2x).

### Top bar

| Property | Value | Source |
| --- | --- | --- |
| Position | `top:0; left:0; right:0`, height 32, `z-index:10` | `Desktop.dc.html:140` |
| Padding | `0 8px` | same |
| Text | 13.5px, weight 600, colour `--bar-fg` | same |
| Glass (translucent) | `--bar` fill, `blur(24px) saturate(160%)` | `Desktop.dc.html:141` |
| Solid | `--bar-solid` fill, no blur | same |
| Layout | Left box `flex:1`, centre clock absolutely centred (`left:50%; translateX(-50%)`), right box `flex:1` right-aligned; boxes use `gap:2px` | `Desktop.dc.html:61-69` |

Every top-bar button is 24 px tall with radius 12 (`pill-bar`). No hover
fill is drawn in these artboards; use `--bar-hover` from tokens.json
(`WifiMenu.dc.html`).

#### Left box

| Element | Measurements |
| --- | --- |
| Activities button | Height 24, padding `0 10px`, radius 12, `gap:10px`. Width 63 with two workspaces. |
| Diamond | 10x10 box, `2px solid currentColor` border, radius 2, rotated 45 deg |
| Workspace pills | Row with `gap:4px`. Active pill 22x7, radius 4, `currentColor`. Inactive pill 7x7, radius 4, `currentColor` at opacity .45. One pill per workspace. |
| Focused app name | Weight 700, padding `0 8px`. Text is the focused app's name; "Desktop" when nothing is focused (`Desktop.dc.html:138`). |

#### Centre: clock

Height 24, padding `0 12px`, radius 12, `gap:8px`, weight 700. Two text
runs, date then time ("Sat Oct 24", "14:10"), then an unread dot: 5x5,
radius 3, `--accent` (`Desktop.dc.html:68`).

#### Right box, as drawn in Desktop

| Element | Measurements |
| --- | --- |
| Search | 32x24, radius 12, 16 px magnifier glyph, centred |
| System menu | Height 24, padding `0 10px`, radius 12, `gap:8px`, three 16 px glyphs: Wi-Fi, volume, battery. Width 84. Right edge at x=1432. |

#### Right box, as drawn in Indicators

Left to right (`Indicators.dc.html:35-113`):

| Order | Element | Measurements | Shown in scenes |
| --- | --- | --- | --- |
| 1 | App indicator buttons | Each 30x24, radius 12, 16 px glyph, `gap:2px` between. Open state fill `--btn-h`. | all |
| 1a | Unread badge | 6x6, radius 3, `--accent`, `top:3px; right:5px` inside the button | Chat only |
| 2 | Overflow button | Height 24, padding `0 8px 0 6px`, radius 12, `gap:2px`; 16 px left chevron + count "+N" at 12px/700. Open fill `--btn-h`. | `overflow`, `everything` |
| 3 | Separator | 1x14, `currentColor` at opacity .2, margin `0 6px` | all |
| 4 | Search | As in Desktop | all |
| 5 | Recording pill | Height 24, padding `0 10px 0 8px`, radius 12, `gap:7px`, fill `--recording`, ink `--pill-ink`, 12.5px/700, tabular numbers. 8x8 radius-2 stop square in ink, then elapsed time "0:42". | `recording`, `everything` |
| 6 | Unsafe mode | 28x24, 16 px warning triangle, no fill, not a button | `everything` |
| 7 | Accessibility | 28x24 button, radius 12, 16 px glyph | `everything` |
| 8 | Input source | Height 24, min-width 32, padding `0 8px`, radius 12, 12px/800, `letter-spacing:.04em`. Text "EN" or "VI". | all |
| 9 | Sharing pill | Height 24, padding `0 9px 0 8px`, `margin-right:4px`, radius 12, `gap:6px`, fill `--privacy`, ink `--pill-ink`; 14 px screen glyph (stroke 1.9) + 8x8 radius-2 square in `#ffffff` | `in a call`, `everything` |
| 10 | System menu | As in Desktop, but left padding drops to 4 when the privacy pill is present (`pillLeft`, `Indicators.dc.html:228`) | all |
| 10a | Privacy pill, inside the system menu button, before the Wi-Fi glyph | Height 20, padding `0 7px`, `margin-right:2px`, radius 10, `gap:6px`, fill `--privacy`, ink `--pill-ink`; one 14 px glyph (stroke 1.9) per active sensor, in order camera, microphone, location, remote desktop | `in a call` (camera, mic), `everything` (all four) |

Pill colours are literals with no token (`Indicators.dc.html:207`):

| Name | Light | Dark |
| --- | --- | --- |
| `--recording` | `#8d151d` | `#e54543` |
| `--privacy` | `#7e2d00` | `#d95613` |
| `--pill-ink` | `#ffffff` | `#16161a` |

The 8x8 square in the sharing pill is `#ffffff` in both themes, not
`--pill-ink` (`Indicators.dc.html:99`).

#### Overflow rule

At most four app indicators fit (`VISIBLE = 4`). With more than four, the
bar shows the first three plus the overflow button, and the rest move to the
overflow menu (`Indicators.dc.html:174-179`). Indicators keep their
registration order.

#### Indicator menus

| Property | App indicator menu | Overflow menu |
| --- | --- | --- |
| Anchor | `top:30px; right:-10px` relative to the button (2 px below the bar, right edge 10 px past the button) | same |
| Box | Width 280, padding 6, radius 14 (`window`), `--panel-solid`, shadow `panel` | Width 240, otherwise same |
| Header | 30 tall, padding `0 12px`, 12px/700, `--dim`; text is the indicator name | none |
| Row | 34 tall, padding `0 12px`, radius 9, `gap:10px`, 13.5px/500, left-aligned | 34 tall, padding `0 10px`, radius 9, `gap:10px`, 13.5px/500: 16 px glyph, name, 12 px right chevron at opacity .55 |
| Separator | 1 px `--border`, margin `5px 10px` | none |
| Switch | 30x18, radius 9, padding 2; knob 14x14 `#ffffff`, shadow `0 1px 2px rgba(0,0,0,.25)`; on: `--accent`, knob right; off: `--btn-h`, knob left | none |
| Shortcut hint | 12px, `--dim`, right-aligned | none |

Row radius 9 and the switch geometry are literals; no token matches.

### Dock

| Property | Value | Source |
| --- | --- | --- |
| Position | `bottom:10px`, centred horizontally, `z-index:9` | `Desktop.dc.html:142` |
| Box | `display:flex; align-items:flex-end; gap:2px`, padding `5px 8px 3px`, radius 24 (`dock`) | same |
| Glass | `--dock` fill, `blur(28px) saturate(180%)` | same |
| Shadow | `inset 0 0 0 1px var(--dock-border), 0 10px 30px rgba(0,0,0,.18)` (`dock`) | same |
| Item | Button, column, `gap:4px`, radius 14: icon, then running dot | `Desktop.dc.html:83-86` |
| Icon | 46, 54 (default) or 62 px square | `Desktop.dc.html:103` |
| Running dot | 4x4, radius 2, `--fg`, opacity .7 when running, 0 otherwise. The dot keeps its space when hidden. | `Desktop.dc.html:130` |
| Separator | 1x40, `--dock-sep`, margin `0 4px 8px`; its bottom lines up with the icon bottoms | `Desktop.dc.html:81` |
| Hover lift | Icon `translateY(-6px)`, `transition: transform .18s ease-out` | `Desktop.dc.html:129` |
| Hover label | 26 tall, padding `0 10px`, radius 13, 12.5px/600, `--panel-solid`, shadow `panel`; centred over the item, its bottom `size + 20` px above the item bottom (12 px above the resting icon, 6 px above the lifted icon) | `Desktop.dc.html:131` |
| Hide transform | `translate(-50%, calc(100% + 12px))`, `transition: transform .25s ease-out` | `Desktop.dc.html:142-143` |

Derived dock sizes (12 children: 9 apps, separator, Show Apps, Trash):

| Icon size | Height | Width with Trash | Width without Trash |
| --- | --- | --- | --- |
| Small 46 | 62 | 553 | 505 |
| Medium 54 | 70 | 641 | 585 |
| Large 62 | 78 | 729 | 665 |

Height is `icon + 16`. At medium the dock top edge is at y=820.

#### Dock order

Pinned apps, then running apps that are not pinned, then the separator, then
Show Apps, then Trash (`Desktop.dc.html:109-118`). The pinned set drawn in
every other artboard is Files, Web, Calendar, Music, Text Editor, Terminal,
Bazaar, Settings. Desktop also shows Image Viewer after Settings. Image Viewer
is in the Launcher grid (`Launcher.dc.html:117`), and the grid excludes
pinned apps, so Image Viewer here is most likely a running, unpinned app.
No separator divides pinned from running apps. Upstream `Dash` puts one
there.

Show Apps uses a full-colour tile icon, not the symbolic grid glyph. Trash
uses a full-colour icon.

## States

### Tweaks in Desktop

| Tweak | Effect |
| --- | --- |
| `scene: desktop` | No window. Bar glass (if `translucentBar`), focused label "Desktop", dock visible. |
| `scene: maximised` | Maximised Text Editor fills `top:32px` to the bottom edge (no strut). Bar solid, focused label "Text Editor", dock hidden (slid down 82 px at medium, fully off screen). Hover labels suppressed. |
| `scene: revealed` | Same window; the dock is shown over it after a bottom-edge reveal. Bar stays solid. Hover works. |
| `iconSize` | 46 / 54 / 62 px icons. Separator stays 40 tall. |
| `translucentBar: false` | Bar always `--bar-solid`. |
| `runningIndicators: false` | Every dot at opacity 0; dot space kept. |
| `showTrash: false` | Trash item removed; the dock shrinks. |
| `dark`, `accent` | Theme and the clock dot colour. |

The bar is solid when `scene != desktop` or `translucentBar` is off
(`Desktop.dc.html:105`). Running in Desktop: Files, Text Editor, Terminal,
Image Viewer. The initial hover is Terminal, so the default render shows the
"Terminal" label and a lifted Terminal icon.

### Scenes in Indicators

| Scene | App indicators | Other right-box items | Focused label |
| --- | --- | --- | --- |
| `everyday` | File sync, Chat (badge), Game launcher | "EN" | "Desktop" |
| `in a call` | File sync, Chat | "EN", sharing pill, privacy pill (camera, mic) | "Video call" |
| `recording` | File sync, Chat | Recording pill "0:42", "EN" | "Desktop" |
| `menu` | As `everyday`; Chat menu open, Chat button `--btn-h` | "EN" | "Desktop" |
| `overflow` | File sync, Chat, Game launcher, "+4"; overflow menu open | "EN" | "Desktop" |
| `everything` | As `overflow` but menu closed | Recording, unsafe, accessibility, "VI", sharing, privacy (camera, mic, location, remote desktop) | "Desktop" |

Click behaviour (`Indicators.dc.html:190, 215`): clicking an indicator opens
its menu and closes any other; clicking the open one closes it; clicking the
overflow button toggles its menu and closes indicator menus. Changing scene
resets both.

### Indicator menu contents

Copy is exact. "toggle" rows are `menuitemcheckbox` with a switch.

| Indicator (accessible name) | Rows |
| --- | --- |
| File sync | "Up to date · 12,408 files"; separator; "Open sync folder"; "Pause syncing" (toggle, off); separator; "Settings…"; "Quit" |
| Chat | "Show Chat" (hint "Ctrl+Shift+C"); "Do Not Disturb" (toggle, off); "Start at login" (toggle, on); separator; "Mute for 1 hour"; separator; "Quit Chat" |
| Game launcher | "Library"; "Friends"; separator; "Exit" |
| Password manager | "Unlock database"; "Lock now" (hint "Ctrl+L"); separator; "Quit" |
| Media player | "Play"; "Next" |
| Clipboard history | "Show history" |
| Mouse · 80 % | "Battery 80 %" |

These menus are sample content. In a real build the rows come from each
app's DBusMenu; only the styling is Apex's.

### States the artboards do not draw

*   Hover and pressed fills on bar buttons, menu rows and dock items (dock
    hover is drawn only as the lift and label).
*   Keyboard focus rings on bar buttons and dock items.
*   Bar during the overview: Overview and Launcher draw Activities with a
    `--btn` fill and `aria-pressed`, no focused label and no Search button
    (`Overview.dc.html:30-36`).
*   Fullscreen windows: bar and dock hidden (stock for the bar).
*   Dock with many apps (overflow or shrink), drag-and-drop reorder, pin and
    unpin, right-click app menu, urgent or attention state, launching
    (spinner or bounce), multiple windows per app (one dot or several).
*   Trash full versus empty icon, drop-to-trash, and its menu (Open, Empty).
*   Dock on a second monitor, and dock position other than bottom.
*   Reveal and hide delays, pressure threshold for the bottom-edge reveal, and
    what happens when the pointer leaves.
*   Bar transition between glass and solid (Desktop draws none; tokens.json
    `motion.duration.slow` records 300 ms from `ApexDesktop.dc.html`).
*   Clock with seconds, 12-hour format, or with the date hidden.
*   Input source button with a single configured source.
*   Recording timer over 1 hour; more than one screen share.
*   Reduce Transparency and Reduce Motion (switches in
    `ApexDesktop.dc.html`): solid bar and dock, no lift, no slide.

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour | `--bar`, `--bar-solid`, `--bar-fg`, `--bar-hover`, `--dock`, `--dock-border`, `--dock-sep`, `--panel-solid`, `--panel-border`, `--fg`, `--dim`, `--border`, `--btn-h`, `--accent`, `--wall`. `--recording`, `--privacy`, `--pill-ink` (in `tokens.json` under `color.shell` since 2026-11-17). |
| Type | `typography.family.ui`; sizes `small` 12px, `small-plus` 12.5px, `ui` 13.5px; weights 500, 600, 700, 800; `features.numbers` (tabular) on the recording timer |
| Radius | `pill-bar` 12 (bar buttons), `window` 14 (menus, dock items), `dock` 24, `circle` (dots). Literals: 2 (diamond), 4 (pills), 9 (menu rows, switch), 10 (privacy pill), 13 (hover label) |
| Shadow | `dock`, `panel` (menus, hover label) |
| Glass | Top bar 24/160 `--bar`, radius 96 at scale 2; Dock 28/180 `--dock`, radius 112 |
| Motion | `easeOut` for the dock lift (.18 s) and dock hide (.25 s); `slow` 300 ms for the bar change (from ApexDesktop) |
| Spacing | `topBarHeight` 32, `topBarButtonHeight` 24, `topBarPadding` `0 8px`, `dockPadding`, `dockBottomOffset` 10, `dockIcon` |

Conflict: `--bar-solid` in `Desktop.dc.html:18-19` is `#ebebef` / `#151518`;
tokens.json takes `#f3f3f5` / `#121215` from ApexDesktop. Use the token
value unless the owner says otherwise.

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Bar height, padding, type, button pills | Theme | `#panel` and `.panel-button` CSS |
| Glass bar (live blur + saturation) | Patch | Stock panel is opaque. Needs `Shell.BlurEffect` on `#panel` and the saturation patch (0003). |
| Bar solid while a window is maximised | Patch | Needs window tracking on the active workspace and monitor; stock has no such state |
| Diamond in Activities | Patch (small) | Needs an extra actor in `ActivitiesButton`. A `background-image` in CSS might work but is fragile |
| Workspace pills | Theme | Stock GNOME 45+ draws them; sizes and opacity via CSS |
| Focused app name and "Desktop" fallback | Patch | Removed upstream in GNOME 45; re-add a label bound to `Shell.WindowTracker` focus-app |
| Clock date and weekday | Stock (settings) | `clock-show-date`, `clock-show-weekday` |
| Clock unread dot | Theme | Stock `MessagesIndicator`; restyle to 5x5 accent |
| Search button | Patch | New panel item that opens Spotlight |
| System menu glyphs | Theme | Apex Symbolic icon set |
| Recording and sharing pills | Theme | Stock indicators exist; recolour, resize |
| Privacy pill grouping several sensors in one fill | Patch (small) | Stock shows separate icons in the Quick Settings indicator box with no shared container |
| Order of right-box items (recording before input source, sharing just before the system menu) | Patch (small) | Stock order is fixed in `panel.js` |
| Unsafe mode, accessibility | Stock + theme | |
| Input source uppercase "EN" / "VI" | Patch (small) | Stock shows the source's short name in its own case; St has no `text-transform` |
| App indicators | Extension | AppIndicator extension, restyled with Apex CSS |
| Overflow "+N" and its menu | Patch | Not in the extension; needs a container that measures and moves items |
| Indicator menu styling | Theme | `.popup-menu` CSS plus switch styling |
| Separator between app indicators and Search | Patch (small) | New actor |
| Dock always visible outside the overview | Extension or patch | Dash to Dock fork or `ApexDock` |
| Fixed icon sizes 46/54/62 | Extension or patch | Stock `Dash` picks from `[16, 22, 24, 32, 48, 64]` to fit |
| Dock glass | Patch | `Shell.BlurEffect` + saturation patch |
| Hide behind maximised windows, bottom-edge reveal | Extension or patch | Dash to Dock intellihide in "maximised windows" mode, plus pressure barrier |
| No strut (windows extend under the dock) | Extension or patch | |
| Running dot 4x4 at .7 | Theme | `.app-well-app-running-dot` CSS |
| Order: pinned, running, separator, Show Apps, Trash | Patch | Stock `Dash` places a separator between favourites and running apps and none before Show Apps |
| Full-colour Show Apps tile | Patch (small) | Stock uses a symbolic icon in a button |
| Trash item | Extension or patch | Dash to Dock has `show-trash`; stock has none |
| Hover lift -6 px | Patch (small) | Stock hover is a background highlight |
| Hover label style | Theme | `.dash-label` CSS |
| Hover label position (6 px above lifted icon) | Patch (small) | Offset is computed in `dash.js` |
| Overview's own dash hidden, Show Apps bound to the dock | Patch | `overviewControls.js` |

Cost: the glass bar and dock are cheap only if blur is cached while nothing
underneath changes (the "decision 14" note in `AltTab.dc.html`, SPEC line
204). Live blur over moving windows on the Radeon iGPU at 2880x1800 needs a
performance budget; measure before committing. The dock as a whole is the
largest item in this group: either a maintained fork of Dash to Dock or about
800 lines of new shell code that must track every GNOME release.

## Accessibility

*   Contrast: `--bar-fg` on `--bar-solid` is 15.2:1 light, 16.9:1 dark. On
    glass it depends on the wallpaper; test with both stock Apex wallpapers
    and a white and a black image. Menu `--dim` text is 6.4:1 light and 6.3:1
    dark on `--panel-solid`. Recording pill ink is 9.3:1 light and 4.52:1 dark;
    privacy pill ink is 9.3:1 light and 4.55:1 dark. The dark pills are at the
    AA limit, so do not lighten their fills.
*   The Chat badge and the clock dot use colour only. Expose "unread" in the
    accessible name (for example "Chat, unread messages").
*   Accessible names as drawn: "Activities", "Search", "System menu", "Dock",
    each dock app name, each indicator name, "N more app indicators" for the
    overflow button, "More app indicators" for its menu, "Stop screen
    recording, 0:42", "Unsafe mode is on", "Accessibility", "Input source:
    English (US)" / "Input source: Vietnamese (Telex)", "Stop screen sharing",
    "In use: camera, microphone" (and the four-item form). The recording name
    must update with the timer at a rate a screen reader can follow (for
    example once a minute).
*   Roles: indicator buttons `aria-haspopup="menu"` with `aria-expanded`;
    menu rows `menuitem` or `menuitemcheckbox` with `aria-checked`.
*   Keyboard: Ctrl+Alt+Tab must reach the bar and the dock (the roadmap
    text says "Ctrl+Alt+Tab focus"). Arrow keys move along the bar and the
    dock; Enter or Space opens; Escape closes a menu and returns focus to its
    button. The dock must reveal while it holds keyboard focus.
*   Reduced motion: no lift, no slide; the dock appears and disappears
    instantly. Reduce Transparency: `--bar-solid` and an opaque dock fill.
*   Large text: the bar is fixed at 32 px; at text scale 1.25 the 13.5 px
    labels must still fit, or the bar grows. Owner decision.

## Acceptance criteria

1.  The top bar is 32 px tall (64 device px) across the full monitor width,
    with 8 px side padding.
2.  Every bar button is 24 px tall with radius 12.
3.  The clock is horizontally centred on the monitor (centre at x=720 on a
    1440-wide layout) regardless of the width of the left and right boxes.
4.  The Activities button shows a 10x10 diamond, then one pill per
    workspace: the active one 22x7, the others 7x7 at 45 % opacity.
5.  With no focused window the bar shows "Desktop" next to Activities; with
    a focused window it shows that app's name in weight 700.
6.  With `translucentBar` on and no maximised window, the bar shows the
    wallpaper blurred (sigma 24 logical px) under a `--bar` tint.
7.  When a window on the current workspace and monitor is maximised, the bar
    turns `--bar-solid` within 300 ms; it returns to glass when the window is
    unmaximised, minimised or closed.
8.  With `translucentBar` off, the bar is `--bar-solid` in every state.
9.  The dock sits 10 px above the bottom edge, centred, radius 24, padding
    5/8/3, and at medium size measures 641x70 with 9 apps, Show Apps and Trash.
10. Icon size Small, Medium, Large render dock icons at 46, 54 and 62 px.
11. Running apps show a 4x4 dot 4 px below the icon; with running indicators
    off no dot shows and the dock height does not change.
12. The separator is 1x40 with 4 px side margins and sits immediately
    before Show Apps, and its bottom aligns with the icon bottoms.
13. With Show Trash off, Trash is not in the dock and the dock narrows by
    one icon plus 2 px.
14. A running app that is not pinned appears after the pinned apps and
    before the separator, with no extra separator.
15. Hovering a dock icon raises it 6 px over 180 ms and shows its name in a
    26 px label whose bottom is 6 px above the raised icon.
16. When a window is maximised, the dock slides fully below the screen edge
    in 250 ms; pushing the pointer against the bottom edge brings it back over
    the window; moving away hides it again.
17. A maximised window's content extends to the bottom screen edge (no
    strut reserved for the dock).
18. With four or fewer app indicators, all show; with five or more, the
    first three show followed by a "+N" button, where N is the remainder.
19. Clicking an app indicator opens a 280 px menu whose right edge is 10 px
    right of the button and whose top is 2 px below the bar; clicking it
    again closes it; opening one closes any other.
20. The recording pill shows a stop square and the elapsed time in tabular
    figures and stops recording when clicked.
21. While the camera, microphone, location or remote desktop is in use, a
    single `--privacy` pill inside the system menu button shows one glyph per
    sensor in the order camera, microphone, location, remote desktop.
22. A 1x14 separator at 20 % opacity divides the app indicators from Search.
23. Clicking Search opens Spotlight (see `shell-overview-launcher-spotlight.md`).
24. With Reduce Motion on, the dock neither lifts nor slides.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here. Ranked by how much
they block engineering.

1.  Dock route: Dash to Dock fork or an `ApexDock` subclass of `Dash`
    (roadmap text, `Desktop.dc.html:43`)? It decides most of the cost.
2.  Hide rule: the Settings switch reads "Hide Behind Maximized Windows"
    (`ApexDesktop.dc.html:166`), but `Tiling.dc.html` draws no dock at all
    with two tiled, unmaximised windows. Does the dock also dodge tiled or
    overlapping windows (full intellihide)?
3.  Reveal and hide timings, pressure threshold, and behaviour when a menu
    or label is open.
4.  Is Image Viewer in `Desktop.dc.html:114` pinned or a running unpinned
    app? Every other artboard pins eight apps.
5.  The input source button shows "EN" in `Indicators.dc.html:96` but is
    absent from the bar in Desktop, AltTab, Tiling, Overview, Launcher and
    Spotlight. Show it with one source, or only with two or more (stock)?
6.  The clock unread dot is drawn in Desktop and Indicators only. Confirm it
    means unread notifications.
7.  `--bar-solid` value: Desktop `#ebebef` / `#151518` versus ApexDesktop
    `#f3f3f5` / `#121215`.
8.  App indicator support means shipping the AppIndicator extension enabled
    by default. Confirm.
9.  The overflow limit of four: fixed, or computed from free bar width?
10. Indicator menu rows use weight 500 (`Indicators.dc.html:48`); tokens.json
    calls 600 the default UI weight. Confirm 500 for menus.
11. Answered 2026-11-17: `--recording`, `--privacy` and `--pill-ink` are in
    `tokens.json` (`color.shell`). In dark, `--pill-ink` on the pills is 4.5:1,
    just at AA for 12.5 px bold text.
12. Multi-monitor: bar and dock on every monitor or primary only?
