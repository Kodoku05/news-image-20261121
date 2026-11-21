"""Flat vector-style illustrations for the v5 front page.

All artwork here is original, drawn programmatically with Pillow:
night skylines, a cyclone spiral, scales of justice, a candle, a
cricket scene, a spacecraft, three flags, and a dotted world map.
Nothing is copied, traced, or reused from any other entry's artwork.
Positions that look random use fixed seeds, so every render is
byte-identical.

Each function takes a target size and returns an RGB image.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ART = Path(__file__).with_name("art")

# Coarse continent polygons on a 240x120 mask (west -> east, north ->
# south), sampled as dots for the "WHERE IT HAPPENED" map.
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


def canvas(w, h, colour):
    img = Image.new("RGB", (w, h), colour)
    return img, ImageDraw.Draw(img)


def starburst(draw, cx, cy, r_outer, r_inner, points=12, fill="#ffb000"):
    """Explosion star: alternating long/short spikes."""
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def stars(draw, w, h, count, seed, ymax=None):
    """Deterministic star field (fixed seed => identical every run)."""
    rng = random.Random(seed)
    ymax = h if ymax is None else ymax
    for _ in range(count):
        x = rng.uniform(2, w - 2)
        y = rng.uniform(2, ymax)
        r = rng.choice((0.7, 1.0, 1.3))
        draw.ellipse((x - r, y - r, x + r, y + r), fill="#e8ecf5")


def skyline(draw, w, h, base_y, colour, windows, seed, lit="#ffd76a"):
    """Dark building silhouettes with a few lit windows."""
    rng = random.Random(seed)
    x = 0
    while x < w:
        bw = rng.randint(w // 9, w // 5)
        bh = rng.randint(h // 4, int(h * 0.62))
        draw.rectangle((x, base_y - bh, min(x + bw, w), base_y), fill=colour)
        for _ in range(windows):
            wx = rng.uniform(x + 3, x + bw - 6)
            wy = rng.uniform(base_y - bh + 4, base_y - 8)
            draw.rectangle((wx, wy, wx + 3, wy + 4), fill=lit)
        x += bw + rng.randint(1, 4)


def kyiv_night(w, h):
    """Lead illustration: night barrage over Kyiv."""
    img, draw = canvas(w, h, "#0d1b2e")
    stars(draw, w, h, 42, seed=7, ymax=int(h * 0.55))
    # Crescent moon: the cutout is offset far enough to read as a
    # crescent rather than a ring.
    draw.ellipse((w - 34, 6, w - 12, 28), fill="#f2ead2")  # moon
    draw.ellipse((w - 26, 4, w - 6, 28), fill="#0d1b2e")
    skyline(draw, w, h, h - 6, "#060d18", 26, seed=11)
    # Ground glow + two explosions.
    draw.ellipse((w * 0.08, h - 22, w * 0.5, h + 6), fill="#7a2d12")
    starburst(draw, w * 0.30, h * 0.42, 20, 8, fill="#ff9d00")
    starburst(draw, w * 0.30, h * 0.42, 10, 4, fill="#ffe066")
    starburst(draw, w * 0.68, h * 0.30, 15, 6, fill="#ff9d00")
    starburst(draw, w * 0.68, h * 0.30, 7, 3, fill="#ffe066")
    # Missile streaks.
    draw.line((w * 0.52, 8, w * 0.68, h * 0.30), fill="#ffd76a", width=2)
    draw.line((w * 0.12, 6, w * 0.30, h * 0.42), fill="#ffd76a", width=2)
    return img


def cop31_globe(w, h):
    """Lead illustration: a warming globe, a thermometer, no deal."""
    img, draw = canvas(w, h, "#dcead9")
    # Globe.
    gx, gy, gr = w * 0.32, h * 0.52, min(w, h) * 0.42
    draw.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill="#3f7fbf",
                 outline="#1f4d7a", width=2)
    draw.ellipse((gx - gr * 0.55, gy - gr * 0.6, gx + gr * 0.1,
                  gy - gr * 0.05), fill="#69a85e")
    draw.ellipse((gx - gr * 0.1, gy + gr * 0.15, gx + gr * 0.6,
                  gy + gr * 0.65), fill="#69a85e")
    draw.ellipse((gx + gr * 0.25, gy - gr * 0.7, gx + gr * 0.7,
                  gy - gr * 0.25), fill="#69a85e")
    # Thermometer, mercury near the top.
    tx = w * 0.72
    draw.rectangle((tx - 6, h * 0.12, tx + 6, h * 0.78), fill="#f4f1e6",
                   outline="#8a1f1f", width=2)
    draw.ellipse((tx - 13, h * 0.72, tx + 13, h * 0.98), fill="#c22f2f",
                 outline="#8a1f1f", width=2)
    draw.rectangle((tx - 3, h * 0.22, tx + 3, h * 0.80), fill="#c22f2f")
    # Red "no deal" cross over a draft sheet.
    sx, sy = w * 0.86, h * 0.30
    draw.rectangle((sx, sy, sx + 34, sy + 44), fill="#ffffff",
                   outline="#5a5245", width=1)
    for i in range(4):
        ly = sy + 8 + i * 8
        draw.line((sx + 5, ly, sx + 29, ly), fill="#9a938a", width=2)
    draw.line((sx - 4, sy - 4, sx + 38, sy + 48), fill="#c22f2f", width=4)
    draw.line((sx + 38, sy - 4, sx - 4, sy + 48), fill="#c22f2f", width=4)
    return img


def kryvyi_rih(w, h):
    """Dusk strike: smoke column over a darkened city."""
    img, draw = canvas(w, h, "#e8c9a0")
    draw.rectangle((0, 0, w, h * 0.55), fill="#d98d5f")
    skyline(draw, w, h, h - 2, "#3a2a26", 8, seed=23, lit="#ffd76a")
    # Smoke column.
    for i, (sx, sy, sr) in enumerate(((0.62, 0.72, 9), (0.60, 0.55, 12),
                                      (0.63, 0.38, 14), (0.58, 0.22, 11))):
        draw.ellipse((w * sx - sr, h * sy - sr, w * sx + sr, h * sy + sr),
                     fill="#6b625c" if i % 2 else "#7d7470")
    starburst(draw, w * 0.30, h * 0.55, 13, 5, fill="#ff9d00")
    starburst(draw, w * 0.30, h * 0.55, 6, 2.5, fill="#ffe066")
    return img


def cyclone(w, h):
    """Cyclone spiral over the sea, coastline below."""
    img, draw = canvas(w, h, "#7fb3d9")
    cx, cy = w * 0.52, h * 0.48
    for i, r in enumerate((34, 27, 20, 13, 7)):
        start = 200 + i * 55
        draw.arc((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8),
                 start=start, end=start + 250, fill="#ffffff", width=4)
    draw.ellipse((cx - 4, cy - 3, cx + 4, cy + 3), fill="#ffffff")
    # Coastline.
    draw.polygon([(0, h), (0, h * 0.82), (w * 0.3, h * 0.88),
                  (w * 0.6, h * 0.80), (w, h * 0.90), (w, h)],
                 fill="#c9a86a")
    # Rain streaks.
    for x in range(6, w, 18):
        draw.line((x, 4, x - 4, 14), fill="#dfeef7", width=1)
    return img


def scales(w, h):
    """Scales of justice on a teal ground."""
    img, draw = canvas(w, h, "#bfe3dd")
    cx = w * 0.5
    draw.rectangle((cx - 2, h * 0.16, cx + 2, h * 0.84), fill="#7a5a1f")
    draw.rectangle((cx - 26, h * 0.84, cx + 26, h * 0.90), fill="#7a5a1f")
    draw.line((cx - 34, h * 0.24, cx + 34, h * 0.24), fill="#7a5a1f",
              width=3)
    draw.ellipse((cx - 4, h * 0.12, cx + 4, h * 0.22), fill="#c9a227")
    for sx in (cx - 34, cx + 34):
        draw.line((sx, h * 0.24, sx - 12, h * 0.58), fill="#7a5a1f",
                  width=2)
        draw.line((sx, h * 0.24, sx + 12, h * 0.58), fill="#7a5a1f",
                  width=2)
        draw.arc((sx - 13, h * 0.50, sx + 13, h * 0.74), start=0, end=180,
                 fill="#c9a227", width=3)
    return img


def interception(w, h):
    """Night interception: missile streak meets a burst over Riyadh."""
    img, draw = canvas(w, h, "#101b30")
    stars(draw, w, h, 22, seed=31, ymax=int(h * 0.5))
    skyline(draw, w, h, h - 2, "#050a14", 12, seed=37)
    # Tower silhouette (tall, centre-right).
    draw.rectangle((w * 0.68, h * 0.30, w * 0.78, h - 2), fill="#050a14")
    draw.polygon([(w * 0.68, h * 0.30), (w * 0.73, h * 0.16),
                  (w * 0.78, h * 0.30)], fill="#050a14")
    # Incoming streak + interception burst.
    draw.line((w * 0.08, 4, w * 0.45, h * 0.42), fill="#ff8a5c", width=2)
    starburst(draw, w * 0.45, h * 0.42, 14, 6, fill="#ffd76a")
    starburst(draw, w * 0.45, h * 0.42, 7, 3, fill="#fff3c4")
    draw.line((w * 0.80, h - 4, w * 0.47, h * 0.44), fill="#9fd0ff",
              width=2)
    return img


def candle(w, h):
    """A single candle flame on a dark ground."""
    img, draw = canvas(w, h, "#1c1a24")
    cx = w * 0.5
    for r, col in ((34, "#2c2836"), (26, "#3a3244"), (18, "#4a3f52")):
        draw.ellipse((cx - r, h * 0.42 - r * 0.8, cx + r,
                      h * 0.42 + r * 0.8), fill=col)
    draw.rectangle((cx - 7, h * 0.48, cx + 7, h * 0.92), fill="#efe8d8")
    draw.rectangle((cx - 1, h * 0.42, cx + 1, h * 0.50), fill="#3a2a1a")
    draw.ellipse((cx - 6, h * 0.16, cx + 6, h * 0.44), fill="#ff9d00")
    draw.ellipse((cx - 3, h * 0.24, cx + 3, h * 0.42), fill="#ffe066")
    draw.rectangle((cx - 12, h * 0.90, cx + 12, h * 0.95), fill="#8a7a5a")
    return img


def chip(w, h):
    """A computer chip beside a subpoena document."""
    img, draw = canvas(w, h, "#12261a")
    cx, cy, s = w * 0.34, h * 0.52, min(w, h) * 0.30
    for i in range(5):
        off = -s + i * (2 * s / 4)
        draw.line((cx + off, cy - s - 7, cx + off, cy - s), fill="#c9c9c9",
                  width=2)
        draw.line((cx + off, cy + s, cx + off, cy + s + 7), fill="#c9c9c9",
                  width=2)
        draw.line((cx - s - 7, cy + off, cx - s, cy + off), fill="#c9c9c9",
                  width=2)
        draw.line((cx + s, cy + off, cx + s + 7, cy + off), fill="#c9c9c9",
                  width=2)
    draw.rectangle((cx - s, cy - s, cx + s, cy + s), fill="#1f9d55",
                   outline="#0d5c2e", width=2)
    draw.rectangle((cx - s * 0.45, cy - s * 0.45, cx + s * 0.45,
                    cy + s * 0.45), fill="#0d5c2e")
    # Document.
    dx, dy = w * 0.68, h * 0.18
    draw.rectangle((dx, dy, dx + 34, dy + 40), fill="#ffffff",
                   outline="#5a5245", width=1)
    for i in range(4):
        ly = dy + 8 + i * 8
        draw.line((dx + 5, ly, dx + 29, ly), fill="#9a938a", width=2)
    draw.ellipse((dx + 22, dy + 30, dx + 32, dy + 40), fill="#b32b23")
    return img


def cricket(w, h):
    """Cricket: bat, ball and stumps on a green field.

    High-contrast shapes: the first version's tan bat vanished
    against the tan pitch, so the bat is dark brown and the stumps
    carry a dark outline.
    """
    img, draw = canvas(w, h, "#7fae5a")
    draw.rectangle((0, h * 0.62, w, h), fill="#5d8f3e")
    # Pitch: a light strip down the middle.
    draw.rectangle((w * 0.38, h * 0.18, w * 0.60, h * 0.96),
                   fill="#d9c49a", outline="#a8895a")
    # Stumps: three yellow posts with a dark outline.
    for sx in (0.44, 0.49, 0.54):
        draw.rectangle((w * sx - 2, h * 0.22, w * sx + 2, h * 0.52),
                       fill="#f2d060", outline="#7a5a1f")
    # Bat: a thick dark-brown diagonal across the pitch.
    draw.line((w * 0.56, h * 0.26, w * 0.44, h * 0.82), fill="#7a5230",
              width=6)
    draw.line((w * 0.56, h * 0.26, w * 0.44, h * 0.82), fill="#a97c46",
              width=2)
    # Ball: red with a white highlight, bottom right.
    draw.ellipse((w * 0.76, h * 0.60, w * 0.88, h * 0.92), fill="#b32b23",
                 outline="#7a1f1f")
    draw.ellipse((w * 0.78, h * 0.64, w * 0.82, h * 0.74),
                 fill="#ff8a7a")
    return img


def voyager(w, h):
    """Voyager 1: dish and bus against the stars."""
    img, draw = canvas(w, h, "#060814")
    stars(draw, w, h, 30, seed=53)
    cx, cy = w * 0.46, h * 0.52
    # Dish.
    draw.arc((cx - 26, cy - 20, cx + 10, cy + 20), start=90, end=270,
             fill="#d9d9d9", width=4)
    draw.line((cx - 8, cy, cx + 14, cy), fill="#d9d9d9", width=3)
    # Bus + boom + antenna.
    draw.rectangle((cx + 8, cy - 8, cx + 26, cy + 8), fill="#c9a227",
                   outline="#8a6d1a")
    draw.line((cx + 26, cy, cx + 40, cy - 12), fill="#d9d9d9", width=2)
    draw.ellipse((cx + 38, cy - 16, cx + 44, cy - 10), fill="#ff9d00")
    draw.line((cx + 17, cy - 8, cx + 17, cy - 22), fill="#d9d9d9", width=2)
    return img


def flags(w, h):
    """Three flags on poles: United States, China, Russia."""
    img, draw = canvas(w, h, "#bcd6e8")
    draw.rectangle((0, h * 0.86, w, h), fill="#8a9a6a")
    poles = (w * 0.18, w * 0.50, w * 0.82)
    for px in poles:
        draw.line((px, h * 0.10, px, h * 0.88), fill="#5a5245", width=2)
        draw.ellipse((px - 2, h * 0.06, px + 2, h * 0.12), fill="#c9a227")
    fw, fh = 34, 20
    # United States: stripes + canton.
    ux, uy = poles[0] + 2, h * 0.14
    for i in range(5):
        draw.rectangle((ux, uy + i * fh / 5, ux + fw,
                        uy + (i + 1) * fh / 5),
                       fill="#b32b23" if i % 2 == 0 else "#f4f1e6")
    draw.rectangle((ux, uy, ux + fw * 0.4, uy + fh * 0.6), fill="#1f4d7a")
    # China: red field, yellow stars.
    cx, cy = poles[1] + 2, h * 0.14
    draw.rectangle((cx, cy, cx + fw, cy + fh), fill="#c22f2f")
    starburst(draw, cx + 8, cy + 6, 5, 2, points=5, fill="#ffd76a")
    starburst(draw, cx + 20, cy + 4, 3, 1.2, points=5, fill="#ffd76a")
    starburst(draw, cx + 24, cy + 10, 3, 1.2, points=5, fill="#ffd76a")
    # Russia: white-blue-red horizontal bands.
    rx, ry = poles[2] + 2, h * 0.14
    for i, col in enumerate(("#f4f1e6", "#1f4d7a", "#c22f2f")):
        draw.rectangle((rx, ry + i * fh / 3, rx + fw,
                        ry + (i + 1) * fh / 3), fill=col)
    return img


def framed_art(name, w, h):
    """Load one of our generated art assets, fitted to w x h."""
    art = Image.open(ART / name).convert("RGB")
    return ImageOps.fit(art, (w, h), Image.LANCZOS)


def map_mask():
    """240x120 land mask for the dotted world map."""
    mask = Image.new("L", (240, 120), 0)
    mask_draw = ImageDraw.Draw(mask)
    for poly in CONTINENTS:
        mask_draw.polygon(poly, fill=255)
    for x, y, r in ISLANDS:
        mask_draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
    return mask


def lonlat_to_mask(lon, lat):
    """Map lon/lat to mask coordinates (mask spans -180..180 lon,
    90..-60 lat)."""
    return ((lon + 180) / 360 * 240, (90 - lat) / 150 * 120)


def draw_dotted_map(draw, x0, y0, x1, y1, pins, dot_fill="#8a1f1f"):
    """Draw the dotted world map in the given box (squashed to fit,
    like a newspaper locator map) and numbered pins.

    pins: list of (number, lon, lat). Returns nothing.
    """
    mask = map_mask()
    px = mask.load()
    # Sample in OUTPUT space so dot density is even in both directions
    # (sampling in mask space made horizontal gaps ~3x the vertical
    # ones and the continents read as streaks).
    step = 4
    dot_r = 1.3
    box_w, box_h = x1 - x0, y1 - y0
    y = y0 + step // 2
    while y < y1:
        x = x0 + step // 2
        while x < x1:
            gx = min(239, int((x - x0) / box_w * 240))
            gy = min(119, int((y - y0) / box_h * 120))
            if px[gx, gy]:
                draw.ellipse((x - dot_r, y - dot_r, x + dot_r, y + dot_r),
                             fill=dot_fill)
            x += step
        y += step
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 8)
    for number, lon, lat in pins:
        mx, my = lonlat_to_mask(lon, lat)
        x = x0 + (mx / 240) * (x1 - x0)
        y = y0 + (my / 120) * (y1 - y0)
        r = 7 if number >= 10 else 6
        draw.ellipse((x - r - 1, y - r - 1, x + r + 1, y + r + 1),
                     fill="#ffffff")
        draw.ellipse((x - r, y - r, x + r, y + r), fill="#b32b23")
        label = str(number)
        box = draw.textbbox((0, 0), label, font=font)
        tw, th = box[2] - box[0], box[3] - box[1]
        draw.text((x - tw / 2 - box[0], y - th / 2 - box[1]), label,
                  font=font, fill="#ffffff")
