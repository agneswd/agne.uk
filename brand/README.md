# Agne Studio brand kit

Everything needed to use the Agne Studio logo somewhere new. Use these files as they are. Do not redraw the logo or set it again in a font.

## The logo

| Mark | What it is | Use it for |
| --- | --- | --- |
| Wordmark | "Agne Studio" handwritten in Caveat, with an amber underline under "Studio" | Headers, title cards, share images, anywhere with room for the full name |
| Icon | A handwritten "a" with a short amber underline, on a tile | App and profile pictures, favicons, small spaces |

## Files

`svg/` (vector, preferred):

| File | Background | Notes |
| --- | --- | --- |
| `wordmark-on-dark.svg` | transparent | Light letters, amber line. Main version, for dark backgrounds. |
| `wordmark-on-light.svg` | transparent | Dark letters, deep amber line. For light backgrounds. |
| `wordmark-on-dark-filled.svg` | near-black | Same as on-dark, with its own background. |
| `wordmark-white.svg`, `wordmark-black.svg` | transparent | One color only. For print, embossing, or photos. |
| `icon-dark-rounded.svg` | near-black tile, rounded | Favicon and places that show the tile as is. |
| `icon-dark-square.svg` | near-black tile, square | Profile pictures and stores that apply their own mask or circle crop. |
| `icon-light-rounded.svg`, `icon-light-square.svg` | paper tile | Light variant of the icon. |
| `icon-mark-white.svg`, `icon-mark-black.svg` | transparent | The "a" and line only, one color. |

`png/` (exports of the SVGs):

| File | Size | Used for |
| --- | --- | --- |
| `icon-dark-1024.png`, `icon-dark-512.png`, `icon-dark-192.png` | square | General icon use. 512 is the Google Play developer icon. |
| `icon-dark-rounded-512.png` | 512, transparent corners | Places that do not round corners themselves. |
| `icon-light-512.png` | 512 | Light icon. |
| `apple-touch-icon-180.png` | 180 | iOS home screen (also in `public/`). |
| `avatar-800.png` | 800 | YouTube and other profile pictures (they crop to a circle; the mark stays inside). |
| `wordmark-on-dark-2400.png`, `wordmark-on-light-2400.png` | 2400 x 803 | Wordmark with background. |
| `wordmark-transparent-2400.png` | 2400 x 803 | Wordmark for dark backgrounds, transparent. |
| `og-1200x630.png` | 1200 x 630 | Link previews (also `public/og.png`). |
| `play-header-4096x2304.png` | 4096 x 2304 | Google Play developer page header. |

## Colors

| Name | Hex | Use |
| --- | --- | --- |
| Ink | `#141311` | Page background (warm near-black, never pure black) |
| Tile | `#161513` | Icon tile |
| Paper | `#EFE9DD` | Text and marks on dark, light backgrounds |
| Amber | `#E2A54B` | The underline and accents on dark |
| Deep amber | `#C9852A` | The underline on light backgrounds |
| Dark ink | `#1B1A17` | Text and marks on light backgrounds |
| Dim | `#A59F93` | Secondary text on dark |

## Type

- **Caveat** (SIL OFL 1.1, `source/OFL-Caveat.txt`): the logo, and short handwritten notes only. Never body text.
- **Instrument Serif** (SIL OFL 1.1, upright only): headlines.
- System sans-serif: body text.

The web fonts are in `../public/fonts/`.

## Rules

- Keep clear space around the wordmark of at least the height of the lowercase "n" on every side. Around the icon tile, keep at least 10% of its width.
- Minimum size: the wordmark 96 px wide on screen, the icon 16 px.
- Use the amber line only as drawn: under "Studio", or under the "a". Do not move, recolor (other than the one-color files), or remove it.
- Do not stretch, rotate, slant, outline, add shadows or glows, or put the logo on busy photos without a solid area behind it.
- Do not add dots, sparkles, or other decoration to the logo or to headlines.
- Do not set "Agne Studio" in Caveat as live text to imitate the logo. Use the SVG.

## Rebuilding the files

The SVGs come from the font, so they can be made again exactly:

```sh
python3 -m venv .venv && .venv/bin/pip install fonttools
.venv/bin/python brand/build.py         # writes brand/svg/, public/img/wordmark.svg, public/favicon.svg, and the hero in public/index.html
bun add -d playwright-core               # once, if needed
node brand/export.mjs                    # writes brand/png/ (or CDP_URL=http://127.0.0.1:9222 to use a running Chromium)
```

To change the logo, change `build.py` (weights, the underline path, colors), run both steps, and check the results on dark and light backgrounds and at 16 px.
