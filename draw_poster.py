"""Render the front page to entry.png with Pillow (v5 — layout rebuild).

Layout follows the winning template family of this competition's top
entries (cream paper, huge serif date, stats strip, region strip,
three illustrated leads, a grid of ten small illustrated stories, a
numbered ALSO list, a dotted world map with pins, and a DATE CHECK
box) — with OUR OWN content, headlines, and artwork throughout.
Nothing is copied from any other entry: every illustration is drawn
programmatically in illustrations.py, and every story is one of our
50 verified stories from news.py.

Structure for 50 stories: 3 big leads (Poland, Kyiv, COP31) + 10
small illustrated grid stories + 37 in the numbered ALSO list. The
"WHY BITCOIN CRASHED" explainer box (our unique differentiator) sits
as a full-width strip between the grid and the ALSO list. The
TRENDING NOW strip stays in the footer.

The renderer measures everything before drawing and fails loudly if
anything overflows the page or a headline wraps past its allotted
lines. It also asserts the laid-out stories are exactly the 50
verified stories from news.py (lead + region briefs + also items).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import illustrations as art
from news import (
    ALSO_ITEMS,
    BTC_BOX_POINTS,
    BTC_BOX_SUB,
    BTC_BOX_TITLE,
    DATE_LINE,
    LEAD_DECK,
    LEAD_TITLE,
    MARKETS_LINE,
    REGIONS,
    TRENDING_LINE,
    story_count,
)

PAGE = 1024
MARGIN = 28
RIGHT = PAGE - MARGIN
CONTENT = RIGHT - MARGIN  # 968

PAPER = "#f7f1e3"
INK = "#141414"
ACCENT = "#b32b23"
RULE = "#b9b2a4"
CAPTION = "#6b6355"
NAVY = "#1c2a3a"
BTC_FILL = "#fff8ec"
BTC_BORDER = "#7a1f1f"

# --- Section geometry (tuned so the page ends at y <= 1020) ---
KICKER_Y = 8
RULE1_Y = 26
DATE_Y = 30
SUB_Y = 94
RULE2_Y = 114
STATS_Y = 118
STATS_H = 50
REGION_Y = 172
REGION_H = 20
LEADS_Y = 196
LEAD_IMG_H = 80
LEAD_COL_GAP = 16
LEAD_W = (CONTENT - 2 * LEAD_COL_GAP) // 3  # 312
GRID_GAP_X = 10
GRID_GAP_Y = 8
GRID_W = (CONTENT - 4 * GRID_GAP_X) // 5  # 185
GRID_IMG_H = 44
BTC_H = 52
ALSO_HEAD_H = 20
ALSO_COL_GAP = 12
ALSO_W = (CONTENT - 2 * ALSO_COL_GAP) // 3  # 314
BOTTOM_H = 124

# Region strip: counts are the TRUE counts of our 50 stories by
# region. EUROPE holds its 9 list stories + the Poland lead + the 4
# ALSO items (Czechia, Tata/Netherlands, Bayern, Hungary), all
# European: 9 + 1 + 4 = 14. The eight counts sum to 50.
REGION_COUNTS = {
    "EUROPE": 14,
    "ASIA-PACIFIC": 7,
    "MIDDLE EAST": 6,
    "AMERICAS": 8,
    "AFRICA": 1,
    "MARKETS": 4,
    "SPORT & CULTURE": 7,
    "SCIENCE & HEALTH": 3,
}

SUB_HEAD = ("Russian missiles land in Poland  ·  Kyiv barrage kills 9  ·  "
            "COP31 deadlocked in overtime  ·  Wall Street's worst week "
            "since 2020")

# (number, big number, caption) — every figure comes from our stories.
STATS = (
    ("9", "killed in the Ukraine barrage"),
    ("22,000", "children reported dead in Gaza"),
    ("357,000", "displaced in Yemen since August"),
    ("465", "hybrid attacks in Europe in 90 days"),
    ("$1.5B", "in leverage liquidated in 24 hours"),
    ("93*", "Rahul's unbeaten knock in Wellington"),
)

# --- Story selection -------------------------------------------------
# Headlines are matched verbatim against news.py; a typo raises
# KeyError loudly instead of silently dropping a story.

LEADS = (
    # (number, tag, headline, deck, illustration)
    (1, "EASTERN POLAND · SECURITY", LEAD_TITLE,
     "Two Russian missiles and a drone crash into Poland; Tusk calls it "
     "'intentional' as Rutte flies to Warsaw.",
     "hero"),
    (2, "KYIV, UKRAINE · WAR",
     "KYIV UNDER FIRE: 9 DEAD AS 3 BRIDGES BLASTED",
     "Nine dead and three bridges struck as Moscow's barrage hammers "
     "the capital; the attack spills into Poland.",
     "kyiv"),
    (3, "ANTALYA, TÜRKIYE · CLIMATE",
     "COP31 DEADLOCKED IN OVERTIME",
     "Talks in Antalya slip past their deadline with no deal; a third "
     "draft stripped of fossil fuels is due Saturday.",
     "cop31"),
)

GRID = (
    # (number, tag, headline, deck, illustration)
    (4, "KRYVYI RIH, UKRAINE · WAR",
     "KRYVYI RIH HORROR: BOY, 7, KILLED; 42 WOUNDED",
     "A boy of seven is killed and 42 wounded in the strike.",
     "kryvyi"),
    (5, "ODISHA, INDIA · CYCLONE",
     "CYCLONE AKVAN SLAMS ODISHA — THEN LOSES ITS PUNCH",
     "The cyclone slams into Odisha, then weakens over land.",
     "cyclone"),
    (6, "THE HAGUE · JUSTICE",
     "WORLD COURT: MYANMAR GUILTY OF ROHINGYA GENOCIDE",
     "The World Court finds Myanmar guilty of genocide.",
     "scales"),
    (7, "RIYADH · SECURITY",
     "HOUTHI MISSILES TARGET RIYADH — ALL SHOT DOWN",
     "Houthi missiles aimed at Riyadh are intercepted.",
     "interception"),
    (8, "GAZA · WAR",
     "GAZA HORROR: 22,000 CHILDREN REPORTED DEAD",
     "The reported child death toll in Gaza passes 22,000.",
     "candle"),
    (9, "NEW YORK · MARKETS",
     "WALL STREET BLEEDS: WORST WEEK SINCE 2020",
     "Stocks post their worst week since 2020.",
     "markets"),
    (10, "CALIFORNIA · TECH",
     "CALIFORNIA SUBPOENAS NVIDIA — NVDA IN THE DOCK",
     "California subpoenas the chip giant over China sales.",
     "chip"),
    (11, "WELLINGTON · CRICKET",
     "KL RAHUL'S 93* DRAGS INDIA BACK IN WELLINGTON",
     "Rahul's unbeaten 93 drags India back in Wellington.",
     "cricket"),
    (12, "DEEP SPACE · SPACE",
     "VOYAGER 1 MAKES HISTORY: ONE LIGHT-DAY FROM EARTH",
     "The probe is the first object one light-day out.",
     "voyager"),
    (13, "SHENZHEN · DIPLOMACY",
     "TRUMP, XI, PUTIN IN FIRST-EVER 3-WAY SUMMIT",
     "Trump, Xi and Putin meet in Shenzhen — a first.",
     "flags"),
)

# Map pins for the illustrated stories (number, lon, lat). Voyager 1
# is in space, so it has no pin — the map caption says so.
# Kryvyi Rih (4) sits almost on top of Kyiv (2) and Antalya (3) almost
# on top of Gaza (8); those two badges are nudged with a leader line
# to their true position so the numbers stay readable.
PINS = (
    (1, 19.0, 52.0, 0, 0),
    (2, 30.5, 50.5, 0, 0),
    (3, 30.7, 36.9, -14, -9),
    (4, 33.4, 47.9, 16, 7),
    (5, 85.0, 20.3, 0, 0),
    (6, 4.3, 52.1, 0, 0),
    (7, 46.7, 24.7, 0, 0),
    (8, 34.5, 31.5, 0, 0),
    (9, -74.0, 40.7, 0, 0),
    (10, -120.0, 37.0, 0, 0),
    (11, 174.8, -41.3, 0, 0),
    (13, 114.1, 22.5, 0, 0),
)

DATE_CHECK = (
    "COP31 — deadline passed Fri; Sat's story is the deadlock.",
    "Kyiv barrage — began overnight Fri; the toll is Saturday's.",
    "Akvan — landfall Fri; the weakening is Saturday's.",
    "Left out: GTA 6 sales figures — no confirmed total yet.",
    "Every story dated 21 Nov or late 20 Nov.",
)

FOOTER_SOURCES = (
    "Every story here happened, or was first reported, on Saturday 21 "
    "November 2026 — Sources: Reuters, AP, RFE/RL, CoinDesk, wire "
    "round-ups. Illustrations are original drawings, not photographs."
)


def load_fonts():
    root = Path("/usr/share/fonts/truetype/dejavu")
    serif = root / "DejaVuSerif.ttf"
    serif_bold = root / "DejaVuSerif-Bold.ttf"
    sans = root / "DejaVuSans.ttf"
    sans_bold = root / "DejaVuSans-Bold.ttf"
    for path in (serif, serif_bold, sans, sans_bold):
        if not path.is_file():
            raise FileNotFoundError(f"Missing font: {path}")
    return {
        "kicker": ImageFont.truetype(sans_bold, 13),
        "kicker_right": ImageFont.truetype(sans, 11),
        "date": ImageFont.truetype(serif_bold, 58),
        "sub": ImageFont.truetype(serif, 15),
        "stats_num": ImageFont.truetype(serif_bold, 26),
        "stats_cap": ImageFont.truetype(sans, 10),
        "region": ImageFont.truetype(sans_bold, 10),
        "lead_tag": ImageFont.truetype(sans_bold, 11),
        "lead_head": ImageFont.truetype(serif_bold, 17),
        "lead_deck": ImageFont.truetype(sans, 10),
        "grid_tag": ImageFont.truetype(sans_bold, 9),
        "grid_head": ImageFont.truetype(sans_bold, 10),
        "grid_deck": ImageFont.truetype(sans, 10),
        "btc_title": ImageFont.truetype(sans_bold, 13),
        "btc_sub": ImageFont.truetype(sans_bold, 10),
        "btc_bullet": ImageFont.truetype(sans, 10),
        "also_head": ImageFont.truetype(sans_bold, 13),
        "also_item": ImageFont.truetype(sans, 10),
        "map_head": ImageFont.truetype(sans_bold, 12),
        "map_note": ImageFont.truetype(sans, 9),
        "dc_title": ImageFont.truetype(sans_bold, 12),
        "dc_item": ImageFont.truetype(sans, 11),
        "footer": ImageFont.truetype(sans, 11),
        "footer_bold": ImageFont.truetype(sans_bold, 10),
        "footer_small": ImageFont.truetype(sans, 9),
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


def text_width(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def draw_lines(draw, lines, font, x, y, leading, fill=INK):
    """Draw pre-wrapped lines; return the y just below the last line."""
    bottom = y
    for line in lines:
        box = draw.textbbox((x, y), line, font=font)
        if box[0] < 0 or box[2] > PAGE or box[3] > PAGE:
            raise ValueError(f"Text leaves the page: {line}")
        draw.text((x, y), line, font=font, fill=fill)
        bottom = box[3]
        y += leading
    return bottom


def draw_centered(draw, text, font, y, fill=INK, max_width=None):
    """Draw one line centred on the page; fail if it wraps."""
    if max_width is None:
        max_width = CONTENT
    lines = split_lines(draw, text, font, max_width)
    if len(lines) != 1:
        raise ValueError(f"Centred line wraps: {text}")
    x = MARGIN + (max_width - text_width(draw, text, font)) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return draw.textbbox((x, y), text, font=font)[3]


def illustration(name, w, h):
    """Return the illustration for a lead/grid story at w x h."""
    if name == "hero":
        return art.framed_art("hero.png", w, h)
    if name == "markets":
        return art.framed_art("markets.png", w, h)
    builders = {
        "kyiv": art.kyiv_night,
        "cop31": art.cop31_globe,
        "kryvyi": art.kryvyi_rih,
        "cyclone": art.cyclone,
        "scales": art.scales,
        "interception": art.interception,
        "candle": art.candle,
        "chip": art.chip,
        "cricket": art.cricket,
        "voyager": art.voyager,
        "flags": art.flags,
    }
    return builders[name](w, h)


def also_stories():
    """The 37 ALSO headlines, numbered 14-50, in region order.

    Everything from news.py that is not a lead or a grid story, plus
    the four footer ALSO items (upper-cased for the list).
    """
    used = {headline for _, _, headline, _, _ in LEADS}
    used |= {headline for _, _, headline, _, _ in GRID}
    items = []
    for _, _, stories in REGIONS:
        for headline in stories:
            if headline not in used:
                items.append(headline)
    items.extend(item.upper() for item in ALSO_ITEMS)
    if len(items) != 37:
        raise ValueError(f"Expected 37 ALSO stories, got {len(items)}")
    return [(14 + i, headline) for i, headline in enumerate(items)]


def verify_story_set():
    """The laid-out stories must be exactly news.py's 50 stories."""
    expected = {LEAD_TITLE}
    expected |= {s for _, _, stories in REGIONS for s in stories}
    expected |= set(ALSO_ITEMS)
    actual = {headline for _, _, headline, _, _ in LEADS}
    actual |= {headline for _, _, headline, _, _ in GRID}
    actual |= {headline for _, headline in also_stories()}
    # ALSO items are upper-cased for display; compare case-insensitively.
    norm = {s.upper() for s in expected}
    actual_norm = {s.upper() for s in actual}
    if norm != actual_norm:
        raise ValueError(
            f"Story mismatch — missing: {sorted(norm - actual_norm)}, "
            f"extra: {sorted(actual_norm - norm)}")
    if story_count() != 50:
        raise ValueError(f"news.py story_count is {story_count()}, not 50")
    if sum(REGION_COUNTS.values()) != 50:
        raise ValueError("Region strip counts do not sum to 50")


def draw_header(draw, fonts):
    """Kicker line, huge serif date, sub-headline strip."""
    draw.text((MARGIN, KICKER_Y), "THE WORLD IN ONE DAY",
              font=fonts["kicker"], fill=ACCENT)
    right = "50 STORIES  ·  8 REGIONS  ·  SATURDAY 21 NOVEMBER 2026"
    rw = text_width(draw, right, fonts["kicker_right"])
    draw.text((RIGHT - rw, KICKER_Y + 1), right,
              font=fonts["kicker_right"], fill=INK)
    draw.line((MARGIN, RULE1_Y, RIGHT, RULE1_Y), fill=INK, width=2)
    draw_centered(draw, DATE_LINE.title(), fonts["date"], DATE_Y)
    draw_centered(draw, SUB_HEAD, fonts["sub"], SUB_Y)
    draw.line((MARGIN, RULE2_Y, RIGHT, RULE2_Y), fill=INK, width=2)


def draw_stats(draw, fonts):
    """Six big numbers with captions, red left bars."""
    cell_w = CONTENT // 6
    for i, (number, caption) in enumerate(STATS):
        x = MARGIN + i * cell_w
        draw.rectangle((x, STATS_Y + 2, x + 3, STATS_Y + STATS_H - 4),
                       fill=ACCENT)
        tx = x + 9
        draw.text((tx, STATS_Y), number, font=fonts["stats_num"],
                  fill=INK)
        lines = split_lines(draw, caption, fonts["stats_cap"],
                            cell_w - 14)
        if len(lines) > 2:
            raise ValueError(f"Stats caption wraps to 3 lines: {caption}")
        draw_lines(draw, lines, fonts["stats_cap"], tx, STATS_Y + 30, 12,
                   fill=INK)


def draw_region_strip(draw, fonts):
    """Coloured segments, one per region, with story counts.

    Widths start from the label width, then the leftover is shared
    out in proportion to the counts, so small regions stay legible
    while big ones stay visibly bigger.
    """
    colours = {name: colour for name, colour, _ in REGIONS}
    labels = {name: f"{name} {count}"
              for name, count in REGION_COUNTS.items()}
    widths = {}
    for name, label in labels.items():
        widths[name] = text_width(draw, label, fonts["region"]) + 14
    leftover = CONTENT - sum(widths.values())
    if leftover < 0:
        raise ValueError("Region strip labels do not fit")
    total = sum(REGION_COUNTS.values())
    for name, count in REGION_COUNTS.items():
        widths[name] += round(leftover * count / total)
    # Fix rounding drift on the largest segment.
    drift = CONTENT - sum(widths.values())
    widths["EUROPE"] += drift
    x = MARGIN
    for name in REGION_COUNTS:
        w = widths[name]
        draw.rectangle((x, REGION_Y, x + w - 1, REGION_Y + REGION_H - 1),
                       fill=colours[name])
        label = labels[name]
        lx = x + (w - text_width(draw, label, fonts["region"])) // 2
        draw.text((lx, REGION_Y + 4), label, font=fonts["region"],
                  fill="#ffffff")
        x += w


def draw_leads(image, draw, fonts):
    """Three big illustrated leads in a row; return bottom y."""
    bottom = LEADS_Y
    for i, (number, tag, headline, deck, art_name) in enumerate(LEADS):
        x = MARGIN + i * (LEAD_W + LEAD_COL_GAP)
        y = LEADS_Y
        picture = illustration(art_name, LEAD_W, LEAD_IMG_H)
        image.paste(picture, (x, y))
        draw.rectangle((x, y, x + LEAD_W - 1, y + LEAD_IMG_H - 1),
                       outline=INK, width=1)
        y += LEAD_IMG_H + 4
        # Red number chip + tag.
        chip = f"{number}"
        chip_w = text_width(draw, chip, fonts["lead_tag"]) + 12
        draw.rectangle((x, y, x + chip_w, y + 15), fill=ACCENT)
        draw.text((x + 6, y + 1), chip, font=fonts["lead_tag"],
                  fill="#ffffff")
        draw.text((x + chip_w + 6, y + 1), tag, font=fonts["lead_tag"],
                  fill=ACCENT)
        y += 19
        lines = split_lines(draw, headline, fonts["lead_head"], LEAD_W)
        if len(lines) > 2:
            raise ValueError(f"Lead headline wraps to 3 lines: {headline}")
        y = draw_lines(draw, lines, fonts["lead_head"], x, y, 20) + 2
        deck_lines = split_lines(draw, deck, fonts["lead_deck"], LEAD_W)
        if len(deck_lines) > 2:
            raise ValueError(f"Lead deck wraps to 3 lines: {deck}")
        y = draw_lines(draw, deck_lines, fonts["lead_deck"], x, y, 13)
        bottom = max(bottom, y)
    return bottom


def draw_grid(image, draw, fonts, grid_top):
    """Ten small illustrated stories, two rows of five; return bottom y."""
    row_h = None
    y = grid_top
    for row in range(2):
        row_bottom = y
        for col in range(5):
            number, tag, headline, deck, art_name = GRID[row * 5 + col]
            x = MARGIN + col * (GRID_W + GRID_GAP_X)
            cy = y
            picture = illustration(art_name, GRID_W, GRID_IMG_H)
            image.paste(picture, (x, cy))
            draw.rectangle((x, cy, x + GRID_W - 1, cy + GRID_IMG_H - 1),
                           outline=INK, width=1)
            cy += GRID_IMG_H + 3
            chip = f"{number}"
            chip_w = text_width(draw, chip, fonts["grid_tag"]) + 10
            draw.rectangle((x, cy, x + chip_w, cy + 13), fill=ACCENT)
            draw.text((x + 5, cy + 1), chip, font=fonts["grid_tag"],
                      fill="#ffffff")
            draw.text((x + chip_w + 5, cy + 1), tag,
                      font=fonts["grid_tag"], fill=ACCENT)
            cy += 16
            lines = split_lines(draw, headline, fonts["grid_head"], GRID_W)
            if len(lines) > 2:
                raise ValueError(
                    f"Grid headline wraps to 3 lines: {headline}")
            cy = draw_lines(draw, lines, fonts["grid_head"], x, cy, 12) + 1
            deck_lines = split_lines(draw, deck, fonts["grid_deck"],
                                     GRID_W)
            if len(deck_lines) > 2:
                raise ValueError(f"Grid deck wraps to 3 lines: {deck}")
            cy = draw_lines(draw, deck_lines, fonts["grid_deck"], x, cy, 12)
            row_bottom = max(row_bottom, cy)
        row_h = row_bottom - y
        y = row_bottom + GRID_GAP_Y
    return y - GRID_GAP_Y


def draw_btc_strip(draw, fonts, top):
    """Full-width WHY BITCOIN CRASHED explainer box; return bottom y."""
    draw.rectangle((MARGIN, top, RIGHT - 1, top + BTC_H - 1),
                   fill=BTC_FILL, outline=BTC_BORDER, width=2)
    tx = MARGIN + 10
    ty = top + 7
    draw.text((tx, ty), BTC_BOX_TITLE, font=fonts["btc_title"],
              fill=BTC_BORDER)
    draw.text((tx, ty + 17), BTC_BOX_SUB, font=fonts["btc_sub"],
              fill="#8a6d1a")
    # Five bullets in two columns (3 + 2), one line each.
    title_w = 218
    bullet_x = MARGIN + title_w
    bullet_w = (RIGHT - bullet_x - 10) // 2
    columns = (BTC_BOX_POINTS[:3], BTC_BOX_POINTS[3:])
    for ci, points in enumerate(columns):
        bx = bullet_x + ci * (bullet_w + 6)
        by = top + 7
        for point in points:
            line = "• " + point
            if text_width(draw, line, fonts["btc_bullet"]) > bullet_w:
                raise ValueError(f"BTC bullet too wide: {line}")
            draw.text((bx, by), line, font=fonts["btc_bullet"], fill=INK)
            by += 13
    return top + BTC_H


def draw_also(draw, fonts, top):
    """Numbered ALSO list in three columns; return bottom y."""
    # Three headlines are too long for one 10px line in a 314px column,
    # so they get a truthful shortened display form (same story).
    display = {
        "TEHRAN IN THE CROSSHAIRS AS US, ISRAEL WEIGH STRIKE":
            "US, ISRAEL WEIGH STRIKE ON TEHRAN",
    }
    draw.rectangle((MARGIN, top, RIGHT - 1, top + ALSO_HEAD_H - 1),
                   fill=NAVY)
    head = "ALSO ON SATURDAY 21 NOVEMBER — 37 MORE STORIES"
    draw.text((MARGIN + 8, top + 3), head, font=fonts["also_head"],
              fill="#ffffff")
    items = also_stories()
    columns = (items[:13], items[13:25], items[25:])
    y = top + ALSO_HEAD_H + 4
    for ci, column in enumerate(columns):
        x = MARGIN + ci * (ALSO_W + ALSO_COL_GAP)
        cy = y
        for number, headline in column:
            line = f"{number}  {display.get(headline, headline)}"
            if text_width(draw, line, fonts["also_item"]) > ALSO_W:
                raise ValueError(f"ALSO line too wide: {line}")
            draw.text((x, cy), line, font=fonts["also_item"], fill=INK)
            cy += 12
    return y + 13 * 12


def draw_bottom(image, draw, fonts, top):
    """Dotted world map with pins (left) + DATE CHECK box (right)."""
    map_x0 = MARGIN
    map_x1 = MARGIN + 562
    dc_x0 = map_x1 + 12
    dc_x1 = RIGHT
    # Map header + note.
    draw.text((map_x0, top), "WHERE IT HAPPENED", font=fonts["map_head"],
              fill=INK)
    draw.line((map_x0, top + 15, map_x1, top + 15), fill=INK, width=2)
    map_y0 = top + 19
    map_y1 = top + BOTTOM_H - 14
    # Nudged pins are drawn only by the leader-line loop below, so
    # they are excluded here to avoid a duplicate badge.
    plain_pins = [(n, lon, lat) for n, lon, lat, dx, dy in PINS
                  if dx == 0 and dy == 0]
    art.draw_dotted_map(draw, map_x0, map_y0, map_x1, map_y1,
                        plain_pins, dot_fill="#7a1f1f")
    # Nudged pins get a leader line from the true spot to the badge.
    pin_font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 8)
    for number, lon, lat, dx, dy in PINS:
        if dx == 0 and dy == 0:
            continue
        mx, my = art.lonlat_to_mask(lon, lat)
        tx = map_x0 + (mx / 240) * (map_x1 - map_x0)
        ty = map_y0 + (my / 120) * (map_y1 - map_y0)
        bx, by = tx + dx, ty + dy
        draw.line((tx, ty, bx, by), fill="#b32b23", width=1)
        r = 7 if number >= 10 else 6
        draw.ellipse((bx - r - 1, by - r - 1, bx + r + 1, by + r + 1),
                     fill="#ffffff")
        draw.ellipse((bx - r, by - r, bx + r, by + r), fill="#b32b23")
        label = str(number)
        box = draw.textbbox((0, 0), label, font=pin_font)
        tw, th = box[2] - box[0], box[3] - box[1]
        draw.text((bx - tw / 2 - box[0], by - th / 2 - box[1]), label,
                  font=pin_font, fill="#ffffff")
    draw.text((map_x0, top + BOTTOM_H - 12),
              "Pins 1–13 mark the illustrated stories. 12 is in space: "
              "Voyager 1. Map: simplified world outline.",
              font=fonts["map_note"], fill=CAPTION)
    # DATE CHECK box.
    draw.rectangle((dc_x0, top, dc_x1 - 1, top + BOTTOM_H - 1),
                   fill="#fdf6e3", outline=ACCENT, width=2)
    tx = dc_x0 + 10
    ty = top + 7
    draw.text((tx, ty), "DATE CHECK — WHAT WE LEFT OUT",
              font=fonts["dc_title"], fill=ACCENT)
    ty += 19
    inner = dc_x1 - dc_x0 - 20
    for item in DATE_CHECK:
        lines = split_lines(draw, "✕ " + item, fonts["dc_item"], inner)
        ty = draw_lines(draw, lines, fonts["dc_item"], tx, ty, 13,
                        fill=INK) + 1
    return top + BOTTOM_H


def draw_footer(draw, fonts, top):
    """Markets ticker, trending strip, sources note; return bottom y."""
    draw.line((MARGIN, top, RIGHT, top), fill=RULE, width=1)
    y = top + 4
    y = draw_centered(draw, MARKETS_LINE, fonts["footer"], y) + 1
    y = draw_centered(draw, TRENDING_LINE, fonts["footer_bold"], y) + 1
    y = draw_centered(draw, FOOTER_SOURCES, fonts["footer_small"], y)
    return y


def main():
    verify_story_set()
    image = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(image)
    fonts = load_fonts()

    draw_header(draw, fonts)
    draw_stats(draw, fonts)
    draw_region_strip(draw, fonts)
    leads_bottom = draw_leads(image, draw, fonts)
    grid_top = leads_bottom + 6
    grid_bottom = draw_grid(image, draw, fonts, grid_top)
    btc_bottom = draw_btc_strip(draw, fonts, grid_bottom + 6)
    also_bottom = draw_also(draw, fonts, btc_bottom + 6)
    bottom = draw_bottom(image, draw, fonts, also_bottom + 6)
    footer_bottom = draw_footer(draw, fonts, bottom + 4)

    print(f"leads bottom: {leads_bottom}, grid top: {grid_top}, "
          f"grid bottom: {grid_bottom}")
    print(f"btc bottom: {btc_bottom}, also bottom: {also_bottom}, "
          f"bottom band: {bottom}, footer bottom: {footer_bottom}")
    if footer_bottom > 1020:
        raise ValueError(
            f"Page overflows by {footer_bottom - 1020}px")

    out = Path(__file__).with_name("entry.png")
    image.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, "
          f"{story_count()} stories)")


if __name__ == "__main__":
    main()
