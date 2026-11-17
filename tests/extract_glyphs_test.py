"""Tests reading the glyph list out of a contact sheet without running it."""

import pathlib
import tempfile
import unittest

from apex_desktop.entrypoints import extract_glyphs


def _sheet(body: str) -> str:
    return f"<script>\n    const GL = [\n{body}\n    ];\n</script>"


class GlyphListTest(unittest.TestCase):

    def test_reads_both_quote_styles(self) -> None:
        html = _sheet(
            "      ['Group', [\n"
            "        ['go-down', 'Down', 'M8 2.5v10', '', ''],\n"
            '        ["go-up", "Up", "M8 13.5v-10", "", ""]\n'
            "      ]]"
        )
        self.assertEqual(
            extract_glyphs.glyph_list(html),
            [
                [
                    "Group",
                    [
                        ["go-down", "Down", "M8 2.5v10", "", ""],
                        ["go-up", "Up", "M8 13.5v-10", "", ""],
                    ],
                ]
            ],
        )

    def test_rejects_code(self) -> None:
        html = _sheet("      ['Group', [bat(10)]]")
        with self.assertRaises(extract_glyphs.SheetError):
            extract_glyphs.glyph_list(html)

    def test_rejects_two_drawings_for_one_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = pathlib.Path(tmp)
            for index, sheet in enumerate(extract_glyphs.SHEETS):
                (project / sheet).write_text(
                    _sheet(f"['G', [['x', 'X', 'M{index} 1h1', '', '']]]"),
                    encoding="utf-8",
                )
            with self.assertRaises(extract_glyphs.SheetError):
                extract_glyphs.extract(project)


if __name__ == "__main__":
    unittest.main()
