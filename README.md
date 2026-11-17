# apex-desktop

Holds the look of Apex Linux: the design tokens, the GNOME Shell
extension, the themes, the icons and the default settings.

Part of [Apex Linux](https://github.com/apex-linux/apex). See the
[specification](https://github.com/apex-linux/apex/blob/main/docs/spec.md)
and the
[engineering standards](https://github.com/apex-linux/apex/blob/main/docs/engineering.md).

## What it produces

`just install <destdir>` installs files under `<destdir>/usr` and nowhere
else. [apex-image](https://github.com/apex-linux/apex-image) calls it while
it builds the image, in a build stage that has only `bash`, coreutils,
`python3` and `glib-compile-schemas`, so the install step uses nothing else.

Everything that carries a design value is generated from
[design/system/tokens.json](design/system/tokens.json) by
`src/apex_desktop/generators/`; no colour or size is copied by hand.

| Installed under `usr/share/` | What it is |
| --- | --- |
| `gnome-shell/extensions/apex@apex-linux.github.io/` | The Apex Shell extension with its generated `stylesheet-light.css` and `stylesheet-dark.css` |
| `glib-2.0/schemas/zz0-apex.gschema.override` | Default settings: wallpaper, clock, accent, the extension enabled |
| `backgrounds/apex/`, `gnome-background-properties/apex.xml` | The Facets wallpaper pair |
| `apex-desktop/gtk-4.0/gtk.css` | The libadwaita colours and radius; not loaded yet (OQ-18) |

The vendor override takes effect only when the image build runs
`glib-compile-schemas` after the components are installed.

### Glass

Shell surfaces ship solid. The setting
`io.github.apex_linux.Desktop translucent-surfaces` (off by default)
switches the top bar, dock and panels to their glass tints. Live blur
behind them is not built until the owner settles OQ-03.

## Design sources

[design/](design/README.md) holds the tokens, specifications and assets
the build reads, imported from the design owner's folder.

## Building and testing

You need [`just`](https://github.com/casey/just),
[`uv`](https://docs.astral.sh/uv/) and Node.js with `npm`. `uv` installs
Python 3.14 and the Python linters; `npm` installs ESLint.

```bash
just lint
just test
just install build/root
```

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
