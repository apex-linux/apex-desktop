# Software Updates and update health failure

## Summary

This spec covers how Apex shows image updates to the user, from the first
check to a failed boot:

| No. | Surface | Artboard |
| --- | --- | --- |
| 18 | Settings: Software Updates panel (System subpage) | `Updates.dc.html` |
| 26 | Update health failure alert (two states) | `Rollback.dc.html` |

It also fixes the cross-links to surfaces specified elsewhere:

*   The "Updates Ready" banner (`Transients.dc.html:43-58`), specified in
    [shell-calendar-notifications-osd.md](shell-calendar-notifications-osd.md).
*   The "Start the new version next time" switch in the Power Off dialog
    (`EndSession.dc.html:66-78`) and the Polkit dialog for going back
    (`Polkit.dc.html`), specified in [dialogs.md](dialogs.md).
*   The `apexctl` CLI drawn in terminals (`Polkit.dc.html`, `Tiling.dc.html`,
    `Screenshot.dc.html`, `Rollback.dc.html`).

The window chrome (sidebar, header bar, boxed lists, switches) is the shared
Settings chrome in [settings.md](settings.md#shared-window-chrome).

## Upstream mapping

| Part | Nearest upstream | Confidence |
| --- | --- | --- |
| OS image updates | bootc (OCI image, ostree deployments: booted, staged, rollback); rpm-ostree has the same model | Medium: the artboards show `sha256:` digests, "Channel stable (running image)" and a rollback slot, which fit bootc. The base is not confirmed by the owner |
| Signature check | containers-policy (`/etc/containers/policy.json`, sigstore signed images) used by bootc on pull | Medium |
| Health checks and fallback | greenboot (`/etc/greenboot/check/required.d`, `wanted.d`; GRUB `boot_counter`, default 3 attempts, then the previous entry) | Medium: "three times in a row" and "failed-units" match greenboot; greenboot's bootc support should be checked for the Fedora release used |
| Settings panel | None. GNOME Software's Updates page is the nearest. GNOME Settings has no updates page; this is a new subpage of System (`panels/system/`) | High that it is new |
| Update banner | GNOME Shell `MessageTray` notification from a user-session agent | High |
| Power Off switch | GNOME Shell `js/ui/endSessionDialog.js`, which already has a PackageKit offline-update checkbox ("Install pending software updates") and "Restart & Install Updates" labels | High; it needs to read the Apex updater instead of PackageKit |
| Go back authorisation | polkit action plus GNOME Shell `js/ui/components/polkitAgent.js` | High |
| `apexctl` | New CLI; the Rust test output in `Terminal.dc.html:247` shows a crate named `apexctl` | High that it is new |

Recommended architecture (not drawn, needed for consistency): one system
D-Bus service (the updater) that wraps bootc and greenboot state, exposes
the state machine below with properties and signals, and checks polkit.
The Settings panel, the banner agent, the Power Off dialog and `apexctl`
are all clients of it. Without one service the four surfaces will disagree.

## Layout and measurements

### Software Updates panel (18)

Window 1220x756 at left 110, top 50. Sidebar selects System. Content header
has a back button (`aria-label="Back to System"`, 32x32, radius 8) and the
title "Software Updates" (`Updates.dc.html:65-66`). Window buttons are drawn
as static spans. Column max 620, group gap 26.

| Element | Measurement and copy |
| --- | --- |
| Hero card | Card padding 28 20 22, centred column, gap 14, text centred |
| Hero tile | 72x72, radius 20, fill `--wall`, `shadow.lifted`, Apex mark (26 px square, 3 px `--accent` border, radius 5, rotated 45°) |
| Hero badge | 26 circle at right -6, bottom -6, white 14 px glyph, ring `0 0 0 3px var(--card)`. Fill and glyph per state (table below) |
| Hero title | h1 20/800, letter-spacing -0.3 |
| Hero text | 12.5, line-height 1.45, `--dim`, max-width 460, `text-wrap:pretty` |
| Progress (downloading) | 320 wide; bar 6 tall, radius 3, track `--btn-h`, fill `--accent` (64 % drawn); caption 11.5 `--dim` tabular "264 of 412 MB · about 1 minute left", gap 6 |
| Hero buttons | gap 10; 36 tall, padding 0 18, radius 18, 13/600. Secondary fill `--btn`; primary fill `--accent`, white |
| Hold note | `role=note`, flex gap 12, padding 14 16, radius 12, fill `--warn-bg`. 16 px warning glyph in `--warn`. Title 13.5/700 "Settings 51.1 is held back"; text 12.5, line-height 1.45, `--dim`: "Apex's Settings changes do not apply to 51.1 yet, so this update keeps 51.0. Not a security update. Held for up to 14 days, then Apex ships the stock 51.1." |
| What's New group | Title "What’s New". Disclosure row (button, `aria-expanded`, open by default): "GNOME 51.0 → 51.1, Linux 7.2.7 → 7.2.9, Mesa 26.1.0 → 26.1.2" / "and 5 other packages · 45.20261010.133, built Oct 10"; 16 px chevron rotates 180° when open, 150 ms |
| Package list | border-top 1px `--border`, padding 8 14 12, grid `80px minmax(0,1fr) auto`, column gap 14, row gap 6, 12 px. Kind in `--dim` ("upgraded"); package in JetBrains Mono 11.5/600, ellipsised; versions in mono 11.5 `--dim`, right-aligned. Rows: gnome-shell `51.0-1 → 51.1-1`; kernel `7.2.7-300 → 7.2.9-300`; mesa-dri-drivers and mesa-dri-drivers.i686 `26.1.0-1 → 26.1.2-1`; glibc and glibc.i686 `2.42-3 → 2.42-4` |
| Versions group | Rows (56, padding 10 14): "Running" / mono 12 `--dim` "45.20261008.131 · sha256:3f9c…a71e", trailing "built Oct 8" 12 `--dim`. "Next Restart" (ready only) / "45.20261010.133 · sha256:9e41…0c2b", trailing chip "Checked": 22 tall, padding 0 9, radius 11, fill `color-mix(in srgb, var(--accent) 16%, transparent)`, `--accent` 11.5/700. "Previous" / "45.20261001.124 · sha256:b02d…19c4", trailing button "Use at Next Restart…" (32 tall, padding 0 14, radius 8, `--btn`, 13/600) that opens the Polkit dialog |
| Versions footer | 12, line-height 1.45, `--dim`, padding 0 4: "If a new version keeps failing to start, Apex goes back to the previous one by itself." |
| Preferences group | "Automatic Downloads" / "Waits for mains power and an unmetered network", switch (on). "Update Channel" / "Qualified builds signed with the release key", value "Stable" 13.5 `--dim` (not a control). "Last Checked" / "Today at 09:00", button "Check Now" (32 tall, padding 0 14, radius 8, `--btn`, 13/600) |

### Update health failure alert (26)

| Element | Measurement and copy |
| --- | --- |
| Alert | `role=alert`, top 44, centred, 500 wide, padding 14, gap 14, radius 16 (`radius.lg`); glass `--panel` blur 30 saturate 180 %; `shadow.panel` |
| Icon tile | 38x38, radius 12, fill `--warn-bg`, 20 px restore-with-exclamation glyph in `--warn` |
| Meta line | 11.5 `--dim`, gap 6: "Apex Updates" (600) · "now" |
| Title | 14/700 |
| Body | 12.5, line-height 1.45, `--dim` |
| Dismiss | 24 circle, `--btn`, 14 px close glyph |
| Details grid | margin-left 50, padding 10 12, radius 10, fill `--btn`, columns `auto minmax(0,1fr)`, gaps 14 / 5; labels 12 `--dim`; values JetBrains Mono 11.5 |
| Buttons | margin-left 50, gap 8; each flex 1, 32 tall, radius 16, 13/600; secondary `--btn`, primary `--accent` white |
| Top bar | Clock "Wed Oct 21 08:52" with a 5 px `--accent` dot (unread notification) |

Copy by state (`Rollback.dc.html:108-122`):

| | check failed (default) | fell back after 3 boots |
| --- | --- | --- |
| Title | "Update Failed Its Startup Check" | "Apex Went Back to the Previous Version" |
| Body | "45.20261010.133 is running, but a required check did not pass. Going back to the version you had before is the safe choice. Nothing restarts until you say so." | "The update did not start properly three times in a row, so Apex started the version you had before. That build will not be offered again; a newer one will be." |
| Details | Failed check `failed-units`; Running `45.20261010.133`; Previous `45.20261008.131` | Running `45.20261008.131`; Set aside `45.20261010.133`; Your files `unchanged` |
| Buttons | "Keep This Version" (secondary); "Go Back…" (primary, opens Polkit) | "Show Changes" (secondary); "OK" (primary) |
| Behind | Terminal (840x420 at 300, 250) running `apexctl status`; top bar app name "Terminal" | Desktop only; app name "Desktop" |

### Cross-linked surfaces

| Surface | What this spec requires |
| --- | --- |
| "Updates Ready" banner (`Transients.dc.html:47-55`) | Source "Apex Updates"; title "Updates Ready"; body "45.20261010.133 is downloaded. GNOME 51.1, Linux 7.2.9 and 6 other packages start at the next restart."; buttons "Later", "Restart Now" (both `--btn`). Posted once per build on entering Ready |
| Power Off dialog switch (`EndSession.dc.html:66-78`) | Row "Start the new version next time" / "45.20261010.133 · GNOME 51.1, Linux 7.2.9, Mesa 26.1.2", switch default on (`:87`). On: middle button "Restart & Update"; off: "Restart" (`:105`). Shown only in Ready |
| Polkit dialog (`Polkit.dc.html`) | Title "Authentication Required"; message "Booting the previous version of Apex at the next restart needs an administrator password."; Details: Action `io.github.apex-linux.apex.update.rollback`, Vendor "Apex"; hint "Or touch the fingerprint reader" |

## States

### State machine

Updater states (one per machine, owned by the system service). The panel
`state` tweak covers the first five; `Rollback.dc.html` covers the two
health states.

| State | Meaning (bootc terms) | Panel hero | Drawn |
| --- | --- | --- | --- |
| `up-to-date` | Booted image is the newest on the channel | "Apex Is Up to Date" / "45.20261008.131 is the newest build on the stable channel. Checked today at 09:00." Primary "Check Now". Badge check, fill `#3a944a` | Yes |
| `checking` | Registry query in progress | Spinner; Check Now insensitive | No |
| `available` | Newer digest found, not downloaded (Automatic Downloads off) | "Update Available" / "45.20261010.133 · 412 MB. It downloads in the background and nothing changes until you restart." Primary "Download". Badge download, `--accent` | Yes |
| `waiting` | Automatic Downloads on, but a condition fails | "Update Waiting" / "The laptop is on battery. 45.20261010.133 downloads when it is plugged in." Secondary "Download Anyway". Badge pause, fill `#9c6500` | Yes (battery only) |
| `downloading` | Pulling layers, then verifying the signature | "Downloading Update" / "45.20261010.133. You can keep working; Apex checks the signature before keeping it." Progress bar, no buttons. Badge download, `--accent` | Yes |
| `ready` | Signature checked; deployment staged but locked, so it is not finalised at shutdown unless the user chose to apply | "Restart to Finish Updating" / "45.20261010.133 is downloaded and its signature checked. Your current version stays in place until you restart." Secondary "Keep Current Version", primary "Restart Now". Badge restart, `--accent`. Versions shows "Next Restart" with "Checked" | Yes (default) |
| `rollback-pending` | User chose "Use at Next Restart…" or "Go Back…" and authenticated | Not drawn. Needs a hero ("Restart to Go Back") and Versions showing the previous build as Next Restart | No |
| `health-check-failed` | Booted the new build; greenboot required check failed; auto-reboot disabled | Alert "check failed". Panel hero not drawn | Alert only |
| `fell-back` | Boot counter ran out; GRUB booted the previous entry; the failed build is set aside and denied | Alert "fell back after 3 boots". Panel hero not drawn | Alert only |
| `error` | Check, download or signature failed; disk full; registry unreachable | Not drawn | No |

The What's New group shows in every state except `up-to-date`
(`Updates.dc.html:256`); "Next Restart" shows only in `ready` (`:257`).

Transitions:

| From | Event | To | Surface |
| --- | --- | --- | --- |
| any idle | Timer, or Check Now | `checking` | Panel |
| `checking` | Nothing newer | `up-to-date` | Last Checked updates |
| `checking` | Newer build, Automatic Downloads off | `available` | Panel only, no banner (not drawn; confirm) |
| `checking` | Newer build, Automatic Downloads on, AC power and unmetered | `downloading` | |
| `checking` | Newer build, on battery or metered | `waiting` | |
| `available` | Download | `downloading` | |
| `waiting` | Download Anyway, or conditions met | `downloading` | |
| `downloading` | Pull and signature OK | `ready` | Banner "Updates Ready"; Power Off switch appears |
| `downloading` | Failure | `error` | Not drawn |
| `ready` | Restart Now (panel or banner), or Restart & Update / Power Off with the switch on | Unlock the staged deployment, then reboot or power off | Banner "Restart Now" should open the Restart dialog with the switch on, not reboot at once (confirm) |
| `ready` | Keep Current Version, or Restart / Power Off with the switch off | Stay in `ready` after the next boot (re-stage locked from the stored image) | Q-UPD-4 |
| `ready` | Banner Later or dismiss | `ready`; banner not shown again for this build | |
| booting new build | Boot completes and greenboot passes | `up-to-date`; Previous becomes the old booted build | |
| booting new build | Boot does not complete, 3 times | GRUB falls back; service fixes the deployment order and denies the build | `fell-back` alert |
| booted new build | Required check fails | `health-check-failed` | Alert; no automatic reboot |
| `health-check-failed` | Keep This Version | Mark boot good (greenboot `boot_success`), `up-to-date` | |
| `health-check-failed` | Go Back… then authenticate | `rollback-pending` | Polkit dialog; then restart is up to the user |
| `fell-back` | OK | `up-to-date` (on the old build) | |
| `fell-back` | Show Changes | Opens this panel (destination not drawn; confirm) | |
| `up-to-date` or `ready` | Previous: Use at Next Restart…, authenticate | `rollback-pending` | Polkit |

The hold note (`showHold`) is independent of the state: it means the next
build pins one package (here gnome-control-center at 51.0) while the rest
moves. It should show only when the pending build contains a held package,
not in `up-to-date` (the tweak allows that combination).

### Required design choices behind the states

*   No automatic reboots. "Nothing restarts until you say so" and
    "apexctl never reboots the computer by itself" (`Screenshot.dc.html:55`)
    rule out bootc's stock `bootc-fetch-apply-updates.timer`, which applies
    and reboots. Mask it. Greenboot's red-boot auto reboot must also be
    off for required checks, or the `health-check-failed` state cannot
    exist.
*   Two failure paths. "Did not start properly three times" is the boot
    counter (no user session). "Started but a required check failed" is a
    greenboot check that ran after boot. They need different checks and the
    owner must list which checks are required (only `failed-units` is
    named).
*   Denylist. "That build will not be offered again" is not a bootc or
    greenboot feature; the service must keep a list of rejected digests.
*   Locked staging. `apexctl status` draws the staged build as "locked:
    not used at the next boot" (`Tiling.dc.html:52-53`), and "Start the
    new version next time" off must leave the current version in place on
    the next boot. Stage updates locked
    (ostree finalisation lock; rpm-ostree `--lock-finalization`; check the
    bootc download-only mode in the version shipped) and unlock only when
    the user applies.
*   Automatic Downloads is a system policy (one updater for the machine),
    so it belongs in the service's config, not a per-user GSettings key.
    GNOME Software's `org.gnome.software download-updates` is the per-user
    analogue and should not be used.

### `apexctl` output contract

Commands and output drawn, as data:

| Command | Output |
| --- | --- |
| `apexctl status` (up to date, `Polkit.dc.html:57-64`) | "Apex is up to date (45.20261008.131)." blank line, then a key column 11 characters wide: `Booted     45.20261008.131  built 2026-10-08`, next line indented 11 with `sha256:3f9c0e7a…a71e`; `Rollback   45.20261001.124  built 2026-10-01` / `sha256:b02d4c19…19c4`; `Channel    stable (running image)`; `Checked    2026-10-11 09:00 UTC` |
| `apexctl status` (ready, `Tiling.dc.html:47-56`) | "An update is downloaded and waiting." / "Use it at the next restart with: apexctl update apply", then the same block with an extra row after Booted: `Staged     45.20261010.133  built 2026-10-10` / indented `locked: not used at the next boot`. This confirms the locked-staging model; `apexctl update apply` unlocks it |
| `apexctl status` (check failed, `Rollback.dc.html:47-54`) | "The last update failed its health checks." then Booted .133, Rollback .131, Channel; no Checked line |
| `apexctl update changes` (`Screenshot.dc.html:43-51`) | Summary "GNOME 51.0 → 51.1, Linux 7.2.7 → 7.2.9, Mesa 26.1.0 → 26.1.2, 5 other packages", blank, then rows `upgraded  <package>  <old> → <new>` with full NEVRs (`2.42-3.fc45`), sorted by name |
| `apexctl update apply` (`Screenshot.dc.html:53-55`) | "Applied 45.20261010.133 (sha256:9e41…0c2b). It will be used at the next boot." / "Reboot to finish the update. apexctl never reboots the computer by itself." |
| `apexctl update rollback` (`Polkit.dc.html:66-67`) | "Waiting for authorization…" while the Polkit dialog is up |

Not drawn but needed: `apexctl update check`, `download`, `keep`
(mark good), exit codes, `--json`, and the output after rollback
succeeds.

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour | `--win`, `--side`, `--fg`, `--dim`, `--border`, `--card`, `--card-border`, `--btn`, `--btn-h`, `--accent`, `--warn`, `--warn-bg`, `--panel`, `--panel-border`, `--shadow`, `--wall`; terminal scene `--term-*`. Literals: badge `#3a944a` (Green accent, not `--ok`), badge `#9c6500` (light `--warn`, used in both themes), chip `color-mix(… 16%)` |
| Type | `typography.family.ui`, `family.mono` (versions, digests, package rows, details values); sizes 11.5, 12, 12.5, 13, 13.5, 14, 20; weights 600, 700, 800; tabular numbers on progress |
| Radius | `sm` 8, `md` 10, `pill-bar` 12, `window` 14, `lg` 16, `card-lg` 18 (hero pills), `toast` 20 (hero tile); literals 3 (progress), 11 (chip) |
| Shadow | `window`, `card`, `knob`, `lifted`, `panel`; badge ring `0 0 0 3px var(--card)` |
| Glass | Alert: Quick Settings / toast row (30 px, 180 %) |
| Motion | `duration.fast` (chevron), switch `duration.base` with `easing.standard` |

Token conflict: `--warn-bg` is `rgba(200,136,0,.12)` / `.16` in
`Updates.dc.html:18-19` and `.14` / `.2` in `Rollback.dc.html:18-19`
(recorded in `tokens.json`).

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Updater service (states, denylist, locked staging, policy) | Patch (new component) | Nothing upstream provides this for bootc |
| Software Updates subpage under System | Patch | New page in gnome-control-center, or a standalone "Apex Updates" app opened from a System row. The notification source name "Apex Updates" suggests the app route is open |
| Hero, Versions, Preferences, What's New | Patch | New UI, built from stock libadwaita widgets (status page, boxed list, expander row) |
| Hold note | Patch | Needs build metadata listing held packages and the hold deadline |
| Banner | Stock widget, new sender | A notification with two actions from a session agent |
| Health failure alert details grid | Patch | Stock notifications render title and body only; the monospace key/value grid needs a shell change, or must become body lines (cheaper, recommended) |
| Persistent alert | Stock | Critical urgency keeps a notification on screen |
| Power Off switch | Patch | `endSessionDialog.js` already has the offline-update checkbox flow for PackageKit; point it at the Apex service and change the copy |
| Polkit dialog | Theme | Stock agent; action and message come from the policy file |
| greenboot checks and boot counting | Stock plus config | Configure required checks, disable auto reboot |
| `apexctl` | Patch (new CLI) | Client of the service |

## Accessibility

*   The alert uses `role=alert` (drawn); the shell must announce it once,
    not on every re-show.
*   The progress bar needs a progressbar role with value and the text
    "264 of 412 MB" as its description.
*   The hero badge glyph is decorative; the title carries the state.
*   The "Checked" chip needs an accessible description, for example
    "Signature checked".
*   Digests are truncated; expose the full digest as a tooltip and to
    screen readers, and make it selectable for copy.
*   White on `--accent` pills (Restart Now, Download, Go Back…) fail AA for
    some accents at 13 px; see [settings.md](settings.md#accessibility).
*   Focus order: back, hero buttons, What's New disclosure, Use at Next
    Restart…, Automatic Downloads, Check Now. In the alert: Dismiss,
    secondary, primary; Escape dismisses.

## Acceptance criteria

1.  Each updater state shows exactly the hero title, text, badge and
    buttons in the state table, and the panel updates without reopening
    when the service changes state.
2.  "Next Restart" appears in Versions only in `ready`; What's New is
    hidden only in `up-to-date`.
3.  In `downloading`, the bar width equals downloaded / total, and the
    caption shows both sizes in MB and a time estimate.
4.  With Automatic Downloads on, a new build does not download on battery
    or on a metered connection; the panel shows `waiting` with a reason that
    names the actual condition (battery or metered).
5.  Download Anyway starts the download in either condition.
6.  A build whose signature does not verify against the release key is
    never staged, and the panel shows an error.
7.  Entering `ready` posts one "Updates Ready" banner per build; Later
    dismisses it and it does not return for that build.
8.  In `ready`, the Power Off and Restart dialogs show the "Start the new
    version next time" switch, on by default. With it on, after restart
    `bootc status` (or `apexctl status`) shows the new build booted. With it
    off, the old build boots and the panel is still `ready`.
9.  Keep Current Version keeps the current build on the next boot, and the
    update stays available without downloading again.
10. No updater path reboots or powers off the machine without a user
    action. `bootc-fetch-apply-updates.timer` is masked.
11. Use at Next Restart… and Go Back… both raise the Polkit dialog for the
    rollback action; cancelling changes nothing; authenticating makes the
    previous build the next boot entry and does not reboot.
12. When a required greenboot check fails, the session shows the "check
    failed" alert with the failed check's name, and the machine does not
    reboot by itself.
13. Keep This Version marks the boot good; the alert does not return on
    the next boot.
14. When the new build fails to boot three times, the previous build boots,
    the "fell back" alert appears after login, and `apexctl update check`
    never offers the failed digest again.
15. Package counts in the panel, banner, Power Off row and `apexctl update
    changes` are computed from the same diff and agree.
16. Every version string, digest and build date is read from the image
    metadata; none is hard-coded.
17. `apexctl status` output matches the drawn layout (11-character key
    column) for up to date, ready and check failed.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

*   **Q-UPD-1** Version scheme `45.YYYYMMDD.NNN` (for example
    `45.20261008.131`). The leading 45 ties Apex's version to the Fedora
    major. NNN looks like a global build counter (124 on Oct 1, 131 on
    Oct 8, 133 on Oct 10), while Fedora's own image versions use a
    per-day respin index (`NN.YYYYMMDD.0`). Is the date UTC? What happens
    at a Fedora major rebase? This text is old-spec until confirmed.
*   **Q-UPD-2** Policy id `io.github.apex-linux.apex.update.rollback`
    (`Polkit.dc.html:118`). It uses `apex-linux` with a hyphen while the
    GSettings schema drawn elsewhere uses `io.github.apex_linux`
    (`Terminal.dc.html:258`), and "apex" repeats. Pick one reverse-DNS
    prefix for app id, D-Bus name, schema and policy ids (for example
    `io.github.apex_linux.Updates.rollback`), and list the other actions
    (check, download, apply, keep, change channel) with their defaults.
*   **Q-UPD-3** Is the base bootc or rpm-ostree? Locked staging, rollback
    and greenboot integration differ in detail between them.
*   **Q-UPD-4** What does "Keep Current Version" mean: skip this restart
    (stay `ready`), or discard the download (back to `available`)? The same
    question applies to the Power Off switch turned off. Related wording
    conflict: in `ready` the panel labels the staged build "Next Restart"
    (`Updates.dc.html:144`), while `apexctl status` says "locked: not used
    at the next boot" (`Tiling.dc.html:53`) and the Power Off switch
    defaults to on. Decide whether a restart without the dialog (for
    example `systemctl reboot`) applies the update.
*   **Q-UPD-5** The hold note says that after 14 days "Apex ships the stock
    51.1". If the Apex Settings patches carry this Updates page and the
    Apex Desktop panel, shipping stock Settings removes them. Is that
    accepted, or does the hold block the whole GNOME update?
*   **Q-UPD-6** Package counts disagree: "and 5 other packages" with three
    named (`Updates.dc.html:119`) but six rows listed (`:240-247`);
    "6 other packages" in the banner (`Transients.dc.html:49`); "5 other
    packages" in `apexctl` (`Screenshot.dc.html:44`). Define how a package
    is counted (are `.i686` builds separate?).
*   **Q-UPD-7** Missing panel states: `checking`, `error`, metered network
    in `waiting`, `rollback-pending`, the panel after `fell-back` (Previous
    would then be the failed build, which must not offer "Use at Next
    Restart…"), a cancel action while downloading, and low disk space.
*   **Q-UPD-8** Should `available` (Automatic Downloads off) also post a
    banner? Only `ready` is drawn.
*   **Q-UPD-9** Update Channel is shown as plain text "Stable". Are other
    channels planned, and who may switch?
*   **Q-UPD-10** Old-spec text in these artboards: "apex@fedora" (terminal
    titles and prompts), "fc45" package releases, "Fedora Linux 45",
    "GNOME 51", "Linux 7.2", "Mesa 26.1". Treat as sample data. The waiting
    copy says "The laptop is on battery"; desktops have no battery, so use
    the machine-neutral reason ("on battery power", "on a metered
    connection").
*   **Q-UPD-11** Digest truncation differs: `sha256:3f9c…a71e` (4+4,
    Updates panel) against `sha256:3f9c0e7a…a71e` (8+4, `apexctl`), and
    `apexctl` itself shows `sha256:9e41…0c2b` (4+4) next to 8+4 values
    (`Rollback.dc.html:51,53`). Pick one rule.
*   **Q-UPD-12** Banner and alert differ: banner 460 wide, padding 12,
    title 13.5, both buttons `--btn` (`Transients.dc.html:43-55`); alert 500
    wide, padding 14, title 14, accent primary (`Rollback.dc.html:60-85`).
    Are these two notification sizes intended?
*   **Q-UPD-13** Which icon does "Apex Updates" use? The banner and Power
    Off row use the GNOME Software icon (`91d271bb…`); the alert uses a
    warning tile. If GNOME Software is not shipped (dock shows Bazaar), a
    dedicated icon is needed.
