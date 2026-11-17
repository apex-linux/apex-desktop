# Quick Settings and screenshot UI

## Summary

This spec covers two shell surfaces:

*   Quick Settings with the Wi-Fi submenu open (artboard 17,
    `WifiMenu.dc.html`). The artboard draws the whole Quick Settings panel,
    not only the submenu: the system row, the volume and brightness sliders
    and six toggle tiles are visible, with the Wi-Fi network list expanded
    inline under the first row of tiles.
*   The screenshot and screencast UI (artboard 19, `Screenshot.dc.html`),
    with three capture-area modes over a Terminal window.

The top bar and dock in both artboards are specified in
[shell-top-bar-and-dock.md](shell-top-bar-and-dock.md).

## Upstream mapping

| Surface | Upstream component | Confidence |
| --- | --- | --- |
| Quick Settings panel | GNOME Shell `js/ui/quickSettings.js` (`QuickSettingsMenu`, `QuickToggle`, `QuickMenuToggle`, `QuickSlider`), assembled in `js/ui/panel.js` | High |
| System row | `js/ui/status/system.js` (battery, Screenshot, Settings, Lock, Power Off menu) | High |
| Volume slider | `js/ui/status/volume.js` | High |
| Brightness slider | `js/ui/status/brightness.js` | High |
| Wi-Fi tile and submenu | `js/ui/status/network.js` (`NMWirelessToggle`, wireless device and network items) | High |
| Bluetooth tile | `js/ui/status/bluetooth.js` | High |
| Power Mode tile | `js/ui/status/powerProfiles.js` (power-profiles-daemon) | High |
| Night Light, Dark Style | `js/ui/status/nightLight.js`, `js/ui/status/darkMode.js` | High |
| Do Not Disturb tile | Not a Quick Settings tile in the Shell versions I can confirm; stock DND lives in the calendar panel. Verify against the target Shell release; if absent, it is a small new `QuickToggle` bound to `org.gnome.desktop.notifications show-banners` | Medium |
| Screenshot UI | `js/ui/screenshot.js` (`ScreenshotUI`, `UIAreaSelector`, `UIWindowSelector`, `UIMonitorSelector`) | High |

## Layout and measurements

All values are logical px on the 1440x900 artboard.

### Quick Settings panel

| Element | Value | Source |
| --- | --- | --- |
| System menu button (open) | Top-bar pill 24 px tall, padding `0 10px`, radius 12 px, fill `--bar-hover`; Wi-Fi, volume and battery glyphs 16 px, 8 px gap | `WifiMenu.dc.html:35-39` |
| Panel | `top: 38px`, `right: 8px`, width 376 px, padding 14 px, radius 26 px, column flex, gap 14 px; `--panel` with glass 30 / 180; `shadow.panel` | `:57` |
| Panel height | About 697 px with the submenu open (y 38 to 735) | computed |
| System row | 36 px tall, gap 8 px | `:58` |
| Battery | Not a button: pill 36 px, padding `0 14px`, radius 18 px, `--btn`, battery glyph 16 px, 6 px gap, "87%" 13 px / 600 | `:59` |
| Round buttons | Screenshot, Settings, Lock, Power: 36 px circles, `--btn`, 16 px glyphs, right-aligned after a flexible spacer | `:60-64` |
| Sliders block | Padding `0 4px`, gap 6 px, two rows | `:67` |
| Slider row | 20 px glyph, 12 px gap, slider fills the rest | `:68-74` |
| Slider | 28 px hit height; track 6 px, radius 3 px, `--btn-h`; fill `--accent`; knob 20 px white circle, shadow `0 1px 4px rgba(0,0,0,.3),0 0 0 .5px rgba(0,0,0,.1)` | `:70`, `:74` |
| Slider values | Volume 62 %, brightness 78 % | `:70`, `:74` |
| Tile grid | 2 equal columns, gap 10 px; each tile 169 px wide | `:78` |
| Tile | 54 px tall, radius 27 px, padding `0 14px`, gap 10 px, 20 px glyph; title 13 px / 700; subtitle 11.5 px, ellipsized | `:79-124` |
| Tile on | Fill `--accent-strong` (`color-mix(in srgb, <accent> 75%, #000)`), text `#fff`, subtitle opacity .9 | `:22`, `:79`, `:86`, `:110` |
| Tile off | Fill `--btn`, text `--fg`, subtitle opacity .78 | `:114-124` |
| Split tile (Wi-Fi) | Main area padding `0 4px 0 14px`; arrow area 40 px wide, fill `rgba(0,0,0,.12)` over the tile, 16 px down chevron; `aria-expanded="true"` | `:79-84` |

Tile order, left to right and top to bottom:

| Row | Left | Right |
| --- | --- | --- |
| 1 | Wi-Fi, on, "Apex-5G", split with arrow | Bluetooth, on, "Keychron K3", no arrow |
| Submenu | Wi-Fi networks card spanning both columns | |
| 2 | Power Mode, on, "Balanced", no arrow | Night Light, off, "Off" |
| 3 | Dark Style, off, "Off" | Do Not Disturb, off, "Off" |

### Wi-Fi submenu card

| Element | Value | Source |
| --- | --- | --- |
| Card | Spans both columns, padding 8 px, radius 18 px, `--card`, ring `0 0 0 1px var(--card-border)`, column flex, gap 2 px; about 351 px tall | `WifiMenu.dc.html:91` |
| Header | Padding `4px 6px 8px`, gap 10 px; 32 px accent circle with white 16 px Wi-Fi glyph; "Wi‑Fi" 15 px / 700; adapter name right-aligned, 11.5 px `--dim` | `:92-95` |
| Network row | 38 px tall, padding `0 10px`, radius 8 px, gap 12 px, 13.5 px; 400 weight, or 600 with `--btn` fill when connected | `:98`, `:153` |
| Signal glyph | 16 px; three levels by dimming the outer arcs to opacity .28 (3 bars: none dimmed; 2: outer dimmed; 1: both arcs dimmed) | `:99`, `:144-151` |
| Name | Flexes, ellipsized | `:100` |
| Secured glyph | 14 px padlock, opacity .6, accessible name "Secured" | `:101` |
| Connected mark | 18 px slot; 16 px check in `--accent`, accessible name "Connected" | `:102` |
| Separator | 1 px `--border`, margin `4px 8px` | `:105` |
| Footer items | "All Networks…" and "Wi‑Fi Settings": 38 px, padding `0 10px`, radius 8 px, 13.5 px | `:106-107` |

The panel does not dim the other tiles while the submenu is open.

### Screenshot UI

| Element | Value | Source |
| --- | --- | --- |
| Scene | Terminal window at (200, 80), 1040 x 600, radius 14 px; dark theme fallback, see States | `Screenshot.dc.html:40` |
| Panel | Centred, `bottom: 48px`, width 440 px, padding 14 px, radius 26 px, column flex, gap 12 px; `--panel` with glass 30 / 180; `shadow.panel`; about 210 px tall (y 642 to 852) | `:91` |
| Header | Padding `0 2px 0 8px`; heading 13.5 px / 700 ("Screenshot" or "Screencast"); close button 30 px circle, `--btn`, 16 px cross | `:92-94` |
| Area picker | Radio group, 3 equal columns, gap 8 px; each 132 x 64 px, radius 16 px, column flex, gap 5 px, 20 px glyph, label 12.5 px / 600; `--btn-h` when chosen, `--btn` otherwise | `:96-102`, `:127` |
| Bottom row | Grid `1fr auto 1fr`, centred vertically | `:104` |
| Show pointer | Switch, 38 px circle at the start; off `--btn`; on `--accent` with white 16 px pointer glyph | `:105`, `:147` |
| Capture button | 64 px circle, transparent, ring `inset 0 0 0 4px var(--fg)` | `:108` |
| Capture dot | Screenshot: 48 px circle in `--fg`. Screencast: 26 px square, radius 8 px, `#e62d42`. 200 ms `cubic-bezier(.2,.8,.2,1)` between them | `:144` |
| Type toggle | Radio group at the end; padding 3 px, radius 19 px, `--btn`; two segments 40 x 32 px, radius 16 px; chosen segment `--panel-solid` with `0 1px 3px rgba(0,0,0,.15)`; 150 ms ease on background | `:111-113`, `:128` |

Capture-area overlays:

| Mode | Overlay | Source |
| --- | --- | --- |
| Selection | Rectangle at (216, 126), 760 x 300; ring `0 0 0 1px rgba(255,255,255,.9)`; outside dimmed by `0 0 0 9999px rgba(0,0,0,.45)`; four 14 px white corner handles centred on the corners, shadow `0 1px 4px rgba(0,0,0,.35)`; size label "760 × 300" above the top-right corner (top -34 px), 24 px tall, padding `0 10px`, radius 12 px, `rgba(0,0,0,.6)`, white JetBrains Mono 11.5 px / 600 | `:74-81` |
| Screen | Whole screen: `inset 0 0 0 3px var(--accent)` and `rgba(0,0,0,.12)` | `:83-85` |
| Window | Whole screen dimmed `rgba(0,0,0,.45)`; selected window outlined `0 0 0 3px var(--accent)` at its own position and radius | `:86-89` |

In Window mode the dimming layer (z 20) also covers the selected window, so
the chosen window is drawn dimmed. Treat that as a drawing error: the selected
window stays undimmed.

### Copy

Quick Settings: "87%", "Wi‑Fi" (with U+2011 non-breaking hyphen), "Apex-5G",
"Bluetooth", "Keychron K3", "Power Mode", "Balanced", "Night Light", "Dark
Style", "Do Not Disturb", "Off", "Intel Wi‑Fi 6 AX200", "All Networks…",
"Wi‑Fi Settings". Accessible names: "Quick Settings", "System menu",
"Screenshot", "Settings", "Lock", "Power", "Wi-Fi networks", "Secured",
"Connected". Sample networks: "Apex-5G", "Apex-2.4G", "Phone Hotspot",
"Library Guest" (open), "DIRECT-4F Printer".

Screenshot UI: "Screenshot", "Screencast", "Selection", "Screen", "Window",
"760 × 300". Accessible names: "Close", "Capture area", "Show pointer",
"Take screenshot" / "Start recording", "Capture type", "Screenshot",
"Screencast", "Selected area, 760 by 300", "Selected window".

## States

### Modelled by the artboards

| State | Behaviour | Source |
| --- | --- | --- |
| Light / dark, accent | Tweaks | both |
| Connected network | Clicking a row connects at once: bold, `--btn` fill, check, and the tile subtitle changes | `WifiMenu.dc.html:152`, `:160` |
| Signal strength | Three levels | `:144-151` |
| Secured / open | Padlock shown or not | `:101` |
| Capture area | Selection (default), Screen, Window | `Screenshot.dc.html:123`, `:134-138` |
| Capture type | Screenshot (default) or Screencast; heading, capture label and capture dot follow | `:133`, `:143-144` |
| Show pointer | Off (default) or on | `:145-147` |

### Needed but not drawn

Quick Settings:

*   **Tile hover, focus and pressed** looks; **submenu closed** (the normal
    view); **slider hover and drag**.
*   **Wi-Fi off**, **no adapter**, **hardware or airplane-mode block**,
    **scanning**, **no networks found**, **connecting** (spinner),
    **password needed** (stock opens the NetworkManager agent dialog),
    **failed**, **captive portal**, **hotspot active**.
*   **Four signal levels.** Stock NetworkManager icons have none, weak, ok,
    good and excellent; the artboard draws three.
*   **Other submenus.** Bluetooth and Power Mode are drawn without arrows;
    stock gives both a submenu (devices; Performance / Balanced / Power
    Saver). Decide whether to keep the stock arrows (recommended).
*   **Volume output selector** (stock arrow at the end of the volume slider)
    and the **microphone slider** shown while an app records.
*   **Battery states**: charging, charge limit reached, low, critical, and
    "Battery" opening Power settings (stock makes it a button; the artboard
    draws a plain label).
*   **Power button menu**: Suspend, Restart…, Power Off…, Log Out (stock).
*   **Background Apps** section at the bottom (stock since GNOME 44).

Screenshot UI:

*   **Selection being drawn or resized** (cursor changes), **no selection
    yet**, **multi-monitor** Screen mode, **window picker with several
    windows**.
*   **Recording in progress**: stock shows a top-bar indicator with elapsed
    time and a stop button, and the UI closes during recording.
*   **After capture**: the stock "Screenshot captured" notification, which
    artboard 34 already shows (`DateMenu.dc.html:130`).
*   **Screencast options** in newer Shell releases (audio, if present in the
    target release).
*   **Theme.** The JS falls back to dark when `dark` is unset
    (`Screenshot.dc.html:131`) while the tweak default is light (`:119`), so
    the artboard renders light. The real UI follows the session style.

## Main view tiles: what the panel must have

The artboard answers part of this: the main view is drawn behind the submenu.
Recommended main-view content for this laptop (ASUS Vivobook Pro M7400QC):

| Item | Drawn | Recommendation |
| --- | --- | --- |
| Battery, Screenshot, Settings, Lock, Power | Yes | Stock |
| Volume slider | Yes | Stock, with output selector |
| Brightness slider | Yes | Stock; the OLED panel's backlight interface must work (`amdgpu_bl*` or the vendor interface) |
| Wi-Fi (Intel AX200, `iwlwifi`) | Yes | Stock |
| Bluetooth (AX200, `btintel`) | Yes | Stock, with device submenu |
| Power Mode | Yes | Stock; power-profiles-daemon on Ryzen uses `amd-pstate` |
| Night Light, Dark Style | Yes | Stock |
| Do Not Disturb | Yes | New or stock depending on Shell release; same setting as the calendar switch |
| Airplane Mode | No | Stock rfkill toggle; keep, since the laptop has both Wi-Fi and Bluetooth radios |
| Keyboard backlight | No | Ask: stock Shell shows a keyboard brightness toggle when UPower exposes one; check whether this model's backlight is exposed |
| Wired, VPN, Hotspot | No | Stock, shown only when present or configured |
| Camera, location, screen-sharing indicators | No | Stock privacy indicators |
| Discrete GPU state | No | No stock tile. Ask whether NVIDIA RTX 3050 power state needs a tile; recommend none |

## Tokens used

| Group | Tokens and literals |
| --- | --- |
| Colour | `--fg`, `--dim`, `--border`, `--btn`, `--btn-h`, `--card`, `--card-border`, `--panel`, `--panel-solid`, `--panel-border`, `--bar`, `--bar-fg`, `--bar-hover`, `--accent`; `--accent-strong` (defined only in this artboard; now recorded in `tokens.json` as `accent.derived`); literals `#fff`, `rgba(0,0,0,.12)` (split-tile arrow), `#e62d42` (record, equal to the red accent), `rgba(0,0,0,.45)` and `rgba(0,0,0,.12)` (capture dimming), `rgba(255,255,255,.9)` (selection ring), `rgba(0,0,0,.6)` (size label) |
| Type | Inter; `caption` 11.5, `small-plus` 12.5, `body` 13, `ui` 13.5, `subtitle` 15; weights 400, 600, 700; JetBrains Mono 11.5 / 600 for the size label |
| Radius | `hairline` / 3 px literal (slider track), `sm` 8 (rows), `pill-bar` 12 (size label), 15 px literal (close), 16 (area buttons, type segments), `card-lg` 18 (card, battery pill, round buttons), `field` 19 (type toggle, pointer), `toast` 20 (knob), `panel` 26, 27 px literal (tiles), 32 px literal (capture button) |
| Shadow | `shadow.panel`; slider knob literal (differs from `shadow.knob`); segment `0 1px 3px rgba(0,0,0,.15)`; handle `0 1px 4px rgba(0,0,0,.35)` |
| Glass | "Quick Settings, calendar, toast": blur 30, saturate 180, `--panel` (both panels) |
| Motion | `standard` easing with `base` 200 ms (capture dot); `ease` with `fast` 150 ms (type toggle). Panel and submenu motion: stock |

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Panel structure (system row, sliders, 2-column tile grid, inline submenu) | Stock | `quickSettings.js` layout |
| Panel, tile, slider, row metrics and colours | Theme | `.quick-settings`, `.quick-toggle`, `.quick-menu-toggle`, `.slider`, `.quick-toggle-menu` |
| Glass behind the panel | Patch | Same blur and saturation patch as the calendar ([shell-calendar-notifications-osd.md](shell-calendar-notifications-osd.md)) |
| Checked tile in `--accent-strong` | Theme (verify) | The accent is a runtime setting. St in GNOME 47+ exposes `-st-accent-color` and colour functions (`st-mix()`, `st-darken()` and similar), which should express a 25 % black mix; confirm on the target release, otherwise a small patch precomputes it |
| No dimming of other tiles while a submenu is open | Patch | Stock `QuickSettingsMenu` dims the grid in JS; drop the dim or keep stock (recommended) |
| Bluetooth and Power Mode without arrows | Patch if kept | Stock tiles are menu toggles; recommend stock |
| Battery as a label | Patch if kept | Stock is a button; recommend stock |
| Submenu header with adapter name | Theme or stock | Stock shows the device name when relevant; the name comes from NetworkManager, never from copy |
| "All Networks…" | Verify | Check the stock `network.js` strings for the target release; use stock wording |
| Do Not Disturb tile | Stock or small new toggle | Depends on Shell release |
| Screenshot panel layout, area picker, pointer switch, capture button, type toggle | Stock | `screenshot.js` has all of these |
| "Screenshot" / "Screencast" heading in the panel | Patch | Stock has no heading label; only the close button sits at the top |
| Size label on the selection | Patch | Stock `UIAreaSelector` draws no dimensions |
| Window mode in place (outline over the real window) | Patch, expensive | Stock lays windows out in a grid, like the overview. Outlining windows in place needs a new selector in `screenshot.js` |
| Screencast capture dot as a red rounded square | Theme | `.screenshot-ui-capture-button` styles; see Open questions about the shape |

## Accessibility

*   **Contrast.** White on `--accent-strong` is about 5.9:1 for blue and 5:1
    for yellow, which passes for 13 px text. Off-tile subtitles at opacity
    .78 over `--btn` need a measurement in both themes. The accent check and
    the accent switch on the pointer button are non-text (3:1); the yellow
    accent is borderline.
*   **Roles.** Area picker and type toggle are radio groups; Show pointer is a
    switch; the Wi-Fi split tile has a separate expand button with
    `aria-expanded`. Network rows must expose connected, secured and
    signal-strength state to screen readers (the artboard names only the
    padlock and the check).
*   **Keyboard.** Super+S or the system menu opens Quick Settings (stock).
    Arrow keys move between tiles; Enter toggles; the arrow area opens the
    submenu; Esc closes the submenu first, then the panel. Print opens the
    screenshot UI; Shift+Print captures the screen and Alt+Print the window
    (stock). In the screenshot UI, S/C/W choose Selection, Screen, Window,
    V toggles screencast, P toggles the pointer, Enter or Space captures, Esc
    closes (stock; verify the single-letter keys on the target release).
*   **Reduced motion.** Capture dot and toggle transitions are instant when
    animations are off.
*   **Large text.** Tile subtitles ellipsize; network names ellipsize; check
    the 169 px tiles at text scaling 1.25.

## Acceptance criteria

1.  Opening the system menu shows a 376 px panel whose top is 6 px below the
    top bar and whose right edge is 8 px from the screen edge, with a 26 px
    radius.
2.  The system row shows the battery percentage and four 36 px round buttons
    (Screenshot, Settings, Lock, Power) aligned to the right.
3.  The volume and brightness sliders have a 6 px track, accent fill and a
    20 px white knob, and follow the real levels.
4.  Tiles are 54 px tall pills in a 2-column grid with a 10 px gap; checked
    tiles use the accent darkened 25 % with white text, unchecked use the
    neutral fill.
5.  The Wi-Fi tile has a 40 px arrow area; activating it expands the network
    card inline below the first tile row, spanning both columns.
6.  The network card header shows the Wi-Fi glyph in an accent circle, the
    title "Wi‑Fi" and the adapter name reported by NetworkManager (for
    example "Intel Wi‑Fi 6 AX200" on this laptop, another name elsewhere).
7.  Each network row is 38 px tall with signal glyph, name, padlock for
    secured networks and, for the connected one, bold text, neutral fill
    and an accent check.
8.  Choosing a secured network with no saved password opens the stock
    password dialog; while connecting, the row shows progress.
9.  "All Networks…" and "Wi‑Fi Settings" sit under a separator;
    "Wi‑Fi Settings" opens Settings at the Wi-Fi panel.
10. Turning Wi-Fi off from the tile hides the network list and sets the tile
    to unchecked with subtitle "Off".
11. The Do Not Disturb tile and the calendar Do Not Disturb switch show the
    same state at all times.
12. Pressing Print opens the screenshot panel 48 px above the bottom edge,
    440 px wide, with Selection chosen and Screenshot as the type.
13. In Selection mode, the area outside the selection is dimmed at 45 % black
    and the selection has four 14 px handles.
14. In Screen mode the whole monitor has a 3 px accent inset outline; in
    Window mode the pointed window has a 3 px accent outline and is not
    dimmed.
15. Switching to Screencast changes the capture button's inner mark with a
    200 ms transition and changes its accessible name to "Start recording".
16. Turning on Show pointer fills the pointer button with the accent; the
    pointer then appears in the capture.
17. After a screenshot, the image is on the clipboard, saved to
    `~/Pictures/Screenshots`, and the stock "Screenshot captured"
    notification appears.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

1.  **Main view tiles** (blocks Quick Settings work). Confirm the table in
    "Main view tiles": in particular Airplane Mode, keyboard backlight, a
    Do Not Disturb tile, and whether Bluetooth and Power Mode keep their
    stock submenus.
2.  **`--accent-strong`** is now in `tokens.json` (`accent.derived`). The
    same colour appears as `color-mix(in srgb, #000 25%, <accent>)` in
    `DateMenu.dc.html:164` and `Polkit.dc.html`. Open: how St derives it from
    the runtime accent (OQ-31 in `../OPEN-QUESTIONS.md`).
3.  **Window mode.** In place (patch, expensive) or the stock window grid?
4.  **Size label and heading** in the screenshot UI (two small patches): keep?
    Should the label show logical px (760 x 300) or device px (1520 x 600 at
    scale 2)?
5.  **Record mark.** The screencast mark is a red rounded square, which reads
    as "stop"; stock uses a red circle for "start recording". Confirm.
6.  **Machine-specific text.** "Intel Wi‑Fi 6 AX200" must come from the
    detected adapter, not copy. "Keychron K3", the network names and
    "87%" are sample data. The Terminal behind the screenshot UI shows
    "apex@fedora: ~", `apexctl update` output and version strings such as
    "45.20261010.133" and "GNOME 51.0 → 51.1" (`Screenshot.dc.html:41-55`);
    those are scene content, not requirements.
7.  **Slider knob shadow** differs from `shadow.knob`; pick one.
