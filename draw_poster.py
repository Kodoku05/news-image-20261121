"""Render the front page to entry.png with Pillow (v2 — dense edition).

Layout: navy masthead band with a story-count line, one big lead with a
key-numbers strip, then a three-column briefs grid grouped by region
(coloured section headers, one headline per story), and a navy footer
with the markets ticker plus an "also" line. The renderer measures every
column before drawing and fails loudly if anything overflows the page.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from news import (
    ALSO_LINE,
    COLUMNS,
    DATE_LINE,
    KICKER,
    LEAD_DECK,
    LEAD_TITLE,
    MARKETS_LINE,
    MASTHEAD,
    REGIONS,
    STATS_LINE,
    story_count,
)

PAGE = 1024
MARGIN = 40
RIGHT = PAGE - MARGIN
CONTENT = RIGHT - MARGIN

PAPER = "#f8f4ec"
INK = "#101f34"
ACCENT = "#b32b23"
RULE = "#b9b2a4"
FOOTER_TOP = 960

MASTHEAD_H = 116
GRID_TOP = 344

COL_GAP = 18
COL_W = (CONTENT - 2 * COL_GAP) // 3


def load_fonts():
    """Serif for display type, sans for decks, labels and briefs."""
    root = Path("/usr/share/fonts/truetype")
    serif = root / "dejavu" / "DejaVuSerif-Bold.ttf"
    sans = root / "dejavu" / "DejaVuSans.ttf"
    sans_bold = root / "dejavu" / "DejaVuSans-Bold.ttf"
    if not (serif.is_file() and sans.is_file() and sans_bold.is_file()):
        raise FileNotFoundError("DejaVu Serif/Sans fonts are required")
    return {
        "masthead": ImageFont.truetype(serif, 56),
        "dateline": ImageFont.truetype(sans_bold, 22),
        "count": ImageFont.truetype(sans_bold, 16),
        "kicker": ImageFont.truetype(sans_bold, 18),
        "lead": ImageFont.truetype(serif, 40),
        "lead_deck": ImageFont.truetype(sans, 20),
        "stats": ImageFont.truetype(sans_bold, 15),
        "region": ImageFont.truetype(sans_bold, 16),
        "story": ImageFont.truetype(serif, 14),
        "footer": ImageFont.truetype(sans, 15),
    }


def split_lines(draw, text, font, max_width):
    """Greedy word wrap; raises if a single word cannot fit."""
    lines = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        box = draw.textbbox((0, 0), trial, font=font)
        if box[2] - box[0] <= max_width:
            current = trial
        else:
            if not current:
                raise ValueError(f"Word too wide for its column: {word}")
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_text(draw, text, font, x, y, width, leading, fill=INK, center=False):
    """Draw wrapped text and return the y just below its last line."""
    bottom = y
    for line in split_lines(draw, text, font, width):
        anchor = "ma" if center else "la"
        pos = (x + width // 2, y) if center else (x, y)
        box = draw.textbbox(pos, line, font=font, anchor=anchor)
        if box[0] < 0 or box[2] > PAGE or box[3] > PAGE:
            raise ValueError(f"Text leaves the page: {line}")
        draw.text(pos, line, font=font, fill=fill, anchor=anchor)
        bottom = box[3]
        y += leading
    return bottom


def draw_masthead(draw, fonts):
    draw.rectangle((0, 0, PAGE - 1, MASTHEAD_H - 1), fill=INK)
    paint_text(draw, MASTHEAD, fonts["masthead"], MARGIN, 4, CONTENT, 62,
               fill=PAPER, center=True)
    paint_text(draw, DATE_LINE, fonts["dateline"], MARGIN, 66, CONTENT, 26,
               fill=PAPER, center=True)
    count_line = f"{story_count()} STORIES  ·  7 REGIONS"
    paint_text(draw, count_line, fonts["count"], MARGIN, 92, CONTENT, 20,
               fill="#d8cfae", center=True)
    draw.line((0, MASTHEAD_H, PAGE - 1, MASTHEAD_H), fill=ACCENT, width=3)


def draw_lead(draw, fonts):
    y = 128
    # Kicker chip.
    chip_w = draw.textbbox((0, 0), KICKER, font=fonts["kicker"])[2] + 24
    draw.rectangle((MARGIN, y, MARGIN + chip_w, y + 24), fill=ACCENT)
    draw.text((MARGIN + 12, y + 2), KICKER, font=fonts["kicker"], fill=PAPER)
    y += 30
    bottom = paint_text(draw, LEAD_TITLE, fonts["lead"], MARGIN, y, CONTENT,
                        46, fill=INK)
    bottom = paint_text(draw, LEAD_DECK, fonts["lead_deck"], MARGIN,
                        bottom + 8, CONTENT, 24, fill=INK)
    # Key-numbers strip between thin rules.
    y = bottom + 12
    draw.line((MARGIN, y, RIGHT, y), fill=RULE, width=1)
    paint_text(draw, STATS_LINE, fonts["stats"], MARGIN, y + 5, CONTENT, 20,
               fill=ACCENT, center=True)
    draw.line((MARGIN, y + 27, RIGHT, y + 27), fill=RULE, width=1)
    return y + 27


def measure_grid(draw, fonts):
    """Return per-column heights; raise if any column overflows."""
    region_map = {name: (colour, stories) for name, colour, stories in REGIONS}
    heights = []
    for column in COLUMNS:
        total = 0
        for name in column:
            _, stories = region_map[name]
            total += 25  # section header + rule
            for story in stories:
                lines = split_lines(draw, story, fonts["story"], COL_W - 14)
                total += len(lines) * 17 + 5
            total += 6  # gap after a section
        heights.append(total)
    return heights


def draw_grid(draw, fonts):
    region_map = {name: (colour, stories) for name, colour, stories in REGIONS}
    for i, column in enumerate(COLUMNS):
        x = MARGIN + i * (COL_W + COL_GAP)
        y = GRID_TOP
        for name in column:
            colour, stories = region_map[name]
            draw.text((x, y), name, font=fonts["region"], fill=colour)
            draw.line((x, y + 21, x + COL_W, y + 21), fill=colour, width=2)
            y += 25
            for story in stories:
                draw.rectangle((x, y + 5, x + 7, y + 12), fill=colour)
                bottom = paint_text(draw, story, fonts["story"], x + 14, y,
                                    COL_W - 14, 17, fill=INK)
                y = bottom + 5
            y += 6
        # Column divider (skip after the last column).
        if i < len(COLUMNS) - 1:
            dx = x + COL_W + COL_GAP // 2
            draw.line((dx, GRID_TOP, dx, FOOTER_TOP - 8), fill=RULE, width=1)


def draw_footer(draw, fonts):
    # Each footer line must fit on exactly one line; a wrapped second
    # line would overlap the line below it, so fail loudly instead.
    for line in (MARKETS_LINE, ALSO_LINE):
        if len(split_lines(draw, line, fonts["footer"], CONTENT)) != 1:
            raise ValueError(f"Footer line wraps: {line}")
    draw.rectangle((0, FOOTER_TOP, PAGE - 1, PAGE - 1), fill=INK)
    draw.line((0, FOOTER_TOP, PAGE - 1, FOOTER_TOP), fill=ACCENT, width=3)
    paint_text(draw, MARKETS_LINE, fonts["footer"], MARGIN, FOOTER_TOP + 8,
               CONTENT, 21, fill=PAPER, center=True)
    paint_text(draw, ALSO_LINE, fonts["footer"], MARGIN, FOOTER_TOP + 33,
               CONTENT, 21, fill="#d8cfae", center=True)


def main():
    image = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(image)
    fonts = load_fonts()

    heights = measure_grid(draw, fonts)
    available = FOOTER_TOP - GRID_TOP
    print(f"grid columns: {heights} (available {available})")
    if max(heights) > available:
        raise ValueError(
            f"Grid overflows by {max(heights) - available}px: {heights}")

    draw_masthead(draw, fonts)
    lead_bottom = draw_lead(draw, fonts)
    if lead_bottom > GRID_TOP:
        raise ValueError(f"Lead overflows into grid: {lead_bottom}")
    draw_grid(draw, fonts)
    draw_footer(draw, fonts)

    out = Path(__file__).with_name("entry.png")
    image.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, "
          f"{story_count()} stories)")


if __name__ == "__main__":
    main()
