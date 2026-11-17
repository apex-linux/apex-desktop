# GDM greeter and lock screen

## Summary

The greeter is the sign-in screen GDM shows after boot: a user list, then a
password prompt for the chosen user. The lock screen is the prompt shown when
a signed-in session is locked: a large clock, the user's avatar and name, and
a password field. Both draw white content on a blurred, darkened wallpaper.

| No. | Artboard | Title | Tweaks | Interactive states |
| --- | --- | --- | --- | --- |
| 12 | `Main.dc.html` | GDM greeter | None | User list; click a user to get the prompt; Back returns; the arrow button shows "Signing in…" |
| 20 | `Lock.dc.html` | Lock screen | `state`: `password` (default), `wrong password`, `fingerprint`, `fingerprint not recognized`; `dark`: false (default) / true | None beyond the tweaks |

Both are fixed scenes (`fixedScenes.greeterAndLock` in `tokens.json`); they
do not use the `.apx-l` / `.apx-d` colour roles and have no accent.

## Upstream mapping

Both surfaces are GNOME Shell code. GDM only runs GNOME Shell in its `gdm`
session mode; the greeter UI is not in the GDM repository.

| Element | Upstream | Confidence |
| --- | --- | --- |
| Greeter | GNOME Shell `js/gdm/loginDialog.js` (`LoginDialog`, `UserList`, `UserListItem`) | High |
| Prompt (both surfaces) | `js/gdm/authPrompt.js` (`AuthPrompt`: cancel button, entry, message label, spinner well) | High |
| Authentication | `js/gdm/util.js` (`ShellUserVerifier`): runs `gdm-password` and, when a reader exists, `gdm-fingerprint` as parallel PAM conversations | High |
| Lock screen | `js/ui/screenShield.js` (locking, idle) and `js/ui/unlockDialog.js` (`UnlockDialog`, `Clock`, blurred background) | High |
| Avatar, name | `js/ui/userWidget.js` (`Avatar`, `UserWidget`) | High |
| Top bar | `js/ui/sessionMode.js` panel layouts for the `gdm` and `unlock-dialog` modes | High |
| Footer logo | `org.gnome.login-screen logo` key, drawn by `LoginDialog` (`_logoBin`) | High |
| Styles | `data/theme/gnome-shell-sass/widgets/_login-dialog.scss`, `_screen-shield.scss`, compiled into `gnome-shell-theme.gresource` | High |

On an image-based system the Shell theme gresource and any patched JS are
baked into the image, so replacing them is a build step, not a runtime hack.

## Layout and measurements

All values are logical px on the 1440x900 artboard; device px are twice these.

### Shared background

| Layer | Value | Source |
| --- | --- | --- |
| Base colour | `#0c1122` greeter, `#0f1115` lock | `Main.dc.html:24`, `Lock.dc.html:23` |
| Wallpaper | Default light wallpaper on the greeter (`3d451127….svg`); on the lock, light wallpaper, or the dark one (`f6073325….svg`) when `dark` | `Main.dc.html:21`, `Lock.dc.html:19-20` |
| Wallpaper inset | `inset: -40px` (oversized so blurred edges do not show) | `Main.dc.html:25`, `Lock.dc.html:24` |
| Filter | `blur(30px) saturate(130%)` | same lines |
| Scrim | `rgba(8,10,20,.68)`; lock in dark mode `rgba(8,10,20,.34)` | `Main.dc.html:26`, `Lock.dc.html:70` |
| Text | `#fff`, Inter, features `cv05`, `ss03` | `Main.dc.html:24` |

### Top bar

| Property | Greeter (`Main.dc.html:28-36`) | Lock (`Lock.dc.html:27-31`) |
| --- | --- | --- |
| Height | 32 | 32 |
| Padding | 0 16 | 0 16 |
| Type | 13 px / 600 | 13 px / 600 |
| Left | Clock "Sun Oct 11  10:09", weight 700 | None |
| Right | Icons 16 px, gap 10: Accessibility, Wi-Fi connected, Volume, Battery 87 percent | Icons 16 px, gap 10: Wi-Fi connected, Volume, Battery 87 percent |
| Background | None (transparent) | None |

The greeter clock string contains two ASCII spaces, which HTML collapses to
one when rendered. Stock GNOME separates date and time with a wider space
(the wall clock format); use the stock format.

The icons are plain SVGs, not buttons. A real build keeps the stock menus
behind them (see "States").

### Greeter, user list

Column centred, top 286, gap 18. `Main.dc.html:39-54`.

| Element | Value |
| --- | --- |
| Heading | "Choose a user", 22 px (`title-2`) / 600, opacity .92 |
| List card | 380 wide (x 530 to 910), radius 12, fill `rgba(255,255,255,.14)`, `backdrop-filter: blur(20px)`, shadow `inset 0 0 0 1px rgba(255,255,255,.22), 0 10px 30px rgba(0,0,0,.18)`, clips children |
| Row | 62 tall, padding 0 12, gap 14, `border-top: 1px solid rgba(255,255,255,.12)` on every row |
| Row hover | Fill `rgba(255,255,255,.06)` |
| Row keyboard focus | Fill `rgba(255,255,255,.01)`, ring `inset 0 0 0 2px #fff` |
| Avatar | 48 x 48 circle, no fill, ring `inset 0 0 0 1px rgba(255,255,255,.35)`, initial 19 px / 700 |
| Name | 15 px (`subtitle`) / 700 |
| Account type | 12.5 px, opacity .72; gap 1 under the name |
| Chevron | 16 px, `M6 3l5 5-5 5`, opacity .7 |
| "Not listed?" | 13 px / 600, opacity .8, no underline |

Rows in the artboard: "Apex" / "Administrator" (initial A) and "Guest" /
"Standard account" (initial G) (`Main.dc.html:97-100`).

Every row has a top border, including the first, so a hairline sits just
inside the card's top edge. Draw separators between rows only, unless the
owner wants that line.

### Greeter, password prompt

Column centred, top 330, gap 14. `Main.dc.html:58-78`.

| Element | Value |
| --- | --- |
| Avatar | 92 x 92 circle, no fill, shadow `inset 0 0 0 1px rgba(255,255,255,.35), 0 10px 30px rgba(0,0,0,.25)`, initial 36 px / 700 |
| Name | 19 px / 700 |
| Form row | Gap 8; total 342 wide (x 549 to 891) |
| Back button | 38 x 38, radius 19, fill `rgba(255,255,255,.12)`, ring `inset 0 0 0 1px rgba(255,255,255,.2)`, icon 16 px `M10 3 5 8l5 5` |
| Password field | 250 x 38 (x 595 to 845), radius 19 (`field`), fill `rgba(255,255,255,.18)`, `backdrop-filter: blur(20px)`, ring `inset 0 0 0 1px rgba(255,255,255,.25)`, padding 0 16 |
| Entry text | 14 px / 500, `#fff`, caret `#fff`; placeholder "Enter Password" at opacity .96 (`Main.dc.html:17`) |
| Sign-in button | 38 x 38, radius 19, fill `rgba(255,255,255,.22)`, ring `inset 0 0 0 1px rgba(255,255,255,.25)`, arrow icon drawn at 20 px |
| Hint | 12.5 px, opacity .7 |
| Fingerprint pill | Margin-top 6 (20 below the hint in total), 30 tall, padding 0 14, radius 15, fill `rgba(255,255,255,.1)`, gap 8, fingerprint icon 16 px, text 12.5 px / 600 "Or touch the fingerprint reader" |

### Greeter, footer

Column centred, bottom 44, gap 12. `Main.dc.html:81-87`.

| Element | Value |
| --- | --- |
| Wordmark row | Gap 12; diamond 14 x 14, `border: 2px solid #fff`, radius 3, rotated 45 deg; "Apex" 18 px (`title-4`) / 800, letter-spacing -0.3 px |
| Line | "Built on Fedora Linux 45 · GNOME", 12 px, letter-spacing 0.4 px, `rgba(255,255,255,.62)` |

### Lock screen

`Lock.dc.html:33-54`.

| Element | Value |
| --- | --- |
| Clock block | Column centred, top 128, gap 2 |
| Date | "Wednesday October 21", 22 px (`title-2`) / 600, opacity .92 |
| Time | "10:09", 118 px (`display-1`) / 700, letter-spacing -4 px, line-height 1.05, tabular figures |
| Prompt block | Column centred, top 540, gap 14 |
| Avatar | 92 x 92 circle, fill `rgba(255,255,255,.22)`, shadow `inset 0 0 0 1px rgba(255,255,255,.35), 0 10px 30px rgba(0,0,0,.25)`, initial "A" 36 px / 700 |
| Name | "Apex", 19 px / 700 |
| Form row | Gap 8; field plus button, 296 wide (x 572 to 868). No Back button |
| Password field | As the greeter field, including `backdrop-filter: blur(20px)` (`Lock.dc.html:74`); error ring see "States" |
| Unlock button | As the greeter sign-in button; label "Unlock" |
| Status line | `role="status"`, row with gap 8, 12.5 px, opacity .7 (1 on error); fingerprint icon 16 px in fingerprint states |

The date-above-time order and the 118 px clock are the design. Stock
`unlockDialog.js` stacks time, then date, then a hint.

## States

### Greeter

| State | What shows | Source |
| --- | --- | --- |
| User list | Heading, list, "Not listed?", footer | `Main.dc.html:38-55` |
| Row hover / focus | See the list table | `Main.dc.html:19-20` |
| Prompt | Avatar, name, Back, field, sign-in button, hint "Press Enter to sign in", fingerprint pill | `Main.dc.html:57-79`, `:108` |
| Signing in | Hint changes to "Signing in…" (the prototype sets it from the arrow button only) | `Main.dc.html:108-110` |
| Back | Returns to the list and clears the busy flag | `Main.dc.html:109` |

Needed but not drawn:

*   Wrong password on the greeter. Use the lock screen's error treatment.
*   "Not listed?" opens the stock username entry (prompt with a "Username"
    field and no avatar). Not drawn.
*   Fingerprint states on the greeter (scanning, not recognised, too many
    tries). The pill is always visible in the artboard.
*   Spinner while verifying. Stock shows a spinner in the button well; the
    artboard swaps the hint text instead.
*   Caps Lock warning (stock "Caps lock is on.").
*   Session chooser (stock gear button) and the "show password" peek icon in
    the entry (stock; hide it with
    `org.gnome.desktop.lockdown disable-show-password` if unwanted).
*   Single-user systems: stock GDM shows the user list even with one user;
    the canvas does not say whether to skip to the prompt.
*   No users (first boot before initial setup), disabled user list
    (`org.gnome.login-screen disable-user-list`), banner message, smart card.
*   Power menu. Stock GDM offers Power Off, Restart and Suspend from the top
    bar; the artboard's icons are not interactive.
*   Multiple monitors: the prompt shows on the primary monitor only.

### Lock screen

| `state` tweak | Status line | Ring | Icon | Opacity |
| --- | --- | --- | --- | --- |
| `password` | "Press Enter to unlock" | `inset 0 0 0 1px rgba(255,255,255,.25)` | No | .7 |
| `wrong password` | "Wrong password. Try again." | `inset 0 0 0 2px #ffcfcf` light, `#ff8a8a` dark | No | 1 |
| `fingerprint` | "Or touch the fingerprint reader" | Normal | Yes | .7 |
| `fingerprint not recognized` | "Fingerprint not recognized. Try again." | Normal (no red ring) | Yes | 1 |

Source: `Lock.dc.html:60-74`. The `dark` tweak switches the wallpaper to the
dark one and the scrim to `.34`.

Needed but not drawn:

*   The stock lock screen first shows the clock alone with a hint ("Click or
    press a key to unlock") and notifications, then slides to the prompt and
    fades the clock. The artboard shows the clock and the prompt together,
    with no notifications and no hint. Confirm which the owner wants.
*   Cancel back to the clock view (stock cancel button). The artboard has no
    Back button on the lock.
*   "Switch User" (stock bottom-right button when other users exist).
*   Verifying spinner, Caps Lock warning, too many fingerprint tries, and the
    lock-out after repeated failures.
*   Media controls and notifications on the lock screen.

### Fingerprint conditions

The fingerprint hint, pill and icon must appear only when all of these hold:

1.  fprintd reports a reader (`net.reactivated.Fprint.Manager.GetDefaultDevice`).
2.  The selected user has at least one enrolled finger
    (`Device.ListEnrolledFingers(username)` returns a non-empty list).
3.  `org.gnome.login-screen enable-fingerprint-authentication` is true and
    the `gdm-fingerprint` PAM stack exists.

Stock `ShellUserVerifier` checks the reader and the setting. Verify whether
the installed version also checks enrolled fingers; if not, that check is a
small patch. On machines without a reader none of the fingerprint UI shows.

The copy "Or touch the fingerprint reader" assumes a press-type sensor.
fprintd reports the scan type (`press` or `swipe`); stock text differs per
type ("place finger" or "swipe finger"). Decide the swipe-type wording.

The ELAN reader on the reference laptop must be supported by the libfprint in
the image; some ELAN match-on-chip readers need a recent libfprint driver.
Confirm the USB ID.

### Old-spec text

"Built on Fedora Linux 45 · GNOME" (`Main.dc.html:86`) is hard-coded. The base
distribution is not confirmed and the version will change every release.
Treat the line as a placeholder. If it stays, generate it from
`/etc/os-release` at image build time, or read it at runtime (patch).

The dates in the two artboards (greeter "Sun Oct 11", lock "Wednesday
October 21") are sample data.

## Tokens used

| Group | Tokens and literals |
| --- | --- |
| Colour | `fixedScenes.greeterAndLock`: scrim `rgba(8,10,20,.68)` / `.34`, field `rgba(255,255,255,.18)`, field ring `rgba(255,255,255,.25)`, avatar ring `rgba(255,255,255,.35)`, row hover `rgba(255,255,255,.06)`, focus `inset 0 0 0 2px #fff`. Literals with no token: list card `rgba(255,255,255,.14)` and ring `.22`, row separator `.12`, Back fill `.12` and ring `.2`, submit fill `.22`, pill fill `.1`, lock avatar fill `.22`, footer text `.62`, error rings `#ffcfcf` (light lock) and `#ff8a8a` (dark lock), base colours `#0c1122` and `#0f1115` |
| Wallpaper | `--wall` light and dark images |
| Type | `typography.family.ui`; sizes `title-2` 22, `title-4` 18, `subtitle` 15, `small-plus` 12.5, `small` 12, `display-1` 118, and literals 13 (top bar, "Not listed?"), 14 (entry), 19 (name, list initial), 36 (big initial); weights 500, 600, 700, 800; tabular figures on the clock |
| Radius | `field` 19, `pill-bar` 12 (list card), `circle`, literals 15 (pill) and 3 (footer diamond) |
| Shadow | `shadow.focusRingOnWallpaper`; literals `0 10px 30px rgba(0,0,0,.18)` (list) and `.25` (avatar) |
| Glass | `glass` rows "Lock background" (30 px, 130 %) and "Lock password field" (20 px) |
| Motion | None in these artboards |

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Greeter blurred wallpaper and scrim | Theme | Pre-render one image (wallpaper, blur, saturation and scrim baked in) and set it as the `#lockDialogGroup` background in the Shell theme. The greeter wallpaper is fixed, so a live blur buys nothing |
| Lock blurred wallpaper | Stock, tuned by patch | `unlockDialog.js` already blurs the user's wallpaper with `Shell.BlurEffect`. Changing sigma and brightness is a constant change (patch). Saturation 130 % needs the patched `Shell.BlurEffect` ("patch 0003"). The blue-black tint needs an extra tint actor; stock brightness only darkens neutrally |
| Blur behind the list card and fields | Drop it | It blurs an already blurred background; the visual difference is near zero and it costs a `BACKGROUND`-mode blur per widget. Draw flat fills |
| Clock left in the greeter top bar | Patch | Stock `gdm` mode puts the date menu in the centre (`sessionMode.js`) |
| Lock top bar icons | Stock | Stock `unlock-dialog` panel shows the same indicators |
| "Choose a user" heading | Patch | Stock `LoginDialog` has no heading |
| User rows: account type line and chevron | Patch | Stock `UserListItem` shows avatar and name only |
| Initials in avatars | Patch | Stock Shell `Avatar` falls back to a generic person icon, not initials; users with a photo show the photo |
| "Not listed?" | Stock | Stock string and behaviour |
| Back button left of the field | Stock, themed | `AuthPrompt` cancel button |
| Round submit arrow right of the field | Patch | Recent `AuthPrompt` has no visible submit button; it shows a spinner well |
| Hints "Press Enter to sign in", "Press Enter to unlock", "Signing in…" | Patch | Stock message label is empty until PAM or an error sets it |
| Fingerprint pill (greeter) and icon line (lock) | Patch | Stock shows a text message only |
| "Wrong password. Try again." and "Fingerprint not recognized. Try again." | Patch | Stock messages come from PAM and Shell defaults; this replaces them |
| Red ring on the field | Theme | Style class on error, if `AuthPrompt` exposes one; otherwise a one-line patch |
| Lock clock: date above time, 118 px | Theme plus small patch | Sizes are CSS; the order is set in `unlockDialog.js` `Clock` |
| Clock and prompt visible together | Patch | Stock fades the clock when the prompt appears |
| Footer wordmark | Settings plus asset | `org.gnome.login-screen logo` with a PNG |
| Footer version line | Settings plus asset, or patch | Bake it into the logo PNG at image build time, or add a label (patch) |
| Guest account | Not stock | GDM has no guest session; drop the row or define the feature |

Overall cost: the greeter and lock are a theme plus a moderate patch set
against `loginDialog.js`, `authPrompt.js`, `unlockDialog.js` and
`userWidget.js`. Each GNOME release can move these files, so the patches need
an owner.

## Accessibility

*   Contrast, computed on the wallpaper base `#e8ebf0` under the .68 scrim:
    white at .7 (hints) is about 4.8:1 and passes AA; the footer line at .62
    is about 4.2:1 and fails AA for 12 px text. Over the lightest wallpaper
    areas (near white) .7 drops to about 4.4:1. Raise the footer to at least
    .72 and the hints to .75, or verify against the real pre-blurred image.
*   Dark lock (.34 scrim on the dark wallpaper) is about 9.6:1 for hints.
*   Focus order, greeter list: rows in order, then "Not listed?". Prompt:
    field (initial focus), sign-in button, Back. Escape acts as Back.
*   Focus styles: rows have a 2 px white inner ring. The Back, sign-in and
    unlock buttons and the field have none in the artboards; give them the
    same 2 px white ring.
*   Screen reader names: "Back to user list", "Sign in", "Unlock" and
    "Password" as in the artboards; rows read name and account type. The
    lock status line is a live region (`role="status"`); the greeter hint is
    not, and should be.
*   The top-bar icons need their stock accessible names and menus.
*   Large text (`text-scaling-factor` 1.25 and above): fields grow in height
    and the list rows grow; the 118 px clock may scale too; check it does not
    collide with the prompt at 900 px tall.
*   Reduced motion: none drawn. Respect `enable-animations` for the stock
    clock-to-prompt transition.

## Acceptance criteria

1.  With two users, the greeter shows the heading "Choose a user" with its
    top at 286 px, and the list card 380 px wide and 124 px tall, 18 px below
    the heading's line box (about 331 px from the top with Inter's normal
    line height).
2.  Each user row is 62 px tall with a 48 px avatar; a separator appears
    between rows and not above the first.
3.  Hovering a row fills it with white at .06; Tab focus draws a 2 px white
    inner ring.
4.  Choosing a user shows a 92 px avatar, the name at 19 px bold, and a 250 x
    38 px field with a 38 px button on each side, gaps 8 px, centred.
5.  The greeter footer shows the wordmark 44 px above the bottom edge and the
    version line under it. The version line matches the running image's
    `/etc/os-release`, not a fixed string.
6.  The greeter background is static: no `Shell.BlurEffect` actor is created
    for it (check with Looking Glass).
7.  On a machine with no fingerprint reader, no fingerprint pill, icon or
    text appears on the greeter or the lock screen.
8.  With a reader but no enrolled finger for the user, no fingerprint UI
    appears for that user.
9.  With an enrolled finger, the greeter shows the pill and a matching touch
    signs in; the lock shows the icon line and a matching touch unlocks.
10. A wrong password on the lock screen shows "Wrong password. Try again." at
    full opacity and a 2 px ring (`#ffcfcf` light, `#ff8a8a` dark); the next
    key press restores the normal state.
11. An unrecognised finger shows "Fingerprint not recognized. Try again."
    with the fingerprint icon and no red ring.
12. The lock clock is 118 px logical (236 device px), weight 700, tabular
    figures, with the date 22 px above it, block top at 128 px.
13. Switching the lock to dark style uses the dark wallpaper and the .34
    scrim.
14. The lock background blur equals CSS blur 30 px: `Shell.BlurEffect` radius
    120 device px at scale 2 (sigma 60).
15. Keyboard only: a user can pick a user, type the password and sign in
    without a pointer; Escape returns to the list.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

| ID | Question | Blocks |
| --- | --- | --- |
| GL-1 | Lock flow: clock and prompt together as drawn, or stock clock-first with notifications? | `unlockDialog.js` patch scope |
| GL-2 | Footer line "Built on Fedora Linux 45 · GNOME": keep, and generated from what? The base distribution is unconfirmed. | Footer |
| GL-3 | Guest account: is it a feature? GDM has none. | User list |
| GL-4 | Power menu, session chooser and accessibility menu on the greeter are not drawn. | Top bar |
| GL-5 | Greeter error, "Not listed?" username entry, single-user and no-user states are not drawn. | Greeter states |
| GL-6 | Error ring colours differ: `#ffcfcf` (light lock), `#ff8a8a` (dark lock, disk unlock). One value or two? | Theme |
| GL-7 | Swipe-type fingerprint wording; ELAN reader USB ID and libfprint support. | Copy, hardware |
| GL-8 | Avatar fill differs: none on the greeter, white .22 on the lock. Intended? | Theme |
| GL-9 | Saturation in the lock blur needs the patched `Shell.BlurEffect`; drop it if that patch is not taken. | Patch list |
