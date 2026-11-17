# Authentication and Power Off dialogs

## Summary

Two GNOME Shell system-modal dialogs drawn over the desktop:

*   **Authentication Required**: the polkit prompt. The artboard shows it
    asking for an administrator password to boot the previous Apex version,
    after a rollback request (drawn as `apexctl update rollback` in a
    terminal; `apexctl` is cut, so the real trigger is "Use at Next
    Restart…" in Software Updates or `sudo bootc rollback`).
*   **Power Off**: the end-session dialog with a countdown, a switch that
    decides whether the next boot starts the staged update, and Cancel,
    Restart and Power Off buttons.

| No. | Artboard | Title | Tweaks | Interactive states |
| --- | --- | --- | --- | --- |
| 13 | `Polkit.dc.html` | Authentication dialog | `state`: `password` (default), `wrong password`; `dark`: false; `accent`: nine colours, default `#3584e4` | Details disclosure, open by default |
| 14 | `EndSession.dc.html` | Power off dialog | `dark`: false; `accent`: nine colours, default `#3584e4` | Countdown from 54; switch toggles the Restart label |

In `EndSession.dc.html` the `dark` tweak declares default false (line 83),
but `renderVals()` uses `this.props.dark ?? true` (line 101), so the
artboard renders dark when the prop is absent. Both themes must be built.

Both use the `.apx-l` / `.apx-d` colour roles. Both artboards set `--dim`
light to `rgba(29,29,33,.72)`, not the majority `.62`
(`Polkit.dc.html:20`, `EndSession.dc.html:18`; listed as a conflict in
`tokens.json`).

## Upstream mapping

| Element | Upstream | Confidence |
| --- | --- | --- |
| Authentication dialog | GNOME Shell `js/ui/components/polkitAgent.js` (`AuthenticationDialog`, `AuthenticationAgent`), on `PolkitAgent.Session` | High |
| Power Off dialog | GNOME Shell `js/ui/endSessionDialog.js` (`EndSessionDialog`, dialog type `shutdown`) | High |
| Dialog frame, scrim, buttons | `js/ui/modalDialog.js` (`ModalDialog`, `Lightbox`) and `js/ui/dialog.js` (`Dialog`, `MessageDialogContent`) | High |
| User row in the polkit dialog | `js/ui/userWidget.js` (`UserWidget`, `Avatar`) | High |
| Styles | `data/theme/gnome-shell-sass/widgets/_dialogs.scss`, `_end-session-dialog.scss` | High |
| Update switch backend | Stock binds a checkbox to PackageKit offline updates (`org.freedesktop.PackageKit.Offline`). It must bind to the bootc staged deployment instead (stock `bootc`, decided 2026-11-17, OQ-04) | High |

## Layout and measurements

All values are logical px on the 1440x900 artboard; device px are twice
these.

### Shared frame

| Element | Authentication | Power Off | Source |
| --- | --- | --- | --- |
| Scrim | `--dialog-scrim` (`rgba(0,0,0,.32)`) over the whole screen, top bar and dock included | Same | `Polkit.dc.html:85`, `EndSession.dc.html:57` |
| Dialog position | Centred on screen | Centred | `:87`, `:59` |
| Width | 440 | 460 | same |
| Height | Content height | Content height | |
| Padding | 28 28 22 | 28 28 22 | |
| Radius | 26 (`panel`) | 26 | |
| Fill | `--panel-solid` | `--panel-solid` | |
| Shadow | `shadow.panel` (`--shadow`, inset 1 px `--panel-border`) | Same | |
| Column gap | 18 | 20 | |
| Icon disc | 56 x 56, radius 28, fill accent at 16 % (`color-mix(in srgb, var(--accent) 16%, transparent)`), glyph `--accent` | 56 x 56, radius 28, fill `--btn`, glyph `--fg` | `:88-90`, `:60-62` |
| Glyph | Shield with keyhole, 28 px, stroke 1.5 | Power, 26 px, stroke 1.5 | |
| Title | 20 px (`title-3`) / 700, letter-spacing -0.2 px, centred | Same | `:92`, `:64` |
| Title to body gap | 6 | 6 | |
| Body | 13.5 px (`ui`), line-height 1.45, `--dim`, centred, `text-wrap: pretty` | 13.5 px, line-height 1.45, `--dim`, tabular figures | `:93`, `:65` |
| Button row | Gap 10, buttons 36 tall, radius 18, 13 px (`body`) / 600 | Same | `:123-126`, `:75-79` |

### Authentication dialog body

`Polkit.dc.html:95-122`.

| Element | Value |
| --- | --- |
| Auth block | Column, gap 10, full width |
| User row | Padding 0 4, gap 10 |
| User avatar | 32 x 32 circle, fill accent mixed with 25 % black (`color-mix(in srgb, #000 25%, var(--accent))`), initial "A" 14 px / 700 `#fff` |
| User name | "Apex", 13.5 px / 600 |
| User role | "Administrator", 11.5 px (`caption`), `--dim` |
| Password field | Height 38, radius 19 (`field`), fill `--btn`, ring `inset 0 0 0 2px` accent (error: `--err`), padding 0 16, gap 10 |
| Entry text | 14 px / 500, caret `--accent`; placeholder "Password" at `--fg` opacity .55 |
| Status line | Padding 0 6, gap 8, 12.5 px (`small-plus`), `--dim` (error: `--err`); fingerprint icon 16 px when not in error |
| Details box | Full width, radius 12, ring `inset 0 0 0 1px var(--border)`, clips |
| Details button | Full width, 38 tall, padding 0 12, gap 8, 12.5 px / 600, `--dim`; chevron 14 px, rotated 90 deg when open, `transform .15s ease` |
| Details content | Grid `76px minmax(0,1fr)`, row gap 6, padding 0 12 12 34, 12 px (`small`); labels `--dim` |
| Details rows | "Action" `io.github.apex_linux.Updates.rollback` (the artboard draws `io.github.apex-linux.apex.update.rollback`; replaced per OQ-04 and OQ-08) in JetBrains Mono 11.5 px, wraps anywhere; "Vendor" "Apex" |
| Buttons | "Cancel" (flex 1, fill `--btn`) and "Authenticate" (flex 1, fill accent mixed with 25 % black, text `#fff`); each 187 px wide |

The field ring is always 2 px accent in the artboard: it shows the focused
state, which is correct because the field takes focus when the dialog opens.
An unfocused field is not drawn; use the same fill with no ring.

### Power Off dialog body

`EndSession.dc.html:63-79`.

| Element | Value |
| --- | --- |
| Body copy | "The system will power off automatically in {seconds} seconds." |
| Update card | Full width, padding 12 14, radius 12 (`pill-bar`), fill `--card`, shadow `shadow.card`, gap 12 |
| Card icon | Software app icon (`91d271bbd5c894bdd2ed6a39ef85e177.svg`), 36 x 36, decorative (`alt=""`) |
| Card text | Column, gap 2: "Start the new version next time" 13.5 px / 600; version line 12 px (`small`), `--dim`, line-height 1.35 |
| Version line | "45.20261010.133 · GNOME 51.1, Linux 7.2.9, Mesa 26.1.2" |
| Switch track | 40 x 22, radius 11, on: accent, off: `--btn-h`; `background .2s cubic-bezier(.2,.8,.2,1)` |
| Switch knob | 18 x 18, radius 9, `#fff`, `shadow.knob`, top 2, left 2 (off) or 20 (on), `left .2s cubic-bezier(.2,.8,.2,1)` |
| Buttons | "Cancel" flex 1 (about 107 px), Restart flex 1.4 (about 149 px), "Power Off" flex 1.2 (128 px) |
| Button fills | Cancel and Restart `--btn`; Power Off `--destructive` (`#c01c28`) with `#fff` text in both themes |

Style objects: `track` and `knob` at `EndSession.dc.html:107-108`.

### Background scene (context only)

The artboards draw the top bar and dock as in `shell-top-bar-and-dock.md`.
Behind the polkit dialog is a terminal window 860 x 560 at (250, 96) running
`apexctl status` and `apexctl update rollback`, ending "Waiting for
authorization…" (`Polkit.dc.html:45-69`). None of it is part of this spec.
It contains old-spec text: the host "apex@fedora" and versions
"45.20261008.131" and "45.20261001.124".

## States

### Authentication dialog

| State | Ring | Status line | Source |
| --- | --- | --- | --- |
| `password` | 2 px accent | Fingerprint icon + "Or touch the fingerprint reader", `--dim` | `Polkit.dc.html:141-144` |
| `wrong password` | 2 px `--err` | "Sorry, that didn’t work. Please try again.", `--err`, no icon | same |
| Details open (default) | | Action and Vendor rows visible, chevron rotated 90 deg | `:134`, `:146-148` |
| Details closed | | Only the "Details" row | |

"Sorry, that didn’t work. Please try again." is the stock `polkitAgent.js`
string, with a typographic apostrophe.

Needed but not drawn:

*   Authenticating: stock shows a spinner and makes the entry insensitive
    while PAM runs.
*   Several administrators: stock shows the first admin; there is no chooser.
    Decide whether to show one.
*   Caps Lock warning, and the "show password" peek icon in the entry.
*   PAM messages other than wrong password (account expired, lock-out).
*   No fingerprint reader, or no enrolled finger: the fingerprint line must
    be absent (same conditions as in `greeter-and-lock.md`).
*   Fingerprint not recognised, too many tries.
*   Dialog for an action with no description, or a long description.

### Fingerprint in polkit is expensive

The greeter and lock run password and fingerprint as two parallel PAM
conversations. Polkit runs one PAM stack (`polkit-1`). With `pam_fprintd` in
that stack (Fedora `authselect ... with-fingerprint`), PAM asks for the finger
first and falls back to the password only after the fingerprint times out
or fails. The artboard draws both at once ("Or touch the fingerprint
reader" under a live password field). Getting that needs either a custom PAM
arrangement or an agent change that runs two sessions; both are non-trivial
and need security review. The cheap option is stock sequential behaviour,
showing the PAM prompt text.

### Power Off dialog

| State | What shows | Source |
| --- | --- | --- |
| Switch on (default) | Track accent, knob at 20; middle button "Restart & Update" | `EndSession.dc.html:87`, `:105` |
| Switch off | Track `--btn-h`, knob at 2; middle button "Restart" | same |
| Countdown | Body updates every second | `:89-93` |

The prototype starts at 54 and wraps from 1 back to 60 so it never ends.
A real build uses the stock 60 s countdown and, at 0, runs the default
action, Power Off. The copy needs plural forms
("…in 1 second.", "…in 2 seconds."), as stock already has with `ngettext`.

Switch semantics, settled by OQ-04 (2026-11-17, stock `bootc` only; details
in [updates-and-rollback.md](updates-and-rollback.md#cross-linked-surfaces)):

| Switch | Power Off | Restart |
| --- | --- | --- |
| On | Runs `bootc upgrade --from-downloaded` through the Apex helper, then powers off; the next boot starts the new version | Same, then restarts into the new version |
| Off | Powers off; the next boot starts the current version; bootc discards the download-only update and the next check stages it again from cache | Restarts into the current version, same discard |

The card and switch show only for a download-only update
(`staged.downloadOnly` true in `bootc status`). A plain staged update
applies at any shutdown, so the dialog shows no switch and the middle button
reads "Restart & Update". The verified bootc behaviour and sources are in
the update spec.

Without a staged version the dialog is the stock three-button Power Off.

The version line must come from the staged deployment's `version` in
`bootc status`. bootc provides no package diff, so the drawn "GNOME 51.1,
Linux 7.2.9, Mesa 26.1.2" is cut until OQ-37 decides a source; the line reads
"Apex <version>". The format "45.20261010.133" follows the
Fedora-major.date.serial scheme and is old-spec text; it is hard-coded in the
artboard and in `Updates.dc.html:119`.

Needed but not drawn:

*   Low battery with an update pending (stock: "Running on battery power:
    Please plug in before installing updates."). The artboard's top bar
    battery icon is nearly empty (`EndSession.dc.html:38`, fill 1 px wide).
*   Applications inhibiting shutdown ("Some applications are busy or have
    unsaved work") with the app list.
*   Other users signed in, with the list of sessions.
*   The separate Restart and Log Out dialogs.

## Tokens used

| Group | Tokens and literals |
| --- | --- |
| Colour | `--panel-solid`, `--panel-border`, `--fg`, `--dim` (artboard value .72 light), `--border`, `--btn`, `--btn-h`, `--card`, `--card-border`, `--err` (light `#c01c28`, dark `#ff7b63`), `--accent`, `--accent-tint` (icon disc), `--accent-strong` (avatar, Authenticate), `--dialog-scrim`, `--destructive` (Power Off fill); literal `#fff` (knob, text on filled buttons) |
| Type | `typography.family.ui`, `typography.family.mono` (Action id); sizes `title-3` 20, `ui` 13.5, `body` 13, `small-plus` 12.5, `small` 12, `caption` 11.5, literal 14 (entry); weights 500, 600, 700; tabular figures on the countdown |
| Radius | `panel` 26, `field` 19, `pill-bar` 12, `circle`; literals 18 (36 px buttons), 28 (icon disc), 11 and 9 (switch) |
| Shadow | `shadow.panel`, `shadow.card`, `shadow.knob` |
| Glass | None; both dialogs are opaque |
| Motion | `motion.duration.fast` with `motion.easing.ease` (chevron); `motion.duration.base` with `motion.easing.standard` (switch) |

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Scrim, frame, radius, padding, fills | Theme | `_dialogs.scss`, lightbox opacity |
| Pill buttons, red Power Off | Theme | Button style classes; Power Off as destructive |
| Icon disc above the title | Patch | Stock dialogs since GNOME 3.36 have no icon; add an `St.Icon` in each dialog |
| Title, body, countdown | Stock | Stock strings and countdown |
| Horizontal user row with 32 px avatar | Patch | Stock `UserWidget` is vertical in the polkit dialog; the orientation is a constructor argument, so the change is small |
| "Administrator" role line | Patch | Not in stock `UserWidget` |
| Initial on accent avatar | Patch | Stock falls back to a person icon |
| Accent focus ring, error ring | Theme | Entry focus style; error style class |
| Fingerprint line alongside the password | Patch, expensive | See "Fingerprint in polkit is expensive" |
| Details disclosure | Patch | Stock dialog has no Details. Action id comes from the polkit request; Vendor needs a lookup through `Polkit.Authority` action descriptions. Default open, as drawn, shows an internal id to every user; consider closed by default |
| Update card and switch | Patch | Stock shows a checkbox "Install pending software updates" bound to PackageKit; replace with a switch bound to the staged deployment |
| "Restart & Update" label | Patch | Stock label is "Restart" |
| Version line | Patch plus backend | Needs the cached staged-version summary |

## Accessibility

*   Contrast: `--dim` (.72) on `--panel-solid` is about 6.4:1 light and 6.3:1
    dark. `--err` is about 5.7:1 light and 5.6:1 dark. White on the Power Off
    red is about 6.1:1. White on accent mixed with 25 % black is 5.0:1
    (yellow) to 8.8:1 (purple), so every accent passes for 13 px bold text.
*   Non-text contrast of the 2 px accent focus ring against the field (3:1
    needed): yellow in light (about 2.8:1) and purple in dark (about 2.4:1)
    fail. Raise the ring for those accents or add a darker or lighter outer
    edge.
*   Authentication focus order: field (initial), Details, Cancel,
    Authenticate. Enter authenticates; Escape cancels.
*   Power Off focus order: switch, Cancel, Restart, Power Off. Initial focus
    on Cancel or Power Off, per stock (confirm). Escape cancels. Space toggles
    the switch.
*   Screen reader: dialogs are labelled by their title (`aria-labelledby` in
    the artboards). The Details button reports expanded or collapsed. The
    switch has role switch and the label "Start the new version next time".
    The countdown must not be announced every second; announce it once when
    the dialog opens.
*   Reduced motion: with animations off, the switch and chevron change
    without transition.
*   Large text: the dialogs grow in height; the 36 px button row must not
    truncate "Restart & Update" at 1.25x text scale (149 px wide at 1x).

## Acceptance criteria

1.  Running `pkexec true` as an administrator shows a 440 px wide dialog
    with 26 px radius, centred, over a full-screen scrim of black at .32.
2.  The dialog shows the shield icon in a 56 px accent-tinted disc, the
    title "Authentication Required" at 20 px bold, and the action's message.
3.  The user row shows the administrator's avatar at 32 px, name and
    "Administrator".
4.  The password field is 38 px tall, focused on open, with a 2 px accent
    ring.
5.  A wrong password turns the ring and the status line `--err` and shows
    "Sorry, that didn’t work. Please try again."
6.  On a machine without a fingerprint reader, or for a user with no
    enrolled finger, no fingerprint line appears.
7.  Clicking Details toggles the Action and Vendor rows; the chevron
    rotates 90 deg in 150 ms; the Action row shows the requested action id.
8.  Changing the accent in Settings changes the icon disc, the ring, the
    avatar and the Authenticate button without a restart.
9.  Choosing Power Off with no staged update shows the stock three buttons
    and no update card.
10. With a download-only update, the card shows "Start the new version next
    time" and "Apex <version>" from `bootc status`, within 100 ms of opening
    the dialog.
11. The switch is on by default; turning it off changes the middle button
    from "Restart & Update" to "Restart" and moves the knob from 20 px to
    2 px in 200 ms.
12. With the switch off, Restart boots the current version; afterwards
    `bootc status` shows no staged deployment, and Software Updates offers
    the same version again without a full download.
13. The countdown starts at 60, decreases by one each second with correct
    plural forms, and at 0 powers off.
14. On battery with an update pending, the low-battery warning appears.
15. Both dialogs render correctly in light and dark styles with all nine
    accents.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

| ID | Question | Blocks |
| --- | --- | --- |
| DLG-1 | Answered 2026-11-17 (OQ-04): stock bootc; "do not start the new version" is bootc's download-only staging, discarded at boot. | Update switch |
| DLG-2 | Polkit fingerprint: accept stock sequential behaviour, or fund parallel password and fingerprint? | Auth dialog scope |
| DLG-3 | Version line format: the source is the image's `version` in `bootc status`; the scheme is OQ-08. | Card copy |
| DLG-4 | Details disclosure open or closed by default; is it shown at all to non-technical users? | Auth dialog |
| DLG-5 | Low battery, inhibitors, other users, Restart and Log Out dialogs are not drawn. | End-session states |
| DLG-6 | Column gap differs: 18 (polkit) and 20 (Power Off). Intended? | Theme |
| DLG-7 | Answered 2026-11-17: `--destructive` (`#c01c28`, both themes) is in `tokens.json` under `color.status`. | Tokens |
