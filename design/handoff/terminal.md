# Terminal

## Summary

The Terminal app: a session-oriented terminal with a sidebar of sessions
grouped by where they run (this computer, a Toolbx container, an SSH host),
per-session state (needs you, running, done, failed, idle), split panes and
an AI coding agent ("claude") asking for permission inside a pane.

| No. | Artboard | Defaults |
| --- | --- | --- |
| 32 | `Terminal.dc.html` | `session` image, light |
| 33 | `TerminalSplit.dc.html` | `session` gnome (split side by side, agent waiting), dark |

`diff` shows the two files are identical except for the `<title>`, the
`session` and `dark` defaults in `data-props` (line 156) and the matching
fallbacks in `renderVals()` (lines 165-166). Line numbers below are from
`Terminal.dc.html` and hold for both.

The top bar and dock are covered by
[shell-top-bar-and-dock.md](shell-top-bar-and-dock.md).

## Upstream mapping

Recommended base: **Ptyxis** (`org.gnome.Ptyxis`, Fedora Workstation's
default terminal since Fedora 41). GTK 4, libadwaita, VTE, with
container-aware profiles. Confidence that Ptyxis is the best base: medium to
high. Confidence that the design can be built on Ptyxis without carrying
large downstream patches: low.

| Feature in the design | Ptyxis today | GNOME Console (`kgx`) | Confidence |
| --- | --- | --- | --- |
| Tabs as sessions | Stock: `AdwTabView`, tab bar, tab overview | Stock | High |
| Vertical session sidebar | Not available. Patch: a sidebar list bound to the tab view's pages | Not available | High |
| Toolbx / Distrobox / Podman containers as profiles | Stock (`ptyxis-agent` discovers containers; profiles can default to a container) | Not available | High |
| Group sessions by host, container, SSH host | Not available. Patch. Container is known per tab; the SSH host name is not | Not available | Medium |
| Root and SSH indication | Stock indicators for superuser and remote sessions (check how they are drawn in the shipped version) | Stock (coloured header) | Medium |
| Working directory in the header (`~/src/apex-gnome`) | Stock via OSC 7 (`vte.sh`) | Stock | High |
| Foreground program tag (`claude`, `zsh`, `just`, `ssh`) | Partly: Ptyxis tracks the process leader kind, not a name label. Patch | No | Medium |
| Running / done / failed state | Not available as states. Needs shell integration that reports command start and end with exit code (OSC 133 or VTE shell termprops). Patch | No | Medium |
| "Needs you" | Partly: a bell in a background tab marks the tab as needing attention (`AdwTabPage:needs-attention`). The design's state model is a patch | Partly | Medium |
| Progress bar per session (73 %) | VTE 0.80+ parses OSC 9;4 progress and recent Ptyxis shows it on tabs (check version). Sidebar bar is a patch | No | Low to medium |
| Relative "when" column (now, 4m, 1h) | Not available. Patch | No | High |
| Split panes (right, down) | Not available; upstream has not adopted splits. Large patch | Not available | High |
| Find | Stock | Stock | High |
| Custom ANSI palette, light and dark variants | Stock (palette files) | Fixed palettes | High |
| Agent permission prompt with choices | Not a terminal feature. The CLI draws it (see below) | Same | High |

GNOME Console is the alternative base. It is smaller and easier to patch but
has no container profiles or palettes, so more of the design would be new
code. A new app (GTK 4 + VTE) is the third option; the sidebar, state model
and splits are most of what such an app would be, so the cost difference
against heavy Ptyxis patches is smaller than it looks. A Ptyxis fork is the
cheapest start; the cost is rebasing on an active upstream.

### What the terminal does not own

*   **The agent prompt.** "Run the checks before I open the pull request?",
    the `❯ 1. Yes` menu and its outcomes are output of the `claude` CLI, not
    terminal UI. The terminal cannot turn output rows into buttons. Clicking
    a choice works only if the CLI enables mouse reporting; keys (arrows,
    1-3, Enter) are the CLI's own. The copy will change whenever the CLI
    changes, so it is not an acceptance criterion for the terminal.
*   **Prompts.** `~/src/apex-gnome $`, `⬢ ~/src/apex-desktop $` and
    `builder@apex-builder:~$` are shell `PS1` output. The `⬢` prefix is
    Toolbx's own prompt convention. If Apex wants this prompt, ship it as
    shell configuration (`/etc/profile.d`, zsh and bash rc files), not as
    terminal code.
*   **Semantic subtitles.** "pulling base images" and "all passed" cannot be
    derived from a byte stream. A terminal can know the command name, its
    run time and exit code; anything richer needs the program to report it
    (window title, OSC 9;4, or a new escape sequence). Generic fallback
    strings are proposed under [States](#session-states).

## Layout and measurements

### Window

| Property | Value | Source |
| --- | --- | --- |
| Frame | x 100, y 48, 1240 x 762, radius 14 (`radius.window`) | :48 |
| Shadow | `shadow.window` | :48 |
| Sidebar | 272 wide, `--side`, 1 px `--border` on the right | :50 |
| Content | 968 wide, `--t-bg` | :94 |

### Sidebar

| Element | Measurements | Source |
| --- | --- | --- |
| Header | 47 high, padding 0 8 0 16; "Terminal" 14 px / 700 | :51-52 |
| Header buttons | "New session" (+) and "Main menu", 32 x 32, radius 8, gap 2 | :53-55 |
| List | padding 2 8 8, gap 2, scrolls | :58 |
| Group header | 12 px / 700 `--dim`, gap 8, padding 6 10 6 (first) or 18 10 6; 16 px glyph | :296 |
| Group pill | JetBrains Mono 11 px / 600, padding 1 7, radius 6 (literal), `--btn` | :64 |
| Group "N needs you" | right-aligned, 11.5 px / 700, `--st-needs` | :66 |
| Session row | min-height 52, padding 8 10, radius 9 (literal), gap 10 | :303 |
| Session row, current | fill `--sel` | :303 |
| Row title | 13.5 px, weight 600; 800 when the session needs you; ellipsis | :304 |
| Row subtitle | 12 px `--dim`, ellipsis, 2 px below the title | :73 |
| Row "when" | 11.5 px `--dim`, tabular numbers | :75 |
| Row state icon | 16 px, after "when" (table below) | :76-80 |
| Row progress | 2 high, inset 10 left and right, 3 from the bottom, radius 1; track `--btn-h`, fill `--accent` | :81, :306 |
| Footer | padding 12 18 14, gap 16, 1 px `--border` on top, 12 px / 600 `--dim`, tabular | :86 |
| Footer counters | 14 px icon + number, gap 6, in the order needs, running, failed, done | :87-90 |

State icons (16 px in rows, 14 px in the footer):

| State | Glyph | Colour | Accessible name |
| --- | --- | --- | --- |
| needs | ring with a filled centre dot | `--st-needs` | Needs you |
| running | 28 % ring with a quarter arc, rotating 1.1 s linear | `--accent` | Running |
| done | check mark | `--dim` | Done |
| failed | filled disc with an X cut out in `--side` | `--st-fail` | Failed |
| idle | 16 px empty spacer | none | none |

### Header bar

| Element | Measurements | Source |
| --- | --- | --- |
| Bar | 47 high + 1 px `--border`, padding 0 10 0 14, gap 6, `--head` | :95 |
| Title | session title, 14 px / 700 | :97 |
| Path | 12.5 px `--dim`, ellipsis, 10 px after the title; reads "2 panes" when split | :98, :345 |
| Program tag | JetBrains Mono 11.5 px / 600, padding 2 8, radius 6, `--btn`, `--dim`; hidden when split | :99 |
| Split right, Split down | 32 x 32, radius 8, toggle (`aria-pressed`), `--btn-h` when on | :101-102, :323 |
| Find, Session menu | 32 x 32, radius 8 | :103-104 |
| Window controls | margin-left 8, gap 10, 24 px circles in `--btn`, named Minimize, Maximize, Close | :105-108 |

### Panes

| Element | Measurements | Source |
| --- | --- | --- |
| Pane container | flex row (split right) or column (split down) | :351 |
| Divider | 1 px `--border` before the second pane | :333 |
| Pane header (split only) | 34 high, padding 0 6 0 14, gap 8, 12.5 px, `--head`, 1 px `--border` bottom | :334 |
| Pane header content | needs icon 14 px (agent pane), title 700, path `--dim`, program tag (mono 11 px / 600, padding 1 7, radius 6), Close pane | :117-122 |
| Close pane | second pane only, 28 x 28, radius 7 (literal), 14 px X | :122 |
| Unfocused pane | header opacity .7, body opacity .62 | :334-335 |
| Terminal body | padding 12 18, JetBrains Mono 13 px, line height 20 px, `--t-fg` | :335 |
| Line | 20 px, `white-space: pre` | :127 |
| Cursor | block, one cell, `--t-fg` fill with `--t-bg` text; not blinking | :22 |
| Agent choices | rows 24 high, line-height 24, radius 4, full width | :194 |

Grid size this gives with JetBrains Mono (advance 0.6 em = 7.8 px):

| Layout | Columns x rows (approx.) |
| --- | --- |
| One pane | 119 x 34 |
| Split right | 57 x 32 each |
| Split down | 119 x 14 each |

13 px is 9.75 pt at 96 dpi; the closest Pango size is "JetBrains Mono 10"
(13.3 px). A 20 px line at that size needs VTE cell height scale of about
1.15 (`vte_terminal_set_cell_height_scale`; check whether the shipped Ptyxis
exposes it).

## States

### Tweaks

| Tweak | Options | Default (32 / 33) |
| --- | --- | --- |
| `session` | gnome, image, system, desktop, builder | image / gnome |
| `dark` | on, off | off / on |
| `accent` | the nine accents | blue |

### Sessions

The sidebar always shows all five sessions (`:273-284`):

| Group | Session | Subtitle | When | State | Panes |
| --- | --- | --- | --- | --- | --- |
| This computer | apex-gnome | claude · wants to run just check | now | needs | split right: "Turn on dock glass" (`claude`) and "Shell" (`zsh`) |
| This computer | apex-image | just vm-image · pulling base images | 18m | running, progress 73 % | one: "just vm-image" (`just`) |
| This computer | apex-system | cargo test · all passed | 4m | done | one: "cargo test" (`zsh`) |
| fedora-45 `toolbox` | apex-desktop | rpmbuild · exit 1 | 12m | failed | one: "rpmbuild" (`zsh`) |
| apex-builder `ssh` | builder VM | podman images | 1h | idle | one: "builder@apex-builder" (`ssh`), path `~` |

Group glyphs: a monitor (This computer), a hexagon (toolbox), a two-unit
server (ssh).

Footer in the default state: 1 needs you, 1 running, 1 failed, 1 done. Its
accessible names are "1 session needs you" (or "N sessions need you"),
"N running", "N failed", "N done".

The group header shows "1 needs you" next to "This computer" while
apex-gnome needs you.

### Session states

The artboard's state model, with proposed generic strings for a real build
where the program gives no richer status:

| State | When it applies (proposed) | Row subtitle, artboard | Generic fallback (proposal) |
| --- | --- | --- | --- |
| needs | The foreground program rang the bell or sent a notification escape while the session was not focused | claude · wants to run just check | `<program> · needs input` |
| running | A command is running (shell integration preexec seen, no postexec yet) | just vm-image · pulling base images | `<command> · running` |
| done | The last command exited 0 and the session has not been viewed since | cargo test · all passed | `<command> · done` |
| failed | The last command exited non-zero | rpmbuild · exit 1 | `<command> · exit <n>` |
| idle | At a prompt, nothing new | podman images | last command |

Clearing rules are not drawn. Proposal: viewing a session clears done and
needs; failed stays until the next command.

### Agent permission flow (apex-gnome)

Drawn in the left pane of apex-gnome. Before an answer (`:190-197`):

```
> Turn on dock glass in the Apex layer

● Updated desktop/shell/js/ui/apex/layer.js
    10 - const FEATURES = [];
    10 + const FEATURES = ['dock-glass'];
● Updated …/theme/apex/_apex-tokens.scss  +10 −4

  Run the checks before I open the pull request?
  $ just check

❯ 1. Yes
  2. Yes, and don’t ask again for just check here
  3. No, and tell claude what to do instead
```

The first choice is `--t-blue` / 600; the others `--t-fg`. The choices
group is named "Answer claude".

| Answer | Pane adds | Session state | Subtitle |
| --- | --- | --- | --- |
| 1. Yes | `  ✓ Allowed just check once`, blank, `● just check`, `  eslint ok · sassc ok · layer tests running…` | running | claude · running just check |
| 2. Yes, and don't ask again | `  ✓ Allowed just check in this folder from now on`, then as above | running | claude · running just check |
| 3. No | `  ✕ Not running just check`, blank, `> ` and cursor | idle | claude · waiting for your reply |

After any answer the footer drops to 0 needs you. Answer 3 ends in idle
although the agent is waiting for the user; see open questions.

### Split panes

*   apex-gnome opens split right. Every other session opens as one pane.
*   Split right and Split down are toggles. Pressing the active one returns
    to one pane; pressing the other switches direction (`:346-347`).
*   Splitting a single-pane session adds a fresh "Shell" pane (`zsh`, same
    path, prompt and cursor) and focuses it (`:318`, `:322`).
*   Clicking a pane focuses it. The unfocused pane dims (header .7, body
    .62).
*   Close pane (second pane only) returns to one pane and focus 0.
*   Split state is remembered per session while the window is open
    (`s.split[id]`). Selecting a session in the sidebar resets focus to the
    first pane.
*   With one pane the pane header is hidden and the window header shows the
    path and program tag; when split the window header shows "2 panes" and
    each pane header shows its own title, path and tag.

### Session output by tweak

Sample program output, quoted in the artboard (`:176-271`). The engineer
does not build this; the tester can use it to check palette mapping.

| Session | Content | Colours used |
| --- | --- | --- |
| gnome, right pane | `git status --short`, two ` M` lines, `git diff --shortstat`, prompt | blue path, dim `$`, red ` M` |
| image | `just vm-image` build log: four `==` stages, two `built`, two `mirror` lines, `# sig=…`, Copying blob progress `412.3MiB / 563.0MiB` | bold, green 600 `Finished`, green `built`, cyan `mirror`, dim hashes, blue progress bar |
| system | `cargo test --workspace`, 214 and 96 tests passed | green 600 `Compiling`, `Finished`, `Running`, `ok` |
| desktop | `rpmbuild -bb packaging/apex-desktop.spec` in Toolbx, `error: File not found: …gschema.xml` | magenta `⬢`, red `error:`, bold `RPM build errors:` |
| builder | `Last login: Sat Oct 24 08:51:12 2026 from 10.0.2.2`, `podman images` table | green `builder@apex-builder`, blue `~`, dim separators, bold table header |

### Not drawn, needed by a real build

Scrollback and scrollbar; text selection colour; hover and pressed states;
keyboard focus; the New session menu (profiles, containers, SSH hosts); the
Session menu contents; rename session; reorder and close sessions;
session restore after restart; empty state with no sessions; a session
whose process exited; pane resize by dragging the divider; more than two
panes; narrow window (collapse the sidebar); find bar; inactive window;
desktop notifications for needs and failed while the window is hidden; a
read-only or root session; bell settings.

## Terminal palette

### Terminal app (`--t-*`)

Defined in `Terminal.dc.html:18-19`, recorded in tokens.json
`color.terminal-app`. These map onto a Ptyxis palette file (one `[Light]`
and one `[Dark]` section). Ptyxis palette key names below are from memory;
verify them against the shipped version.

| ANSI slot | Role | Light | Dark | Contrast on `--t-bg` (L / D) | Source |
| --- | --- | --- | --- | --- | --- |
| Background | `--t-bg` | `#ffffff` | `#1b1b1e` | | drawn |
| Foreground | `--t-fg` | `#1d1d21` | `#ececef` | 16.8 / 14.6 | drawn |
| Cursor | block, `--t-fg` on `--t-bg` | `#1d1d21` | `#ececef` | | drawn |
| Faint (SGR 2) | `--t-dim` | `rgba(29,29,33,.66)` | `rgba(236,236,239,.6)` | 5.4 / 6.0 | drawn |
| Bold (SGR 1) | `--t-fg` at weight 600 | | | | drawn |
| Color0 black | not drawn | `#1d1d21` | `#5e5c64` | | proposal |
| Color1 red | `--t-red` | `#c01c28` | `#ff7b7b` | 6.1 / 6.9 | drawn |
| Color2 green | `--t-green` | `#1b7a43` | `#8ff0a4` | 5.4 / 12.4 | drawn |
| Color3 yellow | not drawn | `#9c6500` (`--warn`) | `#f8c454` (`--warn`) | 4.9 / 10.7 | proposal |
| Color4 blue | `--t-blue` | `#1a5fb4` | `#99c1f1` | 6.3 / 9.2 | drawn |
| Color5 magenta | `--t-magenta` | `#813d9c` | `#dc8add` | 6.8 / 7.1 | drawn |
| Color6 cyan | `--t-cyan` | `#0e6f82` | `#93ddc2` | 5.8 / 10.9 | drawn |
| Color7 white | not drawn | `#77767b` | `#ececef` | 4.5 / 14.6 | proposal |
| Color8-15 bright | not drawn | | | | open question |

Notes:

*   Only red, green, blue, magenta and cyan are drawn. Black, yellow,
    white and all eight bright colours are missing; the proposals above
    reuse existing tokens or GNOME palette greys and need owner sign-off.
*   The artboard draws bold at 600 with the normal colour ("bold is
    bright" off). VTE takes the font's bold face from fontconfig (700), so
    600 may not be reachable with the static JetBrains Mono family;
    accept 700 or ship the variable font.
*   VTE draws faint text by blending with the background; the exact
    `--t-dim` alpha is not configurable. Treat `--t-dim` as approximate.
*   `--st-fail` equals `--t-red` in both styles. `--st-needs`
    (`#b04000` / `#ffa348`) is an orange that is not in the ANSI palette.
*   `--t-a`, `--t-b`, `--t-c` in the same token group belong to the
    Overview window thumbnail, not to this app.

### Two terminal palettes disagree

tokens.json records two palettes. `--term-*` is how other artboards draw a
terminal window inside a scene (`Polkit.dc.html:20-21`, also Rollback,
Screenshot, Tiling). `--t-*` is the Terminal app. They disagree:

| Role | `--term-*` light | `--t-*` light | `--term-*` dark | `--t-*` dark |
| --- | --- | --- | --- | --- |
| Background | `#fcfcfd` | `#ffffff` | `#1c1c1f` | `#1b1b1e` |
| Foreground | `#2a2a30` | `#1d1d21` | `#e8e8ec` | `#ececef` |
| Green (prompt user) | `#26a269` (3.2:1, fails AA) | `#1b7a43` | `#8ff0a4` | same |
| Blue (prompt path, keys) | `#1c71d8` | `#1a5fb4` | `#99c1f1` | same |

They also disagree beyond colour:

| Aspect | In-scene terminal | Terminal app |
| --- | --- | --- |
| Prompt | `apex@fedora:~$`, user green 600, `:` dim, path blue 600 | `~/src/apex-gnome $`, path blue 400, ` $ ` dim, no user or host |
| Type | 13 px, line height 1.6 (20.8 px) | 13 px, line height 20 px |
| Padding | 12 16 16 | 12 18 |
| Chrome | no sidebar; "New tab" button and centred title "apex@fedora: ~" (`Polkit.dc.html:46-48`) | session sidebar, title + path + tag |

And the Overview thumbnail (`Overview.dc.html:20-21`) labels its blue
`--t-a` "prompt" and its green `--t-b` "path": the reverse of the in-scene
terminal, where green is the user and blue the path.

Recommendation: one palette, `--t-*`, everywhere; redraw the in-scene
terminals with it. The in-scene light green fails contrast.

## Tokens used

| Group | Tokens |
| --- | --- |
| Colour, surface | `--side`, `--head`, `--t-bg` (`--win` and `--view` defined, unused) |
| Colour, content | `--fg`, `--dim`, `--border` (`--faint` defined, unused) |
| Colour, control | `--btn`, `--btn-h`, `--sel`, `--accent` |
| Colour, status | `--st-needs`, `--st-fail` |
| Colour, terminal | `--t-fg`, `--t-dim`, `--t-red`, `--t-green`, `--t-blue`, `--t-magenta`, `--t-cyan` |
| Type | `ui` (Inter) for chrome, `mono` (JetBrains Mono 400 and 600) for terminal, tags and pills; sizes `micro` 11, `caption` 11.5, `small` 12, `small-plus` 12.5, `body` 13, `ui` 13.5, `heading` 14; weights 600, 700, 800; line height 20 px (mono) |
| Radius | `xs` 4 (choices), `sm` 8 (buttons), `window` 14, `circle`; literals 1 (progress), 6 (pills, tags), 7 (close pane), 9 (session rows) |
| Shadow | `shadow.window` |
| Glass | none inside the window |
| Motion | `duration.spinner` 1.1 s linear (`apxspin`) |
| Icon | Apex Symbolic, 16 px grid, stroke 1.75 |

## Build classification

| Element | Class | Why / how |
| --- | --- | --- |
| Window frame, header colours, window controls | theme | libadwaita CSS |
| Terminal font, size, padding 12 18 | theme / settings | Profile font; padding via CSS on `vte-terminal` |
| Line height 20 px | settings or patch | Cell height scale; patch if the shipped Ptyxis does not expose it |
| ANSI palette, light and dark | theme (asset) | Ship a Ptyxis palette file and make it the default profile palette |
| Prompts (`⬢`, colours, no user@host) | settings | Shell configuration shipped by the distro |
| Session sidebar with groups | patch | New sidebar bound to tab pages; grouping by container is cheap, by SSH host needs process inspection. Medium to high cost |
| Group pills (`toolbox`, `ssh`) | patch | Part of the sidebar |
| Session states and footer counters | patch | Needs shell integration (OSC 133 or VTE termprops) in every shell, including inside Toolbx and over SSH. Over SSH only the bell and title are reliable. High cost to make trustworthy |
| "Needs you" | patch, built on stock | Background bell / notification sets attention today; the state, weight 800 title and counts are new |
| Progress bar in a row | patch, built on VTE | OSC 9;4 is parsed by recent VTE; drawing it in the sidebar is new |
| "When" column | patch | Track time of last state change per tab |
| Semantic subtitles | patch + program cooperation | See [What the terminal does not own](#what-the-terminal-does-not-own) |
| Program tag in header and pane header | patch | Foreground process name from the agent |
| Split right / split down, pane headers, Close pane, focus dimming | patch | Ptyxis has no splits. Needs a pane tree inside each tab, focus handling, shortcuts, restore and tab overview support. High cost; the biggest single item |
| Find | stock | |
| New session (+) | stock behaviour, theme placement | Stock new-tab menu with profiles and containers; moved into the sidebar header |
| Agent prompt and its outcomes | stock (program output) | Drawn by the `claude` CLI; not terminal code |
| Running spinner | patch | Part of the sidebar |

## Accessibility

*   Contrast: every drawn palette colour passes 4.5:1 on `--t-bg` in both
    styles (lowest: light green 5.4:1, `--t-dim` light 5.4:1). `--dim` on
    `--side`: 4.5:1 light, 6.2:1 dark. `--st-needs` on `--side`: 5.2:1 /
    7.1:1. `--st-fail`: 5.4:1 / 5.6:1.
*   State is not colour-only: each state has its own glyph and an accessible
    name. The idle state has no name; give it one ("Idle") or none
    consistently.
*   The needs-you title uses weight 800 as a second cue. Keep it.
*   Sidebar rows are buttons with `aria-current="page"` for the open
    session. Pane regions are named "<session>, <pane title>" (for example
    "apex-gnome, Turn on dock glass").
*   The progress bar is named only "Progress". Name it after the session
    ("apex-image progress").
*   Keyboard: the design draws no shortcuts. Needed: next and previous
    session, jump to the next session that needs you, split right, split
    down, move focus between panes, close pane. Ptyxis tab shortcuts apply
    to sessions.
*   Screen readers: VTE exposes terminal text through its accessibility
    support; check it in the shipped version. Announce state changes
    (needs you, failed) as a polite live region on the sidebar.
*   Reduced motion: stop the spinner rotation when
    `gtk-enable-animations` is off; show the static arc.
*   Large text: rows have min-height 52 and ellipsize; the 272 px sidebar
    will clip long titles and the footer counters at large text sizes.

## Acceptance criteria

1.  The window opens at 1240 x 762 logical px with a 272 px sidebar and a
    47 px header bar.
2.  The default terminal profile uses JetBrains Mono at 13 px with 20 px
    lines and 12 px top / 18 px side padding; a full window shows about
    119 x 34 cells.
3.  `printf '\e[31mR\e[32mG\e[34mB\e[35mM\e[36mC\e[0m'` renders
    `#c01c28 #1b7a43 #1a5fb4 #813d9c #0e6f82` on `#ffffff` in the light
    style and `#ff7b7b #8ff0a4 #99c1f1 #dc8add #93ddc2` on `#1b1b1e` in the
    dark style (screenshot colour pick, tolerance 2 per channel).
4.  Switching the system style between light and dark switches the
    palette without restarting the terminal.
5.  Sessions are listed under group headers: "This computer", then each
    Toolbx container by name with a `toolbox` pill, then each SSH host with
    an `ssh` pill.
6.  A session running a command shows the accent spinner; after `false`
    it shows the failed glyph and "<command> · exit 1"; after `true` it
    shows the done glyph.
7.  `printf '\a'` in a background session marks it "needs you": orange
    glyph, title at weight 800, group header "1 needs you", footer needs
    count 1. Opening the session clears it.
8.  `printf '\e]9;4;1;73\e\\'` in a session shows a 2 px accent bar at
    73 % under its sidebar row.
9.  The footer counts equal the number of sessions in each state at all
    times.
10. Split right creates a second pane side by side with a 1 px divider,
    focuses it, and shows 34 px pane headers; the window header path reads
    "2 panes". Split down does the same top to bottom.
11. The unfocused pane draws its header at 70 % and its body at 62 %
    opacity. Clicking it focuses it.
12. Close pane on the second pane returns to one pane with no pane header.
13. Every sidebar state glyph and every header button has an accessible
    name.
14. With animations disabled, the running spinner does not rotate.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here. Ranked by
how much they block engineering.

1.  Base: Ptyxis fork with downstream patches, Console, or a new app? The
    sidebar, state model and split panes together are a large, permanent
    downstream delta.
2.  Are split panes required for the first release? They are the most
    expensive item and Ptyxis upstream has no splits.
3.  Is the AI agent part of the product? The design depends on a
    third-party CLI ("claude"). If it ships, who owns its install,
    updates and terms? If not, the needs-you state still works for any
    program that rings the bell.
4.  Session state semantics: what clears done and needs? Should answer 3
    ("No, and tell claude what to do instead") leave the session idle, as
    drawn, or needs you, since the agent waits for the user?
5.  Full ANSI palette: approve or replace the proposals for black, yellow,
    white and the eight bright colours.
6.  One terminal palette or two: retire `--term-*` in favour of `--t-*`?
7.  Default shell: the tags read `zsh` but Fedora defaults to bash. Is zsh
    the Apex default? Who ships the prompt?
8.  Old-spec and sample text: `fc45`, `fedora-45`, `fedora-bootc 45`,
    `gnome-shell-0:51.0-1.fc45.apex18`, `apex@fedora` in the in-scene
    terminals. Not requirements.
9.  Session persistence: restore sessions, splits and groups after a
    restart or reboot?
10. SSH grouping: how is the host found (parse the `ssh` command line,
    terminal title, or a profile per host)?
