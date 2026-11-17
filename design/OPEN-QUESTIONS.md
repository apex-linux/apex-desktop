# Open questions

Decisions the owner needs to make before or while engineering builds from the
canvas. Each question has a global ID (`OQ-nn`). The handoff specs raised
most of them under local IDs (for example `BOOT-3` or `Q-UPD-4`); the
"Spec refs" line maps each global ID to those local IDs, so a spec's own
question list stays valid.

Two sources outside the canvas already answer part of this list. Read the
[status table](#status-against-the-binding-spec-and-legacy-decisions) first:

*   The binding product spec, `apex/docs/spec.md` in the workspace
    (architecture, reference machine, milestones M0 to M4).
*   The old attempt's `docs/DESIGN.md` (bare mirror `.legacy/apex.git`,
    adopted 2026-10-23, edited to 2026-11-04). It records dated owner decisions
    about the same canvas. The old attempt was torn down for poor quality, so
    these decisions are not binding until the owner confirms them, but most
    of them are only a "yes, carry it over" away.

## Contents

*   [Status against the binding spec and legacy decisions](#status-against-the-binding-spec-and-legacy-decisions)
*   [How this list is ranked](#how-this-list-is-ranked)
*   [Tier 1: blocks engineering from starting](#tier-1-blocks-engineering-from-starting)
*   [Tier 2: blocks one surface](#tier-2-blocks-one-surface)
*   [Tier 3: consistency the design owner can settle](#tier-3-consistency-the-design-owner-can-settle)
*   [Tier 4: sample and old-spec text](#tier-4-sample-and-old-spec-text)
*   [Local ID map](#local-id-map)
*   [Not drawn: gaps a distribution needs](#not-drawn-gaps-a-distribution-needs)

## Status against the binding spec and legacy decisions

"Answered" means `apex/docs/spec.md` decides it. "Legacy" means the old
`DESIGN.md` records an owner decision; the owner only needs to confirm it
carries over. "Open" means neither source answers it.

| ID | Status | What the sources say |
| --- | --- | --- |
| OQ-01 | Answered | Fedora `bootc` base image, currently Fedora 45; one OCI image installs and updates. |
| OQ-02 | Partly answered | Spec non-goal: "Theming and extensions come first; a patch to an upstream component needs a reason an extension cannot satisfy." The legacy attempt carried a large GNOME patch series (`apex-gnome`, shell patches 0001 to 0016); the new rule means each spec's "patch" rows need that reason or a cut. | The update hold ("Held for up to 14 days") is cut with OQ-04.
| OQ-03 | Legacy, partly | Glass on shell surfaces only, text-heavy modal dialogs solid; Reduce Transparency swaps to solid tokens; re-blur only when the redraw clip covers the box. The budget lived in legacy ADR 0014 and `0003-blur.patch`, which the new patch rule puts in question. |
| OQ-04 | Answered 2026-11-17 | Owner: "Chỉ bootc gốc", stock `bootc` only, confirming the spec. Holds, the rejected-build list, the three-boot fallback, greenboot checks, `apexctl` and the "Apex Updates" notifications are cut; download-only staging, rollback and signed images stay. Residual checks are OQ-36 and OQ-37. |
| OQ-05 | Answered | Spec goal 1: hardware support "by component ... never by one machine's profile"; the M7400QC is "the first acceptance target, not the only one". Its 80 % charge limit is a required check. |
| OQ-06 | Partly answered | The iGPU drives the desktop; the NVIDIA driver ships "as prebuilt modules in an image flavor". Still open: early KMS (`amdgpu` in the initramfs) and the Secure Boot plan (spec: off for now). |
| OQ-07 | Partly answered | `.legacy/apex.git` keeps `docs/DESIGN.md`, `docs/ARCHITECTURE.md`, `docs/ROADMAP.md` and ADRs including 0014. `DESIGN.md` says it "replaces `design/SPEC.md`", so the SPEC.md the canvas quotes is gone; its radius and performance sections are not recoverable from the mirrors. |
| OQ-08 | Partly answered | Org and image: `apex-linux`, `ghcr.io/apex-linux/apex`. Legacy schema `io.github.apex_linux.Apex.Desktop` (underscore). Version scheme still open. |
| OQ-09 | Legacy, conflicts with canvas | Legacy: favourites Files, Web, Calendar, Music, Text Editor, Terminal, Software, Settings ("no Mail, decision 10"), then running apps, separator, Show Apps, Trash; Hide Behind Maximized Windows with a bottom-edge barrier; primary monitor only; keep "Launch Using Discrete Graphics Card". The canvas pins Bazaar where legacy pins Software. |
| OQ-10 | Legacy | Super+Space opens Spotlight; input sources move to Super+Alt+Space (English and Vietnamese Telex); Super+A opens the launcher; Ctrl+Space stays free. |
| OQ-11 | Legacy; milestone M4 | One Spotlight engine behind Super+Space, the bar button, the overview pill and typing in the overview; sections Calculator 1, Applications 4, Settings 3, Files 4; 1 s per provider. Spec schedules Spotlight in M4. |
| OQ-12 | Legacy | Apex Desktop is the first Settings panel; stock panels gain no rows except Power's "Graphics and Display"; stock Power rows stay. The new patch rule decides whether a Settings patch is acceptable at all. |
| OQ-13 | Legacy; milestone M4 | Disk footer, item-count bar, recent strip (four items), details pane as an overlay split view, search chips, accent folders through nine `Apex-<accent>` themes. |
| OQ-14 | Legacy; milestone M4 | Ptyxis with an Apex patch series; sessions sidebar grouped by host, container or ssh; two-pane split; "needs you" = bell or notification while unfocused. |
| OQ-15 | Open | Neither source decides whether an AI agent ships. |
| OQ-16 | Legacy | "App icons are full-colour Colloid, from a pinned upstream commit." Provenance of the 11 C2PA-marked files is still open. |
| OQ-17 | Legacy, partly | Apex Symbolic drawn in-house ("decision 11 resolved 2026-10-23"); "larger renders keep the same pixel weight". Source of truth after extraction is open. |
| OQ-18 | Legacy | App chrome keeps libadwaita's colours, metrics and shadows (decision 4); only the window radius changes (decision 5, 0 / 8 / 14 / 20 via a generated `gtk.css`). Type: Adwaita Sans with `ss03` through fontconfig at 13.5 px, hinting off; the canvas's Inter + `cv05` is "the same design". |
| OQ-19 | Legacy, partly | Lock is single-stage, clock and prompt together (decision 7); greeter keeps the stock layout over a pre-blurred image; GRUB hidden unless the previous boot failed (decision 17); Plymouth script theme with a two-step fallback. Guest, polkit fingerprint and TPM2 stay open. |
| OQ-20 | Legacy | Toggles: Wi-Fi, Bluetooth, Power Mode, Night Light, Dark Style, Do Not Disturb, Airplane Mode, VPN; Restart and Power Off confirm. |
| OQ-21 | Partly; updates part answered by OQ-04 | No update banner in M3; the only update notification is the "You Started the Previous Version" alert, posted by the Apex Shell extension from stock bootc state (owner to confirm). Dock menu bookmarks, OSD value and screenshot window mode are open. |
| OQ-22 | Open | Builder delivery and scope. Spec schedules Apex Code in M4. |
| OQ-23 | Legacy | Welcome is "not scheduled" in legacy; the spec puts it in M3. | The rollback sentence on page 1 must change: nothing goes back by itself under OQ-04.
| OQ-24 | Legacy | Owner rule: when a board value fails contrast, the token changes; dim text in light is .72, not .62. |
| OQ-31 | Legacy | Small white text sits on the accent mixed 25 % toward black, so all nine accents reach 4.5:1; the clock's unread dot uses the bar foreground, not the accent (owner, 2026-11-04); selection tint is the accent at 16 %. |
| OQ-36 | Open, new 2026-11-17 | Stock bootc behaviours the update spec depends on but the docs do not state; to verify on the reference machine. |
| OQ-37 | Open, new 2026-11-17 | Whether What's New lists packages again, which needs `apex-image` CI to publish a package diff. |
| Others | Open | Tier 3 items not listed here have no recorded answer. |

Milestones from the spec also change how much each tier blocks: boot, greeter,
lock, shell surfaces, dialogs, icons, wallpapers and themes are M2; Software
Updates, health failure and Welcome are M3; Files, Terminal, Apex Code and
Spotlight are M4.

## How this list is ranked

*   **Tier 1** questions decide architecture, the base system or the patch
    budget. Engineering cannot plan without them.
*   **Tier 2** questions block one surface or one app; other work can go on.
*   **Tier 3** questions are inconsistencies between artboards. The design
    owner proposes an answer for each; the owner only needs to confirm.
*   **Tier 4** is the inventory of text on the canvas that belongs to the old
    single-machine or old-base spec. None of it is a requirement.

Within a tier, questions are in order of how much they block. "Expensive"
marks items that look costly to build faithfully.

## Tier 1: blocks engineering from starting

### OQ-01: Is the base Fedora image-based plus GNOME, and which flavour?

The whole canvas assumes it: GDM, GNOME Shell, Nautilus, GNOME Builder as
"Apex Code", Fedora version strings, `fc45` packages, a bootc or rpm-ostree
style A/B update with rollback. Answered since the canvas was drawn:
`apex/docs/spec.md` fixes the base as the Fedora `bootc` base image, currently
Fedora 45. What remains is how version strings and the greeter footer are
generated (OQ-08).

*   Remaining sub-question: the canvas title "Apex Fedora Mockups" and the
    volume label "Apex Fedora" versus the product name Apex Linux.
*   Blocks: every spec; the update design most of all.
*   Spec refs: `DLG-1`, `DLG-3`, `GL-2`, `Q-UPD-3`.

### OQ-02: How much downstream patching of GNOME is acceptable?

Faithful builds need patches to GNOME Shell (dock, Spotlight, lock flow,
switcher captions, dock menus, OSD value, screenshot window mode, indicator
overflow), GDM, gnome-control-center (two new pages, sidebar changes),
Nautilus (Home dashboard, details pane, filter chips, status bar), Ptyxis
(session sidebar, states, splits) and GNOME Builder (agent panel). Each patch
must be rebased on every GNOME release. The Updates artboard planned for
this with a per-package hold ("Settings 51.1 is held back ... Held for up to
14 days, then Apex ships the stock 51.1"). Stock bootc updates the image as
a whole and has no hold, so the hold is cut (OQ-04, 2026-11-17): a GNOME
release that breaks an Apex patch must be fixed before the image is
published, or the image is not published.

*   Proposal: the owner sets a patch budget per component; each spec's
    "Build classification" table lists stock, theme and patch items so the
    owner can cut by row.
*   Blocks: scope of every shell and app spec.
*   Spec refs: `Q-SET-1`; every spec's build classification. (`Q-UPD-5` is
    cut with the hold.)

### OQ-03: Is live glass with saturation in scope, and what is its budget? (expensive)

The canvas makes translucency first-class: top bar, dock, Quick Settings,
calendar, banners, OSD, switcher, screenshot panel and Spotlight all blur
what is behind them with extra saturation. Stock GNOME Shell blurs only the
lock screen and overview background, and `Shell.BlurEffect` has no
saturation; the canvas's own notes call for "patch 0003" to add it.

*   Cost: live blur re-renders on every change behind the surface; at scale 2
    on the Radeon iGPU with the NVIDIA GPU asleep, radii reach 96 to 160
    device px. The SPEC excerpt refers to a performance acceptance
    ("section 7") that is not on the canvas.
*   Conflicts to settle at the same time: the SPEC glass table says overview
    36 px / 150 % and launcher 40 px / 160 %, the artboards draw 40 px /
    140 % for both; the tile preview blurs (20 px / 160 %) though the table
    does not list it.
*   Proposal: build every glass surface with a solid fallback
    (`--panel-solid`, `--bar-solid`) first, behind one switch; add live blur
    per surface only after it meets a measured frame-time budget.
*   Blocks: shell theming, the lock screen, the greeter.
*   Spec refs: `GL-9`; glass sections of all `shell-*.md` specs.

### OQ-04: How do updates work end to end?

**Answered 2026-11-17.** The owner chose stock `bootc` only ("Chỉ bootc
gốc"), confirming `apex/docs/spec.md`: no custom update daemon, and the
Settings panel is a front end to `bootc upgrade`, `bootc rollback` and
`bootc status`.

The canvas promised updates "that never surprise you" with an `Update1`
daemon. Checked against the bootc documentation (sources in
[updates-and-rollback.md](handoff/updates-and-rollback.md#what-stock-bootc-provides-and-what-is-cut)):

*   **Kept, stock:** background download that is not used at the next boot
    (`bootc upgrade --download-only`, then `--from-downloaded`); applying at
    a restart the user confirms; going back (`bootc rollback`); signed
    images through `/etc/containers/policy.json`.
*   **Kept, with image config only:** Automatic Downloads on mains power
    (an Apex timer running `bootc upgrade --download-only` with
    `ConditionACPower=true`); the stock `bootc-fetch-apply-updates.timer`
    is disabled because it reboots.
*   **Cut:** the per-package hold; the metered-network wait; the
    three-boot automatic fallback and the "startup check" (bootc has no
    boot counting or health checks); the rejected-build list; the package
    list in What's New (OQ-37); the "Updates Ready" banner and the "Apex
    Updates" sender; `apexctl`.
*   **Replaced:** the health failure flow becomes "You Started the Previous
    Version": the user picks the previous entry in the startup menu after a
    failed boot, and the session offers to keep that version.

Answers to the old sub-questions: there is no shared D-Bus service; clients
read `bootc status` (through a status file if it needs root) and call a
stateless `pkexec` helper. "Not Now" and the Power Off switch turned off
skip one restart: stock bootc discards a download-only update at boot and
stages it again from cache. A plain `systemctl reboot` applies a staged
update but not a download-only one. The polkit actions are
`io.github.apex_linux.Updates.{check,download,apply,rollback}` (naming per
OQ-08).

*   Still open: OQ-36 (behaviours to verify on the machine), OQ-37
    (package list), and whether the alert is posted by the Shell extension
    (OQ-21).
*   Spec refs: `DLG-1`, `Q-UPD-3`, `Q-UPD-4`, `Q-UPD-7`, `Q-UPD-8`,
    `Q-UPD-9` (all answered or moot; see the spec).

### OQ-05: How does machine-specific design become conditional?

The canvas was drawn for one machine, the owner's ASUS Vivobook Pro 14X OLED
(M7400QC: 2880x1800 90 Hz OLED at scale 2, RTX 3050, ELAN reader). Apex now
targets many machines and must still fully support this one. Several
surfaces show this laptop's features as if every machine had them:

*   Welcome: "made for the Vivobook Pro 14X OLED", "Sharp on the OLED",
    "Tuned for this laptop".
*   Settings > Power: 80 % charge limit, NVIDIA power-down row, 60 / 90 Hz
    refresh on battery.
*   Boot: assets drawn only at scale 2.
*   Fingerprint prompts on greeter, lock and polkit.

Proposal (already written into the specs): every such item shows only when
the hardware and backend are detected (UPower charge threshold, switcheroo
and runtime PM, Mutter display modes, fprintd with an enrolled finger), and
the copy is machine-neutral. The owner needs to confirm this rule and name
the other machines Apex is tested on, and the scales to support.

*   Spec refs: `BOOT-1`, `GL-7`, `Q-SET-3`, `Q-UPD-10`; welcome questions
    3 and 5; settings "hardware-dependent rows".

### OQ-06: Which NVIDIA driver, and which GPU drives the panel at boot?

Proprietary driver (akmods, Secure Boot signing, image build cost) or
nouveau / NVK. The Power panel's "Powered down until an app asks for it" row
depends on runtime power management working with the chosen driver. Plymouth
needs `amdgpu` in the initramfs for early KMS, or the splash starts on
`simpledrm` and flickers. The dock menu item "Launch using Discrete Graphics
Card" is not drawn; the design owner recommends keeping it on dual-GPU
machines.

*   Spec refs: `BOOT-3`, `Q-SET-3`.

### OQ-07: Which project artefacts from the old canvas still hold?

The canvas quotes documents and decisions from the previous attempt that do
not exist in the new workspace: SPEC.md (sections 2.6 Glass, 2.7 Radii, 4,
7), ARCHITECTURE "answer 10" (no Tour, Firefox on request), "decision 14",
ADR 0014 (`ApexDock`), "patch 0003", a roadmap stage "S2a", an issue
"apex-desktop#38", and an icon "scan" tool (`check-icons`). The specs treat
their content as intent, not requirement.

*   Ask: should these be recovered from the old organisation before it is torn
    down, or re-decided here? At least SPEC.md section 2.7 (radii) and
    section 7 (performance) would remove guesswork.
*   Spec refs: `apex-symbolic.md` question 2; `shell-top-bar-and-dock.md`
    question 1.

### OQ-08: What are the product's identifiers and version scheme?

*   Reverse-DNS prefix: the canvas uses both `io.github.apex-linux` (polkit
    action `io.github.apex-linux.apex.update.rollback`, which the update
    spec now replaces with `io.github.apex_linux.Updates.rollback`) and
    `io.github.apex_linux` (GSettings schema). D-Bus and GSettings names
    cannot contain hyphens, so `io.github.apex_linux` is the safe choice for
    all of them.
*   Version scheme `45.YYYYMMDD.NNN` ties the version to the Fedora major and
    uses a global build counter; what happens at a rebase?
*   App ids: Apex Code keeps `org.gnome.Builder`; the welcome app needs one.
*   Spec refs: `Q-UPD-1`, `Q-UPD-2`, `DLG-3`, `Q-SET-6`.

## Tier 2: blocks one surface

### OQ-09: Dock: which implementation, which apps, which hide rule?

*   Route: fork Dash to Dock, or build `ApexDock`, a subclass of the shell's
    `Dash` (the roadmap text drawn in `Desktop.dc.html`). This decides most of
    the dock's cost.
*   Hide rule: "Hide Behind Maximized Windows" only, or full intellihide? The
    Tiling artboard draws no dock with two unmaximised tiled windows.
    Reveal timings and pressure threshold are not drawn.
*   Contents: 23 artboards pin Files, Web, Calendar, Music, Text Editor,
    Terminal, Bazaar, Settings; Settings > Apex Desktop previews Files, Web,
    Mail, Calendar, Music, Text Editor, Terminal, Software, Settings.
    `Desktop.dc.html` adds Image Viewer, probably running but not pinned,
    with no pinned/running separator. Is GNOME Software shipped at all? Its
    icon was reused for "Apex Updates", which OQ-04 cut; the Power Off
    update row still uses it.
*   Default browser: GNOME Web is pinned; a canvas note says "Firefox on
    request".
*   Spec refs: `Q-SET-2`, `Q-UPD-13`; `shell-top-bar-and-dock.md`
    questions 1 to 4; `shell-overview-launcher-spotlight.md` question 12.

### OQ-10: Which keybindings change from GNOME's defaults?

The Launcher and Welcome copy give Super+Space to Spotlight and
Super+Alt+Space to input sources. Super+Space is GNOME's input-source
shortcut, and the top bar draws a Vietnamese (Telex) input source. The owner
types Vietnamese, so this affects daily use.

*   Spec refs: `shell-overview-launcher-spotlight.md` question 1; welcome
    question 4.

### OQ-11: Spotlight: new surface or overview search? (expensive)

Spotlight is a centred search dialog that GNOME does not have (the design
owner estimates 1000+ lines as a shell patch or extension). Does overview
"Type to search" stay as stock full results, or hand off to Spotlight? Which
search providers map to which section, and does the calculator use GNOME
Calculator's provider or run in the shell?

*   Spec refs: `shell-overview-launcher-spotlight.md` questions 2, 4, 5.

### OQ-12: Where do the Apex Desktop and Software Updates pages live?

A gnome-control-center patch (as drawn: first rows of the Settings sidebar),
extension preferences, or a separate app. Tied to OQ-02. (The 14-day hold
that tied it to Settings releases is cut with OQ-04.)
Also: Apex Desktop's "Corner Radius" for all windows needs a compositor-side
clip for every toolkit (expensive), and "Lower Refresh Rate on Battery" needs
a new daemon that must not fight the Displays panel.

*   Spec refs: `Q-SET-1`, `Q-SET-4`, `Q-SET-5`, `Q-SET-12`.

### OQ-13: How much of the Files redesign is in scope? (expensive)

The Home dashboard (Recent cards above the folder grid in one scroll), the
details pane, filter chips with counts, the persistent status bar and the
sidebar storage summary are all Nautilus patches; the dashboard is the
hardest because `GtkGridView` owns its scrolling. Accent-coloured folder
icons need nine generated icon variants or a Nautilus patch.

*   Spec refs: `files.md` questions 1, 2, 9, 10.

### OQ-14: Terminal: Ptyxis fork, Console or a new app? Are splits required? (expensive)

Ptyxis has no session sidebar, no session state model and no split panes.
Splits are the single most expensive terminal feature. Session persistence
and SSH grouping are also undefined. The default shell is drawn as `zsh`;
Fedora defaults to bash.

*   Spec refs: `terminal.md` questions 1, 2, 4, 7, 9, 10.

### OQ-15: Is an AI coding agent part of the product?

The Terminal artboards show a third-party CLI agent ("claude") asking for
permission inline, with a "needs you" session state; Apex Code shows an agent
panel. If the agent ships, who owns its installation, updates and terms, and
is it opt-in? If not, the "needs you" state still works for any program that
rings the bell.

The Apex Code agent panel is a new Agent Client Protocol (ACP) client plugin
for GNOME Builder; the design owner estimates two engineers for 8 to 12 weeks,
then ongoing upkeep against ACP and Builder changes. It names a third-party
product ("Claude Code") in the UI. (expensive)

*   Spec refs: `terminal.md` question 3; `AC-1`.

### OQ-16: App icons: Colloid, and how is the icon theme chained?

The canvas says "App icons stay Colloid": the app icons are the third-party
Colloid icon theme (GPL-3.0), not Apex originals, and the 36 SVGs on the
canvas were uploaded by a co-writer and must be sanitised before shipping.
Three of them are referenced by no artboard. The Apex Symbolic theme must
coexist with Colloid; the design owner recommends `Apex -> Adwaita ->
hicolor` with Colloid's full-colour icons merged at build time and its
symbolic icons dropped, so Colloid's symbolics never win over Apex's.

*   Provenance: 11 of the 36 SVGs carry a C2PA manifest saying an AI tool may
    have created or modified them. Diff every icon against a pinned Colloid
    commit before shipping, and decide whether shipped files keep the
    manifests.
*   Sub-questions: confirm Colloid (licence, tracking upstream); what the
    three unreferenced icons are and which app "Mail" is; whether the Apex
    Code tile and folders follow the accent (Colloid's hues are not GNOME's
    nine accents); whether icons keep their stripped drop shadows.
*   Spec refs: `apex-symbolic.md` question 1; `AW-1` to `AW-8`.

### OQ-17: Apex Symbolic: what is the source of truth, and are the collapsed families intended?

*   After extraction, do master SVGs in the repository replace the canvas
    sheets as the source? (Strokes must become filled outlines at build time
    because GTK recolours fills only.)
*   Several state families are drawn as one picture (all ten battery charging
    levels, wired-network states, microphone levels, Wi-Fi good and
    excellent). Intended, or unfinished?
*   Names that are not upstream names (`go-next-arrow`, `apex-desktop`,
    `system-rollback`, `selection-area`, `briefcase`, `globe`) need aliases or
    code changes. Names likely requested at runtime are not drawn.
*   Optical sizes: other artboards draw these glyphs at strokes from 0.95 to
    2.25. Shipping that is a second set of drawings (expensive).
*   Spec refs: `apex-symbolic.md` questions 2 to 10.

### OQ-18: How do app colours and fonts reach GTK apps?

libadwaita has no theme API. Apex's app colours (`--win`, `--view`,
`--side` and so on differ slightly from Adwaita) need a libadwaita patch, a
GTK style sheet, or acceptance of stock Adwaita colours with only the shell
themed. Also: ship Inter, or rely on Adwaita Sans (derived from Inter); and
confirm `cv05`, `ss03` and tabular figures render in both GTK and St.

*   Spec refs: `system/README.md`, "Mapping to GNOME".

### OQ-19: Sign-in, lock and authentication flows

*   Lock: clock and password prompt together as drawn (patch to
    `unlockDialog.js`), or stock clock first with notifications?
*   Greeter: guest account (GDM has none); power menu, session chooser,
    accessibility menu, "Not listed?" username entry, error, single-user and
    no-user states are not drawn.
*   Polkit: the artboard offers password and fingerprint at the same time.
    One PAM conversation runs them in sequence; parallel needs PAM and agent
    work plus a security review (expensive). Accept stock sequential?
*   Disk unlock: which disk is named when several ask, Caps Lock and layout
    indicators, translations inside the initramfs, TPM2 unlock.
*   Spec refs: `GL-1`, `GL-3`, `GL-4`, `GL-5`, `DLG-2`, `DLG-4`, `BOOT-2`,
    `BOOT-6`, `BOOT-7`, `BOOT-9`.

### OQ-20: Quick Settings main view

The Wi-Fi submenu artboard also draws the main view behind it (Wi-Fi,
Bluetooth, Power Mode, Night Light, Dark Style, Do Not Disturb, sliders,
buttons). Open: Airplane Mode (the AX200 has both radios), a keyboard
backlight toggle, whether Bluetooth and Power Mode keep their stock submenus,
and whether the target Shell has a stock Do Not Disturb tile.

*   Spec refs: `shell-quick-settings-and-screenshot.md` question 1.

### OQ-21: Notifications, OSD and dock menus

*   Update notifications, answered by OQ-04 (2026-11-17): the "Updates
    Ready" banner and the calendar's "Settings / Update ready" are both cut.
    The one update notification left is the "You Started the Previous
    Version" alert, sender "Software Updates". Open: may the Apex Shell
    extension post it, or does it appear only in the Settings panel?
*   "Restart Now" opens GNOME's restart dialog and never restarts directly
    (settled in the update spec).
*   Dock menu bookmarks for Files and a window count instead of the window
    list are patches. The OSD numeric value is a patch.
*   Screenshot window mode outlines windows in place (patch, expensive)
    instead of stock's grid; the screencast mark is a red rounded square,
    which reads as "stop".
*   Spec refs: `shell-calendar-notifications-osd.md` questions 2 to 5, 8;
    `shell-quick-settings-and-screenshot.md` questions 3 to 5.

### OQ-22: Apex Code: how does Builder ship, and which features are in?

*   Every Builder patch means Apex builds Builder itself: an RPM in the image
    or an Apex Flatpak. Keeping the app id `org.gnome.Builder` collides with
    Flathub's Builder. Where the GtkSourceView style schemes install depends
    on this.
*   Features Builder lacks and that look expensive: code folding (GtkSourceView
    5 has none), "Open 6 results as one buffer", reference-count lenses, a
    version-control pane with commit. Builder already has the minimap,
    completion, debugger panes, global search, project tree and find in
    files, so those are styling only.
*   Spec refs: `AC-2` to `AC-5`, `AC-12`.

### OQ-23: Welcome app

New small libadwaita app or a GNOME Tour fork, its app id, how it is
reopened. Its rollback promise ("If one fails to start, Apex goes back by
itself") does not hold under OQ-04; proposed copy: "If one does not start,
choose the previous version in the startup menu."

*   Spec refs: welcome questions 2, 5, 7.

### OQ-36: Stock bootc behaviours to verify on the reference machine (added 2026-11-17)

The update spec relies on behaviour the bootc docs either state for
upstream only or do not state. The M3 session must check each on the
Fedora 45 image before building the panel on it:

*   The shipped bootc has `--download-only` and `--from-downloaded` (the
    release that added them is not documented; v1.16.10 is likely).
*   `bootc upgrade --check` fills `cachedUpdate` in `bootc status`.
*   Whether `bootc status` works without root.
*   Which status field marks a queued rollback (`rollbackQueued` is the
    candidate) and which shows that the booted deployment is not the
    bootloader's default (after picking it in the menu).
*   Whether a second `bootc rollback` restores the original order (Cancel),
    and which command makes a manually booted older deployment the default
    (Keep This Version).
*   That `bootc upgrade` refuses an unsigned image under a policy that
    requires signatures, and what it prints.
*   That Fedora's GRUB shows the menu after a failed boot of a bootc
    deployment (legacy decision 17 relies on this).
*   Whether Fedora enables `bootc-fetch-apply-updates.timer` by default
    (Fedora's docs could not be read automatically).

A later owner decision, not for M3: whether to add greenboot for boot
counting and health checks. The bootc book says greenboot does not yet
integrate with bootc, while greenboot-rs says it is designed for bootc.

*   Blocks: `updates-and-rollback.md` acceptance criteria 4 and 7 to 10.
*   Spec refs: `Q-UPD-14`.

### OQ-37: Should What's New list packages? (added 2026-11-17)

bootc gives no package diff between images. The drawn summary ("GNOME 51.0
→ 51.1, Linux 7.2.7 → 7.2.9, Mesa 26.1.0 → 26.1.2") and package table need
`apex-image` CI to publish a diff with each build (for example a release
note or an image label). Until then What's New shows the version, build
date and a Release Notes link.

*   Blocks: the What's New group only.
*   Spec refs: `Q-UPD-6`.

## Tier 3: consistency the design owner can settle

These are differences between artboards. Each has a proposed resolution; the
owner only needs to say "agreed" or override. Values and sources are in
`system/tokens.json` (`conflicts`).

| ID | Inconsistency | Proposed resolution |
| --- | --- | --- |
| OQ-24 | `--dim` (light) is `.62` on 20 artboards and `.72` on 11 shell artboards. | Two named tokens: `--dim` `.62` for apps, `--dim-shell` `.72` on glass, where contrast varies with the wallpaper. |
| OQ-25 | `--bar-solid`: `#ebebef` / `#151518` (Desktop) vs `#f3f3f5` / `#121215` (Apex Desktop). | Take Desktop's values; Desktop is the artboard about the bar. |
| OQ-26 | `--panel` is more opaque on the Launcher (`.86` / `.82`); `--head`, `--card`, `--faint` differ on DateMenu, Desktop, Overview, Spotlight. | Majority values everywhere; Launcher folder may keep `.86` as `--panel-strong` if the owner liked it. |
| OQ-27 | Two terminal palettes: `--term-*` (in-scene) vs `--t-*` (Terminal app). The in-scene light green fails AA (3.2:1). Overview swaps prompt and path colours. | Retire `--term-*`; use `--t-*` everywhere; complete the ANSI palette (black, yellow, white and eight brights are proposed in `terminal.md`). |
| OQ-28 | `--warn` and `--warn-bg` differ between Updates, Rollback and Code; `--err` (dark) is `#ff7b7b` or `#ff7b63`; badges use literals; destructive red `#c01c28` has no token. | One status set: `--err` `#c01c28` / `#ff7b7b`, `--warn` `#9c6500` / `#f8c454`, `--warn-bg` `.14` / `.2`; add `--destructive`. (`--destructive` added to `tokens.json` 2026-11-17; the rest still needs the owner's yes.) |
| OQ-29 | Radii: Spotlight 24 vs 26 for other panels; notification card 18 (calendar) vs banner 16; search entry 440 (Overview) vs 400 (Launcher); dialog column gap 18 vs 20. | Panels 26, notification cards 18, search entry 440, gap 18. |
| OQ-30 | Error rings `#ffcfcf` (light lock) vs `#ff8a8a` (dark lock, disk unlock); placeholder opacity .96 vs .62; avatar fill none vs white .22. | One error ring `#ff8a8a` on all wallpaper surfaces; placeholder .62; avatar fill white .22 on both. |
| OQ-31 | Contrast failures: white text on accent fills fails 4.5:1 for every accent but Purple; accent text on `--win` fails for most accents; `--faint` is 2.45:1; greeter footer about 4.2:1; the 2 px focus ring fails 3:1 for Yellow (light) and Purple (dark). | Adopt `--accent-strong` (accent mixed 75 % with black, already on three artboards) for fills under white text and for accent text, following libadwaita's `accent_bg_color` / `accent_color` split; `--faint` only for exempt uses; raise the footer to `--dim`; per-accent focus-ring check in CI. |
| OQ-32 | Copy: three wrong-password strings ("Wrong password. Try again.", "Sorry, that didn’t work. Please try again.", "Wrong passphrase. Try again."); Title Case vs sentence case in shell panels; "colour" vs "color"; "78%" vs "78 %"; package counts disagree; digest truncation 4+4 vs 8+4; "unlock Apex" uses Apex as user and distro. | Follow GNOME HIG (header capitalisation for buttons and titles, sentence case for body); US spelling; locale-formatted percentages; one wrong-secret string pattern; digests 8+4; "unlock the computer". |
| OQ-33 | Inline glyphs on non-icon artboards use strokes from 0.95 to 2.25; 73 sheet glyphs cross the keyline by up to 0.38 px; top-bar previews on sheets 31b and 31c drop dimmed layers. | Every shipped glyph comes from the Apex Symbolic sheets at 1.75; keyline overshoots are fixed during extraction. |
| OQ-34 | Small prototype bugs: Files "Documents" says 5 items but holds 6; Files window controls have no accessible names; Files folder-glyph fallback differs between the three Files artboards; Tiling draws a different Files window (196 px sidebar, fixed blue folders); EndSession and Screenshot JS defaults to dark while the tweak defaults to light; `--card-solid` is referenced but never defined; `--row-h` is defined but never used; Apex Code's find count and search counts do not match its text; "1 warning" has no plural form. | Treat Files.dc.html as the reference; ignore the rest. No owner action needed unless the canvas is updated. |
| OQ-35 | Apex Code: modified lines use `--accent` in the gutter but `--mod` (orange) in the tree, and deletions also use `--mod`; editor line height 21 px vs panel 20 px; Markdown colours differ from Text Editor's `--md-head` / `--md-code`. | `--mod` for modified, `--add` for added, `--err` for deleted; editor 21 px, panels 20 px; one Markdown palette shared by both apps through the style scheme. |

## Tier 4: sample and old-spec text

None of this text is a requirement. Real values come from the system at run
time. Listed so engineering does not copy it and so the canvas can be cleaned
if the owner wants.

| Text | Where | Why it is old-spec or sample |
| --- | --- | --- |
| "Built on Fedora Linux 45 · GNOME" | Greeter footer (`Main.dc.html`) | Hard-coded base and version; base unconfirmed (OQ-01). |
| "Fedora Linux 45 and GNOME 51, made for the Vivobook Pro 14X OLED" | Welcome page 1 | Machine- and release-specific (OQ-05). |
| "Sharp on the OLED", "2880 × 1800 panel runs at 90 Hz and exactly 2× scale" | Welcome | Machine-specific. |
| "Tuned for this laptop", "NVIDIA power saving and an 80 % charge limit" | Welcome | Machine-specific. |
| "English ↔ Vietnamese Telex" | Welcome shortcuts | The owner's input setup, not a default. |
| "Limit Charging to 80 %", "NVIDIA GeForce RTX 3050 Laptop GPU", "60 Hz on battery, 90 Hz when plugged in" | Settings > Power | Hardware-conditional rows (OQ-05). |
| "ELAN fingerprint reader", "Intel Wi‑Fi 6 AX200" | Fingerprint, Quick Settings | Must come from the detected device. |
| "Version 45.20261008.131 · GNOME Shell 51.0 on Wayland · Fedora Linux 45" and every `45.2026…` version, `sha256:` digest, "GNOME 51.1, Linux 7.2.9, Mesa 26.1.2" | Apex Desktop, Updates, Power Off, banner, terminals | Computed values; scheme open (OQ-08). |
| `apex@fedora`, `apex-fedora`, `~/apex-fedora/design`, `fc45`, `fedora-45`, `fedora-bootc 45`, `fedora-toolbox-45`, `gnome-shell-0:51.0-1.fc45.apex18` | Terminals, Files, Apex Code | Sample session content. |
| "Apex Fedora" (volume label), "588 GB free of 1 TB", "Apex Fedora — Spec.odt", "mockup-2880x1800.png", "Fedora-Workstation-Live-45.iso" | Files, Tiling | Sample data; the volume name is open (OQ-08). |
| "Fedora 45 go/no-go", "Fedora 45 release", "S1b starts", "Canvas boards 34 to 36", "just vm-image … apex-image" | Calendar | Sample events and notifications. |
| "2880 / 1.5" | Spotlight calculator example | Echo of the old panel spec. |
| `io.github.apex-linux.apex.update.rollback` | Polkit Details | Replaced by `io.github.apex_linux.Updates.rollback` (OQ-04, OQ-08). |
| SPEC.md excerpt, roadmap "S2a", ADR 0014 | Window switcher and Desktop editor content | Old project documents (OQ-07). |

## Local ID map

The specs use local IDs. This table maps the numbered ones; specs without
numbered IDs refer to their questions by position and are cited above as
"`spec.md` question n".

| Local IDs | Global |
| --- | --- |
| `BOOT-1` | OQ-05 |
| `BOOT-2`, `BOOT-6`, `BOOT-7`, `BOOT-9` | OQ-19 |
| `BOOT-3` | OQ-06 |
| `BOOT-4`, `BOOT-5`, `BOOT-8` | Gaps, item 2 |
| `GL-1`, `GL-3`, `GL-4`, `GL-5` | OQ-19 |
| `GL-2` | OQ-01, Tier 4 |
| `GL-6`, `GL-8` | OQ-30 |
| `GL-7` | OQ-05 |
| `GL-9` | OQ-03 |
| `DLG-1` | OQ-01, OQ-04 |
| `DLG-2`, `DLG-4` | OQ-19 |
| `DLG-3` | OQ-08 |
| `DLG-5` | Gaps, item 4 |
| `DLG-6` | OQ-29 |
| `DLG-7` | OQ-28 |
| `Q-SET-1`, `Q-SET-4`, `Q-SET-5`, `Q-SET-12` | OQ-12 |
| `Q-SET-2` | OQ-09 |
| `Q-SET-3` | OQ-05, OQ-06 |
| `Q-SET-6` | OQ-08 |
| `Q-SET-7`, `Q-SET-10` | OQ-12 (Settings layout follows upstream unless the owner says otherwise) |
| `Q-SET-8`, `Q-SET-9`, `Q-SET-11` | OQ-32 |
| `Q-UPD-1`, `Q-UPD-2` | OQ-08 |
| `Q-UPD-3`, `Q-UPD-4`, `Q-UPD-7`, `Q-UPD-8`, `Q-UPD-9` | OQ-04 (answered) |
| `Q-UPD-14` | OQ-36 |
| `Q-UPD-5` | Cut (OQ-04) |
| `Q-UPD-6` | OQ-37 |
| `Q-UPD-11` | OQ-32 |
| `Q-UPD-10` | OQ-05, Tier 4 |
| `Q-UPD-12`, `Q-UPD-13` | OQ-21, OQ-09 (mostly moot after OQ-04) |
| `AC-1` | OQ-15 |
| `AC-2` to `AC-5`, `AC-12` | OQ-22 |
| `AC-6`, `AC-7`, `AC-9` | OQ-35 |
| `AC-8` | OQ-28 |
| `AC-10` | Tier 4 |
| `AC-11`, `AC-13` | OQ-34 |
| `AW-1` to `AW-8` | OQ-16 (`AW-8`: OQ-09) |
| `AW-9` | OQ-07 |

## Not drawn: gaps a distribution needs

Surfaces and states the canvas does not draw. Each needs either a design or a
decision to ship stock GNOME unchanged.

1.  **Installer and first account creation.** No installer (Anaconda WebUI,
    a bootc install flow, or preinstalled images) and no gnome-initial-setup
    pages. Blocks first-boot engineering. Welcome assumes the account exists.
2.  **Firmware and boot loader.** Firmware logo (keep ASUS BGRT or cut to
    black), boot menu visibility, how a user picks the previous deployment,
    "booting previous version", emergency and tries-exhausted states, the
    splash on shutdown and during firmware updates (`BOOT-4`, `BOOT-5`,
    `BOOT-8`).
3.  **Update states:** checking, error, low disk space, rollback pending,
    "You Started the Previous Version" in the panel, and cancelling a
    download. `updates-and-rollback.md` now specifies them in words on the
    drawn metrics (2026-11-17); they still have no drawing (`Q-UPD-7`).
4.  **Power and session:** Restart and Log Out dialogs, low battery,
    inhibitors, other users signed in (`DLG-5`); Power panel without a
    battery or with the dGPU active.
5.  **Fingerprint:** retry, duplicate finger, reader failure; enrolment for a
    second finger.
6.  **Shell:** hover and focus states on most surfaces; per-app window
    switcher (Alt+\`); right-half and keyboard tiling; dock right-click menu,
    pinning and a full Trash; empty last workspace (dynamic workspaces);
    notification grouping; media player card; Wi-Fi connecting, password and
    failure; screen recording in progress; Do Not Disturb side effects.
7.  **Multi-monitor:** bar and dock on every monitor or primary only.
8.  **Accessibility settings:** reduce transparency (needed if glass ships;
    OQ-03), reduce motion, large text, high contrast. Only "Reduce Motion"
    appears, with copy that overstates what `enable-animations` does
    (`Q-SET-12`).
9.  **Dark greeter.** The greeter always uses the light wallpaper.
10. **Other apps the dock pins** (Web, Calendar, Music, Text Editor, Bazaar)
    and the Launcher's apps are not drawn; they ship stock unless the owner
    says otherwise.
