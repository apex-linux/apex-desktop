# Software Updates and update health failure

## Summary

This spec covers how Apex shows image updates, from the first check to a
version that does not start. Milestone M3 of `apex/docs/spec.md` builds it.

| No. | Surface | Artboard |
| --- | --- | --- |
| 18 | Settings: Software Updates panel (System subpage) | `Updates.dc.html` |
| 26 | Update health failure alert | `Rollback.dc.html` |

**Owner decision, 2026-11-17 (OQ-04):** updates use stock `bootc` only
("Chỉ bootc gốc"). There is no Apex update daemon. The Settings panel is a
front end to `bootc upgrade`, `bootc rollback` and `bootc status`. This
confirms `apex/docs/spec.md` ("A custom update daemon. Apex uses what `bootc`
provides.").

The artboards were drawn for an update daemon (`Update1`) that the decision
removes. Where this spec and the artboards disagree, **this spec wins**. The
artboards remain the visual reference for every element this spec keeps:
sizes, type, colours, radii and the window chrome. The
[cut list](#what-stock-bootc-provides-and-what-is-cut) names every drawn
element that no longer ships.

It also fixes the cross-links to surfaces specified elsewhere:

*   The "Updates Ready" banner (`Transients.dc.html:43-58`) is cut; see
    [shell-calendar-notifications-osd.md](shell-calendar-notifications-osd.md).
*   The "Start the new version next time" switch in the Power Off dialog
    (`EndSession.dc.html:66-78`) and the Polkit dialog for going back
    (`Polkit.dc.html`), specified in [dialogs.md](dialogs.md).
*   The `apexctl` CLI drawn in terminals is cut; terminals use `bootc`
    directly.

The window chrome (sidebar, header bar, boxed lists, switches) is the shared
Settings chrome in [settings.md](settings.md#shared-window-chrome).

## Upstream mapping

| Part | Upstream | Confidence |
| --- | --- | --- |
| OS image updates | `bootc` on the Fedora 45 bootc base: `bootc upgrade`, `bootc rollback`, `bootc status`, with the ostree backend (booted, staged, rollback deployments) | High: owner decision and binding spec |
| Signature check | containers-policy (`/etc/containers/policy.json`, sigstore) applied by bootc when it pulls | High that bootc uses it; how `bootc upgrade` reports a refused pull must be checked (see below) |
| Boot failure handling | None in stock bootc. The user picks the previous deployment in the GRUB menu | High: the bootc docs say nothing falls back automatically |
| Settings panel | None upstream. GNOME Settings has no updates page; this is a new subpage of System (`panels/system/`), or a separate page if OQ-12 moves it | High that it is new |
| Privileged calls | polkit, through a small Apex helper executable run with `pkexec` (not a daemon) | Medium: proposal, see [Architecture](#architecture-without-a-daemon) |
| Power Off switch | GNOME Shell `js/ui/endSessionDialog.js`, which has a PackageKit offline-update checkbox | High; it must read bootc state instead of PackageKit |
| Go back authorisation | polkit action plus GNOME Shell `js/ui/components/polkitAgent.js` | High |

### What stock bootc provides and what is cut

Checked against the bootc documentation on 2026-11-17 (bootc v1.17.4 was
the latest release). The docs moved from `bootc-dev.github.io/bootc` to
`bootc.dev/bootc`. "Verified" means the documentation states it; nothing
here was run on a machine yet. The Fedora bootc docs
(`docs.fedoraproject.org/en-US/bootc/`) refused automated access, so
Fedora-specific defaults are unverified.

| Behaviour | What stock bootc does | Source | Status |
| --- | --- | --- | --- |
| Check for an update | `bootc upgrade --check` fetches only the manifest and config | [bootc-upgrade(8)](https://bootc.dev/bootc/man/bootc-upgrade.8.html) | Verified |
| Download without using it at the next boot | `bootc upgrade --download-only` stages the update without applying it; `bootc status --verbose` shows "Download-only: yes" | [bootc-upgrade(8)](https://bootc.dev/bootc/man/bootc-upgrade.8.html), [bootc-upgrades(7)](https://bootc.dev/bootc/bootc-upgrades.7.html) | Verified. The release that added it is not stated (release notes suggest v1.16.10); check the version in Fedora 45 |
| Apply a downloaded update | `bootc upgrade --from-downloaded` unlocks the staged deployment without contacting the registry; add `--apply` to reboot | [bootc-upgrades(7)](https://bootc.dev/bootc/bootc-upgrades.7.html) | Verified |
| A download-only update across a reboot | Discarded at reboot; the cached image data stays, so staging it again is fast | [bootc-upgrades(7)](https://bootc.dev/bootc/bootc-upgrades.7.html) | Verified |
| Plain `bootc upgrade` | Stages the update; it applies at shutdown through `ostree-finalize-staged.service`; it does not reboot | [bootc-upgrade(8)](https://bootc.dev/bootc/man/bootc-upgrade.8.html) | Verified |
| Go back | `bootc rollback` changes the bootloader entry order so the rollback deployment boots next; it discards a staged deployment; it reboots only with `--apply` | [bootc-rollback(8)](https://bootc.dev/bootc/man/bootc-rollback.8.html) | Verified. Going back more than one step is not documented |
| Machine-readable state | `bootc status --format=json --format-version=1`: `booted`, `staged`, `rollback`, `rollbackQueued`, `otherDeployments`; per entry `image` (`image.image`, `image.signature`), `imageDigest`, `version`, `timestamp`, `cachedUpdate`, `downloadOnly`, `pinned` | [bootc-status(8)](https://bootc.dev/bootc/man/bootc-status.8.html), [host-v1.schema.json](https://bootc.dev/bootc/host-v1.schema.json) | Verified. Whether `--check` fills `cachedUpdate`, and whether a non-root user may run `bootc status`, are not documented |
| Programmatic interface | No D-Bus and no IPC; fork and exec the CLI. `--progress-fd` emits JSON Lines progress (pulling, importing, staging) and is experimental | [bootc-relationships(7)](https://bootc.dev/bootc/bootc-relationships.7.html), [book](https://bootc.dev/bootc/print.html) | Verified |
| State change hook | `bootc-status-updated.path` watches `/ostree/bootc`; `bootc-status-updated.target` is for units that react | [book](https://bootc.dev/bootc/print.html) | Verified (names as documented; check the exact unit names on the image) |
| Automatic updates | `bootc-fetch-apply-updates.timer` checks, downloads and **reboots**; upstream ships it enabled for daily updates; disable with `systemctl disable` | [book](https://bootc.dev/bootc/print.html), [bootc-management-services(7)](https://bootc.dev/bootc/building/bootc-management-services.7.html) | Verified upstream. Fedora's default not verified |
| Signed images | bootc honours `/etc/containers/policy.json`; `--enforce-container-sigpolicy` on `switch` and install config rejects pulls when the policy says `insecureAcceptAnything` | [bootc-switch(8)](https://bootc.dev/bootc/man/bootc-switch.8.html), [book](https://bootc.dev/bootc/print.html) | Partly. That `bootc upgrade` refuses an unsigned image under a signature-requiring policy is not stated; M3 must demonstrate it |
| Boot counting and automatic fallback | Not provided. ostree relies on systemd boot assessment; the composefs backend configures none; the docs say nothing falls back automatically and the system must health-check itself | [bootc-boot-failure-detection(7)](https://bootc.dev/bootc/bootc-boot-failure-detection.7.html), [book](https://bootc.dev/bootc/print.html) | Verified: **cut** |
| Health checks | Not provided. The bootc book says "greenboot does not yet integrate with bootc"; greenboot-rs (0.16.x, the `greenboot` RPM) says it is designed for bootc. The sources disagree, and greenboot is an extra package either way | [book](https://bootc.dev/bootc/print.html), [greenboot-rs](https://github.com/fedora-iot/greenboot-rs) | **Cut** for M3 (OQ-36) |
| Rejected-build list | Not provided | none | **Cut** |
| Holds or deferrals per package | Not provided (an image is updated as a whole) | none | **Cut** |
| Battery or metered-network awareness | Not provided by bootc. systemd's `ConditionACPower=` can gate a timer; there is no systemd condition for metered networks | systemd.unit(5) (from knowledge; not rechecked) | Battery: kept through the timer. Metered: **cut** |
| Package changelog between builds | Not provided (`bootc-config-diff` covers `/etc` only) | [book](https://bootc.dev/bootc/print.html) | Package list **cut**; see [What's New](#whats-new) |
| Pin a deployment | Schema has `pinned` and `otherDeployments`; no bootc command to pin is documented | [host-v1.schema.json](https://bootc.dev/bootc/host-v1.schema.json) | Not used |

Element by element:

| Drawn element | Decision | Replacement |
| --- | --- | --- |
| Hero states up to date, available, downloading, ready | Keep | Driven by `bootc status` and the exit of `bootc upgrade --check` |
| `waiting` state, battery reason | Merge into `available` | Text says the download starts when the computer is plugged in |
| `waiting` state, metered reason | Cut | none |
| Hold note "Settings 51.1 is held back… Held for up to 14 days" | Cut | none; an image updates as a whole |
| "Checked" chip on Next Restart | Cut | Every staged image is signed once M3's signature policy is on, so the chip carries no information |
| What's New package list | Cut for M3 | A summary row from image metadata and a Release Notes link |
| Versions: Running, Next Restart, Previous | Keep | `booted`, `staged`, `rollback` |
| "Use at Next Restart…" on Previous | Keep | `bootc rollback` through polkit |
| Footer "Apex goes back to the previous one by itself" | Cut (false without boot counting) | New copy pointing at the startup menu |
| Automatic Downloads switch | Keep, reworded | Enables an Apex timer that runs `bootc upgrade --download-only` on mains power |
| Update Channel "Stable" | Keep as read-only text | Tag of `booted.image.image` (for example `main`) |
| Last Checked, Check Now | Keep | The panel's own check, or the timer's last run |
| Alert "Update Failed Its Startup Check" (`failed-units`) | Cut | Needs greenboot (OQ-36) |
| Alert "Apex Went Back to the Previous Version" after three boots | Cut | Replaced by "You Started the Previous Version", which detects a manual choice in the startup menu |
| "That build will not be offered again" | Cut | A label on the panel when the offered build is the one the user went back from |
| "Updates Ready" banner, "Apex Updates" sender | Cut | none for M3; the panel and the Power Off switch show a downloaded update |
| `apexctl` CLI and its output | Cut | `bootc status`, `bootc upgrade`, `sudo bootc rollback` |
| Power Off switch "Start the new version next time" | Keep, needs the Shell patch in [dialogs.md](dialogs.md) | `bootc upgrade --from-downloaded` before the restart |
| `bootc-fetch-apply-updates.timer` | Disable on the image | It reboots, which breaks "nothing restarts until you say so" |

### Architecture without a daemon

Not drawn; needed so that the panel, the Power Off dialog and the alert agree.

*   **Reading state.** A oneshot unit `apex-bootc-status.service`, wanted by
    `bootc-status-updated.target`, writes `bootc status --format=json
    --format-version=1` to `/run/apex/bootc-status.json` (mode 0644). The
    panel, the Shell and the Power Off dialog read that file and watch it
    for changes. This runs only when bootc changes state, so it is not a
    daemon. If `bootc status` turns out to work without root, the clients
    call it directly and the unit is not needed.
*   **Changing state.** One helper executable,
    `/usr/libexec/apex/bootc-action`, accepts exactly `check`, `download`,
    `apply`, `rollback` and runs the matching `bootc` command. Each verb has
    its own polkit action (ids in the table below), so the policy can differ
    per verb. Clients run it with `pkexec`. It holds no state and exits when
    `bootc` exits.
*   **Automatic Downloads.** `apex-update-download.timer` (daily, randomised
    delay) starts `apex-update-download.service`, which runs
    `bootc upgrade --download-only --quiet` with `ConditionACPower=true`. The
    switch enables or disables this timer. `bootc-fetch-apply-updates.timer`
    is disabled in the image. Automatic Downloads is system-wide, not a
    per-user GSettings key.

| Verb | Command | polkit action | Default for an active local admin |
| --- | --- | --- | --- |
| `check` | `bootc upgrade --check` | `io.github.apex_linux.Updates.check` | Allowed without a password |
| `download` | `bootc upgrade --download-only` | `io.github.apex_linux.Updates.download` | Allowed without a password |
| `apply` | `bootc upgrade --from-downloaded` | `io.github.apex_linux.Updates.apply` | Allowed without a password (the image is already downloaded and verified; a password at Power Off would be hostile) |
| `rollback` | `bootc rollback` | `io.github.apex_linux.Updates.rollback` | Administrator password, kept for the session (matches `Polkit.dc.html`) |

The ids follow the underscore rule in OQ-08; the drawn id
`io.github.apex-linux.apex.update.rollback` is replaced.

## Layout and measurements

### Software Updates panel (18)

Window 1220x756 at left 110, top 50. Sidebar selects System. Content header
has a back button (`aria-label="Back to System"`, 32x32, radius 8) and the
title "Software Updates" (`Updates.dc.html:65-66`). Column max 620, group gap
26. Group order: hero card, What's New, Versions, Preferences.

| Element | Measurement and copy |
| --- | --- |
| Hero card | Card padding 28 20 22, centred column, gap 14, text centred |
| Hero tile | 72x72, radius 20, fill `--wall`, `shadow.lifted`, Apex mark (26 px square, 3 px `--accent` border, radius 5, rotated 45°) |
| Hero badge | 26 circle at right -6, bottom -6, white 14 px glyph, ring `0 0 0 3px var(--card)`. Fill and glyph per state (table below) |
| Hero title | h1 20/800, letter-spacing -0.3 |
| Hero text | 12.5, line-height 1.45, `--dim`, max-width 460, `text-wrap:pretty` |
| Progress (downloading) | 320 wide; bar 6 tall, radius 3, track `--btn-h`, fill `--accent`; caption 11.5 `--dim`, tabular numbers |
| Hero buttons | gap 10; 36 tall, padding 0 18, radius 18, 13/600. Secondary fill `--btn`; primary fill `--accent-strong` with white text (see [Accessibility](#accessibility)) |
| Hold note | Cut |
| Versions group | Rows 56 tall, padding 10 14. Title mono 12 `--dim` "<version> · sha256:<first 4>…<last 4>", trailing text 12 `--dim` "built <Mon D>". Rows and trailing items by state below |
| Versions footer | 12, line-height 1.45, `--dim`, padding 0 4: "If a new version does not start, restart and choose the previous version in the startup menu." (proposed copy, replaces the drawn sentence) |
| Preferences group | "Automatic Downloads" / "Downloads updates when the computer is plugged in", switch. "Update Channel" / "Signed builds from Apex", value 13.5 `--dim` (the image tag, for example "main"; not a control). "Last Checked" / "Today at 09:00", button "Check Now" (32 tall, padding 0 14, radius 8, `--btn`, 13/600) |

#### What's New

Kept as one disclosure group, reduced for M3:

| Element | Measurement and copy |
| --- | --- |
| Summary row | Title "Apex <version>"; subtitle "Built <Mon D>". Same row metrics as the drawn disclosure row (`Updates.dc.html:119`), without the chevron |
| Release Notes row | Title "Release Notes", trailing 16 px external-link glyph; opens the release page for that version in the browser |
| Package list | Cut for M3. If the owner wants it back, `apex-image` CI must publish the package diff with each build (OQ-37) |

The drawn summary "GNOME 51.0 → 51.1, Linux 7.2.7 → 7.2.9, Mesa 26.1.0 →
26.1.2" needs per-package data that bootc does not provide.

#### Versions rows by state

| State | Running | Second row | Previous |
| --- | --- | --- | --- |
| `up-to-date`, `available`, `downloading` | `booted` | none | `rollback`, button "Use at Next Restart…" |
| `downloaded` | `booted` | "Downloaded" / `staged`, trailing "Not used until you restart from here" 12 `--dim` | `rollback`, button "Use at Next Restart…" |
| `staged` | `booted` | "Next Restart" / `staged` | `rollback`, button "Use at Next Restart…" |
| `rollback-pending` | `booted` | "Next Restart" / the queued previous build | none; the current build becomes Previous after the restart |
| `previous-started` | `booted` (the older build) | none | The newer build, labelled "Did not start" in `--warn`, no button |

"Use at Next Restart…" is hidden when there is no `rollback` deployment
(first boot after install).

### Health failure alert (26), reduced

The alert keeps the drawn metrics and changes its content.

| Element | Measurement and copy |
| --- | --- |
| Alert | `role=alert`, top 44, centred, 500 wide, padding 14, gap 14, radius 16 (`radius.lg`); glass `--panel` blur 30 saturate 180 % (solid `--panel-solid` until OQ-03 allows glass); `shadow.panel` |
| Icon tile | 38x38, radius 12, fill `--warn-bg`, 20 px restore-with-exclamation glyph in `--warn` |
| Meta line | 11.5 `--dim`, gap 6: "Software Updates" (600) · "now" |
| Title | 14/700: "You Started the Previous Version" |
| Body | 12.5, line-height 1.45, `--dim`: "Apex <new> did not finish starting, so this is Apex <old>. Your files are unchanged. The next restart tries <new> again unless you keep this version." |
| Details grid | Cut (it needed check names from greenboot); the body carries the versions |
| Dismiss | 24 circle, `--btn`, 14 px close glyph |
| Buttons | margin-left 50, gap 8; each flex 1, 32 tall, radius 16, 13/600. Secondary "Try Again Next Time" (`--btn`); primary "Keep This Version…" (`--accent-strong`, white), which raises the polkit dialog |

The alert is posted at login by the Apex GNOME Shell extension from
`/run/apex/bootc-status.json`. It is the only update notification left, and
it reads stock bootc state, so it is not daemon-sourced. If the owner does
not want the extension to post it, the panel shows the same content as its
`previous-started` hero and nothing appears until the user opens Settings
(OQ-21).

### Cross-linked surfaces

| Surface | What this spec requires |
| --- | --- |
| "Updates Ready" banner (`Transients.dc.html:47-55`) | Cut |
| Power Off dialog switch (`EndSession.dc.html:66-78`) | Shown only in `downloaded`. Row "Start the new version next time" / "Apex <version>". Switch default on: middle button "Restart & Update", and confirming runs `bootc-action apply` before the restart. Off: "Restart", and the restart leaves the download-only update unused (stock bootc discards it at boot). In `staged` the update applies on any restart, so the dialog shows no switch, and the middle button reads "Restart & Update" |
| Polkit dialog (`Polkit.dc.html`) | Title "Authentication Required"; message "Booting the previous version of Apex at the next restart needs an administrator password."; Details: Action `io.github.apex_linux.Updates.rollback`, Vendor "Apex"; hint "Or touch the fingerprint reader" only when OQ-19 allows fingerprint for polkit |
| Startup menu | Fedora's GRUB shows the menu after a boot that did not complete (legacy decision 17); this spec depends on that for `previous-started`. Not verified on a bootc image; see [boot-and-disk-unlock.md](boot-and-disk-unlock.md) |

## States

### State machine

The panel derives its state from `bootc status` each time the status file
changes, plus one transient state while a `bootc-action` call runs. Nothing
stores state outside bootc.

| State | Condition from `bootc status` | Hero | Drawn |
| --- | --- | --- | --- |
| `up-to-date` | No `staged`; the last check found nothing newer than `booted.imageDigest` | "Apex Is Up to Date" / "Apex <version> is the newest build. Checked today at 09:00." Primary "Check Now". Badge check, fill `#3a944a` | Yes |
| `checking` | `bootc-action check` running | Spinner in place of the badge; Check Now insensitive; text "Checking for updates…" | No |
| `available` | No `staged`; the last check found a newer digest | "Update Available" / "Apex <version> is ready to download. Nothing changes until you restart." Primary "Download". With Automatic Downloads on and the computer on battery, the text adds "It downloads by itself when the computer is plugged in." Badge download, `--accent` | Yes (battery variant merges the drawn `waiting`) |
| `downloading` | `bootc-action download` running | "Downloading Update" / "Apex <version>. You can keep working." Progress bar from `--progress-fd` when available, else an indeterminate bar. Button "Cancel" (secondary) | Yes, without Cancel |
| `downloaded` | `staged.downloadOnly` is true | "Restart to Update" / "Apex <version> is downloaded. Your current version stays in place until you restart from here or from the Power Off menu." Secondary "Not Now", primary "Restart Now…" | Yes (drawn as `ready`) |
| `staged` | `staged` exists and `downloadOnly` is false | "Restart to Finish Updating" / "Apex <version> starts the next time the computer restarts." Primary "Restart Now…". Badge restart, `--accent` | Partly (drawn as `ready`) |
| `rollback-pending` | `bootc rollback` ran since the last boot (the bootloader's next entry is the previous deployment; check which status field shows it, `rollbackQueued` is the candidate) | "Restart to Go Back" / "Apex <previous> starts the next time the computer restarts. Apex <current> stays installed." Secondary "Cancel", primary "Restart Now…". Badge restore, `--accent` | No |
| `previous-started` | The booted deployment is older than the bootloader's default entry (the user picked it in the startup menu) | Same title and body as the alert; secondary "Try Again Next Time", primary "Keep This Version…" | Alert only |
| `error` | The last `bootc-action` exited non-zero | "Update Did Not Download" (or "Could Not Check for Updates") / one line from the failure class: no network, the registry refused, the signature did not verify, not enough disk space. Primary "Try Again" | No |

"Restart Now…" opens GNOME's restart confirmation dialog. In `downloaded`
it runs `bootc-action apply` first. No path reboots without the dialog.
"Not Now" only closes the hero's urgency for this session and changes
nothing in bootc.

The panel shows a `--warn` note in `available` and `downloaded` when the
offered digest equals the deployment the user went back from: "This is the
version you went back from." This replaces the drawn rejected-build promise.
It is computed from status and stores nothing.

Transitions:

| From | Event | To | Command |
| --- | --- | --- | --- |
| any idle state | Check Now, or the panel opens and the last check is older than 1 hour | `checking` | `bootc-action check` |
| `checking` | Nothing newer | `up-to-date` | |
| `checking` | Newer digest | `available` | |
| `checking` | Failure | `error` | |
| `available` | Download, or the timer runs on mains power | `downloading` | `bootc-action download` |
| `downloading` | Pull and signature policy pass | `downloaded` | |
| `downloading` | Cancel | `available` | Terminate the `bootc` process; cached layers stay |
| `downloading` | Failure, including a signature the policy rejects | `error` | |
| `downloaded` | Restart Now…, confirmed | reboot into the new build | `bootc-action apply`, then the session restarts |
| `downloaded` | Power Off or Restart with the switch on | reboot or power off, the new build boots next | `bootc-action apply` |
| `downloaded` | Power Off or Restart with the switch off, or any other reboot | the old build boots; bootc discards the staged update; the next check finds it again and the timer re-stages it from cache | none |
| `staged` | any restart | the new build boots | ostree finalises at shutdown |
| `up-to-date`, `available`, `downloaded`, `staged` | Use at Next Restart…, authenticated | `rollback-pending`; a staged update is discarded | `bootc-action rollback` |
| `rollback-pending` | Cancel, authenticated | the state before (without the discarded staged update) | `bootc-action rollback` again; must be verified to restore the order |
| boot | The new build fails to start; the user restarts and picks the previous entry in the startup menu | `previous-started` | none |
| `previous-started` | Keep This Version…, authenticated | `up-to-date` or `available` on the older build | Make the booted deployment the default. The command must be verified: `bootc rollback` is the candidate (OQ-36) |
| `previous-started` | Try Again Next Time, or dismiss | unchanged; the next boot uses the newer build | none |

### States a real build needs and the artboards do not draw

`checking`, `error`, `downloading` with Cancel, `staged` without the switch,
`rollback-pending`, `previous-started` in the panel, the first boot after
install (no Previous), low disk space as an `error` reason, and the "version
you went back from" note. Each needs a drawing before M3 sign-off, or the
owner accepts this spec's copy and the drawn metrics as enough.

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour | `--win`, `--side`, `--fg`, `--dim`, `--border`, `--card`, `--card-border`, `--btn`, `--btn-h`, `--accent`, `--accent-strong`, `--warn`, `--warn-bg`, `--panel`, `--panel-solid`, `--panel-border`, `--shadow`, `--wall`. Literal: badge `#3a944a` (Green accent, not `--ok`) |
| Type | `typography.family.ui`, `family.mono` (versions and digests); sizes 11.5, 12, 12.5, 13, 13.5, 14, 20; weights 600, 700, 800; tabular numbers on progress |
| Radius | `sm` 8, `md` 10, `pill-bar` 12, `window` 14, `lg` 16, `card-lg` 18 (hero pills), `toast` 20 (hero tile); literal 3 (progress) |
| Shadow | `window`, `card`, `knob`, `lifted`, `panel`; badge ring `0 0 0 3px var(--card)` |
| Glass | Alert: Quick Settings / toast row (30 px, 180 %), solid fallback first (OQ-03) |
| Motion | switch `duration.base` with `easing.standard` |

Token conflict: `--warn-bg` is `rgba(200,136,0,.12)` / `.16` in
`Updates.dc.html:18-19` and `.14` / `.2` in `Rollback.dc.html:18-19`
(recorded in `tokens.json`).

## Build classification

| Element | Class | Why |
| --- | --- | --- |
| Updates and rollback | Stock | `bootc upgrade`, `bootc rollback` |
| Disabling `bootc-fetch-apply-updates.timer` | Theme (image config) | A preset in `apex-image` |
| `apex-update-download.timer` and service | Theme (image config) | Two systemd units calling stock bootc |
| `apex-bootc-status.service` | Theme (image config) | A oneshot wanted by a stock bootc target; skip if `bootc status` works without root |
| `bootc-action` helper and its polkit policy | Patch (new, small) | About 40 lines plus a `.policy` file; no state, no daemon |
| Software Updates subpage | Patch | New page in gnome-control-center, or a separate page if OQ-12 moves it; stock libadwaita widgets |
| Health failure alert | Extension | Posted by the Apex Shell extension from the status file |
| Power Off switch | Patch | `endSessionDialog.js`; see [dialogs.md](dialogs.md). M3 can ship without it: the panel's Restart Now… covers the flow |
| Polkit dialog | Theme | Stock agent; message from the policy file |
| Signature policy | Theme (image config) | `/etc/containers/policy.json` requiring sigstore signatures for `ghcr.io/apex-linux` |

## Accessibility

*   The alert uses `role=alert`; the shell announces it once per boot.
*   The progress bar exposes a progressbar role with its value, and the
    caption as its description. The indeterminate bar announces "Downloading".
*   The hero badge glyph is decorative; the title carries the state.
*   Digests are truncated; expose the full digest as a tooltip and to
    screen readers, and make it selectable.
*   White text on the primary pills uses `--accent-strong`, which passes AA
    for all nine accents; plain `--accent` fails for eight of them at 13 px.
*   Focus order: back, hero buttons, What's New rows, Use at Next Restart…,
    Automatic Downloads, Check Now. In the alert: Dismiss, secondary,
    primary; Escape dismisses.
*   "Did not start" is text, not colour alone.

## Acceptance criteria

1.  `systemctl is-enabled bootc-fetch-apply-updates.timer` reports
    `disabled` or `masked` on a fresh install, and no update path reboots
    or powers off without the user confirming a GNOME dialog.
2.  Each state shows the hero title, text, badge and buttons in the state
    table, and the panel updates without reopening when bootc state changes
    (for example after `sudo bootc upgrade --download-only` in a terminal).
3.  With Automatic Downloads on and mains power, a new build is downloaded
    within one timer period and the panel shows `downloaded`. On battery
    nothing is downloaded and `available` shows the plugged-in sentence.
4.  In `downloaded`, a restart with the Power Off switch off (or
    `systemctl reboot`) boots the old build, and `bootc status` afterwards
    shows no staged deployment. The next download of the same build
    transfers almost nothing (cached layers).
5.  In `downloaded`, Restart Now… confirmed, or the Power Off switch on,
    boots the new build; `bootc status` shows it as `booted` and the old one
    as `rollback`.
6.  With the signature policy installed, pointing the image at an unsigned
    tag makes the download fail, nothing is staged, and the panel shows
    `error` with the signature reason. This also demonstrates the M3 rule
    "the system refuses unsigned images".
7.  Use at Next Restart… raises the polkit dialog; cancelling changes
    nothing; authenticating makes the previous build boot next, discards a
    staged update and does not reboot. After the restart the previous build
    is `booted`.
8.  Cancel in `rollback-pending` restores the original boot order (verify
    that a second `bootc rollback` does this).
9.  **Forced bad update (M3 exit):** an image built to fail before the
    greeter is staged and applied. On the next boot it fails; after a
    restart the startup menu appears without holding a key, the previous
    entry boots, and the alert "You Started the Previous Version" appears
    after login with both version strings.
10. Keep This Version… makes the older build the default: the next restart
    boots it without the menu, and `bootc status` agrees.
11. Try Again Next Time leaves the order unchanged; the next restart boots
    the newer build.
12. After going back, when the panel offers the same digest again it shows
    "This is the version you went back from."
13. Every version, digest and date shown is read from `bootc status`; none
    is hard-coded. Versions use the scheme decided in OQ-08.
14. Nothing named `apexctl`, "Apex Updates" or "Updates Ready" appears in
    the image.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

*   **Q-UPD-1** Version scheme `45.YYYYMMDD.NNN` (for example
    `45.20261008.131`). bootc shows the image's `version` field, so
    `apex-image` decides it at build time. Is the date UTC? What happens at
    a Fedora major rebase? Old-spec until confirmed.
*   **Q-UPD-2** Polkit ids: this spec proposes
    `io.github.apex_linux.Updates.{check,download,apply,rollback}`. Confirm
    the prefix (OQ-08) and the per-verb defaults in the
    [architecture table](#architecture-without-a-daemon).
*   **Q-UPD-3** Answered 2026-11-17: stock bootc.
*   **Q-UPD-4** Answered by stock behaviour: a download-only update is
    discarded at reboot unless applied, so "Not Now" and the Power Off switch
    turned off skip one restart, and the update comes back from cache.
    `systemctl reboot` does not apply a download-only update; it does apply a
    plain staged one.
*   **Q-UPD-5** Cut with the hold note.
*   **Q-UPD-6** Moot for M3 (no package list). Returns with OQ-37.
*   **Q-UPD-7** The undrawn states are now specified in this file. Does the
    owner want them drawn before M3 sign-off?
*   **Q-UPD-8** Moot: no update banner in M3.
*   **Q-UPD-9** Update Channel shows the image tag. Switching channels
    (`bootc switch`) is out of M3. Rolling `main` versus tagged releases is
    an `apex-image` decision.
*   **Q-UPD-10** Sample data in the artboards ("apex@fedora", "fc45", GNOME
    51, Linux 7.2, Mesa 26.1). The waiting copy said "The laptop"; this spec
    uses "the computer".
*   **Q-UPD-11** Digest truncation: this spec uses 4 + 4 everywhere.
*   **Q-UPD-12** Moot: the banner is cut; only the alert's metrics remain.
*   **Q-UPD-13** The alert's sender is now "Software Updates" with the warning
    tile; the Power Off row needs an icon only if OQ-09 keeps GNOME Software
    out of the image.
*   **Q-UPD-14** Verification still needed on the reference machine: the
    Fedora 45 bootc version supports `--download-only` and
    `--from-downloaded`; `--check` fills `cachedUpdate` (otherwise parse the
    check's exit and output); whether `bootc status` needs root; which status
    field marks a queued rollback and a manually chosen older boot; that
    Fedora's GRUB shows the menu after a failed boot of a bootc deployment;
    the command for Keep This Version. See OQ-36.
