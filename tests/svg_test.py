"""Tests the SVG sanitiser that guards canvas assets."""

import unittest

from apex_desktop.kernel import svg

_HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">'


class SanitizeTest(unittest.TestCase):

    def test_keeps_geometry_and_paint(self) -> None:
        clean = svg.sanitize(
            f'{_HEAD}<rect width="4" height="4" rx="1" fill="#e8ebf0"/></svg>'
        )
        self.assertIn('<rect width="4" height="4" rx="1" fill="#e8ebf0"', clean)

    def test_drops_metadata_and_empty_images(self) -> None:
        clean = svg.sanitize(
            '<svg xmlns="http://www.w3.org/2000/svg"'
            ' xmlns:c2pa="http://c2pa.org/manifest">'
            "<metadata><c2pa:manifest>AAAA</c2pa:manifest></metadata>"
            '<image width="60" height="62"/><path d="M0 0h1"/></svg>'
        )
        self.assertNotIn("metadata", clean)
        self.assertNotIn("c2pa", clean)
        self.assertNotIn("<image", clean)
        self.assertIn('<path d="M0 0h1"', clean)

    def test_drops_editor_namespaces(self) -> None:
        clean = svg.sanitize(
            '<svg xmlns="http://www.w3.org/2000/svg"'
            ' xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">'
            '<path inkscape:label="x" d="M0 0h1"/></svg>'
        )
        self.assertNotIn("inkscape", clean)

    def test_is_idempotent(self) -> None:
        once = svg.sanitize(
            f'{_HEAD}<g transform="rotate(45)"><rect/></g></svg>'
        )
        self.assertEqual(svg.sanitize(once), once)

    def test_rejects_unsafe_content(self) -> None:
        cases = {
            "script": f"{_HEAD}<script>alert(1)</script></svg>",
            "event": f'{_HEAD}<rect onload="alert(1)"/></svg>',
            "foreign": f"{_HEAD}<foreignObject/></svg>",
            "use": f'{_HEAD}<use href="other.svg#a"/></svg>',
            "data uri": f'{_HEAD}<rect fill="url(data:x)"/></svg>',
            "external url": f'{_HEAD}<rect fill="url(http://x/a)"/></svg>',
            "doctype": f'<!DOCTYPE svg [<!ENTITY a "b">]>{_HEAD}</svg>',
            "not svg": "<html/>",
            "broken": f"{_HEAD}<rect>",
        }
        for name, text in cases.items():
            with self.subTest(name):
                with self.assertRaises(svg.UnsafeSvgError):
                    svg.sanitize(text)

    def test_allows_local_paint_references(self) -> None:
        clean = svg.sanitize(f'{_HEAD}<rect fill="url(#g)"/></svg>')
        self.assertIn('fill="url(#g)"', clean)


if __name__ == "__main__":
    unittest.main()
