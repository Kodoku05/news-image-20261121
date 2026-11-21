"""Render the front page to entry.png with Pillow.

The news itself lives in news.py; this file only draws it. Layout is a
classic broadsheet: navy masthead band, a red kicker over the lead
headline, a three-step "how the day unfolded" strip, a two-column story
grid, one full-width story, and a navy footer with the markets line.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from news import (
    DATE_LINE,
    FOOTER_LINES,
    KICKER,
    LEAD_DECK,
    LEAD_TITLE,
    MASTHEAD,
    STORIES,
    TIMELINE,
    WIDE_DECK,
    WIDE_TITLE,
)

PAGE = 1024
MARGIN = 44
RIGHT = PAGE - MARGIN
CONTENT = RIGHT - MARGIN

PAPER = "#f8f4ec"
INK = "#101f34"
ACCENT = "#b32b23"
RULE = "#b9b2a4"
STRIP_BG = "#efe8d6"
FOOTER_TOP = 946


def load_fonts():
    """Serif for display type, sans for decks and labels."""
    root = Path("/usr/share/fonts/truetype")
    serif = root / "dejavu" / "DejaVuSerif-Bold.ttf"
    sans = root / "dejavu" / "DejaVuSans.ttf"
    sans_bold = root / "dejavu" / "DejaVuSans-Bold.ttf"
    if not (serif.is_file() and sans.is_file() and sans_bold.is_file()):
        raise FileNotFoundError("DejaVu Serif/Sans fonts are required")
    return {
        "masthead": ImageFont.truetype(serif, 60),
        "dateline": ImageFont.truetype(sans_bold, 25),
        "kicker": ImageFont.truetype(sans_bold, 20),
        "lead": ImageFont.truetype(serif, 50),
        "lead_deck": ImageFont.truetype(sans, 23),
        "step_head": ImageFont.truetype(sans_bold, 18),
        "step_body": ImageFont.truetype(sans, 17),
        "headline": ImageFont.truetype(serif, 29),
        "deck": ImageFont.truetype(sans, 19),
        "wide_head": ImageFont.truetype(serif, 30),
        "wide_deck": ImageFont.truetype(sans, 20),
        "footer": ImageFont.truetype(sans, 18),
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
    draw.rectangle((0, 0, PAGE - 1, 116), fill=INK)
    paint_text(draw, MASTHEAD, fonts["masthead"], MARGIN, 12, CONTENT, 66,
               fill=PAPER, center=True)
    paint_text(draw, DATE_LINE, fonts["dateline"], MARGIN, 82, CONTENT, 30,
               fill=PAPER, center=True)
    draw.rectangle((0, 117, PAGE - 1, 121), fill=ACCENT)


def draw_timeline(draw, fonts, y):
    """Three-step strip: summit -> strikes -> missile in Poland."""
    height = 96
    draw.rectangle((MARGIN, y, RIGHT, y + height), fill=STRIP_BG,
                   outline=INK, width=2)
    cell = CONTENT // 3
    for i, (head, body) in enumerate(TIMELINE):
        x = MARGIN + i * cell
        inset = 13 if i == 0 else 30
        inner = cell - inset - 13
        top = paint_text(draw, head, fonts["step_head"], x + inset, y + 10,
                         inner, 22, fill=ACCENT)
        paint_text(draw, body, fonts["step_body"], x + inset, top + 4,
                   inner, 21)
        if i > 0:
            mid = y + height // 2
            draw.line((x, y + 12, x, y + height - 12), fill=RULE)
            draw.line((x + 4, mid - 8, x + 16, mid), fill=ACCENT, width=3)
            draw.line((x + 16, mid, x + 4, mid + 8), fill=ACCENT, width=3)
    return y + height


def draw_story(draw, fonts, x, y, width, title, summary):
    head_bottom = paint_text(draw, title, fonts["headline"], x, y, width, 34)
    return paint_text(draw, summary, fonts["deck"], x, head_bottom + 4,
                      width, 24)


def draw_footer(draw, fonts):
    draw.rectangle((0, FOOTER_TOP, PAGE - 1, PAGE - 1), fill=INK)
    draw.rectangle((0, FOOTER_TOP, PAGE - 1, FOOTER_TOP + 3), fill=ACCENT)
    paint_text(draw, FOOTER_LINES[0], fonts["footer"], MARGIN, 958,
               CONTENT, 23, fill=PAPER, center=True)
    paint_text(draw, FOOTER_LINES[1], fonts["footer"], MARGIN, 984,
               CONTENT, 23, fill=PAPER, center=True)


def render():
    fonts = load_fonts()
    image = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(image)
    draw_masthead(draw, fonts)

    # Red kicker tag above the lead headline.
    tag = draw.textbbox((0, 0), KICKER, font=fonts["kicker"])
    tag_w = tag[2] - tag[0] + 24
    draw.rectangle((MARGIN, 136, MARGIN + tag_w, 136 + 30), fill=ACCENT)
    draw.text((MARGIN + 12, 140), KICKER, font=fonts["kicker"], fill=PAPER)

    y = 176
    y = paint_text(draw, LEAD_TITLE, fonts["lead"], MARGIN, y, CONTENT, 56)
    y = paint_text(draw, LEAD_DECK, fonts["lead_deck"], MARGIN, y + 8,
                   CONTENT, 29)
    y = draw_timeline(draw, fonts, y + 18)

    draw.line((MARGIN, y + 14, RIGHT, y + 14), fill=ACCENT, width=3)
    y += 26

    gutter = 32
    column = (CONTENT - gutter) // 2
    for row in range(0, len(STORIES), 2):
        pair = STORIES[row:row + 2]
        bottoms = []
        for j, (title, summary) in enumerate(pair):
            cell_x = MARGIN + j * (column + gutter)
            bottoms.append(draw_story(draw, fonts, cell_x, y, column,
                                      title, summary))
        if len(pair) == 2:
            draw.line((PAGE // 2, y + 4, PAGE // 2, max(bottoms)), fill=RULE)
        y = max(bottoms) + 14
        if row + 2 < len(STORIES):
            draw.line((MARGIN, y, RIGHT, y), fill=RULE)
            y += 12

    # Full-width story with a red bar on its left.
    draw.rectangle((MARGIN, y + 2, MARGIN + 6, y + 64), fill=ACCENT)
    head_bottom = paint_text(draw, WIDE_TITLE, fonts["wide_head"],
                             MARGIN + 20, y, CONTENT - 20, 36)
    y = paint_text(draw, WIDE_DECK, fonts["wide_deck"], MARGIN + 20,
                   head_bottom + 2, CONTENT - 20, 25)

    if y > FOOTER_TOP - 8:
        raise ValueError(f"Story grid runs into the footer at y={y}")
    draw_footer(draw, fonts)
    image.save(Path(__file__).with_name("entry.png"), optimize=True)


if __name__ == "__main__":
    render()
