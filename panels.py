"""13 bespoke story-specific editorial graphic panels (panel_01 .. panel_13) — Iteration 3 (run 8).

Each panel is rendered at 3x supersampling with Lanczos downsampling.
- Tonal cadence: 4 dark panels (3, 4, 6, 12 — zero horizontal, vertical, or lead-to-row2 adjacency),
  9 light panels.
- Giant bold focal callout (15–20px) inside EVERY panel, legible in the 300px preview.
- Zero white KPI sticker boxes; zero motif reuse across cards.
- Small panels (4..13) leave top-right ~54x14px clear for the confidence pill overlay.
- Hygiene fixes applied:
  * Panel 1: INDIA 17% IF DEAL moved off China->US arrow cleanly into bottom ribbon.
  * Panel 2: STRAIT OPEN replaced with '2 TANKERS HIT · IRAN SAYS'.
"""
import math
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/noto/"
S = 3  # 3x supersampling


def _f(name, sz):
    return ImageFont.truetype(FONT_DIR + name, max(6, int(round(sz * S))))


def _text_centered(draw, cx, cy, txt, font, fill, stroke_w=0, stroke_fill=None):
    bb = draw.textbbox((0, 0), txt, font=font, stroke_width=stroke_w)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    kw = {}
    if stroke_w > 0 and stroke_fill is not None:
        kw["stroke_width"] = stroke_w
        kw["stroke_fill"] = stroke_fill
    draw.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), txt, fill=fill, font=font, **kw)


def _ribbon(draw, x0, y0, x1, y1, text, bg="#181D26", fg="#FFFFFF", font_sz=7.6, radius=2, bold=True, condensed=True):
    draw.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=int(radius * S), fill=bg)
    fn = ("NotoSans-CondensedBold.ttf" if condensed else "NotoSans-Bold.ttf") if bold else "NotoSans-SemiCondensed.ttf"
    fnt = _f(fn, font_sz)
    _text_centered(draw, (x0 + x1) * S / 2, (y0 + y1) * S / 2, text, fnt, fg)


def _star_pts(cx, cy, r_out, r_in, n=5, angle_deg=-90):
    pts = []
    for i in range(n * 2):
        ang = math.radians(angle_deg + i * 180.0 / n)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def _dashed_line(draw, p0, p1, fill, width, dash=6, gap=4):
    x0, y0 = p0
    x1, y1 = p1
    dist = math.hypot(x1 - x0, y1 - y0)
    if dist < 1:
        return
    ux, uy = (x1 - x0) / dist, (y1 - y0) / dist
    d = 0.0
    while d < dist:
        e = min(d + dash * S, dist)
        draw.line([(x0 + ux * d, y0 + uy * d), (x0 + ux * e, y0 + uy * e)], fill=fill, width=int(width * S))
        d += (dash + gap) * S


def _dashed_polyline(draw, pts, fill, width, dash=5, gap=3.5):
    for a, b in zip(pts, pts[1:]):
        _dashed_line(draw, a, b, fill, width, dash=dash, gap=gap)


def _starburst(draw, cx, cy, r_out, r_in=None, spikes=10, outer="#D93829", mid="#F39C12", core="#FFF3B0"):
    if r_in is None:
        r_in = r_out * 0.45
    draw.polygon(_star_pts(cx, cy, r_out, r_in, spikes, -90), fill=outer)
    draw.polygon(_star_pts(cx, cy, r_out * 0.68, r_in * 0.65, spikes, -90 + 180 / spikes), fill=mid)
    draw.ellipse([cx - r_out * 0.24, cy - r_out * 0.24, cx + r_out * 0.24, cy + r_out * 0.24], fill=core)


def _finish(img, w, h):
    out = img.resize((w, h), Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(out)
    d.rectangle([0, 0, w - 1, h - 1], outline="#B8AFA0", width=1)
    return out


# =============================================================================
# ROW 1 — LEADS (322 x 124)
# =============================================================================

def panel_01(w=322, h=124):
    """Lead 1 (LIGHT): US & China flags, bold +20% focal callout, clean terms ribbon (incl. India 17%)."""
    W, H = w * S, h * S
    sy = h / 104.0
    img = Image.new("RGB", (W, H), "#C9C1B3")
    d = ImageDraw.Draw(img)

    for y in range(14, int(h - 24), 16):
        d.line([(0, y * S), (W, y * S)], fill="#BAB1A0", width=1)

    # --- US FLAG (left) ---
    fx, fy, fw, fh = 12 * S, 13 * sy * S, 96 * S, 58 * S
    d.rectangle([fx + 2 * S, fy + 2 * S, fx + fw + 2 * S, fy + fh + 2 * S], fill="#B7B0A1")
    d.rectangle([fx, fy, fx + fw, fy + fh], fill="#FFFFFF")
    sh = fh / 13.0
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([fx, fy + i * sh, fx + fw, fy + (i + 1) * sh], fill="#B8292F")
    cw, ch = fw * 0.42, sh * 7
    d.rectangle([fx, fy, fx + cw, fy + ch], fill="#1D3564")
    for r in range(5):
        cols = 6 if r % 2 == 0 else 5
        for c in range(cols):
            sx = fx + (c + (0.6 if r % 2 == 0 else 1.1)) * (cw / 6.2)
            sy_pt = fy + (r + 0.65) * (ch / 5.3)
            d.ellipse([sx - 1.3 * S, sy_pt - 1.3 * S, sx + 1.3 * S, sy_pt + 1.3 * S], fill="#FFFFFF")
    d.rectangle([fx, fy, fx + fw, fy + fh], outline="#7E776B", width=S)
    _text_centered(d, fx + fw / 2, fy + fh + 9.5 * S, "UNITED STATES", _f("NotoSans-Bold.ttf", 7.4), "#1D3564")

    # --- CHINA FLAG (right) ---
    cx0, cy0, cw0, ch0 = 214 * S, 13 * sy * S, 96 * S, 58 * S
    d.rectangle([cx0 + 2 * S, cy0 + 2 * S, cx0 + cw0 + 2 * S, cy0 + ch0 + 2 * S], fill="#B7B0A1")
    d.rectangle([cx0, cy0, cx0 + cw0, cy0 + ch0], fill="#C92228")
    d.polygon(_star_pts(cx0 + 17 * S, cy0 + 17 * S, 8.5 * S, 3.3 * S), fill="#F7CE2C")
    for (ox, oy, ang) in [(31, 8.5, -20), (35, 16, 10), (35, 24.5, 35), (30, 31, 60)]:
        d.polygon(_star_pts(cx0 + ox * S, cy0 + oy * S, 2.9 * S, 1.2 * S, angle_deg=ang), fill="#F7CE2C")
    d.rectangle([cx0, cy0, cx0 + cw0, cy0 + ch0], outline="#7E776B", width=S)
    _text_centered(d, cx0 + cw0 / 2, cy0 + ch0 + 9.5 * S, "CHINA", _f("NotoSans-Bold.ttf", 7.4), "#A11C21")

    # --- CENTER FOCAL CALLOUT (+20% at 20px) + CLEAN STACK & DIRECTIONAL ARROW ---
    _text_centered(d, 161 * S, 27 * sy * S, "+20%", _f("NotoSans-Black.ttf", 20.0), "#B3261E")
    _text_centered(d, 161 * S, 42 * sy * S, "NEW TARIFF", _f("NotoSans-CondensedBold.ttf", 7.5), "#262B36")

    # Rightward US -> China tariff arrow
    ax0, ax1, ay1 = 121 * S, 201 * S, 54 * sy * S
    d.line([(ax0, ay1), (ax1 - 7 * S, ay1)], fill="#B3261E", width=int(2.6 * S))
    d.polygon([(ax1, ay1), (ax1 - 9 * S, ay1 - 4.8 * S), (ax1 - 9 * S, ay1 + 4.8 * S)], fill="#B3261E")

    # Stacked bar (~25% existing + 20% proposed) cleanly beneath arrow (no India label here!)
    bx0, by0, bw0, bh0 = 123 * S, 64 * sy * S, 76 * S, 14 * S
    d.rectangle([bx0, by0, bx0 + 42 * S, by0 + bh0], fill="#2B3240")
    d.rectangle([bx0 + 42 * S, by0, bx0 + bw0, by0 + bh0], fill="#B3261E")
    _text_centered(d, bx0 + 21 * S, by0 + bh0 / 2, "~25% BASE", _f("NotoSans-CondensedBold.ttf", 6.8), "#FFFFFF")
    _text_centered(d, bx0 + 59 * S, by0 + bh0 / 2, "+20%", _f("NotoSans-CondensedBold.ttf", 7.2), "#FFFFFF")

    # Bottom ribbon with exact hygiene-fixed terms including INDIA 17% IF DEAL
    _ribbon(d, 8, h - 22, 314, h - 6,
            "CHINA +20% · EU/JAPAN/KOREA 15% CAP · INDIA 17% IF DEAL · 14 PARTNERS",
            bg="#171D27", fg="#F8F4EC", font_sz=7.1, radius=2)

    return _finish(img, w, h)


def panel_02(w=322, h=124):
    """Lead 2 (LIGHT): Strait of Hormuz map, 2 burning tankers, focal '2 TANKERS', ribbon '2 TANKERS HIT · IRAN SAYS'."""
    W, H = w * S, h * S
    sy = h / 104.0
    img = Image.new("RGB", (W, H), "#9EC4DC")
    d = ImageDraw.Draw(img)

    for y in (36, 56, 76):
        d.line([(0, y * sy * S), (W, y * sy * S)], fill="#91B9D3", width=max(1, S // 2))

    iran = [
        (0, 0), (322, 0), (322, 46), (294, 44), (272, 42), (250, 38),
        (228, 28), (206, 20), (180, 17), (156, 21), (128, 26), (102, 24),
        (76, 20), (48, 23), (22, 19), (0, 16)
    ]
    d.polygon([(x * S, y * sy * S) for x, y in iran], fill="#D3C39E", outline="#8B7F69", width=S)

    qeshm = [(142, 26), (168, 22), (176, 25), (166, 31), (144, 32)]
    d.polygon([(x * S, y * sy * S) for x, y in qeshm], fill="#CCB991", outline="#8B7F69", width=max(1, int(0.8 * S)))

    oman_uae = [
        (0, 104), (0, 84), (26, 84), (56, 86), (88, 84), (118, 78),
        (146, 69), (166, 60), (178, 52), (186, 51), (192, 57), (190, 67),
        (196, 75), (210, 85), (232, 95), (256, 104)
    ]
    d.polygon([(x * S, y * sy * S) for x, y in oman_uae], fill="#D3C39E", outline="#8B7F69", width=S)
    _dashed_line(d, (156 * S, 75 * sy * S), (196 * S, 75 * sy * S), "#877A64", 0.9, dash=3, gap=2.5)

    lane = [(14 * S, 70 * sy * S), (84 * S, 66 * sy * S), (144 * S, 52 * sy * S),
            (186 * S, 39 * sy * S), (228 * S, 48 * sy * S), (274 * S, 65 * sy * S), (316 * S, 73 * sy * S)]
    _dashed_polyline(d, lane, "#184C82", 1.5, dash=6, gap=4)

    def draw_tanker(tx, ty_base, scale=1.0):
        ty = ty_base * sy
        d.ellipse([(tx - 16 * scale) * S, (ty + 3 * scale) * S, (tx + 16 * scale) * S, (ty + 6 * scale) * S], fill="#7B9FB8")
        hull = [
            ((tx - 15 * scale) * S, (ty - 2 * scale) * S),
            ((tx + 12 * scale) * S, (ty - 2 * scale) * S),
            ((tx + 16 * scale) * S, (ty - 5 * scale) * S),
            ((tx + 14 * scale) * S, (ty + 4 * scale) * S),
            ((tx - 14 * scale) * S, (ty + 4 * scale) * S),
        ]
        d.polygon(hull, fill="#212933", outline="#0F141A", width=max(1, int(0.7 * S)))
        d.line([((tx - 13 * scale) * S, (ty + 3.2 * scale) * S), ((tx + 13 * scale) * S, (ty + 3.2 * scale) * S)],
               fill="#B3261E", width=max(1, int(1.4 * S)))
        d.rectangle([((tx - 13 * scale) * S), ((ty - 8 * scale) * S),
                     ((tx - 7 * scale) * S), ((ty - 2 * scale) * S)], fill="#F4F6F9", outline="#38424F", width=max(1, int(0.6 * S)))
        d.line([((tx - 5 * scale) * S, (ty - 3 * scale) * S), ((tx + 9 * scale) * S, (ty - 3 * scale) * S)],
               fill="#8D99AE", width=max(1, int(1.1 * S)))
        for (sx, sy_o, sr, col) in [(2, -11, 5.5, "#4E545C"), (7, -17, 6.5, "#697078"), (13, -22, 5.2, "#838A92")]:
            d.ellipse([((tx + sx * scale - sr * scale) * S), ((ty + sy_o * scale - sr * scale) * S),
                       ((tx + sx * scale + sr * scale) * S), ((ty + sy_o * scale + sr * scale) * S)], fill=col)
        _starburst(d, (tx + 3 * scale) * S, (ty - 4 * scale) * S, 7.8 * scale * S, 3.5 * scale * S, spikes=9)

    draw_tanker(162, 46, 1.02)
    draw_tanker(248, 56, 1.06)

    def draw_mine(mx, my_base):
        my = my_base * sy
        r = 3.8 * S
        for a in range(0, 360, 45):
            rad = math.radians(a)
            d.line([(mx * S, my * S), (mx * S + (r + 2.2 * S) * math.cos(rad), my * S + (r + 2.2 * S) * math.sin(rad))],
                   fill="#1C2026", width=max(1, int(1.0 * S)))
        d.ellipse([mx * S - r, my * S - r, mx * S + r, my * S + r], fill="#242933", outline="#B3261E", width=max(1, int(0.9 * S)))
        d.ellipse([mx * S - 1.3 * S, my * S - 1.3 * S, mx * S + 1.3 * S, my * S + 1.3 * S], fill="#F25C54")

    draw_mine(136, 58)
    draw_mine(224, 65)

    # GIANT FOCAL CALLOUT (18px) cleanly over open Persian Gulf water on left (above shipping lane)
    _text_centered(d, 68 * S, 40 * sy * S, "2 TANKERS", _f("NotoSans-CondensedBlack.ttf", 18.0),
                   "#8F1914", stroke_w=int(1.2 * S), stroke_fill="#D7EAF5")
    _text_centered(d, 68 * S, 55 * sy * S, "NAVAL MINES · HORMUZ", _f("NotoSans-CondensedBold.ttf", 7.2), "#163A54")

    d.text((18 * S, 4 * sy * S), "I R A N", fill="#544B3C", font=_f("NotoSans-Bold.ttf", 8.8))
    d.text((152 * S, 83 * sy * S), "OMAN", fill="#544B3C", font=_f("NotoSans-Bold.ttf", 8.0))
    d.text((28 * S, 89 * sy * S), "U.A.E.", fill="#635A4B", font=_f("NotoSans-SemiBold.ttf", 7.2))
    d.text((240 * S, 89 * sy * S), "STRAIT OF HORMUZ", fill="#1B425E", font=_f("NotoSans-Bold.ttf", 7.0))

    # Hygiene fix: replace STRAIT OPEN with 2 TANKERS HIT · IRAN SAYS
    _ribbon(d, 162, 6, 314, 21, "2 TANKERS HIT  ·  IRAN SAYS", bg="#A6211A", fg="#FFFFFF", font_sz=7.5, radius=2)

    return _finish(img, w, h)


def panel_03(w=322, h=124):
    """Lead 3 (DARK #1): Night strike on Ukraine power plant, giant '5 REGIONS' focal callout."""
    W, H = w * S, h * S
    sy = h / 104.0
    img = Image.new("RGB", (W, H), "#111A2C")
    d = ImageDraw.Draw(img)

    for i in range(28):
        y0 = int((29 + i * 2.15) * sy * S)
        y1 = int((32 + i * 2.15) * sy * S)
        r = int(17 + i * 0.9)
        g = int(26 + i * 0.8)
        b = int(44 + i * 0.8)
        d.rectangle([0, y0, W, y1], fill=(r, g, b))

    for (sx, sy_p) in [(168, 12), (218, 18), (274, 14), (298, 28), (195, 30), (146, 16)]:
        d.ellipse([sx * S - S, sy_p * sy * S - S, sx * S + S, sy_p * sy * S + S], fill="#6C82A8")

    gy_blast = 61 * sy
    for rad, col in [(46, "#2A2436"), (31, "#452930"), (18, "#70342A")]:
        d.ellipse([(166 - rad) * S, (gy_blast - rad) * S, (166 + rad) * S, (gy_blast + rad) * S], fill=col)

    _dashed_line(d, (286 * S, 16 * sy * S), (170 * S, 58 * sy * S), "#F6B93B", 1.35, dash=5, gap=3)
    d.line([(212 * S, 42 * sy * S), (170 * S, 58 * sy * S)], fill="#FF7B54", width=int(2.1 * S))

    d.rectangle([0, 81 * sy * S, W, H], fill="#0B111D")

    ct1 = [(26, 81), (32, 55), (30, 44), (54, 44), (52, 55), (58, 81)]
    d.polygon([(x * S, y * sy * S) for x, y in ct1], fill="#1E2B40", outline="#3A4E6E", width=S)
    ct2 = [(64, 81), (69, 60), (68, 50), (88, 50), (87, 60), (92, 81)]
    d.polygon([(x * S, y * sy * S) for x, y in ct2], fill="#1A2639", outline="#344766", width=S)
    d.rectangle([98 * S, 57 * sy * S, 180 * S, 81 * sy * S], fill="#162033", outline="#334663", width=S)
    for wx in range(104, 174, 12):
        d.rectangle([wx * S, 63 * sy * S, (wx + 6) * S, 69 * sy * S], fill="#0C1320")
    stack = [(140, 57), (143, 28), (149, 28), (152, 57)]
    d.polygon([(x * S, y * sy * S) for x, y in stack], fill="#24334C", outline="#445C82", width=max(1, int(0.8 * S)))
    for st_y in (33, 41, 49):
        d.rectangle([142.5 * S, st_y * sy * S, 149.5 * S, (st_y + 3) * sy * S], fill="#B33939")

    pylon = [(212, 81), (222, 41), (226, 41), (236, 81)]
    d.polygon([(x * S, y * sy * S) for x, y in pylon], outline="#4F688F", width=S)
    d.line([(208 * S, 50 * sy * S), (240 * S, 50 * sy * S)], fill="#4F688F", width=int(1.4 * S))
    d.line([(211 * S, 62 * sy * S), (237 * S, 62 * sy * S)], fill="#4F688F", width=int(1.2 * S))
    d.line([(180 * S, 61 * sy * S), (198 * S, 71 * sy * S), (203 * S, 77 * sy * S)], fill="#F6B93B", width=S)

    _starburst(d, 166 * S, 59 * sy * S, 14 * S, 6.0 * S, spikes=11)

    # GIANT FOCAL CALLOUT (19px) in clear upper-left night sky (replaces competing ribbon)
    d.text((14 * S, 7 * S), "5 REGIONS", fill="#F7C948", font=_f("NotoSans-ExtraBold.ttf", 19.0))
    d.text((15 * S, 31 * S), "POWER CUT · DTEK PLANT HIT", fill="#D6E0F0", font=_f("NotoSans-CondensedBold.ttf", 7.6))

    # 5 dark-grid nodes on right
    for i in range(5):
        nx = (250 + i * 13) * S
        ny = 67 * sy * S
        d.ellipse([nx - 4.4 * S, ny - 4.4 * S, nx + 4.4 * S, ny + 4.4 * S], fill="#0E1524", outline="#F25C54", width=int(1.3 * S))
        d.line([(nx - 2.3 * S, ny - 2.3 * S), (nx + 2.3 * S, ny + 2.3 * S)], fill="#F25C54", width=S)

    d.text((12 * S, (h - 16.5) * S), "DTEK THERMAL PLANT HALTED", fill="#C8D6EB", font=_f("NotoSans-CondensedBold.ttf", 7.3))
    d.text((184 * S, (h - 16.5) * S), "ZNPP: 17TH EXTERNAL OUTAGE", fill="#F6C453", font=_f("NotoSans-CondensedBold.ttf", 7.3))

    return _finish(img, w, h)


# =============================================================================
# ROW 2 — SMALL CARDS 4..8 (188 x 65)  [Keep top-right ~54x14 clear for pill!]
# =============================================================================

def panel_04(w=188, h=65):
    """Card 4 (DARK #2): Asian stocks plunge curves + giant '-5.3%' focal callout."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#151C28")
    d = ImageDraw.Draw(img)

    cx0, cx1 = 6, 98
    y_top_chart = 16.5
    y_bot_chart = h - 7.5
    y_span = y_bot_chart - y_top_chart
    for frac in (0.0, 0.33, 0.67, 1.0):
        gy = y_top_chart + y_span * frac
        d.line([(cx0 * S, gy * S), (cx1 * S, gy * S)], fill="#243044", width=1)
    _dashed_line(d, (cx0 * S, y_top_chart * S), (cx1 * S, y_top_chart * S), "#5E7390", 0.9, dash=3, gap=2.5)

    def plot_series(vals, color, width=1.65):
        pts = []
        n = len(vals) - 1
        for i, v in enumerate(vals):
            x = (cx0 + (cx1 - cx0) * (i / n)) * S
            y = (y_top_chart + (-v / 6.0) * y_span) * S
            pts.append((x, y))
        d.line(pts, fill=color, width=int(width * S))
        lx, ly = pts[-1]
        d.ellipse([lx - 2.3 * S, ly - 2.3 * S, lx + 2.3 * S, ly + 2.3 * S], fill=color)

    plot_series([0.0, -0.3, -0.5, -0.8, -1.1, -1.0, -1.5, -1.8, -2.0, -1.9, -2.2, -2.3], "#4CC9F0", 1.55)
    plot_series([0.0, -0.4, -0.9, -1.2, -1.4, -1.8, -2.1, -2.0, -2.4, -2.7, -2.8, -2.9], "#C3ADF0", 1.45)
    plot_series([0.0, -0.7, -1.4, -2.0, -2.8, -3.1, -3.6, -4.2, -4.5, -4.9, -5.0, -5.1], "#F6B93B", 1.55)
    plot_series([0.0, -0.9, -1.6, -2.4, -3.1, -3.8, -4.3, -4.6, -5.0, -5.2, -5.1, -5.3], "#FF5E57", 1.85)

    _ribbon(d, 5, 3, 52, 13, "WED EARLY", bg="#E5A93B", fg="#111827", font_sz=6.4, radius=1.5)

    # GIANT FOCAL CALLOUT (-5.3% at 19px) cleanly below top-right pill
    _text_centered(d, 143 * S, 33 * S, "-5.3%", _f("NotoSans-ExtraBold.ttf", 19.0), "#FF6058")
    _text_centered(d, 143 * S, 49 * S, "KOREA · TAIWAN -5.1%", _f("NotoSans-CondensedBold.ttf", 6.8), "#D6E2F5")
    _text_centered(d, 143 * S, 57.5 * S, "MSCI APAC -2.3%", _f("NotoSans-CondensedBold.ttf", 6.6), "#4CC9F0")

    return _finish(img, w, h)


def panel_05(w=188, h=65):
    """Card 5 (LIGHT): FT-style US macro dual-line chart + giant '3.8% / 4.3%' focal callout."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#DBC8B2")
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, int(2.5 * S)], fill="#C05E4B")

    y_bot = h - 8.5
    y_top = 16.5
    y_span = y_bot - y_top

    def y_of(pct):
        return (y_bot - ((pct - 3.0) / 1.6) * y_span) * S

    for pct in (3.0, 3.5, 4.0, 4.5):
        yy = y_of(pct)
        d.line([(8 * S, yy), (74 * S, yy)], fill="#C9B7A2", width=1)

    _dashed_line(d, (8 * S, y_of(3.6)), (74 * S, y_of(3.6)), "#BC736B", 0.9, dash=2.5, gap=2)
    _dashed_line(d, (8 * S, y_of(3.4)), (74 * S, y_of(3.4)), "#6E92B5", 0.9, dash=2.5, gap=2)

    gdp_pts = [(10 + i * 6.9, v) for i, v in enumerate([3.2, 3.3, 3.4, 3.4, 3.5, 3.7, 3.9, 4.1, 4.2, 4.3])]
    pce_pts = [(10 + i * 6.9, v) for i, v in enumerate([3.4, 3.45, 3.5, 3.55, 3.6, 3.6, 3.65, 3.7, 3.75, 3.8])]

    d.line([(x * S, y_of(v)) for x, v in gdp_pts], fill="#1A548F", width=int(2.2 * S))
    d.line([(x * S, y_of(v)) for x, v in pce_pts], fill="#B3261E", width=int(2.2 * S))

    gx, gy = gdp_pts[-1][0] * S, y_of(4.3)
    px, py = pce_pts[-1][0] * S, y_of(3.8)
    d.ellipse([gx - 3.0 * S, gy - 3.0 * S, gx + 3.0 * S, gy + 3.0 * S], fill="#1A548F", outline="#FFFFFF", width=max(1, int(0.7 * S)))
    d.ellipse([px - 3.0 * S, py - 3.0 * S, px + 3.0 * S, py + 3.0 * S], fill="#B3261E", outline="#FFFFFF", width=max(1, int(0.7 * S)))

    d.text((6 * S, 4 * S), "US MACRO · BEA", fill="#3A3128", font=_f("NotoSans-CondensedBold.ttf", 6.8))

    # GIANT FOCAL CALLOUT (3.8% / 4.3% at 16px, two-tone PCE crimson + GDP navy)
    f_big = _f("NotoSans-CondensedExtraBold.ttf", 16.0)
    parts = [("3.8%", "#A61D17"), (" / ", "#4F463D"), ("4.3%", "#154B82")]
    tot_w = sum(d.textbbox((0, 0), t, font=f_big)[2] - d.textbbox((0, 0), t, font=f_big)[0] for t, _ in parts)
    cur_x = 135 * S - tot_w / 2
    ref_bb = d.textbbox((0, 0), "3.8%", font=f_big)
    ty = 34 * S - (ref_bb[3] - ref_bb[1]) / 2 - ref_bb[1]
    for txt, col in parts:
        bb = d.textbbox((0, 0), txt, font=f_big)
        d.text((cur_x - bb[0], ty), txt, fill=col, font=f_big)
        cur_x += (bb[2] - bb[0])

    _text_centered(d, 135 * S, 51.5 * S, "PCE INFLATION  ·  Q3 GDP", _f("NotoSans-CondensedBold.ttf", 6.9), "#3A3128")
    return _finish(img, w, h)


def panel_06(w=188, h=65):
    """Card 6 (DARK #3): Ras Tanura dusk refinery skyline, radar intercept, giant '4 DRONES' focal callout."""
    W, H = w * S, h * S
    sy = h / 54.0
    img = Image.new("RGB", (W, H), "#171C2E")
    d = ImageDraw.Draw(img)

    for i in range(16):
        y0 = int((18 + i * 1.5) * sy * S)
        y1 = int((20.5 + i * 1.5) * sy * S)
        d.rectangle([0, y0, W, y1], fill=(24 + i * 3, 27 + i * 1, 46 + i // 2))
    gy = 45 * sy
    d.rectangle([0, gy * S, W, H], fill="#0E1524")
    d.line([(0, gy * S), (W, gy * S)], fill="#644A59", width=S)

    for tx, tr in [(14, 6.2), (27, 5.8), (39, 5.2)]:
        d.ellipse([(tx - tr) * S, (gy - 2 * tr) * S, (tx + tr) * S, gy * S], fill="#101520", outline="#4B5875", width=max(1, int(0.8 * S)))
    for rx, rw, rh in [(49, 4, 21), (56, 5, 16), (64, 3.5, 24), (72, 5.5, 13)]:
        d.rectangle([rx * S, (gy - rh * sy) * S, (rx + rw) * S, gy * S], fill="#0F1420", outline="#44526E", width=max(1, int(0.7 * S)))
    flare_top = gy - 22 * sy
    d.line([(82 * S, gy * S), (82 * S, flare_top * S)], fill="#4B5875", width=S)
    d.ellipse([79 * S, (flare_top - 5) * S, 85 * S, (flare_top + 1) * S], fill="#F39C12")
    d.ellipse([80.5 * S, (flare_top - 3.5) * S, 83.5 * S, (flare_top - 0.5) * S], fill="#FFF3B0")

    # Green radar arc + 4 intercepted drone X-marks cleanly on left/center
    d.arc([20 * S, 16 * sy * S, 102 * S, 76 * sy * S], start=205, end=335, fill="#45D69D", width=int(1.4 * S))
    drones = [(32, 24), (50, 17), (70, 18), (88, 25)]
    for dx, dy_base in drones:
        dy = dy_base * sy
        _dashed_line(d, ((dx + 14) * S, (dy + 8 * sy) * S), (dx * S, dy * S), "#FF6B63", 0.95, dash=2.2, gap=1.8)
        d.line([(dx - 2.8) * S, (dy - 2.8) * S, (dx + 2.8) * S, (dy + 2.8) * S], fill="#F9CC59", width=int(1.35 * S))
        d.line([(dx - 2.8) * S, (dy + 2.8) * S, (dx + 2.8) * S, (dy - 2.8) * S], fill="#F9CC59", width=int(1.35 * S))

    d.text((6 * S, 4 * S), "RAS TANURA · RIYADH", fill="#D6E0F2", font=_f("NotoSans-CondensedBold.ttf", 6.7))

    # GIANT FOCAL CALLOUT (4 DRONES at 17px) on right below pill
    _text_centered(d, 141 * S, 34 * S, "4 DRONES", _f("NotoSans-CondensedExtraBold.ttf", 17.0), "#F7C948")
    _text_centered(d, 141 * S, 50.5 * S, "DOWNED · SAUDIS", _f("NotoSans-CondensedBold.ttf", 7.0), "#D6E0F2")
    return _finish(img, w, h)


def panel_07(w=188, h=65):
    """Card 7 (LIGHT — PROMOTED): UK energy price cap — house + rising bill graphic, giant '£2,166' focal callout."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#D6D1C2")
    d = ImageDraw.Draw(img)

    # Subtle ledger grid lines
    for gy in (18, 34, 50):
        d.line([(0, gy * S), (W, gy * S)], fill="#C7C1B0", width=1)

    # Ground line
    d.rectangle([0, 56 * S, W, H], fill="#BFB8A6")

    # UK House silhouette (left, x=11..56)
    hx0, hx1, h_base, h_eave, h_peak = 12, 54, 56, 33, 17
    roof = [((hx0 - 4) * S, h_eave * S), ((hx0 + hx1) / 2 * S, h_peak * S), ((hx1 + 4) * S, h_eave * S)]
    d.polygon(roof, fill="#1E3557", outline="#112036", width=S)
    # Chimney
    d.rectangle([42 * S, 18 * S, 48 * S, 29 * S], fill="#2C4263", outline="#112036", width=max(1, int(0.8 * S)))
    # Walls
    d.rectangle([hx0 * S, h_eave * S, hx1 * S, h_base * S], fill="#243B5E", outline="#112036", width=S)
    # Warm lit windows + door
    d.rectangle([17 * S, 38 * S, 26 * S, 46 * S], fill="#F7C948", outline="#112036", width=max(1, int(0.6 * S)))
    d.rectangle([40 * S, 38 * S, 49 * S, 46 * S], fill="#F7C948", outline="#112036", width=max(1, int(0.6 * S)))
    d.rectangle([29 * S, 43 * S, 37 * S, 56 * S], fill="#B3261E", outline="#112036", width=max(1, int(0.6 * S)))

    # Rising bill stair-step bars & sharp crimson upward arrow (x=59..91)
    bars = [(60, 48, "#6E7A8A"), (69, 42, "#526073"), (78, 34, "#C94B38"), (87, 23, "#B3261E")]
    for bx, bt, col in bars:
        d.rectangle([bx * S, bt * S, (bx + 6.5) * S, 56 * S], fill=col)
    # Upward arrow over bars
    d.line([(61 * S, 44 * S), (88 * S, 19 * S)], fill="#B3261E", width=int(2.1 * S))
    d.polygon([(92 * S, 15.5 * S), (84 * S, 17.5 * S), (89.5 * S, 23.5 * S)], fill="#B3261E")

    d.text((6 * S, 4 * S), "UK ENERGY CAP · OFGEM", fill="#25344A", font=_f("NotoSans-CondensedBold.ttf", 6.7))

    # GIANT FOCAL CALLOUT (£2,166 at 19px) on right below OFFICIAL pill
    _text_centered(d, 141 * S, 33.5 * S, "£2,166", _f("NotoSans-ExtraBold.ttf", 19.0), "#A61F18")
    _text_centered(d, 141 * S, 49.5 * S, "+26% · 20M HOMES", _f("NotoSans-CondensedBold.ttf", 7.0), "#1E2D42")

    return _finish(img, w, h)


def panel_08(w=188, h=65):
    """Card 8 (LIGHT): Gaza coastline map with Beach camp marker + giant 'GAZA' focal callout."""
    W, H = w * S, h * S
    sy = h / 54.0
    img = Image.new("RGB", (W, H), "#A8CAE0")
    d = ImageDraw.Draw(img)

    land = [(42, 54), (68, 34), (92, 16), (114, 0), (188, 0), (188, 54)]
    d.polygon([(x * S, y * sy * S) for x, y in land], fill="#DACBA8", outline="#8F846F", width=S)

    gaza = [(42, 54), (68, 34), (92, 16), (105, 6), (118, 14), (101, 36), (76, 54)]
    d.polygon([(x * S, y * sy * S) for x, y in gaza], fill="#CEB992")
    _dashed_polyline(d, [(105 * S, 6 * sy * S), (118 * S, 14 * sy * S), (101 * S, 36 * sy * S), (76 * S, 54 * sy * S)], "#73644E", 1.1, dash=3.5, gap=2.5)

    px, py = 86 * S, 24 * sy * S
    d.ellipse([px - 8.2 * S, py - 8.2 * S, px + 8.2 * S, py + 8.2 * S], outline="#B3261E", width=int(1.25 * S))
    d.ellipse([px - 4.4 * S, py - 4.4 * S, px + 4.4 * S, py + 4.4 * S], fill="#B3261E", outline="#FFFFFF", width=max(1, int(0.8 * S)))

    d.text((7 * S, 8 * sy * S), "MED.", fill="#254E6B", font=_f("NotoSans-CondensedBold.ttf", 6.8))
    d.text((7 * S, 16 * sy * S), "SEA", fill="#254E6B", font=_f("NotoSans-CondensedBold.ttf", 6.8))

    # GIANT FOCAL CALLOUT (GAZA at 18px) over clean land area on right below pill
    _text_centered(d, 145 * S, 33.5 * S, "GAZA", _f("NotoSans-ExtraBold.ttf", 18.0), "#8F1D17")
    _text_centered(d, 145 * S, 49.5 * S, "BEACH CAMP · 2ND/24H", _f("NotoSans-CondensedBold.ttf", 6.7), "#3A3229")

    return _finish(img, w, h)


# =============================================================================
# ROW 3 — SMALL CARDS 9..13 (188 x 65)  [Keep top-right ~54x14 clear for pill!]
# =============================================================================

def panel_09(w=188, h=65):
    """Card 9 (LIGHT): Rosstat/BBC ledger bars + giant '490,334' focal callout."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#D4CCB9")
    d = ImageDraw.Draw(img)

    x_base, x_max = 8, 178
    for val in (0, 250, 500, 750):
        xx = (x_base + (x_max - x_base) * (val / 750.0)) * S
        d.line([(xx, 34 * S), (xx, (h - 4) * S)], fill="#C4B9A3", width=1)

    # GIANT FOCAL CALLOUT (490,334 at 18.5px) in clear upper-left, clear of CONFIRMED pill
    d.text((7 * S, 5 * S), "490,334", fill="#A61F18", font=_f("NotoSans-ExtraBold.ttf", 18.5))
    d.text((9 * S, 26.5 * S), "ROSSTAT / BBC CONFIRMED DEAD", fill="#2B2721", font=_f("NotoSans-CondensedBold.ttf", 6.6))

    # Two bold horizontal comparison bars below
    b1_w = (x_max - x_base) * (490.334 / 750.0)
    d.rectangle([x_base * S, 37 * S, (x_base + b1_w) * S, 46.5 * S], fill="#B3261E")
    d.text(((x_base + 3) * S, 38.0 * S), "490k CONFIRMED", fill="#FFFFFF", font=_f("NotoSans-CondensedBold.ttf", 6.4))

    b2_w = (x_max - x_base) * (700.0 / 750.0)
    d.rectangle([x_base * S, 49.5 * S, (x_base + b1_w) * S, 59 * S], fill="#2E3440")
    d.rectangle([(x_base + b1_w) * S, 49.5 * S, (x_base + b2_w) * S, 59 * S], fill="#667080", outline="#2E3440", width=max(1, int(0.7 * S)))
    hx = x_base + b1_w + 3
    while hx < x_base + b2_w - 2:
        d.line([(hx * S, 58.5 * S), ((hx + 6) * S, 50.0 * S)], fill="#3B4252", width=max(1, int(0.8 * S)))
        hx += 5
    d.text(((x_base + 3) * S, 50.5 * S), "700k+ WITH MISSING", fill="#FFFFFF", font=_f("NotoSans-CondensedBold.ttf", 6.4))

    return _finish(img, w, h)


def panel_10(w=188, h=65):
    """Card 10 (LIGHT): Sudan / Blue Nile map with Damazin marker + giant '19 DEAD' focal callout."""
    W, H = w * S, h * S
    sy = h / 54.0
    img = Image.new("RGB", (W, H), "#DDD0B6")
    d = ImageDraw.Draw(img)

    eth = [(98, 0), (188, 0), (188, 54), (92, 54), (104, 36), (106, 18)]
    d.polygon([(x * S, y * sy * S) for x, y in eth], fill="#CFC2A7", outline="#958870", width=S)

    bn = [(36, 22), (96, 17), (103, 34), (88, 48), (46, 46)]
    d.polygon([(x * S, y * sy * S) for x, y in bn], fill="#DBB27D", outline="#A2743D", width=S)

    river = [(118, 46), (100, 39), (82, 33), (66, 26), (52, 16), (40, 0)]
    d.line([(x * S, y * sy * S) for x, y in river], fill="#347CAE", width=int(2.5 * S))

    dx, dy = 74 * S, 30 * sy * S
    d.ellipse([dx - 7.0 * S, dy - 7.0 * S, dx + 7.0 * S, dy + 7.0 * S], outline="#B3261E", width=int(1.2 * S))
    d.ellipse([dx - 3.6 * S, dy - 3.6 * S, dx + 3.6 * S, dy + 3.6 * S], fill="#B3261E", outline="#FFFFFF", width=max(1, int(0.7 * S)))

    d.text((7 * S, 4 * S), "SUDAN · BLUE NILE", fill="#4D4335", font=_f("NotoSans-CondensedBold.ttf", 7.0))
    d.text((8 * S, 49 * S), "DAMAZIN", fill="#8F1D17", font=_f("NotoSans-CondensedBold.ttf", 7.0))

    # GIANT FOCAL CALLOUT (19 DEAD at 17.5px) cleanly on right below pill
    _text_centered(d, 144 * S, 33.5 * S, "19 DEAD", _f("NotoSans-CondensedExtraBold.ttf", 17.5), "#961D17")
    _text_centered(d, 144 * S, 49.5 * S, "20+ WOUNDED", _f("NotoSans-CondensedBold.ttf", 7.0), "#3A3128")

    return _finish(img, w, h)


def panel_11(w=188, h=65):
    """Card 11 (LIGHT): SW Pacific map (Australia + Solomon Islands), two flags, giant 'NO BASE' focal callout."""
    W, H = w * S, h * S
    sy = h / 54.0
    img = Image.new("RGB", (W, H), "#A8CCE2")
    d = ImageDraw.Draw(img)

    aus = [(0, 26), (18, 22), (32, 16), (40, 22), (52, 34), (66, 48), (68, 54), (0, 54)]
    d.polygon([(x * S, y * sy * S) for x, y in aus], fill="#DACBA8", outline="#8F856F", width=S)
    png = [(18, 0), (50, 0), (66, 8), (58, 12), (38, 8), (20, 6)]
    d.polygon([(x * S, y * sy * S) for x, y in png], fill="#CFC09F", outline="#8F856F", width=max(1, int(0.7 * S)))

    sol_islands = [
        [(84, 15), (94, 19), (92, 22), (82, 18)],
        [(95, 21), (104, 25), (102, 28), (93, 24)],
    ]
    for isl in sol_islands:
        d.polygon([(x * S, y * sy * S) for x, y in isl], fill="#246E28", outline="#154217", width=max(1, int(0.8 * S)))

    arc_pts = [(46 * S, 36 * sy * S), (64 * S, 26 * sy * S), (84 * S, 22 * sy * S)]
    _dashed_polyline(d, arc_pts, "#185E37", 1.65, dash=3.5, gap=2.5)

    # Australia mini-flag (bottom-left)
    ax, ay, aw, ah = 7 * S, (h - 20) * S, 26 * S, 15 * S
    d.rectangle([ax, ay, ax + aw, ay + ah], fill="#0C2C6E", outline="#FFFFFF", width=max(1, int(0.7 * S)))
    d.line([(ax, ay), (ax + aw * 0.48, ay + ah * 0.5)], fill="#FFFFFF", width=max(1, int(0.7 * S)))
    d.line([(ax + aw * 0.48, ay), (ax, ay + ah * 0.5)], fill="#FFFFFF", width=max(1, int(0.7 * S)))
    d.line([(ax + aw * 0.24, ay), (ax + aw * 0.24, ay + ah * 0.5)], fill="#D1262D", width=max(1, int(1.1 * S)))
    d.line([(ax, ay + ah * 0.25), (ax + aw * 0.48, ay + ah * 0.25)], fill="#D1262D", width=max(1, int(1.1 * S)))
    for sx, sy_p in [(0.74, 0.28), (0.86, 0.48), (0.74, 0.72), (0.64, 0.48)]:
        d.ellipse([ax + aw * sx - S, ay + ah * sy_p - S, ax + aw * sx + S, ay + ah * sy_p + S], fill="#FFFFFF")

    # Solomon Islands mini-flag (bottom-mid-left)
    bx, by, bw, bh = 38 * S, (h - 20) * S, 26 * S, 15 * S
    d.polygon([(bx, by), (bx + bw, by), (bx, by + bh)], fill="#1D56A8")
    d.polygon([(bx + bw, by), (bx + bw, by + bh), (bx, by + bh)], fill="#247A3C")
    d.line([(bx, by + bh), (bx + bw, by)], fill="#F4C427", width=int(2.0 * S))
    for sx, sy_p in [(0.16, 0.22), (0.34, 0.22), (0.25, 0.38)]:
        d.ellipse([bx + bw * sx - 0.8 * S, by + bh * sy_p - 0.8 * S, bx + bw * sx + 0.8 * S, by + bh * sy_p + 0.8 * S], fill="#FFFFFF")
    d.rectangle([bx, by, bx + bw, by + bh], outline="#FFFFFF", width=max(1, int(0.7 * S)))

    # GIANT FOCAL CALLOUT (NO BASE at 17.5px) on right below pill
    _text_centered(d, 142 * S, 34 * S, "NO BASE", _f("NotoSans-CondensedExtraBold.ttf", 17.5),
                   "#123F24", stroke_w=int(1.0 * S), stroke_fill="#D7EAF5")
    _text_centered(d, 142 * S, 50.5 * S, "AUS · SOLOMON IS.", _f("NotoSans-CondensedBold.ttf", 7.0), "#163B52")

    return _finish(img, w, h)


def panel_12(w=188, h=65):
    """Card 12 (DARK #4): Orbital diagram — Tiangong + Shenzhou-24 over Earth limb, giant '08:18' focal callout."""
    W, H = w * S, h * S
    sy = h / 54.0
    img = Image.new("RGB", (W, H), "#0F182A")
    d = ImageDraw.Draw(img)

    for (sx, sy_p) in [(14, 10), (38, 7), (68, 11), (104, 8), (118, 20), (54, 24), (24, 19)]:
        d.ellipse([sx * S - 0.85 * S, sy_p * sy * S - 0.85 * S, sx * S + 0.85 * S, sy_p * sy * S + 0.85 * S], fill="#93AED6")

    limb_dy = (h - 54)
    d.ellipse([-48 * S, (26 + limb_dy * 0.65) * S, 104 * S, (148 + limb_dy * 0.65) * S], fill="#1D5488", outline="#76D0FA", width=int(1.7 * S))
    d.pieslice([-40 * S, (32 + limb_dy * 0.65) * S, 94 * S, (140 + limb_dy * 0.65) * S], start=235, end=275, fill="#2F6E56")
    d.text((6 * S, (h - 12.5) * S), "JIUQUAN", fill="#C8EAFA", font=_f("NotoSans-CondensedBold.ttf", 6.4))

    orbit_pts = []
    for i in range(16):
        t = i / 15.0
        ox = 14 + t * 94
        oy = (45 - math.sin(t * math.pi * 0.72) * 29) * sy
        orbit_pts.append((ox * S, oy * S))
    _dashed_polyline(d, orbit_pts, "#8AC2EC", 1.15, dash=3, gap=2.5)

    tx, ty = 86 * S, 19 * sy * S
    d.rectangle([tx - 10.5 * S, ty - 2.1 * S, tx + 10.5 * S, ty + 2.1 * S], fill="#EEF3FA")
    for sx_off in (-6.5, 6.5):
        d.rectangle([tx + (sx_off - 2.1) * S, ty - 10.5 * S, tx + (sx_off + 2.1) * S, ty - 2.4 * S], fill="#4DA6EB", outline="#C2E4FC", width=max(1, int(0.6 * S)))
        d.rectangle([tx + (sx_off - 2.1) * S, ty + 2.4 * S, tx + (sx_off + 2.1) * S, ty + 10.5 * S], fill="#4DA6EB", outline="#C2E4FC", width=max(1, int(0.6 * S)))
    d.text((64 * S, 3 * S), "TIANGONG", fill="#C4DDF7", font=_f("NotoSans-CondensedBold.ttf", 6.4))

    cx, cy = 54 * S, 24.5 * sy * S
    d.polygon([(cx + 6.0 * S, cy), (cx + 1 * S, cy - 2.6 * S), (cx - 5.0 * S, cy - 2.6 * S), (cx - 5.0 * S, cy + 2.6 * S), (cx + 1 * S, cy + 2.6 * S)], fill="#F6C453")
    d.line([(cx - 1 * S, cy - 6.4 * S), (cx - 1 * S, cy + 6.4 * S)], fill="#88CEFA", width=int(1.25 * S))

    # GIANT FOCAL CALLOUT (08:18 at 19.5px) cleanly on right below CONFIRMED pill
    _text_centered(d, 144 * S, 34 * S, "08:18", _f("NotoSans-ExtraBold.ttf", 19.5), "#F7C948")
    _text_centered(d, 144 * S, 50.5 * S, "CST · CREW OF 3", _f("NotoSans-CondensedBold.ttf", 7.0), "#C8EAFA")

    return _finish(img, w, h)


def panel_13(w=188, h=65):
    """Card 13 (LIGHT — PROMOTED): Zambia generic HIV shots — vial & dose syringe graphic, giant '2x/YR' focal callout."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#CEDAD1")
    d = ImageDraw.Draw(img)

    # Clean clinical horizontal cadence lines
    for gy in (18, 36, 54):
        d.line([(0, gy * S), (W, gy * S)], fill="#BFCFC3", width=1)

    d.text((6 * S, 4 * S), "LENACAPAVIR · ZAMBIA", fill="#19453B", font=_f("NotoSans-CondensedBold.ttf", 6.7))

    # --- ILLUSTRATED MEDICAL VIAL (left, x=14..42, y=18..57) ---
    # Metal crimp cap + teal top
    d.rectangle([20 * S, 17 * S, 36 * S, 21 * S], fill="#0E6B5A", outline="#0A453A", width=max(1, int(0.8 * S)))
    d.rectangle([22 * S, 21 * S, 34 * S, 25 * S], fill="#95A5A6", outline="#526063", width=max(1, int(0.7 * S)))
    # Glass vial body
    d.rounded_rectangle([15 * S, 25 * S, 41 * S, 57 * S], radius=int(4 * S), fill="#EFF5F2", outline="#3F5954", width=S)
    # Amber/teal liquid inside bottom half
    d.rounded_rectangle([17 * S, 40 * S, 39 * S, 55 * S], radius=int(2.5 * S), fill="#6BB8A6")
    # Crisp label band on vial with medical cross
    d.rectangle([16 * S, 31 * S, 40 * S, 44 * S], fill="#0E6B5A")
    d.rectangle([26.5 * S, 33.5 * S, 29.5 * S, 41.5 * S], fill="#FFFFFF")
    d.rectangle([24 * S, 36 * S, 32 * S, 39 * S], fill="#FFFFFF")

    # --- CRISP SYRINGE / INJECTABLE DOSE GRAPHIC (x=48..92, angled up-right) ---
    # Needle
    d.line([(79 * S, 27 * S), (91 * S, 18 * S)], fill="#2D3D3A", width=int(1.2 * S))
    # Barrel (angled polygon from (56,44) to (79,27))
    ux, uy = 0.80, -0.60  # unit vector along syringe
    nx, ny = 0.60, 0.80   # perpendicular
    bx0, by0 = 57.0, 44.0
    blen, bhw = 27.0, 4.4
    p1 = ((bx0 - nx * bhw) * S, (by0 - ny * bhw) * S)
    p2 = ((bx0 + nx * bhw) * S, (by0 + ny * bhw) * S)
    p3 = ((bx0 + ux * blen + nx * bhw) * S, (by0 + uy * blen + ny * bhw) * S)
    p4 = ((bx0 + ux * blen - nx * bhw) * S, (by0 + uy * blen - ny * bhw) * S)
    d.polygon([p1, p2, p3, p4], fill="#F4F9F7", outline="#2E4A44", width=S)
    # Liquid fill inside syringe
    fl = 17.0
    q3 = ((bx0 + ux * fl + nx * (bhw - 1.2)) * S, (by0 + uy * fl + ny * (bhw - 1.2)) * S)
    q4 = ((bx0 + ux * fl - nx * (bhw - 1.2)) * S, (by0 + uy * fl - ny * (bhw - 1.2)) * S)
    q1 = ((bx0 + ux * 2 - nx * (bhw - 1.2)) * S, (by0 + uy * 2 - ny * (bhw - 1.2)) * S)
    q2 = ((bx0 + ux * 2 + nx * (bhw - 1.2)) * S, (by0 + uy * 2 + ny * (bhw - 1.2)) * S)
    d.polygon([q1, q2, q3, q4], fill="#178572")
    # Plunger rod + thumb flange
    d.line([(bx0 * S, by0 * S), ((bx0 - ux * 11) * S, (by0 - uy * 11) * S)], fill="#2E4A44", width=int(2.0 * S))
    px, py = bx0 - ux * 11, by0 - uy * 11
    d.line([((px - nx * 4.5) * S, (py - ny * 4.5) * S), ((px + nx * 4.5) * S, (py + ny * 4.5) * S)], fill="#0E6B5A", width=int(2.2 * S))

    # Two semi-annual dose pills beneath syringe (JAN / JUL visual cue)
    for dx_dot in (63, 79):
        d.ellipse([(dx_dot - 3.6) * S, 51 * S, (dx_dot + 3.6) * S, 58.2 * S], fill="#0E6B5A", outline="#FFFFFF", width=max(1, int(0.7 * S)))
    d.line([(66.6 * S, 54.6 * S), (75.4 * S, 54.6 * S)], fill="#0E6B5A", width=int(1.2 * S))

    # GIANT FOCAL CALLOUT (2x/YR at 19px) cleanly on right below REPORTED pill
    _text_centered(d, 142 * S, 34 * S, "2x/YR", _f("NotoSans-ExtraBold.ttf", 19.0), "#0E5A4C")
    _text_centered(d, 142 * S, 50.5 * S, "GENERIC HIV JAB", _f("NotoSans-CondensedBold.ttf", 7.0), "#1F3B35")

    return _finish(img, w, h)


PANEL_FUNCS = {
    1: panel_01,
    2: panel_02,
    3: panel_03,
    4: panel_04,
    5: panel_05,
    6: panel_06,
    7: panel_07,
    8: panel_08,
    9: panel_09,
    10: panel_10,
    11: panel_11,
    12: panel_12,
    13: panel_13,
}
