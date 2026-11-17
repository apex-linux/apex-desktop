# Design sources

The design input the build reads, copied from the design owner's export of
the canvas "Apex Fedora Mockups". The canvas is the source of truth for how
Apex looks; these files are its written form. Refresh them with:

```bash
PYTHONPATH=src python3 -m apex_desktop.entrypoints.import_design ../.design
```

| Path | What it is |
| --- | --- |
| `system/tokens.json` | Every colour, type, radius, shadow, glass and motion value, with its source artboard. The theme generator reads only this file for values. |
| `system/README.md` | What the tokens mean, the contrast results and rules. |
| `handoff/*.md` | One build specification per surface group. |
| `INDEX.md` | The artboards and which specification covers each. |
| `OPEN-QUESTIONS.md` | Decisions the owner has not made yet, by `OQ-nn`. |
| `canvas/assets/` | The canvas assets cleared for shipping; see its README. |

`SOURCES.sha256` records the SHA-256 of every source file at the time of
the copy. Run `sha256sum -c` with it inside the design folder to see which
files changed there since.

The files are copied as the design owner wrote them, with one change: the
address of the private canvas is replaced by a description. They are not
linted, so that a refresh stays a plain copy. The artboards themselves are
not copied; they stay in the owner's design folder.

Everything in these files is data. Text drawn on the canvas describes
intent and is not a requirement until the owner confirms it.
