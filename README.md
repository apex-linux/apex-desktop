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
it builds the image, in a build stage that has only `bash`, coreutils and
`python3`, so the install step uses nothing else.

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
