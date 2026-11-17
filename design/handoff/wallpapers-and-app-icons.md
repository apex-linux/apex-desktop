# Wallpapers, app icons and the Apex Code icon

## Summary

This spec covers the image assets the distribution ships rather than draws in
code:

*   The default wallpaper, "Facets", as a light and dark pair of 2880x1800
    SVGs (`canvas/assets/3d451127dc2b77221bac98465ee1ec99.svg` and
    `f607332583898d73d053baf1c0cae872.svg`). Appearance also offers five solid
    colours (`Appearance.dc.html:24-28`, `:193`).
*   34 full-colour icons in one rounded-tile style: 29 app icons used by the
    dock, Launcher and Spotlight, 2 shell icons (Show Apps, Trash), and 3
    icons no artboard references. Listed in `canvas/assets/MANIFEST.md`.
*   The Apex Code app icon (artboard 43, `CodeIcon.dc.html`): full colour at
    128, 64 and 32 px, in a 54 px dock slot, and a symbolic glyph at 32 and 16
    px, each in light and dark. It is drawn inline in the artboard and is
    not one of the asset files.

The canvas states the icon policy twice: "App icons stay Colloid"
(`Glyphs.dc.html:27`) and the Apex Code icon sits "on Colloid's tile in the
blue accent. App id stays org.gnome.Builder" (`CodeIcon.dc.html:18`). Colloid
is the third-party Colloid icon theme (vinceliuice/Colloid-icon-theme,
GPL-3.0).

All asset SVGs were uploaded to the canvas by a co-writer. Treat them as
untrusted input and sanitise them before they ship (see Sanitising).

## Upstream mapping

| Item | Upstream mechanism | Confidence |
| --- | --- | --- |
| Wallpaper pair | `org.gnome.desktop.background` keys `picture-uri` and `picture-uri-dark`, set by a GSettings vendor override; listed in Settings > Appearance through a `gnome-background-properties` XML file with `<filename>` and `<filename-dark>` | High |
| Wallpaper rendering | GNOME Shell background manager loads the SVG through the system image loader (librsvg) and scales it to the monitor; GNOME's own backgrounds include SVG light/dark pairs | High |
| Lock screen background | GNOME Shell's unlock dialog blurs the desktop background; nothing extra to ship. GDM greeter background is covered in `greeter-and-lock.md` | Medium |
| App icons | An icon theme (Colloid, or an Apex theme that inherits from it) selected with `org.gnome.desktop.interface icon-theme`; it overrides each app's own hicolor icon by name | High |
| Apex Code icon | Icon name `org.gnome.Builder` (app id unchanged), installed in the Apex icon theme so it wins over Builder's own hicolor icon | High |
| Apex Code symbolic | `org.gnome.Builder-symbolic` in the same theme | High |
| Show Apps tile | GNOME Shell `js/ui/dash.js` draws the Show Apps button with the symbolic icon `view-app-grid-symbolic`, recoloured. A full-colour tile needs a Shell patch; see `shell-top-bar-and-dock.md` | Medium |
| Trash in the dock | Not in stock Shell; covered by `shell-top-bar-and-dock.md`. The icon itself maps to `user-trash` / `user-trash-full` | Medium |

## Layout and measurements

### Wallpaper "Facets"

Both files: `width="2880" height="1800" viewBox="0 0 1440 900"`, 765 bytes,
flat fills, no gradients, filters, text or external references. The two
files differ only in fill colours.

| Layer | Geometry (viewBox units) | Light | Dark |
| --- | --- | --- | --- |
| Base | full rect 1440 x 900 | `#e8ebf0` | `#0f1115` |
| Large diamond, ring 1 | group at translate(1160 820) rotate(45); square 1120, rx 72 | `#dfe3e9` | `#14171d` |
| Ring 2 | square 800, rx 56 | `#d3d9e2` | `#1a1f27` |
| Ring 3 | square 500, rx 40 | `#bfcbdc` | `#222b39` |
| Core | square 236, rx 24 | `#90a9cf` | `#2f4469` |
| Small diamond, outer | group at translate(236 168) rotate(45); square 168, rx 18 | `#dfe3e9` | `#14171d` |
| Small diamond, inner | square 80, rx 10 | `#d3d9e2` | `#1a1f27` |

The large diamond is centred near the bottom-right corner and runs off two
edges; the small one sits top left. The motif is the Apex diamond (the boot
wordmark and Apex Code core use the same rotated rounded square).

The artboards draw the wallpaper as `--wall`: base colour, then the SVG,
`center/cover no-repeat`. Use `zoom` (cover) in GNOME and set the
primary colour to the base colour, so a monitor with another aspect ratio
crops evenly and the first frame before the SVG loads matches.

### Solid wallpapers

Appearance lists five more wallpapers, all flat colours with no dark
variant (`Appearance.dc.html:24-28`):

| Name | Colour |
| --- | --- |
| Slate | `#4d5868` |
| Sage | `#8a9a86` |
| Sand | `#d8cfc1` |
| Mist | `#c7d1dd` |
| Ink | `#1b1e25` |

Ship each as a one-rect SVG at 2880x1800, so it appears in the Appearance
chooser like any other picture. The colours are tokens:
`wallpaper.solid.{slate,sage,sand,mist,ink}.value` in `tokens.json`.

### App icon style (asset files)

All 34 icons are 64 x 64 px. Two document conventions occur, with the same
drawing at different units:

| Convention | Files | Tile | Radius |
| --- | --- | --- | --- |
| Pixel document | `width="64" height="64"`, no viewBox | 56.002 x 56.002 at (4, 3.969) | 13.002 |
| Inkscape millimetre document | `viewBox="0 0 16.933 16.933"` (64 px at 96 dpi = 16.933 mm) | 14.817 x 14.817 at (1.058, 1.05) | 3.44 |

14.817 mm x 3.7795 px/mm = 56 px and 3.44 mm = 13 px, so both describe a
56 px tile with a 13 px radius and a 4 px margin. On top of the tile every
icon draws:

*   A bottom shade band, 1 px high, black at opacity .1 to .15, following the
    lower corners.
*   A top highlight band, 1 px high, white at opacity .15 to .5, following
    the upper corners.
*   A glyph: flat fills, a few gradients and blur filters; tile colours are
    saturated (for example `#33c4fe`, `#4fe373`, `#1598ff`, `#35e9ba`), not
    the libadwaita palette.
*   An empty `<image>` element (no `href`) behind the tile, almost always
    60.882 x 62.001 at (1.559, 2) or the millimetre equivalent 16.108 x 16.404
    at (.413, .529). This is where a bitmap drop shadow was embedded; the
    bitmap has been stripped. The icons therefore render with no drop
    shadow, while the Apex Code icon draws a vector shadow (see AW-4).

Exceptions: `app-files` and `app-settings` start with a 64 x 64 transparent
rect; `app-maps` uses a 50 x 50 tile at (7, 7) with radius 10 (a different
silhouette). In `app-mail`, `app-system-monitor`, `app-fonts`,
`app-contacts` and `shell-trash` the tile is not a plain `<rect>`; check
their silhouettes against the template when sanitising.

### Apex Code icon (`CodeIcon.dc.html:21-28`)

Full colour, 128 x 128 viewBox:

| Part | Geometry | Paint |
| --- | --- | --- |
| Shadow | rect x 8, y 10.5, 112 x 112, rx 26; Gaussian blur stdDeviation 2.4; filter region -10 %, -10 %, 120 % x 125 % | `#000` at .3 |
| Tile | rect x 8, y 8, 112 x 112, rx 26 | `#3584e4` (libadwaita blue) |
| Bottom shade | 2-unit band along the lower edge and corners | black at .15 |
| Top highlight | 2-unit band along the upper edge and corners | `#fff` at .15 |
| Brackets | polylines (51,41)-(28,64)-(51,87) and (77,41)-(100,64)-(77,87); stroke 10, round caps and joins | `#fff` |
| Core | diamond (64,53.5), (74.5,64), (64,74.5), (53.5,64) | `#fff` |

At 64 px this is exactly the Colloid tile above: 56 px, radius 13, 4 px
margin, 1 px bands.

Symbolic, 16 x 16 viewBox:

| Part | Geometry | Paint |
| --- | --- | --- |
| Brackets | (6.3,3.9)-(2.2,8)-(6.3,12.1) and (9.7,3.9)-(13.8,8)-(9.7,12.1); stroke 1.75, round caps and joins | `currentColor` |
| Core | diamond (8,6.2), (9.8,8), (8,9.8), (6.2,8) | `currentColor` |

Stroke 1.75 matches the Apex Symbolic default (`tokens.json` `icon.stroke`).

### Artboard 43 presentation

| Element | Value |
| --- | --- |
| Canvas | 1440 x 900, padding 56 px, gap 28 px, background `#e8ebf0` (literal; the light wallpaper base) |
| Title | "Apex Code: app icon (apex-desktop#38)", 26 px / 800, `#1d1d21` |
| Subtitle | 14 px, `rgba(29,29,33,.7)` (literal) |
| Light and Dark panels | equal width, radius 20 px, padding 36 px, gap 28 px, `--win`, ring 1 px `--border`; heading 18 px / 700 |
| Size row | 128, 64, 32 px icons, gap 40 px, bottom-aligned; captions 12 px `--dim` |
| Symbolic row | top `--border`, padding-top 8 px, gap 32 px; label "Symbolic" 13 px / 600 `--dim`; glyphs at 32 and 16 px in `--fg` |
| Dock strip | padding 8 12 px, radius 24 px, `--dockbg`, gap 8 px; three placeholder tiles 54 x 54, radius 14 px, `rgba(127,127,127,.18)`; then the icon at 54 px |

The full-colour icon is not drawn at 16 px; the brief's "16 px" exists only
as the symbolic glyph.

## Asset inventory and icon names

Icon names are my best mapping from the manifest's app names to current
GNOME and Fedora app ids; check each against the installed `.desktop`
file's `Icon=` key.

| Asset | Blob id (prefix) | Likely icon name | Notes |
| --- | --- | --- | --- |
| app-audio-player | `1d6c04a7` | `org.gnome.Decibels` | |
| app-bazaar | `f45103bf` | `io.github.kolunmi.Bazaar` | Third-party store |
| app-calculator | `a4bbb92f` | `org.gnome.Calculator` | |
| app-calendar | `5971067e` | `org.gnome.Calendar` | Fixed date "26" in the art |
| app-camera | `7ff4d256` | `org.gnome.Snapshot` | |
| app-characters | `f7d96d4c` | `org.gnome.Characters` | |
| app-clocks | `e5ecb308` | `org.gnome.clocks` | |
| app-contacts | `efec7a0b` | `org.gnome.Contacts` | |
| app-disk-usage-analyzer | `b41f8f6b` | `org.gnome.baobab` | |
| app-disks | `b72c2176` | `org.gnome.DiskUtility` | |
| app-document-viewer | `bc02ebfe` | `org.gnome.Papers` | |
| app-extensions | `3bc3f374` | `org.gnome.Extensions` | |
| app-files | `906e0970` | `org.gnome.Nautilus` | |
| app-firmware | `d96660b5` | `org.gnome.Firmware` | |
| app-fonts | `8d834efe` | `org.gnome.font-viewer` | |
| app-help | `e8c9a43c` | `org.gnome.Yelp` | |
| app-image-viewer | `20ab5f44` | `org.gnome.Loupe` | |
| app-logs | `4d76f5dc` | `org.gnome.Logs` | |
| app-mail | `74c5be1b` | unknown | No default mail app named; see AW-7 |
| app-maps | `0d61a941` | `org.gnome.Maps` | Different tile silhouette |
| app-music | `e11cf854` | `org.gnome.Music` | |
| app-settings | `b105969f` | `org.gnome.Settings` | |
| app-software | `91d271bb` | `org.gnome.Software` | |
| app-system-monitor | `4aec024e` | `org.gnome.SystemMonitor` | |
| app-terminal | `96c3f6cf` | `org.gnome.Ptyxis` | |
| app-text-editor | `f55cc335` | `org.gnome.TextEditor` | |
| app-videos | `aaf8912c` | `org.gnome.Showtime` | |
| app-weather | `5f54e8cc` | `org.gnome.Weather` | |
| app-web | `91d42915` | `org.gnome.Epiphany` | |
| shell-show-apps | `87f74383` | (Shell asset) | Stock Shell uses `view-app-grid-symbolic` |
| shell-trash | `8bef2467` | `user-trash` / `user-trash-full` | |
| unreferenced-blue-globe | `8a791f1b` | unknown | Blue tile, white globe |
| unreferenced-red-flame | `2dd02531` | probably `org.mozilla.firefox` | Light tile, red and yellow flame resembling Firefox's mark |
| unreferenced-teal-paw | `483418a7` | unknown | Teal tile, white paw print; possibly a GNOME foot mark (`start-here`, GNOME Tour). Guess only |

### Restyled or new

I can only infer this from the files; I could not compare them with the
Colloid repository offline.

*   **New Apex designs**: the Apex Code icon and both wallpapers. Neither
    appears in Colloid, both use the Apex diamond, and the wallpapers carry
    no third-party traits.
*   **Existing app icons in Colloid's style (34 files)**: every one depicts
    an existing app or a standard shell icon, none an Apex app. Traits
    consistent with one upstream theme's template: identical tile geometry
    in two unit systems, identical stripped shadow-bitmap placeholders,
    Inkscape leftovers (`-inkscape-stroke:none` in `app-image-viewer`,
    `app-logs`, `unreferenced-blue-globe`), and svgo-style single-letter
    ids. That fits "App icons stay Colloid": these are most likely Colloid's
    own files, not Apex originals.
*   **Possibly modified**: 11 files carry a C2PA content-credentials
    manifest in `<metadata>` signed "Anthropic Claude Content Signing",
    stating that Claude provided the file and "may have created or modified
    the file contents", with origin confidence "unknown". They are
    app-calendar, app-files, app-mail, app-music, app-settings,
    app-software, app-terminal, app-text-editor, app-web, shell-show-apps
    and shell-trash. The other 23 have no provenance data.

Before shipping, diff each file against the matching file in the pinned
Colloid release. Identical files can be dropped from the Apex tree and taken
from the Colloid package. Changed files are derivative works of a GPL-3.0
theme and stay GPL-3.0.

### Colloid: licence, tracking and accents

*   Licence: GPL-3.0. Ship the licence text and a source offer with the
    theme (an RPM with `License: GPL-3.0-only` or `-or-later` per upstream's
    files, and `/usr/share/licenses/<package>/COPYING`). The Apex Code icon
    and wallpapers need their own licence statement.
*   Tracking: Colloid is a single-maintainer project without formal
    releases on a fixed schedule. Pin a commit, package it (Fedora may
    already carry a package; check), and keep Apex overrides in a separate
    theme that inherits from Colloid so updates do not overwrite them.
*   Accents: Colloid's installer builds colour variants named default
    (blue), purple, pink, red, orange, yellow, green, teal and grey, with
    light and dark sub-variants. Eight map to GNOME's accents by name; grey
    stands in for slate. Two caveats:
    *   The variants are separate icon themes chosen at install time; GNOME's
        `accent-color` key does not switch icon themes. Following the accent
        needs a small helper that sets `icon-theme` when `accent-color`
        changes (patch or session service, small).
    *   Colloid's hues are its own, not libadwaita's (the canvas folder
        colours `--folder` `#5b9bf8` and `--folder-back` `#3f7fe0` in
        `Tiling.dc.html:18` look like Colloid's blue, not `#3584e4`). As far
        as I know the variants recolour folders and places, not app tiles,
        so app icons do not change with the accent either way.
    *   Shipping all nine variants costs disk in the image; measure the
        installed size before deciding.
*   Coverage: apps Colloid does not cover (most Flathub apps) keep their own
    Adwaita-style icons, so the dock and app grid will mix two styles. This
    is inherent in choosing a third-party theme.

## Sizes and install layout

GNOME needs one scalable full-colour SVG and one symbolic SVG per app. No
bitmap sizes are required; the 128/64/32/54 px renderings in artboard 43 are
previews of the same SVG. GNOME's guidelines draw app icons on a 128 px
canvas; the Colloid style uses 64 px, which is fine for a scalable icon.

Apex-owned app icons (none yet besides Apex Code; for future Apex apps),
hicolor layout:

```
/usr/share/icons/hicolor/scalable/apps/<app-id>.svg
/usr/share/icons/hicolor/symbolic/apps/<app-id>-symbolic.svg
```

Theme overrides for upstream apps, including Apex Code (icon name stays
`org.gnome.Builder`):

```
/usr/share/icons/Apex/index.theme          # Inherits=Colloid,Adwaita,hicolor
/usr/share/icons/Apex/scalable/apps/org.gnome.Builder.svg
/usr/share/icons/Apex/symbolic/apps/org.gnome.Builder-symbolic.svg
/usr/share/icons/Colloid*/...              # from the Colloid package
```

Select it with a GSettings vendor override:

```
# /usr/share/glib-2.0/schemas/zz0-apex.gschema.override
[org.gnome.desktop.interface]
icon-theme='Apex'
```

Build steps in the image build (the `/usr` tree is read-only at run time
on an image-based system, so caches must be generated at build time):

```
gtk-update-icon-cache -f /usr/share/icons/hicolor
gtk-update-icon-cache -f /usr/share/icons/Apex
glib-compile-schemas /usr/share/glib-2.0/schemas
```

Icon themes apply to Flatpak apps too: the theme override is looked up by
icon name before the app's exported hicolor icon. If Apex Code ships as a
Flatpak, the shell, dock and app grid still show the Apex icon, but in-app
uses (About dialog) show whatever the Flatpak bundles unless the build
replaces it.

### Wallpaper install

```
/usr/share/backgrounds/apex/facets-l.svg
/usr/share/backgrounds/apex/facets-d.svg
/usr/share/backgrounds/apex/{slate,sage,sand,mist,ink}.svg
/usr/share/gnome-background-properties/apex.xml
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">
<wallpapers>
  <wallpaper deleted="false">
    <name>Facets</name>
    <filename>/usr/share/backgrounds/apex/facets-l.svg</filename>
    <filename-dark>/usr/share/backgrounds/apex/facets-d.svg</filename-dark>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>#e8ebf0</pcolor>
    <scolor>#0f1115</scolor>
  </wallpaper>
  <!-- One entry per solid colour: Slate, Sage, Sand, Mist, Ink. -->
</wallpapers>
```

```
# same override file as above
[org.gnome.desktop.background]
picture-uri='file:///usr/share/backgrounds/apex/facets-l.svg'
picture-uri-dark='file:///usr/share/backgrounds/apex/facets-d.svg'
picture-options='zoom'
primary-color='#e8ebf0'

[org.gnome.desktop.screensaver]
picture-uri='file:///usr/share/backgrounds/apex/facets-l.svg'
```

GNOME switches between `picture-uri` and `picture-uri-dark` when the
`color-scheme` changes, and Settings > Appearance shows the pair as one
split thumbnail.

## Sanitising

Run every asset through a reviewed pipeline before it enters a package:

1.  Optimise with `svgo` (or `scour`) with a config that keeps `viewBox`,
    keeps ids referenced by `url(#…)` filters and gradients, and removes
    `<metadata>`, editor namespaces and comments.
2.  Remove the empty `<image>` elements (dead nodes; all 34 icon files
    contain one or two).
3.  Reject any file that contains `<script>`, event attributes (`on*`),
    `<foreignObject>`, external `href`s or `data:` URIs. I found none in the
    current files.
4.  Remove the C2PA manifests from shipped files (about 6 KB each), but keep
    the original files and a provenance record in the design repository
    (see AW-6).
5.  Render each file before and after with `rsvg-convert` at 64 and 128 px
    and compare; differences above anti-aliasing noise fail the step.
6.  Record the SHA-256 of each shipped file next to `MANIFEST.md`.

## States

| State | Behaviour |
| --- | --- |
| Light style | `picture-uri` (facets-l); icons unchanged |
| Dark style | `picture-uri-dark` (facets-d); icons unchanged (Colloid light and dark variants differ in places and symbolic colours, not app tiles) |
| Accent change | Wallpaper unchanged; Apex Code tile stays `#3584e4` as drawn; see AW-3 |
| Solid wallpaper chosen | Same picture in light and dark |
| Unknown aspect ratio (external monitor) | `zoom` crops evenly; base colour fills during load |
| High contrast | Not drawn. GNOME high contrast does not change full-colour app icons |
| Missing theme icon | Falls back through Colloid, Adwaita, hicolor |

## Tokens used

*   Colour: `--wall` (light `#e8ebf0` + facets-l, dark `#0f1115` +
    facets-d), `--win`, `--fg`, `--dim` (artboard 43 uses `.66` light and
    `.62` dark; recorded as conflicts in `tokens.json`), `--border`,
    `--dockbg`.
*   Accent: blue `#3584e4` as a fixed literal in the icon tile.
*   Radius: `toast` 20 px (artboard 43 panels), `dock` 24 px (dock strip);
    14 px placeholder tiles (`window`). Icon radii (13 of 56, 26 of 112) are
    artwork, not tokens.
*   Type: 26 px / 800 title and 14 px subtitle (no token for 26 px), 18 px
    `title-4`, 13 px `body`, 12 px `small`.
*   Icon: Apex Symbolic stroke 1.75, round caps and joins, `currentColor`.
*   Literals: `#e8ebf0` canvas, `rgba(29,29,33,.7)` subtitle,
    `rgba(127,127,127,.18)` placeholder tiles, `#000` at .3 icon shadow.

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Facets wallpaper pair | Theme | Files + background-properties XML + GSettings override |
| Solid-colour wallpapers | Theme | One-rect SVGs |
| Colloid icon theme as default | Theme | Package + GSettings override |
| Apex icon theme with Apex Code override | Theme | Small theme inheriting Colloid |
| Apex Code icon and symbolic | Theme | Two SVGs |
| Accent-following icon theme | Patch (S) | Helper to switch `icon-theme` on `accent-color` change; only if AW-3 says so |
| Show Apps full-colour tile | Patch | Shell draws a symbolic icon; see `shell-top-bar-and-dock.md` |
| Trash in the dock | Patch | Not in stock Shell; see `shell-top-bar-and-dock.md` |
| "Apex Code" name on `org.gnome.Builder` | Patch (S) | Desktop file name; see `apex-code.md` |

## Accessibility

*   App icons are decorative next to their app name; every place that shows
    an icon must also expose the app name (Shell does this by default).
*   The symbolic Apex Code glyph sits off the pixel grid (points at .3, .7
    and .1 px). At 16 px on a scale-1 display the 1.75 stroke will blur;
    snap to the grid or accept it, since the target panel is scale 2.
*   Wallpaper contrast: the top bar and dock sit on glass over the
    wallpaper. The strongest tone (`#90a9cf` light core) sits bottom right,
    away from the top bar, and the dock is centred, so bar and dock text sit
    on the pale tones at 16:10 and 16:9 crops.
*   Reduced motion and large text do not apply.

## Acceptance criteria

1.  On a fresh install, `gsettings get org.gnome.desktop.background
    picture-uri` and `picture-uri-dark` return the facets-l and facets-d
    file URIs.
2.  Switching Settings > Appearance between light and dark changes the
    desktop wallpaper between the two files without logging out.
3.  Settings > Appearance lists Facets as one light/dark split thumbnail
    plus Slate, Sage, Sand, Mist and Ink.
4.  A screenshot of the empty desktop at 2880x1800 device px matches a
    reference render of each SVG (`rsvg-convert -w 2880 -h 1800`) within
    anti-aliasing tolerance; layer colours match the table above exactly.
5.  On a 1920x1080 monitor the wallpaper fills the screen with no bars and
    no stretching.
6.  `gsettings get org.gnome.desktop.interface icon-theme` returns `'Apex'`
    and `/usr/share/icons/Apex/index.theme` inherits from Colloid.
7.  The dock, app grid and Alt+Tab show the Apex Code icon for
    `org.gnome.Builder`, whether Builder is installed as an RPM or a
    Flatpak.
8.  `gtk4-icon-browser` (or a lookup script) resolves
    `org.gnome.Builder-symbolic` to the Apex file and renders it in the
    foreground colour in both styles.
9.  The Apex Code icon at 64 px overlays the Colloid tile template exactly
    (56 px tile, 13 px radius, 4 px margin).
10. No shipped SVG contains `<metadata>`, `<image>`, `<script>`, `on*`
    attributes, `<foreignObject>`, `data:` URIs or external references
    (grep in the built image).
11. The image contains the GPL-3.0 licence text for the icon theme and a
    licence statement for the Apex Code icon and wallpapers.
12. Each of the 29 app icons resolves for the app id in the inventory table
    on the installed system, or the table is corrected.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

*   **AW-1**: Confirm Colloid as the app icon theme, and pin a commit or
    package version. This decides licence obligations and whether the 34
    asset files ship at all or come from the Colloid package.
*   **AW-2**: Are the 11 C2PA-marked icons modified from Colloid? A diff
    against the pinned Colloid tree answers it. Modified files need review
    and stay GPL-3.0.
*   **AW-3**: Should the Apex Code tile follow the system accent (nine
    variants plus a switcher) or stay blue? Should the icon theme follow the
    accent through Colloid's colour variants? Neither is drawn.
*   **AW-4**: Drop shadows: the asset icons lost their bitmap shadow
    (empty `<image>`), while the Apex Code icon draws a vector shadow
    (`CodeIcon.dc.html:21`). Restore Colloid's shadows, or remove the
    shadow from Apex Code so they match?
*   **AW-5**: Identity and purpose of the three unreferenced icons
    (blue globe, red flame, teal paw). If the flame is Firefox, which ships
    "on request" per the Launcher notes, the icon comes from Colloid anyway.
*   **AW-6**: Keep or strip the C2PA provenance manifests in shipped files?
    This spec proposes stripping them from packages and keeping originals in
    the design repository.
*   **AW-7**: Which app is "Mail" (`app-mail`), shown only in the Settings >
    Apex Desktop dock preview? GNOME has no default mail client.
*   **AW-8**: The dock order differs between the main dock (Bazaar) and the
    Apex Desktop preview (Mail, Software); see `MANIFEST.md`. Settle it in
    `shell-top-bar-and-dock.md`.
*   **AW-9**: The artboard title cites "apex-desktop#38", an issue tracker
    reference with no other context.
