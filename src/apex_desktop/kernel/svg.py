"""Sanitises SVG files that come from the design canvas.

Canvas assets were uploaded by a co-writer, so they are untrusted. The
sanitiser parses a file and writes it back from an allowlist of elements
and attributes. Anything that can run code or reach outside the file makes
it fail; metadata and empty bitmap placeholders are dropped.
"""

import re
from xml.etree import ElementTree

_SVG_NS = "http://www.w3.org/2000/svg"

_ELEMENTS = frozenset(
    {
        "svg",
        "g",
        "defs",
        "path",
        "rect",
        "circle",
        "ellipse",
        "line",
        "polyline",
        "polygon",
        "linearGradient",
        "radialGradient",
        "stop",
        "title",
    }
)

# Dropped without complaint: they carry no picture.
_DROPPED = frozenset({"metadata", "desc", "image"})

# Make the whole file fail: they run code, embed documents or fetch data.
_FORBIDDEN = frozenset(
    {
        "script",
        "foreignObject",
        "iframe",
        "use",
        "a",
        "animate",
        "set",
        "style",
    }
)

_ATTRIBUTES = frozenset(
    {
        "id",
        "width",
        "height",
        "viewBox",
        "x",
        "y",
        "x1",
        "y1",
        "x2",
        "y2",
        "cx",
        "cy",
        "r",
        "rx",
        "ry",
        "fx",
        "fy",
        "d",
        "points",
        "transform",
        "fill",
        "fill-rule",
        "fill-opacity",
        "stroke",
        "stroke-width",
        "stroke-linecap",
        "stroke-linejoin",
        "stroke-opacity",
        "opacity",
        "offset",
        "stop-color",
        "stop-opacity",
        "gradientUnits",
        "gradientTransform",
        "clip-rule",
    }
)

_URL_REF = re.compile(r"url\((?!#)", re.IGNORECASE)


class UnsafeSvgError(ValueError):
    """Raised when a file contains something the sanitiser will not ship."""


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _clean(source: ElementTree.Element) -> ElementTree.Element:
    name = _local(source.tag)
    if name in _FORBIDDEN or name not in _ELEMENTS:
        raise UnsafeSvgError(f"element <{name}> is not allowed")
    target = ElementTree.Element(name)
    for key, value in source.attrib.items():
        attribute = _local(key)
        if attribute.startswith("on"):
            raise UnsafeSvgError(f"event attribute {attribute} on <{name}>")
        if "data:" in value or _URL_REF.search(value):
            raise UnsafeSvgError(f"external reference in {attribute}")
        if attribute in _ATTRIBUTES and "}" not in key:
            target.set(attribute, value)
    if name == "title" and source.text:
        target.text = source.text
    for child in source:
        if _local(child.tag) in _DROPPED:
            continue
        target.append(_clean(child))
    return target


def sanitize(text: str) -> str:
    """Returns a clean copy of an SVG document.

    Args:
        text: the SVG file's contents.

    Returns:
        The document rebuilt from allowed elements and attributes, with the
        SVG namespace as the only namespace.

    Raises:
        UnsafeSvgError: the file has a DTD, scripts, event handlers, foreign
            content or references to anything outside itself.
    """
    if "<!DOCTYPE" in text or "<!ENTITY" in text:
        raise UnsafeSvgError("document type declarations are not allowed")
    try:
        root = ElementTree.fromstring(text)
    except ElementTree.ParseError as error:
        raise UnsafeSvgError(f"not well-formed XML: {error}") from error
    if _local(root.tag) != "svg":
        raise UnsafeSvgError("the root element is not <svg>")
    clean = _clean(root)
    clean.set("xmlns", _SVG_NS)
    ElementTree.indent(clean)
    return ElementTree.tostring(clean, encoding="unicode") + "\n"
