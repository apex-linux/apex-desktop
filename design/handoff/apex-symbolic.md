# Apex Symbolic icon set

## Summary

Apex Symbolic is the monochrome (symbolic) icon set for the shell and the
GNOME apps Apex themes. Four contact sheets on the canvas define it:

| No. | Artboard | Title | Size | Groups | Entries |
| --- | --- | --- | --- | --- | --- |
| 31 | `Glyphs.dc.html` | Apex Symbolic: contact sheet | 1440x1520 | 7 | 78 |
| 31b | `GlyphFamilies.dc.html` | Apex Symbolic: states and gaps | 1440x1600 | 7 | 74 |
| 31c | `GlyphActions.dc.html` | Apex Symbolic: everyday actions | 1440x1300 | 5 | 64 |
| 31d | `GlyphMore.dc.html` | Apex Symbolic: everywhere else | 1440x1600 | 5 | 75 |
| | | | | **24** | **291** |

The 291 entries carry 289 distinct icon names (two names appear on two
boards with identical paths) and 224 distinct drawings: 65 names reuse
another name's drawing. Every glyph is a 16x16 SVG drawn as up to three
path layers with stroke 1.75, round caps and joins, in `currentColor`.

The sheets state their scope in their intro lines (quoted exactly):

*   31, `Glyphs.dc.html:27`: "The symbolic glyphs for the top bar, Quick
    Settings, sign-in, the Settings and Files sidebars, header bars and the
    screenshot tool. App icons stay Colloid."
*   31b, `GlyphFamilies.dc.html:27`: "Every state the top bar, Quick
    Settings and the OSDs switch between, so a family never falls back to
    Adwaita halfway; then the gaps the icon scan found most visible in the
    shell and the toolkit. Fewer bars or arcs, then dimmed parts, then a
    slash for off. Board 31 holds the rest."
*   31c, `GlyphActions.dc.html:27`: "The next names check-icons found
    falling back to Adwaita, by where they show: the shell and its OSDs,
    every app through GTK and libadwaita, then Files and Settings. Names
    that mean the same thing share a drawing with board 31."
*   31d, `GlyphMore.dc.html:27`: "The 73 names the icon scan still found
    only in Adwaita, and the switch's two status shapes, which the shell
    otherwise takes from its own resources: the shell's last gaps first
    (mobile broadband, the accessibility menu, a window without an app
    icon, the switch marks for Show Status Shapes), then Settings, Files
    and setup, then the default apps. Parts are shared with boards 31 to
    31c, so every family stays one family. The shell's other own names
    reuse drawn glyphs: its screenshot UI's area, screen, window, pointer
    and close (board 19), its Screenshot button (camera-photo, board 17)
    and the notification expander (pan-down)."

The 31d count checks out: 73 Adwaita-only names plus `switch-on` and
`switch-off` is the 75 entries on the board. The "icon scan" /
"check-icons" tool and its result list are not in `.design/`; the counts
cannot be re-derived from it (see open questions).

Every name replaces the same name upstream: shipping
`network-wireless-signal-weak-symbolic.svg` in the Apex theme makes it win
over Adwaita's file of that name. A few names on the sheets are not
upstream names or are not the name the requesting code asks for; they are
flagged in the inventory and in open questions.

The full name list, grouped as the sheets group it, is in the
[appendix](#appendix-glyph-inventory).

## Upstream mapping

| Piece | Upstream component | Confidence |
| --- | --- | --- |
| Icon theme format | freedesktop Icon Theme Specification; `index.theme`, theme directories, `Inherits=` | High |
| Icon names | freedesktop Icon Naming Specification plus Adwaita's (`adwaita-icon-theme`) extra `*-symbolic` names | High for most; see flags |
| Lookup and recolouring in apps | GTK 4 `GtkIconTheme` (and GTK 3 for GTK 3 apps) | High |
| Lookup and recolouring in the shell | GNOME Shell `St` (`st-icon-theme.c`, a fork of GTK 3's `GtkIconTheme`; `st-texture-cache.c`) | High |
| Shell-owned icons | GNOME Shell's icon gresource (screenshot UI, some status icons) | Medium |
| Switch marks | GNOME Shell switch styling for the "Show Status Shapes" accessibility setting | Low; may be stylesheet assets, not icon lookups |
| App-bundled icons | GTK 4 and libadwaita gresources, Nautilus, GNOME Settings (`org.gnome.Settings-*-symbolic`), Ptyxis | Medium |
| Full-colour app icons | Colloid icon theme (third party, GPL-3.0) | High (stated on 31) |

### Ship it as a GTK icon theme

Package one theme, `Apex`, installed system-wide:

```
/usr/share/icons/Apex/
  index.theme
  icon-theme.cache
  scalable/actions/*-symbolic.svg
  scalable/apps/*-symbolic.svg
  scalable/categories/*-symbolic.svg
  scalable/devices/*-symbolic.svg
  scalable/emblems/*-symbolic.svg
  scalable/mimetypes/*-symbolic.svg
  scalable/places/*-symbolic.svg
  scalable/status/*-symbolic.svg
```

```ini
[Icon Theme]
Name=Apex
Comment=Apex Symbolic
Inherits=Adwaita,hicolor
Hidden=false
Directories=scalable/actions,scalable/apps,scalable/categories,scalable/devices,scalable/emblems,scalable/mimetypes,scalable/places,scalable/status

[scalable/actions]
Context=Actions
Size=16
MinSize=8
MaxSize=512
Type=Scalable
# ...one block per directory, same Size/MinSize/MaxSize/Type
```

The context directory does not affect lookup; it only keeps the tree
readable. Use Adwaita's context for each name so diffs against Adwaita stay
simple.

*   Build the cache at image build time: `gtk4-update-icon-cache -f -t
    /usr/share/icons/Apex`. On an image-based (bootc / ostree) system `/usr`
    is read-only at runtime, so the cache must ship in the image. A stale
    cache makes GTK and St fall back to scanning directories, which works
    but hides packaging mistakes.
*   Make Apex the default with a GSettings override, for example
    `/usr/share/glib-2.0/schemas/zz-apex.gschema.override` setting
    `[org.gnome.desktop.interface] icon-theme='Apex'`, then
    `glib-compile-schemas`. The GDM greeter runs as its own user, so check
    that the override (or a `gdm` dconf profile) reaches it.
*   Names with identical drawings ship as symlinks to one file.

### Coexisting with Colloid

The sheets keep app icons as Colloid. The theme the user selects is the one
in `icon-theme`, and lookups walk that theme's `Inherits=` chain. GTK and St
insert inherited themes depth-first: Apex, then the first parent and its own
parents, then the next parent. They then loop over themes on the outside and
candidate names (including generic fallbacks) on the inside. So the first
theme in the chain that has any candidate name wins, even if a later theme
has a more specific name. Confidence: medium-high; confirm against the GTK
and St versions shipped.

| Option | Chain | Undrawn symbolic names come from | Risk |
| --- | --- | --- | --- |
| A | `Apex -> Colloid -> Adwaita -> hicolor` | Colloid | High. Colloid ships its own `*-symbolic` icons in a different style. Every name Apex does not draw shows Colloid's drawing, and a family can mix three styles. Colloid's own `Inherits=` is also inserted before Adwaita. |
| B | `Apex -> Adwaita -> Colloid -> hicolor` | Adwaita | Medium. Symbolic fallbacks are consistent with GNOME. Adwaita's full-colour places, mimetypes and devices beat Colloid's, so Files shows Adwaita folders and file types; Colloid only wins for app icons Adwaita lacks. |
| C (recommended) | `Apex -> Adwaita -> hicolor`, with Colloid's full-colour directories copied into Apex at build time and every Colloid `*-symbolic` file dropped | Adwaita | Low at runtime. Costs: GPL-3.0 obligations, tracking Colloid releases, a larger package. The result is deterministic. |

Whatever the choice, the acceptance tests below treat a Colloid
`*-symbolic` file opened at runtime as a failure, just like an Adwaita one.

Some GTK versions fall back from `foo-symbolic` to a full-colour `foo` when
no theme has the symbolic name. With Colloid in the chain, a full-colour
Colloid icon can then appear where a symbolic one was asked for. Confidence:
low-medium; test it.

### How symbolic recolouring works, and why strokes must become fills

GTK (3 and 4) and GNOME Shell's St recolour a `*-symbolic.svg` the same
basic way. They load the SVG through librsvg with an injected stylesheet
that forces `fill` on shape elements to the foreground colour. The
stylesheet also has `.warning`, `.error` and `.success` classes for the
semantic colours. For example, GTK 3 wraps the icon with a rule of the form
`rect,circle,path { fill: <fg> !important; }`. GTK 4 renders the result as
an alpha mask and tints it at draw time. St takes the colours from the
theme node's `color`, `warning-color`, `error-color` and `success-color`.
Confidence: high for the fill-override mechanism. The exact selector list
varies by version.

Consequences for Apex Symbolic, whose glyphs are mostly strokes:

1.  A stroke is not recoloured. It keeps whatever `stroke` resolves to.
    `currentColor` has no CSS `color` context inside the loader, so it
    typically renders black, which is invisible on the dark top bar.
2.  A stroked path with `fill="none"` gets the forced fill. Open arcs (the
    Wi-Fi arcs, the volume waves) become filled chords.
3.  Only the selected elements are recoloured. Use `<path>` only, not
    `<line>`, `<polyline>`, `<polygon>` or `<ellipse>`.
4.  Opacity survives. `opacity` / `fill-opacity` on a path is kept, which
    is how Adwaita draws its dimmed parts; Apex's 35 % parts can use the
    same mechanism.

So every glyph must be converted at build time to filled outlines: stroke
to path, round caps and joins included. Newer GTK releases are reworking
symbolic rendering, and some may draw strokes natively. Do not rely on it:
the shell's St loader and GTK 3 apps still need fill-only files.

The cost of stroke-to-path, stated plainly:

*   Stroke weight is baked in. The sheets' 1.5 / 1.75 / 2 tweak becomes three
    separate builds; ship only 1.75.
*   The shipped SVGs are build output. Nobody can hand-edit them; edits go
    to stroked masters and the build reruns.
*   Converters approximate round caps and joins with curves. Small
    differences against the master need a render-diff check (below).
*   Overlapping strokes inside one layer (the X of `window-close`, the slash
    over a dimmed body) must be unioned. Two overlapping paths that each
    carry `opacity .35` would otherwise darken where they overlap.
*   `fill-rule="evenodd"` fills (gear hole in `emblem-system`, the "!"
    knock-out in `emblem-important`) must survive conversion, or be turned
    into an equivalent nonzero outline with boolean path operations.

### How GNOME Shell picks up symbolic icons

*   St reads `org.gnome.desktop.interface icon-theme` through `St.Settings`
    and resolves names with its own `StIconTheme` (forked from GTK 3), so
    the shell follows the same theme and `Inherits=` chain as apps.
    Confidence: high.
*   `St.Icon` actors (top bar indicators, Quick Settings toggles, OSDs, the
    dash, dialogs) request `*-symbolic` names. The theme node's `color`
    recolours them, and `-st-icon-style: symbolic` forces symbolic lookup.
    Panel icons are 16 px logical by the stock stylesheet.
*   The shell adds its own icon gresource to the search path. GTK-style
    resource paths behave as part of `hicolor`, so a same-named file in
    Apex wins over the shell's bundled one. Confidence: medium; verify for
    the screenshot UI names (`screenshot-ui-*-symbolic` in recent shells)
    and for whatever the shell requests for switch marks.
*   Assets the shell stylesheet references by URL (`resource:///...`) are
    not icon-theme lookups. If the switch status shapes are drawn that way,
    the Apex shell stylesheet has to point at Apex assets instead.
*   Changing `icon-theme` reloads icons live. No shell restart is needed.

## Layout and measurements

### Glyph drawing rules

Rules are read from the per-glyph markup (`Glyphs.dc.html:63-64`, identical
on all four sheets) and the rule line (`Glyphs.dc.html:28`): "16 px grid ·
1 px keyline · {{ swLabel }} px stroke, round caps and joins · solid cores
for small closed shapes · inactive parts at 35 %".

| Rule | Value | Evidence |
| --- | --- | --- |
| Canvas | `viewBox="0 0 16 16"` | `Glyphs.dc.html:63` |
| Grid | 16 units; the overlay draws lines at every integer 0 to 16 | `Glyphs.dc.html:183` |
| Keyline | `M1 1H15V15H1z`: 1 unit inset, 14x14 live area | `Glyphs.dc.html:61` |
| Stroke | 1.75 units default; tweak 1.5 / 1.75 / 2 | `Glyphs.dc.html:74`, `:171` |
| Caps and joins | `stroke-linecap="round"`, `stroke-linejoin="round"` | `Glyphs.dc.html:63` |
| Colour | `currentColor` for stroke and fill | `Glyphs.dc.html:63` |
| Default fill | `fill="none"` on the glyph | `Glyphs.dc.html:63` |
| Layer order | 1. `o` (inactive, stroked, `stroke-opacity=".35"`); 2. `d` (active, stroked); 3. `f` (solid, `fill="currentColor" stroke="none" fill-rule="evenodd"`) | `Glyphs.dc.html:63` |
| Solid sub-shapes | Small closed shapes are drawn in `f` as fills, never as thick strokes: dots, lock bodies, the microphone capsule, battery level bars, lens circles, the speaker cone | inventory |
| Knock-outs | Holes inside a solid shape use `evenodd` subpaths: `emblem-system`, `system-run`, `applications-system` (gear hole), `emblem-important` ("!" cut out) | `Glyphs.dc.html:102`, `GlyphMore.dc.html:522` |
| Inactive parts | Same geometry at 35 % stroke opacity: weaker Wi-Fi arcs, cellular bars, volume waves | `GlyphFamilies.dc.html:100` |
| Off state | A full-opacity slash `M2.5 2.5l11 11` over the whole glyph at 35 %; no gap is cut around the slash | `GlyphFamilies.dc.html:140` |
| "Acquiring" state | The whole glyph at 35 %, sometimes with three 0.9-radius dots | `GlyphFamilies.dc.html:117-121`, `:363-367` |
| Error / no route | A short bar `M13.4 8.6v2.4` and a 0.8-radius dot at the lower right | `GlyphFamilies.dc.html:124-128` |
| Offline | A small x `M11.6 10.4l2.4 2.4M14 10.4l-2.4 2.4` at the lower right | `GlyphFamilies.dc.html:131-135` |

Ladder for state families, as the 31b intro puts it: fewer bars or arcs,
then dimmed parts, then a slash for off.

Battery level bars follow one formula: the bar runs from x 3.5 to
x = 4 + (level - 5) / 15 + 0.5. That is width 1.33 at 10 %, 4 at 50 %,
7.33 at 100 %; it is 3 units tall (y 6.5 to 9.5) with 0.5 corner radius.
The values on 31 (`h5` for 80 %, `h1` for 20 %) and 31b agree.

Keyline overshoot: 73 of 291 entries reach outside the 14x14 keyline by up
to 0.38 units once half the stroke is counted. The worst are the battery
family (x 0.62 to 15.5), `camera-photo` and `computer` (x 0.62 to 15.38).
None leaves the 16x16 canvas. The keyline is a soft guide, not a hard
clip.

### Optical sizes

The sheets define a single 16 px master. Each card shows it at 40 px (2.5x,
so the stroke renders 4.375 px) and again at 16 px in the corner
(`Glyphs.dc.html:64`, opacity .9). There are no 24 or 32 px variants. GTK
scales one scalable SVG uniformly, so a 64 px empty-state icon gets a 7 px
stroke.

Other artboards draw the same 16-unit glyphs with compensated strokes: thin
at large sizes, heavy at small sizes. The scan below lists them. If those
are meant to ship, they need optical-size assets: a second scalable
directory, for example `Size=64 MinSize=24 MaxSize=512`, holding redrawn
large variants, which GTK picks by requested size. That doubles the
drawing work for every affected name.

### Sheet layout (for rebuilding the sheets, not for shipping)

| Element | Value |
| --- | --- |
| Board | 1440 wide; padding 56 / 64; column flex, gap 40; `--win` background |
| Title | 34px / 800, letter-spacing -.6px |
| Intro | 15px, line-height 1.5, `--dim`; max-width 700 |
| Rule line | 12.5px / 600, `--dim` |
| Top bar preview caption | "At 16 px in the top bar", 12px / 600, `--dim` |
| Top bar previews | Two tiles 236x48, radius 12, gap 10, ring `0 0 0 1px var(--border)`; bar 32 tall at top 8, padding 0 14, gap 12, right-aligned, 13.5px / 600; light bar `rgba(250,250,252,.45)`, text `#16161a`; dark bar `rgba(12,12,16,.4)`, text `#f6f6f8`; both `blur(24px) saturate(160%)`; battery label "87 %" with gap 5 |
| Group heading | 15px / 700; count 12.5px / 600 `--dim`; gap 8 |
| Group grid | 15 columns, gap 8; section gap 12 |
| Card | 80 tall, radius 12, `--card`, shadow `0 0 0 1px var(--card-border), 0 1px 3px rgba(0,0,0,.05)` |
| Glyph | 40x40 centred; 16x16 copy at right 7, bottom 7, opacity .9 |
| Caption | 11.5px / 600, line-height 1.3, centred, gap 6 above |
| Grid overlay | 40x40; lines stroke .06 `--grid`; keyline stroke .08 `--key` |

### Other artboards that break the stroke rule

A scan of every other artboard for inline SVGs with `viewBox="0 0 16 16"`
and a `stroke-width` other than 1.75 finds the entries below. "Visual" is
stroke x size / 16, the rendered line width in logical px; the sheet
default renders 1.75 at 16 px.

| Location | Size | Stroke | Visual | Glyph |
| --- | --- | --- | --- | --- |
| `Appearance.dc.html:125` | 12 | 2.25 | 1.69 | check mark |
| `Code.dc.html:55` | 12 | 1.9 | 1.43 | chevron down |
| `Code.dc.html:61` | 16 | 1.6 | 1.6 | folder |
| `Code.dc.html:70` | 16 | 1.6 | 1.6 | sparkle |
| `Code.dc.html:81` | 16 | 1.6 | 1.6 | view switcher (`{{ v.d }}`) |
| `Code.dc.html:90` | 16 | 1.6 | 1.6 | row icons (`{{ t.icon }}`) |
| `Code.dc.html:157` | 11 | 2 | 1.38 | chevron down |
| `Code.dc.html:183-184` | 14 | 1.9 | 1.66 | chevrons up and down |
| `Code.dc.html:185` | 13 | 1.9 | 1.54 | close |
| `Code.dc.html:274` | 14 | 2 | 1.75 | check mark |
| `Code.dc.html:298` | 16 | 1.6 | 1.6 | `{{ hi.d }}` |
| `DateMenu.dc.html:50` | 48 | 1.2 | 3.6 | notifications bell (empty state) |
| `DateMenu.dc.html:62` | 12 | 2 | 1.5 | close |
| `Desktop.dc.html:32` | 10 | 2.2 | 1.38 | window minimize |
| `Desktop.dc.html:33` | 10 | 2 | 1.25 | window maximize |
| `Desktop.dc.html:34` | 10 | 2.2 | 1.38 | window close |
| `EndSession.dc.html:61` | 26 | 1.5 | 2.44 | power |
| `Files.dc.html:118`, `FilesList.dc.html:118`, `FilesSearch.dc.html:118` | 64 | 1.1 | 4.4 | empty-state glyph (`{{ emptyGlyph }}`) |
| `Fingerprint.dc.html:104` | 64 | 1.1 | 4.4 | check mark |
| `Fingerprint.dc.html:107` | 84 | 0.95 | 4.99 | fingerprint |
| `Indicators.dc.html:71` | 12 | 1.9 | 1.43 | chevron |
| `Indicators.dc.html:99` | 14 | 1.9 | 1.66 | `{{ shareGlyph }}` |
| `Indicators.dc.html:106` | 14 | 1.9 | 1.66 | `{{ p.glyph }}` |
| `Launcher.dc.html:73` | 12 | 2 | 1.5 | close |
| `Polkit.dc.html:89` | 28 | 1.5 | 2.63 | `dialog-password` shield |
| `Power.dc.html:81` | 28 | 1.5 | 2.63 | battery charging |
| `Spotlight.dc.html:50` | 10 | 2.2 | 1.38 | close |
| `Spotlight.dc.html:94` | 12 | 2.2 | 1.65 | check mark |

Not on the 16 grid, so not counted: `Tiling.dc.html:89` (64 viewBox, 1.5),
`Tiling.dc.html:98` (22x26 pointer, 1.6), `Files*.dc.html:144` and `:184`
(64 viewBox folders, 1.5), `Spotlight.dc.html:66` (32 viewBox, 1.5),
`Fingerprint.dc.html:98` (184 viewBox ring, 6) and `CodeIcon.dc.html`
(128 viewBox app icon, 10).

## States

### Sheet tweaks

| Tweak | Options | Default | Effect |
| --- | --- | --- | --- |
| `stroke` | 1.5, 1.75, 2 | 1.75 | `stroke-width` on every glyph and the top bar previews; also the rule-line text |
| `grid` | on / off | off | Grid and keyline overlay behind each 40 px glyph |
| `dark` | on / off | off | Swaps `.apx-l` for `.apx-d` |

The top bar previews show different names per sheet (`bar:` at
`Glyphs.dc.html:189`, `GlyphFamilies.dc.html:650`, `GlyphActions.dc.html:570`,
`GlyphMore.dc.html:647`). They render only the `d` and `f` layers, and the
first slot only `d`, so some previews are wrong:

*   31b: `network-wireless-signal-ok` loses its dimmed outer arc,
    `audio-volume-low` loses its dimmed wave, and `power-profile-balanced`
    loses its needle dot.
*   31c: `network-error` shows only the "!" without the dimmed arcs.

The `f` path in the previews also lacks `fill-rule="evenodd"`.

### Icon states the set models

The state families, as drawn:

| Family | Names drawn | Distinct drawings |
| --- | --- | --- |
| Wi-Fi | `network-wireless`, `-signal-excellent/good/ok/weak/none`, `-acquiring`, `-no-route`, `-offline`, `-disabled`, `-encrypted`, `-hotspot` | `excellent`, `good` and `network-wireless` are one drawing |
| Cellular | `network-cellular`, `-connected`, `-signal-excellent/good/ok/weak/none`, `-acquiring`, `-disabled`, `-offline` | the first three are one drawing |
| Wired | `network-wired`, `-disconnected`, `-acquiring`, `-no-route` | **all four are one drawing** |
| Generic network | `network-error`, `network-offline`, `network-vpn`, `-acquiring`, `-disabled`, `network-transmit-receive` | distinct |
| Battery | `battery-level-0` to `-100` in tens, `-N-charging` for 0 to 90, `battery-level-100-charged`, `battery`, `battery-low`, `battery-caution`, `battery-action` | **all ten charging levels are one drawing (bolt, no level)**; `-100-charged` equals `-100` |
| Volume | `audio-volume-muted`, `-low`, `-medium`, `-high`, `-overamplified` | `medium`, `high` and `overamplified` are one drawing |
| Microphone | `audio-input-microphone`, `microphone-sensitivity-high/medium/low/muted` | `high`, `medium` and `low` are one drawing |
| Bluetooth | `bluetooth-active`, `-acquiring`, `-disabled` | distinct |
| Power profiles | `power-profile-power-saver`, `-balanced`, `-performance` | distinct (needle left, up, right) |
| Thunderbolt | `thunderbolt`, `-acquiring` | distinct |
| Night light, airplane, touchpad, camera, location, user tracking | on and `-disabled` / off forms | distinct, except location has no off form |

### States a real build needs that the sheets do not draw

Likely runtime requests not on any sheet (examples to confirm by runtime
capture; confidence medium):

*   `battery-level-N-charging` with a visible level, and a charged mark.
*   Wired disconnected, acquiring and no-route glyphs that differ from
    connected.
*   `audio-speakers-symbolic` (sound output device),
    `location-services-disabled-symbolic`, `battery-missing-symbolic`.
*   `process-working-symbolic` (GTK spinner fallback).
*   GTK emoji chooser sections `emoji-recent-symbolic` and
    `emoji-symbols-symbolic`; 31d draws the other eight.
*   The weather set beyond showers (`weather-clear`, `-few-clouds`,
    `-overcast`, `-fog`, `-snow`, `-storm`, the `-night` forms). The
    calendar offers "Select Weather Location…" (`DateMenu.dc.html:99`).
*   On-screen keyboard icons, if the OSK is in scope.
*   libadwaita's own `adw-*-symbolic` resource icons, for example
    expander arrows and external-link marks.
*   GNOME Settings panel icons under their app-specific names
    (`org.gnome.Settings-*-symbolic`). Read them from the installed panels'
    `.desktop` files.
*   Hover, pressed, disabled and selected states need no extra assets.
    Widgets change `color` and opacity, and recolouring follows.

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour (sheet) | `--win` (dark `#1e1e21` here conflicts with the majority `#242428`; tokens.json records it), `--fg`, `--dim`, `--border`, `--card`, `--card-border` |
| Colour (sheet overlay) | `--grid`, `--key` (icon-sheet group) |
| Colour (glyphs) | none; `currentColor` only |
| Colour (top bar preview) | literals `rgba(250,250,252,.45)`, `#16161a`, `rgba(12,12,16,.4)`, `#f6f6f8`; card shadow literal `rgba(0,0,0,.05)`; no tokens |
| Type | display-2 34px, subtitle 15px, ui 13.5px, small-plus 12.5px, small 12px, caption 11.5px; weights heavy 800, bold 700, semibold 600 |
| Radius | pill-bar 12px (cards and preview tiles) |
| Glass | top bar preview `blur(24px) saturate(160%)` |
| Icon | `icon.grid` 16 x 16, `icon.stroke.default` 1.75, options 1.5 / 1.75 / 2, round caps and joins, `fill`, `color` |
| Motion | none |

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| `Apex` icon theme (index.theme, SVGs, cache) | theme | Icon theme files only |
| Default `icon-theme='Apex'` | theme | GSettings override |
| Stroke-to-fill build step | theme (tooling) | Build-time only; nothing changes upstream |
| Overriding shell-bundled icons by name (screenshot UI, expander) | theme | A same-named file in Apex wins over hicolor-level resources; verify |
| Switch status shapes | theme (shell stylesheet) | Probably stylesheet assets, not icon lookups; then the Apex shell CSS must reference Apex files |
| Colloid coexistence (option C) | theme (packaging) | Copy and filter Colloid at build time |
| `apex-desktop`, `system-rollback` | patch | No upstream code requests these names; the Apex Desktop panel and the Apex update UI must request them |
| `go-next-arrow` | patch or rename | Not a known upstream name; rename to what the unlock prompt requests, or patch the prompt |
| `selection-area`, `window`, `pointer` | theme (rename) | Ship under the shell's screenshot UI names too |
| Files bookmarks `briefcase` ("Projects"), `globe` ("Public"), `text-x-script` ("Code") | patch | Nautilus picks sidebar icons from special-directory type; custom bookmarks get `folder-symbolic`. Low confidence; check whether GIO metadata can set a custom symbolic icon |
| Collapsed state families (charging, wired, mic, volume) | theme (redraw) | Design work; no code change |
| Optical-size variants | theme | A second size directory; costly to draw |
| Flatpak apps | theme (packaging) | They do not see host themes reliably; needs a Flatpak icon-theme extension; out of scope for the drawn surfaces |
| Recolouring, semantic colours | stock | GTK and St already do this |

## Accessibility

*   Contrast, from the sheet colours: `--fg` on `--win` is 16.1:1 light and
    15.1:1 dark. Parts at 35 % are 2.16:1 light and 3.03:1 dark, below the
    3:1 non-text minimum on light. That is acceptable only because a dimmed
    part never carries the state on its own; the active part does. Keep it
    that way when redrawing.
*   On the glass top bar, contrast depends on the wallpaper. That belongs in
    the top bar spec. Icons follow the bar's text colour.
*   State must not depend on a glyph alone where the family collapses. The
    wired states, the charging levels and the microphone levels currently
    differ only in text (tooltips, Quick Settings subtitles).
*   Icons have no accessible names. The widget provides them. For
    icon-only buttons that Apex adds, use the sheet labels (for example
    "Show Password", "Hide Password") as the accessible name and tooltip.
*   High contrast: GTK 4 and libadwaita keep the same icon theme. Decide
    whether 35 % parts should go up (for example to 50 %) in high contrast.
    That needs a CSS rule; one SVG cannot carry both.
*   Large text: the shell sizes panel icons in em, so they scale with the
    text scaling factor and the stroke scales with them. GTK app icons
    stay 16 px.
*   No motion. "Acquiring" states are static images.

## Acceptance criteria

Packaging and files:

1.  `/usr/share/icons/Apex/index.theme` exists with `Name=Apex`, the chosen
    `Inherits=` line, and a `Directories=` entry for every directory that
    holds SVGs. `icon-theme.cache` is present and newer than every theme
    directory.
2.  A new user's `gsettings get org.gnome.desktop.interface icon-theme`
    returns `'Apex'`. The GDM greeter also resolves icons from Apex
    (checked with criterion 12 on the greeter).
3.  The theme contains a `<name>-symbolic.svg` for each of the 289 names in
    the appendix, under the drawn name and under every alias the build adds
    (screenshot UI names, renamed custom names).
4.  Every shipped SVG has `viewBox="0 0 16 16"`, `width="16"`,
    `height="16"`. It contains only `<svg>`, `<path>` and optionally
    `<title>` elements, and no `stroke*`, `transform`, `clip-path`, `mask`,
    `filter`, `style`, `class`, `<text>` or `<image>`.
5.  Every path's fill opacity is 1 or 0.35 (±0.01). Paths at 0.35 exist
    only for names whose sheet entry has a non-empty `o` layer.
6.  All painted geometry lies inside x and y 0.5 to 15.5 (the drawn maximum
    is 0.62 to 15.5).

Fidelity:

7.  Render each shipped SVG and its stroked master (stroke 1.75) with
    `rsvg-convert` at 16, 32 and 64 px. At 32 px no pixel's alpha differs by
    more than 16/255, and fewer than 0.5 % of pixels differ by more than
    4/255.
8.  At 64 px, the width of a straight stroke (for example `list-remove`,
    `M2.5 8h11`) measures 7.0 px ±0.25.
9.  Recolour test: render each SVG with an injected stylesheet
    `path { fill: #ff0000 !important }`, the way GTK forces fill. Every
    non-transparent pixel has hue red and no pixel is black or grey, which
    catches strokes left behind.
10. Glyphs that use `evenodd` on the sheets (`emblem-system`, `system-run`,
    `applications-system`, `emblem-important`) render with their holes
    transparent at 64 px.

Runtime resolution (the drawn surfaces):

11. A scripted session opens a test image whose Adwaita and Colloid
    `*-symbolic` files have been replaced by solid magenta squares of the
    same names. The session visits every state below in light and dark. No
    screenshot contains magenta (`#ff00ff`, tolerance 10).
    *   Top bar: each Wi-Fi level, Wi-Fi acquiring, off, offline and no
        route; wired on and off; VPN on, acquiring and off; Bluetooth on,
        off and acquiring; each battery level in tens, charging and full;
        each volume level and muted; mic levels and muted; airplane mode;
        screen sharing, camera, location and recording indicators.
    *   Quick Settings: every toggle on and off, the Wi-Fi, Bluetooth,
        power-mode and sound submenus, and the system buttons.
    *   OSDs: volume, brightness, keyboard backlight, mic, eject.
    *   Calendar and notifications: empty state, a notification with its
        expander, weather with a location set.
    *   Lock screen, GDM greeter, polkit and end-session dialogs, password
        reveal and conceal, Caps Lock warning.
    *   Screenshot UI: area, screen and window modes, pointer toggle,
        screencast.
    *   Settings: every sidebar row and every panel page top level.
    *   Files: sidebar, header bar, view switcher, menus, properties,
        empty folder, Trash empty and full, a mounted USB drive.
    *   Terminal: header bar, tabs, menus, preferences.
12. During the same session, an `openat` trace of `gnome-shell`,
    `gnome-control-center`, `nautilus` and `ptyxis` shows no `*-symbolic.svg`
    opened under `/usr/share/icons/Adwaita/` or any Colloid directory.
13. With `GTK_DEBUG=icontheme` on Settings, Files and Terminal, every
    logged lookup of a `*-symbolic` name resolves to a file under
    `/usr/share/icons/Apex/`.
14. Changing `icon-theme` from Adwaita to Apex at runtime updates the top
    bar within 1 s, without a restart.
15. Each family in the states table resolves every member to Apex. None
    falls back to a generic name in a parent theme: no
    `network-wireless-signal-*` request ends at an Adwaita file.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.
Ranked by how much they block engineering:

1.  **Inherits chain with Colloid.** Options A, B or C above. This blocks
    packaging and the acceptance tests.
2.  **The icon scan.** 31c names "check-icons" and 31b and 31d an "icon
    scan", but neither the tool nor its output is in the repo. Acceptance
    needs the list of names requested at runtime, so ship the tool or its
    output, and say which GNOME versions it ran against.
3.  **Source of truth after extraction.** Is it the canvas sheets or
    stroked master SVGs in the repo? The build needs one.
4.  **Collapsed families.** Is it intended that the charging levels, the
    wired states, the mic levels, overamplified volume, Wi-Fi good versus
    excellent, `battery-level-100-charged` versus `-100`, and headset versus
    headphones look the same? The wired case shows a connected icon when
    unplugged (`GlyphActions.dc.html:117-135`).
5.  **Non-upstream names.** `go-next-arrow` (`Glyphs.dc.html:113`),
    `selection-area`, `window`, `pointer` (`:164-166`), `apex-desktop`
    (`:116`), `system-rollback` (`:108`), and `briefcase`, `globe`,
    `text-x-script` (`:139-142`). Each needs its real requester or an
    alias.
6.  **Settings panel names.** 31 uses generic names (for example
    `preferences-desktop-appearance`). Settings may request
    `org.gnome.Settings-*-symbolic` names. Confirm, and add aliases.
7.  **Undrawn but likely requested names** (see States). These decide
    whether acceptance criterion 11 can pass.
8.  **Optical sizes.** Other artboards draw large glyphs thinner and small
    ones heavier (scan table). Do these need separate assets?
9.  **Dimmed parts are stroked where the active form fills.** Examples are
    the camera lens in `camera-disabled`, the head in `user-not-tracked`
    and the capsule in `microphone-sensitivity-muted`. Is that the intent?
    Should the slash cut a gap through the dimmed body, as Adwaita does?
10. **Keyline overshoot** up to 0.38 units (battery, camera, computer).
    Confirm it is allowed.
11. **Top bar previews** omit the `o` layer and `evenodd`
    (`GlyphFamilies.dc.html:35-38`). This is a sheet bug, but the 31b and
    31c previews misrepresent their icons.
12. **tokens.json `icon.conflicts`** first cited only Tiling, Polkit and
    EndSession. It now records the 0.95 to 2.25 range across all 28
    locations listed here and the keyline overshoots (fixed by the design
    owner on 2026-11-17).
13. **Flatpak apps** are outside the drawn surfaces but will show Adwaita.
    Is a Flatpak icon-theme extension in scope?
14. **Copy.** Labels use U+2011 (non-breaking hyphen) in "Wi‑Fi"
    (`GlyphFamilies.dc.html:79`), and the preview writes "87 %" with a
    space. Labels are not shipped in SVGs, but they are candidate tooltips.

## Build pipeline outline

1.  **Extract.** For each sheet, read the `const GL = [...]` array in the
    `Component` script (`Glyphs.dc.html:77-170`, `GlyphFamilies.dc.html:77-631`,
    `GlyphActions.dc.html:77-551`, `GlyphMore.dc.html:77-628`). Each entry is
    `[id, label, d, f, o]` under `[groupTitle, items]`. Normalise to JSON:
    single to double quotes, drop trailing commas. Fail if one name has two
    different drawings. Deduplicate identical repeats.
2.  **Masters.** Write `masters/<id>-symbolic.svg` per name: the three
    layers in sheet order (`o` stroked at `stroke-opacity .35`, `d` stroked,
    `f` filled with `evenodd`), stroke 1.75, round caps and joins. Masters
    are reviewable in a browser and are the input to every later step.
3.  **Outline.** Convert strokes to fills with a scripted tool, for example
    picosvg (skia-pathops), or the Inkscape 1.x command line with
    `object-stroke-to-path`. Per layer: union all outlined `d` geometry into
    one path. Union `o` into one path carrying `fill-opacity="0.35"`. Keep
    `f` as its own path, either with `fill-rule="evenodd"` or simplified to
    nonzero.
4.  **Normalise.** Set `viewBox="0 0 16 16" width="16" height="16"`, one
    plain fill colour, and coordinates rounded to 3 decimals. Strip ids,
    metadata and editor namespaces. Run svgo with a preset that does not
    merge paths across opacity layers.
5.  **Validate.** Run acceptance criteria 4 to 10 in CI: element and
    attribute allowlist, bounds 0.5 to 15.5, the `rsvg-convert` render diff
    against the master, the injected-stylesheet recolour test, evenodd
    holes.
6.  **Alias.** Symlink names with identical drawings to one file. Add the
    upstream aliases decided in open questions 5 and 6.
7.  **Coverage report.** Compare the theme's names with the Adwaita file
    list and with the runtime capture list (criteria 12 and 13). Fail CI
    when a name that was covered loses coverage.
8.  **Package.** Build an RPM `apex-icon-theme` with the tree, the
    index.theme, the GSettings override and the Colloid merge (if option
    C). Run `gtk4-update-icon-cache` during the image build, and install it
    into the bootc image.

## Appendix: glyph inventory

Names are as the sheets give them (each figure's `title` is
`id + '-symbolic'`). "Line" is the line of the entry in the board's file
(31 `Glyphs.dc.html`, 31b `GlyphFamilies.dc.html`, 31c
`GlyphActions.dc.html`, 31d `GlyphMore.dc.html`). "Same drawing as" lists
other names with identical paths. Labels and group titles write "Wi‑Fi"
with U+2011; the tables use a plain hyphen.

### 31: Top bar and status (11)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `network-wireless-signal-excellent-symbolic` | Wi-Fi | 79 | `network-wireless`, `network-wireless-signal-good` |  |
| `network-wireless-signal-weak-symbolic` | Wi-Fi, weak | 80 |  | Also on 31b, identical. |
| `audio-volume-high-symbolic` | Volume | 81 | `audio-volume-medium`, `audio-volume-overamplified` |  |
| `audio-volume-muted-symbolic` | Muted | 82 |  |  |
| `battery-level-80-symbolic` | Battery | 83 | `gnome-power-manager` |  |
| `battery-level-20-symbolic` | Battery, low | 84 | `battery-low` |  |
| `battery-level-80-charging-symbolic` | Charging | 85 | `battery-level-0-charging`, `battery-level-10-charging`, `battery-level-20-charging`, `battery-level-30-charging` +5 | Bolt only; no level fill. |
| `bluetooth-active-symbolic` | Bluetooth | 86 |  |  |
| `audio-input-microphone-symbolic` | Microphone | 87 | `microphone-sensitivity-high`, `microphone-sensitivity-medium`, `microphone-sensitivity-low` |  |
| `go-down-symbolic` | Downloading | 88 |  |  |
| `dialog-warning-symbolic` | Warning | 89 |  |  |

### 31: Quick Settings (8)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `night-light-symbolic` | Night Light | 92 |  |  |
| `notifications-disabled-symbolic` | Do Not Disturb | 93 |  |  |
| `airplane-mode-symbolic` | Airplane Mode | 94 |  |  |
| `network-vpn-symbolic` | VPN | 95 |  |  |
| `power-profile-balanced-symbolic` | Power Mode | 96 |  | Also on 31b, identical. |
| `display-brightness-symbolic` | Brightness | 97 |  |  |
| `dark-mode-symbolic` | Dark Style | 98 |  |  |
| `camera-photo-symbolic` | Screenshot | 99 |  |  |

### 31: System and sign-in (12)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `emblem-system-symbolic` | Settings | 102 | `system-run` |  |
| `system-lock-screen-symbolic` | Lock | 103 | `network-wireless-encrypted`, `locked`, `channel-secure`, `changes-prevent` |  |
| `system-shutdown-symbolic` | Power Off | 104 |  |  |
| `system-reboot-symbolic` | Restart | 105 |  |  |
| `system-log-out-symbolic` | Log Out | 106 |  |  |
| `software-update-available-symbolic` | Updates | 107 |  |  |
| `system-rollback-symbolic` | Rolled Back | 108 |  | Apex name; requested only by Apex update UI. |
| `preferences-system-notifications-symbolic` | Notifications | 109 |  |  |
| `system-search-symbolic` | Search | 110 | `edit-find` |  |
| `auth-fingerprint-symbolic` | Fingerprint | 111 |  |  |
| `dialog-password-symbolic` | Authentication | 112 |  |  |
| `go-next-arrow-symbolic` | Unlock | 113 |  | Not a known Adwaita name. Check what the unlock prompt requests. |

### 31: Settings panels (12)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `apex-desktop-symbolic` | Apex Desktop | 116 | `start-here` | Apex name; no upstream requester. Apex Desktop panel must request it. |
| `network-wired-symbolic` | Network | 117 | `network-wired-disconnected`, `network-wired-acquiring`, `network-wired-no-route` |  |
| `video-display-symbolic` | Displays | 118 | `user-desktop` |  |
| `preferences-desktop-appearance-symbolic` | Appearance | 119 |  |  |
| `preferences-system-multitasking-symbolic` | Multitasking | 120 |  |  |
| `view-app-grid-symbolic` | Apps | 121 |  |  |
| `security-high-symbolic` | Privacy & Security | 122 |  |  |
| `input-keyboard-symbolic` | Keyboard | 123 | `keyboard-brightness` |  |
| `input-mouse-symbolic` | Mouse & Touchpad | 124 |  |  |
| `preferences-desktop-accessibility-symbolic` | Accessibility | 125 | `org.gnome.Settings-accessibility` |  |
| `system-users-symbolic` | Users | 126 | `emoji-body` |  |
| `computer-symbolic` | System | 127 |  |  |

### 31: Files (15)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `document-open-recent-symbolic` | Recent | 130 |  |  |
| `starred-symbolic` | Starred | 131 |  |  |
| `user-home-symbolic` | Home | 132 |  |  |
| `folder-symbolic` | Folder | 133 | `document-open`, `folder-open`, `folder-remote` |  |
| `folder-documents-symbolic` | Documents | 134 | `emblem-documents` |  |
| `folder-download-symbolic` | Downloads | 135 | `document-save` |  |
| `folder-music-symbolic` | Music | 136 | `audio-x-generic`, `applications-multimedia` |  |
| `folder-pictures-symbolic` | Pictures | 137 |  |  |
| `folder-videos-symbolic` | Videos | 138 | `video-x-generic` |  |
| `briefcase-symbolic` | Projects | 139 | `folder-projects` | Files redesign bookmark; not an XDG folder. |
| `globe-symbolic` | Public | 140 | `folder-publicshare` | Files redesign "Public"; Nautilus requests folder-publicshare. |
| `folder-templates-symbolic` | Templates | 141 |  |  |
| `text-x-script-symbolic` | Code | 142 |  | Files redesign "Code" bookmark. |
| `user-trash-symbolic` | Trash | 143 | `edit-delete` |  |
| `drive-harddisk-symbolic` | Drive | 144 |  |  |

### 31: Header bar and windows (15)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `go-previous-symbolic` | Back | 147 |  |  |
| `go-next-symbolic` | Forward | 148 |  |  |
| `pan-down-symbolic` | Expand | 149 |  |  |
| `open-menu-symbolic` | Main Menu | 150 |  |  |
| `view-grid-symbolic` | Grid View | 151 |  |  |
| `view-list-symbolic` | List View | 152 |  |  |
| `sidebar-show-symbolic` | Sidebar | 153 |  |  |
| `sidebar-show-right-symbolic` | Details Pane | 154 |  |  |
| `dialog-information-symbolic` | Details | 155 | `help-about` |  |
| `view-more-symbolic` | More | 156 | `view-more-horizontal` |  |
| `list-add-symbolic` | Add | 157 |  |  |
| `object-select-symbolic` | Done | 158 |  |  |
| `window-minimize-symbolic` | Minimize | 159 |  |  |
| `window-maximize-symbolic` | Maximize | 160 |  |  |
| `window-close-symbolic` | Close | 161 |  |  |

### 31: Capture and media (5)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `selection-area-symbolic` | Selection | 164 | `view-fullscreen` | Shell screenshot UI uses its own resource names; alias needed. |
| `window-symbolic` | Window | 165 |  | Shell screenshot UI resource name; alias needed. |
| `pointer-symbolic` | Pointer | 166 |  | Shell screenshot UI resource name; alias needed. |
| `camera-video-symbolic` | Screencast | 167 |  |  |
| `media-playback-pause-symbolic` | Pause | 168 |  |  |

### 31b: Wi-Fi (11)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `network-wireless-symbolic` | Wi-Fi | 82 | `network-wireless-signal-excellent`, `network-wireless-signal-good` | Same drawing as excellent. |
| `network-wireless-signal-good-symbolic` | Wi-Fi, good | 89 | `network-wireless-signal-excellent`, `network-wireless` | Same drawing as excellent: good and excellent are not told apart. |
| `network-wireless-signal-ok-symbolic` | Wi-Fi, fair | 96 |  |  |
| `network-wireless-signal-weak-symbolic` | Wi-Fi, weak | 103 |  | Also on 31, identical. |
| `network-wireless-signal-none-symbolic` | Wi-Fi, no signal | 110 |  | Whole glyph at 35 %, small dot. |
| `network-wireless-acquiring-symbolic` | Connecting | 117 |  |  |
| `network-wireless-no-route-symbolic` | No internet | 124 |  |  |
| `network-wireless-offline-symbolic` | Offline | 131 | `network-offline` |  |
| `network-wireless-disabled-symbolic` | Wi-Fi off | 138 |  |  |
| `network-wireless-encrypted-symbolic` | Secured | 145 | `system-lock-screen`, `locked`, `channel-secure`, `changes-prevent` |  |
| `network-wireless-hotspot-symbolic` | Hotspot | 152 |  |  |

### 31b: Battery (19)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `battery-level-0-symbolic` | Battery 0 % | 164 | `battery-caution` |  |
| `battery-level-10-symbolic` | Battery 10 % | 171 |  |  |
| `battery-level-30-symbolic` | Battery 30 % | 178 |  |  |
| `battery-level-40-symbolic` | Battery 40 % | 185 |  |  |
| `battery-level-50-symbolic` | Battery 50 % | 192 |  |  |
| `battery-level-60-symbolic` | Battery 60 % | 199 |  |  |
| `battery-level-70-symbolic` | Battery 70 % | 206 |  |  |
| `battery-level-90-symbolic` | Battery 90 % | 213 |  |  |
| `battery-level-100-symbolic` | Battery 100 % | 220 | `battery-level-100-charged`, `battery` |  |
| `battery-level-0-charging-symbolic` | Charging 0 % | 227 | `battery-level-80-charging`, `battery-level-10-charging`, `battery-level-20-charging`, `battery-level-30-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-10-charging-symbolic` | Charging 10 % | 234 | `battery-level-80-charging`, `battery-level-0-charging`, `battery-level-20-charging`, `battery-level-30-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-20-charging-symbolic` | Charging 20 % | 241 | `battery-level-80-charging`, `battery-level-0-charging`, `battery-level-10-charging`, `battery-level-30-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-30-charging-symbolic` | Charging 30 % | 248 | `battery-level-80-charging`, `battery-level-0-charging`, `battery-level-10-charging`, `battery-level-20-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-40-charging-symbolic` | Charging 40 % | 255 | `battery-level-80-charging`, `battery-level-0-charging`, `battery-level-10-charging`, `battery-level-20-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-50-charging-symbolic` | Charging 50 % | 262 | `battery-level-80-charging`, `battery-level-0-charging`, `battery-level-10-charging`, `battery-level-20-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-60-charging-symbolic` | Charging 60 % | 269 | `battery-level-80-charging`, `battery-level-0-charging`, `battery-level-10-charging`, `battery-level-20-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-70-charging-symbolic` | Charging 70 % | 276 | `battery-level-80-charging`, `battery-level-0-charging`, `battery-level-10-charging`, `battery-level-20-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-90-charging-symbolic` | Charging 90 % | 283 | `battery-level-80-charging`, `battery-level-0-charging`, `battery-level-10-charging`, `battery-level-20-charging` +5 | Bolt only; no level fill. All charging levels look the same. |
| `battery-level-100-charged-symbolic` | Charged | 290 | `battery-level-100`, `battery` | Same drawing as battery-level-100; no charged mark. |

### 31b: Sound and input (7)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `audio-volume-low-symbolic` | Volume, low | 302 |  |  |
| `audio-volume-medium-symbolic` | Volume, medium | 309 | `audio-volume-high`, `audio-volume-overamplified` |  |
| `audio-volume-overamplified-symbolic` | Volume, over 100 % | 316 | `audio-volume-high`, `audio-volume-medium` | Same drawing as high; over 100 % is not told apart. |
| `microphone-sensitivity-high-symbolic` | Microphone, high | 323 | `audio-input-microphone`, `microphone-sensitivity-medium`, `microphone-sensitivity-low` | Same drawing as audio-input-microphone. |
| `microphone-sensitivity-medium-symbolic` | Microphone, medium | 330 | `audio-input-microphone`, `microphone-sensitivity-high`, `microphone-sensitivity-low` | Same drawing as high. |
| `microphone-sensitivity-low-symbolic` | Microphone, low | 337 | `audio-input-microphone`, `microphone-sensitivity-high`, `microphone-sensitivity-medium` | Same drawing as high. |
| `microphone-sensitivity-muted-symbolic` | Microphone off | 344 |  |  |

### 31b: Radios and power (7)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `bluetooth-disabled-symbolic` | Bluetooth off | 356 |  |  |
| `bluetooth-acquiring-symbolic` | Bluetooth, connecting | 363 |  | Whole glyph at 35 %. |
| `power-profile-power-saver-symbolic` | Power Saver | 370 |  |  |
| `power-profile-balanced-symbolic` | Balanced | 377 |  | Also on 31, identical. |
| `power-profile-performance-symbolic` | Performance | 384 |  |  |
| `network-vpn-acquiring-symbolic` | VPN, connecting | 391 |  | Whole glyph at 35 %. |
| `network-vpn-disabled-symbolic` | VPN off | 398 |  |  |

### 31b: Editing and navigation (10)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `pan-up-symbolic` | Collapse | 410 |  |  |
| `pan-start-symbolic` | Previous | 417 |  |  |
| `pan-end-symbolic` | Next | 424 |  |  |
| `go-up-symbolic` | Up | 431 |  |  |
| `edit-find-symbolic` | Find | 438 | `system-search` |  |
| `edit-clear-symbolic` | Clear | 445 | `process-stop`, `edit-clear-rtl` |  |
| `edit-copy-symbolic` | Copy | 452 | `view-restore` |  |
| `view-reveal-symbolic` | Show Password | 459 |  |  |
| `view-conceal-symbolic` | Hide Password | 466 |  |  |
| `caps-lock-symbolic` | Caps Lock | 473 |  |  |

### 31b: Media and privacy (9)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `media-playback-start-symbolic` | Play | 485 |  |  |
| `media-skip-backward-symbolic` | Previous Track | 492 |  |  |
| `media-skip-forward-symbolic` | Next Track | 499 |  |  |
| `media-record-symbolic` | Recording | 506 |  |  |
| `screen-shared-symbolic` | Screen Sharing | 513 |  |  |
| `camera-web-symbolic` | Camera | 520 |  |  |
| `location-services-active-symbolic` | Location | 527 | `mark-location` |  |
| `audio-headphones-symbolic` | Headphones | 534 | `audio-headset` |  |
| `audio-headset-symbolic` | Headset | 541 | `audio-headphones` | Same drawing as headphones; no boom mic. |

### 31b: People, input and emblems (11)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `night-light-disabled-symbolic` | Night Light off | 553 |  |  |
| `input-touchpad-symbolic` | Touchpad | 560 |  |  |
| `touchpad-disabled-symbolic` | Touchpad off | 567 |  |  |
| `avatar-default-symbolic` | User | 574 |  |  |
| `emblem-ok-symbolic` | Done | 581 | `check-outlined`, `emblem-default` |  |
| `check-outlined-symbolic` | Checked | 588 | `emblem-ok`, `emblem-default` | Same drawing as emblem-ok. |
| `emblem-default-symbolic` | Default | 595 | `emblem-ok`, `check-outlined` | Same drawing as emblem-ok. |
| `locked-symbolic` | Locked | 602 | `system-lock-screen`, `network-wireless-encrypted`, `channel-secure`, `changes-prevent` |  |
| `emblem-documents-symbolic` | Documents | 609 | `folder-documents` |  |
| `emblem-shared-symbolic` | Shared | 616 |  |  |
| `emblem-synchronizing-symbolic` | Syncing | 623 |  |  |

### 31c: Shell (20)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `view-refresh-symbolic` | Refresh | 82 | `rotation-allowed`, `media-playlist-repeat` |  |
| `rotation-allowed-symbolic` | Auto Rotate | 89 | `view-refresh`, `media-playlist-repeat` |  |
| `rotation-locked-symbolic` | Rotation Locked | 96 |  |  |
| `document-edit-symbolic` | Edit | 103 |  |  |
| `user-trash-full-symbolic` | Trash, full | 110 |  |  |
| `network-wired-disconnected-symbolic` | Wired, unplugged | 117 | `network-wired`, `network-wired-acquiring`, `network-wired-no-route` | Same drawing as connected network-wired. |
| `network-wired-acquiring-symbolic` | Wired, connecting | 124 | `network-wired`, `network-wired-disconnected`, `network-wired-no-route` | Same drawing as connected network-wired. |
| `network-wired-no-route-symbolic` | Wired, no internet | 131 | `network-wired`, `network-wired-disconnected`, `network-wired-acquiring` | Same drawing as connected network-wired. |
| `network-error-symbolic` | Network error | 138 |  |  |
| `network-offline-symbolic` | Offline | 145 | `network-wireless-offline` |  |
| `thunderbolt-symbolic` | Thunderbolt | 152 |  |  |
| `thunderbolt-acquiring-symbolic` | Thunderbolt, connecting | 159 |  | Whole glyph at 35 %. |
| `channel-secure-symbolic` | Secure | 166 | `system-lock-screen`, `network-wireless-encrypted`, `locked`, `changes-prevent` |  |
| `channel-insecure-symbolic` | Not secure | 173 |  |  |
| `system-switch-user-symbolic` | Switch User | 180 |  |  |
| `find-location-symbolic` | Find Location | 187 |  |  |
| `audio-x-generic-symbolic` | Audio | 194 | `folder-music`, `applications-multimedia` |  |
| `face-smile-symbolic` | Smile | 201 | `emoji-people` |  |
| `face-sad-symbolic` | Sad | 208 |  |  |
| `gnome-power-manager-symbolic` | Power | 215 | `battery-level-80` | Legacy name. |

### 31c: OSDs (8)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `media-eject-symbolic` | Eject | 227 |  |  |
| `drive-removable-media-symbolic` | Removable drive | 234 | `media-removable` |  |
| `media-removable-symbolic` | Removable media | 241 | `drive-removable-media` |  |
| `action-unavailable-symbolic` | Unavailable | 248 |  |  |
| `battery-low-symbolic` | Battery low | 255 | `battery-level-20` |  |
| `battery-caution-symbolic` | Battery critical | 262 | `battery-level-0` |  |
| `battery-action-symbolic` | Battery action | 269 |  |  |
| `keyboard-brightness-symbolic` | Keyboard Backlight | 276 | `input-keyboard` |  |

### 31c: Every app (GTK and libadwaita) (7)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `document-save-symbolic` | Save | 288 | `folder-download` |  |
| `document-open-symbolic` | Open | 295 | `folder`, `folder-open`, `folder-remote` |  |
| `edit-cut-symbolic` | Cut | 302 |  |  |
| `edit-paste-symbolic` | Paste | 309 |  |  |
| `edit-undo-symbolic` | Undo | 316 |  |  |
| `edit-redo-symbolic` | Redo | 323 |  |  |
| `font-x-generic-symbolic` | Font | 330 | `font-select` |  |

### 31c: Files (13)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `zoom-in-symbolic` | Zoom In | 342 |  |  |
| `zoom-out-symbolic` | Zoom Out | 349 |  |  |
| `tab-new-symbolic` | New Tab | 356 |  |  |
| `window-new-symbolic` | New Window | 363 |  |  |
| `folder-new-symbolic` | New Folder | 370 |  |  |
| `folder-projects-symbolic` | Projects | 377 | `briefcase` |  |
| `x-office-calendar-symbolic` | Calendar | 384 |  |  |
| `x-office-spreadsheet-symbolic` | Spreadsheet | 391 |  |  |
| `process-stop-symbolic` | Stop | 398 | `edit-clear`, `edit-clear-rtl` |  |
| `edit-clear-rtl-symbolic` | Clear | 405 | `edit-clear`, `process-stop` |  |
| `view-more-horizontal-symbolic` | More | 412 | `view-more` |  |
| `bookmark-new-symbolic` | Bookmark | 419 | `user-bookmarks` |  |
| `non-starred-symbolic` | Not starred | 426 |  |  |

### 31c: Settings and apps (16)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `edit-delete-symbolic` | Delete | 438 | `user-trash` |  |
| `dialog-error-symbolic` | Error | 445 |  |  |
| `dialog-question-symbolic` | Question | 452 |  |  |
| `folder-open-symbolic` | Open Folder | 459 | `folder`, `document-open`, `folder-remote` |  |
| `help-about-symbolic` | About | 466 | `dialog-information` |  |
| `list-drag-handle-symbolic` | Drag | 473 |  |  |
| `folder-publicshare-symbolic` | Public | 480 | `globe` |  |
| `folder-remote-symbolic` | Network Folder | 487 | `folder`, `document-open`, `folder-open` |  |
| `system-run-symbolic` | Run | 494 | `emblem-system` |  |
| `user-desktop-symbolic` | Desktop | 501 | `video-display` |  |
| `utilities-terminal-symbolic` | Terminal | 508 |  |  |
| `applications-multimedia-symbolic` | Multimedia | 515 | `folder-music`, `audio-x-generic` |  |
| `list-remove-symbolic` | Remove | 522 |  |  |
| `view-restore-symbolic` | Restore | 529 | `edit-copy` |  |
| `view-fullscreen-symbolic` | Fullscreen | 536 | `selection-area` |  |
| `mail-unread-symbolic` | Mail | 543 |  |  |

### 31d: Shell (19)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `application-x-executable-symbolic` | App without an icon | 82 |  |  |
| `org.gnome.Settings-accessibility-symbolic` | Accessibility menu | 89 | `preferences-desktop-accessibility` | Shell accessibility menu name. |
| `insert-object-symbolic` | Insert | 96 |  |  |
| `network-workgroup-symbolic` | Workgroup | 103 |  |  |
| `network-cellular-symbolic` | Mobile broadband | 110 | `network-cellular-connected`, `network-cellular-signal-excellent` |  |
| `network-cellular-connected-symbolic` | Mobile connected | 117 | `network-cellular`, `network-cellular-signal-excellent` |  |
| `network-cellular-signal-excellent-symbolic` | Mobile excellent | 124 | `network-cellular`, `network-cellular-connected` |  |
| `network-cellular-signal-good-symbolic` | Mobile good | 131 |  |  |
| `network-cellular-signal-ok-symbolic` | Mobile OK | 138 |  |  |
| `network-cellular-signal-weak-symbolic` | Mobile weak | 145 |  |  |
| `network-cellular-signal-none-symbolic` | Mobile none | 152 |  |  |
| `network-cellular-acquiring-symbolic` | Mobile connecting | 159 |  |  |
| `network-cellular-disabled-symbolic` | Mobile off | 166 |  |  |
| `network-cellular-offline-symbolic` | Mobile offline | 173 |  |  |
| `airplane-mode-disabled-symbolic` | Airplane mode off | 180 |  |  |
| `drive-harddisk-usb-symbolic` | External drive | 187 |  |  |
| `focus-windows-symbolic` | Focused window | 194 |  |  |
| `switch-on-symbolic` | Switch on mark | 201 |  | Shell switch mark (Show Status Shapes). |
| `switch-off-symbolic` | Switch off mark | 208 |  | Shell switch mark (Show Status Shapes). |

### 31d: Settings, Files, setup, Text Editor and Ptyxis (9)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `computer-fail-symbolic` | Computer with a fault | 220 |  |  |
| `input-tablet-symbolic` | Graphics tablet | 227 |  |  |
| `preferences-system-devices-symbolic` | Devices | 234 |  |  |
| `preferences-system-privacy-symbolic` | Privacy | 241 |  |  |
| `start-here-symbolic` | Start | 248 | `apex-desktop` |  |
| `web-browser-symbolic` | Web account | 255 |  |  |
| `edit-find-replace-symbolic` | Find and replace | 262 |  |  |
| `font-select-symbolic` | Font | 269 | `font-x-generic` |  |
| `preferences-desktop-keyboard-shortcuts-symbolic` | Shortcuts | 276 |  |  |

### 31d: Viewers, Contacts, Web and Maps (20)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `image-missing-symbolic` | Missing image | 288 |  |  |
| `object-rotate-left-symbolic` | Rotate left | 295 |  |  |
| `object-rotate-right-symbolic` | Rotate right | 302 |  |  |
| `mark-location-symbolic` | Location | 309 | `location-services-active` |  |
| `zoom-fit-best-symbolic` | Fit | 316 |  |  |
| `video-x-generic-symbolic` | Video | 323 | `folder-videos` |  |
| `camera-disabled-symbolic` | Camera off | 330 |  |  |
| `applications-system-symbolic` | System | 337 |  |  |
| `mail-send-symbolic` | Send | 344 |  |  |
| `phone-symbolic` | Phone | 351 |  |  |
| `selection-mode-symbolic` | Select | 358 |  |  |
| `application-x-addon-symbolic` | Extension | 365 |  |  |
| `applications-engineering-symbolic` | Developer tools | 372 |  |  |
| `face-uncertain-symbolic` | Uncertain | 379 |  |  |
| `go-home-symbolic` | Home | 386 |  |  |
| `go-jump-symbolic` | Go | 393 |  |  |
| `package-x-generic-symbolic` | Package | 400 |  |  |
| `user-not-tracked-symbolic` | Not tracked | 407 |  |  |
| `view-wrapped-symbolic` | Wrap lines | 414 |  |  |
| `document-print-symbolic` | Print | 421 |  |  |

### 31d: Characters and Weather (10)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `emoji-people-symbolic` | Smileys and people | 433 | `face-smile` | GTK emoji chooser section. |
| `emoji-body-symbolic` | People and body | 440 | `system-users` |  |
| `emoji-nature-symbolic` | Animals and nature | 447 |  |  |
| `emoji-food-symbolic` | Food and drink | 454 |  |  |
| `emoji-activities-symbolic` | Activities | 461 |  |  |
| `emoji-travel-symbolic` | Travel and places | 468 |  |  |
| `emoji-objects-symbolic` | Objects | 475 |  |  |
| `emoji-flags-symbolic` | Flags | 482 |  |  |
| `weather-showers-symbolic` | Showers | 489 |  |  |
| `weather-showers-scattered-symbolic` | Scattered showers | 496 |  |  |

### 31d: Firmware, Disks, Usage, System Monitor and Help (17)

| Icon name | Label | Line | Same drawing as | Note |
| --- | --- | --- | --- | --- |
| `alarm-symbolic` | Alarm | 508 |  |  |
| `battery-symbolic` | Battery | 515 | `battery-level-100`, `battery-level-100-charged` |  |
| `emblem-important-symbolic` | Important | 522 |  |  |
| `media-playlist-repeat-symbolic` | Repeat | 529 | `view-refresh`, `rotation-allowed` |  |
| `media-playlist-repeat-song-symbolic` | Repeat one | 536 |  |  |
| `network-transmit-receive-symbolic` | Transfer | 543 |  |  |
| `security-low-symbolic` | Security low | 550 |  |  |
| `security-medium-symbolic` | Security medium | 557 |  |  |
| `software-update-urgent-symbolic` | Urgent update | 564 |  |  |
| `task-due-symbolic` | Due | 571 |  |  |
| `changes-prevent-symbolic` | Locked | 578 | `system-lock-screen`, `network-wireless-encrypted`, `locked`, `channel-secure` |  |
| `changes-allow-symbolic` | Unlocked | 585 |  |  |
| `drive-multidisk-symbolic` | Multiple disks | 592 |  |  |
| `media-playback-stop-symbolic` | Stop | 599 |  |  |
| `drive-harddisk-system-symbolic` | System disk | 606 |  |  |
| `document-properties-symbolic` | Properties | 613 |  |  |
| `user-bookmarks-symbolic` | Bookmarks | 620 | `bookmark-new` |  |
