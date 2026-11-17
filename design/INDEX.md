# Apex design index

The design canvas "Apex Fedora Mockups"
(the owner's private canvas) has 38 artboards in ten
rows. This index lists every artboard, the tweaks the canvas offers on it, the
interactive states its prototype models, and the handoff spec that covers it.

## Layout of `.design/`

| Path | Contents |
| --- | --- |
| `canvas/project/` | The canvas files as pulled: `canvas.json` and one `*.dc.html` per artboard. Do not edit. |
| `canvas/assets/` | The 36 SVG assets the artboards reference as `/_blob/<id>`, plus `MANIFEST.md`. |
| `system/tokens.json` | Design tokens with sources and conflicts. |
| `system/README.md` | What each token group means and the rules the canvas implies. |
| `handoff/` | One build spec per surface group; `handoff/README.md` lists them. |
| `OPEN-QUESTIONS.md` | Decisions the owner needs to make, ranked by how much they block engineering. |

## How to read the columns

*   **No.** is the number in the artboard title. Numbers are not in row order
    and one number (11) has two artboards; 31 has four (31, 31b, 31c, 31d).
    Numbers 02 to 10 do not exist on the canvas.
*   **Theme** is the default of the `dark` tweak: L (light) or D (dark).
    "L/D" means the tweak exists; "fixed" means the artboard has no theme
    tweak.
*   **Accent** says whether the artboard has the nine-colour `accent` tweak.
*   **States** lists the other tweaks (`name: options, default first`) and the
    behaviour its JS models when you interact with it.
*   All artboards are 1440x900 unless the size column says otherwise.

## Artboards

### Row 1: Boot

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Boot splash | `Boot.dc.html` | | fixed (black) | no | `progress`: 0 to 100 %, default 58. Static otherwise. | [boot-and-disk-unlock](handoff/boot-and-disk-unlock.md) |
| 30 | Disk unlock | `BootUnlock.dc.html` | | fixed (black) | no | `state`: passphrase, wrong passphrase. Typing and Enter runs an unlock progress bar, then resets. | [boot-and-disk-unlock](handoff/boot-and-disk-unlock.md) |

### Row 2: Sign-in and session

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | GDM greeter | `Main.dc.html` | | fixed (light wallpaper, dark scrim) | no | No tweaks. Interactive: user list, pick a user, password field with "Press Enter to sign in" and "Signing in…", back to user list, "Not listed?", fingerprint hint. | [greeter-and-lock](handoff/greeter-and-lock.md) |
| 20 | Lock screen | `Lock.dc.html` | | L/D, default L | no | `state`: password, wrong password, fingerprint, fingerprint not recognized. Clock 118 px. | [greeter-and-lock](handoff/greeter-and-lock.md) |
| 13 | Authentication dialog | `Polkit.dc.html` | | L/D, default L | yes | `state`: password, wrong password. Details disclosure (Action, Vendor) toggles. Terminal running `apexctl update rollback` behind it. | [dialogs](handoff/dialogs.md) |
| 14 | Power off dialog | `EndSession.dc.html` | | L/D, default L | yes | Countdown seconds; "Start the new version next time" switch changes the primary button to "Restart & Update". | [dialogs](handoff/dialogs.md) |

### Row 3: Desktop and shell

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 21 | Welcome | `Welcome.dc.html` | | L/D, default L | yes | Three pages with Back / Next / Get Started and a page indicator; style (Default, Dark) and accent pickers. | [welcome](handoff/welcome.md) |
| 22 | Edge tiling | `Tiling.dc.html` | | L/D, default L | yes | `target`: left half, maximize. Files window being dragged, Terminal tiled right, tile preview animates. | [shell-window-management](handoff/shell-window-management.md) |
| 15 | Window switcher | `AltTab.dc.html` | | L/D, default D | yes | Click an app tile to select it (default: Terminal, with two window dots). Text Editor behind shows the SPEC.md glass table. | [shell-window-management](handoff/shell-window-management.md) |
| 16 | OSD, banner and popup menu | `Transients.dc.html` | | L/D, default L | yes | `volume`: 0 to 100, default 62. Static banner ("Updates Ready", Later / Restart Now) and dock popup menu. | [shell-calendar-notifications-osd](handoff/shell-calendar-notifications-osd.md) |
| 37 | Desktop: dock and top bar | `Desktop.dc.html` | | L/D, default L | yes | `scene`: desktop, maximised, revealed. `iconSize`: small, medium, large (default medium). `translucentBar`, `runningIndicators`, `showTrash`: on by default. Dock tooltips on hover. | [shell-top-bar-and-dock](handoff/shell-top-bar-and-dock.md) |
| 39 | Top bar: indicators | `Indicators.dc.html` | | L/D, default L | yes | `scene`: everyday, in a call, recording, menu, overflow, everything. App indicator menus and overflow. | [shell-top-bar-and-dock](handoff/shell-top-bar-and-dock.md) |

### Row 4: Settings

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 18 | Settings: Software Updates | `Updates.dc.html` | | L/D, default L | yes | `state`: up-to-date, available, downloading, ready (default), waiting. `showHold`: on. Automatic Downloads switch. Partly superseded: OQ-04 (stock bootc) cuts `waiting` (metered), the hold and the package list. | [updates-and-rollback](handoff/updates-and-rollback.md) |
| 23 | Settings: Appearance | `Appearance.dc.html` | | L/D, default L | yes | Style, accent and background pickers are live (clicking restyles the window). | [settings](handoff/settings.md) |
| 24 | Settings: Power | `Power.dc.html` | | L/D, default L | yes | Switches (charge limit, battery percentage, lower refresh rate, dim screen) and power-mode radio group are live. | [settings](handoff/settings.md) |
| 25 | Fingerprint enrollment | `Fingerprint.dc.html` | | L/D, default L | yes | `progress`: 0 to 100, default 55 (enrollment ring). | [settings](handoff/settings.md) |
| 11 | Settings: Apex Desktop | `ApexDesktop.dc.html` | | L/D, default L | yes | Live options (dock icon size, bar glass, buttons, trash and more) restyle a desktop preview. | [settings](handoff/settings.md) |
| 11 | Settings: Apex Desktop, scrolled | `ApexDesktopScrolled.dc.html` | | L/D, default L | yes | Same panel scrolled to its lower groups. | [settings](handoff/settings.md) |

### Row 5: Quick Settings, capture and recovery

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | Quick Settings: Wi-Fi submenu | `WifiMenu.dc.html` | | L/D, default L | yes | Network list (connected, secured, hotspot, printer). | [shell-quick-settings-and-screenshot](handoff/shell-quick-settings-and-screenshot.md) |
| 19 | Screenshot UI | `Screenshot.dc.html` | | L/D, default L | yes | Capture type (screenshot, screencast), capture area (selection, screen, window), show pointer switch; primary button label follows the type. | [shell-quick-settings-and-screenshot](handoff/shell-quick-settings-and-screenshot.md) |
| 26 | Update health failure | `Rollback.dc.html` | | L/D, default L | yes | `state`: check failed, fell back after 3 boots. Alert with Keep This Version / Go Back… or Show Changes / OK. Both states cut by OQ-04; the spec replaces them with "You Started the Previous Version". | [updates-and-rollback](handoff/updates-and-rollback.md) |

### Row 6: Files redesign

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 27 | Files: Home | `Files.dc.html` | | L/D, default L | yes | `folder`: home (default), documents, downloads, pictures, wallpapers, projects, music, videos, recent, starred, trash. `view`: grid. `details`: off. `selected`, `query`: empty. Sidebar, view switch and selection are live. | [files](handoff/files.md) |
| 28 | Files: list and details | `FilesList.dc.html` | | L/D, default L | yes | Same component: `folder` documents, `view` list, `details` on, `selected` "Apex Fedora — Spec.odt". | [files](handoff/files.md) |
| 29 | Files: search | `FilesSearch.dc.html` | | L/D, default D | yes | Same component: `view` list, `query` "apex". | [files](handoff/files.md) |

### Row 7: Apex Symbolic

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | Apex Symbolic: contact sheet | `Glyphs.dc.html` | 1440x1520 | L/D, default L | no | `stroke`: 1.5, 1.75 (default), 2. `grid`: off. | [apex-symbolic](handoff/apex-symbolic.md) |
| 31b | Apex Symbolic: states and gaps | `GlyphFamilies.dc.html` | 1440x1600 | L/D, default L | no | Same tweaks. | [apex-symbolic](handoff/apex-symbolic.md) |
| 31c | Apex Symbolic: everyday actions | `GlyphActions.dc.html` | 1440x1300 | L/D, default L | no | Same tweaks. | [apex-symbolic](handoff/apex-symbolic.md) |
| 31d | Apex Symbolic: everywhere else | `GlyphMore.dc.html` | 1440x1600 | L/D, default L | no | Same tweaks. | [apex-symbolic](handoff/apex-symbolic.md) |

### Row 8: Terminal

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 32 | Terminal: sessions | `Terminal.dc.html` | | L/D, default L | yes | `session`: gnome, image (default), system, desktop, builder. Session sidebar with state counts, inline agent permission prompt (yes / always / no). | [terminal](handoff/terminal.md) |
| 33 | Terminal: split panes, needs you | `TerminalSplit.dc.html` | | L/D, default D | yes | Same component, `session` gnome, split panes. | [terminal](handoff/terminal.md) |

### Row 9: Calendar, overview, launcher and Spotlight

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 34 | Calendar and notifications | `DateMenu.dc.html` | | L/D, default L | yes | Month navigation, day selection with events, Do Not Disturb switch, dismissable notifications and empty state. | [shell-calendar-notifications-osd](handoff/shell-calendar-notifications-osd.md) |
| 35 | Overview | `Overview.dc.html` | | L/D, default L | yes | Workspace tabs; window thumbnails; search pill. | [shell-overview-launcher-spotlight](handoff/shell-overview-launcher-spotlight.md) |
| 36 | Launcher | `Launcher.dc.html` | | L/D, default L | yes | Search filters the grid ("No Results" empty state); Utilities folder opens as a dialog. | [shell-overview-launcher-spotlight](handoff/shell-overview-launcher-spotlight.md) |
| 38 | Spotlight | `Spotlight.dc.html` | | L/D, default L | yes | `scene`: search, calculator, copied, empty. | [shell-overview-launcher-spotlight](handoff/shell-overview-launcher-spotlight.md) |

### Row 10: Apex Code

| No. | Title | File | Size | Theme | Accent | States | Spec |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 40 | Apex Code (Builder): editor | `Code.dc.html` | | L/D, default L | yes | `view`: project, outline, search, git. `file`: dock.js, feature.js, README.md, engine.rs. `panel`, `completion`, `map` on; `blame`, `find`, `debug`, `agent`, `palette` off. | [apex-code](handoff/apex-code.md) |
| 41 | Apex Code (Builder): palette and agent panel, dark | `CodePalette.dc.html` | | L/D, default D | yes | Imports Code with git view, palette, agent and blame on. | [apex-code](handoff/apex-code.md) |
| 42 | Apex Code (Builder): debugging, find and outline | `CodeDebug.dc.html` | | L/D, default L | yes | Imports Code with outline view, `engine.rs`, debug, find and bottom panel on. | [apex-code](handoff/apex-code.md) |
| 43 | Apex Code: app icon | `CodeIcon.dc.html` | | both shown | no | Static: 128, 64, 32 px and 16 px symbolic, light and dark, in the dock. | [wallpapers-and-app-icons](handoff/wallpapers-and-app-icons.md) |

## Cross-artboard facts

*   Every artboard with a theme tweak uses the same two token classes,
    `.apx-l` and `.apx-d`; see `system/tokens.json` for the values and the
    artboards that deviate.
*   The nine accent options are identical on every artboard that has the
    tweak; the default is Blue `#3584e4`.
*   The GDM greeter has no dark variant and no accent; it always shows the
    light wallpaper under a dark scrim.
*   The dock, top bar and wallpaper appear on 25 artboards. Their order and
    contents are listed in `canvas/assets/MANIFEST.md`.
*   Text from the old single-machine spec appears on several artboards; it is
    collected in `OPEN-QUESTIONS.md`.
