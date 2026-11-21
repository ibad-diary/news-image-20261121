#!/usr/bin/env python3
"""Render the one-page newspaper front page for Saturday 21 November 2026.

Build-time only: reads stories.json next to this file and writes entry.png
(1024x1024, <= 1 MiB) next to this file. All artwork is vector shapes drawn
in code; nothing is downloaded and nothing is random, so the output is
deterministic. The script refuses to finish if the footer would run past
the bottom edge instead of clipping silently.
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width

INK = (18, 18, 18)
GREY = (90, 90, 90)
RED = (178, 34, 34)
RULE = (160, 160, 160)
PAPER = (252, 250, 244)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text; shrink the font until it fits max_lines. Returns (lines, font)."""
    size = fnt.size
    while size > 9:
        f = font(fnt.path, size) if hasattr(fnt, "path") else fnt
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return lines, f
        size -= 1
    return wrap(draw, text, font(fnt.path, 9), max_w), font(fnt.path, 9)


def draw_art(draw, kind, x, y, w, h):
    """Original vector illustration for one art kind, inside box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    if kind == "chartdown":
        draw.rectangle([x, y, x + w, y + h], fill=(220, 233, 247))
        draw.line([x + 8, y + h - 10, x + w - 6, y + h - 10], fill=INK, width=2)
        draw.line([x + 8, y + 8, x + 8, y + h - 10], fill=INK, width=2)
        pts = [(x + 12, y + 14), (x + w // 3, y + h // 3),
               (x + 2 * w // 3, y + h // 2), (x + w - 10, y + h - 16)]
        draw.line(pts, fill=RED, width=4)
        draw.polygon([(x + w - 10, y + h - 16), (x + w - 22, y + h - 18),
                      (x + w - 14, y + h - 6)], fill=RED)
        for i, bh in enumerate((18, 30, 12)):
            bx = x + 16 + i * 18
            draw.rectangle([bx, y + h - 12 - bh, bx + 10, y + h - 12],
                           fill=(120, 140, 170))
    elif kind == "rockets":
        draw.rectangle([x, y, x + w, y + h], fill=(29, 43, 74))
        for sx, sy in ((10, 10), (w - 14, 16), (w // 2, 8), (14, h - 12),
                       (w - 20, h - 20), (w // 3, h - 8)):
            draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                         fill=(255, 255, 255))
        bx0, bx1 = cx - 9, cx + 9
        draw.polygon([(cx, y + 8), (bx1, y + 30), (bx1, y + h - 34),
                      (bx0, y + h - 34), (bx0, y + 30)], fill=(235, 235, 235))
        draw.polygon([(cx, y + 8), (bx1, y + 30), (bx0, y + 30)], fill=RED)
        draw.ellipse([cx - 4, y + 34, cx + 4, y + 42], fill=(70, 130, 200))
        draw.polygon([(bx0, y + h - 40), (bx0 - 8, y + h - 26), (bx0, y + h - 26)],
                     fill=(200, 60, 60))
        draw.polygon([(bx1, y + h - 40), (bx1 + 8, y + h - 26), (bx1, y + h - 26)],
                     fill=(200, 60, 60))
        draw.polygon([(cx - 6, y + h - 32), (cx + 6, y + h - 32),
                      (cx, y + h - 8)], fill=(255, 160, 40))
    elif kind == "cop":
        draw.rectangle([x, y, x + w, y + h], fill=(217, 239, 230))
        r = min(w, h) // 2 - 8
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 139, 87))
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=(255, 255, 255), width=2)
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
        draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                     outline=(255, 255, 255), width=2)
        draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
        draw.line([x + w - 26, y + h - 8, x + w - 26, y + 12], fill=INK, width=2)
        draw.polygon([(x + w - 26, y + 12), (x + w - 6, y + 17),
                      (x + w - 26, y + 22)], fill=RED)
    elif kind == "bars":
        draw.rectangle([x, y, x + w, y + h], fill=(236, 236, 236))
        base = y + h - 10
        heights = (0.35, 0.55, 0.45, 0.75, 0.6)
        bw = (w - 24) // 5
        for i, frac in enumerate(heights):
            bx = x + 10 + i * bw
            bh = int((h - 22) * frac)
            col = RED if i == 3 else (70, 110, 160)
            draw.rectangle([bx, base - bh, bx + bw - 5, base], fill=col)
        draw.line([x + 6, base, x + w - 6, base], fill=INK, width=2)
    elif kind == "coin":
        draw.rectangle([x, y, x + w, y + h], fill=(247, 232, 195))
        r = min(w, h) // 2 - 8
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(212, 160, 40),
                     outline=(150, 105, 20), width=3)
        bf = font(SANS_B, r)
        draw.text((cx, cy), "B", font=bf, fill=(90, 60, 10), anchor="mm")
        draw.arc([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], 200, 320,
                 fill=(255, 240, 190), width=3)
    elif kind == "waves":
        draw.rectangle([x, y, x + w, y + h], fill=(214, 236, 245))
        for k, col in enumerate(((40, 110, 170), (80, 160, 210), (140, 190, 220))):
            yy = y + 16 + k * (h // 4)
            pts = []
            for t in range(0, w - 4, 6):
                import math
                pts.append((x + 4 + t, yy + int(7 * math.sin(t / 9.0 + k))))
            draw.line(pts, fill=col, width=3)
        draw.ellipse([x + w - 26, y + 8, x + w - 10, y + 24], fill=(255, 210, 90))
    elif kind == "flags":
        draw.rectangle([x, y, x + w, y + h], fill=(242, 242, 242))
        draw.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=INK, width=2)
        for px, col in ((x + w // 4, RED), (x + 3 * w // 4, (40, 90, 170))):
            draw.line([px, y + h - 8, px, y + 10], fill=INK, width=2)
            draw.polygon([(px, y + 10), (px + 26, y + 17), (px, y + 24)], fill=col)
        draw.ellipse([cx - 3, y + h - 16, cx + 3, y + h - 10], fill=(46, 139, 87))
    elif kind == "cyclone":
        draw.rectangle([x, y, x + w, y + h], fill=(227, 232, 240))
        r = min(w, h) // 2 - 6
        for k in range(4):
            rr = r - k * (r // 4)
            draw.arc([cx - rr, cy - rr, cx + rr, cy + rr],
                     30 + k * 55, 300 + k * 55, fill=(60, 90, 140), width=3)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        for dx in (-14, 0, 14):
            draw.line([cx + dx, y + h - 16, cx + dx - 3, y + h - 8],
                      fill=(60, 90, 140), width=2)
    else:
        draw.rectangle([x, y, x + w, y + h], fill=(230, 230, 230))


def main():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    y = 12

    # --- top line -------------------------------------------------------
    f_top = font(SANS_B, 11)
    draw.text((MARGIN, y), data["topline_left"], font=f_top, fill=INK)
    rw = draw.textlength(data["topline_right"], font=f_top)
    draw.text((W - MARGIN - rw, y), data["topline_right"], font=f_top, fill=INK)
    y += 18
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 8

    # --- masthead + red date badge --------------------------------------
    f_badge = font(SANS_B, 13)
    badge_text = "SAT · 21 NOV"
    bw = int(draw.textlength(badge_text, font=f_badge)) + 20
    bh = 24
    size = 38
    while size > 26:
        f_mast = font(SERIF_B, size)
        mw = draw.textlength(data["masthead"], font=f_mast)
        if (W - mw) / 2 + mw + 16 + bw <= W - MARGIN:
            break
        size -= 2
    f_mast = font(SERIF_B, size)
    mw = draw.textlength(data["masthead"], font=f_mast)
    mx = (W - mw) / 2
    draw.text((mx, y), data["masthead"], font=f_mast, fill=INK)
    bx = W - MARGIN - bw
    by = y + (size - bh) // 2 + 4
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=11, fill=RED)
    draw.text((bx + bw / 2, by + bh / 2), badge_text, font=f_badge,
              fill=(255, 255, 255), anchor="mm")
    y += size + 8
    draw.line([MARGIN, y, W - MARGIN, y], fill=RED, width=3)
    y += 8

    # --- kicker ----------------------------------------------------------
    f_kick = font(SERIF_I, 15)
    kw = draw.textlength(data["kicker"], font=f_kick)
    draw.text(((W - kw) / 2, y), data["kicker"], font=f_kick, fill=INK)
    y += 20

    # --- numbers strip ---------------------------------------------------
    nums = data["numbers"]
    col_w = CW / len(nums)
    f_big = font(SANS_B, 20)
    f_cap = font(SANS, 9)
    top_y = y
    for i, item in enumerate(nums):
        cx0 = MARGIN + i * col_w
        bw_big = draw.textlength(item["big"], font=f_big)
        draw.text((cx0 + (col_w - bw_big) / 2, y), item["big"],
                  font=f_big, fill=RED)
        lines = wrap(draw, item["cap"], f_cap, col_w - 12)
        ly = y + 26
        for ln in lines[:2]:
            lw = draw.textlength(ln, font=f_cap)
            draw.text((cx0 + (col_w - lw) / 2, ly), ln, font=f_cap, fill=GREY)
            ly += 12
        if i:
            draw.line([cx0, y + 2, cx0, y + 44], fill=RULE, width=1)
    y = top_y + 50
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 10

    # --- 3 illustrated leads ---------------------------------------------
    gap = 12
    lead_w = (CW - 2 * gap) // 3
    art_h = 84
    lead_top = y
    f_place = font(SANS_B, 9)
    f_head = font(SERIF_B, 17)
    f_sum = font(SANS, 11)
    for i, lead in enumerate(data["leads"]):
        lx = MARGIN + i * (lead_w + gap)
        draw_art(draw, lead["art"], lx, y, lead_w, art_h)
        ty = y + art_h + 6
        draw.text((lx, ty), lead["place"], font=f_place, fill=RED)
        ty += 13
        lines, hf = fit_lines(draw, lead["headline"], f_head, lead_w, 3)
        for ln in lines:
            draw.text((lx, ty), ln, font=hf, fill=INK)
            ty += hf.size + 2
        ty += 2
        for ln in wrap(draw, lead["summary"], f_sum, lead_w):
            draw.text((lx, ty), ln, font=f_sum, fill=(40, 40, 40))
            ty += 14
        if i < 2:
            draw.line([lx + lead_w + 6, y, lx + lead_w + 6, ty],
                      fill=RULE, width=1)
    y = lead_top + art_h + 6 + 13 + (3 * 19) + 2 + (4 * 14) + 8
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)
    y += 10

    # --- 10 illustrated features, grid 2 x 5 ----------------------------
    feat_w = (CW - gap) // 2
    feat_h = 66
    f_fplace = font(SANS_B, 8)
    f_fhead = font(SERIF_B, 13)
    f_fsum = font(SANS, 10)
    thumb_w = 86
    for row in range(5):
        for col in range(2):
            feat = data["features"][row * 2 + col]
            fx = MARGIN + col * (feat_w + gap)
            fy = y + row * (feat_h + 4)
            draw_art(draw, feat["art"], fx, fy, thumb_w, feat_h)
            tx = fx + thumb_w + 8
            tw = feat_w - thumb_w - 8
            draw.text((tx, fy), feat["place"], font=f_fplace, fill=RED)
            lines, hf = fit_lines(draw, feat["headline"], f_fhead, tw, 2)
            ty = fy + 11
            for ln in lines:
                draw.text((tx, ty), ln, font=hf, fill=INK)
                ty += hf.size + 1
            for ln in wrap(draw, feat["summary"], f_fsum, tw)[:2]:
                draw.text((tx, ty), ln, font=f_fsum, fill=(40, 40, 40))
                ty += 13
    y += 5 * feat_h + 4 * 4 + 8
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)
    y += 8

    # --- 24 one-line briefs, 2 columns -----------------------------------
    f_brief_h = font(SANS_B, 11)
    draw.text((MARGIN, y), "IN BRIEF", font=f_brief_h, fill=INK)
    y += 17
    f_bplace = font(SANS_B, 10)
    f_btext = font(SANS, 10)
    f_bsrc = font(SANS_B, 9)
    brief_col_w = (CW - gap) // 2
    row_h = 13
    for i, brief in enumerate(data["briefs"]):
        col = i // 12
        row = i % 12
        bx0 = MARGIN + col * (brief_col_w + gap)
        by0 = y + row * row_h
        ptxt = brief["place"].upper() + " — "
        pw = draw.textlength(ptxt, font=f_bplace)
        draw.text((bx0, by0), ptxt, font=f_bplace, fill=RED)
        tw = draw.textlength(brief["text"], font=f_btext)
        draw.text((bx0 + pw, by0), brief["text"], font=f_btext, fill=INK)
        stxt = " (" + brief["source"] + ")"
        draw.text((bx0 + pw + tw, by0), stxt, font=f_bsrc, fill=GREY)
    y += 12 * row_h + 8

    # --- footer: date check + sources ------------------------------------
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 6
    f_dc = font(SANS_B, 10)
    for ln in wrap(draw, data["date_check"], f_dc, CW):
        draw.text((MARGIN, y), ln, font=f_dc, fill=INK)
        y += 13
    y += 2
    f_src = font(SERIF_I, 9)
    for ln in wrap(draw, data["sources"], f_src, CW):
        draw.text((MARGIN, y), ln, font=f_src, fill=GREY)
        y += 12
    y += 6

    # --- overflow guard: refuse to finish past the bottom edge -----------
    if y > H - 6:
        sys.exit("OVERFLOW: footer ends at y=%d, past bottom edge %d" % (y, H - 6))

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote %s (%dx%d, %d bytes, footer ends y=%d)"
          % (out, W, H, os.path.getsize(out), y))


if __name__ == "__main__":
    main()
