# Settings: Appearance, Power, fingerprint, Apex Desktop

## Summary

This spec covers four GNOME Settings surfaces and the window chrome they
share:

| No. | Surface | Artboard |
| --- | --- | --- |
| 23 | Appearance panel | `Appearance.dc.html` |
| 24 | Power panel | `Power.dc.html` |
| 25 | Fingerprint enrollment dialog over the Users page | `Fingerprint.dc.html` |
| 11 | Apex Desktop panel (new), top and scrolled | `ApexDesktop.dc.html`, `ApexDesktopScrolled.dc.html` |

`ApexDesktopScrolled.dc.html` differs from `ApexDesktop.dc.html` only in the
title and in `<main>` (lines 84-85): `overflow:hidden`, `display:flex`,
`flex-direction:column`, `justify-content:flex-end`, so the column is drawn
bottom-aligned. It shows the same panel scrolled to the end (the tail of
Dock, then Windows and Effects). It has no other content or state.

The Software Updates panel (artboard 18) uses the same chrome. It is
specified in [updates-and-rollback.md](updates-and-rollback.md).

Several Power settings come from the owner's laptop (ASUS Vivobook Pro 14X
OLED, M7400QC: 14 inch 2880x1800 90 Hz OLED, RTX 3050, ELAN reader). They
are correct for that machine. The distro targets many machines, so each
hardware-specific row must appear only when the hardware and backend
support it, and the M7400QC must still get every one of them. See
[Hardware-dependent rows](#hardware-dependent-rows).

## Upstream mapping

| Surface | Upstream component | Confidence |
| --- | --- | --- |
| Window, sidebar, header bars, boxed lists | GNOME Settings `CcWindow` (`shell/cc-window.ui`), `CcPanelList`, libadwaita `AdwNavigationSplitView`, `AdwHeaderBar`, `AdwPreferencesGroup` with `.boxed-list` | High |
| Appearance | `panels/background/cc-background-panel` (titled Appearance since GNOME 42; Style and Accent Color sections since GNOME 47), `cc-background-chooser` | High |
| Power | `panels/power/cc-power-panel` (Power Mode via power-profiles-daemon, Power Saving Options, Automatic Suspend dialog, battery rows; GNOME 48 added a Battery Charging section backed by UPower charge thresholds) | High for stock rows; medium for the charge-limit row (GNOME 48 draws it as a "Preserve Battery Health" choice, not a switch; verify against the GNOME version shipped) |
| Users page and fingerprint dialog | `panels/system/users/cc-users-page`, `cc-fingerprint-dialog` (fprintd D-Bus `net.reactivated.Fprint`); Users moved under System in GNOME 46 | High |
| Apex Desktop | No upstream panel. Either a downstream panel added to gnome-control-center (`panels/apex-desktop/`), or the preferences window of the Apex Shell extension. The artboards put it first in the Settings sidebar, which only a gnome-control-center patch can do. | High that it is new; the placement needs an owner decision (Q-SET-1) |

Evidence that the design already assumes a patched Settings: the Updates
hold note says "Apex's Settings changes do not apply to 51.1 yet"
(`Updates.dc.html:109`).

## Layout and measurements

All values are logical px on the 1440x900 artboard.

### Shared window chrome

| Element | Measurement | Source |
| --- | --- | --- |
| Window, Appearance and Apex Desktop | 1100x730 at left 170, top 64 | `Appearance.dc.html:53`, `ApexDesktop.dc.html:216` |
| Window, Power, Fingerprint, Updates | 1220x756 at left 110, top 50 | `Power.dc.html:45`, `Fingerprint.dc.html:44` |
| Window radius | 14 (`radius.window`); Apex Desktop binds it to the Corner Radius setting | `ApexDesktop.dc.html:216` |
| Window shadow | `shadow.window`: `var(--shadow), 0 0 0 1px var(--border)` | |
| Sidebar | 252 wide, fill `--side`, right border 1px `--border` | `:52`/`:54` |
| Sidebar header | 47 tall, padding 0 8 0 16; "Settings" 14/700; Main menu button 32x32, radius 8, 16 px glyph `menu` | |
| Sidebar search | wrapper padding 0 10 8; field 32 tall, radius 8, fill `--btn`, padding 0 10, gap 8, 16 px search glyph, 13 px placeholder "Search" in `--dim` | |
| Panel list | padding 0 8 10, gap 3, `overflow:hidden` (clipped, see below) | |
| Panel row | 36 tall, padding 0 8, radius 8, gap 12, 13.5 px; weight 400, selected 600 with fill `--btn-h` | `ApexDesktop.dc.html:151` |
| Panel icon tile | 24x24, radius 7, coloured fill, white 16 px glyph, stroke 1.75 | `:150` |
| Separator | 1px `--border`, margin 6 8 | `:60` |
| Content header | 47 tall, padding 0 10; title centred across the pane, 14/700; window buttons 24x24 circles, fill `--btn`, gap 10, 14 px glyphs (maximize is 12 px in the static artboards, 14 px in Apex Desktop) | `:72-81` |
| Back button (subpages) | 32x32, radius 8, 16 px chevron, left of the header | `Fingerprint.dc.html:66` |
| Content scroller | padding 12 32 36; column max 620 centred; group gap 28 (Appearance, Apex Desktop) or 26 (Power, Users, Updates) | |
| Group title | h2 13.5/700, padding 0 4, gap 10 above the card | |
| Boxed list card | fill `--card`, radius 12 (`radius.pill-bar`), `shadow.card`, `overflow:hidden` | |
| Row | min-height 56, padding 10 14, gap 12; title 13.5/400; subtitle 12 `--dim`, 2 px below; divider 1px `--border` on every row after the first | `ApexDesktop.dc.html:193` |
| Switch | track 40x22 radius 11, off `--btn-h`, on `--accent`; knob 18x18 white, top 2, left 2 (off) or 20 (on), `shadow.knob`; both animate 200 ms `cubic-bezier(.2,.8,.2,1)` | `:154-155` |
| Segmented control | container padding 3, radius 10, fill `--btn`, gap 2; segment min-width 34, height 28, padding 0 10, radius 7, 12.5/600; selected fill `--view`, shadow `0 1px 3px rgba(0,0,0,.15)`, text `--fg`; others transparent, `--dim`; fill animates 150 ms | `:191` |
| Drop-down button | 32 tall, padding 0 10 0 12, radius 8, fill `--btn`, 13/600, 14 px chevron-down, gap 6 | `Power.dc.html:145` |
| Navigation row | as Row, trailing 16 px chevron-right at opacity .6 | `Power.dc.html:147-150` |

Sidebar order, all artboards except Fingerprint, with tile colours:

| Item | Tile | Item | Tile |
| --- | --- | --- | --- |
| Apex Desktop | `--accent` | Appearance | `#d56199` |
| (separator) | | Multitasking | `#2190a4` |
| Wi-Fi | `#3584e4` | Notifications | `#ed5b00` |
| Network | `#6f8396` | Search | `#6f8396` |
| Bluetooth | `#3584e4` | Apps | `#9141ac` |
| (separator) | | (separator) | |
| Displays | `#7d5ce6` (no token; not one of the nine accents) | Privacy & Security | `#3584e4` |
| Sound | `#e62d42` | Keyboard | `#6f8396` |
| Power | `#3a944a` | Mouse & Touchpad | `#6f8396` |
| (separator) | | System | `#6f8396` |

The list is clipped: at 730 px window height, Mouse & Touchpad (y 610-646 in
a 643 px area) is cut and System is hidden; at 756 px, System (649-685 in
669) is half visible, although Updates selects it. A real build scrolls.
The artboards omit upstream panels that must stay: Online Accounts,
Sharing, Color, Printers, Accessibility, Wacom (when present).

The glyphs are Apex Symbolic paths inlined in each artboard (`G` object,
`ApexDesktop.dc.html:137`); see [apex-symbolic.md](apex-symbolic.md).

### Appearance (23)

| Element | Measurement and copy |
| --- | --- |
| Style group | Title "Style". Card padding 20, 2-column grid, gap 20, `role=radiogroup` |
| Style option | Button, column, gap 10, label 13/600 "Default" or "Dark". Thumbnail full width, 16:10, radius 12; selected ring `0 0 0 3px var(--accent)`, else `0 0 0 1px var(--border)`; 150 ms. Thumbnail background is the selected wallpaper (light or dark variant). Inside: bar 9 tall full width (`rgba(250,250,252,.6)` / `rgba(12,12,16,.5)`); window at left 14 %, top 20 %, 60 x 58 %, radius 8, `#fafafb` / `#242428`, shadow `0 4px 12px rgba(0,0,0,.12)` / `.4`; dock at left 38 %, bottom 5 %, 24 x 9 %, radius 4, `rgba(250,250,252,.6)` / `rgba(34,34,38,.6)` (`Appearance.dc.html:90-105`) |
| Accent group | Title "Accent". Card padding 18 20, flex, `justify-content:space-between`, `aria-label="Accent colour"` |
| Swatch | 32x32 circle, fill the accent; selected ring `0 0 0 2px var(--card-solid, var(--win)), 0 0 0 4px <accent>`, 150 ms. Order and names: Blue, Teal, Green, Yellow, Orange, Red, Pink, Purple, Slate (`accent.options`) |
| Background group | Title "Background" with the current wallpaper name right-aligned, 12 `--dim` (for example "Facets"). Card padding 20, 4-column grid, gap 14 |
| Wallpaper tile | 16:10, radius 10; selected ring `0 0 0 3px var(--accent)` plus a 20 px `--accent` badge at right 6, bottom 6 with a 12 px white check (stroke 2.25); unselected `inset 0 0 0 1px var(--border)` |
| Wallpapers | Facets (light and dark SVGs, follows Style), Slate `#4d5868`, Sage `#8a9a86`, Sand `#d8cfc1`, Mist `#c7d1dd`, Ink `#1b1e25` (`Appearance.dc.html:23-28`) |
| Add tile | Last grid cell, 16:10, radius 10, ring `inset 0 0 0 1.5px var(--btn-h)`, 16 px plus glyph over "Add Picture…" 12/600 `--dim` |
| Caption | 12, line-height 1.45, `--dim`, padding 0 4: "Facets has a light and a dark version and follows the style. The others are single colours." |

### Power (24)

| Element | Measurement and copy |
| --- | --- |
| Top bar battery | Charging glyph plus "78%" at 12.5 px (`Power.dc.html:39-40`) |
| Battery card | Card padding 22 22 20, gap 16 |
| Icon tile | 52x52, radius 16, fill `color-mix(in srgb, var(--accent) 14%, transparent)`, 28 px battery-charging glyph in `--accent`, stroke 1.5 |
| Level | "78 %", 28/800 (`display-3`, `heavy`), letter-spacing -0.6, tabular |
| Charge line | 12.5 `--dim`: limit on "Plugged in · charging to 80 %, about 10 minutes left"; off "Plugged in · charging to 100 %, about 50 minutes left" |
| Level bar | 10 tall, radius 5, track `--btn-h`, fill 78 % `--accent`. With the limit on, a 2 px `--fg` marker at 80 %, 4 px above and below the track |
| Bar labels | 11.5 `--dim`, tabular: "0 %" left; right "Stops at 80 %" (limit on) or "100 %" |
| Battery group | "Limit Charging to 80 %" / "Keeps the battery healthy when the laptop stays plugged in", switch. "Show Battery Percentage", switch |
| Power Mode group | `role=radiogroup`. Rows are buttons, min-height 56, padding 10 14, gap 14. Radio 20x20 ring `inset 0 0 0 2px` (`--accent` selected, `--btn-h` otherwise) with a 10 px `--accent` dot. "Performance" / "High performance and power usage"; "Balanced" / "Standard performance and power usage"; "Power Saver" / "Reduced performance and power usage" |
| Graphics and Display group | "NVIDIA GeForce RTX 3050 Laptop GPU" / "Powered down until an app asks for it", trailing status chip: 24 tall, padding 0 10, radius 12, fill `--btn`, 7 px `--ok` dot, "Off" 12/600. "Lower Refresh Rate on Battery" / "60 Hz on battery, 90 Hz when plugged in", switch |
| Power Saving group | "Dim Screen" / "Reduce brightness when the computer is inactive", switch. "Screen Blank", drop-down "5 minutes". "Automatic Suspend" / "When on battery power", navigation row |

### Fingerprint enrollment (25)

Background page (Users, a System subpage with a back button):

| Element | Measurement and copy |
| --- | --- |
| Avatar | 96 circle, fill `--accent`, "A" 38/700 white |
| Name, role | "Apex" 20/800, letter-spacing -0.3; "Administrator" 12.5 `--dim`; column gap 10, padding-top 8 |
| Group | "Authentication & Login" 13.5/700 |
| Rows | min-height 52 (not 56), padding 0 14: "Password" with "••••••••" (13, letter-spacing 2, `--dim`); "Fingerprint Login" with "Not Set Up" (13 `--dim`); "Automatic Login" with an off switch |
| Scrim | `rgba(0,0,0,.28)` over the Settings window only (top bar and dock stay clear) |

Dialog:

| Element | Measurement and copy |
| --- | --- |
| Dialog | 440 wide, centred on the content pane (x = 110 + 252 + 968/2 = 846) and vertically on the artboard; radius 20 (`radius.toast`); fill `--win`; `shadow.window` |
| Header | 47 tall, padding 0 10: "Cancel" (32 tall, padding 0 12, radius 8, 13.5/600); title "Fingerprint" 14/700 centred; "Done" (32 tall, padding 0 14, radius 8, 13.5/600): disabled fill `--btn`, text `--faint`; enabled fill `--accent`, white |
| Body | padding 20 32 30, centred column, gap 22 |
| Ring | 184x184 SVG rotated -90°, r 86, stroke 6; track `--btn-h`; progress `--accent`, round cap, `stroke-dasharray` 540.35 (2π·86), offset `540.35 × (1 - p/100)`, 400 ms standard easing |
| Glyph disc | 132 circle; in progress fill `color-mix(in srgb, var(--accent) 12%, transparent)` with an 84 px fingerprint glyph (stroke 0.95) in `--accent`; done fill `--accent` with a 64 px white check (stroke 1.1); fill animates 300 ms |
| Title | 20/700, letter-spacing -0.2 |
| Status | `role=status`, 13.5, line-height 1.45, `--dim`, max-width 320 |
| Finger row | full width, min-height 52, padding 0 14, radius 12, fill `--card`, ring `0 0 0 1px var(--card-border)`: "Finger" / "ELAN fingerprint reader" and a drop-down "Right Index" |

### Apex Desktop (11)

| Element | Measurement and copy |
| --- | --- |
| Header card | Card padding 28 20 22, centred column, gap 14 |
| Logo tile | 72x72, radius 20, fill the current wallpaper (`.wp`), `shadow.lifted`; centred 26 px square, 3 px `--accent` border, radius 5, rotated 45° |
| Title | "Apex Desktop" h1 20/800, letter-spacing -0.3 |
| Version line | 12.5 `--dim`: "Version 45.20261008.131 · GNOME Shell 51.0 on Wayland · Fedora Linux 45" (`ApexDesktop.dc.html:93`). Must be computed (see Q-SET-6) |
| Groups | Top Bar, Dock, Windows, Effects; rows as in the shared table |

Every setting the panel exposes (`ApexDesktop.dc.html:156-179`, defaults
from `:131`):

| Group | Row title / subtitle | Control | Default | Key |
| --- | --- | --- | --- | --- |
| Top Bar | Translucent Top Bar / "Turns solid when a window is maximized" | Switch | On | New: `io.github.apex_linux.Desktop` `top-bar-translucent` (b) |
| Top Bar | Show Focused App Name | Switch | On | New: `top-bar-show-app-name` (b). Upstream Shell has no app name in the bar since GNOME 45 |
| Top Bar | Show Date in Clock | Switch | On | Stock: `org.gnome.desktop.interface clock-show-date` |
| Top Bar | Show Battery Percentage | Switch | On | Stock: `org.gnome.desktop.interface show-battery-percentage` (upstream default false; Apex overrides to true). Same key as the Power panel row |
| Top Bar | Hot Corner / "Touch the top-left corner to open the overview" | Switch | On | Stock: `org.gnome.desktop.interface enable-hot-corners` (also in Multitasking) |
| Dock | Icon Size | Segmented S / M / L | M | New: `dock-icon-size` (s: `small`, `medium`, `large` = 46, 54, 62 px; `spacing.fixed.dockIcon`). With Dash to Dock: `org.gnome.shell.extensions.dash-to-dock dash-max-icon-size` |
| Dock | Hide Behind Maximized Windows / "Move the pointer to the bottom edge to reveal it" | Switch | On | New: `dock-intellihide` (b). With Dash to Dock: `dock-fixed` false, `intellihide` true, `intellihide-mode` `MAXIMIZED_WINDOWS` (verify value names) |
| Dock | Show Running Indicators | Switch | On | New: `dock-show-running-indicators` (b). Dash to Dock has no plain on/off key for the dots |
| Dock | Show Trash | Switch | On | New: `dock-show-trash` (b). With Dash to Dock: `show-trash` |
| Windows | Corner Radius / "Maximized windows are always square" | Segmented 0 / 8 / 14 / 20 | 14 | New: `window-corner-radius` (u, one of 0, 8, 14, 20) |
| Windows | Titlebar Buttons | Segmented All / Close only | All | Stock: `org.gnome.desktop.wm.preferences button-layout`: All = `appmenu:minimize,maximize,close`, Close only = `appmenu:close` (upstream default is close only; Apex overrides) |
| Windows | Drag to Top Edge to Maximize | Switch | On | Stock: `org.gnome.mutter edge-tiling` (it also controls side tiling; see Q-SET-4) |
| Effects | Reduce Transparency / "Replace glass surfaces with solid colors" | Switch | Off | New: `reduce-transparency` (b). No upstream key known as of GNOME 48; check GNOME 51 |
| Effects | Reduce Motion / "Disable window and dock animations" | Switch | Off | Stock: `org.gnome.desktop.interface enable-animations`, inverted (also in Accessibility) |

The schema id `io.github.apex_linux.Desktop` is taken from the schema file
name drawn in a terminal error (`Terminal.dc.html:258`). It is evidence, not
a decision.

How the artboard previews each setting on the live desktop around the
window (`ApexDesktop.dc.html:197-217`):

| Setting | Drawn effect |
| --- | --- |
| Translucent Top Bar, Reduce Transparency | Bar is glass (`--bar`, blur 24 saturate 160 %) only when Translucent is on and Reduce Transparency is off; otherwise `--bar-solid`; 300 ms. Dock becomes `--panel-solid` with no blur when Reduce Transparency is on |
| Show Focused App Name | "Settings" label after Activities appears or hides |
| Show Date in Clock | "Wed Oct 21" appears or hides before "14:02" |
| Show Battery Percentage | "87 %" after the battery glyph |
| Icon Size | Dock icons 46, 54 or 62 px, 200 ms ease |
| Show Running Indicators | 4 px dot under Settings, `--fg` at .7 |
| Show Trash | Trash after Show Apps |
| Corner Radius | Settings window radius, 200 ms ease |
| Titlebar Buttons | Minimize and Maximize hide |
| Hot Corner, Hide Behind Maximized Windows, Drag to Top Edge, Reduce Motion | No drawn effect |

Dock content in this artboard: Files, Web, Mail, Calendar, Music, Text
Editor, Terminal, Software, Settings, then Show Apps and Trash
(`ApexDesktop.dc.html:199-203`). Every other artboard (23 of them) draws
Files, Web, Calendar, Music, Text Editor, Terminal, Bazaar, Settings, with
no Mail and Bazaar in place of Software (for example
`Appearance.dc.html:138-145`). The Software icon here
(`91d271bbd5c894bdd2ed6a39ef85e177`) is the same asset the "Apex Updates"
banner and the Power Off dialog use. Treat the Apex Desktop dock as stale
(Q-SET-2).

## States

### Shared

| State | Drawn | Notes |
| --- | --- | --- |
| Light, dark | Yes, `dark` tweak | `.apx-l` / `.apx-d` |
| Accent | Yes, nine options | `--accent` |
| Row hover, pressed | No | Use libadwaita defaults |
| Keyboard focus | No | Needs a focus ring on switches, segments, swatches and tiles (`shadow.focusRing`) |
| Narrow window | No | Upstream collapses the split view below 900 px; keep that |
| Search results | No | Stock |

### Appearance

| State | Trigger | Effect |
| --- | --- | --- |
| Default / Dark | Click a Style option | Whole desktop restyles |
| Accent | Click a swatch | Ring moves; accent changes everywhere |
| Wallpaper | Click a tile | Wallpaper, its name and both Style thumbnails change; Facets switches between light and dark variants with the style |
| Add Picture… | Click | Not drawn; stock file chooser |
| Custom pictures | Not drawn | Added pictures join the grid; stock lets users remove them |

### Power

| State | Drawn | Notes |
| --- | --- | --- |
| Charge limit on / off | Yes | Changes the charge line, the marker and the right bar label |
| Battery percentage on / off | Yes (switch only) | Top bar label should follow |
| Power mode | Yes, Balanced default | |
| Lower refresh rate on / off | Yes | |
| Dim screen on / off | Yes | |
| Discharging, full, not charging (held at limit), critical | No | Charge line copy for each is needed |
| No battery (desktop) | No | Hide Battery card and Battery group, as upstream |
| Performance unavailable | No | power-profiles-daemon can report it degraded or missing; upstream shows a reason |
| dGPU active | No | Chip needs an "On" state, ideally naming the app holding it |
| Battery health, multiple batteries, peripherals' batteries | No | Upstream lists device batteries; keep |

### Fingerprint

| State | Trigger | Copy |
| --- | --- | --- |
| Waiting for first touch | `progress` = 0 | Title "Right Index Finger"; status "Touch the fingerprint reader with your right index finger." |
| In progress | 0 < `progress` < 100 | Title "Right Index Finger"; status "Lift your finger, then touch the reader again with a slightly different part of it." Done disabled |
| Saved | `progress` = 100 | Title "Fingerprint Saved"; status "You can now unlock Apex and approve admin requests with your finger." Done enabled; check glyph |

Progress is `enroll-stage-passed` count / `num-enroll-stages` from fprintd.
States a build needs that are not drawn: retry results
(`enroll-retry-scan`, `enroll-swipe-too-short`, `enroll-finger-not-centered`,
`enroll-remove-and-retry`), `enroll-duplicate`, `enroll-data-full`,
`enroll-failed`, device disconnected or busy, a choice of finger before
the first touch, the list of enrolled fingers with delete, and the Users
page after enrollment ("Fingerprint Login" no longer "Not Set Up"). Upstream
`cc-fingerprint-dialog` has all of these.

### Apex Desktop

Every switch and segmented control is live (table above). States not drawn:
a setting unavailable because its backend is missing (for example the dock
extension disabled), a maximized window (to show the solid bar), and Reset
to Defaults.

## Hardware-dependent rows

Each row below must be detected at runtime. On the M7400QC all of them
must appear and work.

| Row | Shows when | Backend |
| --- | --- | --- |
| Limit Charging to 80 % | UPower reports the battery supports charge thresholds (`ChargeThresholdSupported`) | UPower `ChargeThresholdEnabled`; the kernel's `charge_control_end_threshold` on the battery (on ASUS through `asus-wmi` / `asus-nb-wmi`, which exposes the end threshold only). The "80" in the label, the marker and "Stops at 80 %" must come from the configured end threshold, not a constant. Check that UPower accepts a battery with an end threshold and no start threshold |
| NVIDIA GeForce RTX 3050 Laptop GPU status | A second GPU exists (switcheroo-control `HasDualGpu`) and its runtime PM state is readable | GPU name from switcheroo-control `GPUs`; state from `/sys/bus/pci/devices/<dGPU>/power/runtime_status` (`suspended` = Off). Needs runtime D3: the NVIDIA driver with `NVreg_DynamicPowerManagement=0x02` (default for Ampere and newer notebooks in recent drivers), or nouveau / NVK with runtime PM. The driver choice is Q-SET-3 |
| Lower Refresh Rate on Battery | The built-in panel offers at least two refresh rates at its current resolution | Mutter `org.gnome.Mutter.DisplayConfig` (`GetCurrentState`, `ApplyMonitorsConfig`), triggered by UPower `OnBattery`. The subtitle must be built from the modes ("{low} Hz on battery, {high} Hz when plugged in"); on the M7400QC panel that is 60 and 90. New key: `io.github.apex_linux.Desktop` `lower-refresh-rate-on-battery` (b, default true). Nothing upstream does this; it needs a small daemon or a gnome-settings-daemon patch, and must not overwrite the refresh rate the user picked in Displays |
| Fingerprint Login and the dialog | fprintd reports a default device | `net.reactivated.Fprint.Manager.GetDefaultDevice`. "ELAN fingerprint reader" must be the device `name` from fprintd (libfprint reports driver names such as "ElanTech Embedded Fingerprint Sensor", so the drawn string will differ). Confirm the M7400QC reader's USB id is supported by a libfprint driver (`elan`, `elanmoc` or `elanspi`) |
| Power Mode: Performance | power-profiles-daemon lists `performance` | Stock. On AMD it uses `amd-pstate` EPP and `platform_profile`, which `asus-wmi` exposes on ASUS laptops. The three modes drawn are the stock power-profiles-daemon modes; nothing ASUS-specific (no Silent or Turbo) is drawn |

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour | `--win`, `--view`, `--side`, `--fg`, `--dim`, `--faint`, `--border`, `--card`, `--card-border`, `--btn`, `--btn-h`, `--accent`, `--ok` (Power only), `--bar`, `--bar-solid`, `--bar-fg`, `--dock`, `--dock-border`, `--dock-sep`, `--panel-solid`, `--shadow`, `--wall`. Literals with no token: sidebar tile colours (accent hexes plus `#7d5ce6`), solid wallpapers (`#4d5868`, `#8a9a86`, `#d8cfc1`, `#c7d1dd`, `#1b1e25`), fingerprint scrim `rgba(0,0,0,.28)`, Style thumbnail fills, `--card-solid` (undefined, falls back to `--win`) |
| Type | `typography.family.ui`, `features.ui`; sizes `caption` 11.5, `small` 12, `small-plus` 12.5, `body` 13, `ui` 13.5, `heading` 14, `title-3` 20, `display-3` 28; 38 (avatar initial, no token); weights 400, 600, 700, 800 |
| Radius | `xs` 4 (marker 1, no token), `sm` 8, `md` 10, `pill-bar` 12, `window` 14, `lg` 16, `toast` 20; literals 7 (sidebar tiles, segments), 5 (logo square, level bar), 11 (switch track) |
| Shadow | `window`, `card`, `knob`, `lifted`, `dock`; segment `0 1px 3px rgba(0,0,0,.15)` (no token) |
| Glass | Top bar 24 / 160 %, dock 28 / 180 % (shared with the shell spec) |
| Motion | `easing.standard` with `duration.base` (switches), `duration.fast` (segments, rings), `duration.slow` (bar, glyph disc), `duration.progress` (fingerprint ring), `easing.ease` (icon size, window radius) |

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Window, header bars, boxed lists, rows, switches, drop-downs | Theme | libadwaita widgets; colours and radii via the Apex stylesheet. Fine-tuning row heights (56 vs libadwaita's) is CSS |
| Coloured sidebar tiles | Patch | `CcPanelList` rows show monochrome symbolic icons. Per-panel coloured tiles need code or per-row CSS names |
| Apex Desktop entry in the sidebar | Patch | gnome-control-center has no plugin API for third-party panels |
| Sidebar order | Patch | Appearance before Multitasking and Notifications, Search before Apps differ from upstream order |
| Appearance Style, Accent, wallpaper grid | Stock | GNOME 47+ |
| Solid-colour wallpapers | Theme | gnome-background-properties XML with `options` none and a `pcolor` (verify the chooser renders colour-only items) |
| Wallpaper name beside the heading; Add Picture… as the last tile | Patch (small) | Upstream puts Add Picture… in the group header and shows no name |
| Power Mode, Dim Screen, Screen Blank, Automatic Suspend, Show Battery Percentage | Stock | |
| Battery card (big percentage, bar with limit marker) | Patch | Upstream shows a plain battery row with a level bar |
| Limit Charging switch | Patch (small) or stock | GNOME 48 has the feature as a two-way choice; the drawn switch and copy are a change. Accepting upstream wording avoids the patch |
| NVIDIA status row | Patch | No upstream equivalent |
| Lower Refresh Rate on Battery | Patch plus new service | No upstream equivalent |
| Users page, Authentication & Login group | Stock | |
| Fingerprint dialog layout (ring, disc, finger row) | Patch | Upstream dialog has a different layout; behaviour is the same |
| Apex Desktop panel itself | Patch (new panel) | New C or Python panel, plus the keys it writes |
| Translucent / solid top bar, focused app name, running indicators | Patch | Shell extension or `js/ui/panel.js` change |
| Corner Radius | Patch, expensive | Client-side decorations draw their own corners; changing all windows means a compositor-side rounded clip in Mutter or an extension like Rounded Window Corners. It costs GPU time, needs care with shadows and fullscreen, and differs per toolkit (GTK 3, GTK 4, Qt, Electron, Xwayland) |
| Reduce Transparency | Patch | New key read by every Apex glass surface |
| Clock date, hot corner, titlebar buttons, edge tiling, Reduce Motion | Stock keys | Only the defaults change (vendor GSettings override) |

## Accessibility

*   Contrast: `--dim` on `--card` is about 4.7:1 in light, passes AA. White
    13.5/600 on `--accent` (Done button) is about 3.8:1 for Blue and lower
    for Yellow (`#c88800`) and Orange; it fails AA for small text. Use
    libadwaita's accent-on-background colour, or darken as the Polkit
    dialog does (`color-mix(in srgb, #000 25%, var(--accent))`).
*   `--faint` for the disabled Done label is exempt but must not be the only
    cue: set `aria-disabled` (drawn) and make it insensitive.
*   Focus order: sidebar search, panel list, header buttons, then groups top
    to bottom; in the dialog Cancel, Finger drop-down, Done. Escape cancels
    the dialog.
*   Names: switches use the row title (drawn); segmented controls are
    radiogroups named by the row title (drawn); swatches and wallpaper
    tiles are radios with colour or wallpaper names (drawn). The NVIDIA chip
    needs a name such as "GPU status: Off". The battery bar needs a level-bar
    role with value and the limit. The fingerprint ring has "Enrollment N
    percent complete" (drawn) and the status line is a live region (drawn).
*   Reduce Motion must also turn off the switch, ring and radius transitions
    here.
*   Large text: rows grow (min-height, not height); the 620 px column and
    segmented controls must wrap or scroll, not clip.

## Acceptance criteria

1.  The sidebar is 252 px wide at scale 1 and rows are 36 px tall with 3 px
    gaps; the selected row has `--btn-h` fill and 600 weight.
2.  Header bars of sidebar and content are 47 px; content titles are
    centred across the content pane.
3.  Content is a single column no wider than 620 px, centred, with 12 px top
    and 36 px bottom padding and 28 px (Appearance, Apex Desktop) or 26 px
    (Power, Users) between groups.
4.  Boxed-list rows are at least 56 px tall with 14 px side padding and a
    1 px `--border` between rows; switches are 40x22 with an 18 px knob.
5.  Choosing Dark in Appearance sets `color-scheme` to `prefer-dark`;
    choosing Default sets `default`. Both thumbnails show the current
    wallpaper.
6.  Each of the nine swatches sets `accent-color` to its name (`blue` …
    `slate`) and the selected swatch shows a 2 px gap and 2 px accent ring.
7.  Selecting Facets sets `picture-uri` and `picture-uri-dark` to the two
    Facets files; selecting a solid colour sets a colour-only background.
    The heading shows the selected name.
8.  On a machine whose battery has no charge threshold support, the Limit
    Charging row and the limit marker are absent. On the M7400QC they are
    present and the row writes UPower's charge threshold setting; after
    plugging in at 79 %, charging stops at the configured end threshold.
9.  With the limit on, the bar shows a marker at the configured end
    threshold and the right label reads "Stops at N %".
10. On a machine with one GPU, the Graphics and Display group shows no GPU
    row. On the M7400QC the row names the dGPU and the chip reads "Off"
    while `runtime_status` is `suspended`, and changes within 2 s when an
    app starts on the dGPU.
11. On a panel with one refresh rate, Lower Refresh Rate on Battery is
    absent. On the M7400QC, unplugging switches the internal panel to
    60 Hz within 2 s and plugging in restores 90 Hz; the user's Displays
    choice is restored when the switch is off.
12. Power Mode rows set power-profiles-daemon's `ActiveProfile`; Performance
    is hidden or explained when not offered.
13. Show Battery Percentage in Power and in Apex Desktop are the same key:
    toggling one updates the other and the top bar at once.
14. Fingerprint enrollment advances the ring by one stage per accepted
    touch, shows the drawn copy at 0, in progress and done, and enables Done
    only when enrollment completes. A retry result shows a distinct
    message without advancing.
15. With no fingerprint reader, Fingerprint Login is absent from the Users
    page.
16. After enrollment, the lock screen and the Polkit dialog accept the
    finger (`pam_fprintd` enabled through authselect `with-fingerprint`).
17. Every Apex Desktop row writes the key listed in the table; `gsettings
    get` shows the new value immediately and the shell applies it without
    logging out.
18. Dock Icon Size S, M, L give 46, 54, 62 px icons.
19. Corner Radius 0, 8, 14, 20 changes the radius of non-maximized windows
    of GTK 4, GTK 3 and Xwayland apps; maximized and tiled windows stay
    square.
20. Titlebar Buttons All shows minimize, maximize and close; Close only
    shows close only.
21. Reduce Transparency makes the top bar and dock opaque (`--bar-solid`,
    `--panel-solid`) and removes their blur.
22. The Apex Desktop version line shows the running image version, the
    running GNOME Shell version, the session type and the base OS, read at
    runtime.
23. The default dock matches the other 23 artboards (Q-SET-2), not the Apex
    Desktop artboard, until the owner decides otherwise.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

*   **Q-SET-1** Where does the Apex Desktop panel live: a gnome-control-center
    patch (first sidebar row, as drawn) or extension preferences / a
    separate app? The patch is carried on every GNOME release; the
    Updates hold note (`Updates.dc.html:109`) shows the design already
    expects such delays.
*   **Q-SET-2** Default dock apps. `ApexDesktop.dc.html:199-203` has Mail and
    Software; 23 other artboards have Bazaar and no Mail. Which mail app,
    if any? Is GNOME Software shipped at all (its icon is reused for
    "Apex Updates")?
*   **Q-SET-3** NVIDIA driver: proprietary (akmods, signing for Secure
    Boot, image build cost) or nouveau / NVK. The "Powered down" row
    depends on runtime PM working with the chosen driver.
*   **Q-SET-4** "Drag to Top Edge to Maximize" maps to `edge-tiling`, which
    also controls side tiling. Rename the row ("Edge Tiling") or add a new
    key that only blocks top-edge maximize (patch)?
*   **Q-SET-5** Corner Radius for all windows is expensive (see Build
    classification). Accept the cost, limit it to windows Apex can style
    (libadwaita apps through CSS), or drop the setting?
*   **Q-SET-6** The version line and Updates use "45.20261008.131",
    "GNOME Shell 51.0", "Fedora Linux 45". These must be computed; the
    version scheme itself is Q-UPD-1 in
    [updates-and-rollback.md](updates-and-rollback.md).
*   **Q-SET-7** Fingerprint nav (`Fingerprint.dc.html:157`) has a top-level
    Users item and drops Mouse & Touchpad; the page header has a back
    button, which means a System subpage. Upstream (GNOME 46+) puts Users
    under System. Which is intended?
*   **Q-SET-8** "You can now unlock Apex …" (`Fingerprint.dc.html:173`):
    "Apex" is both the distro and the sample user name. Use "unlock the
    computer"?
*   **Q-SET-9** Spelling: "Accent colour" (aria-label) and "single
    colours" (caption) are British; the rest ("colors" in Apex Desktop,
    GNOME strings) is US. Pick one.
*   **Q-SET-10** Upstream Power rows the artboard drops: Automatic Power
    Saver (low battery), Automatic Screen Brightness (only with a light
    sensor), Power Button Behavior. Keep them (recommended) or remove
    (patch)?
*   **Q-SET-11** Percent spacing: "87 %" (`ApexDesktop.dc.html:45`), "78 %"
    (`Power.dc.html:83`) but "78%" in the Power top bar (`Power.dc.html:40`).
    GNOME uses the locale's format; follow it.
*   **Q-SET-12** Reduce Motion subtitle says "window and dock animations",
    but `enable-animations` turns off all animations. Change the copy or
    add a narrower key?
