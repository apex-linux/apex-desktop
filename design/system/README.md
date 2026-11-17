# Apex design system

This directory holds the design tokens extracted from the design canvas "Apex
Fedora Mockups" and the rules the canvas implies. `tokens.json` holds the
values; this file explains them.

The canvas is the source of truth. Every value in `tokens.json` names the
artboard files it comes from (in `../canvas/project/`). Where artboards
disagree, `tokens.json` keeps the majority value in `value` and lists the
others in `conflicts`. It does not pick a winner; open conflicts are tracked in
`../OPEN-QUESTIONS.md`.

## Contents

*   [How the canvas defines tokens](#how-the-canvas-defines-tokens)
*   [Colour](#colour)
*   [Accent](#accent)
*   [Typography](#typography)
*   [Radius](#radius)
*   [Spacing and fixed sizes](#spacing-and-fixed-sizes)
*   [Shadow](#shadow)
*   [Glass](#glass)
*   [Motion](#motion)
*   [Icons](#icons)
*   [Fixed scenes](#fixed-scenes)
*   [Contrast](#contrast)
*   [Mapping to GNOME](#mapping-to-gnome)

## How the canvas defines tokens

Each artboard is an HTML prototype. Most of them put the whole UI inside an
element with the class `apx` plus either `apx-l` (light) or `apx-d` (dark),
chosen by the artboard's `dark` tweak. Those two classes define CSS custom
properties such as `--win`, `--panel` and `--dock`. The accent is a separate
custom property, `--accent`, set inline from the `accent` tweak.

Each artboard carries its own copy of the two classes. That is why values can
drift between artboards, and why `tokens.json` records per-artboard sources.

Four artboards do not use the classes at all: Boot splash, Disk unlock, the
GDM greeter and the lock screen. Their literal values are under `fixedScenes`.

All sizes are logical pixels on a 1440x900 artboard. The canvas was drawn for
the owner's laptop, whose 2880x1800 panel runs at scale 2, so there one
logical pixel is two device pixels. Apex targets other machines too: build in
logical pixels and test at scale 1, 1.25, 1.5 and 2.

## Colour

72 colour roles, in nine groups. Each role has a light and a dark value.

| Group | Roles | What it is for |
| --- | --- | --- |
| `surface` | `--win`, `--view`, `--side`, `--head`, `--card`, `--card-border`, `--pop`, `--msg-card`, `--shot`, `--file` | Backgrounds inside application windows. `--win` is the window and header area, `--view` the content view, `--side` the sidebar, `--card` boxed lists. |
| `content` | `--fg`, `--dim`, `--faint`, `--border` | Text and hairlines. `--dim` is secondary text, `--faint` tertiary text and placeholders. |
| `control` | `--btn`, `--btn-h`, `--sel`, `--row-h`, `--bar-hover` | Flat button fill, hover or selected fill, selected list row, hovered shell row. |
| `shell` | `--bar`, `--bar-solid`, `--bar-fg`, `--dock`, `--dock-border`, `--dock-sep`, `--panel`, `--panel-solid`, `--panel-border`, `--pill`, `--pill-border`, `--scrim`, `--folder`, `--folder-back`, `--shadow`, `--wall` | GNOME Shell surfaces. Translucent tints (`--bar`, `--dock`, `--panel`, `--scrim`) sit on top of live blur; `--panel-solid` is the opaque variant for modal dialogs and popup menus. |
| `status` | `--err`, `--warn`, `--warn-bg`, `--ok`, `--st-needs`, `--st-fail`, `--mod`, `--add`, `--exec` | Error, warning and success colours, terminal session states, version-control and debugger marks. |
| `terminal-in-scene` | `--term-bg`, `--term-fg`, `--term-user`, `--term-path`, `--term-key` | A terminal window drawn inside another artboard (Polkit, Rollback, Screenshot, Tiling). |
| `terminal-app` | `--t-*` | The Terminal app's own palette (Terminal artboards and the Overview thumbnail). |
| `syntax` | `--k`, `--s`, `--f`, `--n`, `--ty`, `--c`, `--line`, `--md-head`, `--md-code` | Code highlighting in Apex Code and Markdown in Text Editor. |
| `icon-sheet` | `--grid`, `--key`, `--dockbg` | Presentation-only overlays on the icon sheets. Not for the product. |

Rules the values imply:

*   Light mode is near-white with a faint blue-grey cast (`#fafafb`,
    `#f1f1f4`); dark mode is neutral grey (`#242428`, `#1e1e21`). Text is
    never pure black or pure white (`#1d1d21`, `#f4f4f6`).
*   Secondary and tertiary text are the foreground at reduced alpha
    (light `.62` and `.4`, dark `.64` and `.4`), not separate greys. Build
    them as alpha so they adapt to the surface under them.
*   Hairlines are tinted alpha too: `rgba(0,0,10,.09)` in light,
    `rgba(255,255,255,.08)` in dark.
*   Terminal and syntax colours reuse the GNOME palette (for example
    `#1c71d8`, `#26a269`, `#99c1f1`, `#8ff0a4`, `#dc8add`, `#ffa348`).

Main colour conflicts (full list in `tokens.json`):

*   `--dim` (light) is `.62` on 20 artboards and `.72` on 11 shell
    artboards (DateMenu, Desktop, EndSession, Indicators, Launcher, Overview,
    Polkit, Screenshot, Spotlight, Transients, WifiMenu). This looks like a
    deliberate "shell text is stronger on glass" split, but it is not named.
*   `--head`, `--card`, `--faint` and `--card-border` differ on DateMenu,
    Desktop, Overview or Spotlight.
*   `--panel` is more opaque on Launcher (`.86` light, `.82` dark).
*   `--warn` and `--warn-bg` differ between Updates, Rollback and Code.
*   `--err` (dark) is `#ff7b7b` in Code and `#ff7b63` in Polkit.
*   `--win` (dark) is `#1e1e21` on the four icon sheets instead of
    `#242428`.
*   Two terminal palettes: `--term-*` (terminal drawn in other artboards,
    background `#fcfcfd` / `#1c1c1f`) and `--t-*` (Terminal app, background
    `#ffffff` / `#1b1b1e`, green `#1b7a43` instead of `#26a269`).

## Accent

Nine accents, default Blue: Blue `#3584e4`, Teal `#2190a4`, Green `#3a944a`,
Yellow `#c88800`, Orange `#ed5b00`, Red `#e62d42`, Pink `#d56199`, Purple
`#9141ac`, Slate `#6f8396`. These are exactly the GNOME accent colours, so the
picker maps to the stock `org.gnome.desktop.interface accent-color` key.

One derived colour appears: `--accent-strong`, the accent mixed 75 % with
black (defined in `WifiMenu.dc.html`, computed inline in `DateMenu.dc.html`
and `Polkit.dc.html`). It is the canvas's own answer to white text on accent
fills, but only three artboards use it.

The canvas uses `--accent` both as a fill (selected tiles, switches, primary
buttons, focus rings) and as text (headings in the SPEC.md editor view). See
[Contrast](#contrast) for why those two uses need two colours.

## Typography

*   **UI family:** Inter (variable, `opsz` 14 to 32, weight 400 to 800),
    falling back to Adwaita Sans, then `system-ui`. Adwaita Sans is GNOME's
    default UI font since GNOME 48 and is derived from Inter, so the fallback
    is close; whether Apex ships Inter itself is an open question.
*   **Mono family:** JetBrains Mono 400 and 600, for terminals, code, hashes
    and `apexctl` output.
*   **Font features:** `'cv05', 'ss03'` on all UI text: Inter's lower-case l
    with a tail (cv05) and round quotes and commas (ss03). In GTK this is CSS
    `font-feature-settings` on the window; in GNOME Shell it is the
    `font-feature-settings` property in the shell theme, and both need to be
    tested because not every widget inherits it.
*   **Tabular figures:** `font-variant-numeric: tabular-nums` on clocks,
    percentages, sizes, counters and versions, so numbers do not jitter.
*   **Weights:** 600 is the default UI weight (labels, rows, buttons, top
    bar); indicator menu rows use 500. 700 for titles and app names, 800 for the wordmark, page titles and
    big numbers, 500 for text in password fields, 400 almost never. This is
    heavier than stock libadwaita, which uses 400 for body text.
*   **Sizes:** 13.5 px is the workhorse (top bar, rows), with 11, 11.5, 12,
    12.5, 13, 14 and 15 px around it, titles at 18, 20, 22, 24 and 28 px,
    display at 34 px and the lock clock at 118 px. The half-pixel steps map to
    whole device pixels at scale 2.
*   **Tracking:** negative only at large sizes: -0.2 px on dialog titles,
    -0.5 px on the wordmark and display text, -4 px on the lock clock.
*   **Smoothing:** grayscale antialiasing.

## Radius

| Token | Value | Use |
| --- | --- | --- |
| `hairline` | 2 px | Progress bars, small marks |
| `xs` | 4 px | Checkboxes, tiny chips |
| `sm` | 8 px | Header-bar icon buttons, path bar, list rows |
| `md` | 10 px | Linked and segmented controls |
| `pill-bar` | 12 px | 24 px top-bar buttons, cards, boxed lists |
| `window` | 14 px | Application windows, popup menus |
| `lg` | 16 px | Window-switcher tiles, notification banner |
| `card-lg` | 18 px | Wi-Fi network list, dialog buttons |
| `field` | 19 px | 38 px entries on greeter, lock and disk unlock |
| `toast` | 20 px | 40 px toasts, OSD, fingerprint dialog |
| `dock` | 24 px | Dock, Spotlight |
| `panel` | 26 px | Quick Settings, calendar, switcher, screenshot panel, modal dialogs |
| `circle` | 50 % | Avatars, round buttons |

Rule: controls are fully rounded pills (radius is half the height: 24 px
buttons get 12, 38 px fields get 19, 40 px toasts get 20). Containers step up
with size: rows 8, cards 12, windows 14, shell panels 26.

The SPEC.md excerpt on the canvas stops at the heading "2.7 Radii", so the
canvas never states the radius table itself; these values are measured.

## Spacing and fixed sizes

Spacing runs on a 2 px base. The common steps are 2, 4, 6, 8, 10, 12, 14,
16 and 18 px, with 28, 40 and 48 px for page-level gaps. Fixed sizes that
recur:

| Item | Size |
| --- | --- |
| Top bar height | 32 px, padding `0 8px` |
| Top-bar button | 24 px tall pill |
| App header bar | 47 px plus 1 px border |
| Dock | 10 px from the bottom, padding `5px 8px 3px`, icons 46, 54 (default) or 62 px |
| Sidebar width | 232 px (Files), 252 px (Settings), 272 px (Terminal) |
| Entry on lock surfaces | 38 px tall |
| Default window | 1240x762 at 100 px from the sides and 48 px from the top |

## Shadow

| Token | Value | Use |
| --- | --- | --- |
| `--shadow` (light) | `0 18px 50px rgba(20,30,60,.22), 0 2px 8px rgba(20,30,60,.10)` | Windows and shell panels |
| `--shadow` (dark) | `0 18px 50px rgba(0,0,0,.5), 0 2px 8px rgba(0,0,0,.3)` | Same |
| `window` | `var(--shadow), 0 0 0 1px var(--border)` | Windows get an outer hairline |
| `panel` | `var(--shadow), inset 0 0 0 1px var(--panel-border)` | Shell panels get an inner light edge |
| `dock` | `inset 0 0 0 1px var(--dock-border), 0 10px 30px rgba(0,0,0,.18)` | Dock |
| `card` | `0 0 0 1px var(--card-border), 0 1px 3px rgba(0,0,0,.05)` | Boxed lists |
| `focusRing` | `inset 0 0 0 2px var(--accent)` | Keyboard focus, selected tile |

Rule: glass surfaces get an *inner* highlight edge (`--panel-border`,
`--dock-border`, white at .6 to .65 in light mode); opaque surfaces get an
*outer* hairline (`--border`). The light shadow is tinted navy, not black.

## Glass

The canvas treats translucency as a first-class surface property. The table
comes from SPEC.md section 2.6, which the canvas draws as editor text in the
window-switcher artboard (`AltTab.dc.html`):

| Surface | Blur | Saturate | Tint | Matches the artboards? |
| --- | --- | --- | --- | --- |
| Top bar | 24 px | 160 % | `--bar` | Yes |
| Dock | 28 px | 180 % | `--dock` | Yes |
| Quick Settings, calendar, toast | 30 px | 180 % | `--panel` | Yes; the switcher, screenshot panel, banner, OSD and Launcher folder use it too |
| Spotlight | 34 px | 180 % | `--panel` | Yes |
| Overview scrim | 36 px | 150 % | `--scrim` | No: drawn as 40 px, 140 % |
| Launcher scrim | 40 px | 160 % | `--scrim` | No: drawn as 40 px, 140 % |
| Lock background | 30 px | 130 % | `rgba(8,10,20,.68)` light, `.34` dark | Yes |
| Lock password field | 20 px | none | `rgba(255,255,255,.18)` | Yes (greeter and lock) |

Conversion to GNOME Shell: CSS `blur(N)` is a Gaussian with sigma N logical
px. `Shell.BlurEffect` takes a radius in device px and uses sigma = radius /
2, so radius = 2 x N x scale. At scale 2: top bar 96, dock 112, panels 120,
Spotlight 136, overview 144, launcher 160, lock 120, lock field 80.

What this costs:

*   Stock GNOME Shell blurs only the lock screen and the overview background,
    and `Shell.BlurEffect` has no saturation. The canvas's own notes say
    saturation needs a patched `Shell.BlurEffect` ("patch 0003").
*   Live (`BACKGROUND` mode) blur behind the top bar, dock and every panel
    re-renders whenever what is behind changes. Large radii at scale 2 on an
    integrated Radeon GPU, with the NVIDIA GPU powered down, need a
    performance budget. The SPEC excerpt says a performance acceptance exists
    ("section 7"), but the canvas does not include it.
*   Overview and Launcher draw a blurred *wallpaper* (static), not live
    content. That is cheap; it is also different from what the SPEC table
    calls "live glass".

## Motion

The canvas specifies motion only through CSS transitions in the prototypes:

*   **Easing:** `cubic-bezier(.2,.8,.2,1)` (fast out, soft landing) for
    switches, progress, indicators and width changes; plain `ease` for
    hover fills; `ease-out` for the dock reveal.
*   **Durations:** 150 ms (hover, focus, disclosure), 200 ms (switch knob,
    fills, icon size), 250 ms (page indicator), 300 ms (tile preview, solid
    or glass bar), 400 ms (fingerprint ring), 1.1 s linear spinner.

Shell-level animations (overview, workspace switch, OSD, notifications) are
not drawn. Stock GNOME timings apply until the owner says otherwise. Every
animation must honour `org.gnome.desktop.interface enable-animations` and
reduced motion.

## Icons

Apex Symbolic is the symbolic icon set for the top bar, Quick Settings,
sign-in, the Settings and Files sidebars, header bars and the screenshot tool.
App icons are not part of it; the canvas says app icons "stay Colloid" (the
Colloid icon theme). The sheets state the drawing rules:

*   16 x 16 px grid with a 1 px keyline.
*   Stroke 1.75 px by default (the sheets also preview 1.5 and 2), round caps
    and round joins, `fill="none"`, colour `currentColor`.
*   Small closed shapes get solid cores (a sub-path with
    `fill="currentColor" stroke="none"`).
*   Inactive parts of a glyph (for example unfilled signal bars) are drawn at
    35 % opacity.

GTK recolours symbolic icons through fills, so stroked glyphs must be
converted to outlines when the theme is built. See
`../handoff/apex-symbolic.md`.

## Fixed scenes

*   **Boot and disk unlock:** black background, white Apex wordmark (a 26 px
    diamond with a 3 px stroke and 5 px radius, rotated 45 degrees, plus
    "Apex" at 34 px weight 800) in a 41 px row whose top is at y 408, and a
    160 x 3 px progress bar at y 489. The passphrase field replaces the bar: 250 x 38 px, radius
    19, white at .18, red ring `#ff8a8a` on error.
*   **Greeter and lock:** the wallpaper blurred 30 px with 130 % saturation
    under a `rgba(8,10,20,.68)` scrim (`.34` on the dark lock screen); white
    text; 38 px fields at white .18; focus is a 2 px white inner ring. The
    greeter always uses the light wallpaper.

## Contrast

Target: WCAG 2.2 AA, which is 4.5:1 for text under 18.66 px bold or 24 px
regular and 3:1 for large text and for non-text UI such as focus rings and
switch tracks. Measured from `tokens.json` (alpha colours composited on the
surface named):

| Pair | Light | Dark | Result |
| --- | --- | --- | --- |
| `--fg` on `--win` | 16.1 | 14.1 | Pass |
| `--dim` on `--win` | 4.67 | 6.60 | Pass |
| `--dim` on `--side` | 4.53 | 6.20 | Pass, light is at the edge |
| `--dim` .72 variant on `--win` | 6.50 | n/a | Pass |
| `--faint` on `--win` | 2.45 | 3.47 | Fails for text; only for placeholders, disabled text and decoration |
| `--warn` on `--side` | 4.36 | 8.74 | Light fails by a little |
| `--err` on `--win` | 5.86 | 6.09 | Pass |
| `--bar-fg` on `--bar` over the wallpaper | 11.3 or more | 12.7 or more | Pass on the default wallpaper |
| `--fg` on `--panel` over the wallpaper | 13.7 or more | 12.5 or more | Pass on the default wallpaper |
| White text on accent fill (13.5 px, 600) | 3.0 to 5.9 | same | Fails for every accent except Purple |
| Accent as text on `--win` | 2.9 to 5.7 | 2.6 to 5.1 | Fails for most accents |

Rules that follow:

1.  Use `--faint` only where WCAG exempts it (placeholders paired with a
    label, disabled controls, decoration). Never for information.
2.  Follow libadwaita's split between `accent_bg_color` (fills) and
    `accent_color` (a contrast-adjusted standalone colour for text and icons
    on neutral surfaces). Do not put body-size accent text on `--win`.
3.  White labels on accent fills (primary buttons, selected chips) need the
    accent darkened for the fill, or bold large text; libadwaita darkens the
    accent for fills in light mode. Measure every accent, not only Blue.
4.  Glass contrast depends on the wallpaper. The pairs above pass on the
    default wallpaper only. Shell text on glass must meet 4.5:1 over the
    worst case of any shipped wallpaper, and user wallpapers need a fallback
    (a more opaque tint, or the solid variant, when the computed contrast
    drops below target).
5.  Focus rings (2 px accent inner ring) must reach 3:1 against the surface
    they sit on.

## Mapping to GNOME

The tokens map to GNOME as follows. These are proposals; the handoff specs
confirm them per surface.

| Apex token | libadwaita (apps) | GNOME Shell theme |
| --- | --- | --- |
| `--win` | `window_bg_color` | n/a |
| `--view` | `view_bg_color` | n/a |
| `--side` | `sidebar_bg_color` | n/a |
| `--head` | `headerbar_bg_color` | n/a |
| `--card` | `card_bg_color` | n/a |
| `--fg` | `window_fg_color`, `view_fg_color` | `$fg_color` |
| `--dim` | `dim-label` opacity | `$fg_color` at alpha |
| `--border` | `borders` | `$borders_color` |
| `--pop` | `popover_bg_color` | n/a |
| `--accent` | `accent_bg_color` and `accent_color` | `-st-accent-color` |
| `--err`, `--warn`, `--ok` | `error_color`, `warning_color`, `success_color` | `$error_color` and so on |
| `--bar`, `--dock`, `--panel`, `--panel-solid`, `--scrim` | n/a | Shell theme stylesheet (`#panel`, `#dash`, `.quick-settings`, `.modal-dialog`) |

libadwaita lets a distribution set these colours only through a GTK style
sheet or by patching libadwaita; it deliberately has no theme API. How Apex
applies its app colours (patch libadwaita, ship a `gtk.css`, or accept stock
Adwaita colours and theme only the shell) is an open question.
