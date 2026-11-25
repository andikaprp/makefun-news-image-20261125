#!/usr/bin/env python3
"""Broadsheet front-page renderer for news-image-20261125 (Wednesday 25 November 2026).

Follows DESIGN-GEMINI.md zone-by-zone using locked content from data.json (verbatim from STORIES-FINAL.md).
Produces 1024x1024 PNG at gemini-candidate/entry.png.
"""
import json
import os
import sys
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

from panels import PANEL_FUNCS
from worldmap import render_world_map

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/noto/"

# Master Palette (DESIGN-GEMINI.md §2A)
PAPER = "#F8F4EC"
HEADER_BAND_BG = "#FAF7F0"
INK_PRIMARY = "#111111"
INK_HEADLINE = "#0E0E0E"
INK_BODY = "#1F1D1A"
INK_MUTED = "#4E4942"
ACCENT_CRIMSON = "#B3261E"
RULE_HAIRLINE = "#BDB3A2"
RULE_SUBTLE = "#D4CBB9"

# 7-Color Region Threading Palette + Global
REGION_COLORS = {
    "europe":        {"name": "Europe",       "fill": "#1F5E9C", "ink": "#1A4E82"},
    "middle_east":   {"name": "Middle East",  "fill": "#7E3B8F", "ink": "#682E78"},
    "asia":          {"name": "Asia",         "fill": "#177A6B", "ink": "#126357"},
    "americas":      {"name": "N. America",   "fill": "#B83227", "ink": "#99261D"},
    "latin_america": {"name": "Latin Am.",    "fill": "#C96818", "ink": "#A6520E"},
    "africa":        {"name": "Africa",       "fill": "#7C6E1E", "ink": "#635714"},
    "oceania":       {"name": "Oceania",      "fill": "#2E7D32", "ink": "#236326"},
    "global":        {"name": "Global",       "fill": "#3B4252", "ink": "#2E3440"},
}

# Confidence Badge Pills (DESIGN-GEMINI.md §2A)
CONF_STYLES = {
    "CONFIRMED": {"border": "#1F6E43", "fill": "#EAF5EE", "text": "#165734"},
    "OFFICIAL":  {"border": "#9A6B12", "fill": "#FCF5E3", "text": "#7A530B"},
    "REPORTED":  {"border": "#546170", "fill": "#EFF2F5", "text": "#3D4754"},
}

_FONT_CACHE = {}


def F(name, size):
    key = (name, round(size, 2))
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _FONT_CACHE[key]


def wrap_text(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if font.getlength(cand) <= max_w:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered_text(draw, cx, cy, text, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), text, fill=fill, font=font)


def draw_badge_circle(draw, cx, cy, diam, num, fill_col, font_1d, font_2d):
    r = diam / 2.0
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill_col)
    txt = str(num)
    fnt = font_1d if len(txt) == 1 else font_2d
    draw_centered_text(draw, cx, cy, txt, fnt, "#FFFFFF")


def draw_conf_pill(draw, right_x, top_y, conf_key, label=None, font_sz=7.5, pad_x=4, h=12):
    st = CONF_STYLES[conf_key]
    txt = label or conf_key
    fnt = F("NotoSans-CondensedBold.ttf", font_sz)
    bb = draw.textbbox((0, 0), txt, font=fnt)
    tw = bb[2] - bb[0]
    w = tw + pad_x * 2
    x0 = right_x - w
    draw.rounded_rectangle([x0, top_y, right_x, top_y + h], radius=2, fill=st["fill"], outline=st["border"], width=1)
    draw_centered_text(draw, (x0 + right_x) / 2, top_y + h / 2, txt, fnt, st["text"])
    return x0


def draw_rich_lines(draw, x, y, segments, max_w, lh):
    """Wrap and draw mixed-font/color text segments [(text, font, color), ...].
    Returns (visual_bottom_y, line_count, max_line_w).
    """
    # Tokenize into (word, font, color)
    tokens = []
    for seg_text, seg_font, seg_color in segments:
        for word in seg_text.split():
            tokens.append((word, seg_font, seg_color))

    lines = []
    cur_line = []
    cur_w = 0.0
    for word, fnt, col in tokens:
        sp_w = fnt.getlength(" ") if cur_line else 0.0
        w_len = fnt.getlength(word)
        if cur_line and (cur_w + sp_w + w_len) > max_w:
            lines.append((cur_line, cur_w))
            cur_line = [(word, fnt, col)]
            cur_w = w_len
        else:
            cur_line.append((word, fnt, col))
            cur_w += sp_w + w_len
    if cur_line:
        lines.append((cur_line, cur_w))

    cy = y
    max_line_w = 0.0
    vis_bottom = y
    for line, lw in lines:
        if lw > max_line_w:
            max_line_w = lw
        cx = x
        for i, (word, fnt, col) in enumerate(line):
            if i > 0:
                cx += fnt.getlength(" ")
            draw.text((cx, cy), word, fill=col, font=fnt)
            bb = fnt.getbbox(word)
            if bb:
                vis_bottom = max(vis_bottom, cy + bb[3])
            cx += fnt.getlength(word)
        cy += lh
    return vis_bottom, len(lines), max_line_w


def split_source_tail(sub_text):
    """Split 'body text — Source' so the source attribution can be bolded without altering a single char."""
    idx = sub_text.rfind(" — ")
    if idx != -1:
        return sub_text[:idx + 3], sub_text[idx + 3:]
    return sub_text, ""


def render_page(data_path, out_path):
    with open(data_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    W, H = 1024, 1024
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    overflows = []

    # =========================================================================
    # ZONE 1: MASTHEAD STRAP (y = 6..20)
    # =========================================================================
    f_strap_l = F("NotoSans-Bold.ttf", 10.2)
    f_strap_r = F("NotoSans-SemiBold.ttf", 10.0)
    draw.text((16, 7), data["strap_left"], fill=ACCENT_CRIMSON, font=f_strap_l)
    rw = f_strap_r.getlength(data["strap_right"])
    draw.text((1008 - rw, 7), data["strap_right"], fill="#262422", font=f_strap_r)

    # =========================================================================
    # ZONE 2: GIANT SERIF DATE + DOUBLE RULE (y = 20..84)
    # =========================================================================
    date_txt = data["date_display"]
    # Auto-fit bold serif between 54 and 66px so width lands in 860..920px
    date_sz = 64
    f_date = F("NotoSerif-ExtraBold.ttf", date_sz)
    while f_date.getlength(date_txt) > 916 and date_sz > 54:
        date_sz -= 1
        f_date = F("NotoSerif-ExtraBold.ttf", date_sz)
    bb_d = draw.textbbox((0, 0), date_txt, font=f_date)
    dw, dh = bb_d[2] - bb_d[0], bb_d[3] - bb_d[1]
    draw.text(((W - dw) / 2 - bb_d[0], 22 + (55 - dh) / 2 - bb_d[1]), date_txt, fill=INK_PRIMARY, font=f_date)
    # Double rule y = 80..84
    draw.rectangle([16, 80, 1008, 81], fill=INK_PRIMARY)
    draw.line([(16, 83), (1008, 83)], fill=INK_PRIMARY, width=1)

    # =========================================================================
    # ZONE 3: UTC TIMELINE STRIP (y = 84..122)
    # =========================================================================
    draw.rectangle([16, 84, 1008, 121], fill=HEADER_BAND_BG)
    # Left crimson pill
    draw.rounded_rectangle([16, 88, 78, 117], radius=2, fill=ACCENT_CRIMSON)
    draw_centered_text(draw, 47, 97, "THE DAY", F("NotoSans-Bold.ttf", 8.8), "#FFFFFF")
    draw_centered_text(draw, 47, 108, "IN UTC", F("NotoSans-Bold.ttf", 8.8), "#FFFFFF")

    f_utc_t = F("NotoSans-Bold.ttf", 11.2)
    f_utc_l = F("NotoSans-SemiCondensed.ttf", 8.6)
    col_w = 132
    for idx, item in enumerate(data["utc_timeline"]):
        x0 = 84 + idx * col_w
        cx = x0 + col_w / 2
        if idx > 0:
            draw.line([(x0, 88), (x0, 117)], fill="#D8D0C2", width=1)
        draw_centered_text(draw, cx, 92, item["time"], f_utc_t, ACCENT_CRIMSON)
        lines = wrap_text(item["label"], f_utc_l, col_w - 8)
        if len(lines) == 1:
            draw_centered_text(draw, cx, 108, lines[0], f_utc_l, "#1E1D1B")
        else:
            draw_centered_text(draw, cx, 104, lines[0], f_utc_l, "#1E1D1B")
            draw_centered_text(draw, cx, 113.5, lines[1], f_utc_l, "#1E1D1B")
            if len(lines) > 2:
                overflows.append(f"UTC {item['time']}: {len(lines)} lines")
    draw.line([(16, 121), (1008, 121)], fill=RULE_HAIRLINE, width=1)

    # =========================================================================
    # ZONE 4: STAT BAND — THE DAY IN NUMBERS (y = 122..163)
    # =========================================================================
    draw.rectangle([16, 122, 1008, 162], fill=HEADER_BAND_BG)
    draw.rounded_rectangle([16, 126, 78, 158], radius=2, fill=INK_PRIMARY)
    draw_centered_text(draw, 47, 134.5, "THE DAY", F("NotoSans-CondensedBold.ttf", 8.2), "#FFFFFF")
    draw_centered_text(draw, 47, 143, "IN", F("NotoSans-CondensedBold.ttf", 7.6), "#D8D0C2")
    draw_centered_text(draw, 47, 151.5, "NUMBERS", F("NotoSans-CondensedBold.ttf", 8.2), "#FFFFFF")

    f_stat_n = F("NotoSerif-ExtraBold.ttf", 16.5)
    f_stat_c = F("NotoSans-SemiCondensed.ttf", 8.2)
    stat_w = 154
    for idx, st in enumerate(data["stat_band"]):
        x0 = 84 + idx * stat_w
        cx = x0 + stat_w / 2
        if idx > 0:
            draw.line([(x0, 126), (x0, 158)], fill="#D8D0C2", width=1)
        draw_centered_text(draw, cx, 133.5, st["figure"], f_stat_n, INK_PRIMARY)
        lines = wrap_text(st["caption"], f_stat_c, stat_w - 8)
        if len(lines) == 1:
            draw_centered_text(draw, cx, 150, lines[0], f_stat_c, "#3A3834")
        else:
            draw_centered_text(draw, cx, 147, lines[0], f_stat_c, "#3A3834")
            draw_centered_text(draw, cx, 156, lines[1], f_stat_c, "#3A3834")
            if len(lines) > 2:
                overflows.append(f"Stat {st['figure']}: {len(lines)} lines")
    draw.line([(16, 162), (1008, 162)], fill=RULE_HAIRLINE, width=1)

    # =========================================================================
    # ZONE 5: LEAD ROW — CARDS 1..3 (y = 165..383) — NO OUTER CARD BOXES!
    # =========================================================================
    lead_w, lead_panel_h = 322, 124
    lead_xs = [16, 351, 686]
    f_lead_k = F("NotoSans-Bold.ttf", 10.2)
    f_lead_h = F("NotoSerif-ExtraBold.ttf", 19.5)
    f_lead_s = F("NotoSans-SemiCondensed.ttf", 11.5)
    f_lead_sb = F("NotoSans-SemiCondensedSemiBold.ttf", 11.5)
    f_b1 = F("NotoSans-Bold.ttf", 9.2)
    f_b2 = F("NotoSans-CondensedBold.ttf", 8.6)

    for idx, card in enumerate(data["leads"]):
        x0 = lead_xs[idx]
        reg = REGION_COLORS[card["region"]]
        # Panel (322 x 124 -> 1.91x height / 3.27x area over 188 x 65 small panels)
        p_img = PANEL_FUNCS[card["num"]](lead_w, lead_panel_h)
        img.paste(p_img, (x0, 165))

        # Kicker row y = 291..306
        ky_lead = 165 + lead_panel_h + 2
        draw_badge_circle(draw, x0 + 7.5, ky_lead + 8.0, 15, card["num"], reg["fill"], f_b1, f_b2)
        draw.text((x0 + 19, ky_lead + 1.5), card["kicker"], fill=reg["ink"], font=f_lead_k)
        draw_conf_pill(draw, x0 + lead_w, ky_lead + 1.5, card["confidence"], label=card["pill_text"], font_sz=7.6, pad_x=4.5, h=13)

        # Headline (19.5px ExtraBold Serif, strictly 2 lines; top bearing ~7px)
        hy = ky_lead + 13.5
        h_lines = wrap_text(card["headline"], f_lead_h, lead_w)
        if len(h_lines) != 2:
            overflows.append(f"Lead {card['num']} headline lines={len(h_lines)} != 2")
        hlh = 20.0
        h_vis_bottom = hy
        for line in h_lines:
            if f_lead_h.getlength(line) > lead_w:
                overflows.append(f"Lead {card['num']} headline width > {lead_w}")
            draw.text((x0, hy), line, fill=INK_HEADLINE, font=f_lead_h)
            bb = f_lead_h.getbbox(line)
            if bb:
                h_vis_bottom = max(h_vis_bottom, hy + bb[3])
            hy += hlh

        # Sub-line (11.5px SemiCondensed Sans, <= 2 lines, bold named source)
        body_part, src_part = split_source_tail(card["sub"])
        segs = [(body_part, f_lead_s, INK_BODY)]
        if src_part:
            segs.append((src_part, f_lead_sb, INK_PRIMARY))
        end_y, s_lines, lw = draw_rich_lines(draw, x0, h_vis_bottom + 2.5, segs, lead_w, 13.0)
        if s_lines > 2 or end_y > 382.5 or lw > lead_w:
            overflows.append(f"Lead {card['num']}: s_lines={s_lines}, end_y={end_y:.1f} > 382.5, lw={lw:.1f}")

    # Rule between Row 1 and Row 2
    draw.line([(16, 385), (1008, 385)], fill=RULE_HAIRLINE, width=1)

    # =========================================================================
    # ZONE 6a & 6b: SMALL CARDS 4..8 (y=390..534) & 9..13 (y=541..685)
    # =========================================================================
    sm_w, sm_panel_h = 188, 65
    sm_xs = [16, 217, 418, 619, 820]
    f_sm_k = F("NotoSans-CondensedBold.ttf", 9.2)
    f_sm_h = F("NotoSerif-CondensedExtraBold.ttf", 14.2)
    f_sm_s = F("NotoSans-CondensedMedium.ttf", 9.6)
    f_sm_sb = F("NotoSans-CondensedBold.ttf", 9.6)
    f_sm_xs = F("NotoSans-ExtraCondensedMedium.ttf", 9.6)
    f_sm_xsb = F("NotoSans-ExtraCondensedBold.ttf", 9.6)
    f_sb1 = F("NotoSans-Bold.ttf", 8.2)
    f_sb2 = F("NotoSans-CondensedBold.ttf", 7.8)

    for idx, card in enumerate(data["small_cards"]):
        row = idx // 5
        col = idx % 5
        x0 = sm_xs[col]
        y_top = 390 if row == 0 else 541
        y_limit = 534 if row == 0 else 685
        reg = REGION_COLORS[card["region"]]

        # Panel (188 x 65) + confidence pill tucked 3px inside top-right corner
        p_img = PANEL_FUNCS[card["num"]](sm_w, sm_panel_h)
        img.paste(p_img, (x0, y_top))
        draw_conf_pill(draw, x0 + sm_w - 3, y_top + 3, card["confidence"], label=card["confidence"], font_sz=6.8, pad_x=3.5, h=11)

        # Kicker row
        ky = y_top + sm_panel_h + 2
        draw_badge_circle(draw, x0 + 6.5, ky + 6.5, 13, card["num"], reg["fill"], f_sb1, f_sb2)
        draw.text((x0 + 16, ky + 1.0), card["kicker"], fill=reg["ink"], font=f_sm_k)

        # Headline (14.5px CondensedExtraBold Serif, strictly 2 lines; top bearing ~6px)
        hy = ky + 11.2
        h_lines = wrap_text(card["headline"], f_sm_h, sm_w)
        if len(h_lines) != 2:
            overflows.append(f"Card {card['num']} headline lines={len(h_lines)} != 2")
        hlh = 14.8
        h_vis_bottom = hy
        for line in h_lines:
            if f_sm_h.getlength(line) > sm_w:
                overflows.append(f"Card {card['num']} headline width > {sm_w}")
            draw.text((x0, hy), line, fill=INK_HEADLINE, font=f_sm_h)
            bb = f_sm_h.getbbox(line)
            if bb:
                h_vis_bottom = max(h_vis_bottom, hy + bb[3])
            hy += hlh

        # Sub-line (9.6px CondensedMedium + Bold source, <= 2 lines; fallback to ExtraCondensed 9.6px if needed)
        body_part, src_part = split_source_tail(card["sub"])
        # Measure wrap count with standard CondensedMedium first
        def _count_rich_lines(fb, fs):
            toks = [(w, fb) for w in body_part.split()] + ([(w, fs) for w in src_part.split()] if src_part else [])
            nlines, cw = 1, 0.0
            for w, fnt in toks:
                sp = fnt.getlength(" ") if cw > 0 else 0.0
                wl = fnt.getlength(w)
                if cw > 0 and cw + sp + wl > sm_w:
                    nlines += 1
                    cw = wl
                else:
                    cw += sp + wl
            return nlines

        use_f_s, use_f_sb = (f_sm_s, f_sm_sb) if _count_rich_lines(f_sm_s, f_sm_sb) <= 2 else (f_sm_xs, f_sm_xsb)
        segs = [(body_part, use_f_s, INK_BODY)]
        if src_part:
            segs.append((src_part, use_f_sb, INK_PRIMARY))
        end_y, s_lines, lw = draw_rich_lines(draw, x0, h_vis_bottom + 2.2, segs, sm_w, 11.0)
        if s_lines > 2 or end_y > y_limit or lw > sm_w:
            overflows.append(f"Card {card['num']}: s_lines={s_lines}, end_y={end_y:.1f} > {y_limit}, lw={lw:.1f}")

    # Hairline between Row 2 and Row 3
    draw.line([(16, 537), (1008, 537)], fill=RULE_SUBTLE, width=1)
    # Major 2px section rule below Row 3
    draw.rectangle([16, 688, 1008, 689], fill=INK_PRIMARY)

    # =========================================================================
    # ZONE 7a: WORLD MAP + REGION TALLY LEGEND (x = 16..270, y = 693..946)
    # =========================================================================
    f_sec = F("NotoSans-Bold.ttf", 9.8)
    draw.text((16, 694), "WHERE IT HAPPENED", fill=ACCENT_CRIMSON, font=f_sec)

    all_cards = data["leads"] + data["small_cards"]
    map_img = render_world_map(254, 174, all_cards, REGION_COLORS)
    img.paste(map_img, (16, 709))

    # Count all 39 stories by region
    reg_counts = Counter()
    for c in all_cards:
        reg_counts[c["region"]] += 1
    for b in data["briefs"]:
        reg_counts[b["region"]] += 1

    legend_order = ["europe", "asia", "middle_east", "americas", "africa", "oceania", "latin_america", "global"]
    f_leg = F("NotoSans-SemiCondensed.ttf", 8.6)
    f_leg_b = F("NotoSans-SemiCondensedBold.ttf", 8.6)
    # 3-column legend grid in y=888..931
    for i, rk in enumerate(legend_order):
        col = i % 3
        row = i // 3
        lx = 16 + col * 86
        ly = 889 + row * 14
        rc = REGION_COLORS[rk]
        draw.ellipse([lx, ly + 2.5, lx + 7, ly + 9.5], fill=rc["fill"])
        draw.text((lx + 10, ly), f"{rc['name']} ", fill=INK_BODY, font=f_leg)
        nw = f_leg.getlength(f"{rc['name']} ")
        draw.text((lx + 10 + nw, ly), str(reg_counts[rk]), fill=INK_PRIMARY, font=f_leg_b)

    f_micro = F("NotoSans-Condensed.ttf", 7.8)
    draw.text((16, 934), f"Pins 1–13 match illustrated cards above; all {sum(reg_counts.values())} stories tallied.", fill=INK_MUTED, font=f_micro)

    # =========================================================================
    # ZONE 7b: 26 NUMBERED BRIEFS (2 Columns: x = 284..638 and 654..1008)
    # =========================================================================
    draw.text((284, 694), "ALSO ON WEDNESDAY 25 NOVEMBER", fill=ACCENT_CRIMSON, font=f_sec)
    rcap = "26 MORE VERIFIED STORIES · NUMBERED BY REGION"
    f_rcap = F("NotoSans-SemiCondensed.ttf", 8.2)
    draw.text((1008 - f_rcap.getlength(rcap), 695.5), rcap, fill=INK_MUTED, font=f_rcap)

    f_br_p = F("NotoSans-CondensedBold.ttf", 11.2)
    f_br_t = F("NotoSans-CondensedMedium.ttf", 11.2)
    f_br_sb = F("NotoSans-CondensedBold.ttf", 11.2)
    f_br_n = F("NotoSans-CondensedBold.ttf", 7.8)

    pitch = 18.2
    max_brief_w = 0.0
    for idx, b in enumerate(data["briefs"]):
        col = 0 if idx < 13 else 1
        row = idx % 13
        bx = 284 if col == 0 else 654
        by = 709 + row * pitch
        reg = REGION_COLORS[b["region"]]

        # Region-colored numbered circle centered vertically with 1-line 11.2px text
        draw_badge_circle(draw, bx + 6.75, by + 6.7, 13.5, b["num"], reg["fill"], f_br_n, f_br_n)

        # Split source tail for subtle crispness (preserving every character)
        body_part, src_part = split_source_tail(b["text"])
        segs = [(b["place"], f_br_p, reg["ink"]), (body_part, f_br_t, "#1C1B19")]
        if src_part:
            segs.append((src_part, f_br_sb, "#2B2926"))
        end_y, nlines, lw = draw_rich_lines(draw, bx + 16, by - 1.5, segs, 338, 13.0)
        max_brief_w = max(max_brief_w, lw)
        if nlines != 1 or lw > 338 or end_y > 947:
            overflows.append(f"Brief {b['num']}: lines={nlines}, lw={lw:.1f}, end_y={end_y:.1f}")

    # =========================================================================
    # ZONE 8: COMPACT DATE CHECK (y = 951..1001, 50px tall, crimson border)
    # =========================================================================
    draw.rounded_rectangle([16, 951, 1008, 1001], radius=3, fill="#FAF6EE", outline=ACCENT_CRIMSON, width=1)
    # Extra crisp 1.2px feel via inner top/left tint or clean 1.5px stroke
    draw.rounded_rectangle([17, 952, 1007, 1000], radius=2, outline="#D4746E", width=1)
    draw.rounded_rectangle([16, 951, 1008, 1001], radius=3, outline=ACCENT_CRIMSON, width=1)

    # Solid crimson DATE CHECK pill
    draw.rounded_rectangle([23, 957, 104, 977], radius=2, fill=ACCENT_CRIMSON)
    draw_centered_text(draw, 63.5, 967, "DATE CHECK", F("NotoSans-Bold.ttf", 8.8), "#FFFFFF")
    draw_centered_text(draw, 63.5, 986.5, "10 TRAPS HELD BACK", F("NotoSans-CondensedBold.ttf", 6.8), ACCENT_CRIMSON)

    dc = data["date_check"]
    f_dc_b = F("NotoSans-SemiCondensedBold.ttf", 8.4)
    f_dc_r = F("NotoSans-SemiCondensed.ttf", 8.4)
    dc_body = "; ".join(dc["items"]) + "."
    dc_segs = [
        (dc["lead_in"], f_dc_b, INK_PRIMARY),
        (dc_body, f_dc_r, "#22201E"),
        (dc["not_yet_label"], f_dc_b, ACCENT_CRIMSON),
        (dc["not_yet_text"], f_dc_r, "#22201E"),
    ]
    dc_end, dc_lines, dc_w = draw_rich_lines(draw, 112, 954.5, dc_segs, 888, 10.6)
    if dc_end > 999 or dc_w > 888:
        overflows.append(f"DATE CHECK: end_y={dc_end:.1f} > 999 ({dc_lines} lines, w={dc_w:.1f})")

    # =========================================================================
    # ZONE 9: FOOTER + CONFIDENCE LEGEND (y = 1004..1021)
    # =========================================================================
    draw.line([(16, 1003), (1008, 1003)], fill=RULE_HAIRLINE, width=1)
    f_ft = F("NotoSans-SemiCondensed.ttf", 8.2)
    draw.text((16, 1007.5), data["footer_left"], fill="#3A3834", font=f_ft)

    # Center 3 bordered confidence pills
    cx = 356
    for conf_k, desc in [("CONFIRMED", "2+ outlets"), ("OFFICIAL", "on the record"), ("REPORTED", "one outlet")]:
        st = CONF_STYLES[conf_k]
        pf = F("NotoSans-CondensedBold.ttf", 7.2)
        pw = int(pf.getlength(conf_k)) + 7
        draw.rounded_rectangle([cx, 1007, cx + pw, 1018], radius=2, fill=st["fill"], outline=st["border"], width=1)
        draw_centered_text(draw, cx + pw / 2, 1012.5, conf_k, pf, st["text"])
        cx += pw + 3
        draw.text((cx, 1007.5), desc, fill="#3A3834", font=f_ft)
        cx += int(f_ft.getlength(desc)) + 9

    frw = f_ft.getlength(data["footer_right"])
    draw.text((1008 - frw, 1007.5), data["footer_right"], fill="#3A3834", font=f_ft)

    # Save optimized PNG
    img.save(out_path, format="PNG", optimize=True)
    size_bytes = os.path.getsize(out_path)
    print(f"Rendered {out_path}: {img.size[0]}x{img.size[1]}, {size_bytes:,} bytes ({size_bytes/1024:.1f} KiB)")
    print(f"Region counts (total={sum(reg_counts.values())}): {dict(reg_counts)}")
    if overflows:
        print("OVERFLOW WARNINGS:")
        for o in overflows:
            print("  !", o)
    else:
        print("ZERO text overflows detected!")
    return overflows


if __name__ == "__main__":
    dp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE_DIR, "data.json")
    op = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE_DIR, "entry.png")
    render_page(dp, op)
