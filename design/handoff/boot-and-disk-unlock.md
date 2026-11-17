# Boot splash and disk unlock

## Summary

The boot splash is the black screen with the Apex wordmark and a thin
progress bar that shows from early boot until the greeter appears. The disk
unlock screen is the same scene with the progress bar replaced by a
passphrase field. It appears when the root volume is LUKS-encrypted and needs
a passphrase.

| No. | Artboard | Title | Tweaks |
| --- | --- | --- | --- |
| 01 | `Boot.dc.html` | Boot splash | `progress`: 0 to 100 %, default 58 |
| 30 | `BootUnlock.dc.html` | Disk unlock | `state`: `passphrase` (default), `wrong passphrase` |

Both artboards are fixed scenes: they do not use the `.apx-l` / `.apx-d`
colour roles, have no dark or accent tweak, and take their values from
`fixedScenes.boot` and `fixedScenes.diskUnlock` in `tokens.json`.

## Upstream mapping

| Element | Upstream | Confidence |
| --- | --- | --- |
| Whole scene | Plymouth theme in `/usr/share/plymouth/themes/apex/`, set with `plymouth-set-default-theme apex` and rebuilt into the initramfs | High |
| Theme engine | Plymouth **script** plugin (`ModuleName=script`, `ScriptFile=apex.script`) | High |
| Passphrase request | `systemd-cryptsetup` asks through `systemd-ask-password`; the `systemd-ask-password-plymouth` agent forwards it to Plymouth, which calls the theme's display-password callback | High |
| Progress value | Plymouth boot progress (`Plymouth.SetBootProgressFunction`), estimated from the previous boot's duration in `/var/lib/plymouth/` | High |

### Why script and not two-step

Fedora's default themes (`bgrt`, `spinner`) use the **two-step** plugin. Two-step
can draw a centred logo and a progress bar, but its password prompt is a fixed
layout: the prompt text from systemd as a label, an entry image and bullet
images. It has no placeholder text inside the entry, no custom hint line under
it, and no error state. The artboard's copy ("Enter Passphrase" inside the
field, "Press Enter to unlock the disk" below it, a red ring on failure) needs
`Plymouth.SetDisplayPasswordFunction(fun (prompt, bullets))`, which only the
script plugin offers. The Files artboard also lists an `apex-plymouth` project
with `apex.plymouth`, `apex.script` and `logo@2x.png`
(`Files.dc.html:257`), which agrees.

Confidence that script is required: high. Confidence in the exact script API
names: medium; check them against the Plymouth version in the base image.

### Device pixels and scale

Plymouth draws into the DRM framebuffer at device pixels. On the reference
panel (2880x1800 at scale 2) every logical measurement below doubles. Plymouth
picks an integer device scale itself (from panel DPI, or `DeviceScale=` in
`plymouthd.conf`); it has no fractional scale. The theme must:

*   Read the screen size with `Window.GetWidth()` / `Window.GetHeight()` and
    derive the scale. Check on the target Plymouth whether the script API
    exposes the device scale directly; if not, compute it the way Plymouth
    does (scale 2 above roughly 192 DPI, else 1).
*   Load raster assets for that scale (`@1x`, `@2x`; add `@3x` if a 3x panel
    must be supported).
*   Position everything relative to the screen centre, not at the artboard's
    absolute y values, so other resolutions and aspect ratios work.

## Layout and measurements

All values are logical px on the 1440x900 artboard. "Device px" is at scale 2.

### Scene

| Property | Value | Source |
| --- | --- | --- |
| Background | `#000` | `Boot.dc.html:18` |
| Foreground | `#fff` | `Boot.dc.html:18` |
| Font | Inter, features `cv05`, `ss03`, grayscale antialiasing | `Boot.dc.html:18` |

### Wordmark (both artboards)

A horizontal row, centred, 41 px tall, top 408 (centre y 428.5, which is
21.5 px above screen centre). `Boot.dc.html:19-22`, `BootUnlock.dc.html:21-24`.

| Part | Logical | Device px | Notes |
| --- | --- | --- | --- |
| Diamond box | 26 x 26, `border: 3px solid #fff`, radius 5, rotated 45 deg | 52 x 52, 6 stroke, radius 10 | Box-sizing is border-box. Rotated, the visual diagonal is about 36.8 px, so it overhangs its layout box by about 5.4 px on each side |
| Gap | 18 | 36 | Layout gap between the unrotated box and the text |
| "Apex" | 34 px, weight 800, letter-spacing -0.5 px | 68 px, -1 px | Token size `display-2`, weight `heavy` |

Build the wordmark as one pre-rendered PNG per scale (diamond plus text), not
as live text. That keeps Inter out of the initramfs for this element and makes
the result pixel-exact. Centre the PNG's bounding box at screen centre x and
at y = centre - 21.5 logical.

### Progress bar (boot, and disk unlock after Enter)

Top 489 (39 px below screen centre), horizontally centred.
`Boot.dc.html:23-26`, `BootUnlock.dc.html:37-41`.

| Part | Logical | Device px |
| --- | --- | --- |
| Track | 160 x 3, radius 2, `rgba(255,255,255,.14)` | 320 x 6, radius 4 |
| Fill | width = 160 x progress / 100, full height, radius 2, `#fff` | 320 x progress / 100 |

Horizontal extent at 1440 wide: x 640 to 800.

### Passphrase field (disk unlock, asking)

A column, centred, top 489, gap 14. `BootUnlock.dc.html:27-33`, style object
`fieldStyle` at `BootUnlock.dc.html:84`.

| Part | Value |
| --- | --- |
| Field | 250 x 38 (device 500 x 76), radius 19 (`field` token), fill `rgba(255,255,255,.18)`, padding 0 16 |
| Field ring, normal | `inset 0 0 0 1px rgba(255,255,255,.25)` |
| Field ring, error | `inset 0 0 0 2px #ff8a8a` |
| Entry text | 14 px, weight 500 (`medium`), `#fff`, caret `#fff` |
| Placeholder | "Enter Passphrase", `#fff` at opacity .62 (`BootUnlock.dc.html:16`) |
| Gap to hint | 14 |
| Hint | 12.5 px (`small-plus`), weight inherited (400), `#fff` at opacity .7 normal, 1 on error |

Horizontal extent of the field at 1440 wide: x 595 to 845. Hint top is
489 + 38 + 14 = 541.

The artboard uses a browser password input, so it does not specify the
bullets. Plymouth passes a bullet count, and the theme draws them. Proposed,
pending owner: a white dot 6 px (device 12) with 4 px gaps, left-aligned
at the 16 px padding, clipped at the right padding. Hide the placeholder
when the count is above 0.

Draw the field as pre-rendered PNGs per scale (normal and error ring),
because the script plugin cannot draw rounded rectangles.

## States

### Modelled by the artboards

| State | Trigger | What shows |
| --- | --- | --- |
| Booting | Plymouth boot progress | Wordmark and progress bar at `progress` % (artboard default 58) |
| Asking | Display-password callback | Wordmark, empty field with placeholder, hint "Press Enter to unlock the disk" at .7 |
| Typing | Key press | Bullets replace the placeholder (browser dots in the artboard) |
| Wrong passphrase | Tweak `wrong passphrase` | 2 px `#ff8a8a` ring, hint "Wrong passphrase. Try again." at opacity 1 |
| Unlocking | Enter with a non-empty value | Field and hint are removed, the progress bar returns at the same top (489) |

The artboard's unlock animation starts at 6 % and adds 1.6 % every 50 ms
(about 2.95 s to 100 %), then waits 1.2 s and resets to asking
(`BootUnlock.dc.html:59-71`). That loop is a prototype device. A real build
continues from Plymouth's actual progress value.

Enter with an empty field does nothing (`BootUnlock.dc.html:81`). Keep that:
do not send an empty passphrase to systemd.

### Wrong passphrase in a real build

systemd does not tell Plymouth that the previous passphrase was wrong; it
asks again. The theme must infer the error: when a new password request
arrives for the same prompt text after an answered one, show the error state.
Clear the bullets on each new request. After the configured number of tries
(systemd-cryptsetup default 3) boot fails to the emergency target, which the
canvas does not draw.

### Needed but not drawn

| State | Notes |
| --- | --- |
| Firmware logo hand-off | Fedora's default `bgrt` theme keeps the ASUS firmware logo; this design replaces it with black. Expect a visible cut from the logo to black when Plymouth starts |
| Bootloader | No GRUB or systemd-boot screen is drawn. On an image-based system the menu lists deployments (current, rollback) and must be reachable (hold Shift or Esc) |
| Booting previous version | Stock `bootc` has no automatic fallback (OQ-04, 2026-11-17). After a failed boot the user picks the previous entry in the GRUB menu; the menu must then appear without a key held (legacy decision 17, to verify, OQ-36). The session then shows "You Started the Previous Version" (see [updates-and-rollback.md](updates-and-rollback.md)); the splash needs no message |
| Messages | `Plymouth.SetMessageFunction` (fsck, SELinux relabel, `plymouth display-message`) has no style |
| Multiple encrypted volumes | The artboard hides systemd's prompt text, which names the disk. With two volumes the user cannot tell which one is asked for |
| Caps Lock on | No indicator |
| Keyboard layout | The initramfs uses the console keymap (`vconsole.conf`), which can differ from the GNOME layout. No indicator |
| TPM2 or FIDO2 unlock | With `systemd-cryptenroll` the prompt may never appear, or may ask for a PIN or a key touch. Strings not drawn |
| Tries exhausted, emergency shell | Not drawn |
| Shutdown and reboot | Plymouth also runs in `shutdown` and `reboot` modes; the canvas does not say whether the splash shows there, or with or without the bar |
| Firmware update mode | `fwupd` capsule updates show Plymouth `firmware-upgrade` mode with a status message; not drawn |
| No KMS | Without a DRM device Plymouth falls back to its text plugin; the prompt then looks stock |
| Hand-off to GDM | Black to greeter transition not specified. GDM deactivates Plymouth and takes over the framebuffer |
| Other scales | Only scale 2 at 1440x900 logical is drawn |

## Tokens used

| Group | Tokens and literals |
| --- | --- |
| Colour | `fixedScenes.boot.background` `#000`, `fixedScenes.boot.foreground` `#fff`; literals `rgba(255,255,255,.14)` (track), `rgba(255,255,255,.18)` (field), `rgba(255,255,255,.25)` (ring), `#ff8a8a` (error ring), placeholder opacity .62, hint opacity .7 / 1 |
| Type | Family `typography.family.ui`; sizes `display-2` 34 px, `small-plus` 12.5 px, literal 14 px (entry); weights `heavy` 800, `medium` 500 |
| Radius | `hairline` 2 px (bar), `field` 19 px; literal 5 px (diamond) |
| Shadow | None |
| Glass | None |
| Motion | None specified. The prototype's 50 ms progress tick is not a token |

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Black background, wordmark PNG, progress bar | Theme | Plymouth theme assets and script; no Plymouth code change |
| Passphrase field, placeholder, hint, bullets | Theme | Script theme; two-step cannot do it (see above) |
| Wrong-passphrase detection | Theme | Script logic infers it from repeated requests; fragile, test it |
| Scale handling | Theme | Script logic plus per-scale assets |
| Hint and placeholder text rendering | Theme, with packaging work | `Image.Text` needs a font in the initramfs; to use Inter it must be installed and pulled in by `plymouth-populate-initrd` / dracut |
| Translations of the two strings | Patch-like cost | The script theme has no gettext. Either ship one string table per locale in the script, or pre-render text images per locale |
| Firmware logo replacement | Theme | Choosing a non-BGRT theme is a setting; the cut is a side effect |

## Accessibility

*   Contrast on black: hint at .7 is about 10:1; placeholder at .62 on the
    field fill is about 6.2:1; the white fill of the progress bar is 21:1.
    The .14 track is about 1.35:1. That is acceptable only because the track
    is decorative and the fill carries the value.
*   Keyboard: typing goes to the field without focus handling; Enter submits;
    Backspace removes one bullet. Keep Plymouth's stock Esc behaviour (toggle
    to the text details view) so a user can read boot messages.
*   Screen reader: none exists in the initramfs. The artboard's `role="status"`
    and `aria-label="Disk passphrase"` have no Plymouth equivalent. Note it as
    a known limit.
*   Reduced motion and large text: not applicable; the only motion is the bar.

## Acceptance criteria

1.  On a 2880x1800 panel at scale 2, a screenshot of the splash matches
    `Boot.dc.html` at `progress` 58 within 1 device px for every edge.
2.  The diamond measures 52 x 52 device px before rotation with a 6 device
    px stroke; the gap to the text box is 36 device px.
3.  The progress track is 320 x 6 device px, centred horizontally, with its
    top 78 device px below the screen's vertical centre.
4.  On a 1920x1080 panel at scale 1, all elements are 1x size and keep the
    same offsets from screen centre (wordmark centre 21.5 px above, bar top
    39 px below).
5.  With a LUKS root and no TPM enrolment, the boot stops at the passphrase
    field: 500 x 76 device px, radius 38, placeholder "Enter Passphrase",
    hint "Press Enter to unlock the disk".
6.  The progress bar is not visible while the field is shown.
7.  Typing shows one bullet per character and hides the placeholder;
    Backspace removes one bullet.
8.  Pressing Enter with no characters typed sends nothing and keeps the
    prompt.
9.  Entering a wrong passphrase shows the 2 px `#ff8a8a` ring, the hint
    "Wrong passphrase. Try again." at full opacity, and an empty field.
10. Entering the right passphrase removes the field and hint and shows the
    progress bar at the same position, continuing from Plymouth's progress.
11. The progress fill does not advance while the passphrase prompt is shown.
12. Pressing Esc during boot switches to the text details view and back.
13. `lsinitrd` lists the Apex theme files and the font the hint uses.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

| ID | Question | Blocks |
| --- | --- | --- |
| BOOT-1 | Which other scales and resolutions must Plymouth support (1x, 2x, 3x; portrait panels)? The canvas draws only 2x. | Asset list |
| BOOT-2 | Disk name: hide systemd's prompt text as drawn, or show the volume name when more than one volume asks? | Prompt copy |
| BOOT-3 | NVIDIA hybrid graphics: which GPU drives the internal panel on the M7400QC, and is `amdgpu` in the initramfs for early KMS? Without it Plymouth starts on `simpledrm` and the screen flickers and changes mode when `amdgpu` loads. Keep the NVIDIA driver out of the initramfs unless it drives a panel at boot. | Initramfs contents |
| BOOT-4 | Firmware and bootloader screens: keep the ASUS logo (BGRT) or cut to black; is the boot menu hidden; how does a user pick the rollback deployment? | Boot flow |
| BOOT-5 | "Booting previous version", emergency and tries-exhausted states are not drawn. | Rollback UX |
| BOOT-6 | Bullet style and Caps Lock and keyboard-layout indicators are not drawn. | Field detail |
| BOOT-7 | Localisation of the hint and placeholder inside the initramfs. | Packaging |
| BOOT-8 | Does the splash appear on shutdown and reboot, and in firmware-update mode? | Plymouth modes |
| BOOT-9 | TPM2 auto-unlock or PIN: is it planned, and what does the prompt say? | Copy |
