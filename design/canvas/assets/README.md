# Canvas assets

`MANIFEST.md` lists the 36 SVG files uploaded to the canvas. They came from
a co-writer, so they are untrusted. Only the files below are in this
repository, each rebuilt by the sanitiser in
`src/apex_desktop/kernel/svg.py`, which keeps an allowlist of elements and
attributes, drops metadata and empty bitmap placeholders, and rejects
scripts, event handlers, foreign content and external references.

## Shipped

| File | Blob id | Why it is cleared |
| --- | --- | --- |
| `facets-light.svg` | `3d451127dc2b77221bac98465ee1ec99` | Apex's own "Facets" wallpaper. Flat fills only, no metadata, no third-party traits (`handoff/wallpapers-and-app-icons.md`). |
| `facets-dark.svg` | `f607332583898d73d053baf1c0cae872` | The dark variant of the same design. |

## Withheld

The other 34 files are app and shell icons in the style of the Colloid icon
theme (GPL-3.0). None ships until the owner settles their provenance and
licence.

| Files | Reason | Open question |
| --- | --- | --- |
| `app-calendar`, `app-files`, `app-mail`, `app-music`, `app-settings`, `app-software`, `app-terminal`, `app-text-editor`, `app-web`, `shell-show-apps`, `shell-trash` | They carry a C2PA manifest stating the files may have been created or modified by an AI tool, with unknown origin. Whether they differ from Colloid is unknown until diffed against a pinned Colloid commit. | OQ-16 (AW-2, AW-6) |
| The 20 other referenced app icons | Most likely Colloid's own files, but no provenance data and no pinned Colloid commit to compare against. If identical, they come from Colloid itself, not from here. | OQ-16 (AW-1) |
| `unreferenced-blue-globe`, `unreferenced-red-flame`, `unreferenced-teal-paw` | No artboard uses them and their identity is unknown. | OQ-16 (AW-5) |

Until then the dock and app grid show each app's own icon, and the shell's
Show Apps button keeps its symbolic glyph.
