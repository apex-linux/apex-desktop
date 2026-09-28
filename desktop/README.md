# Desktop

The Apex desktop sources ([ADR 0014](../docs/adr/0014-engine-level-desktop.md),
[ARCHITECTURE 7.4](../docs/ARCHITECTURE.md#74-desktop-layer),
[design/SPEC.md](../design/SPEC.md)).

| Directory | Ships in | Licence |
|---|---|---|
| `shell/` | the rebuilt `gnome-shell` package, as `Source1` ([packaging/pkgs/gnome-shell](../packaging/pkgs/gnome-shell/README.md)) | GPL-2.0-or-later, gnome-shell's licence, so any piece can be offered upstream |
| `schemas/` | `apex-desktop` ([packaging/apex-desktop.spec](../packaging/apex-desktop.spec)) | GPL-3.0-or-later |
| `systemd/` | `apex-desktop`: the shell's crash guard, as user units | GPL-3.0-or-later |

S1b adds the icon theme, Plymouth, wallpaper, fontconfig and Ptyxis directories to
`apex-desktop`.

## `shell/`

The lane ([packaging/README.md](../packaging/README.md#the-rebuild-lane)) packs this
directory with `git archive` and unpacks it at the top of Fedora's gnome-shell tree in
`%prep`, with `tar -k`, so a file here can never replace an upstream file.

| Path | What it is |
|---|---|
| `apex.gresource.xml` | the Apex resource: `/org/gnome/shell/ui/apex` (the layer) and `/org/gnome/shell/theme/stock` (upstream's compiled light and dark sheets, the safe-mode sheets). Patch 0001-build compiles it and links it into libshell next to upstream's JS resource. |
| `js/ui/apex/hooks.js` | the only Apex module upstream files import: `safe()`, `value()`, `run()`, and `loadLayer()` for `main.js` |
| `js/ui/apex/layer.js` | the layer: the configure and enable phases, one `try/catch` per feature, the session-mode colour hook, the crash guard's marker file |
| `js/ui/apex/fault/feature.js` | the fault-injection feature: loaded only when `APEX_SHELL_TEST_FAULT` names a phase, it fails in that phase (below) |
| `data/theme/apex/_apex-tokens.scss` | the design tokens as SCSS variables, imported after upstream's `_colors` |
| `data/theme/apex/_apex.scss` | the Apex sheet, imported last by the light and dark entry files |
| `data/theme/apex/_apex-structure.scss` | Apex actors' geometry for the high-contrast sheet |
| `data/theme/apex/meson.build` | adds the partials to upstream's `theme_sources`, so an edit recompiles the sheets |

Rules, which the lane and `.github/scripts/selftest.sh` enforce:

- Every path must be new to upstream and match `source1_paths` in
  [pkg.env](../packaging/pkgs/gnome-shell/pkg.env). That is why this directory has no
  README, licence file, top-level `meson.build` or ESLint configuration: each would
  collide with an upstream file.
- Every file carries `SPDX-License-Identifier: GPL-2.0-or-later` in its first three
  lines.
- A new JS module is one `<file>` line in `apex.gresource.xml`; the lane fails when a
  `js/ui/apex/` module is missing from the built resource.
- An Apex asset is referenced as `url("resource:///org/gnome/shell/theme/apex/<file>")`,
  as upstream does for its own, once `apex.gresource.xml` gains the
  `/org/gnome/shell/theme/apex` prefix (S1b).

### The layer in S1a

The layer is empty: `FEATURES` in `layer.js` lists no feature. It still does what every
later feature relies on:

- In the user and unlock-dialog modes it gives the session mode the colour scheme
  `'prefer-light'`, so GNOME's `'default'` draws a light shell and Dark Style draws a
  dark one. The gdm mode keeps upstream's `'prefer-dark'`.
- `enable()` creates `$XDG_RUNTIME_DIR/apex-shell-starting` and removes it after 60 s
  or at shutdown, for the crash guard (ADR 0014).
- `APEX_SHELL_TEST_FAULT` in the shell's environment adds the `fault` feature after
  every real one, for the safety net's tests (ROADMAP S1a exit). `configure` makes its
  `configure()` throw and `enable` its `enable()`: the feature is off for the session,
  its hook `test-fault` gives the stock value, and the rest of the layer runs.
  `abort-after-enable` aborts the shell (SIGABRT) 5 s after enable, while the crash
  guard's marker exists. Any other value injects nothing. The image never sets the
  variable: G1 fails on it (`image/checks/desktop.sh`).

Kill switches, strongest first: `apex.safe=1` on the kernel command line or
`APEX_SHELL_SAFE=1` in the shell's environment (every session); `layer-enabled=false`
(one user); `disabled-features` (one user, per feature). Safe mode loads no layer (only
`hooks.js` runs, and every hook gives its stock value) and takes the stylesheets from
`/org/gnome/shell/theme/stock/`. The high-contrast sheet has no stock copy, so safe mode
with high contrast uses the rebuilt one, whose Apex part styles only Apex actors.

`tests/layer/run.sh` (`just layer-test`, and ci.yml) runs `hooks.js` and `layer.js` in
gjs outside the shell: every kill switch, `apex.safe=1` through a bubblewrap bind over
`/proc/cmdline`, the gdm mode, the three fault phases, and the crash guard after an
aborted shell.

For the fault injection in the VM, the variable goes into the shell's environment with
a user drop-in on its unit, which the image never ships:

```bash
mkdir -p ~/.config/systemd/user/org.gnome.Shell@.service.d
printf '[Service]\nEnvironment=APEX_SHELL_TEST_FAULT=abort-after-enable\n' \
    >~/.config/systemd/user/org.gnome.Shell@.service.d/90-fault.conf
systemctl --user daemon-reload
# log out and in: the shell aborts 5 s after the layer's enable; the next login is stock
rm ~/.config/systemd/user/org.gnome.Shell@.service.d/90-fault.conf
systemctl --user daemon-reload
gsettings set io.github.sekirokenjii.Apex.Desktop layer-enabled true
```

## `schemas/`

`io.github.sekirokenjii.Apex.Desktop` holds only keys with no upstream home
(SPEC 6.2). S1a ships `layer-enabled` and `disabled-features`; S1b adds the rest and
the `.Keybindings` child.

```bash
gsettings set io.github.sekirokenjii.Apex.Desktop layer-enabled true   # after the crash guard turned it off
gsettings set io.github.sekirokenjii.Apex.Desktop disabled-features "['glass']"
```

## `systemd/`

The crash guard (ADR 0014; ARCHITECTURE 7.4). GNOME's own safety net covers extensions
only, and the Apex layer is compiled into gnome-shell.

| File | Installed as | What it does |
|---|---|---|
| `user/org.gnome.Shell@.service.d/50-apex.conf` | `/usr/lib/systemd/user/org.gnome.Shell@.service.d/50-apex.conf` | adds `OnFailure=apex-shell-safe.service` to GNOME Shell's user unit, next to upstream's `org.gnome.Shell-disable-extensions.service` |
| `user/apex-shell-safe.service` | `/usr/lib/systemd/user/apex-shell-safe.service` | a oneshot with `DefaultDependencies=no`, ordered before `gnome-session-restart-dbus.service` (the same `OnFailure=` list restarts the session bus, and `gsettings` exits 0 when its write is lost), gated on the layer's `%t/apex-shell-starting`: sets `layer-enabled=false`, leaves `$XDG_STATE_HOME/apex/shell-guard-tripped` for `apex-session-agent` (S1b), and removes the layer's file |

A shell that exits with status 1 does not trip it: upstream's unit counts that as
success, and only an error in the static import graph causes it, which G2 catches.
Until the agent offers it (S1b), turn the layer back on with the `gsettings` line
above. The files must not name the shell's dev-loop or fault-injection variables: G1
searches every text file under `/usr` for them.
