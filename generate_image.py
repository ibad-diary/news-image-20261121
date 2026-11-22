#!/usr/bin/env python3
"""Render the one-page newspaper for Saturday 21 November 2026.

Reads stories.json next to this file and writes entry.png (1024x1024,
deterministic: fixed fonts, fixed strings, no clock, no randomness).
"""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
MUTED = (90, 86, 78)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
SEA = (214, 228, 238)
LAND = (232, 226, 210)
GOLD = (180, 130, 30)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, kind, cx, cy, s, color):
    """Small hand-drawn pictograms, centred on (cx, cy), size s."""
    h = s / 2.0
    if kind == "globe":
        draw.ellipse([cx - h, cy - h, cx + h, cy + h], outline=color, width=3)
        draw.ellipse([cx - h * 0.45, cy - h, cx + h * 0.45, cy + h],
                     outline=color, width=2)
        draw.line([cx - h, cy, cx + h, cy], fill=color, width=2)
        draw.line([cx - h * 0.82, cy - h * 0.55, cx + h * 0.82, cy - h * 0.55],
                  fill=color, width=1)
        draw.line([cx - h * 0.82, cy + h * 0.55, cx + h * 0.82, cy + h * 0.55],
                  fill=color, width=1)
    elif kind == "blast":
        pts = []
        for i in range(16):
            ang = math.pi * i / 8.0
            r = h if i % 2 == 0 else h * 0.45
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        draw.polygon(pts, fill=(234, 88, 12), outline=color)
        draw.ellipse([cx - h * 0.28, cy - h * 0.28, cx + h * 0.28, cy + h * 0.28],
                     fill=(255, 255, 255))
    elif kind == "quake":
        draw.line([(cx - h, cy + h * 0.3), (cx - h * 0.5, cy - h * 0.4),
                   (cx, cy + h * 0.4), (cx + h * 0.5, cy - h * 0.4),
                   (cx + h, cy + h * 0.3)], fill=color, width=3)
        draw.ellipse([cx - h * 0.15, cy - h * 0.85, cx + h * 0.15, cy - h * 0.55],
                     fill=RED)
    elif kind == "ship":
        draw.polygon([(cx - h, cy + h * 0.1), (cx + h, cy + h * 0.1),
                      (cx + h * 0.7, cy + h * 0.7), (cx - h * 0.7, cy + h * 0.7)],
                     fill=color)
        draw.line([cx, cy + h * 0.1, cx, cy - h * 0.8], fill=color, width=3)
        draw.polygon([(cx, cy - h * 0.8), (cx + h * 0.55, cy - h * 0.55),
                      (cx, cy - h * 0.3)], fill=RED)
        for k, wx in enumerate((-0.7, 0.0, 0.7)):
            draw.arc([cx + wx * h - h * 0.25, cy + h * 0.75,
                      cx + wx * h + h * 0.25, cy + h * 1.05],
                     0, 180, fill=BLUE, width=2)
    elif kind == "cuffs":
        draw.ellipse([cx - h, cy - h * 0.45, cx - h * 0.1, cy + h * 0.45],
                     outline=color, width=4)
        draw.ellipse([cx + h * 0.1, cy - h * 0.45, cx + h, cy + h * 0.45],
                     outline=color, width=4)
        draw.line([cx - h * 0.1, cy, cx + h * 0.1, cy], fill=color, width=4)
    elif kind == "chart":
        draw.line([cx - h, cy + h, cx - h, cy - h], fill=color, width=3)
        draw.line([cx - h, cy + h, cx + h, cy + h], fill=color, width=3)
        draw.line([(cx - h * 0.8, cy - h * 0.6), (cx - h * 0.2, cy - h * 0.1),
                   (cx + h * 0.3, cy - h * 0.3), (cx + h * 0.8, cy + h * 0.6)],
                  fill=RED, width=3)
        draw.polygon([(cx + h * 0.8, cy + h * 0.6), (cx + h * 0.45, cy + h * 0.6),
                      (cx + h * 0.8, cy + h * 0.25)], fill=RED)
    elif kind == "flame":
        pts = [(cx, cy - h), (cx + h * 0.55, cy - h * 0.1),
               (cx + h * 0.7, cy + h * 0.45), (cx + h * 0.35, cy + h * 0.85),
               (cx - h * 0.35, cy + h * 0.85), (cx - h * 0.7, cy + h * 0.45),
               (cx - h * 0.55, cy - h * 0.1)]
        draw.polygon(pts, fill=(234, 88, 12))
        draw.ellipse([cx - h * 0.25, cy + h * 0.1, cx + h * 0.25, cy + h * 0.6],
                     fill=(250, 204, 21))
    elif kind == "scroll":
        draw.rectangle([cx - h * 0.8, cy - h * 0.55, cx + h * 0.8, cy + h * 0.55],
                       outline=color, width=3)
        draw.ellipse([cx - h * 0.95, cy - h * 0.7, cx - h * 0.55, cy + h * 0.7],
                     fill=color)
        draw.ellipse([cx + h * 0.55, cy - h * 0.7, cx + h * 0.95, cy + h * 0.7],
                     fill=color)
        draw.line([cx - h * 0.45, cy - h * 0.2, cx + h * 0.45, cy - h * 0.2],
                  fill=color, width=2)
        draw.line([cx - h * 0.45, cy + h * 0.2, cx + h * 0.45, cy + h * 0.2],
                  fill=color, width=2)
    elif kind == "boat":
        draw.polygon([(cx - h, cy + h * 0.2), (cx + h, cy + h * 0.2),
                      (cx + h * 0.65, cy + h * 0.75), (cx - h * 0.65, cy + h * 0.75)],
                     fill=color)
        draw.polygon([(cx, cy - h * 0.85), (cx, cy + h * 0.1),
                      (cx + h * 0.6, cy + h * 0.1)], fill=RED)
        draw.line([cx, cy - h * 0.85, cx, cy + h * 0.1], fill=color, width=2)
    elif kind == "cross":
        draw.rectangle([cx - h * 0.7, cy - h * 0.7, cx + h * 0.7, cy + h * 0.7],
                       fill=(22, 163, 74))
        draw.rectangle([cx - h * 0.16, cy - h * 0.5, cx + h * 0.16, cy + h * 0.5],
                       fill=(255, 255, 255))
        draw.rectangle([cx - h * 0.5, cy - h * 0.16, cx + h * 0.5, cy + h * 0.16],
                       fill=(255, 255, 255))
    elif kind == "target":
        for r, col in ((1.0, RED), (0.66, (255, 255, 255)), (0.33, RED)):
            draw.ellipse([cx - h * r, cy - h * r, cx + h * r, cy + h * r],
                         outline=col, width=3)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    else:
        draw.ellipse([cx - h, cy - h, cx + h, cy + h], outline=color, width=3)
        draw.text((cx, cy), "?", font=font(True, int(s * 0.6)), fill=color,
                  anchor="mm")


# Display positions: dots are nudged so neighbours do not overlap.
# The story cities stay true; only the dot is spaced for legibility.
DISPLAY = {4: (59.9, 25.0), 6: (47.91, 42.0), 7: (38.9, -80.0),
           8: (-6.12, 100.0), 9: (-6.2, 110.5), 12: (55.68, 16.0),
           13: (32.5, 43.5), 14: (41.5, -87.0), 15: (40.71, -69.0),
           2: (26.23, 53.0), 18: (24.71, 46.68), 19: (31.5, 34.47),
           20: (35.68, 139.69), 21: (22.2, 109.5), 22: (22.54, 121.0),
           23: (21.03, 99.0), 24: (24.82, 92.0), 25: (23.81, 84.0),
           26: (23.81, 100.0), 28: (48.86, -3.0), 29: (50.45, 30.52),
           31: (53.35, -9.5), 35: (-47.5, 174.78), 36: (41.72, 41.0),
           37: (40.41, 52.0)}


def project(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (83.0 - lat) / 141.0 * (y1 - y0)
    return x, y


def ellipsize(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=fnt) > max_w:
        text = text[:-1]
    return text + "…"


def tag_chip(draw, x, y, tag):
    f = font(True, 9)
    tw = draw.textlength(tag, font=f) + 10
    fill = RED if tag == "CLAIM" else (BLUE if tag == "OFFICIAL" else INK)
    draw.rounded_rectangle([x, y, x + tw, y + 14], radius=3, fill=fill)
    draw.text((x + 5, y + 7), tag, font=f, fill=(255, 255, 255), anchor="lm")
    return tw


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    stories = sorted(data["stories"], key=lambda s: s["n"])
    leads = [s for s in stories if s["kind"] == "lead"]
    feats = [s for s in stories if s["kind"] == "feature"]
    briefs = [s for s in stories if s["kind"] == "brief"]

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 86], fill=INK)
    d.text((W // 2, 30), "THE WORLD IN ONE DAY", font=font(True, 42),
           fill=(247, 243, 234), anchor="mm")
    d.text((W // 2, 66), "SATURDAY 21 NOVEMBER 2026  ·  37 STORIES  ·  10 REGIONS"
           "  ·  UPDATED 22 NOV 2026 03:30 UTC",
           font=font(True, 13), fill=(220, 200, 140), anchor="mm")

    # ---- number strip ----
    strip = data["strip"]
    sw = (W - 16 - 5 * 6) / 6
    for i, item in enumerate(strip):
        x0 = 8 + i * (sw + 6)
        d.rounded_rectangle([x0, 92, x0 + sw, 128], radius=4,
                            outline=RED, width=2, fill=(255, 255, 255))
        d.text((x0 + sw / 2, 110), item, font=font(True, 10), fill=INK,
               anchor="mm")

    # ---- leads ----
    lw = (W - 16 - 2 * 8) / 3
    for i, s in enumerate(leads):
        x0 = 8 + i * (lw + 8)
        y0 = 136
        d.rounded_rectangle([x0, y0, x0 + lw, y0 + 212], radius=5,
                            outline=(180, 175, 165), width=1,
                            fill=(255, 255, 255))
        tag_chip(d, x0 + 10, y0 + 10, s["tag"])
        d.text((x0 + lw - 10, y0 + 17), "LEAD %d" % s["n"], font=font(True, 9),
               fill=MUTED, anchor="rm")
        draw_icon(d, s["icon"], x0 + 44, y0 + 66, 56, INK)
        d.line([x0 + 84, y0 + 42, x0 + 84, y0 + 90], fill=(200, 195, 185),
               width=1)
        d.text((x0 + 96, y0 + 52), s["city"], font=font(True, 10), fill=RED)
        d.text((x0 + 96, y0 + 70), "SAT 21 NOV 2026", font=font(False, 10),
               fill=MUTED)
        title_lines = wrap(d, s["title"], font(True, 15), lw - 20)
        yy = y0 + 104
        for ln in title_lines[:3]:
            d.text((x0 + 10, yy), ln, font=font(True, 15), fill=INK)
            yy += 18
        dek_lines = wrap(d, s["dek"], font(False, 10), lw - 20)
        for ln in dek_lines[:3]:
            d.text((x0 + 10, yy), ln, font=font(False, 10), fill=MUTED)
            yy += 13

    # ---- world map ----
    mx0, my0, mx1, my1 = 8, 356, 470, 640
    d.rounded_rectangle([mx0, my0, mx1, my1], radius=5, outline=(180, 175, 165),
                        width=1, fill=(255, 255, 255))
    d.text((mx0 + 10, my0 + 14), "THE WORLD — 37 STORIES",
           font=font(True, 12), fill=INK)
    d.text((mx1 - 10, my0 + 14), "DOTS SPACED FOR LEGIBILITY",
           font=font(False, 8), fill=MUTED, anchor="ra")
    gx0, gy0, gx1, gy1 = mx0 + 8, my0 + 30, mx1 - 8, my1 - 52
    d.rectangle([gx0, gy0, gx1, gy1], fill=SEA)
    for k in range(1, 6):
        gx = gx0 + (gx1 - gx0) * k / 6
        d.line([gx, gy0, gx, gy1], fill=(190, 205, 218), width=1)
    for k in range(1, 4):
        gy = gy0 + (gy1 - gy0) * k / 4
        d.line([gx0, gy, gx1, gy], fill=(190, 205, 218), width=1)
    # rough land hints: a few soft blobs so the sea is not empty
    for (bx, by, bw, bh) in [(0.08, 0.30, 0.16, 0.30), (0.30, 0.25, 0.10, 0.35),
                             (0.44, 0.28, 0.12, 0.30), (0.58, 0.22, 0.16, 0.42),
                             (0.78, 0.35, 0.12, 0.30), (0.84, 0.62, 0.10, 0.20)]:
        d.ellipse([gx0 + bw * 0 + (gx1 - gx0) * bx,
                   gy0 + (gy1 - gy0) * by,
                   gx0 + (gx1 - gx0) * (bx + bw),
                   gy0 + (gy1 - gy0) * (by + bh)], fill=LAND)
    for s in stories:
        lat, lon = DISPLAY.get(s["n"], (s["lat"], s["lon"]))
        x, y = project(lon, lat, gx0, gy0, gx1, gy1)
        if s["n"] == 7:
            # Washington: a triangle, not a dot
            d.polygon([(x, y - 8), (x - 8, y + 6), (x + 8, y + 6)],
                      fill=RED, outline=(255, 255, 255))
            d.text((x, y - 13), "7", font=font(True, 9), fill=RED, anchor="mb")
        else:
            d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=RED,
                      outline=(255, 255, 255), width=1)
            d.text((x, y), str(s["n"]), font=font(True, 8),
                   fill=(255, 255, 255), anchor="mm")
    d.text((mx0 + 10, my1 - 40), "Washington shown as a triangle.",
           font=font(False, 8), fill=MUTED)
    d.text((mx0 + 10, my1 - 28), "Kyiv 29 · Kryvyi Rih 6 · Copenhagen 12 ·",
           font=font(False, 8), fill=MUTED)
    d.text((mx0 + 10, my1 - 16), "Gulf of Finland 4 — kept apart on purpose.",
           font=font(False, 8), fill=MUTED)

    # ---- features: 2 columns x 5 rows ----
    fw, fh = 265, 53
    for i, s in enumerate(feats):
        col, row = i % 2, i // 2
        x0 = 478 + col * (fw + 8)
        y0 = 356 + row * (fh + 4)
        d.rounded_rectangle([x0, y0, x0 + fw, y0 + fh], radius=4,
                            outline=(180, 175, 165), width=1,
                            fill=(255, 255, 255))
        d.rectangle([x0, y0, x0 + 44, y0 + fh], fill=(240, 236, 226))
        draw_icon(d, s["icon"], x0 + 22, y0 + fh / 2, 36,
                  RED if s["icon"] in ("flame", "blast") else INK)
        tag_chip(d, x0 + 50, y0 + 4, s["tag"])
        d.text((x0 + fw - 6, y0 + 11), "%d" % s["n"], font=font(True, 10),
               fill=RED, anchor="ra")
        tlines = wrap(d, s["title"], font(True, 11), fw - 56)
        yy = y0 + 20
        for ln in tlines[:2]:
            d.text((x0 + 50, yy), ln, font=font(True, 11), fill=INK)
            yy += 12
        dek = ellipsize(d, s["dek"], font(False, 9), fw - 56)
        d.text((x0 + 50, y0 + 43), dek, font=font(False, 9), fill=MUTED)

    # ---- briefs: 3 columns x 8 rows ----
    bw, bh = 336, 33
    d.text((8, 648), "THE REST OF THE DAY — 24 BRIEFS",
           font=font(True, 12), fill=INK)
    d.line([8, 664, W - 8, 664], fill=INK, width=1)
    for i, s in enumerate(briefs):
        col, row = i % 3, i // 3
        x0 = 8 + col * (bw + 8)
        y0 = 672 + row * bh
        d.text((x0, y0 + 3), "%d." % s["n"], font=font(True, 10), fill=RED)
        tlines = wrap(d, s["title"], font(True, 9), bw - 26)
        yy = y0 + 4
        for ln in tlines[:2]:
            d.text((x0 + 26, yy), ln, font=font(True, 9), fill=INK)
            yy += 11
        d.line([x0, y0 + bh - 4, x0 + bw, y0 + bh - 4],
               fill=(215, 210, 200), width=1)

    # ---- footer: date check + region tally ----
    d.line([8, 944, W - 8, 944], fill=INK, width=2)
    d.text((8, 956), "DATE CHECK", font=font(True, 10), fill=RED)
    dc_lines = wrap(d, data["date_check"], font(False, 9), 640)
    yy = 970
    for ln in dc_lines[:4]:
        d.text((8, yy), ln, font=font(False, 9), fill=INK)
        yy += 12
    tx = 680
    d.text((tx, 956), "10 REGIONS — 37 STORIES", font=font(True, 10), fill=INK)
    regions = data["regions"]
    for i, r in enumerate(regions):
        col, row = i % 2, i // 2
        x0 = tx + col * 170
        d.text((x0, 970 + row * 10),
               "%s %d" % (r["name"], r["count"]), font=font(False, 9),
               fill=INK)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (out, W, H))


if __name__ == "__main__":
    main()
