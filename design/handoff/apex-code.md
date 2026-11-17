# Apex Code (GNOME Builder)

## Summary

Apex Code is the distribution's IDE: GNOME Builder, themed and patched, with
the app id kept as `org.gnome.Builder` (`CodeIcon.dc.html:18`). Three
artboards draw it:

| No. | Artboard | What it draws |
| --- | --- | --- |
| 40 | `Code.dc.html` | The full window and every tweak. Default state: Project view, `dock.js`, bottom panel open, completion popover open, minimap on, light. |
| 41 | `CodePalette.dc.html` | Code with `view=git`, `file=dock.js`, `palette=true`, `panel=false`, `agent=true`, `blame=true`, dark by default (`CodePalette.dc.html:22`). |
| 42 | `CodeDebug.dc.html` | Code with `view=outline`, `file=engine.rs`, `debug=true`, `find=true`, `panel=true`, `completion=false`, light (`CodeDebug.dc.html:49`). |

Artboards 41 and 42 only set props on Code through `<dc-import>`; every
measurement in this spec comes from `Code.dc.html`.

The window holds, left to right: a 264 px sidebar with four views (Project,
Outline, Search, Version control), the editor column (tab bar, editor with
gutter and minimap, bottom panel, status bar), and an optional 344 px agent
panel. Overlays: command palette, find and replace, debugger toolbar and the
completion popover.

## Upstream mapping

Target: GNOME Builder (GTK 4, libadwaita, libpanel, GtkSourceView 5, LSP
through its language-server plugins, runtimes through Flatpak, host and
Podman/toolbox). Confidence notes refer to Builder 43 and later as I know
them; check each "today" claim against the Builder version Fedora ships at
build time.

| Artboard feature | Builder today | Component (best knowledge) | Verdict | Confidence |
| --- | --- | --- | --- | --- |
| Window, panes, toggles | Yes | `IdePrimaryWorkspace`; libpanel `PanelDock` with start, bottom and end areas; `PanelToggleButton` | Stock + theme | High |
| Run split button with menu | Yes | Run button with run / debug / profiler menu in the header | Stock + theme | High |
| Build button in header | Partly | Build is an action and lives in the omnibar popover; no separate header button | Patch (small) | Medium |
| Omnibar (project, branch, build status) | Yes | `IdeOmniBar` | Stock + theme; status strings are patch | High |
| Command palette (files, symbols, commands) | Yes, as global search | Global search popover with search providers (file search, code index / symbols, actions and run commands) | Theme + patch | Medium |
| Palette prefixes `>` `@` `:` | Not that I know of | Search providers | Patch (small) | Low |
| Palette opened by clicking the omnibar | No; the omnibar opens the build popover | | Patch (small) | Medium |
| Project tree with modified dot | Yes (tree; VCS status colouring) | `project-tree` plugin, `git` plugin | Stock + theme; dot is patch (small) | Medium |
| Outline as a sidebar view | Symbol tree exists as a popover/selector, not a sidebar pane | `symbol-tree` plugin | Patch (medium) | Medium |
| Search (find in files) as a sidebar view | Yes, as a pane (usually bottom area; libpanel panes can be docked elsewhere) | `grep` plugin | Stock + settings; restyle | Medium |
| "Open N results as one buffer" | No | | Patch (large); needs a multi-excerpt editor buffer | High |
| Version control view with commit | No staging or commit UI | `git` plugin (libgit2 daemon) | New plugin (large) | Medium |
| Agent-written commit message | No | | Depends on the agent panel | High |
| Tabs | Yes | libadwaita tab bar per frame | Theme | High |
| Line numbers, current line | Yes | `IdeSourceView` / GtkSourceView gutter | Stock + style scheme | High |
| VCS change bar in gutter | Yes | `git` plugin change monitor, editor gutter | Stock + style scheme | High |
| Breakpoint dots in gutter | Yes | `debuggerui` plugin gutter renderer | Stock + theme | Medium |
| Fold chevrons | No; GtkSourceView 5 has no code folding | | Patch (large, in GtkSourceView) or drop | High |
| Minimap | Yes ("overview map") | `GtkSourceMap` | Stock + settings + CSS | High |
| Completion with details pane | Yes | `GtkSourceCompletion` + LSP providers; details through the completion info | Stock + theme; letter kind glyphs are patch (small) | Medium |
| Fuzzy match highlight in completion | Yes | GtkSourceView fuzzy highlight | Theme | Medium |
| Inline diagnostic pill at line end | No; Builder underlines, marks the gutter and shows a tooltip | Diagnostics in `libide-code` + editor | Patch (medium) | Medium |
| "2 references" lens line | No (no LSP code lens) | | Patch (medium to large) | Medium |
| Inline blame on the current line | Not in releases I know | `git` plugin | Patch (medium) if absent | Low |
| Find and replace with Aa / Whole word / regex and "2 of 3" | Yes | Editor search bar (`editorui`) | Stock; floating-card shape is theme or a small patch | Medium |
| Debugger (GDB), paused line, stepping | Yes | `debuggerui` + `gdb` plugins (GDB/MI) | Stock | Medium |
| Floating debugger toolbar over the editor | No; controls sit in the header | | Patch (small to medium) | Medium |
| Variables and call stack panes | Yes (locals, threads/frames, breakpoints) | `debuggerui` panes | Stock + layout patch (two columns in one pane) | Medium |
| Bottom panel: terminal, build output, diagnostics | Yes | `terminal` (VTE), `buildui`, diagnostics/issues pane | Stock + theme | Medium |
| Toolbox runtime chip | Runtime is shown in build configuration, not as a chip | `podman` plugin | Patch (small) | Medium |
| Status bar (Ln/Col, indent, encoding, language) | Yes | libpanel status bar items in the editor | Stock + theme | Medium |
| Warning count and LSP status in status bar | No | | Patch (small) | Medium |
| Agent panel (ACP client) | No | | New plugin (large) | High |

### Agent panel cost

The panel is an Agent Client Protocol (ACP) client: Builder spawns an agent
process (here "Claude Code" through an ACP adapter) and talks JSON-RPC over
stdio. A faithful build needs:

*   ACP transport and session lifecycle (initialize, new session, prompt,
    cancel), streaming message and tool-call updates, permission requests,
    and the file-system and terminal callbacks the agent can ask the client
    to perform. Method names change between ACP revisions; pin one.
*   A chat view with streamed rich text and inline code, message bubbles,
    and file-context chips.
*   A diff card that renders a proposed edit, applies it to the open
    `GtkSourceBuffer` with undo, and opens a full review (Builder has no diff
    review view to reuse).
*   Tool execution inside the build runtime (the artboard says "Ran just check
    in the toolbox"), which means routing agent terminal requests through
    Builder's runtime layer.
*   An "Ask before edits" permission mode, a thread list ("New thread"), and
    error, sign-in, offline and cancelled states (not drawn).
*   Packaging: the agent binary is third-party, needs the user's own account,
    and makes network calls. It cannot be assumed present in the image.
    Showing the product name "Claude Code" may need permission from its
    owner.

Estimate: two engineers, 8 to 12 weeks to a usable in-tree C plugin, plus
ongoing work to track ACP and Builder API changes. Builder's plugin API is not
stable across releases, so this is a carried downstream patch series. This is
the most expensive item in the spec.

### Packaging note

Every "patch" above means Apex ships its own Builder build. The Flathub
`org.gnome.Builder` Flatpak cannot carry them, and an Apex build that keeps the
same app id collides with it if a user installs both. Decide between an RPM in
the base image and an Apex Flatpak remote (see AC-2).

## Layout and measurements

Logical px on the 1440x900 artboard. `*{box-sizing:border-box}` applies, so
heights include borders.

### Scene

| Element | Value | Source |
| --- | --- | --- |
| Background | `--wall` (default wallpaper) | `Code.dc.html:28` |
| Top bar | 32 px shell top bar, "Apex Code" app name, clock "Tue Nov 3 10:24"; see `shell-top-bar-and-dock.md` | `Code.dc.html:30-46` |
| Window | x 100, y 48, 1240 x 762, radius 14 px, `--view`, shadow `var(--shadow), 0 0 0 1px var(--border)` | `Code.dc.html:48` |

### Header bar

Height 47 px including a 1 px `--border` bottom; `--head`; padding 0 10 px;
gap 4 px (`Code.dc.html:50`).

| Element | Measurements | Source |
| --- | --- | --- |
| Icon button (`.ib`) | 32 x 32, radius 8 px, 16 px glyph, stroke 1.75 | `Code.dc.html:24` |
| Show sidebar | `.ib`, pressed: `--btn-h` | `:51` |
| Run split button | margin-left 6 px, radius 9 px, `--btn`. Main part: height 32, padding 0 10 0 11 px, gap 7, 13 px / 700, 14 px play glyph (filled). Divider 1 px `--border`, 7 px vertical inset. Options part 28 x 32, 12 px chevron, stroke 1.9 | `:52-56` |
| Stop debugging | `.ib`, colour `--err`, 14 px filled square; only while debugging | `:57` |
| Build | `.ib`, colour `--dim`, wrench glyph | `:58` |
| Omnibar | centred on the window, 440 x 32, radius 9 px, `--btn`, padding 0 10 0 12 px, gap 9 px, 13 px. Folder glyph 16 px `--dim`; project name 700; branch glyph 13 px + branch name `--dim`; flexible gap; status 12 px / 600; key chip | `:60-67` |
| Key chip (`.chip`) | JetBrains Mono 11 px, padding 1 6 px, radius 5 px, inset 1 px `--border`, `--dim` | `:25` |
| Agent toggle | `.ib`; pressed fill `--btn-h`, otherwise transparent | `:70`, `:698` |
| Bottom panel toggle | `.ib`; same pressed rule | `:71` |
| Main menu | `.ib`, hamburger glyph | `:72` |
| Close | 24 x 24 circle, `--btn`, margin-left 6 px, 14 px glyph. No minimise or maximise button | `:73` |

### Sidebar

Width 264 px including a 1 px right `--border`; `--side` (`Code.dc.html:78`).

| Element | Measurements | Source |
| --- | --- | --- |
| View switcher | margin 10 12 8 px, padding 3 px, radius 10 px, `--btn`, gap 3 px. Four buttons, equal width, height 30, radius 8 px, 16 px glyph, gap 6 px. Selected: `--view` fill, shadow `0 1px 3px rgba(0,0,0,.12)`, `--fg`. Others `--dim`. Badge on Version control: "3", 11 px / 700 | `:79-83`, `:547-554` |
| Tree (Project) | padding 0 8 8 px, 13 px. Rows 28 px, radius 7 px, gap 5 px, padding-left `4 + depth x 14` px, right 10 px. Chevron 14 px `--dim`; file/folder glyph 16 px `--dim`; name ellipsised; selected row `--sel` and 600; modified dot 7 px `--mod` | `:86-95`, `:569-576` |
| Outline | Header row 26 px, 12 px `--dim`, file name. Rows 28 px, radius 7 px, gap 8 px, padding-left 8 px, children +14 px. Kind glyph JetBrains Mono 11 px / 700, min-width 22 px; name ellipsised; line number mono 11 px `--faint`. Current symbol `--sel` and 600 | `:99-108`, `:578-586` |
| Search | padding 0 12 8 px, gap 8 px. Field 34 px, radius 9 px, `--view`, ring `inset 0 0 0 2px var(--accent)`, glyph 16 px `--dim`, query mono 12.5 px. Button 30 px, radius 8 px, `--btn`, 12.5 px / 600. Group header 26 px, 600; folder 12 px / 400 `--dim`; count pill 11 px / 700, padding 0 6 px, radius 8 px, `--btn`, `--dim`. Hit rows 24 px, radius 6 px, padding 0 8 0 12 px, mono 12 px; context `--dim`; match `.t-m` | `:111-127`, `:588-592` |
| Version control | padding 0 12 8 px, gap 8 px. Message box min-height 64, radius 9 px, `--view`, inset 1 px `--border`, padding 9 10 px, 12.5 px / 18 px; second line `--faint`. Commit button 34 px, radius 9 px, `--accent`, `#fff` (literal), 700. "Changes" header 26 px, 600, count pill as above, margin-top 4. Change rows 30 px, radius 7 px, padding 0 8 px, gap 8 px; name 13 px; folder 11.5 px `--dim` ellipsised; line height 15 px; `+N` mono 11.5 px `--add`; `−N` mono 11.5 px `--mod` | `:129-141`, `:593-597` |

Project tree contents (depth, expanded, name, modified):

*   `apex-gnome`: desktop (0, open); shell (1, open); js / ui / apex (2,
    open); dock (3, open, modified); dock.js (4, modified); feature.js (4,
    modified); intellihide.js (4); glass (3, closed); layer.js (3);
    packaging (0, closed); tests (0, open, modified); layer (1, closed,
    modified); shots (1, closed); Justfile (0); README.md (0)
    (`Code.dc.html:557-563`).
*   `apex-system`: crates (0, open); apex-boot, apex-bootc (1, closed);
    apex-updated (1, open); src (2, open); engine.rs, dbus.rs, grubenv.rs,
    main.rs (3); Cargo.toml (2); hardware (0, closed); Cargo.toml, Makefile
    (0) (`:564-568`).

Only `dock.js`, `feature.js`, `README.md` and `engine.rs` open a buffer.

### Editor column

| Element | Measurements | Source |
| --- | --- | --- |
| Tab bar | 40 px including 1 px bottom `--border`; `--head`; padding 0 8 px; gap 4 px. Tab: flexible, max-width 220, height 30, radius 7 px, padding 0 12 px, gap 8 px, 13 px, name centred. Selected `--btn-h` and 700; others `--dim`. Unsaved dot 8 px `--fg` at opacity .55 | `:145-152`, `:600-606` |
| Editor text | JetBrains Mono 13 px, line height 21 px, padding-top 8 px | `:155` |
| Gutter: marks | 20 px column. Breakpoint 11 px circle `--err`. Fold chevron 11 px, stroke 2, `--faint` | `:156-158` |
| Gutter: numbers | 38 px, right-aligned, padding-right 10 px, `--faint`, tabular figures. Current line number `--fg` | `:159-161`, `:525` |
| Gutter: VCS bar | 4 px column, radius 1 px. Added `--add`; modified `--accent` (see AC-6) | `:162-164`, `:516` |
| Text area | padding-left 14 px. Current line background `--line`; paused line `--exec` and a "›" marker in `--warn` / 800 at x -12 px | `:165-168`, `:527` |
| Caret | 2 x 17 px, `--accent`, vertical-align -3 px. Hidden while the palette or debugger is active | `:167`, `:522` |
| Diagnostic pill | margin-left 18 px, padding 1 8 px, radius 6 px, `--warn-bg`, `--warn`, Inter 12 px / 600 | `:167` |
| Note (references, blame) | margin-left 22 px, Inter 12 px, `--faint` | `:167` |
| Minimap | 72 px, left 1 px `--border`, padding 8 6 0 px. Each line 4 px tall, 3 px text, syntax colours. Viewport box: inset 3 px left and right, top `8 + firstVisibleLine x 4`, height `visibleLines x 4`, radius 3 px, `--btn` | `:172-177`, `:713` |
| Bottom panel | 206 px including 1 px top `--border`; `--view` | `:219` |
| Panel tab strip | 38 px, padding 0 8 0 12 px, gap 4 px. Tab 28 px, radius 7 px, padding 0 10 px, gap 7 px, 12.5 px, 14 px glyph. Selected `--btn-h` and 700; others `--dim` | `:220-226`, `:655-661` |
| Runtime chip | mono 11.5 px / 600, padding 2 8 px, radius 6 px, `--btn`, `--dim` | `:225` |
| Text output | mono 12.5 px, line height 20 px, padding 2 18 10 px | `:240-242` |
| Debugger pane | mono 12.5 px / 21 px. Variables column flex 1.2, padding 0 16 px, right `--border`; Call stack flex 1, padding 0 16 px. Headings Inter 11.5 px / 700 `--dim`, 22 px. Variable rows 21 px, indent 16 px per level. Frame rows 21 px, padding 0 8 px, gap 10 px, radius 6 px; current frame `--sel` and 600 | `:227-238`, `:632-635` |
| Status bar | 28 px including 1 px top `--border`; `--head`; padding 0 12 px; gap 14 px; 12 px `--dim`. Paused label `--warn` / 700 with 13 px pause glyph. Problems: 14 px warning glyph + text, 600, `--warn` if any, else `--dim`. LSP: 7 px dot `--add` + server name. Right side: cursor, "Spaces: 4", "UTF-8", language | `:247-253`, `:716-718` |

Visible editor lines are 19 with the bottom panel and 29 without
(`Code.dc.html:494`). The first visible line is
`max(0, min(cursorLine - 9, totalLines - visible))` (`:495`).

### Overlays

All overlays use `--pop` and the shadow `var(--shadow), 0 0 0 1px
var(--border)`.

| Overlay | Measurements | Source |
| --- | --- | --- |
| Find and replace | Anchored top 8, right 86 px (clears the 72 px minimap) of the editor area; 380 px wide; radius 12 px; padding 8 px; gap 6 px; 13 px. Search field 32 px, radius 8 px, ring 2 px `--accent`, mono 12.5 px, counter 12 px `--dim`. Previous, Next, Close: 30 x 30 icon buttons, 14 / 13 px glyphs, stroke 1.9. Replace field 32 px, radius 8 px, `--btn`. "Replace" and "All": 30 px, padding 0 10 px, radius 8 px, `--btn`, 12.5 px / 600. Option chips use `.chip`; active chip `--fg` on `--btn-h` with no ring. Scope label 12 px `--dim` | `:179-194` |
| Search matches in text | Match: `--accent` at 24 % mixed with transparent, radius 2 px. Current match: `--accent` at 50 % plus 1 px `--accent` ring | `:21` |
| Debugger toolbar | Centred, top 8 px of the editor area; padding 4 px; gap 2 px; radius 12 px. Six 32 x 32 icon buttons: Continue (`--add`), Step over, Step into, Step out, Restart, Stop (`--err`) | `:196-200`, `:630` |
| Completion | radius 12 px, clip. List 300 px wide, padding 4 px. Rows 30 px, radius 7 px, padding 0 8 px, gap 8 px; selected `--sel`. Kind glyph 18 px wide, mono 11 px / 800 (`p` in `--ty`, `ƒ` in `--f`). Label mono 12.5 px; matched characters `.t-q` (`--accent`, 800). Type 11.5 px `--dim`. Details pane 250 px, left `--border`, padding 10 12 px, 12.5 px / 18 px: signature mono 12 px with syntax colours; description `--dim`, margin-top 6; footer 11.5 px `--faint`, margin-top 8 | `:202-215`, `:621-628` |
| Completion position | Below the caret line: top `8 + (cursorLine - 1 - firstVisible) x 21 + 23`; left `20 + 38 + 4 + 14 + round(typedChars x 7.8) - 18`. Default scene: top 199, left 183 in the editor area | `:626-628` |
| Command palette | Transparent full-window click catcher (no dimming), then a dialog centred on the window, top 10 px below the header bar, 600 px wide, radius 14 px. Input row 48 px, padding 0 14 px, gap 10 px, bottom `--border`; 16 px search glyph `--dim`; query mono 14 px with 2 x 17 px `--accent` caret; hint 12 px `--dim`. List padding 6 px. Section header 26 px, padding 0 12 px, 11.5 px / 700 `--dim`. Rows 36 px, radius 9 px, padding 0 12 px, gap 10 px, 13.5 px; glyph 16 px `--dim`; title 500 with matched characters `.t-q`; detail 12 px `--dim` ellipsised; optional `.chip`. First row selected (`--sel`). Footer 34 px, padding 0 16 px, gap 16 px, top `--border`, 12 px `--dim` | `:285-310`, `:663-695` |

### Agent panel

Width 344 px including a 1 px left `--border`; `--side`
(`Code.dc.html:257`).

| Element | Measurements | Source |
| --- | --- | --- |
| Header | 40 px, bottom `--border`, `--head`, padding 0 4 0 16 px, gap 8 px. Title 14 px / 700. "ACP" badge mono 10.5 px / 700, padding 1 6 px, radius 5 px, `--btn`, `--dim`. New thread `.ib` `--dim` | `:258-263` |
| Thread | padding 14 14 8 px, gap 12 px, 13 px / 19 px | `:264` |
| User message | right-aligned, max-width 86 %, padding 8 12 px, radius 12 12 4 12 px, `--accent`, `#fff` | `:265` |
| Agent text | inline code mono 12 px | `:266` |
| Diff card | radius 10 px, `--view`, ring 1 px `--border`. Header 34 px, padding 0 10 px, gap 8 px, 12.5 px: file 700, `+6` `--add`, `−0` `--mod`, range `--dim`. Body mono 11.5 px / 17 px, padding 6 10 px, `--add`. Buttons 28 px, padding 0 12 px, radius 7 px, 12.5 px: Accept `--accent` / `#fff` / 700, Review `--btn` / 600 | `:267-273` |
| Tool result | 12.5 px `--dim`, gap 8 px, 14 px check glyph `--add`, command mono 12 px `--fg` | `:274` |
| Composer | outer padding 10 12 12 px; box radius 12 px, `--view`, inset 1 px `--border`, padding 8 10 6 px. Placeholder 13 px `--faint`, 22 px. Context chips 11.5 px, padding 1 8 px, radius 6 px, `--btn`. Mode label 11.5 px `--dim` | `:276-281` |

## States

### Tweaks (`Code.dc.html:315`)

| Tweak | Values | Default | Effect |
| --- | --- | --- | --- |
| `view` | project, outline, search, git | project | Sidebar content |
| `file` | dock.js, feature.js, README.md, engine.rs | dock.js | Buffer, project (`apex-gnome` or `apex-system`), branch, LSP, language, tabs, tree |
| `panel` | boolean | true | Bottom panel; visible lines 19 or 29 |
| `completion` | boolean | true | Completion popover; only for `dock.js` (the only file with typed text), and never with the palette or debugger (`:489`) |
| `blame` | boolean | false | Replaces the note on the cursor line with the blame string; `dock.js` and `feature.js` only |
| `find` | boolean | false | Find popover and match highlights for `pin_rollback` |
| `debug` | boolean | false | Debug session; only takes effect when `file` is `engine.rs` (`:329`) |
| `map` | boolean | true | Minimap |
| `agent` | boolean | false | Agent panel |
| `palette` | boolean | false | Command palette |
| `dark` | boolean | false | `.apx-d` colours |
| `accent` | nine accents | `#3584e4` | `--accent` |

### Interactive states

*   Sidebar switcher sets the view (`:551`). Tree rows, tabs, search hits and
    change rows open their file (`:556`, `:572`, `:588`, `:594`). Tabs for
    files without content (`dbus.rs`, `grubenv.rs`) do nothing.
*   Bottom panel toggle and agent toggle flip their panes (`:720`, `:723`).
*   Clicking the omnibar opens the palette; clicking the click catcher or any
    palette row closes it (`:286`, `:297`, `:725`).
*   Panel tabs switch output (`:658`). Default tab: Debugger while debugging,
    else the terminal tab.
*   Hovered rows (`.row`) use `--btn` (`:23`).

### Per-file data

| File | Project / branch | LSP | Language | Cursor line | VCS added / modified | Extras |
| --- | --- | --- | --- | --- | --- | --- |
| dock.js | apex-gnome / dock-focus-label | typescript-language-server | JavaScript | 21 (26 with completion) | 11, 20-25 / 30, 31 | Note on 15, diagnostic on 4, typed line after 25 |
| feature.js | same | same | JavaScript | 12 | none / 12, 13 | blame string |
| README.md | same | same | Markdown | 6 | none | none |
| engine.rs | apex-system / main | rust-analyzer | Rust | 14 | none | Note on 6, breakpoints on 14 and 26 |

The cursor column is the line length plus one, so the caret sits at the end
of the line (`:716`).

### Debug session (artboard 42)

Run button reads "Continue"; Stop debugging appears; omnibar status "⏸ Paused
at engine.rs:14" in `--warn`; line 14 gets `--exec`, the "›" marker and a
breakpoint dot; caret and completion hidden; status bar shows "Paused ·
apex-updated · gdb"; panel tabs become Debugger, Terminal, Build; the
debugger pane shows variables and the call stack.

### States a real build needs (not drawn)

*   No project open (Builder's greeter / project picker) and cloning.
*   Build running, build failed, run in progress, program exited.
*   Debugger running (not paused), program exited, GDB missing in the
    runtime.
*   LSP starting, crashed, or not installed in the toolbox.
*   No toolbox, toolbox being created, Flatpak SDK missing.
*   Find with zero matches; regex error.
*   Palette with no results; palette loading.
*   Version control: clean tree, staged versus unstaged, conflicts, detached
    HEAD, commit failed (hook), not a repository.
*   Agent: not installed, signed out, offline, streaming, waiting for
    permission, edit rejected, error, cancelled; empty thread.
*   Unsaved changes on close; file changed on disk; read-only file.
*   Narrow window: which panes collapse first.
*   Keyboard focus rings on every control.

## Copy

Quoted exactly. Strings marked (data) are sample content.

*   Header: "Run", "Continue", aria labels "Show sidebar", "Run options",
    "Stop debugging", "Build", "Search files, symbols and commands", "Agent",
    "Show bottom panel", "Main menu", "Close".
*   Omnibar: project and branch names (data); "✓ Built 12 s ago"; "⏸ Paused at
    engine.rs:14"; "Ctrl K".
*   Sidebar views: "Project", "Outline", "Search", "Version control".
*   Search: "_focusShowing" (data); "Open 6 results as one buffer"; groups
    "dock.js" "apex/dock" "4" and "probe.js" "tests/layer" "2" (data).
*   Version control: "dock: the focus label survives its item" (data);
    "Written by the agent from the staged diff"; "Commit to
    dock-focus-label"; "Changes"; rows dock.js +12 −2, feature.js +3 −1,
    run.sh +38 −0 (data).
*   Editor notes (data): "2 references"; "3 references · 2 implementations";
    diagnostic "'LABEL_GAP' is assigned but never used"; blame "Claude · 18
    min ago · dock: the focus label survives its item" and "Claude · 18 min
    ago · dock: disconnect before intellihide goes".
*   Find: "pin_rollback", "2 of 3", "pin_kept", "Replace", "All", "Aa",
    "Whole word", ".*", "In this file"; aria "Previous match", "Next match",
    "Close search".
*   Debugger toolbar aria: "Continue", "Step over", "Step into", "Step out",
    "Restart", "Stop".
*   Completion: items "_focusItem", "_focusShowing", "_focus(item)",
    "_blur(item)"; types "DashItem | null", "void"; details "property
    _focusItem: DashItem | null", "The dock item that has key focus, cleared
    when the item is destroyed.", "typescript-language-server · Enter to
    insert".
*   Bottom panel tabs: "just check", "Build", "Diagnostics 1"; while
    debugging "Debugger", "Terminal", "Build". Chip "⬢ fedora-toolbox-45".
    Debugger headings "Variables", "Call stack · thread
    tokio-runtime-worker".
*   Terminal output (data): "⬢ ~/src/apex-gnome $ just check", "eslint
    desktop/shell tests ok", "sassc 3 sheets ok", "layer 1..729 ok", "✓ all
    checks passed in 41 s". Build: "[meson] build.ninja is up to date",
    "[ninja] [214/214] Generating apex.gresource", "✓ Build succeeded in 3.1
    s". Diagnostics: "⚠ dock.js:4 'LABEL_GAP' is assigned but never used
    eslint(no-unused-vars)".
*   Status bar: "Paused · apex-updated · gdb", "1 warning", "No problems",
    LSP name, "Ln 21, Col 42" (computed), "Spaces: 4", "UTF-8",
    "JavaScript" / "Markdown" / "Rust".
*   Agent: "Claude Code", "ACP", aria "New thread"; user message "Clear the
    focus label when its item is destroyed, and add a layer fact for it.";
    reply "I found the stale reference: _focusItem keeps a disposed DashIcon
    after an unpin. I'll clear it on the item's destroy."; diff header
    "dock.js" "+6" "−0" "lines 20–25"; "Accept", "Review"; "Ran just check
    in the toolbox · 41 s"; "Ask the agent…"; chips "dock.js", "feature.js";
    "Ask before edits".
*   Palette: query "dlab"; hint "Files, symbols and commands"; sections
    "Files", "Symbols", "Commands"; rows "dock_labels.js" "tests/layer/facts",
    "dock-labels.js" "tests/shots", "DockLabels" "class · dock.js:6",
    "DockLabels._keepLabelOnMonitor" "method · dock.js:58", "Dock: Run Layer
    Tests (dock labels)" "in fedora-toolbox-45" "Ctrl Enter"; footer "↑↓ to
    move", "Enter to open", "Esc to close", "> commands only · @ symbols · :
    line".

"1 warning" is built as `count + ' warning'` (`:717`); the real string needs
plural forms.

## Syntax palette and style scheme

### Tokens

The tokeniser (`Code.dc.html:337-365`) assigns:

| Class | Token | Light | Dark | Rule in the artboard |
| --- | --- | --- | --- | --- |
| `.t-p` | `--fg` | `#1d1d21` | `#f4f4f6` | Plain text, punctuation |
| `.t-k` | `--k` | `#813d9c` | `#dc8add` | Keywords. JS list includes `this`, `null`, `true`, `false`; Rust list includes `self`, `Self`, `Ok`, `Err`, `Some`, `None`. Markdown list marker |
| `.t-s` | `--s` | `#1b7a43` | `#8ff0a4` | String literals; Markdown inline code |
| `.t-f` | `--f` | `#1a5fb4` | `#99c1f1` | Any identifier followed by `(`: calls and declarations |
| `.t-n` | `--n` | `#b04000` | `#ffa348` | Integer literals |
| `.t-ty` | `--ty` | `#0e6f82` | `#93ddc2` | Identifiers that start with a capital letter |
| `.t-c` | `--c` | `rgba(29,29,33,.5)` | `rgba(244,244,246,.5)` | `//` comments, italic |
| `.t-h` | `--f`, 700 | | | Markdown headings |

Editor surface tokens:

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--line` | `rgba(0,0,10,.035)` | `rgba(255,255,255,.04)` | Current line |
| `--exec` | `rgba(229,165,10,.2)` | `rgba(248,228,92,.14)` | Paused execution line |
| `--sel` | `rgba(0,0,10,.08)` | `rgba(255,255,255,.1)` | Selected list rows (tree, outline, completion, palette, frames); not text selection |
| `--mod` | `#b04000` | `#ffa348` | Modified dot in tree; deletion counts |
| `--add` | `#1b7a43` | `#8ff0a4` | Added lines, addition counts, success |
| `--pop` | `#ffffff` | `#2e2e33` | Overlays |

### GtkSourceView 5 style scheme

Ship two schemes, `apex-light` and `apex-dark`, with GtkSourceView 5 variant
metadata so Builder picks the one that matches the dark style. Install to
`/usr/share/gtksourceview-5/styles/` for an RPM build; a Flatpak build cannot
read the host directory and must bundle the schemes (see AC-2). Text Editor
reads the same directory, so the Markdown rules also serve Text Editor (its
artboard uses `--md-head` and `--md-code`, which differ; see AC-9).

Use opaque, precomposed colours for every translucent token. Precomposed over
`--view` (`#ffffff` light, `#1e1e21` dark):

| Style name | Light | Dark | From |
| --- | --- | --- | --- |
| `text` | fg `#1d1d21`, bg `#ffffff` | fg `#f4f4f6`, bg `#1e1e21` | `--fg`, `--view` |
| `current-line` | bg `#f6f6f6` | bg `#27272a` | `--line` |
| `line-numbers` | fg `#a5a5a6`, bg `#ffffff` | fg `#747476`, bg `#1e1e21` | `--faint` |
| `current-line-number` | fg `#1d1d21` | fg `#f4f4f6` | `--fg` |
| `cursor` | `--accent` (see below) | | `--accent` |
| `def:keyword`, `def:special-constant`, `def:boolean` | `#813d9c` | `#dc8add` | `--k` |
| `def:string`, `def:special-char` | `#1b7a43` | `#8ff0a4` | `--s` |
| `def:function` | `#1a5fb4` | `#99c1f1` | `--f` |
| `def:number`, `def:decimal`, `def:base-n-integer`, `def:floating-point` | `#b04000` | `#ffa348` | `--n` |
| `def:type` | `#0e6f82` | `#93ddc2` | `--ty` |
| `def:comment`, `def:doc-comment` | `#8e8e90`, italic | `#89898c`, italic | `--c` |
| `def:heading` / `markdown:header` | `#1a5fb4`, bold | `#99c1f1`, bold | `.t-h` |
| `markdown:list-marker` | `#813d9c` | `#dc8add` | `.t-k` |
| `markdown:code-span`, `markdown:code-block` | `#1b7a43` | `#8ff0a4` | `.t-s` |
| `search-match` | bg `#cfe1f9` (blue) | bg `#243650` (blue) | `--accent` 24 % |
| `selection` | bg `#9ac2f2` (blue) | bg `#2a5182` (blue) | `.t-mc` (`--accent` 50 %); proposal, not drawn |
| `map-overview` / map slider (CSS) | `#eeeeef` | `#323235` | `--btn` |
| `right-margin`, `draw-spaces` | `#e8e8e9` | `#303033` | `--border`; not drawn |

Builder-private style names (verify the exact names in the Builder source for
the shipped version; they live in the editor, git and debugger plugins):

| Purpose | Light | Dark | From |
| --- | --- | --- | --- |
| VCS added line | `#1b7a43` | `#8ff0a4` | `--add` |
| VCS changed line | `--accent` as drawn, or `#b04000` / `#ffa348` if `--mod` is chosen (AC-6) | | `Code.dc.html:516` |
| VCS removed line | not drawn | | |
| Debugger current line | bg `#faedce` | bg `#3d3a29` | `--exec` |
| Breakpoint | `#c01c28` | `#ff7b7b` | `--err` |
| Diagnostic warning underline | `#9c6e03` | `#f8e45c` | `--warn` |
| Diagnostic error underline | `#c01c28` | `#ff7b7b` | `--err` |

Accent-dependent colours (`cursor`, `search-match`, `selection`, VCS changed
line) cannot follow the libadwaita accent from a static scheme. Either ship
nine scheme pairs and switch on `accent-color` (patch, small), or have
Builder override those styles at runtime (patch, small), or fix them to blue.
Precomposed values for all nine accents at 24 % / 50 %:

| Accent | Light 24 % | Light 50 % | Dark 24 % | Dark 50 % |
| --- | --- | --- | --- | --- |
| blue | `#cfe1f9` | `#9ac2f2` | `#243650` | `#2a5182` |
| teal | `#cae4e9` | `#90c8d2` | `#1f3940` | `#205762` |
| green | `#d0e5d4` | `#9ccaa4` | `#253a2b` | `#2c5936` |
| yellow | `#f2e2c2` | `#e4c480` | `#473719` | `#735310` |
| orange | `#fbd8c2` | `#f6ad80` | `#502d19` | `#863c10` |
| red | `#f9cdd2` | `#f296a0` | `#4e2229` | `#822632` |
| pink | `#f5d9e7` | `#eab0cc` | `#4a2e3e` | `#7a405d` |
| purple | `#e5d1eb` | `#c8a0d6` | `#3a2642` | `#583066` |
| slate | `#dce1e6` | `#b7c1ca` | `#31363d` | `#46505c` |

Fidelity gaps: GtkSourceView's JavaScript and Rust grammars do not colour
every call site as a function or every capitalised identifier as a type, as
the artboard's regex tokeniser does. Matching the artboard needs LSP semantic
tokens in Builder (patch, medium) or accepting the grammar's output.

## Tokens used

*   Colour, surface: `--view`, `--side`, `--head`, `--pop`, `--wall`.
*   Colour, content: `--fg`, `--dim`, `--faint`, `--border`.
*   Colour, control: `--btn`, `--btn-h`, `--sel`.
*   Colour, status: `--err`, `--warn`, `--warn-bg`, `--mod`, `--add`,
    `--exec`.
*   Colour, syntax: `--k`, `--s`, `--f`, `--n`, `--ty`, `--c`, `--line`.
*   Colour, shell (top bar only): `--bar`, `--bar-fg`, `--shadow`.
*   Accent: `--accent`, with `color-mix` at 24 % and 50 %.
*   Literals with no token: `#fff` on accent fills; `rgba(0,0,0,.12)` switcher
    shadow; `color-mix(in srgb, var(--accent) 24%, transparent)`.
*   Type: UI family Inter; mono JetBrains Mono 400/600. Sizes used: 10.5,
    11, 11.5, 12, 12.5, 13, 13.5, 14 px. 10.5 px (ACP badge) has no token.
    Weights 400, 500, 600, 700, 800. Editor line height 21 px and panel 20
    px; tokens.json now lists both (AC-7).
*   Radius: 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 14 px and 50 %. Of these only 2
    (`hairline`), 8 (`sm`), 10 (`md`), 12 (`pill-bar`), 14 (`window`) and
    50 % (`circle`) are tokens; 5, 6, 7 and 9 px are literals.
*   Shadow: `window` on the window; overlays use `var(--shadow), 0 0 0 1px
    var(--border)` (no token name); focus ring `inset 0 0 0 2px
    var(--accent)` on the search field and find field.
*   Glass: top bar only (`blur(24px) saturate(160%)`); the app has none.
*   Motion: none drawn.

## Build classification

| Element | Class | Why / cost |
| --- | --- | --- |
| Window frame, header layout, tabs, panes, toggles | Theme | libadwaita / libpanel CSS |
| Sidebar view switcher as a segmented control | Theme | Restyle libpanel's frame switcher; check that it accepts a text-free segmented look |
| Run split button, close-only window controls | Stock + theme | |
| Build button in header | Patch (S) | New header button bound to the build action |
| Omnibar content and status strings | Patch (S) | "Built 12 s ago", "Paused at …" |
| Omnibar opens the palette, Ctrl K | Patch (S) + settings | Rebind global search; check conflicts with existing Ctrl K uses |
| Palette sections, fuzzy highlight, key chips, prefixes | Patch (S to M) | Global search exists; sectioning, prefixes and accelerator chips are new |
| Project tree, modified dot | Theme + patch (S) | Dot renderer |
| Outline as a sidebar pane | Patch (M) | Port the symbol tree into a pane with current-symbol tracking |
| Find in files in the sidebar | Theme + settings | Dock the grep pane in the start area |
| Open results as one buffer | Patch (L) | Needs a multi-excerpt buffer; nothing in GtkSourceView to reuse. Consider dropping |
| Version control pane with commit | Patch (L) | New git pane: status, stage, commit, branch |
| Editor colours | Theme | Two style schemes (above) |
| Gutter: numbers, VCS bar, breakpoints | Theme | Style scheme + CSS for column widths |
| Fold chevrons | Patch (L) | GtkSourceView has no folding. Recommend dropping from v1 |
| Minimap | Settings + theme | Enable the overview map; set width; restyle slider |
| Completion popover and details | Theme + patch (S) | Letter kind glyphs instead of icons; details pane on by default |
| Inline diagnostic pill | Patch (M) | End-of-line annotation renderer |
| Reference counts | Patch (M to L) | LSP code lens or reference queries per symbol |
| Inline blame | Patch (M) | If the shipped Builder lacks it: libgit2 blame in the git daemon + annotation renderer |
| Find and replace card | Theme or patch (S) | Builder's search bar is a full-width bar; a floating card may need a layout change |
| Debugger toolbar in the editor | Patch (S to M) | Move or duplicate controls into an editor overlay |
| Debugger variables and call stack side by side | Patch (S) | Combine two panes |
| Runtime chip in panel | Patch (S) | |
| Status bar warning count and LSP status | Patch (S) | |
| Agent panel | Patch (L) | New ACP client plugin; see Agent panel cost |
| App name "Apex Code" with app id `org.gnome.Builder` | Patch (S) | Desktop file `Name=`, about dialog, window title |

## Accessibility

Contrast, computed from the tokens (WCAG 2.x):

| Pair | Light | Dark | Verdict |
| --- | --- | --- | --- |
| Keywords, strings, functions, numbers, types on `--view` | 5.4 to 6.8:1 | 6.9 to 12.0:1 | Pass AA |
| Comments (`--c`) on `--view` | 3.3:1 | 4.8:1 | Light fails AA. Raise light `--c` alpha to at least .6 |
| Line numbers (`--faint`) on `--view` | 2.5:1 | 3.6:1 | Fails AA for text |
| `--dim` on `--side` | 4.5:1 | 6.2:1 | Pass, light at the edge |
| `--warn` on `--warn-bg` (diagnostic pill) | 4.1:1 | 10.0:1 | Light fails AA at 12 px |
| `#fff` on `--accent` (Commit, Accept, user bubble) | 3.0:1 (yellow) to 5.9:1 (purple); blue 3.8:1 | same | Fails AA for 12.5 to 13 px text on most accents; inherited from libadwaita |
| `--accent` text (`.t-q` matches) on `--pop` dark | 2.3:1 (purple) to 4.5:1 (yellow); blue 3.6:1 | | Low. Use libadwaita's foreground accent colour for text, not the fill colour |

Other requirements:

*   Focus order: header (sidebar toggle, run, run options, build, omnibar,
    agent, bottom panel, menu, close), sidebar switcher, sidebar content,
    tabs, editor, bottom panel tabs, panel content, status bar items, agent
    panel.
*   Keyboard: Ctrl K opens the palette; Up/Down move; Enter opens; Esc closes
    and returns focus to the editor. Find popover: Enter next, Shift+Enter
    previous, Esc close. Debugger keys are not drawn; keep Builder's existing
    accelerators. Escape closes completion.
*   Screen reader: keep the artboard's names (aria labels above). The
    sidebar switcher is a tab list; tree and outline are trees with selected
    state; completion and palette are list boxes with selected option. Modified
    dot, unsaved dot and the "›" paused marker need text equivalents
    ("Modified", "Unsaved changes", "Paused here"). Announce streamed agent
    replies and "Paused at engine.rs:14" with GTK accessible announcements.
*   Large text: header, tab and row heights are fixed in the artboard; they
    must grow with the text scaling factor. Editor font size is Builder's own
    setting.
*   Reduced motion: no animation is drawn. Honour `gtk-enable-animations`.
*   High contrast: libadwaita high-contrast mode; the style schemes need a
    high-contrast pair or must fall back to Adwaita's.

## Acceptance criteria

1.  The window opens at the artboard's proportions with a 47 px header bar,
    264 px sidebar, 40 px tab bar, 28 px status bar and, when shown, 206 px
    bottom panel and 344 px agent panel (logical px, measured on a
    screenshot at scale 1).
2.  The header shows, left to right: sidebar toggle, Run split button, Build,
    a centred 440 px omnibar with project, branch, status and "Ctrl K", then
    Agent, Bottom panel, Main menu and a single round Close button.
3.  Pressing Ctrl K or clicking the omnibar opens a 600 px palette 10 px
    below the header, with Files, Symbols and Commands sections, the first
    result selected, and fuzzy-matched characters in the accent colour; Esc
    closes it and returns focus to the editor.
4.  Typing `>` first in the palette limits results to commands, `@` to
    symbols and `:` jumps to a line number.
5.  The sidebar switcher shows Project, Outline, Search and Version control;
    the active segment has the `--view` fill; Version control shows the
    number of changed files.
6.  In a dirty git checkout, modified files show a 7 px `--mod` dot in the
    project tree, and changed lines show a 4 px bar in the gutter (added
    `--add`; modified per AC-6's decision).
7.  The editor uses JetBrains Mono 13 px with 21 px line height; line
    numbers are `--faint` and the cursor line number is `--fg`; the cursor
    line has the `current-line` background from the scheme table.
8.  With `dark` style the editor switches to `apex-dark` without restart, and
    every syntax colour matches the scheme table (eyedropper on a sample
    file per language: JavaScript, Rust, Markdown).
9.  The minimap is 72 px wide, draws one 4 px row per line, and its viewport
    box tracks the visible range.
10. Typing `this._fo` in a JS file with typescript-language-server running
    shows a completion popover with a 300 px list and a 250 px details pane;
    Enter inserts the selected item.
11. Ctrl F opens find with match count "N of M"; all matches get the 24 %
    accent fill; the current match gets the 50 % fill and a 1 px accent
    ring; Replace and All work; Aa, Whole word and `.*` toggle.
12. Starting the debugger on a Rust binary inside the toolbox stops at a
    breakpoint, paints the line with `--exec`, shows "›", changes Run to
    "Continue", shows Stop, shows "Paused · <target> · gdb" in the status
    bar, and opens the Debugger tab with Variables and Call stack side by
    side.
13. Each debugger toolbar button (Continue, Step over, Step into, Step out,
    Restart, Stop) performs its action and has an accessible name.
14. The bottom panel shows a runtime chip naming the active toolbox or
    Flatpak runtime, and tabs for Terminal, Build and Diagnostics with a
    count.
15. The status bar shows the problem count with correct plural forms ("1
    warning", "2 warnings", "No problems"), the LSP name with a green dot
    when running, cursor position, indentation, encoding and language.
16. The agent toggle shows and hides the agent panel; with no agent
    installed the panel shows an install or setup state instead of a broken
    thread.
17. An agent edit appears as a diff card with Accept and Review; Accept
    applies the edit to the buffer as one undoable step; with "Ask before
    edits" no file changes until Accept.
18. All contrast pairs in the Accessibility table meet the stated targets
    after the agreed token changes.
19. Orca reads every header button, sidebar tab, tree item (with
    modified state), tab (with unsaved state), palette option and debugger
    button by the names listed in Copy.

## Open questions

These questions are tracked in [../OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md),
which gives each a global `OQ-nn` ID and maps the local IDs used here.

*   **AC-1**: Is the agent panel in scope for v1? It is the most expensive
    item (two engineers, 8 to 12 weeks), depends on a third-party agent the
    user installs and signs in to, and shows a third-party product name.
*   **AC-2**: Builder delivery: RPM in the bootc image or an Apex Flatpak?
    Every patch requires a downstream build, and keeping app id
    `org.gnome.Builder` collides with Flathub's Builder. Style schemes and
    the icon install path depend on this answer.
*   **AC-3**: Drop or keep fold chevrons ("needs folding in GtkSourceView"),
    "Open 6 results as one buffer" (multi-buffer) and reference counts? Each
    is large.
*   **AC-4**: Version control pane: confirm the scope (stage, unstage,
    commit, push, branch switch, conflicts). None is drawn beyond the commit
    box and a change list.
*   **AC-5**: Should accent-dependent editor colours follow the system
    accent? Needs nine scheme pairs or a runtime override.
*   **AC-6**: Modified lines in the gutter use `--accent`
    (`Code.dc.html:516`) while the tree dot uses `--mod` (`:92`) and
    deletion counts use `--mod` (`:137`, `:268`). Which colour means
    "modified", and should deletions be red (`--err`)?
*   **AC-7**: Editor line height is 21 px (`Code.dc.html:155`) and panel 20
    px (`:240`); `tokens.json` first said "24px (mono, editor)" and now
    records 21 px and 20 px.
*   **AC-8**: Status colours in Code differ from other artboards: `--warn`
    light `#9c6e03` vs `#9c6500`, dark `#f8e45c` vs `#f8c454`; `--err` dark
    `#ff7b7b` vs `#ff7b63`; `--warn-bg` (`Code.dc.html:17-18`, recorded as
    conflicts in `tokens.json`). Pick one set.
*   **AC-9**: Markdown headings and code in Code (`--f`, `--s`) differ from
    Text Editor's `--md-head` / `--md-code` (Desktop). Both apps read the
    same style scheme directory; one scheme or two?
*   **AC-10**: Old-spec and version-bound text: runtime "fedora-toolbox-45"
    (`Code.dc.html:225`, `:684`), deployment versions "45.20261102.0" and
    "45.20261030.1" (`:633`). The chip must show the real runtime name.
*   **AC-11**: The debug tweak only works when `file` is `engine.rs`
    (`Code.dc.html:329`), and completion only for `dock.js` (`:489`). Fine
    for a mock-up; confirm they are not product rules.
*   **AC-12**: Default keyboard shortcut set: only Ctrl K and Ctrl Enter are
    drawn. Confirm the rest stay Builder defaults.
*   **AC-13**: Sample-data mismatches, for whoever refreshes the canvas: the
    find popover says "2 of 3" but `pin_rollback` occurs once in
    `engine.rs` (line 26, `:481`), which is off screen in artboard 42
    (visible lines 6 to 24); the search group says "4" for dock.js but lists
    3 hits and the file has 5 occurrences; the dock.js diagnostic on line 4
    is never on screen in any tweak combination.
