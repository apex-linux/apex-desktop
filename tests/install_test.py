"""Tests the `just install <destdir>` contract that apex-image relies on."""

import pathlib
import subprocess
import tempfile
import unittest

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_INSTALL = _ROOT / "scripts" / "install.sh"


def run_install(destdir: pathlib.Path) -> None:
    """Runs the install script into destdir and fails on a non-zero exit."""
    subprocess.run([str(_INSTALL), str(destdir)], check=True)


class InstallTest(unittest.TestCase):

    def test_writes_only_under_usr(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destdir = pathlib.Path(tmp)
            run_install(destdir)
            self.assertEqual([path.name for path in destdir.iterdir()], ["usr"])

    def test_installs_the_licence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destdir = pathlib.Path(tmp)
            run_install(destdir)
            self.assertTrue(
                (destdir / "usr/share/licenses/apex-desktop/LICENSE").is_file()
            )

    def test_installs_the_generated_desktop(self) -> None:
        extension = "usr/share/gnome-shell/extensions/apex@apex-linux.github.io"
        expected = [
            f"{extension}/metadata.json",
            f"{extension}/extension.js",
            f"{extension}/dock.js",
            f"{extension}/topBar.js",
            f"{extension}/windowWatcher.js",
            f"{extension}/stylesheet-light.css",
            f"{extension}/stylesheet-dark.css",
            f"{extension}/schemas/gschemas.compiled",
            "usr/share/glib-2.0/schemas/zz0-apex.gschema.override",
            "usr/share/gnome-background-properties/apex.xml",
            "usr/share/backgrounds/apex/facets-l.svg",
            "usr/share/backgrounds/apex/facets-d.svg",
            "usr/share/apex-desktop/gtk-4.0/gtk.css",
            "usr/share/icons/Apex/index.theme",
            "usr/share/icons/Apex/symbolic/network-wireless-symbolic.svg",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            destdir = pathlib.Path(tmp)
            run_install(destdir)
            for name in expected:
                with self.subTest(name):
                    self.assertTrue((destdir / name).is_file())

    def test_keeps_icon_aliases_as_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destdir = pathlib.Path(tmp)
            run_install(destdir)
            alias = destdir / (
                "usr/share/icons/Apex/symbolic/"
                "network-wireless-signal-good-symbolic.svg"
            )
            self.assertTrue(alias.is_symlink())
            self.assertTrue(alias.resolve().is_file())

    def test_rejects_a_missing_destdir(self) -> None:
        result = subprocess.run([str(_INSTALL)], check=False)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
