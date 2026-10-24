# Desktop

The Apex desktop sources ([ADR 0014](https://github.com/apex-linux/apex/blob/main/docs/adr/0014-engine-level-desktop.md),
[ARCHITECTURE 7.4](https://github.com/apex-linux/apex/blob/main/docs/ARCHITECTURE.md#74-desktop-layer),
[docs/DESIGN.md](https://github.com/apex-linux/apex/blob/main/docs/DESIGN.md)).

| Directory | Ships in | Licence |
|---|---|---|
| `schemas/` | `apex-desktop` ([packaging/apex-desktop.spec](../packaging/apex-desktop.spec)): the Apex schema and the vendor override | GPL-3.0-or-later |
| `keybindings/` | `apex-desktop`: the Apex rows of Settings > Keyboard | GPL-3.0-or-later |
| `wallpapers/` | `apex-desktop`: Apex Facets, rendered to PNG at build | GPL-3.0-or-later |
| `fontconfig/` | `apex-desktop`: `ss03` for Adwaita Sans | GPL-3.0-or-later |
| `dconf/` | `apex-desktop`: defaults no override can express, in dconf's `distro` database | GPL-3.0-or-later |
| `ptyxis/` | `apex-desktop`: the coloured bash prompt, in `/etc/profile.d/` | GPL-3.0-or-later |
| `tmpfiles/` | `apex-desktop`: the global Flatpak override, created at boot when missing | GPL-3.0-or-later |
| `systemd/` | `apex-desktop`: the shell's crash guard, as user units | GPL-3.0-or-later |
| `icons/` | `apex-desktop`: the `Apex` icon theme, with Colloid's app icons fetched at build | GPL-3.0-or-later; Colloid GPL-3.0-only |
| `plymouth/` | `apex-desktop`: the boot splash, the `apex` script theme and its `apex-twostep` fallback | GPL-3.0-or-later |

The Apex layer itself, `desktop/shell/`, ships inside the rebuilt gnome-shell and lives in
[apex-gnome](https://github.com/apex-linux/apex-gnome), with its own
[desktop/README.md](https://github.com/apex-linux/apex-gnome/blob/main/desktop/README.md).

## `schemas/`

`io.github.apex_linux.Apex.Desktop` holds only keys with no upstream home, with the
types and defaults of [docs/DESIGN.md](https://github.com/apex-linux/apex/blob/main/docs/DESIGN.md#settings-contract), and the
`.Keybindings` child with `toggle-spotlight`. A key's reader may land in a later slice:
the schema is the contract.

```bash
gsettings set io.github.apex_linux.Apex.Desktop layer-enabled true   # after the crash guard turned it off
gsettings set io.github.apex_linux.Apex.Desktop disabled-features "['glass']"
gsettings get io.github.apex_linux.Apex.Desktop.Keybindings toggle-spotlight
```

`90_apex.gschema.override` holds the vendor defaults of GNOME's own schemas (DESIGN.md,
"Vendor defaults"), with no locks. It is installed next to the schema and compiled by
the image build, which validates it with `--strict` against every installed schema; G1
(`image/checks/desktop.sh`) checks it again and fails on a `color-scheme`, because the
rebuilt shell draws GNOME's `'default'` light. The input-source keys move to
Super+Alt+Space, so Super+Space is free for Spotlight. `icon-theme='Apex'` ships in the
same package as the Apex icon theme, whose `Inherits=` reaches Adwaita: a missing theme
would leave GTK 4 with hicolor alone and no Adwaita symbolic icons.

## `dconf/`

Vendor defaults have two homes, and only two:

- `90_apex.gschema.override` holds every default of a fixed-path key.
- dconf's `distro` database (`/etc/dconf/db/distro.d/`, compiled by `dconf update` in the
  image build) holds only defaults no override can express: keys of a relocatable
  schema, which an override cannot reach. Today that is the Ptyxis profile. It never
  holds a lock (ADR 0011).

`distro.d/50-apex-ptyxis` sets the Apex profile's `label='Apex'`,
`cell-height-scale=1.21` (DESIGN.md's line height of 1.6) and `palette='apex'`.
`palette='apex'` names `~/.local/share/org.gnome.Ptyxis/palettes/apex.palette`, which
apex-session-agent writes with the accent as the caret. Until the agent's first write
there is no such palette. Ptyxis 50.1 then draws its `gnome` palette and its stock
window colours: `ptyxis_terminal_update_colors` falls back to `gnome` when the lookup
returns NULL. A profile looks its palette up again only when the `palette` key changes,
so a window opened before the first write keeps `gnome` until it is reopened. The override makes its fixed
UUID Ptyxis's `profile-uuids` and `default-profile-uuid`. The font is not set here:
Ptyxis uses the system monospace font, `monospace-font-name`.

G1 (`image/checks/desktop.sh`) fails when:

- `/etc/dconf/profile/user` does not list `system-db:distro`;
- the compiled database is missing, or older than a keyfile;
- a lock ships;
- a keyfile sets a fixed-path key, or a profile that is not the default;
- a value is not a valid `org.gnome.Ptyxis.Profile` setting.

## `ptyxis/`

`apex-prompt.sh` goes to `/etc/profile.d/` (ARCHITECTURE 7.4), so Fedora's `/etc/bashrc`
sources it in every interactive bash, Ptyxis's included. It draws board 32's prompt in
the terminal palette's ANSI colours: the working directory in blue (34) and a dim (2)
` $`. Over SSH, `user@host` in green (32) and a dim `:` come first. The palette's
colours themselves, and the accent caret, are apex-session-agent's `apex.palette` (S1b).

It replaces PS1 only while PS1 is still Fedora's or bash's default, so a user's own
prompt in `~/.bashrc` wins. `bash-color-prompt.sh` sorts after it and leaves a
non-default PS1 alone. With `NO_COLOR` set, or `apex_prompt_disable=1` exported (from
`~/.bash_profile`, for example), Fedora's prompt stays. Inside a toolbox the container's
own `/etc/profile.d` applies, so a toolbox keeps Fedora's `⬢` prompt. `selftest.sh`
checks each case in a clean bash.

Ptyxis reads each session's state from VTE's shell integration: `vte.sh` sets
`PROMPT_COMMAND` and wraps PS1 in the OSC 133 `D;A` and `B` markers, unless PS1 already
carries them. `apex-prompt.sh` must therefore sort before `vte.sh`. In CI's Fedora job,
`.github/scripts/prompt-vte-check.sh` installs it among the real `/etc/profile.d`
scripts and runs `/etc/bashrc` in an interactive bash with `VTE_VERSION` set. It fails
when the file sorts after `vte.sh`, when PS1 is not our prompt between those markers,
or when `PROMPT_COMMAND` does not run VTE's prompt command.

## `tmpfiles/`

Flatpak apps run sandboxed, so GTK 4 in Bazaar sees `~/.config/gtk-4.0/apex.css`, the
window radius apex-session-agent writes, only when an override grants
`xdg-config/gtk-4.0:ro`. `/var` is not image content on bootc, so
`apex-desktop.conf`, installed in `/usr/lib/tmpfiles.d/`, creates the system-wide
override at boot:

```ini
# /var/lib/flatpak/overrides/global
[Context]
filesystems=xdg-config/gtk-4.0:ro;
```

Its `f` line never touches an existing file. When `global` already exists without
the grant, an admin's own override for example, Flatpak apps keep stock corners
until the admin adds it:

```bash
sudo flatpak override --system --filesystem=xdg-config/gtk-4.0:ro
```

`.github/scripts/tmpfiles-check.sh` applies the entry to an empty root and to one that
already has a `global`. It fails unless the first gets exactly the file above, at 0644,
and the second is left as it was. `make check-data` runs it as root.

## `keybindings/`

`60-apex.xml` goes to `/usr/share/gnome-control-center/keybindings/`, so Settings >
Keyboard lists and edits "Open Spotlight" under Launchers.

G1's `image/checks/keybindings.sh` fails when two default bindings share a combination
across `wm.keybindings`, mutter's two schemas, the shell's, media keys and the Apex
Keybindings schema. It reads the image's compiled schemas with the override applied, and
treats `<Primary>` and `<Control>`, `<Mod4>` and `<Super>`, and any modifier order as one.

## `wallpapers/`

The spec renders `apex-facets-{light,dark}.svg` with `rsvg-convert` at 3840×2400, which
covers the laptop's 2880×1800 panel and a 4K monitor, into `/usr/share/backgrounds/apex/`.
`apex-facets.xml` pairs them for the background chooser
(`/usr/share/gnome-background-properties/`); the override points
`picture-uri` and `picture-uri-dark` at the same PNGs.

## `icons/`

The `Apex` icon theme, in `/usr/share/icons/Apex/` (DESIGN.md, "Visual principles"):

| Directory | What it holds |
|---|---|
| `scalable/apps/` | Colloid's full-colour app icons and its alias links, less the one alias with a `-symbolic` name, from the commit `colloid_commit` in the spec pins. `make rpm` fetches that commit with git and archives only `COLLOID_PATHS`; `%prep` checks the archive against `colloid_sha256` |
| `symbolic/` | Apex Symbolic: each `icons/symbolic/NAME.svg` becomes `NAME-symbolic.svg`, its strokes turned into fills by `fill-strokes.sh` (Inkscape's stroke-to-path), because GTK and St recolour fills only |

`index.theme` inherits `Adwaita,hicolor`, so every symbolic icon Apex Symbolic does not
draw yet, and every app icon Colloid lacks, comes from Adwaita and then hicolor. Folders,
places and mimetypes are Adwaita's until S7. Glyphs are drawn on a 16 px grid with a 1 px
keyline, a 1.75 px stroke, and round caps and joins: the 78 glyphs of board 31, named by
the board's ids. Nine of them (`go-next-arrow`, `apex-desktop`, `auth-fingerprint`,
`selection-area`, `pointer`, `window`, `briefcase`, `globe`, `dark-mode`) add icons; the
rest replace Adwaita's symbolic icon of the same name.

`fill-strokes.sh` scales a glyph 100 times before stroke-to-path, because Inkscape offsets
curves to a fixed tolerance in user units, and the 16-unit canvas made that tolerance a
visible 0.2 px at `globe`'s cusps; the output keeps the scale in its viewBox. It ungroups
first, so a group's stroke and transform reach its children, up to two levels of the
glyph's own groups; a deeper stroke is left for `check-theme.sh` to catch. Fills, evenodd
cores and opacities pass through, and a `stroke-opacity` becomes a `fill-opacity`.

`check-theme.sh` fails when `index.theme` lacks a key, a group or
`Inherits=Adwaita,hicolor`, when a directory with icons is not listed, when an SVG does
not parse, when a link is absolute or dangling, when a symbolic icon has a stroke that is
not `none` or sits outside `symbolic/`, and, given the sources, when a glyph's
`stroke-opacity` did not survive as a fill or opacity. The spec's `%check` runs it on the installed theme; `make
check-data` runs it on a theme built from `icons/`. GTK's icon cache is left to the image
build and to gtk-update-icon-cache's file trigger.

To move the Colloid pin, set `colloid_commit` and run `make rpm`: `%prep` fails, and
`sha256sum target/rpm/SOURCES/Colloid-icon-theme-*.tar` gives the new `colloid_sha256`.

## `plymouth/`

Boards 01 (boot splash) and 30 (disk unlock), in `/usr/share/plymouth/themes/`
(DESIGN.md, "Boot"; ARCHITECTURE 7.4):

| Theme | Plugin | What it draws |
|---|---|---|
| `apex` | script | black; the diamond and the Apex wordmark; the 160×3 bar with round ends, driven by Plymouth's boot progress (and an offline update's percentage); no footer. A passphrase request swaps the bar for the lock screen's 250×38 field, "Enter Passphrase", "Press Enter to unlock the disk", and after a wrong passphrase a red ring and "Wrong passphrase. Try again." |
| `apex-twostep` | two-step | the same wordmark, two-step's own square-ended bar and its passphrase dialog: the fallback when the script theme misbehaves |

`build.sh OUTDIR art/*.svg` renders the art with `rsvg-convert` into both themes,
`apex`'s at 1x and `@2x`. The text is pre-rendered in Adwaita Sans, so the initramfs
needs no font and no label plugin; `build.sh` fails when fontconfig does not resolve
Adwaita Sans ExtraBold. Neither theme sets itself as the default: the image runs
`plymouth-set-default-theme apex` before dracut.

Both themes are drawn for `DeviceScale=1`, which the image sets in `plymouthd.conf`.
Plymouth 26 draws a script image at one image pixel per logical pixel and has no call
to change that, so a sharp splash on the 2880×1800 panel needs the panel's pixels to be
logical ones. `apex.script` lays the boards out in logical pixels from the screen's
centre and loads the `@2x` images when the screen is at least 1600 logical pixels high:

- at `DeviceScale=1`, the `@2x` images draw 1:1 and sharp;
- at `DeviceScale=2`, the panel is 1440×900 logical, so the 1x images draw at the right
  size, upscaled and soft. A 1080p monitor gets the 1x images 1:1.

`apex-twostep` has one size: the `@2x` images, a 320×6 bar and 20 pt text.

Esc in either theme shows Plymouth's console viewer, the text view that always shows
the passphrase prompt. Its text is drawn by `label-freetype` (the only label plugin
in the initramfs) at points × 96 dpi × `DeviceScale`, so both keyfiles set
`MonospaceFont=monospace 20`. At `DeviceScale=1` that matches Plymouth's default
`monospace 10` at `DeviceScale=2`: a 28 px passphrase line with 21 px glyphs, against
15 and 11 px without it. The font is the image's `fc-match monospace`, which
plymouth-populate-initrd already copies into the initramfs.

`check-theme.sh THEMES` fails when a keyfile lacks its `Name`, `ModuleName`, `ImageDir`
or `ScriptFile` at `/usr/share/plymouth/themes/`, when an image `apex.script` loads is
missing at 1x or `@2x`, when an `@2x` image is not exactly twice its 1x size, when the bar
is not 160×3 (320×6 for two-step's), when a two-step image is missing or not at `@2x`, or
when a keyfile's `MonospaceFont` is not `monospace 20`. The spec's `%check` runs it on the
installed themes, CI on the built RPM's payload, and `make check-data` on `build.sh`'s
output.

`.github/scripts/plymouth-preview.sh THEMES OUTDIR` boots both themes headless:
plymouthd on its X11 renderer (`plymouth-devel`) in Xvfb, on a 2880×1800 screen at
`DeviceScale` 1, then `apex` again at 2. It shows the splash at 58 %, asks for a
passphrase, types one, answers it, asks again and presses Esc. It saves each frame as
PNG and checks pixels: the black background, the wordmark, the bar's fill and track, the
field, the placeholder, the hint, the first bullet, the error ring and the Esc view.
At `DeviceScale=1` it also checks that the Esc view's passphrase line is 24 to 36 px
high. It hides `label-pango` while it runs, so text is sized as in the initramfs. It runs
as root in a container only, because the themes go to `/run/plymouth/themes`; `make
check-data` runs it there, and CI fails if it skipped.

```bash
podman run --rm -v "$PWD:/src:z" -w /src registry.fedoraproject.org/fedora:45 bash -c \
  'dnf5 -y install make librsvg2-tools adwaita-sans-fonts plymouth-plugin-script \
     plymouth-plugin-two-step plymouth-devel xorg-x11-server-Xvfb xwd xdotool netpbm-progs &&
   make check-data'    # frames in target/check-data/plymouth-frames/
sudo plymouth-set-default-theme apex      # on a machine; -R also rebuilds the initramfs
```

## `fontconfig/`

`60-apex-adwaita-sans-ss03.conf` appends `ss03` to Adwaita Sans's font features, installed
in `/usr/share/fontconfig/conf.avail/` and linked from `/etc/fonts/conf.d/`. The fonts
themselves, `adwaita-sans-fonts` and `jetbrains-mono-fonts`, are in
`image/packages/gnome.txt`.

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
