#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Wednesday, 25 November 2026.

Every story on the page was in the 25 November 2026 news cycle
(New York Times, CNN, Reuters, BBC, Al Jazeera, WHO). The picture is
drawn entirely with Pillow primitives and DejaVu fonts: no photographs,
no borrowed art. Output: entry.png, 1024 x 1024, well under 1 MiB.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
STEEL = (70, 96, 122)
GOLD = (196, 148, 32)
DARK = (16, 24, 40)
SCREEN = (46, 120, 180)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw a wrapped paragraph; return the y just below it."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, fill=RED):
    draw.text((x, y), text.upper(), font=SANS_B(17), fill=fill)
    return y + 24


def headline(draw, x, y, text, size, width, fill=INK):
    fnt = SERIF_B(size)
    y2 = para(draw, x, y, text, fnt, width, fill=fill,
              leading=int(size * 1.12))
    return y2


def draw_cyber_scene(draw, x, y, w, h):
    """A dark server room under attack: racks of servers, a red alert
    triangle, and a cracked shield over the data. All Pillow primitives."""
    draw.rectangle([x, y, x + w, y + h], fill=DARK)
    # glowing data streams across the top
    for i, yy in enumerate((y + 22, y + 48, y + 74)):
        col = (60, 160, 220) if i % 2 == 0 else (90, 200, 140)
        for xx in range(x + 20, x + w - 20, 46):
            draw.rectangle([xx, yy, xx + 26, yy + 5], fill=col)
    # server racks
    for rx in (x + 30, x + 210, x + 390):
        draw.rectangle([rx, y + 100, rx + 150, y + h - 40],
                       fill=(30, 44, 66), outline=(70, 100, 140), width=2)
        for row in range(5):
            ry = y + 112 + row * 22
            draw.rectangle([rx + 10, ry, rx + 140, ry + 14],
                           fill=(52, 72, 100))
            for k in range(4):
                col = (90, 220, 120) if (row + k) % 3 else (255, 80, 60)
                draw.ellipse([rx + 16 + k * 12, ry + 4,
                              rx + 22 + k * 12, ry + 10], fill=col)
    # red alert triangle over the middle rack
    cx, cy, s = x + 285, y + 118, 34
    draw.polygon([(cx, cy - s), (cx + s * 0.7, cy + s * 0.6),
                  (cx - s * 0.7, cy + s * 0.6)],
                 fill=(220, 40, 40), outline=(255, 220, 120))
    draw.text((cx, cy - 4), "!", font=SANS_B(30), fill=(255, 255, 255),
              anchor="ma")
    # cracked shield at the right
    sx, sy = x + 520, y + 150
    draw.polygon([(sx, sy - 42), (sx + 34, sy - 28), (sx + 34, sy + 6),
                  (sx, sy + 42), (sx - 34, sy + 6), (sx - 34, sy - 28)],
                 fill=(46, 120, 180), outline=(255, 220, 120), width=3)
    draw.line([(sx - 6, sy - 34), (sx + 8, sy - 8), (sx - 8, sy + 12),
               (sx + 6, sy + 34)], fill=(255, 220, 120), width=4)
    # caption strip
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(22, 22, 22))
    draw.text((x + 12, y + h - 22),
              "The CIA and ODNI's open-source intelligence network was breached.",
              font=SANS(15), fill=(240, 240, 240))


def draw_tower(draw, cx, cy, s):
    """A tall skyscraper (Riyadh's PIF tower) with a blast burst."""
    draw.polygon([(cx - s * 0.3, cy + s * 0.6), (cx - s * 0.22, cy - s * 0.7),
                  (cx + s * 0.22, cy - s * 0.7), (cx + s * 0.3, cy + s * 0.6)],
                 fill=(70, 96, 122))
    for row in range(4):
        yy = cy - s * 0.5 + row * s * 0.28
        draw.line([(cx - s * 0.2, yy), (cx + s * 0.2, yy)],
                  fill=(220, 230, 240), width=3)
    bx, by = cx + s * 0.32, cy - s * 0.55
    for r, col in ((20, (255, 176, 32)), (13, (255, 120, 24)), (7, (255, 214, 96))):
        pts = []
        for k in range(10):
            ang = k * 3.14159 / 5
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
        draw.polygon(pts, fill=col)


def draw_shield(draw, cx, cy, s):
    """A shield (missile defence) with a small rocket arrow."""
    draw.polygon([(cx, cy - s * 0.7), (cx + s * 0.55, cy - s * 0.45),
                  (cx + s * 0.55, cy + s * 0.1), (cx, cy + s * 0.7),
                  (cx - s * 0.55, cy + s * 0.1), (cx - s * 0.55, cy - s * 0.45)],
                 fill=(28, 68, 128), outline=INK)
    draw.line([(cx - s * 0.25, cy + s * 0.35), (cx + s * 0.25, cy - s * 0.3)],
              fill=(255, 255, 255), width=5)
    draw.polygon([(cx + s * 0.25, cy - s * 0.3), (cx + s * 0.05, cy - s * 0.32),
                  (cx + s * 0.28, cy - s * 0.08)], fill=(255, 255, 255))


def draw_cross(draw, cx, cy, s):
    """A medical cross in a circle (WHO / Ebola response)."""
    r = s * 0.62
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=RED, width=4)
    draw.rectangle([cx - s * 0.14, cy - s * 0.4, cx + s * 0.14, cy + s * 0.4],
                   fill=RED)
    draw.rectangle([cx - s * 0.4, cy - s * 0.14, cx + s * 0.4, cy + s * 0.14],
                   fill=RED)


def draw_chart(draw, cx, cy, s):
    """Rising bars and an arrow (consumer confidence)."""
    base = cy + s * 0.55
    for i, h in enumerate((0.35, 0.5, 0.65, 0.9)):
        bx = cx - s * 0.55 + i * s * 0.32
        draw.rectangle([bx, base - s * h, bx + s * 0.2, base],
                       fill=(28, 68, 128))
    draw.line([(cx - s * 0.55, base - s * 0.3), (cx + s * 0.55, base - s * 0.85)],
              fill=RED, width=6)
    draw.polygon([(cx + s * 0.55, base - s * 0.85), (cx + s * 0.28, base - s * 0.88),
                  (cx + s * 0.52, base - s * 0.58)], fill=RED)


def draw_chip(draw, cx, cy, s):
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   fill=(30, 30, 34))
    draw.rectangle([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4],
                   fill=(196, 148, 32))
    for i in range(3):
        off = (i - 1) * s // 4
        draw.line([(cx + off, cy - s // 2 - 10), (cx + off, cy - s // 2)], fill=INK, width=3)
        draw.line([(cx + off, cy + s // 2), (cx + off, cy + s // 2 + 10)], fill=INK, width=3)
        draw.line([(cx - s // 2 - 10, cy + off), (cx - s // 2, cy + off)], fill=INK, width=3)
        draw.line([(cx + s // 2, cy + off), (cx + s // 2 + 10, cy + off)], fill=INK, width=3)


def story_block(draw, x, y, w, icon, kick, head, body, hsize=30):
    """A small story: icon on the left, kicker, headline, standfirst."""
    y = kicker(draw, x + 96, y, kick)
    icon(draw, x + 44, y + 8, 64)
    y = headline(draw, x + 96, y, head, hsize, w - 96)
    y = para(draw, x + 96, y + 4, body, SANS(18), w - 96)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- Masthead ----
    d.text((W // 2, 18), "THE WORLD", font=SERIF_B(96), fill=INK, anchor="ma")
    rule(d, M, 128, W - M, 4)
    d.text((W // 2, 140), "WEDNESDAY, 25 NOVEMBER 2026", font=SANS_B(30),
           fill=RED, anchor="ma")
    d.text((W // 2, 178), "One day's world news, in one picture  •  Price: one careful look",
           font=SANS(18), fill=(90, 90, 90), anchor="ma")
    rule(d, M, 210, W - M, 2)

    # ---- Lead story: CIA / ODNI cyber breach ----
    ly = 228
    draw_cyber_scene(d, M, ly, 600, 220)
    y = ly + 236
    y = kicker(d, M, y, "Lead story — US intelligence")
    y = headline(d, M, y, "CIA AND ODNI HIT BY CYBER BREACH", 40, 600)
    y = para(d, M, y + 6,
             "The CIA and the Office of the Director of National "
             "Intelligence discovered a breach of the unclassified network "
             "they use to analyse open-source intelligence. Officials said "
             "no classified systems were affected, and the attacker is "
             "unknown. (New York Times, CNN, Reuters)",
             SANS(20), 600)
    rule(d, M, y + 14, M + 600, 2)

    # ---- Right column: Riyadh strike + Saudi missile defences ----
    rx, rw = M + 624, 328
    y = ly
    y = story_block(d, rx, y, rw, draw_tower, "Middle East — Riyadh",
                    "HOUTHI DRONE HITS RIYADH TOWER",
                    "A Houthi drone struck Riyadh's tallest tower, home of "
                    "the Public Investment Fund, wounding 11 people. "
                    "(Reuters)", 26)
    rule(d, rx, y + 12, rx + rw, 2)
    y = story_block(d, rx, y + 28, rw, draw_shield, "Middle East — Defence",
                    "RIYADH SEEKS DEFENCES",
                    "Riyadh asked allies to help restock its missile "
                    "defences. (Reuters)", 26)
    rule(d, rx, y + 12, rx + rw, 2)

    # ---- Bottom row: three stories ----
    by = 740
    rule(d, M, by - 14, W - M, 2)
    col_w = (W - 2 * M - 48) // 3
    xs = [M, M + col_w + 24, M + 2 * (col_w + 24)]
    stories = [
        (draw_cross, "Health — DR Congo",
         "WHO FLEES EBOLA HOSPITAL",
         "WHO evacuated staff from a hospital in Ituri, DR Congo, after "
         "three days sheltering from fierce fighting. (WHO)"),
        (draw_chart, "Business — US economy",
         "US CONFIDENCE SOARS",
         "US consumer confidence jumped to its highest in nearly two "
         "years, on optimism over jobs. (Reuters)"),
        (draw_chip, "Tech — Huawei",
         "HUAWEI GUILTY OF THEFT",
         "A US jury found Huawei guilty of stealing trade secrets, on "
         "10 of 12 counts, but acquitted it of racketeering. "
         "(Reuters, BBC)"),
    ]
    for x, (icon, kick, head, body) in zip(xs, stories):
        y = by
        y = kicker(d, x, y, kick)
        icon(d, x + 30, y + 44, 44)
        y = headline(d, x + 84, y, head, 24, col_w - 84)
        y = para(d, x, y + 6, body, SANS(18), col_w)

    # ---- Footer ----
    rule(d, M, 952, W - M, 2)
    d.text((W // 2, 962),
           "Sources: New York Times • CNN • Reuters • BBC • Al Jazeera • WHO  —  Stories of the 25 November 2026 news cycle",
           font=SANS(16), fill=(90, 90, 90), anchor="ma")

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, "entry.png"), optimize=True)
    print("wrote", os.path.join(out, "entry.png"), img.size)


if __name__ == "__main__":
    main()
