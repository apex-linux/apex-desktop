# Calendar, notifications, banner, OSD and popup menu

## Summary

This spec covers four transient shell surfaces:

*   The calendar and notifications panel that opens from the top-bar clock
    (artboard 34, `DateMenu.dc.html`).
*   A notification banner, drawn as the "Updates Ready" banner with Later and
    Restart Now (artboard 16, `Transients.dc.html`). Its metrics are the
    theme for every banner. Its update content is cut: OQ-04 (2026-11-17)
    chose stock `bootc` with no update daemon, so nothing sends "Updates
    Ready" (see [updates-and-rollback.md](updates-and-rollback.md)).
*   The volume on-screen display (OSD) (artboard 16).
*   A dock app popup menu for Files (artboard 16).

Both artboards draw the top bar and dock in the usual way; those are specified
in [shell-top-bar-and-dock.md](shell-top-bar-and-dock.md) and are only
referred to here.

## Upstream mapping

| Surface | Upstream component | Confidence |
| --- | --- | --- |
| Calendar panel | GNOME Shell `js/ui/dateMenu.js` (`DateMenuButton`, `EventsSection`, `WorldClocksSection`, `WeatherSection`), `js/ui/calendar.js` (`Calendar`, `CalendarMessageList`, `DoNotDisturbSwitch`) | High |
| Notification card in the panel | `js/ui/messageList.js` (`Message`, `NotificationMessage`) | High |
| Banner | `js/ui/messageTray.js` (banner actor, `MessageTray._showNotification`); actions are `Notification.addAction` | High |
| Volume OSD | `js/ui/osdWindow.js` (`OsdWindow`, `OsdWindowManager`) fed by `gsd-media-keys` | High |
| Dock app menu | `js/ui/appMenu.js` (`AppMenu`) on a `js/ui/popupMenu.js` `PopupMenu` with a `BoxPointer`. With a dock extension (Dash to Dock or similar), that extension subclasses the same `AppMenu` | High for `appMenu.js`; the dock choice belongs to the dock spec |
| Unread dot by the clock | `js/ui/dateMenu.js` `MessagesIndicator` | High |

The layout of artboard 34 is the stock GNOME 45+ layout: message list on the
left, date, month grid, events, world clocks and weather on the right, with
the Do Not Disturb switch and Clear button under the list. Most of the work is
theme work. The glass background, the numeric OSD value and the dock menu
contents are not stock.

## Layout and measurements

All values are logical px on the 1440x900 artboard.

### Clock button (open state)

| Property | Value | Source |
| --- | --- | --- |
| Position | Centred in the 32 px top bar | `DateMenu.dc.html:33` |
| Size | 24 px tall, padding `0 12px`, radius 12 px | `:33` |
| Content | `Sat Oct 24` and `13:45` as two labels, 8 px gap, 13.5 px / 700 | `:33` |
| Open fill | `--btn-h` | `:33` |
| Unread dot | 5 x 5 px, radius 3 px, `--accent`, after the time, 8 px gap; shown while the list is not empty | `:33`, `:178` |

### Calendar panel

| Element | Value | Source |
| --- | --- | --- |
| Panel | `top: 38px` (6 px under the bar), `left: 340px`, width 760 px (centred on x = 720), padding 14 px, radius 26 px, gap 14 px between columns | `DateMenu.dc.html:44` |
| Panel fill | `--panel` with glass blur 30 px, saturate 180 % | `:44` |
| Panel shadow | `var(--shadow), inset 0 0 0 1px var(--panel-border)` (token `shadow.panel`) | `:44` |
| Panel height | Content driven. Left column is fixed at 496 px (446 + 10 + 40); right column is about 550 px, so the panel is about 578 px tall | computed |
| Left column | Width 400 px, column flex, gap 10 px | `:46` |
| Notification list | Height 446 px, scrolls (`overflow:auto`), gap 8 px between cards | `:47` |
| Notification card | Padding `12px 10px 12px 14px`, radius 18 px, fill `--msg-card`, ring `0 0 0 1px var(--card-border)`, gap 12 px | `:55` |
| Card icon | 32 x 32 px app icon, top-aligned | `:56` |
| Card header | 11.5 px, `--dim`; app name 600, then `·`, then relative time; 8 px gaps | `:58` |
| Card title | 13.5 px / 700 | `:59` |
| Card body | 13 px / regular, `--dim`, line-height 1.4; text column 296 px wide | `:60` |
| Card close | 24 x 24 px circle, `--btn`, 12 px cross glyph at stroke 2 | `:62` |
| Empty state | Centred in the list: 48 px bell glyph (stroke 1.2, opacity .6, `--dim`), 12 px gap, "No Notifications" 15 px / 700 `--fg` | `:49-51` |
| Footer row | 40 px tall, padding `0 4px`, gap 10 px | `:66` |
| Do Not Disturb | Button with role switch, 32 px tall, padding `0 4px`, 13 px / 600, 12 px gap to the switch | `:67` |
| Switch | Track 46 x 26 px, radius 13 px, `--btn-h` off, `--accent` on; knob 22 px white, `shadow.knob`, left 2 px off and 22 px on; 200 ms `cubic-bezier(.2,.8,.2,1)` on background and left | `:183-184` |
| Clear | Pushed right, 32 px tall, padding `0 16px`, radius 16 px, `--btn`, 13 px / 600; opacity .45 and disabled when the list is empty | `:68`, `:186` |
| Right column | Width 318 px (760 - 28 - 400 - 14), column flex, gap 10 px | `:72` |
| Date header | Padding `2px 6px 0`, gap 1 px; weekday "Saturday" 13 px / 700 `--dim`; date "October 24 2026" 20 px / 800, letter-spacing -0.2 px | `:73-75` |
| Month card | Padding 8 px, radius 18 px, `--card`, ring `--card-border` | `:77` |
| Month header | Padding `2px 2px 6px 8px`; label 14 px / 700; previous and next buttons 32 px circles, 16 px chevrons | `:78-81` |
| Grid | 7 equal columns, 2 px gap; each column about 41.4 px | `:83` |
| Weekday row | 24 px tall, 11 px / 700, `--dim` | `:84` |
| Day cell | 36 px tall, radius 18 px, 13 px tabular numbers, column flex with a 4 x 4 px event dot under the number (2 px gap) | `:163-165` |
| Events card | Padding `10px 14px 12px`, radius 18 px, `--card`, gap 6 px | `:90` |
| Events title | 12.5 px / 700 `--dim`: "Today" for today, otherwise "October 27" style | `:91`, `:192` |
| Event row | 13 px; 4 x 12 px accent bar, radius 2 px; title 600 flexes; time `--dim` tabular; 10 px gaps | `:94` |
| World clocks, weather | Two buttons, 40 px tall, padding `0 14px`, radius 14 px, `--card` with ring, 12.5 px / 600 `--dim`, left aligned, 8 px apart | `:97-99` |

Day cell styles (`DateMenu.dc.html:163-165`):

| Day | Style |
| --- | --- |
| Today | Fill `color-mix(in srgb, #000 25%, <accent>)`, text `#fff`, 700; event dot white |
| Selected (not today) | `inset 0 0 0 2px <accent>`, 700 |
| In month | No fill, `--fg` |
| Outside month | `--faint` (this artboard: light `rgba(29,29,33,.64)`, dark `rgba(244,244,246,.55)`) |
| Has events | 4 px dot in `--accent` (white on today) |

### Notification banner

| Element | Value | Source |
| --- | --- | --- |
| Position | `top: 44px` (12 px under the bar), centred, width 460 px | `Transients.dc.html:43` |
| Box | Padding 12 px, radius 16 px, column flex, gap 12 px; `--panel` with glass 30 / 180; `shadow.panel` | `:43` |
| Icon | 38 x 38 px, gap 12 px to the text | `:45` |
| Header | 11.5 px `--dim`, gap 6 px: "Apex Updates" (600), `·`, "now" | `:47` |
| Title | 13.5 px / 700 | `:48` |
| Body | 12.5 px `--dim`, line-height 1.4; text column 350 px wide | `:49` |
| Dismiss | 24 x 24 px circle, `--btn`, 14 px cross at stroke 1.75 | `:51` |
| Action row | Padding-left 50 px (icon plus gap), gap 8 px; two equal buttons about 189 px wide, 32 px tall, radius 16 px, `--btn`, 13 px / 600 | `:53-55` |

Both actions use the same neutral fill; neither is styled as the default.

### Volume OSD

| Element | Value | Source |
| --- | --- | --- |
| Position | Centred, `bottom: 104px`; box spans y 756 to 796, 24 px above the dock top (y 820) | `Transients.dc.html:75` |
| Box | 40 px tall, padding `0 18px`, radius 20 px, gap 12 px, `--panel` with glass 30 / 180, `shadow.panel`; width 280 px | `:75` |
| Icon | 16 px speaker glyph (two arcs) | `:76` |
| Level bar | 180 x 6 px, radius 3 px, track `--btn-h`, fill `--accent` at `volume`% | `:77`, `:104` |
| Value | 24 px wide, right aligned, 13.5 px / 600, tabular numbers, number only ("62", no % sign) | `:78` |

### Dock app popup menu

| Element | Value | Source |
| --- | --- | --- |
| Position | `left: 325px`, `bottom: 92px`; about 321 px tall, so y 487 to 808, 12 px above the dock | `Transients.dc.html:59` |
| Box | Width 220 px, padding 6 px, radius 14 px, `--panel-solid` (no blur), `shadow.panel`, gap 1 px, 13.5 px text | `:59` |
| Item | 34 px tall, padding `0 10px`, radius 8 px, gap 10 px between icon and label | `:60-72` |
| Hovered item | `--btn-h` (drawn on "Home") | `:62` |
| Separator | 1 px `--border`, margin `4px 8px` | `:61`, `:68`, `:71` |
| Item icons | 16 px Apex Symbolic: home, download, code brackets | `:63-67` |
| Quit row | `justify-content: space-between`; "2 windows" 12 px `--dim` on the right | `:72` |
| No arrow | The box has no BoxPointer arrow | `:59` |

Menu items in order: "New Window", separator, "Home", "Downloads",
"apex-fedora", separator, "Unpin", "App Details", separator, "Quit" with
"2 windows".

The menu is centred on x = 435, but the Files icon it belongs to is centred
on x = 462.5 (dock is 585 px wide starting at x = 427.5). Treat this as a
drawing error: the menu centres on its source icon.

### Copy

Calendar panel (`DateMenu.dc.html`):

*   "No Notifications", "Do Not Disturb", "Clear", "No Events", "Today",
    "Add World Clocks…", "Select Weather Location…".
*   Accessible names: "Notifications and calendar", "Notifications",
    "Previous month", "Next month", "Close <title>", day labels
    "October 24, has events" / "September 30".
*   Weekday initials "S M T W T F S" (week starts on Sunday).
*   Sample notifications (`:126-130`), all sample data:
    *   Settings · now · "Update ready" · "Apex 45.20261024.141 starts after the
        next restart."
    *   Calendar · 5 min ago · "Design review at 14:00" · "Canvas boards 34 to
        36, in 15 minutes."
    *   Terminal · 25 min ago · "Command finished" · "just vm-image exited 0
        after 18 min in apex-image."
    *   Files · 1 h ago · "Copied 4 items" · "To Projects."
    *   Screenshot · 2 h ago · "Screenshot captured" · "You can paste the image
        from the clipboard." (this pair is the stock GNOME Shell screenshot
        notification text)
*   Sample events (`:142-145`): "Design review" 14:00, "Fedora 45 go/no-go"
    16:30, "Fedora 45 release" All day, "S1b starts" All day.

Banner (`Transients.dc.html`): "Apex Updates", "now", "Updates Ready",
"45.20261010.133 is downloaded. GNOME 51.1, Linux 7.2.9 and 6 other packages
start at the next restart.", "Later", "Restart Now", accessible name
"Dismiss".

OSD: accessible name "Volume 62 percent" (static in the artboard, see
States).

Menu: listed above.

## States

### Modelled by the artboards

| State | Artboard behaviour | Source |
| --- | --- | --- |
| Light / dark | `dark` tweak swaps `.apx-l` / `.apx-d` | both |
| Accent | `accent` tweak, nine GNOME accents | both |
| Notifications present | Five cards, newest first | `DateMenu.dc.html:125` |
| Close one | The card leaves the list | `:135` |
| Clear | All cards leave; list shows the empty state; Clear disables at opacity .45 | `:185-186` |
| Empty | Bell glyph and "No Notifications"; unread dot by the clock disappears | `:48-53`, `:178` |
| Do Not Disturb on / off | Switch animates; nothing else changes in the artboard | `:182-184` |
| Month navigation | Previous / next month; selection resets to day 1 | `:171-174` |
| Pick a day | Ring moves to the day; events card retitles and lists that day's events | `:162`, `:168-192` |
| No events | "No Events" in `--dim` | `:92` |
| Volume level | `volume` tweak 0 to 100 sets bar width and number | `Transients.dc.html:96-104` |
| Menu hover | One item drawn in `--btn-h` | `:62` |

### Needed but not drawn

*   **Do Not Disturb side effects.** Stock GNOME hides banners while DND is on
    (critical urgency still shows) and replaces the unread dot by the clock
    with a "notifications disabled" glyph. The artboard keeps the dot tied to
    "list not empty" regardless of DND. Ship the stock behaviour unless the
    owner decides otherwise. The Quick Settings Do Not Disturb tile
    (`WifiMenu.dc.html:122-124`) is the same setting
    (`org.gnome.desktop.notifications show-banners`) and must stay in sync.
*   **Notification grouping.** GNOME Shell 48 and later stack notifications
    from the same app into a group that expands on click. The artboard only
    draws one notification per app, so the grouped, expanded and collapsed
    looks are undefined. Default: stock grouping with these card metrics.
*   **Notification with actions or image in the list**, and **critical
    urgency** styling.
*   **Media player card** (MPRIS) at the top of the list. The dock shows
    Music running, but no player card is drawn.
*   **Hover and focus** on cards, close buttons, day cells and menu items
    other than the one hovered row.
*   **Close button visibility.** The artboard shows the close button on every
    card. Stock shows it on hover and focus only.
*   **Week start and date formats by locale.** "S M T W T F S" and "October
    24 2026" are en_US. Vietnamese and ISO locales start on Monday and format
    dates differently; follow the locale.
*   **World clocks and weather present.** Stock replaces the two buttons with
    clock rows and a forecast once configured. They also need GNOME Clocks
    and GNOME Weather installed; stock hides the sections when the apps are
    absent.
*   **Banner lifecycle.** Slide-in, timeout, hover pause, expand, and what
    "Later" and "Restart Now" do. "Restart Now" should open the End Session
    restart dialog ([dialogs.md](dialogs.md)), not reboot silently.
*   **OSD variants.** Muted (0 and the mute key), the volume glyph per level,
    over-amplification above 100 %, screen brightness, keyboard backlight,
    microphone mute, and an output device label (stock OSD shows the device
    name when several outputs exist). The OSD accessible name must follow the
    value; the artboard hard-codes "Volume 62 percent"
    (`Transients.dc.html:75`).
*   **OSD timeout** (stock hides after 1.5 s) and stacking with a banner.
*   **Dock menu with hybrid graphics.** This laptop has a Radeon iGPU and an
    NVIDIA RTX 3050. Stock `AppMenu` adds "Launch using Discrete Graphics
    Card" (or integrated, per the app's `PrefersNonDefaultGPU`) when
    switcheroo-control reports two GPUs. The artboard does not draw it. Keep
    the stock item, shown only when two GPUs are present.
*   **Dock menu for a pinned app that is not running** (no Quit, "Pin to Dash"
    or "Unpin"), for apps without desktop actions, and the open-windows
    section (see Build classification).

## Tokens used

| Group | Tokens and literals |
| --- | --- |
| Colour | `--fg`, `--dim`, `--faint`, `--border`, `--btn`, `--btn-h`, `--card`, `--card-border`, `--msg-card`, `--panel`, `--panel-solid`, `--panel-border`, `--accent`, `--bar`, `--bar-fg`; literal `#fff` knob and today text; literal `color-mix(in srgb, #000 25%, <accent>)` for today (no token; same colour as the `--accent-strong` that `WifiMenu.dc.html:22` defines) |
| Type | Inter, `cv05` `ss03`; sizes `micro` 11, `caption` 11.5, `small` 12, `small-plus` 12.5, `body` 13, `ui` 13.5, `heading` 14, `subtitle` 15, `title-3` 20; weights 600, 700, 800; `tabular-nums` for days, times and the OSD value |
| Radius | `hairline` 2 (event bar), 3 px literal (OSD bar), `pill-bar` 12 (clock), 13 px literal (switch), `window` 14 (menu, clock buttons), 16 (banner, Clear), `card-lg` 18 (cards, day cells), `toast` 20 (OSD), `panel` 26 |
| Shadow | `shadow.panel`, `shadow.knob`, card ring `0 0 0 1px var(--card-border)` without the second layer of `shadow.card` |
| Glass | "Quick Settings, calendar, toast": blur 30, saturate 180, tint `--panel` (calendar, banner, OSD); none on the popup menu |
| Motion | `standard` easing, `base` 200 ms (switch). Panel, banner and OSD open/close motion is not specified; use stock |

DateMenu overrides four colour roles against the token majority, already
recorded in `tokens.json`: `--card` light `rgba(255,255,255,.72)`,
`--card-border` light `rgba(0,0,10,.06)`, `--faint` `.64` / `.55`, `--dim`
light `.72`. Use the DateMenu values on this surface until the owner rules.

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Panel layout (list left, calendar right, DND and Clear) | Stock | Matches `dateMenu.js` / `calendar.js` |
| Panel, card, day-cell, switch metrics and colours | Theme | `gnome-shell.css` (`.datemenu-*`, `.calendar-*`, `.message`, `.toggle-switch`) |
| Glass blur behind the panel, banner and OSD | Patch | Stock Shell draws these opaque. Needs `Shell.BlurEffect` on each actor plus the saturation patch (`tokens.json` glass, "patch 0003"). Blurring popups that move or animate costs GPU time on every frame; test on the Radeon iGPU at scale 2 |
| Unread dot in accent | Theme | `MessagesIndicator` styling |
| DND glyph by the clock | Stock | Not drawn, keep stock |
| Close button always visible | Patch if kept | Stock toggles it on hover in JS; recommend keeping stock |
| Event accent bar | Theme or small patch | Theme if the stock event row can take a `border-left` style; otherwise one extra actor in `EventsSection` |
| Title-case "Add World Clocks…", "Select Weather Location…" | Stock strings differ | Stock uses sentence case ("Add world clocks…", "Select weather location…"); changing case means patching translations. Recommend stock strings |
| Banner position, width, radius, action buttons | Theme | `.notification-banner` |
| Banner content and sender | Cut | "Apex Updates" / "Updates Ready" had a daemon as sender; OQ-04 removed it. The only update notification left is the health failure alert in [updates-and-rollback.md](updates-and-rollback.md) |
| OSD pill and level bar | Theme | `.osd-window`, `.level` |
| OSD numeric value | Patch | Stock `OsdWindow` has icon, optional label and level bar, no number |
| OSD bottom offset clearing the dock | Theme or dock integration | Stock OSD sits at a fixed bottom margin; with an always-visible dock the margin must account for dock height |
| Popup menu box, item metrics, no arrow | Theme | `.popup-menu-boxpointer`, `-arrow-base: 0` |
| "New Window", "Unpin", "App Details", "Quit" | Stock | `appMenu.js` items |
| Place items "Home", "Downloads", "apex-fedora" with icons | Patch | Stock shows only the static desktop-file actions. Nautilus ships a "New Window" action only. Bookmarks such as "apex-fedora" are per-user and dynamic, so the menu needs code that reads `~/.config/gtk-3.0/bookmarks` (or an app-provided jump list). Expensive for a general mechanism; cheap if limited to Files |
| "2 windows" count on Quit, no window list | Patch | Stock `AppMenu` lists each open window by title and has no count. Removing the list and adding the count changes `appMenu.js` |

## Accessibility

*   **Contrast.** Today's fill is the accent darkened 25 %; white on it is
    about 5.9:1 for blue and 5.0:1 for yellow, which passes. The DND switch
    track and the selected-day ring use the raw accent; they are non-text and
    need 3:1 against the panel, which yellow (`#c88800`) only just reaches.
    Out-of-month days use `--faint` at .64 (light) here; the token majority
    (.4) would fail. Keep .64 for day numbers.
*   **Roles.** List `role="list"` with `listitem` cards; DND is a switch with
    `aria-checked`; the month is a grid of `gridcell` buttons with
    `aria-selected`; the banner and OSD are `role="status"`; the menu is
    `role="menu"` / `menuitem`. Map these to the matching `St` accessible
    roles (stock does for all but the OSD value).
*   **Names.** Close buttons name the notification ("Close Update ready");
    day cells carry "has events". Keep both. The OSD must announce its live
    value.
*   **Keyboard.** Super+V opens the panel (stock). Tab order: notification
    list, DND switch, Clear, previous month, next month, day grid (arrow keys
    move within the grid), events, world clocks, weather. Esc closes. In the
    menu, arrow keys move, Enter activates, Esc closes. Banner actions are
    reachable with Super+N (stock focuses the banner).
*   **Reduced motion.** With `enable-animations` off, the switch and panel
    open without transitions (stock).
*   **Large text.** The list is fixed at 446 px and scrolls; the right column
    grows. Check that "Select Weather Location…" and long event titles
    ellipsize at text scaling 1.25.

## Acceptance criteria

1.  Clicking the clock opens a panel whose top edge is 6 px below the top bar,
    760 px wide, horizontally centred, with a 26 px corner radius.
2.  The panel has a 400 px left column and a 318 px right column with a 14 px
    gap and 14 px padding.
3.  With five notifications, each card is 18 px radius, shows a 32 px icon,
    "App · time" at 11.5 px, a 13.5 px bold title and a 13 px body.
4.  Closing every notification (or pressing Clear) shows the bell glyph and
    "No Notifications" centred in the list, disables Clear, and removes the
    dot next to the clock.
5.  With notifications present, a 5 px accent dot shows 8 px right of the
    time in the top bar.
6.  Toggling Do Not Disturb in the panel toggles the Quick Settings Do Not
    Disturb tile and the reverse; while on, new banners do not appear
    (except critical urgency) and the clock shows the DND glyph.
7.  Today's day cell has the accent darkened 25 % with white bold text; the
    selected day shows a 2 px accent ring; days outside the month use the
    faint colour.
8.  Days with events show a 4 px dot below the number (white on today).
9.  Selecting a day lists its events with a 4 x 12 px accent bar, the title in
    600 and the time right-aligned; a day with none shows "No Events"; today
    is titled "Today".
10. Previous and next month buttons change the grid and the month label.
11. The week start and the date header follow the session locale.
12. A notification banner appears 12 px below the top bar, centred, 460 px
    wide, 16 px radius, with actions in a row of equal-width 32 px pill
    buttons aligned with the text column.
13. A banner with two actions renders them as equal-width pills; choosing an
    action or dismissing leaves the notification in the list unless the
    sender marks it transient. (The drawn update banner itself is cut.)
14. Pressing a volume key shows a 40 px tall OSD pill, 280 px wide, centred,
    whose bottom edge sits 24 px above the dock, with a 180 px accent level
    bar and the numeric value; the OSD hides after the stock timeout.
15. At 0 % or when muted, the OSD shows the muted glyph; the screen reader
    announces the current value.
16. Right-clicking a running Files dock icon opens a solid 220 px menu, 14 px
    radius, no arrow, centred over the icon, 12 px above the dock, with the
    items and separators in the order listed in this spec.
17. On a machine with two GPUs the dock menu offers the stock discrete or
    integrated GPU launch item; on a single-GPU machine it does not.
18. Every glass surface in this spec (panel, banner, OSD) blurs what is behind
    it with blur 30 / saturate 180 in light and dark; the popup menu does not.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

1.  **Glass on transient surfaces** (blocks the panel, banner, OSD). Confirm
    the blur patch and its GPU budget before theming; without it, use
    `--panel-solid`.
2.  **Who sends update notifications, and with which name and text?**
    Artboard 34 shows "Settings" / "Update ready" / "Apex 45.20261024.141
    starts after the next restart." (`DateMenu.dc.html:126`); artboard 16
    shows "Apex Updates" / "Updates Ready" / "45.20261010.133 is downloaded…"
    (`Transients.dc.html:47-49`). Answered 2026-11-17 (OQ-04, OQ-21): both
    are cut; neither ships. The calendar's sample row is sample data only.
3.  **Dock menu contents.** Are bookmarks in the Files menu wanted (patch),
    and should the open-windows list be replaced by a count (patch)?
4.  **OSD numeric value** (patch) and the list of OSD kinds to theme.
5.  **Notification grouping** look for GNOME 48+ stacks.
6.  **Title-case strings** in the panel versus stock sentence case.
7.  **Sample text that names one machine or release.** "Fedora 45 go/no-go",
    "Fedora 45 release", "S1b starts", "just vm-image … apex-image", "Canvas
    boards 34 to 36", "apex-fedora", "Apex 45.20261024.141", "45.20261010.133",
    "GNOME 51.1, Linux 7.2.9". All are sample data; none is shipped copy.
    Version strings in real notifications come from `bootc status`.
8.  **Is a "Restart Now" action allowed to restart directly?** The terminal
    text in artboard 19 says `apexctl` "never reboots the computer by itself"
    (`Screenshot.dc.html:55`); the banner should route through the restart
    dialog. Settled: no update action restarts directly; Restart Now
    actions open the restart dialog.
