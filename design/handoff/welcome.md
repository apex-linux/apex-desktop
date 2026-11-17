# First-run welcome

## Summary

The Welcome app is a three-page window shown on the desktop the first time a
user logs in (artboard 21, `Welcome.dc.html`). Page 1 introduces the system,
page 2 lists keyboard shortcuts, and page 3 sets the style (light or dark)
and the accent colour, applied live to the whole desktop.

The canvas draws no installer, no disk setup and no account creation. The
Welcome app assumes a user account already exists and the session is running
(the top bar shows "Welcome" as the focused app, `Welcome.dc.html:32`).

## Upstream mapping

| Option | Fit | Notes |
| --- | --- | --- |
| New small libadwaita app, or a fork of GNOME Tour (`gnome-tour`, Rust + libadwaita, `Adw.Carousel`) | Best fit | Runs inside the session as a normal window with a close button, Back / Next, page dots, and live settings changes. That is the GNOME Tour shape. GNOME Tour has no settings pages, so the style and accent page is new code either way |
| gnome-initial-setup | Poor fit for this artboard | Runs before or at the start of the first session, with its own header-bar navigation, and owns language, keyboard layout, privacy, time zone, online accounts and user creation. It does not show the desktop behind it |
| GNOME Shell `js/ui/welcomeDialog.js` | Related | The stock "Welcome to GNOME" dialog that offers the tour. Disable it, or point it at the Welcome app, via `org.gnome.shell welcome-dialog-last-shown-version` |

Recommendation: a new app (working name `org.apex.Welcome`), started once per
user by an autostart entry after gnome-initial-setup has finished. Confidence:
medium; it depends on the installer and account flow, which the canvas does
not draw. gnome-initial-setup (or the Fedora installer) is still needed for
account creation.

## Layout and measurements

All values are logical px on the 1440x900 artboard.

### Window

| Element | Value | Source |
| --- | --- | --- |
| Window | 660 x 640 px at (390, 96), horizontally centred; radius 14 px; `--win`; shadow `shadow.window` (`var(--shadow), 0 0 0 1px var(--border)`) | `Welcome.dc.html:45` |
| Header | 47 px tall, no title, padding `0 10px`, close button at the end | `:46` |
| Close | 24 px circle, `--btn`, 14 px cross at stroke 1.75 | `:47` |
| Content | Flexes (517 px tall), padding `0 56px` (548 px content width) | `:50` |
| Footer | 76 px tall, padding `0 24px`, space-between: Back, page dots, Next | `:130` |
| Back | 36 px tall, min width 110 px, padding `0 18px`, radius 18 px, `--btn`, 13 px / 600; hidden (keeps its space) on page 1 | `:131`, `:194` |
| Next | Same size; fill `--accent`, text `#fff`; label "Next", or "Get Started" on page 3 | `:135`, `:195` |
| Page dots | Gap 6 px; dot 7 x 7 px, radius 4 px, `--fg`; current dot 22 px wide at opacity .85, others opacity .25; width animates 250 ms `cubic-bezier(.2,.8,.2,1)`; accessible name "Page N of 3" | `:132-133`, `:190-191` |

### Page 1: Welcome to Apex

| Element | Value | Source |
| --- | --- | --- |
| Stack | Column, centred, gap 28 px, padding-top 8 px | `:52` |
| Hero tile | 96 x 96 px, radius 26 px, background is the wallpaper (`--wall`), shadow `inset 0 0 0 1px var(--border), 0 8px 22px rgba(0,0,0,.12)` | `:53` |
| Hero mark | 32 px square, 4 px `--accent` border, radius 6 px, rotated 45 deg (the Apex diamond) | `:54` |
| Title | "Welcome to Apex", 28 px / 800, letter-spacing -0.6 px | `:57` |
| Subtitle | 13.5 px `--dim`, 6 px under the title | `:58` |
| Feature list | Full width, gap 18 px between rows | `:60` |
| Feature row | Gap 14 px; 36 px icon tile, radius 10 px, fill `color-mix(in srgb, var(--accent) 14%, transparent)`, 20 px glyph in `--accent`; title 14 px / 700; body 12.5 px `--dim`, line-height 1.45, 2 px under the title | `:61-72` |

### Page 2: Get around with the keyboard

| Element | Value | Source |
| --- | --- | --- |
| Stack | Column, gap 22 px, padding-top 8 px, left aligned | `:78` |
| Title | 24 px / 800, letter-spacing -0.5 px | `:80` |
| Subtitle | 13.5 px `--dim`, 6 px under | `:81` |
| Card | Radius 12 px, `--card`, `shadow.card` | `:83` |
| Row | Min height 50 px, padding `0 14px`, gap 12 px; 1 px `--border` between rows; label 13.5 px | `:86`, `:177` |
| Key cap | `kbd`: min width 28 px, 26 px tall, padding `0 8px`, radius 7 px, `--btn`, `inset 0 -1px 0 var(--border)`, Inter 12 px / 600; caps 4 px apart, no "+" between them | `:88` |

### Page 3: Make it yours

| Element | Value | Source |
| --- | --- | --- |
| Title and subtitle | As page 2 | `:99-100` |
| Style picker | Radio group, 2 columns, gap 16 px | `:102` |
| Style option | Column, gap 10 px, label 13 px / 600 below the preview | `:103`, `:110` |
| Preview | Full column width (266 px), aspect 16:10 (about 166 px tall), radius 12 px; light uses the light wallpaper, dark the dark wallpaper; chosen ring `0 0 0 3px var(--accent)`, other `0 0 0 1px var(--border)` | `:104`, `:111`, `:178` |
| Preview contents | Top bar strip 9 px (`rgba(250,250,252,.6)` light, `rgba(12,12,16,.5)` dark); window 62 % x 62 % at 12 % / 16 %, radius 8 px, `#fafafb` light or `#242428` dark, shadow `0 4px 12px rgba(0,0,0,.12)` / `.4` | `:105-106`, `:112-113` |
| Accent label | "Accent" 13.5 px / 700, 12 px above the swatches | `:119` |
| Swatches | Radio group, row, gap 14 px; 30 px circles in the accent colour; chosen ring `0 0 0 2px var(--win), 0 0 0 4px <colour>`; accessible name is the colour name | `:120-122`, `:167` |

Swatch order: Blue `#3584e4`, Teal `#2190a4`, Green `#3a944a`, Yellow
`#c88800`, Orange `#ed5b00`, Red `#e62d42`, Pink `#d56199`, Purple `#9141ac`,
Slate `#6f8396` (`:164`). These are the nine GNOME accents in `tokens.json`.

### Copy

Window: accessible names "Welcome window", "Close"; buttons "Back", "Next",
"Get Started".

Page 1 (`:57-71`):

*   "Welcome to Apex"
*   "Fedora Linux 45 and GNOME 51, made for the Vivobook Pro 14X OLED"
*   "Updates that never surprise you" / "New versions download in the
    background and start only when you restart. If one fails to start, Apex
    goes back by itself."
*   "Sharp on the OLED" / "The 2880 × 1800 panel runs at 90 Hz and exactly 2×
    scale, so text and icons stay crisp."
*   "Tuned for this laptop" / "Speakers, the fingerprint reader, NVIDIA power
    saving and an 80 % charge limit work from the first boot."

Page 2 (`:80-81`, `:169-176`):

*   "Get around with the keyboard" / "Everything is one or two keys away.
    Settings › Keyboard can change any of these."

| Label | Keys |
| --- | --- |
| Overview | Super |
| Search apps, files and settings | Super, Space |
| All apps | Super, A |
| Switch windows | Alt, Tab |
| English ↔ Vietnamese Telex | Super, Alt, Space |
| Lock the screen | Super, L |

Page 3 (`:99-119`): "Make it yours" / "Pick a style and an accent. Settings ›
Apex Desktop has the rest." / "Default" / "Dark" / "Accent".

### Machine-specific and release-specific copy

The owner's laptop is the Vivobook Pro 14X OLED (ASUS M7400QC, 14 inch
2880 x 1800 90 Hz OLED). The distribution targets many machines, so every
string below must be generic, or shown only when the matching hardware or
setting is detected:

| String | Source | Problem | Suggested handling |
| --- | --- | --- | --- |
| "Fedora Linux 45 and GNOME 51, made for the Vivobook Pro 14X OLED" | `:58` | Release numbers go stale; names one machine | Build from `/etc/os-release` and the GNOME version at runtime; drop the machine name or show it only on a detected supported model (DMI product name) |
| "Sharp on the OLED" / "The 2880 × 1800 panel runs at 90 Hz and exactly 2× scale…" | `:67` | True only on this panel | Show only when the built-in panel matches; otherwise a generic display row or none. Values come from Mutter's monitor config, not copy |
| "Tuned for this laptop" / "Speakers, the fingerprint reader, NVIDIA power saving and an 80 % charge limit…" | `:71` | Lists this laptop's hardware and a charge-limit value | Show each item only when present: fingerprint reader (fprintd device), NVIDIA GPU (PCI), charge limit (UPower charge threshold support, value from the setting). Hide the row when nothing applies |
| "English ↔ Vietnamese Telex" with Super+Alt+Space | `:174` | Assumes two specific input sources | Show the row only when two or more input sources are configured; label it "Switch input source" or name the user's sources |
| "80 %" | `:71` | Uses a space before %; Quick Settings uses "87%" (`WifiMenu.dc.html:59`) | Pick one style for the locale |
| "If one fails to start, Apex goes back by itself." | `:63` | Promises automatic rollback | Keep only if the update system ships boot-health rollback; see [updates-and-rollback.md](updates-and-rollback.md) |
| "Settings › Apex Desktop" | `:100` | Names a custom Settings panel | Depends on [settings.md](settings.md) |

## States

### Modelled by the artboard

| State | Behaviour | Source |
| --- | --- | --- |
| Page 1, 2, 3 | Next and Back move one page; dots and Back visibility follow | `:179-195` |
| Light / dark choice | Picking a style re-themes the whole desktop at once | `:162`, `:182`, `:188-189` |
| Accent choice | Picking a swatch changes the accent across the desktop at once | `:163`, `:167` |
| Initial choice | Taken from the current settings (the `dark` and `accent` tweaks) | `:162-163` |

### Needed but not drawn

*   **"Get Started"** does nothing in the artboard (`:180` clamps the page).
    It should close the window and record that the welcome has run.
*   **Close before the end**: also marks the welcome as done (or asks to show
    it again next login; decide).
*   **When it runs**: once per user after first login; not for later logins;
    a way to reopen it (an app-grid entry, or Settings › About).
*   **Keyboard focus** on buttons, rows, previews and swatches.
*   **Window behaviour**: resizable or fixed, and behaviour at smaller
    screens or text scaling (the window is 640 px tall on a 900 px screen).
*   **Swipe** between pages on a touchpad, if `Adw.Carousel` is used.
*   **Locales**: translated strings, and right-to-left layout for the
    footer.

## Tokens used

| Group | Tokens and literals |
| --- | --- |
| Colour | `--win`, `--fg`, `--dim`, `--border`, `--btn`, `--card`, `--card-border`, `--accent`, `--wall`; literal `#fff` on Next; `color-mix(in srgb, var(--accent) 14%, transparent)` for icon tiles (no token); preview literals listed above. Welcome uses the majority `--dim` (`rgba(29,29,33,.62)` light), unlike the shell artboards (`.72`) |
| Type | Inter, `cv05` `ss03`; `small` 12 (key caps), `small-plus` 12.5, `body` 13, `ui` 13.5, `heading` 14, `title-1` 24, `display-3` 28; weights 600, 700, 800; letter-spacing -0.5 px and -0.6 px |
| Radius | `xs` 4 (dots), 6 px literal (hero mark), 7 px literal (key caps), `sm` 8 (preview window), `md` 10 (icon tiles), `pill-bar` 12 (card, previews), `window` 14, 15 px literal (swatches), `card-lg` 18 (buttons), `panel` 26 (hero tile) |
| Shadow | `shadow.window`, `shadow.card`; hero and preview literals above |
| Glass | None (the window is opaque) |
| Motion | `standard` easing; `medium` 250 ms (dots). The style change itself has no transition in the artboard |

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| The app as a whole | New code | No upstream app has these three pages |
| Window, header with close only, footer buttons | Stock libadwaita | `Adw.ApplicationWindow`, `Adw.HeaderBar` with no title, `.pill` buttons, `.suggested-action` for Next |
| Page dots with an elongated current dot | Custom widget | `Adw.CarouselIndicatorDots` draws round dots; the 22 px pill needs a small custom widget or CSS on `Adw.CarouselIndicatorLines` |
| Feature rows, shortcut card | Stock libadwaita | `Adw.PreferencesGroup` / boxed list with `.card`; key caps as labels with a `.keycap` style |
| Style picker | Stock pattern | Same thumbnails as GNOME Settings Appearance (`cc-background-panel` style chooser); writes `org.gnome.desktop.interface color-scheme` (`default` or `prefer-dark`) |
| Accent swatches | Stock setting | Writes `org.gnome.desktop.interface accent-color`; no new key |
| Shortcut values | Config | Read from GSettings at runtime so the list stays correct. The listed bindings are not all GNOME defaults: stock Super+Space switches input source and Alt+Tab switches applications. Apex must ship overrides (`switch-input-source` to Super+Alt+Space, `switch-windows` to Alt+Tab) and a Super+Space binding for Spotlight ([shell-overview-launcher-spotlight.md](shell-overview-launcher-spotlight.md)) |
| Hardware-conditional rows | New code | Detection through fprintd, PCI, UPower and Mutter D-Bus APIs |
| First-run trigger | Config | XDG autostart entry with a per-user "done" flag; disable the stock Shell welcome dialog |

## Accessibility

*   **Contrast.** White 13 px / 600 text on the raw accent fails WCAG AA
    (4.5:1) for every accent: about 3.8:1 on Blue, 3.0:1 on Yellow, 3.3:1 on
    Orange, 3.8:1 on Green. libadwaita draws suggested buttons the same way.
    Either accept libadwaita behaviour or use the darkened accent
    (`--accent-strong`, see [shell-quick-settings-and-screenshot.md](shell-quick-settings-and-screenshot.md))
    for text-bearing fills. Accent glyphs on the 14 % tint (page 1) are
    non-text; Yellow reaches only about 3:1.
*   **Roles.** Style picker and swatches are radio groups with names
    ("Default", "Dark", colour names); the dots have the name "Page N of 3"
    and should be hidden from the tab order. Key caps should be read as
    "Super plus Space", not as separate words.
*   **Keyboard.** Tab order: close, page content, Back, Next. Arrow keys move
    within each radio group. Enter on Next advances; Esc closes. Page
    changes move focus to the page title.
*   **Reduced motion.** With animations off, page changes and the dot width
    change are instant.
*   **Large text.** At text scaling 1.25, page 1 must still fit or scroll
    inside the 517 px content area.

## Acceptance criteria

1.  On a new user's first login, after initial setup, the Welcome window
    opens once, 660 x 640 px, centred horizontally, with no title in its
    header and a 24 px close button.
2.  Page 1 shows the 96 px hero tile with the accent diamond, "Welcome to
    Apex" at 28 px / 800, a subtitle built from the installed OS and GNOME
    versions, and the feature rows.
3.  On a machine without a fingerprint reader, NVIDIA GPU or charge-limit
    support, the "Tuned for this laptop" row does not mention the missing
    item; with none of them, the row is absent.
4.  On a machine whose built-in panel is not 2880 x 1800, the "Sharp on the
    OLED" row is absent or generic and states no wrong numbers.
5.  Back is hidden on page 1; Next reads "Next" on pages 1 and 2 and "Get
    Started" on page 3; the current page dot is 22 px wide.
6.  Page 2 lists six shortcuts whose key caps match the session's actual
    keybindings; changing a binding in Settings › Keyboard changes the cap
    on the next open.
7.  The input-source row appears only when two or more input sources are
    configured.
8.  On page 3, choosing Dark sets `color-scheme` to `prefer-dark` and the
    whole desktop changes at once; choosing Default sets `default`.
9.  Choosing a swatch sets `accent-color` to that colour name and the
    desktop accent changes at once; the chosen swatch shows a 2 px gap and a
    2 px ring in its own colour.
10. "Get Started" or the close button ends the welcome; it does not open
    again at the next login.
11. Every control is reachable with Tab, and radio groups respond to arrow
    keys.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

1.  **Installer and account creation** (blocks first-boot engineering). The
    canvas draws neither. Which installer (Anaconda WebUI, a bootc install
    flow, or preinstalled images) and does gnome-initial-setup create the
    account?
2.  **New app or GNOME Tour fork**, and its app ID and name.
3.  **Machine-specific rows.** Confirm the conditional handling above for the
    page 1 subtitle, "Sharp on the OLED", "Tuned for this laptop" and the
    Telex shortcut.
4.  **Keybinding overrides.** Confirm Super+Space for search, Super+Alt+Space
    for input sources and Alt+Tab for windows; these change GNOME defaults.
5.  **Rollback promise** on page 1: keep only if the update system
    guarantees it.
6.  **Next button contrast**: accept libadwaita behaviour or use the
    darkened accent.
7.  **Reopening the welcome** after it has run: where from?
