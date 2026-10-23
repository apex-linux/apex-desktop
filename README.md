# apex-desktop

The desktop data of [Apex](https://github.com/apex-linux/apex), a Fedora 45 bootc desktop
for one laptop, the ASUS Vivobook Pro 14X OLED (M7400QC). It ships as the `apex-desktop`
RPM, which carries no code:

- the `io.github.apex_linux.Apex.Desktop` GSettings schema, the settings of the Apex
  layer in gnome-shell, and its Keybindings child;
- the vendor defaults: `90_apex.gschema.override` for GNOME's schemas, and dconf's
  `distro` database for the Ptyxis profile;
- the Open Spotlight row of Settings > Keyboard, the `ss03` feature of Adwaita Sans and
  the Apex Facets wallpapers;
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

`make check-data` runs xmllint, `glib-compile-schemas --strict` and `dconf compile` when
they are installed. CI also builds the RPM in Fedora 45. The comment guard is
`apex-lint`, from [apex-ci](https://github.com/apex-linux/apex-ci):
`cargo install --locked --git https://github.com/apex-linux/apex-ci apex-lint`.

## License

GPL-3.0-or-later (`LICENSE`).
