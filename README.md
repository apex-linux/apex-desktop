# apex-desktop

The desktop data of [Apex](https://github.com/apex-linux/apex), a Fedora 45 bootc desktop
for one laptop, the ASUS Vivobook Pro 14X OLED (M7400QC). It ships as the `apex-desktop`
RPM, which carries no code:

- the `io.github.apex_linux.Apex.Desktop` GSettings schema, the settings of the Apex
  layer in gnome-shell, and its Keybindings child;
- the vendor defaults: `90_apex.gschema.override` for GNOME's schemas, dconf's
  `distro` database for the Ptyxis profile, and the coloured bash prompt in
  `/etc/profile.d/`;
- the Open Spotlight row of Settings > Keyboard, the `ss03` feature of Adwaita Sans and
  the Apex Facets wallpapers;
- the `Apex` icon theme: Colloid's app icons from a pinned commit, and the Apex Symbolic
  glyphs with their strokes turned into fills;
- the boot splash: the Plymouth script theme `apex`, with its disk passphrase field, and
  the `apex-twostep` fallback;
- a tmpfiles entry for the global Flatpak override, so Flatpak apps read `apex.css`;
- the shell's crash guard, as user units.

[desktop/README.md](desktop/README.md) describes each directory. The layer itself lives
in [apex-gnome](https://github.com/apex-linux/apex-gnome).
[apex-image](https://github.com/apex-linux/apex-image) pins this repository by commit,
builds the RPM with `.github/scripts/rpms.sh build` in its builder VM, and checks the
installed result in G1 (`image/checks/desktop.sh` and `keybindings.sh`). The design is in
[DESIGN.md](https://github.com/apex-linux/apex/blob/main/docs/DESIGN.md), "Settings
contract".

Other repositories carry copies of the schema for their tests (apex-gnome's layer tests,
apex-system's session agent). apex-image's contracts check fails when a copy differs
from the commit it pins here, so a schema change lands here first and the copies follow.

## Development

```bash
just check        # make check-data, the script self-test and the comment guard
just rpm          # the RPM from git HEAD, on Fedora 45
.github/scripts/rpms.sh key    # the RPM's content key for git HEAD
```

`make check-data` runs xmllint, `glib-compile-schemas --strict`, `dconf compile` and the
icon theme check (Inkscape for the symbolic icons), and builds, checks and renders the
Plymouth themes, when the tools are installed. `make rpm`
fetches Colloid from github.com. CI also builds the RPM in Fedora 45. The comment guard is
`apex-lint`, from [apex-ci](https://github.com/apex-linux/apex-ci):
`cargo install --locked --git https://github.com/apex-linux/apex-ci apex-lint`.

## License

GPL-3.0-or-later (`LICENSE`). The Colloid app icons in the RPM are GPL-3.0-only, from
[Colloid-icon-theme](https://github.com/vinceliuice/Colloid-icon-theme)
(`LICENSE.Colloid`).
