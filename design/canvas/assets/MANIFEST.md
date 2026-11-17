# Canvas assets manifest

The 36 SVG assets uploaded to the "Apex Fedora Mockups" design canvas
(the owner's private canvas), saved here under their blob
id. Artboards reference each one as `/_blob/<id>`. Pulled on 2026-11-17.

Names are ours: taken from the `alt` text or the app name the artboard code gives
the asset. All files are `image/svg+xml`. "Used by" lists artboard files in
`../project/` without the `.dc.html` suffix.

Treat these files as untrusted input: they were uploaded by a canvas co-writer.
Sanitise (for example with `scour` or `svgo`) before shipping any of them.

## Summary

*   2 wallpapers (light and dark variant of one design, 2880x1800).
*   2 shell icons (Show Apps, Trash).
*   29 app icons (64x64), all in the same rounded-tile style.
*   3 app icons that no artboard references.

## Assets

| Name | Blob id | Type | Size (px) | Bytes | SHA-256 (prefix) | Used by | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `wallpaper-apex-default-dark` | `f607332583898d73d053baf1c0cae872` | Wallpaper | 2880x1800 | 765 | `a1fe8b753fd0` | 32 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, Code, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, GlyphActions, GlyphFamilies, GlyphMore, Glyphs, Indicators, Launcher, Lock, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Tiling, Transients, Updates, Welcome, WifiMenu | Default wallpaper, dark. `--wall` in `.apx-d`; `.wall-d`. |
| `wallpaper-apex-default-light` | `3d451127dc2b77221bac98465ee1ec99` | Wallpaper | 2880x1800 | 765 | `8f617957aff8` | 33 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, Code, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, GlyphActions, GlyphFamilies, GlyphMore, Glyphs, Indicators, Launcher, Lock, Main, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Tiling, Transients, Updates, Welcome, WifiMenu | Default wallpaper, light. `--wall` in `.apx-l`; `.wall-l`; GDM greeter background. |
| `shell-show-apps` | `87f74383f084182b8b000aef0f7cb871` | Shell icon | 64x64 | 14574 | `b2967185846e` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | "Show Apps" grid button at the end of the dock. |
| `shell-trash` | `8bef24670debcc9a315a476be8c9a7b4` | Shell icon | 64x64 | 8781 | `e673d0ad190d` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Trash in the dock (Desktop `showTrash` tweak). |
| `app-audio-player` | `1d6c04a7a3e82a19b16cf0adcb706230` | App icon | 64x64 | 2834 | `1734fa5932cf` | Launcher | Audio Player (Decibels). Launcher. |
| `app-bazaar` | `f45103bf26742914e3e3e55be00d0f25` | App icon | 64x64 | 6609 | `c0433ebe0665` | 23 artboards: AltTab, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Bazaar (Flatpak store). Dock. Missing from both Apex Desktop artboards. |
| `app-calculator` | `a4bbb92f85ddabb4acd30339e1c5db82` | App icon | 64x64 | 1643 | `e5132f65f825` | Launcher, Spotlight | Calculator. Launcher grid; Spotlight calculator scene. |
| `app-calendar` | `5971067e1001a6a8052d7fdc7d2df366` | App icon | 64x64 | 10407 | `c9eaf1b06580` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Calendar. Dock. |
| `app-camera` | `7ff4d256cc532fdac896266fcc6af5d9` | App icon | 64x64 | 1043 | `d7b3bce0ec4b` | Launcher, Spotlight | Camera (Snapshot). Launcher. |
| `app-characters` | `f7d96d4c39142f2631e06906f7974d30` | App icon | 64x64 | 1629 | `c1338551c4de` | Launcher, Spotlight | Characters. Launcher Utilities folder. |
| `app-clocks` | `e5ecb308a409db59bffaf2869ac6d455` | App icon | 64x64 | 3379 | `b208abb3f701` | Launcher | Clocks. Launcher. |
| `app-contacts` | `efec7a0b7b7ca359084632c994ed34ba` | App icon | 64x64 | 2151 | `259b22c23bc9` | Launcher, Spotlight | Contacts. Launcher. |
| `app-disk-usage-analyzer` | `b41f8f6b8ed45a0cfdb4f534a6e7f8e6` | App icon | 64x64 | 1066 | `1f8a31d05f3c` | Launcher, Spotlight | Disk Usage Analyzer (Baobab). Launcher Utilities folder. |
| `app-disks` | `b72c21767fe5f13da8acdefc5021d72c` | App icon | 64x64 | 11555 | `8acd72a7b882` | Launcher, Spotlight | Disks. Launcher Utilities folder. |
| `app-document-viewer` | `bc02ebfe989b26d9d2647d86293251e5` | App icon | 64x64 | 1793 | `9a269b61849b` | Launcher, Spotlight | Document Viewer (Papers). Launcher. |
| `app-extensions` | `3bc3f3740bcb034f3d5c5084dd0efa97` | App icon | 64x64 | 1164 | `42a3dfcd3778` | Launcher | Extensions. Launcher. |
| `app-files` | `906e097066ea63ae52a6eb768e945cad` | App icon | 64x64 | 10227 | `d7a66833f858` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Files (Nautilus). Dock. |
| `app-firmware` | `d96660b5aa756ef13b4722f21e42a5e0` | App icon | 64x64 | 5170 | `a8649b9b738b` | Launcher | Firmware. Launcher. |
| `app-fonts` | `8d834efee70c9699249917f2f7cdd8f3` | App icon | 64x64 | 3298 | `b182f64ddba5` | Launcher, Spotlight | Fonts. Launcher Utilities folder. |
| `app-help` | `e8c9a43c549d00652a4455c09ef3ef04` | App icon | 64x64 | 1671 | `0705a0ea350a` | Launcher | Help. Launcher. |
| `app-image-viewer` | `20ab5f44d76b65cf99affe84d1293bd9` | App icon | 64x64 | 2253 | `395a6647e0da` | DateMenu, Desktop, Launcher, Spotlight | Image Viewer (Loupe). Launcher; notification/app source in Calendar and Desktop. |
| `app-logs` | `4d76f5dc44b52dde01b23a3786c8e631` | App icon | 64x64 | 2452 | `bb39fcbef0af` | Launcher, Spotlight | Logs. Launcher Utilities folder. |
| `app-mail` | `74c5be1bf3391d62837391fc3600077f` | App icon | 64x64 | 9229 | `7274e28b9b70` | ApexDesktop, ApexDesktopScrolled | Mail. Only in the dock preview of Settings > Apex Desktop; the main dock has no Mail. |
| `app-maps` | `0d61a941b51cdd7825627f8d78d09f59` | App icon | 64x64 | 10850 | `ac29369f8359` | Launcher, Spotlight | Maps. Launcher. |
| `app-music` | `e11cf854dc88b66ebd8892a3a85856bb` | App icon | 64x64 | 14702 | `6fbcb28b3ce6` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Music. Dock. |
| `app-settings` | `b105969ffb60fc5d63264cdac68e254e` | App icon | 64x64 | 15174 | `f0b01095b75e` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Settings. Dock. |
| `app-software` | `91d271bbd5c894bdd2ed6a39ef85e177` | App icon | 64x64 | 10193 | `1ec51c297db0` | ApexDesktop, ApexDesktopScrolled, EndSession, Transients | Software. In the dock preview of Settings > Apex Desktop (where the main dock has Bazaar), and as the decorative source icon (empty `alt`) of the Apex Updates banner (Transients) and the Power Off dialog (EndSession). |
| `app-system-monitor` | `4aec024e9d7a9eff99a2749451dd4193` | App icon | 64x64 | 6281 | `f61e0293391c` | Launcher, Spotlight | System Monitor. Launcher Utilities folder. |
| `app-terminal` | `96c3f6cf72bce44f603578c27bfdc3a0` | App icon | 64x64 | 8891 | `3dd8a7b3600e` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Terminal (Ptyxis-style). Dock. |
| `app-text-editor` | `f55cc3350da8a870bf8ad2a2a8bf0251` | App icon | 64x64 | 18047 | `3591d69d1542` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Text Editor. Dock. |
| `app-videos` | `aaf8912c2a91f2571a403beb97a67117` | App icon | 64x64 | 3319 | `5a082d7e3652` | Launcher, Spotlight | Videos (Showtime). Launcher. |
| `app-weather` | `5f54e8cc8613fd3b87eb06344282c2d1` | App icon | 64x64 | 1092 | `f43278aa9fdf` | Launcher, Spotlight | Weather. Launcher. |
| `app-web` | `91d42915e99e4ac92159fd8c768573f3` | App icon | 64x64 | 11288 | `bcb4c18c98a6` | 25 artboards: AltTab, ApexDesktop, ApexDesktopScrolled, Appearance, DateMenu, Desktop, EndSession, Files, FilesList, FilesSearch, Fingerprint, Indicators, Launcher, Overview, Polkit, Power, Rollback, Screenshot, Spotlight, Terminal, TerminalSplit, Transients, Updates, Welcome, WifiMenu | Web (Epiphany). Dock. |
| `unreferenced-blue-globe` | `8a791f1bd49462a5c0f30fae49858af9` | App icon (unreferenced) | 64x64 | 13013 | `e12add2467cc` | none | Not referenced by any artboard. Blue tile with a white globe mark. Identity unknown. |
| `unreferenced-red-flame` | `2dd02531f4f80b74eb6420659b4c3825` | App icon (unreferenced) | 64x64 | 3565 | `2b60c509a641` | none | Not referenced by any artboard. Light tile with a red flame mark; probably Firefox, which the Launcher notes say ships "on request". Identity unconfirmed. |
| `unreferenced-teal-paw` | `483418a71ce28c18f8452b2bbcfb07c3` | App icon (unreferenced) | 64x64 | 1316 | `9081a017679e` | none | Not referenced by any artboard. Teal tile with a white paw-print mark. Identity unknown. |

## Dock order

Every artboard with a dock (except the two Settings > Apex Desktop previews) draws
the same order, left to right:

Files, Web, Calendar, Music, Text Editor, Terminal, Bazaar, Settings, separator,
Show Apps, Trash.

Settings > Apex Desktop previews a different dock: Files, Web, Mail, Calendar,
Music, Text Editor, Terminal, Software, Settings. See `../../OPEN-QUESTIONS.md`.
