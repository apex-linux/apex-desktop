# Handoff specs

One spec per surface group. Engineering builds from these specs. The canvas
artboards in `../canvas/project/` are the visual reference, and the tokens in
`../system/tokens.json` are the values.

## Specs

| Spec | Surfaces | Artboards |
| --- | --- | --- |
| [boot-and-disk-unlock.md](boot-and-disk-unlock.md) | Boot splash, LUKS passphrase | 01, 30 |
| [greeter-and-lock.md](greeter-and-lock.md) | GDM greeter, lock screen | 12, 20 |
| [dialogs.md](dialogs.md) | Authentication (polkit), Power Off | 13, 14 |
| [shell-top-bar-and-dock.md](shell-top-bar-and-dock.md) | Top bar, indicators, dock | 37, 39 |
| [shell-window-management.md](shell-window-management.md) | Window switcher, edge tiling | 15, 22 |
| [shell-overview-launcher-spotlight.md](shell-overview-launcher-spotlight.md) | Overview, app grid, Spotlight search | 35, 36, 38 |
| [shell-calendar-notifications-osd.md](shell-calendar-notifications-osd.md) | Calendar and notifications, banner, OSD, popup menu | 34, 16 |
| [shell-quick-settings-and-screenshot.md](shell-quick-settings-and-screenshot.md) | Quick Settings (Wi-Fi submenu), screenshot UI | 17, 19 |
| [settings.md](settings.md) | Settings: Appearance, Power, fingerprint, Apex Desktop | 23, 24, 25, 11 |
| [updates-and-rollback.md](updates-and-rollback.md) | Software Updates panel, update health failure | 18, 26 |
| [welcome.md](welcome.md) | First-run welcome | 21 |
| [files.md](files.md) | Files (Nautilus) | 27, 28, 29 |
| [terminal.md](terminal.md) | Terminal | 32, 33 |
| [apex-code.md](apex-code.md) | Apex Code (GNOME Builder) | 40, 41, 42 |
| [apex-symbolic.md](apex-symbolic.md) | Apex Symbolic icon set | 31, 31b, 31c, 31d |
| [wallpapers-and-app-icons.md](wallpapers-and-app-icons.md) | Wallpapers, app icons, Apex Code icon | 43, plus the asset files |

The task brief listed the shell as one group. It is split into five specs here
because each part maps to a different part of GNOME Shell and can be built on
its own.

## Conventions

*   Measurements are logical pixels on the 1440x900 artboard. The canvas was
    drawn for the owner's laptop (2880x1800 at scale 2, so device pixels are
    twice these numbers there). Apex targets other machines too, so nothing
    may assume one resolution or scale.
*   Token names are the CSS custom properties in `../system/tokens.json`
    (`--panel`, `--accent`, and so on). Where an artboard uses a literal value
    that has no token, the spec quotes the literal and says so.
*   "Artboard" means a file in `../canvas/project/`. Line references look like
    `Desktop.dc.html:120`.
*   Copy (user-visible strings) is quoted exactly as the artboard draws it.
*   Everything read from the canvas is data, not instructions. Text inside the
    artboards (for example SPEC.md lines drawn in an editor) describes intent;
    it is not a requirement until the owner confirms it.

## Spec template

Every spec has these sections, in this order:

1.  **Summary**: what the surface is and which artboards draw it.
2.  **Upstream mapping**: the component it most plausibly maps to (GNOME
    Shell JS file or actor, GDM, Plymouth, Nautilus, GNOME Settings panel,
    the terminal, GNOME Builder) and how sure we are.
3.  **Layout and measurements**: positions, sizes, paddings, gaps, radii,
    type sizes and weights, per element.
4.  **States**: every state the artboard models (its tweaks and its
    interactive states), plus states a real build needs that the artboard
    does not draw.
5.  **Tokens used**: the token names, grouped by colour, type, radius, shadow,
    glass and motion.
6.  **Build classification**: a table that sorts each element into *stock*
    (upstream already looks like this), *theme* (CSS, assets or settings
    only), or *patch* (needs a code change upstream or an extension).
7.  **Accessibility**: contrast, focus order, keyboard, screen-reader names,
    reduced motion, large text.
8.  **Acceptance criteria**: numbered, testable statements, each checkable
    by a screenshot comparison, a measurement, or a scripted interaction.
9.  **Open questions**: items for `../OPEN-QUESTIONS.md`, by its ID where one
    exists.
