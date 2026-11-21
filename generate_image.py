# SPDX-License-Identifier: MIT
"""Draw the news-image-20261121 round-2 front page (1024x1024, PIL, stdlib only).

Original code-drawn newspaper front page: masthead, six-number strip,
region chips, three illustrated leads, ten illustrated features, a coded
world dot-map with numbered story points, a numbered brief list, and a
date-check box. All text comes from stories.json next to this file.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1024
H = 1024
M = 14
CW = W - 2 * M
PAPER = (253, 251, 245)
INK = (17, 17, 17)
RED = (185, 28, 28)
DARKRED = (140, 20, 20)
MUTED = (90, 88, 82)
LINE = (190, 186, 175)
NAVY = (24, 38, 64)
SKY = (214, 232, 240)
SAND = (238, 228, 200)
LAND = (216, 212, 198)
SEA = (233, 240, 244)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(SERIF_I):
    SERIF_I = SERIF


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, lines, x, y, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon(d, kind, x0, y0, x1, y1):
    """Original coded illustration inside box (x0,y0,x1,y1)."""
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if kind == "globe":
        d.rectangle([x0, y0, x1, y1], fill=SKY)
        d.ellipse([cx - 30, cy - 26, cx + 6, cy + 26], outline=NAVY, width=2)
        d.ellipse([cx - 30, cy - 26, cx + 6, cy + 26], fill=(120, 180, 210))
        d.arc([cx - 30, cy - 26, cx + 6, cy + 26], 300, 60, fill=NAVY, width=1)
        d.line([cx - 30, cy, cx + 6, cy], fill=NAVY, width=1)
        d.ellipse([cx - 12, cy - 26, cx - 12, cy + 26], outline=NAVY, width=1)
        d.rectangle([cx + 16, cy - 22, cx + 24, cy + 22], outline=RED, width=2)
        d.rectangle([cx + 18, cy + 2, cx + 22, cy + 20], fill=RED)
        d.ellipse([cx + 14, cy + 16, cx + 26, cy + 28], fill=RED)
        d.line([cx + 20, cy - 30, cx + 20, cy - 22], fill=(200, 120, 40), width=3)
        d.ellipse([cx + 14, cy - 36, cx + 26, cy - 24], fill=(240, 180, 60))
    elif kind == "missiles":
        d.rectangle([x0, y0, x1, y1], fill=NAVY)
        for sx, sy in [(x0 + 20, y0 + 14), (x0 + 90, y0 + 8), (x0 + 160, y0 + 20),
                       (x0 + 240, y0 + 10), (x0 + 290, y0 + 22)]:
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        for bx in [x0 + 10, x0 + 55, x0 + 105, x0 + 150, x0 + 200, x0 + 250, x0 + 295]:
            bh = 18 + ((bx * 7) % 22)
            d.rectangle([bx, y1 - bh, bx + 22, y1], fill=(12, 20, 36))
        for i, (sx, sy, ex, ey) in enumerate([
                (x0 + 40, y0 + 70, x0 + 120, y0 + 18),
                (x0 + 130, y0 + 74, x0 + 210, y0 + 22),
                (x0 + 220, y0 + 72, x0 + 290, y0 + 16)]):
            d.line([sx, sy, ex, ey], fill=(255, 200, 90), width=2)
            d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 90, 60))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    elif kind == "quake":
        d.rectangle([x0, y0, x1, y1], fill=SAND)
        d.polygon([(cx - 70, y1 - 8), (cx - 40, y0 + 42), (cx - 10, y0 + 42),
                   (cx + 18, y1 - 8), (cx + 46, y1 - 8)], fill=(150, 110, 70))
        d.rectangle([cx - 62, y0 + 44, cx - 18, y1 - 8], fill=(200, 170, 120))
        d.rectangle([cx - 50, y0 + 56, cx - 30, y1 - 8], fill=(90, 60, 30))
        pts = [(x0 + 8, cy - 6), (x0 + 30, cy - 6), (x0 + 42, cy - 26),
               (x0 + 56, cy + 12), (x0 + 70, cy - 18), (x0 + 86, cy - 6),
               (x1 - 8, cy - 6)]
        d.line(pts, fill=RED, width=2, joint="curve")
        d.line([cx + 60, y0 + 30, cx + 66, y0 + 44, cx + 60, y0 + 58], fill=INK, width=2)
    elif kind == "bridge":
        d.rectangle([x0, y0, x1, y1], fill=SKY)
        d.line([x0 + 8, y1 - 10, x1 - 8, y1 - 10], fill=NAVY, width=3)
        for tx in (x0 + 40, x0 + 140):
            d.rectangle([tx, y0 + 6, tx + 8, y1 - 10], fill=NAVY)
        d.arc([x0 + 20, y0 - 6, x0 + 168, y0 + 66], 0, 180, fill=RED, width=2)
        d.line([x0 + 48, y0 + 6, x0 + 48, y1 - 10], fill=NAVY, width=1)
        d.line([x0 + 144, y0 + 6, x0 + 144, y1 - 10], fill=NAVY, width=1)
        d.line([x0 + 96, y0 + 22, x0 + 96, y1 - 10], fill=NAVY, width=1)
    elif kind == "drone":
        d.rectangle([x0, y0, x1, y1], fill=(226, 232, 238))
        d.ellipse([cx - 26, cy - 8, cx + 26, cy + 8], fill=(70, 80, 95))
        d.ellipse([cx - 8, cy - 4, cx + 8, cy + 4], fill=(200, 210, 220))
        for rx in (cx - 44, cx + 44):
            d.ellipse([rx - 14, cy - 16, rx + 14, cy - 8], outline=INK, width=2)
            d.line([rx, cy - 12, cx - 20 if rx < cx else cx + 20, cy - 4], fill=INK, width=2)
        d.line([cx, cy + 8, cx, cy + 20], fill=INK, width=2)
        d.ellipse([cx - 4, cy + 18, cx + 4, cy + 26], fill=RED)
    elif kind == "server":
        d.rectangle([x0, y0, x1, y1], fill=(30, 40, 56))
        for i, yy in enumerate((y0 + 6, y0 + 16, y0 + 26)):
            pass
        for i in range(3):
            yy = y0 + 5 + i * 11
            d.rectangle([cx - 34, yy, cx + 34, yy + 8], outline=(150, 170, 200), width=1)
            d.ellipse([cx - 30, yy + 2, cx - 24, yy + 6], fill=(90, 200, 120))
            d.line([cx - 18, yy + 4, cx + 28, yy + 4], fill=(120, 140, 170), width=1)
    elif kind == "flags":
        d.rectangle([x0, y0, x1, y1], fill=(240, 238, 228))
        d.line([cx - 34, y0 + 6, cx - 34, y1 - 6], fill=INK, width=2)
        d.line([cx + 30, y0 + 6, cx + 30, y1 - 6], fill=INK, width=2)
        d.rectangle([cx - 34, y0 + 6, cx - 6, y0 + 18], fill=RED)
        d.rectangle([cx + 30, y0 + 6, cx + 58, y0 + 18], fill=(220, 180, 40))
        d.text((cx - 30, y0 + 8), "*", font=font(SANS_B, 10), fill=(255, 255, 255))
    elif kind == "plane":
        d.rectangle([x0, y0, x1, y1], fill=SKY)
        d.ellipse([cx - 60, cy - 10, cx + 60, cy + 10], fill=(240, 240, 240))
        d.polygon([(cx + 30, cy - 8), (cx + 62, cy - 26), (cx + 70, cy - 8)], fill=(200, 60, 60))
        d.polygon([(cx - 10, cy + 6), (cx + 10, cy + 26), (cx + 26, cy + 6)], fill=(180, 180, 190))
        d.polygon([(cx - 55, cy - 6), (cx - 72, cy - 20), (cx - 60, cy - 6)], fill=(200, 60, 60))
        for wx in range(-40, 41, 16):
            d.ellipse([cx + wx, cy - 3, cx + wx + 5, cy + 2], fill=NAVY)
        d.line([x0 + 8, y1 - 8, x1 - 8, y1 - 8], fill=(120, 140, 120), width=2)
    elif kind == "nodes":
        d.rectangle([x0, y0, x1, y1], fill=(232, 238, 244))
        pts = [(cx - 50, cy - 10), (cx - 16, cy + 8), (cx + 18, cy - 12), (cx + 52, cy + 6)]
        d.line(pts, fill=(90, 120, 170), width=2)
        for (px, py) in pts:
            d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=NAVY)
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    elif kind == "coin":
        d.rectangle([x0, y0, x1, y1], fill=(250, 242, 214))
        d.ellipse([cx - 46, cy - 16, cx - 14, cy + 16], fill=(230, 180, 50))
        d.ellipse([cx - 46, cy - 16, cx - 14, cy + 16], outline=(160, 120, 20), width=2)
        d.text((cx - 38, cy - 12), "B", font=font(SANS_B, 20), fill=(120, 85, 10))
        d.line([(cx - 6, cy + 10), (cx + 12, cy - 2), (cx + 26, cy + 4),
                (cx + 44, cy - 12)], fill=RED, width=2)
        d.polygon([(cx + 44, cy - 12), (cx + 38, cy - 12), (cx + 44, cy - 6)], fill=RED)
    elif kind == "car":
        d.rectangle([x0, y0, x1, y1], fill=(228, 232, 236))
        d.polygon([(cx - 62, cy + 8), (cx - 52, cy - 8), (cx - 20, cy - 14),
                   (cx + 12, cy - 14), (cx + 34, cy - 6), (cx + 58, cy + 2),
                   (cx + 58, cy + 8)], fill=RED)
        d.rectangle([cx - 40, cy - 10, cx - 16, cy + 2], fill=SKY)
        d.rectangle([cx - 10, cy - 10, cx + 10, cy + 2], fill=SKY)
        for wx in (cx - 38, cx + 34):
            d.ellipse([wx - 9, cy - 1, wx + 9, cy + 15], fill=INK)
            d.ellipse([wx - 4, cy + 4, wx + 4, cy + 10], fill=(180, 180, 180))
        d.line([x0 + 6, y1 - 6, x1 - 6, y1 - 6], fill=INK, width=2)
    elif kind == "bat":
        d.rectangle([x0, y0, x1, y1], fill=(238, 240, 226))
        d.line([cx - 52, cy + 12, cx + 44, cy - 12], fill=(150, 110, 60), width=7)
        d.ellipse([cx + 44, cy - 18, cx + 58, cy - 4], fill=RED)
        d.line([cx - 20, cy + 2, cx - 8, cy + 14], fill=INK, width=1)
        d.ellipse([cx - 58, cy + 6, cx - 46, cy + 18], fill=(240, 240, 240))
    elif kind == "robot":
        d.rectangle([x0, y0, x1, y1], fill=(226, 232, 238))
        d.rectangle([cx - 26, cy - 12, cx + 26, cy + 16], fill=(120, 130, 145))
        d.rectangle([cx - 26, cy - 12, cx + 26, cy + 16], outline=INK, width=1)
        d.line([cx, cy - 12, cx, cy - 20], fill=INK, width=2)
        d.ellipse([cx - 3, cy - 24, cx + 3, cy - 18], fill=RED)
        d.ellipse([cx - 16, cy - 4, cx - 6, cy + 6], fill=(255, 255, 255))
        d.ellipse([cx + 6, cy - 4, cx + 16, cy + 6], fill=(255, 255, 255))
        d.ellipse([cx - 13, cy - 1, cx - 9, cy + 3], fill=INK)
        d.ellipse([cx + 9, cy - 1, cx + 13, cy + 3], fill=INK)
        d.line([cx - 10, cy + 11, cx + 10, cy + 11], fill=INK, width=1)


# ---------------------------------------------------------------- world map
LAND_POLYS = [
    [(-168, 66), (-150, 70), (-135, 69), (-120, 72), (-100, 73), (-85, 70),
     (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 39),
     (-76, 34), (-81, 26), (-84, 30), (-90, 21), (-95, 18), (-100, 16),
     (-105, 20), (-110, 24), (-115, 29), (-120, 34), (-125, 40), (-124, 48),
     (-130, 55), (-145, 60), (-160, 58), (-168, 66)],
    [(-58, 62), (-45, 64), (-32, 68), (-22, 70), (-25, 76), (-45, 80),
     (-58, 76), (-60, 70), (-58, 62)],
    [(-79, 9), (-72, 12), (-62, 9), (-52, 5), (-50, 0), (-44, -3), (-38, -8),
     (-35, -15), (-40, -22), (-48, -28), (-55, -34), (-62, -40), (-68, -50),
     (-70, -52), (-73, -40), (-72, -30), (-75, -20), (-80, -12), (-81, -4),
     (-79, 9)],
    [(-10, 35), (-6, 35), (0, 36), (10, 37), (19, 32), (30, 31), (33, 27),
     (38, 20), (43, 12), (51, 11), (48, 4), (41, -2), (40, -10), (36, -18),
     (33, -26), (28, -33), (20, -35), (16, -28), (12, -18), (13, -10),
     (9, -1), (9, 4), (0, 6), (-8, 4), (-13, 8), (-17, 15), (-16, 20),
     (-15, 28), (-10, 35)],
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (3, 53),
     (8, 57), (10, 59), (18, 62), (21, 65), (28, 71), (40, 68), (50, 69),
     (60, 69), (70, 72), (80, 73), (95, 76), (110, 74), (125, 73), (140, 72),
     (155, 70), (170, 67), (178, 65), (170, 60), (162, 56), (158, 52),
     (150, 59), (142, 54), (140, 45), (135, 42), (130, 38), (127, 35),
     (122, 31), (120, 28), (115, 23), (109, 18), (105, 9), (100, 7),
     (98, 10), (94, 16), (90, 22), (86, 20), (80, 13), (77, 8), (74, 14),
     (70, 21), (66, 25), (61, 25), (57, 26), (54, 27), (50, 29), (48, 30),
     (44, 29), (40, 32), (36, 36), (30, 36), (27, 37), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 42), (0, 39), (-2, 37), (-6, 36), (-9, 37)],
    [(114, -22), (118, -20), (122, -14), (126, -14), (131, -12), (136, -12),
     (142, -11), (142, -15), (146, -19), (150, -22), (153, -27), (153, -32),
     (150, -37), (146, -39), (141, -38), (137, -35), (132, -32), (128, -32),
     (124, -33), (119, -35), (115, -32), (114, -28), (114, -22)],
    [(-5, 50), (-3, 53), (-1, 54), (0, 53), (1, 51), (-2, 50), (-5, 50)],
    [(130, 31), (131, 33), (134, 34), (136, 35), (139, 37), (140, 39),
     (141, 41), (143, 43), (145, 44), (143, 42), (141, 39), (139, 35),
     (136, 33), (132, 33), (130, 31)],
    [(167, -45), (168, -43), (171, -42), (173, -40), (175, -38), (177, -38),
     (176, -40), (174, -41), (172, -43), (169, -46), (167, -45)],
]


def build(data, out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_kick = font(SANS_B, 13)
    f_kick_r = font(SANS, 10)
    f_mast = font(SERIF_B, 34)
    f_sub = font(SERIF_I, 13)
    f_num_v = font(SANS_B, 21)
    f_num_l = font(SANS_B, 8)
    f_chip = font(SANS_B, 10)
    f_banner = font(SANS_B, 10)
    f_lead_t = font(SERIF_B, 15)
    f_lead_s = font(SANS, 10)
    f_tag = font(SANS, 8)
    f_tag_b = font(SANS_B, 8)
    f_feat_t = font(SANS_B, 10)
    f_feat_s = font(SANS, 9)
    f_sec = font(SANS_B, 11)
    f_brief = font(SANS, 9)
    f_brief_b = font(SANS_B, 9)
    f_small = font(SANS, 9)
    f_tiny = font(SANS, 8)

    # ---- kicker
    d.text((M, 12), data["kicker"], font=f_kick, fill=RED)
    d.text((W - M, 14), data["kicker_right"], font=f_kick_r, fill=INK, anchor="ra")
    d.line([M, 34, W - M, 34], fill=INK, width=2)

    # ---- masthead + subhead
    d.text((W / 2, 40), data["masthead"], font=f_mast, fill=INK, anchor="ma")
    sub = wrap(data["subhead"], f_sub, 920)
    y = 82
    for ln in sub:
        d.text((W / 2, y), ln, font=f_sub, fill=(40, 38, 34), anchor="ma")
        y += 16
    d.line([M, 114, W - M, 114], fill=INK, width=1)

    # ---- six-number strip
    y0, hh = 120, 42
    bw = (CW - 5 * 4) / 6
    for i, num in enumerate(data["numbers"]):
        x = M + i * (bw + 4)
        d.rectangle([x, y0, x + bw, y0 + hh], outline=LINE, width=1)
        d.rectangle([x, y0, x + bw, y0 + 3], fill=RED)
        d.text((x + bw / 2, y0 + 7), num["value"], font=f_num_v, fill=INK, anchor="ma")
        d.text((x + bw / 2, y0 + 29), num["label"], font=f_num_l, fill=MUTED, anchor="ma")

    # ---- region chips
    y0 = 170
    chips = ["%s %d" % (name, n) for name, n in data["regions"]]
    widths = [f_chip.getlength(c) + 18 for c in chips]
    total = sum(widths) + 6 * (len(chips) - 1)
    x = (W - total) / 2
    for c, wd in zip(chips, widths):
        d.rounded_rectangle([x, y0, x + wd, y0 + 20], radius=10,
                            outline=RED, width=1, fill=(255, 240, 240))
        d.text((x + wd / 2, y0 + 4), c, font=f_chip, fill=DARKRED, anchor="ma")
        x += wd + 6

    # ---- leads
    y0, lh = 198, 214
    lw = (CW - 2 * 9) / 3
    for i, lead in enumerate(data["leads"]):
        x = M + i * (lw + 9)
        d.rectangle([x, y0, x + lw, y0 + lh], outline=LINE, width=1)
        d.rectangle([x, y0, x + lw, y0 + 20], fill=RED)
        d.text((x + 8, y0 + 4), lead["banner"], font=f_banner, fill=(255, 255, 255))
        icon(d, lead["icon"], x + 1, y0 + 21, x + lw - 1, y0 + 105)
        ty = y0 + 110
        for ln in wrap(lead["title"], f_lead_t, lw - 14):
            d.text((x + 7, ty), ln, font=f_lead_t, fill=INK)
            ty += 18
        for ln in wrap(lead["summary"], f_lead_s, lw - 14):
            d.text((x + 7, ty), ln, font=f_lead_s, fill=(40, 38, 34))
            ty += 13
        tag = "%s - %s - %s" % (lead["source"], lead["time"], lead["status"])
        d.text((x + 7, y0 + lh - 14), tag, font=f_tag_b, fill=RED)

    # ---- features (two rows of five)
    fw = (CW - 4 * 6) / 5
    fh = 98
    for row in range(2):
        y0 = 420 + row * (fh + 6)
        for col in range(5):
            feat = data["features"][row * 5 + col]
            x = M + col * (fw + 6)
            d.rectangle([x, y0, x + fw, y0 + fh], outline=LINE, width=1)
            icon(d, feat["icon"], x + 1, y0 + 1, x + fw - 1, y0 + 30)
            ty = y0 + 33
            for ln in wrap(feat["title"], f_feat_t, fw - 10):
                d.text((x + 5, ty), ln, font=f_feat_t, fill=INK)
                ty += 12
            for ln in wrap(feat["summary"], f_feat_s, fw - 10):
                d.text((x + 5, ty), ln, font=f_feat_s, fill=(40, 38, 34))
                ty += 11
            tag = "%s - %s - %s" % (feat["source"], feat["time"], feat["status"])
            d.text((x + 5, y0 + fh - 11), tag, font=f_tag, fill=RED)

    # ---- map
    d.text((M, 626), "WHERE IT HAPPENED  -  37 PLACES, NUMBERED",
           font=f_sec, fill=INK)
    d.text((W - M, 628), "Numbers match the list below",
           font=f_tiny, fill=MUTED, anchor="ra")
    mx0, my0, mx1, my1 = M, 644, W - M, 758
    d.rectangle([mx0, my0, mx1, my1], fill=SEA, outline=LINE, width=1)

    def proj(lon, lat):
        px = mx0 + (lon + 180) / 360.0 * (mx1 - mx0)
        py = my0 + (85 - lat) / 145.0 * (my1 - my0)
        return px, py

    for poly in LAND_POLYS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(170, 165, 150))
    pts_all = data["leads"] + data["features"] + data["briefs"]
    for p in pts_all:
        px, py = proj(p["x"], p["y"])
        px += p.get("dx", 0)
        py += p.get("dy", 0)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py - 4), str(p["n"]), font=f_tag_b, fill=(255, 255, 255),
               anchor="ma")

    # ---- briefs
    d.text((M, 766), "ALSO ON SATURDAY 21 NOVEMBER 2026  -  24 MORE STORIES",
           font=f_sec, fill=INK)
    colw = (CW - 16) / 2
    for idx, b in enumerate(data["briefs"]):
        col = idx // 12
        row = idx % 12
        x = M + col * (colw + 16)
        y = 784 + row * 13
        head = "%d  %s - " % (b["n"], b["place"].upper())
        d.text((x, y), head, font=f_brief_b, fill=RED)
        tx = x + f_brief_b.getlength(head)
        rest = "%s - %s" % (b["text"], b["source"])
        d.text((tx, y), rest, font=f_brief, fill=INK)

    # ---- date check + footer
    y0 = 944
    d.rectangle([M, y0, W - M, y0 + 34], fill=(255, 240, 240), outline=RED, width=1)
    dc = wrap(data["date_check"], f_small, CW - 16)
    yy = y0 + 3
    for ln in dc:
        d.text((M + 8, yy), ln, font=f_small, fill=DARKRED)
        yy += 12
    fy = y0 + 40
    d.text((M, fy), "Every story here happened, or was first reported, on Saturday "
           "21 November 2026. Officials' counts and claims are attributed. "
           "Sources named beside each story - original drawings.",
           font=f_tiny, fill=MUTED)
    d.text((M, fy + 11), data["counts_note"] + "  " + data["not_shown"],
           font=f_tiny, fill=MUTED)
    img.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    build(data, os.path.join(HERE, "entry.png"))
    print("wrote", os.path.join(HERE, "entry.png"))
