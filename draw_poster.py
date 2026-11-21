"""Render the front page to entry.png with Pillow (v4 — headline + SEO round).

Layout: navy masthead band with a subtle dotted world-map texture and the
story count, then a lead block with the headline + deck on the left and a
hero illustration on the right, a key-numbers strip, then a three-column
briefs grid grouped by region (tinted section headers, one headline per
story) with spot illustrations filling the dead space at the bottom of
the shorter columns, and a navy footer with the markets ticker, an "also"
line and a "trending now" strip. The renderer measures everything before
drawing and fails loudly if anything overflows the page. Content (all 40
stories) is unchanged from v2/v3 — only the headlines are punchier and
today's trending search terms are woven in.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

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
    TRENDING_LINE,
    story_count,
)

PAGE = 1024
MARGIN = 40
RIGHT = PAGE - MARGIN
CONTENT = RIGHT - MARGIN
ART = Path(__file__).with_name("art")

PAPER = "#f8f4ec"
INK = "#101f34"
ACCENT = "#b32b23"
RULE = "#b9b2a4"
GOLD = "#d8cfae"
MAP_DOT = "#263c56"
CAPTION = "#6b6355"
FOOTER_TOP = 960

MASTHEAD_H = 108
LEAD_TEXT_W = 560
HERO_X = MARGIN + LEAD_TEXT_W + 16  # 616
HERO_W = RIGHT - HERO_X  # 368
HERO_H = 200

COL_GAP = 18
COL_W = (CONTENT - 2 * COL_GAP) // 3  # 302

SPOT_H = 100  # Fits the ~125px of dead space below columns 0 and 2.
# Spot illustration per column index (None = no spot): (art file, caption).
SPOTS = (
    ("markets.png", "WALL STREET'S WORST WEEK SINCE 2020"),
    None,
    ("cyclone.png", "CYCLONE AKVAN FADES OVER ODISHA"),
)

# Coarse continent polygons on a 240x120 mask (west -> east, north ->
# south), sampled as dots for the masthead's world-map texture.
CONTINENTS = [
    # North America.
    [(8, 18), (55, 12), (78, 18), (72, 38), (60, 55), (45, 52), (30, 45),
     (12, 32)],
    # Greenland.
    [(72, 8), (88, 6), (92, 16), (78, 18)],
    # South America.
    [(58, 62), (78, 60), (82, 78), (70, 100), (60, 88), (54, 72)],
    # Europe.
    [(112, 14), (132, 10), (140, 22), (128, 30), (114, 26)],
    # Africa.
    [(110, 34), (138, 32), (146, 52), (132, 78), (118, 70), (108, 50)],
    # Asia.
    [(140, 10), (225, 8), (232, 30), (205, 48), (180, 44), (160, 36),
     (140, 28)],
    # Australia.
    [(200, 82), (228, 80), (230, 98), (208, 100)],
]
# (x, y, r): UK, Japan, New Zealand, SE Asian islands, Madagascar.
ISLANDS = [(108, 16, 3), (228, 30, 3), (232, 100, 2), (200, 55, 3),
           (212, 60, 3), (195, 62, 3), (138, 66, 3)]


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def blend(foreground, background, amount):
    """Blend foreground over background; amount 0..1."""
    fg = hex_to_rgb(foreground)
    bg = hex_to_rgb(background)
    return tuple(round(bg[i] + (fg[i] - bg[i]) * amount) for i in range(3))


def load_fonts():
    """Serif for display type, sans for decks, labels and briefs."""
    root = Path("/usr/share/fonts/truetype")
    serif = root / "dejavu" / "DejaVuSerif-Bold.ttf"
    sans = root / "dejavu" / "DejaVuSans.ttf"
    sans_bold = root / "dejavu" / "DejaVuSans-Bold.ttf"
    if not (serif.is_file() and sans.is_file() and sans_bold.is_file()):
        raise FileNotFoundError("DejaVu Serif/Sans fonts are required")
    return {
        "masthead": ImageFont.truetype(serif, 52),
        "dateline": ImageFont.truetype(sans_bold, 20),
        "count": ImageFont.truetype(sans_bold, 15),
        "kicker": ImageFont.truetype(sans_bold, 17),
        "lead": ImageFont.truetype(serif, 38),
        "lead_deck": ImageFont.truetype(sans, 19),
        "stats": ImageFont.truetype(sans_bold, 15),
        "region": ImageFont.truetype(sans_bold, 16),
        "story": ImageFont.truetype(serif, 14),
        "caption": ImageFont.truetype(sans_bold, 11),
        "footer": ImageFont.truetype(sans, 15),
        "trending": ImageFont.truetype(sans_bold, 13),
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


def draw_map_texture(draw):
    """Subtle dotted world map across the masthead band."""
    mask = Image.new("L", (240, 120), 0)
    mask_draw = ImageDraw.Draw(mask)
    for poly in CONTINENTS:
        mask_draw.polygon(poly, fill=255)
    for x, y, r in ISLANDS:
        mask_draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
    px = mask.load()
    mx0, my0, mx1, my1 = 28, 6, PAGE - 28, MASTHEAD_H - 6
    step = 3
    dot_r = 1.7
    for gy in range(0, 120, step):
        for gx in range(0, 240, step):
            if px[gx, gy]:
                x = mx0 + (gx / 240) * (mx1 - mx0)
                y = my0 + (gy / 120) * (my1 - my0)
                draw.ellipse((x - dot_r, y - dot_r, x + dot_r, y + dot_r),
                             fill=MAP_DOT)


def draw_masthead(draw, fonts):
    draw.rectangle((0, 0, PAGE - 1, MASTHEAD_H - 1), fill=INK)
    draw_map_texture(draw)
    paint_text(draw, MASTHEAD, fonts["masthead"], MARGIN, 2, CONTENT, 58,
               fill=PAPER, center=True)
    paint_text(draw, DATE_LINE, fonts["dateline"], MARGIN, 60, CONTENT, 24,
               fill=PAPER, center=True)
    count_line = f"{story_count()} STORIES  ·  7 REGIONS"
    paint_text(draw, count_line, fonts["count"], MARGIN, 84, CONTENT, 18,
               fill=GOLD, center=True)
    draw.line((0, MASTHEAD_H, PAGE - 1, MASTHEAD_H), fill=ACCENT, width=3)


def draw_lead(image, draw, fonts):
    """Lead block: text left, hero illustration right, stats strip below.

    Returns the y just below the stats strip (the grid starts below it).
    """
    y = MASTHEAD_H + 12
    # Hero illustration (right) with a thin frame and one-line caption.
    hero = Image.open(ART / "hero.png").convert("RGB")
    hero = ImageOps.fit(hero, (HERO_W, HERO_H), Image.LANCZOS)
    image.paste(hero, (HERO_X, y))
    draw.rectangle((HERO_X, y, HERO_X + HERO_W - 1, y + HERO_H - 1),
                   outline=INK, width=2)
    caption = "JETS SCRAMBLE OVER POLAND — ILLUSTRATION"
    caption_bottom = paint_text(draw, caption, fonts["caption"], HERO_X,
                                y + HERO_H + 4, HERO_W, 14, fill=CAPTION)
    # Kicker chip.
    chip_w = draw.textbbox((0, 0), KICKER, font=fonts["kicker"])[2] + 24
    draw.rectangle((MARGIN, y, MARGIN + chip_w, y + 22), fill=ACCENT)
    draw.text((MARGIN + 12, y + 2), KICKER, font=fonts["kicker"], fill=PAPER)
    text_y = y + 28
    bottom = paint_text(draw, LEAD_TITLE, fonts["lead"], MARGIN, text_y,
                        LEAD_TEXT_W, 42, fill=INK)
    bottom = paint_text(draw, LEAD_DECK, fonts["lead_deck"], MARGIN,
                        bottom + 6, LEAD_TEXT_W, 22, fill=INK)
    # Key-numbers strip between thin rules, below both text and caption.
    strip_y = max(bottom, caption_bottom) + 10
    draw.line((MARGIN, strip_y, RIGHT, strip_y), fill=RULE, width=1)
    paint_text(draw, STATS_LINE, fonts["stats"], MARGIN, strip_y + 4,
               CONTENT, 20, fill=ACCENT, center=True)
    draw.line((MARGIN, strip_y + 26, RIGHT, strip_y + 26), fill=RULE,
              width=1)
    return strip_y + 26


def measure_grid(draw, fonts):
    """Return per-column heights; raise if any column overflows."""
    region_map = {name: (colour, stories) for name, colour, stories in REGIONS}
    heights = []
    for column in COLUMNS:
        total = 0
        for name in column:
            _, stories = region_map[name]
            total += 24  # tinted section header + rule
            for story in stories:
                lines = split_lines(draw, story, fonts["story"], COL_W - 14)
                total += len(lines) * 16 + 4
            total += 5  # gap after a section
        heights.append(total)
    return heights


def draw_spot(image, draw, fonts, column_index, x, y, available):
    """Draw a column's spot illustration if it fits; return bottom y."""
    spot = SPOTS[column_index]
    if spot is None:
        return y
    art_file, caption = spot
    block = SPOT_H + 4 + 14
    if available < block + 6:
        print(f"column {column_index}: spot skipped, "
              f"only {available}px free")
        return y
    art = Image.open(ART / art_file).convert("RGB")
    art = ImageOps.fit(art, (COL_W, SPOT_H), Image.LANCZOS)
    image.paste(art, (x, y))
    draw.rectangle((x, y, x + COL_W - 1, y + SPOT_H - 1), outline=INK,
                   width=1)
    bottom = paint_text(draw, caption, fonts["caption"], x, y + SPOT_H + 4,
                        COL_W, 14, fill=CAPTION)
    return bottom


def draw_grid(image, draw, fonts, grid_top):
    region_map = {name: (colour, stories) for name, colour, stories in REGIONS}
    for i, column in enumerate(COLUMNS):
        x = MARGIN + i * (COL_W + COL_GAP)
        y = grid_top
        for name in column:
            colour, stories = region_map[name]
            tint = blend(colour, PAPER, 0.14)
            draw.rectangle((x, y - 2, x + COL_W, y + 19), fill=tint)
            draw.text((x + 4, y), name, font=fonts["region"], fill=colour)
            draw.line((x, y + 21, x + COL_W, y + 21), fill=colour, width=2)
            y += 24
            for story in stories:
                draw.rectangle((x, y + 5, x + 7, y + 12), fill=colour)
                bottom = paint_text(draw, story, fonts["story"], x + 14, y,
                                    COL_W - 14, 16, fill=INK)
                y = bottom + 4
            y += 5
        # Spot illustration in the dead space below the last section.
        draw_spot(image, draw, fonts, i, x, y + 4,
                  FOOTER_TOP - 8 - (y + 4))
        # Column divider (skip after the last column).
        if i < len(COLUMNS) - 1:
            dx = x + COL_W + COL_GAP // 2
            draw.line((dx, grid_top, dx, FOOTER_TOP - 8), fill=RULE, width=1)


def draw_footer(draw, fonts):
    # Each footer line must fit on exactly one line; a wrapped second
    # line would overlap the line below it, so fail loudly instead.
    for line, font in ((MARKETS_LINE, fonts["footer"]),
                       (ALSO_LINE, fonts["footer"]),
                       (TRENDING_LINE, fonts["trending"])):
        if len(split_lines(draw, line, font, CONTENT)) != 1:
            raise ValueError(f"Footer line wraps: {line}")
    draw.rectangle((0, FOOTER_TOP, PAGE - 1, PAGE - 1), fill=INK)
    draw.line((0, FOOTER_TOP, PAGE - 1, FOOTER_TOP), fill=ACCENT, width=3)
    paint_text(draw, MARKETS_LINE, fonts["footer"], MARGIN, FOOTER_TOP + 5,
               CONTENT, 20, fill=PAPER, center=True)
    paint_text(draw, ALSO_LINE, fonts["footer"], MARGIN, FOOTER_TOP + 25,
               CONTENT, 20, fill=GOLD, center=True)
    paint_text(draw, TRENDING_LINE, fonts["trending"], MARGIN,
               FOOTER_TOP + 46, CONTENT, 16, fill=PAPER, center=True)


def main():
    image = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(image)
    fonts = load_fonts()

    draw_masthead(draw, fonts)
    lead_bottom = draw_lead(image, draw, fonts)
    grid_top = lead_bottom + 12
    heights = measure_grid(draw, fonts)
    available = FOOTER_TOP - grid_top
    print(f"lead bottom: {lead_bottom}, grid top: {grid_top}")
    print(f"grid columns: {heights} (available {available})")
    if max(heights) > available:
        raise ValueError(
            f"Grid overflows by {max(heights) - available}px: {heights}")

    draw_grid(image, draw, fonts, grid_top)
    draw_footer(draw, fonts)

    out = Path(__file__).with_name("entry.png")
    image.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, "
          f"{story_count()} stories)")


if __name__ == "__main__":
    main()
