# Files (Nautilus)

## Summary

The Files app, redesigned on top of GNOME Files (Nautilus). Three artboards
draw it. They are one prototype with different tweak defaults:

| No. | Artboard | Defaults |
| --- | --- | --- |
| 27 | `Files.dc.html` | `folder` home, `view` grid, `details` off, light |
| 28 | `FilesList.dc.html` | `folder` documents, `view` list, `details` on, `selected` "Apex Fedora — Spec.odt", light |
| 29 | `FilesSearch.dc.html` | `folder` home, `view` list, `query` "apex", dark |

`diff` shows the three files share all markup and logic. The only other
differences are the top-bar clock (10:24, 10:31, 10:38), an unused sidebar
`badge` slot that exists only in `Files.dc.html:63`, and the folder-glyph
fallback (see [Folder glyphs](#folder-glyphs)).

The canvas row is called "Files redesign". This spec says, for each element,
whether stock Nautilus already does it, whether CSS or assets can do it, or
whether it needs a Nautilus code change.

The top bar and dock in these artboards are covered by
[shell-top-bar-and-dock.md](shell-top-bar-and-dock.md). They are not
repeated here.

## Upstream mapping

| Element | Upstream component | Confidence |
| --- | --- | --- |
| Window, sidebar and content split | `NautilusWindow` (`nautilus-window.c`, `.ui`), libadwaita split view | High |
| Places list | `NautilusSidebar` / `NautilusGtkPlacesSidebar` | High |
| Header bar: back, forward, path bar, search, view toggle | `NautilusToolbar`, `NautilusPathBar`, `NautilusQueryEditor` | High |
| Grid view | `NautilusGridView` (GtkGridView), `NautilusGridCell` | High |
| List view | `NautilusListView` (GtkColumnView), `NautilusNameCell` | High |
| Empty states | `AdwStatusPage` inside `NautilusFilesView` | High |
| Selection summary | `NautilusFloatingBar` (stock is an overlay, not a bar) | High |
| Recent, Starred, Trash | `recent:///`, `starred:///` (needs LocalSearch), `trash:///` | High |
| Details pane | None. Closest stock code is `NautilusPropertiesWindow` | High that it does not exist |
| Home dashboard (Recent cards above Folders) | None | High that it does not exist |
| Search filter chips with counts | None. Stock has a filter popover (type, date) in `NautilusQueryEditor` | Medium |
| Storage summary in the sidebar | None. Stock shows free space in Other Locations and in Properties | Medium |

Notes on the stock behaviour this spec relies on were written from Nautilus
45 to 49. The target Nautilus version is not fixed (artboard 32 mentions
GNOME 51 packages). Re-check every "stock" claim against the version that
ships.

## Layout and measurements

All numbers are logical px on the 1440x900 artboard (`Files.dc.html` line
numbers; in the other two artboards lines after 292 are 2 higher).

### Window

| Property | Value | Source |
| --- | --- | --- |
| Frame | x 100, y 48, 1240 x 762 | :52 |
| Corner radius | 14 (`radius.window`) | :52 |
| Shadow | `shadow.window`: `var(--shadow), 0 0 0 1px var(--border)` | :52 |
| Sidebar width | 232, `--side`, 1 px `--border` on the right | :54 |
| Content width | 1008 (without details pane), `--view` | :74 |
| Details pane width | 300, `--win`, 1 px `--border` on the left | :182 |
| Status bar | 30 high, 11.5 px `--dim`, centred, 1 px `--border` on top | :205 |

### Sidebar

| Element | Measurements | Source |
| --- | --- | --- |
| Sidebar header | 47 high, padding 0 8 0 16; title "Files" 14 px / 700 | :55-56 |
| Main menu button | 32 x 32, radius 8, 16 px "hamburger" glyph, aria "Main menu" | :57 |
| List container | padding 2 8 8, gap 1 | :59 |
| Row | 34 high, padding 0 10, radius 8, gap 12, 13.5 px; icon 16 | :364 |
| Row, current | weight 600, fill `--btn-h`; otherwise weight 400, transparent | :364 |
| Separator | 1 px `--border`, margin 6 8 | :61 |
| Storage block | padding 12 16 16, gap 6 | :67 |
| Storage label | 16 px drive glyph + "Apex Fedora", 12.5 px / 600, gap 8 | :68 |
| Storage meter | 4 high, radius 2, track `--btn-h`, fill `--accent` at 41 % | :69 |
| Storage caption | "588 GB free of 1 TB", 11.5 px `--dim` | :70 |

Row order (`:356-360`): Recent, Starred, Home, separator, Documents,
Downloads, Music, Pictures, Videos, Trash. There is no Desktop, Other
Locations, bookmarks, devices or network entry.

### Header bar

| Element | Measurements | Source |
| --- | --- | --- |
| Bar | 47 high + 1 px `--border` bottom, padding 0 10, gap 6, `--head` | :75 |
| Back, Forward | 32 x 32, radius 8; disabled at opacity .35 | :76-77, :405 |
| Path bar | flex 1, 32 high, radius 8, `--btn`, padding 0 4, gap 1, 13 px | :79 |
| Crumb | 26 high, padding 0 9, radius 6 (literal, no token) | :368 |
| Crumb, current | weight 700, fill `--btn-h` | :368 |
| Crumb, ancestor | weight 500, transparent, click navigates | :368 |
| Crumb separator | "/", opacity .4, padding 0 2 | :81 |
| Search field (replaces path bar) | 32 high, radius 8, `--btn`, ring `inset 0 0 0 2px var(--accent)`, padding 0 10, gap 8, 13.5 px | :87 |
| Search field glyph | 16 px, opacity .6 | :88 |
| Search button | 32 x 32, radius 8, `--btn-h` when pressed | :92, :390 |
| View switch | radiogroup, padding 2, radius 10 (`radius.md`), `--btn` | :93 |
| View segment | 34 x 28, radius 8; on: `--view` fill, shadow `0 1px 3px rgba(0,0,0,.15)` | :391 |
| Details button | 32 x 32, radius 8, `--btn-h` when pressed | :97, :390 |
| Window controls | margin-left 6, gap 10; three 24 px circles, `--btn` fill; glyphs 14, 12, 14 px | :98-101 |

### Search filter bar (search only)

| Element | Measurements | Source |
| --- | --- | --- |
| Bar | 46 high, padding 0 16, gap 6, 1 px `--border` bottom | :106 |
| Chip | 30 high, padding 0 12, radius 15 (literal), gap 6, 12.5 px / 600 | :353 |
| Chip, selected | fill `color-mix(in srgb, var(--accent) 16%, transparent)`, text `--accent` | :353 |
| Chip, not selected | fill `--btn`, text `--fg` | :353 |
| Chip count | same size, opacity .6, tabular numbers | :108 |

### Home dashboard (Home, grid view only)

| Element | Measurements | Source |
| --- | --- | --- |
| Section block | padding 18 20 0, gap 10 | :125 |
| Section titles "Recent", "Folders" | 13 px / 700; "Folders" has 12 px extra top padding | :126, :136 |
| Recent card grid | 4 equal columns, gap 10 | :127 |
| Recent card | padding 10, radius 12, gap 10, `--card`, ring `0 0 0 1px var(--card-border)` | :387 |
| Card icon | file icon 36 px, or thumbnail 40 x 28, radius 5 (literal), 1 px `--border` ring | :130-131 |
| Card name | 13 px / 600, one line, ellipsis | :132 |
| Card subtitle | 11.5 px `--dim`, "<folder> · <day>" | :132, :387 |

### Grid view

| Element | Measurements | Source |
| --- | --- | --- |
| Container | padding 10 14 16; columns `repeat(auto-fill, minmax(116px, 1fr))`; gap 4 | :141 |
| Columns at 1008 px content | 8 columns of about 119 px; 5 columns with the details pane open | computed |
| Tile | column flex, padding 8 6 10, gap 6, radius 12 | :329 |
| Folder icon | 72 px, back face `color-mix(in srgb, var(--accent) 68%, #000)`, front `--accent`, white 1.5 px emblem | :144 |
| File icon | 72 px page, fill by type (table below), white 40 % fold, extension text 9 px / 800 white | :145 |
| Thumbnail | 92 x 58, margin 7 0, radius 8, 1 px `--border` ring | :146 |
| Label | 13 px, line-height 1.3, centred, padding 1 7, radius 5 (literal), wraps anywhere | :330 |
| Location line (search, Recent, Starred) | 11 px `--dim`, margin-top -2 | :148 |

### List view

| Element | Measurements | Source |
| --- | --- | --- |
| Container | padding 6 10 16 | :155 |
| Columns, folder | `minmax(0,1fr) 90px 160px` (Name, Size, Modified), gap 16 | :331 |
| Columns, search | `minmax(0,1fr) 150px 90px 140px` (Name, Location, Size, Modified) | :331 |
| Header row | 32 high, padding 0 12 0 8, 11.5 px / 600 `--dim`, 1 px `--border` bottom, margin-bottom 4; Name indented 44 | :403, :157 |
| Row | 44 high, padding 0 12 0 8, radius 10 | :331 |
| Icon cell | 32 x 32 box; folder 30 px, file 28 px, thumbnail 32 x 22 radius 4 | :165-168 |
| Name | 13.5 px, one line, ellipsis, gap 12 after icon | :164, :170 |
| Location, Size, Modified | 12.5 px `--dim`; Size right-aligned, tabular numbers | :172-174 |

The list header has no sort indicator and no Starred column.

### Details pane

| Element | Measurements | Source |
| --- | --- | --- |
| Pane | 300 wide, padding 20, gap 18, scrolls | :182 |
| Preview box | 176 high, radius 12, `--btn`, content centred | :183 |
| Preview: folder | 112 px folder icon with emblem | :184 |
| Preview: file | 104 px file icon with extension | :185 |
| Preview: thumbnail | 220 x 138, radius 10, `0 0 0 1px var(--border), 0 6px 18px rgba(0,0,0,.12)` | :186 |
| Name | 15 px / 700, wraps anywhere | :189 |
| Kind | 12.5 px `--dim`, 3 px below name | :190 |
| Facts | grid `76px minmax(0,1fr)`, row gap 10, column gap 12, 12.5 px; labels `--dim` | :192 |
| Location value | JetBrains Mono 11.5 px, wraps anywhere | :195 |
| Actions | pinned to bottom, gap 8 | :197 |
| Open button | flex 1, 36 high, radius 18 (`radius.card-lg`), `--accent` fill, `#fff` 13 px / 600 | :198 |
| Star button | 36 x 36 circle, `--btn`, 16 px star outline, aria "Star" | :199 |

### Empty state

| Element | Measurements | Source |
| --- | --- | --- |
| Block | fills view, centred column, gap 10, `--dim` | :117 |
| Glyph | 64 px, stroke 1.1, opacity .5 | :118 |
| Title | 20 px / 700 (`title-3`), `--fg` | :119 |
| Subtitle | 13 px | :120 |

### File type colours

The file icon fill comes from a literal map (`:275`). The kind string shown
in the details pane comes from `:276`.

| Type | Fill | Kind string | Extension label |
| --- | --- | --- | --- |
| doc | `#3584e4` | Document | from file name, first 4 chars, upper case |
| sheet | `#3a944a` | Spreadsheet | |
| slides | `#986a44` | Presentation | |
| md | `#6f8396` | Markdown | |
| pdf | `#e62d42` | PDF Document | |
| iso | `#5e5c64` | Disk Image | |
| archive | `#c88800` | Archive | |
| audio | `#d56199` | Audio | |
| video | `#9141ac` | Video | |
| code | `#2190a4` | Source Code | "CODE" when the name has no dot |
| image | `#ed5b00` | Image | images with a thumbnail show the thumbnail |
| folder | accent | Folder | |
| other | `#6f8396` | File | |

Seven of these fills are accent hex values, so a file icon can match the
folder colour (for example a blue Document next to a blue folder).

### Folder glyphs

Folder icons carry a white emblem drawn from the Apex Symbolic set
(`SYM`/`SYMF`, `:282-309`): desktop, documents, downloads, music, pictures,
projects, public, templates, videos, screenshots, home. Folders without an
emblem key behave differently per artboard:

*   `Files.dc.html:310`: no emblem (plain folder). Affects Wallpapers and
    all `apex-*` project folders.
*   `FilesList.dc.html:312`, `FilesSearch.dc.html:312`: Wallpapers gets the
    pictures emblem, names starting with "apex" get a code emblem (`</>`),
    anything else gets the templates emblem. In the details pane this gives
    Trash, Recent and Starred a templates emblem.

Pick one rule. Recommendation: the `FilesList` rule for Wallpapers and
project folders, and the Recent / Starred / Trash sidebar glyph for those
places.

## States

### Tweaks

| Tweak | Options | Default (27 / 28 / 29) |
| --- | --- | --- |
| `folder` | home, documents, downloads, pictures, wallpapers, projects, music, videos, recent, starred, trash | home / documents / home |
| `view` | grid, list | grid / list / list |
| `details` | on, off | off / on / off |
| `dark` | on, off | off / off / on |
| `accent` | the nine accents | blue |
| `selected` | an item name (no editor) | "" / "Apex Fedora — Spec.odt" / "" |
| `query` | text (no editor) | "" / "" / "apex" |

### Folders

Every place the `folder` tweak offers, with what it draws. "Crumbs" is the
path bar text; "Current" is the highlighted sidebar row.

| Folder | Crumbs | Current | Contents (name, size, modified) | Status bar |
| --- | --- | --- | --- | --- |
| home | Home | Home | Folders: Desktop (0 items, —), Documents (5 items, Today, 09:12), Downloads (4 items, Oct 9), Music (3 items, Aug 14), Pictures (5 items, Today, 08:55), Projects (6 items, Oct 19), Public (0 items, —), Templates (0 items, —), Videos (2 items, Oct 3). Grid view adds the Recent cards above. | 9 items |
| documents | Home / Documents | Documents | Apex Fedora — Spec.odt (84 KB, Today, 09:12), Design Tokens.ods (26 KB, Yesterday, 18:40), S1b Review.odp (2.1 MB, Oct 20), HIG Notes.md (12 KB, Oct 18), Invoice-2026-09.pdf (148 KB, Oct 2), Keyboard Shortcuts.odt (31 KB, Sep 29) | 6 items |
| downloads | Home / Downloads | Downloads | Fedora-Workstation-Live-45.iso (2.4 GB, Oct 9), adwaita-icons-src.tar.xz (18.2 MB, Oct 5), inter-4.1.zip (4.6 MB, Sep 30), jetbrains-mono-2.304.zip (5.7 MB, Sep 30) | 4 items |
| pictures | Home / Pictures | Pictures | Folders Screenshots (3 items, Oct 20), Wallpapers (4 items, Oct 21); thumbnails mockup-2880x1800.png (1.9 MB, Today, 08:55), icon-grid.png (240 KB, Oct 12), dock-study.png (410 KB, Oct 7) | 5 items |
| wallpapers | Home / Pictures / Wallpapers | Pictures | Thumbnails apex-facets-light.png (38 KB), apex-facets-dark.png (36 KB), both Oct 21; apex-glass.png (2.1 MB), apex-mono.png (92 KB), both Sep 28 | 4 items |
| projects | Home / Projects | none (Projects is not in the sidebar) | Folders apex-shell (4 items, Oct 19), apex-gtk-theme (0 items, Oct 2), apex-icons (0 items, Sep 28), apex-plymouth (3 items, Oct 15); Makefile (2 KB, Oct 19), README.md (6 KB, Oct 19) | 6 items |
| music | Home / Music | Music | Rain on Glass.flac (38.4 MB, Aug 14), Night Drive.opus (6.1 MB, Aug 2), Focus Loop.ogg (4.8 MB, Jul 21) | 3 items |
| videos | Home / Videos | Videos | Boot Animation v3.webm (12.6 MB, Oct 3), Overview Transition.mp4 (28.9 MB, Sep 30) | 2 items |
| recent | Recent | Recent | mockup-2880x1800.png (Pictures), Apex Fedora — Spec.odt (Documents), HIG Notes.md (Documents), Fedora-Workstation-Live-45.iso (Downloads); grid shows the location line | 4 items |
| starred | Starred | Starred | Projects folder (Home), Design Tokens.ods (Documents); grid shows the location line | 2 items |
| trash | Trash | Trash | Empty state | 0 items |

Folders reachable only by double-click: Desktop, Public, Templates,
apex-gtk-theme, apex-icons (all empty), Screenshots (three PNG thumbnails),
apex-shell (stylesheet.scss, metadata.json, extension.js, README.md) and
apex-plymouth (apex.plymouth, apex.script, logo@2x.png thumbnail).

Sidebar highlight rule (`:363`): a row is current when it is the folder or an
ancestor of it, except Home, which is current only on Home itself. While
searching, no row is current.

### Empty states

| Condition | Glyph | Title | Subtitle |
| --- | --- | --- | --- |
| Trash has no items | trash | Trash is Empty | Deleted files appear here for 30 days. |
| Any other folder has no items | folder | Folder is Empty | Drop files here or create a new folder. |
| Searching, query empty | search | Search Everywhere | Type a name to search Home. |
| Searching, no match (after filter) | search | No Results Found | Try a different name or another filter. |

Not drawn, but a real build needs them: Recent with no history, Starred with
nothing starred, LocalSearch (Tracker) disabled, a folder that cannot be read
(permission denied), an unmounted or missing location, and loading (a large
folder or network share).

"Deleted files appear here for 30 days." is only true if the distro turns on
automatic trash cleanup: `org.gnome.desktop.privacy remove-old-trash-files`
must be `true` (stock default `false`) with `old-files-age` 30.

### Grid and list

*   The view switch is a two-option radio group (Grid view, List view).
    Switching keeps the folder, selection and details pane.
*   The Home dashboard (Recent cards plus the "Folders" title) appears only
    on Home, in grid view, when not searching (`:400`). In list view Home is
    a plain list of nine folders.
*   In search, grid tiles show a location line and list view adds a Location
    column. Recent and Starred show the location line in grid view but do
    not get a Location column in list view (`showLocCol` is only true when
    searching, `:401`).

### Selection

*   Single click selects one item (`:327`). Grid: tile fill accent 16 %,
    label becomes an accent pill with `#fff` text. List: row fill accent
    16 %. Recent card: card fill accent 16 %.
*   Click on empty view space clears the selection (`:114`).
*   Double-click on a folder opens it and pushes history (`:328`).
    Double-click on a file does nothing in the prototype.
*   The status bar adds `· “<name>” selected` (curly quotes) to the count,
    for example `6 items · “Apex Fedora — Spec.odt” selected` (`:376`).
*   Only single selection is modelled. Multi-select (Ctrl, Shift, rubber
    band), hover and keyboard focus are not drawn.
*   Bug in the prototype: selecting a Recent card highlights it but the
    status bar and details pane ignore it, because the selected item is
    looked up in the folder list only (`:370`).

### Details pane

*   Toggled by the Details header button (`aria-pressed`). It shows the
    selected item, or a summary of the current folder when nothing is
    selected (`:371`): name = folder label, kind "Folder", Size "N items",
    Modified "—", Location = path ("~", "~/Documents", "Trash", "Recent").
*   Facts: Size, Modified, Location. Location is the full path, for example
    `~/Documents/Apex Fedora — Spec.odt`.
*   "Open" and "Star" are drawn but not wired. The Star button does not
    reflect starred state (Design Tokens.ods is starred, yet the button is
    the same outline).

### Search

*   The Search header button or typing starts search. The path bar is
    replaced by a field with the placeholder "Search everywhere" and an
    accent focus ring.
*   Scope: every folder under Home, recursively, by case-insensitive name
    substring (`:339-342`). The current folder does not narrow the scope.
*   Filter chips: All, Folders, Documents, Images, Audio & Video, each with a
    live count. Documents means doc, sheet, md, pdf and code types; Audio &
    Video means audio and video.
*   Default query "apex" gives 11 results in folder-walk order: Apex Fedora —
    Spec.odt (Documents); apex-facets-light.png, apex-facets-dark.png,
    apex-glass.png, apex-mono.png (Wallpapers); apex-shell, apex-gtk-theme,
    apex-icons, apex-plymouth (Projects); apex.plymouth, apex.script
    (apex-plymouth). Chip counts: All 11, Folders 4, Documents 3, Images 4,
    Audio & Video 0. Status bar: "11 results".
*   Pressing Search again leaves search and clears the query. Navigating
    anywhere also leaves search and resets the filter to All. Editing the
    query keeps the current filter.

### Navigation

*   Back pops history; disabled (opacity .35) when history is empty.
*   Forward is always disabled; forward history is not modelled.

### Not drawn, needed by a real build

Hover and pressed states for every control; keyboard focus rings; rename;
context menus; new folder; drag and drop; file operation progress (stock
header button); undo toasts; the current-folder menu; sort order and sort
indicator; zoom levels; hidden files; inactive window; maximised and tiled
window; narrow widths (stock Nautilus collapses the sidebar); mounted drives,
network and Other Locations in the sidebar; bookmarks (Projects would
normally be a bookmark).

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour, surface | `--win`, `--view`, `--side`, `--head`, `--card`, `--card-border`, `--shot` |
| Colour, content | `--fg`, `--dim`, `--border` (`--faint` is defined but unused) |
| Colour, control | `--btn`, `--btn-h`, `--accent` |
| Colour, literal | file type fills (table above); `#fff` on accent; thumbnail classes `.wp-slate #4d5868`, `.wp-ink #1b1e25`, `.th-grid #d3d9e2`, `.th-dock #c7d1dd`, `.th-logo #0f1115` (placeholder art, not design) |
| Colour, mixes | accent 16 % (selection, chip), accent 68 % + black (folder back) |
| Type | family `ui` (Inter) and `mono` (Location value); sizes `micro` 11, `caption` 11.5, `small-plus` 12.5, `body` 13, `ui` 13.5, `heading` 14, `subtitle` 15, `title-3` 20; weights 400, 500, 600, 700, 800; tabular numbers for sizes and counts |
| Radius | `hairline` 2, `xs` 4, `sm` 8, `md` 10, `pill-bar` 12, `window` 14, `card-lg` 18, `circle`; literals 5, 6, 15 |
| Shadow | `shadow.window`, `shadow.focusRing` (search field), segmented-on `0 1px 3px rgba(0,0,0,.15)` (literal), thumbnail `0 0 0 1px var(--border), 0 6px 18px rgba(0,0,0,.12)` (close to `shadow.lifted`) |
| Glass | none inside the window |
| Motion | none; the prototype has no transitions |
| Icon | Apex Symbolic, 16 px grid, stroke 1.75, round caps and joins |

## Build classification

| Element | Class | Why / how |
| --- | --- | --- |
| Window frame, radius 14, shadow | theme | libadwaita CSS on the window |
| Sidebar with Recent, Starred, Home, XDG folders, Trash | stock | Stock order matches; the separator is stock |
| Sidebar colours, row height 34, radius 8 | theme | CSS on `.navigation-sidebar` rows |
| Sidebar header with "Files" title and main menu | stock or theme | Stock has the main menu in the sidebar header; check the title in the target version |
| Storage summary under the sidebar | patch | No stock widget. Needs a footer in `NautilusSidebar` that reads `filesystem::free` and `filesystem::size` for `$HOME`. Low to medium cost |
| Back, forward, path bar, crumbs | stock + theme | `NautilusPathBar` already looks like this; CSS for 26 px crumbs and weights |
| Search field in place of the path bar | stock | `NautilusQueryEditor` replaces the path bar |
| "Search everywhere" scope | stock (version dependent) | Nautilus 46+ global search; folder search is stock too but scoped to the current folder |
| Filter chip row with live counts | patch | Stock filters live in a popover and have no counts. Counts need the search engine to report per-type totals. Medium cost |
| Two-segment grid/list switch | patch (small) | Stock has a single toggle button; a linked pair is a `.ui` change |
| Details toggle and details pane | patch | New end pane in `NautilusWindow`, bound to the view selection. Can reuse code from `NautilusPropertiesWindow` and thumbnails. Medium to high cost (multi-select, live updates, previews) |
| Home dashboard (Recent cards above folders) | patch | GtkGridView owns its scroll; putting a card row above it in one scroll needs a custom header or a new view. High cost to do well |
| Grid tile layout, selection pill on the label | theme | CSS on `gridview > child`, the label in `NautilusGridCell`; confirm the label can be styled separately |
| Grid icon size 72 px | patch or accept stock | Stock grid zoom levels are fixed in code; 72 px is probably not one of them |
| List rows 44 px, radius 10, columns | theme | CSS on `columnview` rows; column set is stock (Name, Size, Modified; Location in search) |
| Location column in search | stock | |
| Location line under grid labels (search, Recent, Starred) | patch | Not a stock grid caption, as far as known |
| Persistent status bar with count | patch | Stock removed the status bar; the floating bar shows only the selection. Accepting the floating bar is cheaper |
| Accent-coloured folder icons | theme (assets) + patch (switcher) | Full-colour icons cannot follow the accent at runtime. Ship nine generated icon themes and switch `icon-theme` when `accent-color` changes, or patch Nautilus to tint folders |
| Folder emblems (Documents, Downloads, ...) | theme (assets) | Standard `folder-documents` etc. icon names |
| File icons with extension text | theme (assets), partly | Mime-type icons can carry a baked label per type; the label cannot come from the file name at runtime |
| Thumbnails with radius and ring | stock + theme | Thumbnailers are stock; the 1 px ring and radius are CSS |
| Empty states | stock + patch (strings) | `AdwStatusPage` is stock; the titles match stock; the subtitles differ and need string changes |
| Trash "30 days" | settings | GSettings override, see above |
| Size format "84 KB", "1 TB" | patch or accept stock | GLib `g_format_size` gives "84.0 kB" and "1.0 TB". Recommend stock |
| Date format "Today, 09:12", "Oct 20" | patch or accept stock | Stock formats differ by version and locale; verify |
| Window controls as 24 px circles | theme | CSS on `windowcontrols > button` |

## Accessibility

*   Contrast, measured on the artboard colours:
    *   `--dim` text: 4.74:1 on `--view` and 4.53:1 on `--side` (light);
        6.92:1 and 6.2:1 (dark). Passes AA, but light-on-`--side` is close.
    *   `#fff` on `--accent` (Open button, selected label): 3.0:1 (yellow)
        to 5.9:1 (purple); only purple passes 4.5:1 for 13 px text. Use the
        libadwaita accent foreground and the standalone accent colour
        (`@accent_color`) for text, which libadwaita adjusts for contrast.
    *   Selected chip text (`--accent` on 16 % accent tint): 2.5:1 to 4.7:1.
        Fails for most accents. Same fix.
*   Focus order: sidebar rows, back, forward, path bar or search field,
    Search, view switch, Details, window controls, filter chips, items,
    details pane actions. Stock GTK keyboard navigation applies.
*   Keyboard (stock Nautilus): Ctrl+F search, Ctrl+1 / Ctrl+2 list / grid,
    Alt+Left / Alt+Right history, Enter opens, F2 renames, Delete trashes.
    The details pane needs a shortcut; none is drawn.
*   Screen-reader names in the artboard: "Places", "Main menu", "Back",
    "Forward", "Path", "Search", "Search everywhere", "View", "Grid view",
    "List view", "Details", "Filter results", "Items", "Star", "Disk usage"
    (meter, value 41). The three window-control circles have no names
    (`Files.dc.html:99-101`, plain `<span>`s); the Terminal artboard names
    them "Minimize", "Maximize", "Close". Stock libadwaita names them.
*   Grid items are `role="option"` in a listbox and list rows are
    `role="row"` buttons; stock GtkGridView and GtkColumnView expose the
    right roles already.
*   Reduced motion: nothing animates.
*   Large text: labels wrap in grid; list names ellipsize; the details pane
    wraps the name and path. The 76 px facts label column may clip
    translated labels at large text sizes.

## Acceptance criteria

1.  The window opens at 1240 x 762 logical px with radius 14, a 232 px
    sidebar, 47 px header bars and a 30 px status bar (or the stock floating
    bar, if the owner accepts it).
2.  The sidebar lists Recent, Starred, Home, a separator, Documents,
    Downloads, Music, Pictures, Videos and Trash in that order, each row
    34 px high with a 16 px Apex Symbolic glyph.
3.  Opening Pictures > Wallpapers highlights Pictures in the sidebar and
    shows "Home / Pictures / Wallpapers" with "Wallpapers" in bold on a
    `--btn-h` fill.
4.  Opening Home in grid view shows a "Recent" row of four cards above a
    "Folders" title and the folder grid. Switching to list view removes the
    Recent row.
5.  Each Recent card shows a 36 px icon or 40 x 28 thumbnail, the name in
    13 px / 600 and "<folder> · <day>" in 11.5 px `--dim`.
6.  At a 1008 px content width the grid shows 8 columns; with the details
    pane open it shows 5.
7.  Folder icons use the current accent for the front face and the accent
    mixed 68 % with black for the back face. Changing the accent in Settings
    updates them without restarting Files.
8.  Clicking an item selects it: in grid view the label becomes an accent
    pill with white text; in list view the row gets a 16 % accent fill.
    Clicking empty space clears it.
9.  With one item selected the status bar reads
    `N items · “<name>” selected`.
10. The details pane is 300 px wide, toggles from the Details button, and
    shows preview, name, kind, Size, Modified and Location (monospace) for
    the selection, or the folder summary when nothing is selected.
11. Starting search replaces the path bar with a field showing the
    placeholder "Search everywhere" and an accent ring, shows the chip row
    and a Location column in list view.
12. Searching "apex" from Home returns 11 results with chip counts All 11,
    Folders 4, Documents 3, Images 4, Audio & Video 0 (on the sample data
    set), and choosing a chip filters the results without changing counts.
13. An empty folder shows "Folder is Empty" / "Drop files here or create a
    new folder."; empty Trash shows "Trash is Empty" / "Deleted files appear
    here for 30 days."; a search with no match shows "No Results Found" /
    "Try a different name or another filter."
14. On a default install, `gsettings get org.gnome.desktop.privacy
    remove-old-trash-files` returns `true` and `old-files-age` returns 30.
15. The storage block shows the volume name, a 4 px meter whose fill equals
    used / total for the filesystem holding `$HOME`, and "<free> free of
    <total>".
16. Every text and accent-on-fill pair in criteria 8, 10 and 11 meets
    4.5:1 for all nine accents in light and dark styles.
17. All header-bar buttons, including window controls, have accessible
    names.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

1.  Scope of the redesign. The details pane, Home dashboard, filter chips,
    status bar and storage summary are all Nautilus patches. Which of them
    are must-have? The Home dashboard is the most expensive.
2.  Accent folders: generated icon themes plus a switcher, or a Nautilus
    patch? Either way, other apps that show folder icons (file chooser,
    Spotlight) will follow the same icons.
3.  Folder glyph fallback differs between artboards (see
    [Folder glyphs](#folder-glyphs)).
4.  Should Recent and Starred get a Location column in list view, as stock
    Nautilus does?
5.  Size and date formats: keep GLib / Nautilus formats ("84.0 kB") or
    match the artboard ("84 KB")?
6.  The Home folder "Documents" says "5 items" but Documents holds six
    files (`Files.dc.html:243` against `:247`). Sample data only, but a
    tester comparing screenshots will notice.
7.  Old-spec text: the volume label "Apex Fedora", the file names
    "Apex Fedora — Spec.odt", "mockup-2880x1800.png" and
    "Fedora-Workstation-Live-45.iso", and "1 TB" (the M7400QC ships with
    512 GB or 1 TB). The real volume name and size must come from the
    system; what should the volume be called?
8.  The Tiling artboard draws the same Files window differently: 196 px
    sidebar, Home first in the sidebar, folders in a fixed blue
    (`--folder` `#5b9bf8`) rather than the accent (`Tiling.dc.html:66` and
    `:89` against `Files.dc.html:54` and `:144`). Which is right?
9.  Search scope: always Home, or the current folder with a "search
    everywhere" option?
10. Keyboard shortcut and persistence for the details pane (per window, or
    remembered?).
