# Shell: overview, launcher and Spotlight

## Summary

Three ways to find windows, apps and things:

*   **35 Overview** (`Overview.dc.html`): Activities view with a search entry,
    a row of workspace thumbnails and the current workspace's windows laid
    out as previews with title pills. No tweaks beyond `dark` and `accent`;
    clicking a thumbnail switches workspace, clicking a window selects it.
*   **36 Launcher** (`Launcher.dc.html`): the app grid (Show Apps) with a
    "Utilities" folder, an apps-only search that filters the grid in place,
    and a folder dialog.
*   **38 Spotlight** (`Spotlight.dc.html`): a centred search popup over the
    desktop that searches apps, settings and files and evaluates simple sums.
    Tweak `scene`: `search` (query "disk"), `calculator` (query
    "2880 / 1.5"), `copied` (popup closed, "Copied 1920" toast), `empty`
    (popup open, no query).

Overview and Launcher draw the same background: the wallpaper blurred and
saturated, under a `--scrim` tint (`Overview.dc.html:25-26`,
`Launcher.dc.html:25-26`). Spotlight sits over the plain desktop.

## Upstream mapping

| Element | Upstream component | Confidence |
| --- | --- | --- |
| Overview shell | GNOME Shell `js/ui/overview.js`, `js/ui/overviewControls.js` (`ControlsManager`, `ControlsState.WINDOW_PICKER`) | High |
| Search entry | `overviewControls.js` search entry, `js/ui/search.js` `SearchController` | High |
| Workspace thumbnails | `js/ui/workspaceThumbnail.js` `ThumbnailsBox`, `WorkspaceThumbnail` | High |
| Window previews and title | `js/ui/workspace.js`, `js/ui/windowPreview.js` (`.window-caption`) | High |
| Overview background blur and scrim | None upstream. The overview shows the plain wallpaper. | High |
| App grid | `js/ui/appDisplay.js` `AppDisplay`, `IconGrid`, `ControlsState.APP_GRID` | High |
| Folder tile and dialog | `appDisplay.js` `FolderIcon`, `AppFolderDialog`; folders from `org.gnome.desktop.app-folders` | High |
| Launcher in-place search | None. Stock typing in the app grid switches to the full search results view. | High |
| Spotlight popup | None. GNOME has no search surface outside the overview. | High |
| Spotlight result data | `js/ui/search.js` provider plumbing; `appDisplay.js` `AppSearchProvider`; `js/ui/remoteSearch.js` loading D-Bus `org.gnome.Shell.SearchProvider2` providers from `search-providers/*.ini` | High |
| Settings results | GNOME Settings search provider | High |
| Files results | Nautilus search provider, backed by LocalSearch (Tracker 3) | High |
| Calculator result | GNOME Calculator search provider | Medium |
| "Copied" toast | Shares the shell toast style (radius 20, 40 px tall, tokens.json `radius.toast`); nothing upstream shows it | Medium |

## Layout and measurements

All values are logical px on the 1440x900 artboard (device px = 2x).

### Shared background (Overview and Launcher)

| Layer | Value |
| --- | --- |
| Fallback | Root fill `#888` |
| Wallpaper | `--wall`, inset -60 px on every side, `filter: blur(40px) saturate(140%)` |
| Scrim | `--scrim` over the full monitor |

The overscan of 60 px hides the transparent edge the blur produces.

### Top bar in Overview and Launcher

As specified in `shell-top-bar-and-dock.md`, with these differences:
Activities is pressed (`--btn` fill, `aria-pressed="true"`); there is no
focused app label and no Search button; the clock reads "Sat Oct 24"
"13:45" with no unread dot. In Overview the workspace pills follow the
selected thumbnail.

### Overview

| Element | Measurements | Source |
| --- | --- | --- |
| Search entry | 440x40 at x 500, y 52 (centred); radius 20; `--pill` fill; `inset 0 0 0 1px var(--pill-border)`; padding `0 16px`; `gap:10px`; 14px text | `Overview.dc.html:45` |
| Search glyph | 16 px, opacity .7 | `Overview.dc.html:46` |
| Placeholder | "Type to search", text colour at opacity .55 | `Overview.dc.html:17, 47` |
| Thumbnails row | `top:108px`, centred, `gap:10px` | `Overview.dc.html:50` |
| Thumbnail | 116x70, radius 8, clipped; unblurred `--wall` inside; active ring `0 0 0 2px var(--accent)`, others `0 0 0 1px var(--pill-border)` | `Overview.dc.html:143` |
| Mini window | Rect scaled from the real window (x/1440, y/900); radius 2; `--win`; `0 1px 2px rgba(0,0,0,.2)` | `Overview.dc.html:137` |
| Window preview | Radius 14; clipped; `--win`; `--shadow` (overview value, see Tokens); unselected ring `0 0 0 1px var(--line)`; selected ring `0 0 0 3px var(--accent)` | `Overview.dc.html:133` |
| Preview header | 22 tall, `--head`, 10px/700, app name centred, `border-bottom:1px solid var(--line)` | `Overview.dc.html:61` |
| Title pill | Centred under the preview, top edge 25 px below it; 29 tall, radius 14.5, padding `0 12px`, 12.5px/700, `--pill`, `inset 0 0 0 1px var(--pill-border)`, no wrap | `Overview.dc.html:134` |

The preview bodies (`Overview.dc.html:62-80`) are placeholder drawings of
Files, Terminal, Web and Calendar; a real build shows live window clones.

Window rects as drawn (`Overview.dc.html:107-117`):

| Workspace | Title pill text | Header | x, y | Size |
| --- | --- | --- | --- | --- |
| 1 | "Home" | Files | 230, 214 | 420x258 |
| 1 | "apex-image" | Terminal | 790, 214 | 420x258 |
| 1 | "apex-linux · GitHub" | Web | 510, 510 | 420x250 |
| 2 | "October 2026" | Calendar | 300, 240 | 480x300 |
| 2 | "Rain on Glass" | Music | 840, 270 | 330x240 |

These positions are illustrative; the real layout comes from the stock
window layout strategy. Thumbnail tabs are named "Workspace 1" and
"Workspace 2". The dock shows running dots for Files, Web, Terminal,
Calendar and Music (all workspaces).

### Launcher

| Element | Measurements | Source |
| --- | --- | --- |
| Search entry | 400x40 at x 520, y 52 (centred); otherwise as Overview | `Launcher.dc.html:45` |
| Placeholder | "Search apps" | `Launcher.dc.html:47` |
| Grid | `top:144px; left:150px; width:1141px`; 7 columns of 163 px; rows 161 px | `Launcher.dc.html:50` |
| Cell | Column, centred, `gap:8px`, radius 22 | `Launcher.dc.html:129` |
| App icon | 88x88 | `Launcher.dc.html:53` |
| Label | 13px/600, `max-width:136px`, one line, ellipsis | `Launcher.dc.html:59` |
| First search match | `--btn` fill and `inset 0 0 0 2px var(--accent)` | `Launcher.dc.html:129` |
| Folder tile | 88x88, radius 24, `--folder` (Launcher value), `inset 0 0 0 1px var(--pill-border)`; 2x2 grid, padding 10, `gap:4px`; four 30 px icons | `Launcher.dc.html:55-56` |
| No results | Column at `top:300px`, centred, `gap:8px`; title "No Results" 18px/700 `--fg`; body 13px `--dim` | `Launcher.dc.html:64-66` |

Grid contents, A to Z, two full rows (`Launcher.dc.html:112-121`):

| Row | Items |
| --- | --- |
| 1 | Audio Player, Calculator, Camera, Clocks, Contacts, Document Viewer, Extensions |
| 2 | Firmware, Help, Image Viewer, Maps, Utilities (folder), Videos, Weather |

Pinned dock apps (Bazaar, Calendar, Files, Music, Settings, Terminal, Text
Editor, Web) are not in the grid but are found by search. The Utilities
folder holds Characters, Disk Usage Analyzer, Disks, Fonts, Logs and System
Monitor; the tile previews the first four.

#### Folder dialog

| Element | Measurements |
| --- | --- |
| Click catcher | Transparent, `inset:32px 0 0 0`, closes the dialog; no dimming |
| Dialog | 600 wide at x 420, y 250 (centred); padding `18px 18px 22px`; radius 26 (`panel`); `--panel` (Launcher value) glass `blur(30px) saturate(180%)`; shadow `panel`; column `gap:10px`. Height 334 with six apps. |
| Header | Title "Utilities" 16px/700 centred in the row; close button 28x28, radius 14, `--btn`, 12 px cross (stroke 2), name "Close folder" |
| Grid | 3 columns of 188 px, rows 128 px |
| Item | Column, centred, `gap:8px`, radius 18; 72 px icon; label 13px/600 |

The dock in Launcher draws no running dots, and Show Apps has a `--btn` fill
with radius 14 to show it is active (`Launcher.dc.html:85, 148`).

### Spotlight

| Element | Measurements | Source |
| --- | --- | --- |
| Dialog | 680 wide, `top:96px`, centred; radius 24; `--panel` glass `blur(34px) saturate(180%)`; shadow `panel`; clipped | `Spotlight.dc.html:45` |
| Field row | 60 tall, padding `0 20px`, `gap:14px` | `Spotlight.dc.html:46` |
| Search glyph | 20 px, `--dim` | `Spotlight.dc.html:47` |
| Input | 40 tall, 20px/500, `--fg`, caret `--accent`; placeholder `--faint` | `Spotlight.dc.html:17, 48` |
| Clear button | Shown when the query is not empty; 24x24, radius 12, `--btn`, 10 px cross (stroke 2.2) in `--dim` | `Spotlight.dc.html:50` |
| Results area | `border-top:1px solid var(--border)`, padding `6px 8px 8px`, `max-height:620px`, scrolls | `Spotlight.dc.html:55` |
| Section header | 30 tall, text at the bottom, padding `0 12px 6px`, 11.5px/700, `letter-spacing:.04em`, uppercase, `--dim` | `Spotlight.dc.html:58` |
| Row | 48 tall, padding `0 12px`, radius 12, `gap:12px`; selected fill is the accent at alpha .16 | `Spotlight.dc.html:250` |
| Row title | 14px/600, one line, ellipsis. Calculator title 18px/700 tabular. | `Spotlight.dc.html:251` |
| Row subtitle | 12.5px, `--dim`, one line, ellipsis; 1 px below the title | `Spotlight.dc.html:74` |
| Action hint (selected row only) | 12px/600 `--dim` verb ("Open" or "Copy"), `gap:6px`, keycap "Enter": 20 tall, padding `0 6px`, radius 6, `--btn`, 11px/700 | `Spotlight.dc.html:77` |
| No match | `border-top` as above, 72 tall, centred, 13.5px `--dim` | `Spotlight.dc.html:87` |

Row leading icons, all 32 px:

| Kind | Drawing |
| --- | --- |
| App | The app's full-colour icon |
| Setting | 32x32 tile, radius 9, filled with the panel colour; 16 px white glyph (stroke 1.75) |
| Folder | 32 px folder shape filled with `--accent`, a white line at .35 opacity |
| File | 24x30 page, radius 5, `--file`, `inset 0 0 0 1px var(--border)`; extension text at the bottom (padding 5), 7.5px/800, `letter-spacing:.02em`, `--dim` |
| Calculator | The Calculator app icon |

Setting tile colours (`Spotlight.dc.html:176-188`), literals unless noted:

| Panel | Subtitle | Colour |
| --- | --- | --- |
| Displays | Resolution, refresh rate and Night Light | `#7d5ce6` (no token) |
| Power | Power mode, screen blank and battery | `#3a944a` (green accent) |
| Screen Lock | Privacy & Security | `#3584e4` (blue accent) |
| About | System · name, memory and disk capacity | `#6f8396` (slate accent) |
| File History & Trash | Privacy & Security | `#3584e4` |
| Removable Media | Apps · what happens when a disk is plugged in | `#ed5b00` (orange accent) |
| Keyboard | Input sources and shortcuts | `#6f8396` |
| Sound | Output, input and alerts | `#e62d42` (red accent) |
| Wi-Fi | Networks | `#3584e4` |
| Appearance | Style and accent colour | `#d56199` (pink accent) |
| Apex Desktop | Dock, top bar, glass and corner radius | `--accent` |
| Date & Time | System | `#6f8396` |
| Software Updates | System | `#6f8396` |

Copied toast (`Spotlight.dc.html:93-95`): `bottom:92px` (12 px above the
medium dock), centred; 40 tall, padding `0 16px 0 12px`, radius 20
(`toast`), `gap:10px`, 13.5px/600; `--panel` glass `blur(30px)
saturate(180%)`, shadow `panel`; a 22 px `--accent` circle with a 12 px
white check (stroke 2.2), then "Copied " and the value in tabular figures.

Derived dialog heights: `empty` 60; `search` 597; `calculator` 231; no
match 132.

## States

### Overview

Drawn: workspace 1 or 2 (click a thumbnail; the selection resets to the
first window); one window selected at a time (click). Needed, not drawn:
hover on a preview (stock shows a close button and the caption), the
dynamic empty workspace at the end of the thumbnails, drag a window to
another thumbnail, typing (results view), keyboard focus on a preview,
Escape to leave, and the open and close animation (stock timings apply,
tokens.json `motion.note`).

### Launcher

Drawn:

*   Grid with no query.
*   Query typed: the grid shows every matching app from the grid, the
    Utilities folder and the dock, sorted by name; folders are not results;
    the first match is highlighted. Typing closes the folder dialog.
*   No match: "No Results" and "The launcher searches apps only.
    Super+Space searches everything."
*   Utilities folder open (click the tile); closed by the close button or a
    click outside.

Needed, not drawn: Enter launches the highlighted app; arrow keys move the
highlight; more than one page of apps (stock paging and page dots);
drag-and-drop reorder and folder creation; folder rename (stock); the
right-click app menu (pin to dock, app details); hover and pressed states;
first-run "new app" highlight.

### Spotlight

| Scene | Query | Shown |
| --- | --- | --- |
| `search` | "disk" | APPLICATIONS: Disk Usage Analyzer ("Check folder sizes and available disk space"), Disks ("Manage drives and media"). SETTINGS: About, File History & Trash, Removable Media. FILES: disk-usage-2026-10.csv (~/Documents, CSV), disk-unlock-board.png (~/Pictures/Screenshots, PNG), Disk Images (folder, ~/Downloads), diskspace-notes.md (~/apex/docs, MD). First row selected with "Open" Enter. |
| `calculator` | "2880 / 1.5" | CALCULATOR: "1920", subtitle "2880 / 1.5", hint "Copy" Enter. APPLICATIONS: Calculator ("Perform arithmetic, scientific or financial calculations"). |
| `copied` | none | Popup closed; toast "Copied 1920"; Search button not pressed. |
| `empty` | "" | Field row only, placeholder "Search apps, settings and files, or type a sum". |

Behaviour modelled in `Spotlight.dc.html:204-276`:

*   Matching is a case-insensitive substring of the name or of hidden
    keywords. Names that start with the query rank first; otherwise source
    order. Limits: 4 apps, 3 settings, 4 files.
*   A sum is `number operator number` with `+ - * / × ÷ x`; the result is
    rounded to 6 decimals; division by zero gives no calculator row. A sum
    adds the Calculator app to Applications.
*   Section order: Calculator, Applications, Settings, Files.
*   Arrow Down and Up move the selection (clamped, no wrap); hovering a row
    selects it; Enter activates; Escape closes; the clear button empties the
    query and keeps focus.
*   Activating a calculator row closes the popup and shows the toast;
    activating anything else closes the popup.
*   The top-bar Search button is pressed (`--btn-h`) while the popup is
    open; clicking it reopens Spotlight with an empty query.
*   "No results for “{query}”" when nothing matches.

Needed, not drawn: the opening keyboard shortcut (only the Launcher copy
names one, Super+Space), a click outside to close, toast duration, slow
providers (results arriving late, a spinner or not), more results than the
limit ("show more" or open the provider app), file results that need
LocalSearch indexing that has not finished, right-to-left text, and a
second monitor.

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour | `--wall`, `--scrim`, `--pill`, `--pill-border`, `--win`, `--head`, `--line`, `--view`, `--side`, `--t-bg`, `--t-a`, `--t-b`, `--t-c`, `--btn`, `--btn-h`, `--folder`, `--panel`, `--panel-border`, `--file`, `--fg`, `--dim`, `--faint`, `--border`, `--accent` |
| Type | `typography.family.ui`; 10px (preview header, literal), `micro` 11px, `caption` 11.5px, `small` 12px, `small-plus` 12.5px, `body` 13px, `ui` 13.5px, `heading` 14px, 16px (folder title, literal), `title-4` 18px, 20px (Spotlight input, literal); `features.numbers` on calculator values |
| Radius | `hairline` 2 (mini windows), 6 (keycap, literal), `sm` 8 (thumbnails), 9 (setting tile, literal), `pill-bar` 12 (Spotlight rows), `window` 14 (previews, Show Apps), 14.5 (title pill, literal), `card-lg` 18 (folder items), 20 (search entry; `toast`), 22 (grid cell, literal), `dock` 24 (folder tile; Spotlight), `panel` 26 (folder dialog) |
| Shadow | `--shadow` (overview value for previews), `panel`, `focusRing` (Launcher first match) |
| Glass | Spotlight 34/180 `--panel`, radius 136 at scale 2; folder dialog and toast 30/180 `--panel`; Overview and Launcher background, see the conflict below |

Conflicts recorded in tokens.json:

*   **Glass table versus drawing.** The SPEC table gives the overview scrim
    36 px / 150 % and the launcher scrim 40 px / 160 %; both artboards draw
    `blur(40px) saturate(140%)` (`Overview.dc.html:25`,
    `Launcher.dc.html:25`). tokens.json marks both rows `agrees: false`.
*   `--shadow` in Overview is smaller (`0 12px 32px ...`) than the majority
    value; it is probably intended for previews. Use a separate token name.
*   `--head` in Overview is `#ebebee` / `#303034`, not the majority value.
*   `--panel` in Launcher is `.86` / `.82` alpha, not `.8` / `.76`.
*   `--folder` means a translucent tile in Launcher
    (`rgba(255,255,255,.55)` / `.1`) and a blue folder glyph in Tiling. The
    names must be split.
*   Spotlight radius 24 versus 26 for every other shell panel.
*   `--faint` in Spotlight is `.45` alpha, not `.4`.

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Overview search entry position and pill style | Theme | `.search-entry` CSS |
| Blurred, saturated wallpaper with scrim behind overview and grid | Patch | No upstream blur here. The wallpaper is static, so blur it once and cache it; this one is cheap. |
| Workspace thumbnails at 116x70 | Patch (small) | Stock caps thumbnails at a small fraction of the monitor (`MAX_THUMBNAIL_SCALE` in `workspaceThumbnail.js`) |
| Thumbnail active ring | Theme | `.workspace-thumbnail-indicator` |
| Title pill always shown under each preview | Patch | Stock shows the caption on hover only |
| No app icon on previews | Patch (small) | Stock overlays the app icon on each preview |
| Accent ring on the selected preview | Theme | |
| Only the current workspace, no neighbours peeking | Patch (small) | Stock shows adjacent workspaces at the sides |
| Dock instead of the overview dash | Patch | See `shell-top-bar-and-dock.md` |
| App grid, A-to-Z order, folders | Stock | `app-picker-layout`, `app-folders` |
| 7 columns, 88 px icons, 163x161 cells | Patch (small) | Stock `IconGrid` picks from fixed modes and icon sizes |
| Pinned apps left out of the grid | Stock | GNOME 40+ hides favourites from the grid; the artboard comment says so too (`Launcher.dc.html:104`) |
| No workspace strip above the grid | Patch (small) | Stock shows shrunken workspaces above the app grid |
| Folder tile style | Theme | |
| Folder dialog style | Theme | |
| Folder close button | Patch (small) | Stock dialog has no close button |
| No folder dimming | Theme | |
| Launcher in-place, apps-only search | Patch | Stock switches to the full results view; needs a filter mode in `AppDisplay` and a guard in `SearchController` |
| Show Apps active fill in the dock | Patch | Part of the dock |
| Spotlight popup | Patch or extension | Whole new surface; see below |
| Coloured settings tiles | Patch | Providers return a GIcon; Spotlight needs a panel-to-colour table |
| File page icons with extension | Patch | New drawing from the result's MIME type |
| Calculator row and Copied toast | Patch | See below |

### What Spotlight would take

GNOME Shell has no search popup outside the overview, so Spotlight is new
code. It can be an Apex shell module (in-tree patch) or an extension; the
work is the same:

1.  A modal actor in `Main.layoutManager` with `Main.pushModal`, an
    `St.Entry`, and a scrollable result list. Keyboard: arrows, Enter,
    Escape, click outside.
2.  Reuse the provider plumbing from `js/ui/search.js` and
    `js/ui/remoteSearch.js`: the same `SearchProvider2` providers, the same
    `org.gnome.desktop.search-providers` `disabled` and `sort-order`
    settings, and the same `getInitialResultSet`,
    `getSubsearchResultSet`, `getResultMetas` and `activateResult` calls.
    Do not reuse `SearchResultsView` as is: its layout (provider icon
    column, app grid row) is the overview's. Write new result display
    classes for the grouped, typed list.
3.  Grouping by type ("Applications", "Settings", "Files") instead of by
    provider means mapping provider IDs to sections: the built-in app
    provider, the Settings provider, the Nautilus provider, the Calculator
    provider. Other installed providers need a section rule (owner
    decision).
4.  Per-section limits (4, 3, 4) and prefix-first ranking. Stock providers
    rank their own results; re-ranking across providers is extra work.
5.  The calculator: either keep the GNOME Calculator provider (full
    expressions, out of process, small latency) or evaluate simple sums in
    the shell as the artboard does. The Copied toast needs the shell to
    copy the value itself (`St.Clipboard`) or to know that the provider
    copies on activation. Recommend in-shell copy so the toast is reliable.
6.  Settings subtitles and colours are not in the provider's metas; they
    need an Apex table keyed by panel ID.

Relation to overview search: both should use the same providers and
settings so results agree. The artboards keep three search entry points:
"Type to search" in the overview (stock full results, not drawn), "Search
apps" in the launcher (apps only), and Spotlight (everything). The owner
must decide whether overview search stays, or whether typing in the overview
opens Spotlight.

Cost: Spotlight is the largest item in this group (a new modal surface plus
result shaping, likely 1000+ lines with tests). The launcher filter mode and
the always-on captions are moderate patches that touch code that changes
often upstream.

## Accessibility

*   Spotlight placeholder `--faint` at .45 alpha is 2.8:1 on the light panel
    and 4.0:1 on the dark panel. Use `--dim` for the placeholder to reach
    4.5:1.
*   Spotlight selection is shown only by a 16 % accent fill. Model the list
    as `listbox` with `option` rows and `aria-activedescendant` on the
    entry (the artboard uses `aria-current`), and add the `focusRing` in
    High Contrast.
*   Section headers are uppercase by CSS; expose them in sentence case
    ("Applications") as group names.
*   White glyphs on setting tiles are 3.0:1 to 4.6:1 (yellow accent 3.0:1
    on the Apex Desktop tile is the weakest). Glyphs are decorative; the
    row title carries the meaning.
*   The Copied toast is `role="status"`; Orca must announce "Copied 1920".
*   Overview: each preview is a button named by its window title; workspace
    thumbnails are tabs named "Workspace N". Stock keyboard navigation of
    the overview must keep working with the dock in place of the dash.
*   Launcher: grid cells are named by app; the folder dialog is a modal
    `dialog` named "Utilities" that traps focus, closes on Escape and
    returns focus to the folder tile.
*   Reduced motion: no zoom on overview open; Spotlight and the folder dialog
    appear without scaling. Reduce Transparency: solid `--panel-solid`
    fills and an unblurred, more opaque scrim.

## Acceptance criteria

1.  Opening the overview shows the wallpaper blurred and a `--scrim` tint
    across the whole monitor, including under the top bar.
2.  The overview search entry is 440x40 with radius 20, centred, its top
    20 px below the bar, with placeholder "Type to search".
3.  Workspace thumbnails are 116x70 with radius 8, centred in a row 10 px
    apart, with a 2 px accent ring on the active one.
4.  Each window preview has a title pill 25 px below it, 29 px tall,
    showing the window title without hover.
5.  Clicking a thumbnail switches workspace and updates the workspace pills
    in the Activities button.
6.  Show Apps opens the grid with the same background, a 400 px "Search
    apps" entry, and apps in 7 columns with 88 px icons, sorted A to Z.
7.  Apps pinned to the dock do not appear in the grid, but typing their name
    in "Search apps" shows them.
8.  Typing in "Search apps" filters the grid in place to matching apps only
    (including apps inside folders), sorted by name, with the first match
    outlined by a 2 px accent ring; Enter launches it.
9.  A query with no match shows "No Results" and "The launcher searches
    apps only. Super+Space searches everything."
10. Clicking the Utilities tile opens a 600 px dialog titled "Utilities"
    with six apps in 3 columns; the close button and a click outside close
    it.
11. Clicking the top-bar Search button opens Spotlight: 680 px wide, its top
    at y=96, radius 24, with focus in the entry and the button pressed.
12. Typing "disk" shows sections Applications (2 rows), Settings (3 rows) and
    Files (4 rows) with the first row selected and an "Open" Enter hint.
13. Typing "2880 / 1.5" shows a Calculator row "1920" first; Enter closes
    Spotlight, puts "1920" on the clipboard, and shows a "Copied 1920" toast
    12 px above the dock.
14. Arrow keys move the selection between rows across sections; Escape
    closes Spotlight and returns focus to the previous window.
15. A query with no results shows "No results for “{query}”" in a 72 px
    band.
16. Spotlight, the launcher and the overview return the same app results for
    the same query.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here. Ranked by how much
they block engineering.

1.  Super+Space is GNOME's default shortcut for switching input sources,
    and `Indicators.dc.html:223-224` draws a Vietnamese (Telex) source.
    The Launcher copy assigns Super+Space to Spotlight
    (`Launcher.dc.html:66`). Pick another shortcut or move input switching.
2.  Does overview search ("Type to search") stay as stock full results, or
    hand off to Spotlight? This decides whether `SearchResultsView` needs
    restyling at all.
3.  Background glass values: SPEC table (36/150 overview, 40/160 launcher)
    or the drawn 40/140 for both?
4.  Which providers map to which Spotlight section, and what happens to
    third-party providers?
5.  Calculator: GNOME Calculator provider or in-shell evaluation?
6.  Launcher draws no running dots in the dock (`Launcher.dc.html:85`) while
    Overview does (`Overview.dc.html:148`). Missing state or intended?
7.  Overview draws two workspaces and no empty one; stock dynamic
    workspaces always add an empty last workspace. Keep dynamic workspaces?
8.  Search entry width: 440 in Overview, 400 in Launcher. Intended?
9.  Spotlight radius 24 versus 26 elsewhere; `--faint` .45 versus .4.
10. The Displays tile colour `#7d5ce6` is not one of the nine accents.
11. The query "2880 / 1.5" (`Spotlight.dc.html:125`) echoes the old
    2880x1800 panel spec; it is an example only.
12. Web (GNOME Web) is the pinned browser; the Launcher comment mentions
    "Firefox on request" (`Launcher.dc.html:111`). Confirm the default
    browser.
