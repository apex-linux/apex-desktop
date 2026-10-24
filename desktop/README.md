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
| `systemd/` | `apex-desktop`: the shell's crash guard, as user units | GPL-3.0-or-later |
| `icons/` | `apex-desktop`: the `Apex` icon theme, with Colloid's app icons fetched at build | GPL-3.0-or-later; Colloid GPL-3.0-only |

S1b adds the Plymouth directory to `apex-desktop`.

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

`distro.d/50-apex-ptyxis` sets the Apex profile's `label='Apex'` and
`cell-height-scale=1.21`, DESIGN.md's line height of 1.6. The override makes its fixed
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
