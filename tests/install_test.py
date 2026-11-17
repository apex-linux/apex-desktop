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

    def test_rejects_a_missing_destdir(self) -> None:
        result = subprocess.run([str(_INSTALL)], check=False)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
