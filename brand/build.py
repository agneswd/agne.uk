"""Builds every Agne Studio logo SVG from the Caveat font, so the logo can always be made again exactly.

Usage (from the repository root):
    python3 -m venv .venv && .venv/bin/pip install fonttools
    .venv/bin/python brand/build.py

Writes brand/svg/*.svg and public/img/wordmark.svg. PNG files are exported from these SVGs (see brand/README.md).
"""
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent
FONT = ROOT / "source" / "Caveat-Variable.ttf"

# Brand colors. Keep them in sync with brand/README.md and public/styles.css.
INK = "#141311"       # page background, near-black
TILE = "#161513"      # icon tile
PAPER = "#EFE9DD"     # light text and light backgrounds
AMBER = "#E2A54B"     # the underline, on dark
AMBER_DEEP = "#C9852A"  # the underline, on light (more contrast)
DARK_INK = "#1B1A17"  # dark text on light backgrounds


def font_at(weight):
    return instantiateVariableFont(TTFont(FONT), {"wght": weight})


def text_path(font, text):
    """Returns the SVG path data for text set in one line, its advance width, ascent, and descent."""
    glyphs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    ascent = font["hhea"].ascent
    pen, x = SVGPathPen(glyphs), 0
    for ch in text:
        name = cmap[ord(ch)]
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, x, ascent)))
        x += hmtx[name][0]
    return pen.getCommands(), x, ascent, -font["hhea"].descent


def char_bounds(font, ch):
    """Bounding box of one character in SVG coordinates (y down)."""
    glyphs = font.getGlyphSet()
    pen = BoundsPen(glyphs)
    glyphs[font.getBestCmap()[ord(ch)]].draw(pen)
    x0, y0, x1, y1 = pen.bounds
    ascent = font["hhea"].ascent
    return x0, ascent - y1, x1, ascent - y0


def wordmark(letters, line, background=None):
    """The "Agne Studio" wordmark with the underline under "Studio". background=None keeps it transparent."""
    d, width, ascent, descent = text_path(font_at(600), "Agne Studio")
    w, h = width + 80, ascent + descent + 120
    bg = f'<rect x="-40" width="{w}" height="{h}" fill="{background}"/>' if background else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 0 {w} {h}" role="img" aria-label="Agne Studio">{bg}'
            f'<path class="ink" d="{d}" fill="{letters}"/>'
            f'<path class="line" d="M2280 1150 C 2700 1095, 3300 1085, 3980 1120" fill="none" stroke="{line}" stroke-width="46" stroke-linecap="round"/></svg>\n')


def icon(tile, letter, line, radius=0.22):
    """The handwritten "a" on a square tile, with a short underline. radius=0 gives a square for platforms that crop."""
    font = font_at(700)
    d, _, _, _ = text_path(font, "a")
    x0, y0, x1, y1 = char_bounds(font, "a")
    s = 520 / (y1 - y0)
    tx = 500 - (x1 - x0) * s / 2 - x0 * s
    ty = 420 - (y1 - y0) * s / 2 - y0 * s
    rect = f'<rect width="1000" height="1000" rx="{1000 * radius:.0f}" fill="{tile}"/>' if tile else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-label="Agne Studio">{rect}'
            f'<path transform="translate({tx:.1f} {ty:.1f}) scale({s:.4f})" d="{d}" fill="{letter}"/>'
            f'<path d="M285 790 C 420 760, 600 756, 725 778" fill="none" stroke="{line}" stroke-width="54" stroke-linecap="round"/></svg>\n')


def main():
    out = ROOT / "svg"
    out.mkdir(exist_ok=True)
    files = {
        "wordmark-on-dark.svg": wordmark(PAPER, AMBER),
        "wordmark-on-light.svg": wordmark(DARK_INK, AMBER_DEEP),
        "wordmark-white.svg": wordmark("#FFFFFF", "#FFFFFF"),
        "wordmark-black.svg": wordmark("#000000", "#000000"),
        "wordmark-on-dark-filled.svg": wordmark(PAPER, AMBER, INK),
        "icon-dark-rounded.svg": icon(TILE, PAPER, AMBER),
        "icon-dark-square.svg": icon(TILE, PAPER, AMBER, 0),
        "icon-light-rounded.svg": icon(PAPER, DARK_INK, AMBER_DEEP),
        "icon-light-square.svg": icon(PAPER, DARK_INK, AMBER_DEEP, 0),
        "icon-mark-white.svg": icon(None, "#FFFFFF", "#FFFFFF"),
        "icon-mark-black.svg": icon(None, "#000000", "#000000"),
    }
    for name, svg in files.items():
        (out / name).write_text(svg)
    # The site uses the transparent on-dark wordmark and the rounded dark icon as its favicon.
    site = ROOT.parent / "public"
    (site / "img" / "wordmark.svg").write_text(files["wordmark-on-dark.svg"])
    (site / "favicon.svg").write_text(files["icon-dark-rounded.svg"])
    # The hero inlines the wordmark (so it can animate). Replace the part between the markers in index.html.
    index = site / "index.html"
    html = index.read_text()
    start, end = "<!-- wordmark:start -->", "<!-- wordmark:end -->"
    head, rest = html.split(start, 1)
    _, tail = rest.split(end, 1)
    index.write_text(head + start + files["wordmark-on-dark.svg"].strip() + end + tail)
    print(f"Wrote {len(files)} SVGs to {out}")


if __name__ == "__main__":
    main()
