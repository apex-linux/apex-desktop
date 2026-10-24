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
| `ptyxis/` | `apex-desktop`: the coloured bash prompt and the shell's exit status for VTE, in `/etc/profile.d/` | GPL-3.0-or-later |
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
carries them. `apex-prompt.sh` must therefore sort before `vte.sh`.

`vte.sh` reports a command's exit status as `vte.shell.postexec` from `__vte_precmd`,
but Fedora's `/etc/bashrc` puts a title `printf` and systemd's
`__systemd_osc_context_precmdline` ahead of it in the `PROMPT_COMMAND` array, so `$?`
is 0 by then and a failed command reads as a success. `zz-apex-shell-status.sh` sorts
after `vte.sh`:

- it puts `__apex_postexec` first in `PROMPT_COMMAND`, where `$?` is still the
  command's, and sends `vte.shell.postexec` from there;
- it sends it only after a command ran: PS0, which bash expands only before running a
  command, sets a flag, so an empty Enter repeats no stale status;
- it redefines `__vte_precmd` to send only `vte.shell.precmd`.

It does nothing outside an interactive bash, or when `vte.sh` did not load or
`PROMPT_COMMAND` is not an array (older bash, where `vte.sh`'s single
`__vte_prompt_command` reads `$?` first anyway).

In CI's Fedora job, `.github/scripts/prompt-vte-check.sh` installs both files among the
real `/etc/profile.d` scripts and runs `/etc/bashrc` in an interactive bash with `VTE_VERSION` set. It fails
when:

- `apex-prompt.sh` sorts after `vte.sh`, or `zz-apex-shell-status.sh` before it;
- PS1 is not our prompt between those markers;
- `PROMPT_COMMAND` does not run VTE's prompt command;
- `vte.sh`'s `__vte_precmd` is not the one `zz-apex-shell-status.sh` replaces, so a
  VTE update that changes it fails CI instead of breaking quietly;
- in a pty (`script`), `false`, `true`, an empty line and `(exit 3)` do not give exactly
  the expected OSC 666 and 133 sequence: each status once, after the command's
  `preexec`, and none for the empty line.

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
| `32x32/places/`, `32x32@2x/places/`, `scalable/places/` | the Apex folders in blue, built by `build-places.sh` (below) |
| `32x32/mimetypes/`, `32x32@2x/mimetypes/`, `scalable/mimetypes/` | the Apex file icons, built by `build-mimetypes.sh` (below) |
| `symbolic/` | Apex Symbolic: each `icons/symbolic/NAME.svg` becomes `NAME-symbolic.svg`, its strokes turned into fills by `fill-strokes.sh` (Inkscape's stroke-to-path), because GTK and St recolour fills only |

`index.theme` inherits `Adwaita,hicolor`, so every symbolic icon Apex Symbolic does not
draw yet, and every app icon Colloid lacks, comes from Adwaita and then hicolor, as do
the places and content types boards 27 to 29 do not draw. Glyphs are drawn on a 16 px grid with a 1 px
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
`Inherits=Adwaita,hicolor` (`Inherits=Apex` for an `Apex-<accent>` theme), when a directory with icons is not listed, when an SVG does
not parse, when a link is absolute or dangling, when a symbolic icon has a stroke that is
not `none` or sits outside `symbolic/`, and, given the sources, when a glyph's
`stroke-opacity` did not survive as a fill or opacity. The spec's `%check` runs it on the installed theme; `make
check-data` runs it on a theme built from `icons/`. GTK's icon cache is left to the image
build and to gtk-update-icon-cache's file trigger.

### Folders and the accent themes

Boards 27 to 29 draw the folders flat, on a 64-unit grid: a back tab in the accent at
68 % toward black, a 52×35 front with a 4-unit radius in the accent, and a white emblem,
the Apex Symbolic glyph at a 1.5 stroke, at `translate(22 28.5) scale(1.245)`.
`build-places.sh OUTDIR places/folder.svg places/emblems accents` renders the template:

- for each name in `places/emblems` with its glyph. These are the folders GLib 2.90's
  `glocalfileinfo.c` names (home, desktop, the XDG directories with `folder-projects`)
  and plain `folder`, the generic icon of `inode/directory`;
- for each of libadwaita's nine accents in `accents`, into `OUTDIR/Apex-<accent>`, whose
  `index.theme` inherits `Apex`. The blue set also goes into `OUTDIR/Apex` itself.

List sizes draw the folder without its emblem, as board 28's list view does at 30 px.
`32x32/places` and its `Scale=2` twin are Threshold directories from 24 to 40 px, and
`scalable/places` takes 33 px and up. GTK 4 prefers a directory of the request's scale,
then a non-scalable one, so the emblem shows from 41 px up at either scale.
`.github/scripts/places-check.py THEMES` checks that with GTK 4's own lookup: each name, in
`Apex` and every `Apex-<accent>`, at 16 to 32 px and 48 to 256 px, at scale 1 and 2,
resolves to the right directory of that theme, in its accent. `make check-data` runs it
when Python has GTK 4; CI requires it, and runs it again on the RPM's payload.

Not drawn on the boards, so still Adwaita's: `folder-remote`, `user-trash` and
`user-trash-full`. apex-session-agent points `icon-theme` at `Apex-<accent>` (S7).

### File icons

Boards 27 to 29 draw a file as a flat page on the same 64-unit grid, in its kind's
colour, with a 40 % white corner fold and, in the grid, its extension in white Adwaita
Sans ExtraBold at 9 units; the list view draws the page without the label.
`build-mimetypes.sh OUTDIR mimetypes/file.svg mimetypes/kinds mimetypes/types` renders:

- `mimetypes/kinds`: board 27's colour for each kind, and slate for a file it names no
  kind for;
- `mimetypes/types`: each icon name with its kind and label. The generic icons that
  shared-mime-info's `generic-icon` names (`x-office-document`, `text-x-generic`,
  `package-x-generic`, `audio-x-generic` and the rest) have no label, because an icon
  theme cannot know a file's extension; the content types Files shows most get their
  own, labelled icon. Markdown, PDF, ISO images and code need one: their generic icons
  are the document, `application-x-generic` and plain text, in other colours.

Labels become paths in one Inkscape run, so no font is needed where the icons draw;
the build fails when fontconfig does not resolve Adwaita Sans ExtraBold, or when a label
kept its text. List sizes take the unlabelled page, through the same directory pair as
the folders. `.github/scripts/mimetypes-check.py THEMES` fails when a name in `types` is
not one GIO gives any registered content type, or when one of 54 files (board 27's and
common ones), its type guessed by GIO as Files does, does not resolve with GTK 4 to an
Apex file icon in its kind's colour, at list and grid sizes and at scale 1 and 2.

To move the Colloid pin, set `colloid_commit` and run `make rpm`: `%prep` fails, and
`sha256sum target/rpm/SOURCES/Colloid-icon-theme-*.tar` gives the new `colloid_sha256`.

### Symbolic icon coverage

`expected-symbolic.txt` lists every `*-symbolic` name that the Fedora 45 shell, GTK 4,
libadwaita and the apps of apex-image's `gnome.txt` request and do not ship themselves,
with the packages that request it. `tools/icons/scan.sh tools/icons/packages.txt` writes it
in fedora:45 with those packages installed: it reads each package's ELF files, GResources
(through `gresource extract`, so compressed ones too), JavaScript, GtkBuilder, CSS and
Python files. Its `@` lines name the versions it read, so a Fedora update shows up as a
diff. Names built at run time, such as UPower's battery levels and the shell's signal
strengths, are not literals: the scan prints them as templates, and `DYNAMIC` in
`scan.sh` lists the families Apex knows of.

`make check-icons` builds Apex Symbolic, then looks every name up with GTK 4's own
`Gtk.IconTheme` in `Apex` (`.github/scripts/symbolic-check.py`). Through `Inherits=`, an
Apex glyph wins and a stock Adwaita one is fine; a name nothing draws fails, and the check
prints it. It reports how many names each theme draws; `SYMBOLIC_FLAGS=--fallbacks` lists
the names Apex Symbolic does not draw yet. CI runs both in fedora:45, and warns, without
failing, when a fresh scan differs from the committed list.

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
