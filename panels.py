"""13 bespoke story-specific editorial graphic panels (panel_01 .. panel_13).

Each panel is rendered at 3x supersampling with Lanczos downsampling.
- Tonal cadence: 4 dark panels (3, 5, 7, 11 — none horizontally or vertically adjacent), 9 light panels.
- Zero white KPI sticker boxes; second-layer facts integrated into data graphics and editorial ribbons.
- Zero motif reuse across cards.
- Small panels (4..13) leave top-right ~54x14px clear for the confidence pill overlay.
"""
import math
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/noto/"
S = 3  # 3x supersampling


def _f(name, sz):
    return ImageFont.truetype(FONT_DIR + name, max(6, int(round(sz * S))))


def _text_centered(draw, cx, cy, txt, font, fill):
    bb = draw.textbbox((0, 0), txt, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), txt, fill=fill, font=font)


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
# ROW 1 — LEADS (322 x 104)
# =============================================================================

def panel_01(w=322, h=104):
    """Lead 1 (LIGHT): US & China flags, directional tariff schematic, terms ribbon."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#C9C1B3")
    d = ImageDraw.Draw(img)

    for y in range(14, 82, 14):
        d.line([(0, y * S), (W, y * S)], fill="#BAB1A0", width=1)

    # --- US FLAG (left) ---
    fx, fy, fw, fh = 14 * S, 13 * S, 102 * S, 55 * S
    d.rectangle([fx + 2 * S, fy + 2 * S, fx + fw + 2 * S, fy + fh + 2 * S], fill="#C2BBAC")
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
            sy = fy + (r + 0.65) * (ch / 5.3)
            d.ellipse([sx - 1.3 * S, sy - 1.3 * S, sx + 1.3 * S, sy + 1.3 * S], fill="#FFFFFF")
    d.rectangle([fx, fy, fx + fw, fy + fh], outline="#857E72", width=S)
    _text_centered(d, fx + fw / 2, 74.5 * S, "UNITED STATES", _f("NotoSans-Bold.ttf", 7.2), "#1D3564")

    # --- CHINA FLAG (right) ---
    cx0, cy0, cw0, ch0 = 206 * S, 13 * S, 102 * S, 55 * S
    d.rectangle([cx0 + 2 * S, cy0 + 2 * S, cx0 + cw0 + 2 * S, cy0 + ch0 + 2 * S], fill="#C2BBAC")
    d.rectangle([cx0, cy0, cx0 + cw0, cy0 + ch0], fill="#C92228")
    d.polygon(_star_pts(cx0 + 18 * S, cy0 + 16 * S, 8.5 * S, 3.3 * S), fill="#F7CE2C")
    for (ox, oy, ang) in [(32, 8, -20), (36, 15, 10), (36, 23, 35), (31, 29, 60)]:
        d.polygon(_star_pts(cx0 + ox * S, cy0 + oy * S, 3.0 * S, 1.2 * S, angle_deg=ang), fill="#F7CE2C")
    d.rectangle([cx0, cy0, cx0 + cw0, cy0 + ch0], outline="#857E72", width=S)
    _text_centered(d, cx0 + cw0 / 2, 74.5 * S, "CHINA", _f("NotoSans-Bold.ttf", 7.2), "#A11C21")

    # --- CENTER TARIFF FLOW ARROWS & RATE STACK ---
    ax0, ax1, ay1 = 124 * S, 198 * S, 28 * S
    d.line([(ax0, ay1), (ax1 - 7 * S, ay1)], fill="#B3261E", width=int(2.6 * S))
    d.polygon([(ax1, ay1), (ax1 - 9 * S, ay1 - 4.8 * S), (ax1 - 9 * S, ay1 + 4.8 * S)], fill="#B3261E")
    _text_centered(d, 161 * S, 17.5 * S, "NEW +20%", _f("NotoSans-ExtraBold.ttf", 9.5), "#B3261E")

    bx0, by0, bw0, bh0 = 128 * S, 36 * S, 66 * S, 11 * S
    d.rectangle([bx0, by0, bx0 + 36 * S, by0 + bh0], fill="#2B3240")
    d.rectangle([bx0 + 36 * S, by0, bx0 + bw0, by0 + bh0], fill="#B3261E")
    _text_centered(d, bx0 + 18 * S, by0 + bh0 / 2, "~25%", _f("NotoSans-Bold.ttf", 6.8), "#FFFFFF")
    _text_centered(d, bx0 + 51 * S, by0 + bh0 / 2, "+20%", _f("NotoSans-Bold.ttf", 6.8), "#FFFFFF")

    ay2 = 56 * S
    d.line([(ax0 + 7 * S, ay2), (ax1, ay2)], fill="#2B3240", width=int(2.0 * S))
    d.polygon([(ax0, ay2), (ax0 + 8 * S, ay2 - 4 * S), (ax0 + 8 * S, ay2 + 4 * S)], fill="#2B3240")
    _text_centered(d, 161 * S, 66.5 * S, "INDIA 17% IF DEAL", _f("NotoSans-CondensedBold.ttf", 7.2), "#2B3240")

    _ribbon(d, 10, 82, 312, 98, "CHINA +20%  ·  EU/JAPAN/KOREA 15% CAP  ·  14 PARTNERS",
            bg="#171D27", fg="#F8F4EC", font_sz=7.8, radius=2)

    return _finish(img, w, h)


def panel_02(w=322, h=104):
    """Lead 2 (LIGHT): Real Strait of Hormuz coastline map, 2 tankers hit, mines, lane."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#9EC4DC")
    d = ImageDraw.Draw(img)

    for y in (36, 56, 76):
        d.line([(0, y * S), (W, y * S)], fill="#91B9D3", width=max(1, S // 2))

    iran = [
        (0, 0), (322, 0), (322, 49), (294, 47), (272, 45), (250, 41),
        (228, 29), (206, 21), (180, 18), (156, 22), (128, 27), (102, 25),
        (76, 21), (48, 24), (22, 20), (0, 17)
    ]
    d.polygon([(x * S, y * S) for x, y in iran], fill="#D3C39E", outline="#8B7F69", width=S)

    qeshm = [(142, 27), (168, 23), (176, 26), (166, 32), (144, 33)]
    d.polygon([(x * S, y * S) for x, y in qeshm], fill="#CCB991", outline="#8B7F69", width=max(1, int(0.8 * S)))

    oman_uae = [
        (0, 104), (0, 84), (26, 84), (56, 86), (88, 84), (118, 77),
        (146, 68), (166, 59), (178, 51), (186, 50), (192, 56), (190, 66),
        (196, 74), (210, 84), (232, 94), (256, 104)
    ]
    d.polygon([(x * S, y * S) for x, y in oman_uae], fill="#D3C39E", outline="#8B7F69", width=S)
    _dashed_line(d, (156 * S, 74 * S), (196 * S, 74 * S), "#877A64", 0.9, dash=3, gap=2.5)

    lane = [(14 * S, 62 * S), (84 * S, 58 * S), (144 * S, 49 * S), (186 * S, 38 * S), (228 * S, 47 * S), (274 * S, 64 * S), (316 * S, 72 * S)]
    _dashed_polyline(d, lane, "#184C82", 1.5, dash=6, gap=4)

    def draw_tanker(tx, ty, scale=1.0):
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
        for (sx, sy, sr, col) in [(2, -11, 5.5, "#4E545C"), (7, -17, 6.5, "#697078"), (13, -22, 5.2, "#838A92")]:
            d.ellipse([((tx + sx * scale - sr * scale) * S), ((ty + sy * scale - sr * scale) * S),
                       ((tx + sx * scale + sr * scale) * S), ((ty + sy * scale + sr * scale) * S)], fill=col)
        _starburst(d, (tx + 3 * scale) * S, (ty - 4 * scale) * S, 7.5 * scale * S, 3.4 * scale * S, spikes=9)

    draw_tanker(132, 46, 0.95)
    draw_tanker(230, 55, 1.0)

    def draw_mine(mx, my):
        r = 3.6 * S
        for a in range(0, 360, 45):
            rad = math.radians(a)
            d.line([(mx * S, my * S), (mx * S + (r + 2.1 * S) * math.cos(rad), my * S + (r + 2.1 * S) * math.sin(rad))],
                   fill="#1C2026", width=max(1, int(1.0 * S)))
        d.ellipse([mx * S - r, my * S - r, mx * S + r, my * S + r], fill="#242933", outline="#B3261E", width=max(1, int(0.9 * S)))
        d.ellipse([mx * S - 1.2 * S, my * S - 1.2 * S, mx * S + 1.2 * S, my * S + 1.2 * S], fill="#F25C54")

    draw_mine(108, 58)
    draw_mine(206, 64)
    _text_centered(d, 98 * S, 71.5 * S, "NAVAL MINES", _f("NotoSans-CondensedBold.ttf", 6.2), "#8B1D17")

    d.text((22 * S, 4 * S), "I R A N", fill="#544B3C", font=_f("NotoSans-Bold.ttf", 8.5))
    d.text((152 * S, 82 * S), "OMAN", fill="#544B3C", font=_f("NotoSans-Bold.ttf", 7.8))
    d.text((34 * S, 89 * S), "U.A.E.", fill="#635A4B", font=_f("NotoSans-SemiBold.ttf", 7.0))
    d.text((18 * S, 37 * S), "PERSIAN GULF", fill="#2D5673", font=_f("NotoSans-Bold.ttf", 6.6))
    d.text((238 * S, 87 * S), "STRAIT OF HORMUZ", fill="#1B425E", font=_f("NotoSans-Bold.ttf", 7.0))

    _ribbon(d, 152, 6, 314, 21, "2 TANKERS HIT  ·  STRAIT OPEN", bg="#A6211A", fg="#FFFFFF", font_sz=7.6, radius=2)

    return _finish(img, w, h)


def panel_03(w=322, h=104):
    """Lead 3 (DARK #1): Night strike on Ukraine power plant, 5 dark regions, ZNPP note."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#111A2C")
    d = ImageDraw.Draw(img)

    for i in range(28):
        y0 = int((29 + i * 2.15) * S)
        y1 = int((32 + i * 2.15) * S)
        r = int(17 + i * 0.9)
        g = int(26 + i * 0.8)
        b = int(44 + i * 0.8)
        d.rectangle([0, y0, W, y1], fill=(r, g, b))

    for (sx, sy) in [(24, 28), (64, 16), (112, 22), (168, 12), (218, 18), (274, 14), (298, 28), (195, 30)]:
        d.ellipse([sx * S - S, sy * S - S, sx * S + S, sy * S + S], fill="#6C82A8")

    for rad, col in [(42, "#2A2436"), (28, "#452930"), (16, "#70342A")]:
        d.ellipse([(158 - rad) * S, (61 - rad) * S, (158 + rad) * S, (61 + rad) * S], fill=col)

    _dashed_line(d, (278 * S, 16 * S), (162 * S, 58 * S), "#F6B93B", 1.3, dash=5, gap=3)
    d.line([(204 * S, 42 * S), (162 * S, 58 * S)], fill="#FF7B54", width=int(2.0 * S))

    d.rectangle([0, 80 * S, W, H], fill="#0B111D")

    ct1 = [(30, 80), (36, 55), (34, 41), (58, 41), (56, 55), (62, 80)]
    d.polygon([(x * S, y * S) for x, y in ct1], fill="#1E2B40", outline="#3A4E6E", width=S)
    ct2 = [(68, 80), (73, 59), (72, 48), (92, 48), (91, 59), (96, 80)]
    d.polygon([(x * S, y * S) for x, y in ct2], fill="#1A2639", outline="#344766", width=S)
    d.rectangle([100 * S, 57 * S, 174 * S, 80 * S], fill="#162033", outline="#334663", width=S)
    for wx in range(106, 168, 12):
        d.rectangle([wx * S, 63 * S, (wx + 6) * S, 69 * S], fill="#0C1320")
    stack = [(134, 57), (137, 24), (143, 24), (146, 57)]
    d.polygon([(x * S, y * S) for x, y in stack], fill="#24334C", outline="#445C82", width=max(1, int(0.8 * S)))
    for sy in (30, 38, 46):
        d.rectangle([136.5 * S, sy * S, 143.5 * S, (sy + 3) * S], fill="#B33939")

    pylon = [(208, 80), (218, 39), (222, 39), (232, 80)]
    d.polygon([(x * S, y * S) for x, y in pylon], outline="#4F688F", width=S)
    d.line([(204 * S, 49 * S), (236 * S, 49 * S)], fill="#4F688F", width=int(1.4 * S))
    d.line([(207 * S, 61 * S), (233 * S, 61 * S)], fill="#4F688F", width=int(1.2 * S))
    d.line([(174 * S, 61 * S), (192 * S, 71 * S), (197 * S, 77 * S)], fill="#F6B93B", width=S)
    d.line([(204 * S, 49 * S), (195 * S, 55 * S)], fill="#6C84AB", width=S)

    _starburst(d, 158 * S, 59 * S, 13 * S, 5.5 * S, spikes=11)

    d.text((246 * S, 41 * S), "5 REGIONS", fill="#F6C453", font=_f("NotoSans-Bold.ttf", 7.2))
    d.text((246 * S, 50 * S), "POWER OUT", fill="#B6C6DF", font=_f("NotoSans-CondensedBold.ttf", 6.6))
    for i in range(5):
        nx = (250 + i * 13) * S
        ny = 66 * S
        d.ellipse([nx - 4.2 * S, ny - 4.2 * S, nx + 4.2 * S, ny + 4.2 * S], fill="#0E1524", outline="#F25C54", width=int(1.3 * S))
        d.line([(nx - 2.2 * S, ny - 2.2 * S), (nx + 2.2 * S, ny + 2.2 * S)], fill="#F25C54", width=S)

    d.text((12 * S, 86 * S), "DTEK THERMAL PLANT HALTED", fill="#D6E0F0", font=_f("NotoSans-CondensedBold.ttf", 7.2))
    d.text((184 * S, 86 * S), "ZNPP: 17TH EXTERNAL OUTAGE", fill="#F6C453", font=_f("NotoSans-CondensedBold.ttf", 7.2))

    _ribbon(d, 10, 7, 174, 22, "5 REGIONS DARK  ·  PLANT HIT", bg="#E5A93B", fg="#111827", font_sz=7.6, radius=2)

    return _finish(img, w, h)


# =============================================================================
# ROW 2 — SMALL CARDS (188 x 54)  [Keep top-right ~54x14 clear for pill!]
# =============================================================================

def panel_04(w=188, h=54):
    """Card 4 (LIGHT): Savasleyka air-base tactical diagram with 3 MiG-31 + 2 Su-34 split."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#D6CEB8")
    d = ImageDraw.Draw(img)

    for gx in range(24, w, 28):
        d.line([(gx * S, 0), (gx * S, H)], fill="#C7BEA6", width=1)
    for gy in range(18, h, 18):
        d.line([(0, gy * S), (W, gy * S)], fill="#C7BEA6", width=1)

    rwy = [(8, 30), (132, 12), (135, 19), (11, 37)]
    d.polygon([(x * S, y * S) for x, y in rwy], fill="#646E78", outline="#485058", width=max(1, int(0.8 * S)))
    _dashed_line(d, (14 * S, 33 * S), (128 * S, 16 * S), "#F4F1EA", 0.9, dash=4, gap=3)

    apron = [(56, 31), (138, 20), (176, 36), (170, 44), (62, 39)]
    d.polygon([(x * S, y * S) for x, y in apron], fill="#BEB49D", outline="#8F8671", width=max(1, int(0.8 * S)))

    _dashed_polyline(d, [(4 * S, 50 * S), (44 * S, 42 * S), (82 * S, 33 * S)], "#B3261E", 1.3, dash=4, gap=2.5)

    bays = [
        (74, 33, "#B3261E"), (91, 31, "#B3261E"), (108, 29, "#B3261E"),
        (132, 31, "#C96818"), (152, 35, "#C96818"),
    ]
    for bx, by, col in bays:
        r = 5.0 * S
        d.rectangle([bx * S - r, by * S - r * 0.8, bx * S + r, by * S + r * 0.8], fill="#F6F2E9", outline=col, width=int(1.2 * S))
        d.polygon([(bx * S, by * S - 2.8 * S), (bx * S + 2.8 * S, by * S),
                   (bx * S, by * S + 2.8 * S), (bx * S - 2.8 * S, by * S)], fill=col)

    d.text((6 * S, 4 * S), "SAVASLEYKA BASE", fill="#322E27", font=_f("NotoSans-CondensedBold.ttf", 6.8))
    _ribbon(d, 6, 40, 114, 51, "3 MiG-31  +  2 Su-34 HIT", bg="#1B222C", fg="#F8F4EC", font_sz=6.6, radius=1.5)
    return _finish(img, w, h)


def panel_05(w=188, h=54):
    """Card 5 (DARK #2): Ras Tanura dusk refinery skyline, coalition radar intercepting 4 drones."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#171C2E")
    d = ImageDraw.Draw(img)

    for i in range(16):
        y0 = int((18 + i * 1.5) * S)
        y1 = int((20 + i * 1.5) * S)
        d.rectangle([0, y0, W, y1], fill=(24 + i * 3, 27 + i * 1, 46 + i // 2))
    d.rectangle([0, 42 * S, W, H], fill="#0E1524")
    d.line([(0, 42 * S), (W, 42 * S)], fill="#644A59", width=S)

    for tx, tr in [(16, 6), (30, 5.5), (43, 5)]:
        d.ellipse([(tx - tr) * S, (42 - 2 * tr) * S, (tx + tr) * S, 42 * S], fill="#101520", outline="#4B5875", width=max(1, int(0.8 * S)))
    for rx, rw, rh in [(54, 4, 21), (61, 5, 16), (69, 3.5, 24), (77, 6, 13)]:
        d.rectangle([rx * S, (42 - rh) * S, (rx + rw) * S, 42 * S], fill="#0F1420", outline="#44526E", width=max(1, int(0.7 * S)))
    d.line([(88 * S, 42 * S), (88 * S, 20 * S)], fill="#4B5875", width=S)
    d.ellipse([85 * S, 15 * S, 91 * S, 21 * S], fill="#F39C12")
    d.ellipse([86.5 * S, 16.5 * S, 89.5 * S, 19.5 * S], fill="#FFF3B0")

    d.arc([78 * S, 16 * S, 166 * S, 78 * S], start=200, end=330, fill="#45D69D", width=int(1.4 * S))
    d.arc([92 * S, 24 * S, 152 * S, 70 * S], start=205, end=325, fill="#2B8A66", width=max(1, int(0.9 * S)))

    drones = [(104, 24), (122, 19), (140, 22), (156, 29)]
    for dx, dy in drones:
        _dashed_line(d, ((dx + 22) * S, (dy + 11) * S), (dx * S, dy * S), "#FF6B63", 1.0, dash=2.5, gap=2)
        d.line([(dx - 2.8) * S, (dy - 2.8) * S, (dx + 2.8) * S, (dy + 2.8) * S], fill="#F9CC59", width=int(1.3 * S))
        d.line([(dx - 2.8) * S, (dy + 2.8) * S, (dx + 2.8) * S, (dy - 2.8) * S], fill="#F9CC59", width=int(1.3 * S))

    d.text((6 * S, 4 * S), "RAS TANURA · RIYADH", fill="#D6E0F2", font=_f("NotoSans-CondensedBold.ttf", 6.5))
    _ribbon(d, 6, 40, 96, 51, "4 DRONES DOWNED", bg="#E5A93B", fg="#111827", font_sz=6.6, radius=1.5)
    return _finish(img, w, h)


def panel_06(w=188, h=54):
    """Card 6 (LIGHT): Gaza coastline map with Beach camp marker, respectful cartography."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#A8CAE0")
    d = ImageDraw.Draw(img)

    land = [(46, 54), (72, 34), (98, 16), (122, 0), (188, 0), (188, 54)]
    d.polygon([(x * S, y * S) for x, y in land], fill="#DACBA8", outline="#8F846F", width=S)

    gaza = [(46, 54), (72, 34), (98, 16), (112, 6), (126, 14), (108, 36), (82, 54)]
    d.polygon([(x * S, y * S) for x, y in gaza], fill="#CEB992")
    _dashed_polyline(d, [(112 * S, 6 * S), (126 * S, 14 * S), (108 * S, 36 * S), (82 * S, 54 * S)], "#73644E", 1.1, dash=3.5, gap=2.5)

    d.line([(56 * S, 52 * S), (106 * S, 16 * S)], fill="#B09D7D", width=max(1, int(0.8 * S)))

    px, py = 93 * S, 21 * S
    d.ellipse([px - 7.5 * S, py - 7.5 * S, px + 7.5 * S, py + 7.5 * S], outline="#B3261E", width=int(1.1 * S))
    d.ellipse([px - 4 * S, py - 4 * S, px + 4 * S, py + 4 * S], fill="#B3261E", outline="#FFFFFF", width=max(1, int(0.8 * S)))

    d.text((7 * S, 10 * S), "MEDITERRANEAN", fill="#254E6B", font=_f("NotoSans-CondensedBold.ttf", 6.5))
    d.text((15 * S, 18 * S), "SEA", fill="#254E6B", font=_f("NotoSans-CondensedBold.ttf", 6.5))
    d.text((104 * S, 21 * S), "BEACH CAMP", fill="#8F1D17", font=_f("NotoSans-CondensedBold.ttf", 7.0))
    d.text((112 * S, 31 * S), "GAZA CITY", fill="#3A3229", font=_f("NotoSans-CondensedBold.ttf", 6.8))

    _ribbon(d, 6, 40, 102, 51, "NORTH GAZA · EARLY WED", bg="#222832", fg="#F8F4EC", font_sz=6.3, radius=1.5)
    return _finish(img, w, h)


def panel_07(w=188, h=54):
    """Card 7 (DARK #3): Dark terminal chart, 4 Asian intraday index plunge curves + ticker."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#151C28")
    d = ImageDraw.Draw(img)

    cx0, cx1 = 6, 103
    for gy in (16, 27, 38, 48):
        d.line([(cx0 * S, gy * S), (cx1 * S, gy * S)], fill="#243044", width=1)
    _dashed_line(d, (cx0 * S, 16 * S), (cx1 * S, 16 * S), "#5E7390", 0.9, dash=3, gap=2.5)

    def plot_series(vals, color, width=1.5):
        pts = []
        n = len(vals) - 1
        for i, v in enumerate(vals):
            x = (cx0 + (cx1 - cx0) * (i / n)) * S
            y = (16 + (-v / 6.0) * 32) * S
            pts.append((x, y))
        d.line(pts, fill=color, width=int(width * S))
        lx, ly = pts[-1]
        d.ellipse([lx - 2 * S, ly - 2 * S, lx + 2 * S, ly + 2 * S], fill=color)

    plot_series([0.0, -0.3, -0.5, -0.8, -1.1, -1.0, -1.5, -1.8, -2.0, -1.9, -2.2, -2.3], "#4CC9F0", 1.5)
    plot_series([0.0, -0.4, -0.9, -1.2, -1.4, -1.8, -2.1, -2.0, -2.4, -2.7, -2.8, -2.9], "#C3ADF0", 1.4)
    plot_series([0.0, -0.7, -1.4, -2.0, -2.8, -3.1, -3.6, -4.2, -4.5, -4.9, -5.0, -5.1], "#F6B93B", 1.5)
    plot_series([0.0, -0.9, -1.6, -2.4, -3.1, -3.8, -4.3, -4.6, -5.0, -5.2, -5.1, -5.3], "#F25C54", 1.6)

    _ribbon(d, 5, 3, 52, 13, "WED EARLY", bg="#E5A93B", fg="#111827", font_sz=6.2, radius=1.5)

    rows = [
        ("#4CC9F0", "MSCI APAC", "-2.3%"),
        ("#C3ADF0", "NIKKEI", "-2.9%"),
        ("#F6B93B", "TAIWAN", "-5.1%"),
        ("#F25C54", "KOREA", "-5.3%"),
    ]
    f_lbl = _f("NotoSans-CondensedBold.ttf", 6.6)
    f_val = _f("NotoSans-CondensedBold.ttf", 6.7)
    for idx, (col, name, val) in enumerate(rows):
        ry = (16.5 + idx * 8.7) * S
        d.rectangle([108 * S, ry + 1.8 * S, 111.5 * S, ry + 5.4 * S], fill=col)
        d.text((114 * S, ry - 0.5 * S), name, fill="#EEF3FA", font=f_lbl)
        bb = d.textbbox((0, 0), val, font=f_val)
        d.text((184 * S - (bb[2] - bb[0]), ry - 0.5 * S), val, fill=col, font=f_val)

    return _finish(img, w, h)


def panel_08(w=188, h=54):
    """Card 8 (LIGHT): FT-style cream dual-series chart (PCE 3.8% vs 3.6%, GDP 4.3% vs 3.4%)."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#DBC8B2")
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, int(2.4 * S)], fill="#C05E4B")

    def y_of(pct):
        return (44 - ((pct - 3.0) / 1.6) * 29) * S

    for pct in (3.0, 3.5, 4.0, 4.5):
        yy = y_of(pct)
        d.line([(22 * S, yy), (126 * S, yy)], fill="#CEBEA9", width=1)
        d.text((4 * S, yy - 3.5 * S), f"{pct:.1f}%", fill="#544B40", font=_f("NotoSans-CondensedBold.ttf", 6.0))

    _dashed_line(d, (22 * S, y_of(3.6)), (126 * S, y_of(3.6)), "#BC736B", 1.0, dash=3, gap=2.5)
    _dashed_line(d, (22 * S, y_of(3.4)), (126 * S, y_of(3.4)), "#6E92B5", 1.0, dash=3, gap=2.5)

    gdp_pts = [(24 + i * 11, v) for i, v in enumerate([3.2, 3.3, 3.4, 3.4, 3.5, 3.7, 3.9, 4.1, 4.2, 4.3])]
    pce_pts = [(24 + i * 11, v) for i, v in enumerate([3.4, 3.45, 3.5, 3.55, 3.6, 3.6, 3.65, 3.7, 3.75, 3.8])]

    d.line([(x * S, y_of(v)) for x, v in gdp_pts], fill="#1A548F", width=int(2.1 * S))
    d.line([(x * S, y_of(v)) for x, v in pce_pts], fill="#B3261E", width=int(2.1 * S))

    gx, gy = gdp_pts[-1][0] * S, y_of(4.3)
    px, py = pce_pts[-1][0] * S, y_of(3.8)
    d.ellipse([gx - 2.8 * S, gy - 2.8 * S, gx + 2.8 * S, gy + 2.8 * S], fill="#1A548F", outline="#FFFFFF", width=max(1, int(0.7 * S)))
    d.ellipse([px - 2.8 * S, py - 2.8 * S, px + 2.8 * S, py + 2.8 * S], fill="#B3261E", outline="#FFFFFF", width=max(1, int(0.7 * S)))

    d.text((130 * S, 18 * S), "GDP +4.3%", fill="#1A548F", font=_f("NotoSans-CondensedBold.ttf", 7.4))
    d.text((130 * S, 26.5 * S), "adv. 3.4%", fill="#4C6987", font=_f("NotoSans-CondensedBold.ttf", 6.1))
    d.text((130 * S, 34 * S), "PCE 3.8%", fill="#B3261E", font=_f("NotoSans-CondensedBold.ttf", 7.4))
    d.text((130 * S, 42.5 * S), "Sep 3.6%", fill="#8C4943", font=_f("NotoSans-CondensedBold.ttf", 6.1))

    d.text((6 * S, 4 * S), "US MACRO · BEA", fill="#3A3128", font=_f("NotoSans-CondensedBold.ttf", 6.6))
    return _finish(img, w, h)


# =============================================================================
# ROW 3 — SMALL CARDS (188 x 54)  [Keep top-right ~54x14 clear for pill!]
# =============================================================================

def panel_09(w=188, h=54):
    """Card 9 (LIGHT): Sudan / Blue Nile map with Damazin marker, 19 killed / 20+ hurt."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#DDD0B6")
    d = ImageDraw.Draw(img)

    eth = [(128, 0), (188, 0), (188, 54), (120, 54), (134, 36), (136, 18)]
    d.polygon([(x * S, y * S) for x, y in eth], fill="#CEC1A6", outline="#958870", width=S)

    bn = [(72, 23), (126, 17), (134, 34), (118, 48), (80, 46)]
    d.polygon([(x * S, y * S) for x, y in bn], fill="#DBB27D", outline="#A2743D", width=S)

    river = [(164, 48), (144, 42), (126, 36), (108, 30), (92, 22), (76, 12), (62, 0)]
    d.line([(x * S, y * S) for x, y in river], fill="#347CAE", width=int(2.4 * S))

    dx, dy = 106 * S, 29 * S
    d.ellipse([dx - 6.5 * S, dy - 6.5 * S, dx + 6.5 * S, dy + 6.5 * S], outline="#B3261E", width=int(1.1 * S))
    d.ellipse([dx - 3.2 * S, dy - 3.2 * S, dx + 3.2 * S, dy + 3.2 * S], fill="#B3261E", outline="#FFFFFF", width=max(1, int(0.7 * S)))

    d.text((8 * S, 5 * S), "S U D A N", fill="#4D4335", font=_f("NotoSans-Bold.ttf", 7.6))
    d.text((138 * S, 20 * S), "ETHIOPIA", fill="#5E5443", font=_f("NotoSans-CondensedBold.ttf", 6.4))
    d.text((14 * S, 24 * S), "BLUE NILE", fill="#784712", font=_f("NotoSans-CondensedBold.ttf", 7.0))
    d.text((117 * S, 29 * S), "DAMAZIN", fill="#8F1D17", font=_f("NotoSans-CondensedBold.ttf", 7.0))

    _ribbon(d, 6, 40, 108, 51, "19 KILLED  ·  20+ HURT", bg="#1C212A", fg="#F8F4EC", font_sz=6.6, radius=1.5)
    return _finish(img, w, h)


def panel_10(w=188, h=54):
    """Card 10 (LIGHT): Rosstat/BBC archival ledger bar diagram (490,334 vs 700,000+ missing)."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#D4CCB9")
    d = ImageDraw.Draw(img)

    x_base, x_max = 8, 178
    for val, lbl in [(0, "0"), (250, "250k"), (500, "500k"), (750, "750k")]:
        xx = (x_base + (x_max - x_base) * (val / 750.0)) * S
        d.line([(xx, 14 * S), (xx, 45 * S)], fill="#C7BEAC", width=1)
        d.text((xx - (4 if val else 0) * S, 45.5 * S), lbl, fill="#524B42", font=_f("NotoSans-CondensedBold.ttf", 5.8))

    d.text((7 * S, 3.5 * S), "ROSSTAT / BBC RECORDS", fill="#2B2721", font=_f("NotoSans-CondensedBold.ttf", 6.7))

    b1_w = (x_max - x_base) * (490.334 / 750.0)
    d.rectangle([x_base * S, 16 * S, (x_base + b1_w) * S, 27 * S], fill="#B3261E")
    d.text(((x_base + 3) * S, 17.3 * S), "490,334 CONFIRMED DEAD", fill="#FFFFFF", font=_f("NotoSans-CondensedBold.ttf", 6.8))

    b2_w = (x_max - x_base) * (700.0 / 750.0)
    d.rectangle([x_base * S, 31 * S, (x_base + b1_w) * S, 42 * S], fill="#2E3440")
    d.rectangle([(x_base + b1_w) * S, 31 * S, (x_base + b2_w) * S, 42 * S], fill="#667080", outline="#2E3440", width=max(1, int(0.7 * S)))
    hx = x_base + b1_w + 3
    while hx < x_base + b2_w - 2:
        d.line([(hx * S, 41.5 * S), ((hx + 6) * S, 31.5 * S)], fill="#3B4252", width=max(1, int(0.8 * S)))
        hx += 5
    d.text(((x_base + 3) * S, 32.3 * S), "700,000+ WITH MISSING (EST.)", fill="#FFFFFF", font=_f("NotoSans-CondensedBold.ttf", 6.6))

    return _finish(img, w, h)


def panel_11(w=188, h=54):
    """Card 11 (DARK #4): Orbital diagram — Tiangong station + Shenzhou-24 capsule over Earth limb."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#0F182A")
    d = ImageDraw.Draw(img)

    for (sx, sy) in [(16, 10), (42, 7), (76, 12), (112, 8), (128, 22), (168, 24), (176, 36), (62, 25), (28, 20)]:
        d.ellipse([sx * S - 0.8 * S, sy * S - 0.8 * S, sx * S + 0.8 * S, sy * S + 0.8 * S], fill="#93AED6")

    d.ellipse([-44 * S, 26 * S, 118 * S, 148 * S], fill="#1D5488", outline="#76D0FA", width=int(1.7 * S))
    d.pieslice([-36 * S, 32 * S, 108 * S, 140 * S], start=235, end=275, fill="#2F6E56")
    d.text((6 * S, 42 * S), "JIUQUAN", fill="#C8EAFA", font=_f("NotoSans-CondensedBold.ttf", 6.1))

    orbit_pts = []
    for i in range(18):
        t = i / 17.0
        ox = 18 + t * 138
        oy = 44 - math.sin(t * math.pi * 0.72) * 28
        orbit_pts.append((ox * S, oy * S))
    _dashed_polyline(d, orbit_pts, "#8AC2EC", 1.1, dash=3, gap=2.5)

    tx, ty = 104 * S, 19 * S
    d.rectangle([tx - 11 * S, ty - 2 * S, tx + 11 * S, ty + 2 * S], fill="#EEF3FA")
    for sx_off in (-7, 7):
        d.rectangle([tx + (sx_off - 2.2) * S, ty - 11 * S, tx + (sx_off + 2.2) * S, ty - 2.5 * S], fill="#4DA6EB", outline="#C2E4FC", width=max(1, int(0.6 * S)))
        d.rectangle([tx + (sx_off - 2.2) * S, ty + 2.5 * S, tx + (sx_off + 2.2) * S, ty + 11 * S], fill="#4DA6EB", outline="#C2E4FC", width=max(1, int(0.6 * S)))
    d.text((84 * S, 2.5 * S), "TIANGONG", fill="#C4DDF7", font=_f("NotoSans-CondensedBold.ttf", 6.2))

    cx, cy = 67 * S, 24 * S
    d.polygon([(cx + 6 * S, cy), (cx + 1 * S, cy - 2.5 * S), (cx - 5 * S, cy - 2.5 * S), (cx - 5 * S, cy + 2.5 * S), (cx + 1 * S, cy + 2.5 * S)], fill="#F6C453")
    d.line([(cx - 1 * S, cy - 6.5 * S), (cx - 1 * S, cy + 6.5 * S)], fill="#88CEFA", width=int(1.2 * S))
    d.text((40 * S, 15 * S), "SZ-24", fill="#F6C453", font=_f("NotoSans-CondensedBold.ttf", 6.0))

    _ribbon(d, 86, 40, 182, 51, "08:18 CST  ·  CREW OF 3", bg="#E5A93B", fg="#111827", font_sz=6.5, radius=1.5)
    return _finish(img, w, h)


def panel_12(w=188, h=54):
    """Card 12 (LIGHT): SW Pacific map (Australia + Solomon Islands), two flags, NO FOREIGN BASE."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#A8CCE2")
    d = ImageDraw.Draw(img)

    aus = [(0, 26), (18, 22), (32, 16), (40, 22), (52, 34), (66, 48), (68, 54), (0, 54)]
    d.polygon([(x * S, y * S) for x, y in aus], fill="#DACBA8", outline="#8F856F", width=S)
    png = [(20, 0), (54, 0), (74, 8), (66, 12), (42, 8), (22, 6)]
    d.polygon([(x * S, y * S) for x, y in png], fill="#CFC09F", outline="#8F856F", width=max(1, int(0.7 * S)))

    sol_islands = [
        [(102, 14), (112, 18), (110, 21), (100, 17)],
        [(114, 20), (124, 24), (122, 27), (112, 23)],
        [(125, 25), (133, 29), (131, 31), (123, 27)],
    ]
    for isl in sol_islands:
        d.polygon([(x * S, y * S) for x, y in isl], fill="#246E28", outline="#154217", width=max(1, int(0.8 * S)))

    arc_pts = [(48 * S, 36 * S), (72 * S, 26 * S), (96 * S, 22 * S), (114 * S, 22 * S)]
    _dashed_polyline(d, arc_pts, "#185E37", 1.6, dash=4, gap=2.5)

    ax, ay, aw, ah = 7 * S, 34 * S, 26 * S, 15 * S
    d.rectangle([ax, ay, ax + aw, ay + ah], fill="#0C2C6E", outline="#FFFFFF", width=max(1, int(0.7 * S)))
    d.rectangle([ax, ay, ax + aw * 0.48, ay + ah * 0.5], fill="#0C2C6E")
    d.line([(ax, ay), (ax + aw * 0.48, ay + ah * 0.5)], fill="#FFFFFF", width=max(1, int(0.8 * S)))
    d.line([(ax + aw * 0.48, ay), (ax, ay + ah * 0.5)], fill="#FFFFFF", width=max(1, int(0.8 * S)))
    d.line([(ax + aw * 0.24, ay), (ax + aw * 0.24, ay + ah * 0.5)], fill="#D1262D", width=max(1, int(1.2 * S)))
    d.line([(ax, ay + ah * 0.25), (ax + aw * 0.48, ay + ah * 0.25)], fill="#D1262D", width=max(1, int(1.2 * S)))
    for sx, sy in [(0.74, 0.28), (0.86, 0.48), (0.74, 0.72), (0.64, 0.48)]:
        d.ellipse([ax + aw * sx - S, ay + ah * sy - S, ax + aw * sx + S, ay + ah * sy + S], fill="#FFFFFF")

    bx, by, bw, bh = 150 * S, 19 * S, 26 * S, 15 * S
    d.polygon([(bx, by), (bx + bw, by), (bx, by + bh)], fill="#1D56A8")
    d.polygon([(bx + bw, by), (bx + bw, by + bh), (bx, by + bh)], fill="#247A3C")
    d.line([(bx, by + bh), (bx + bw, by)], fill="#F4C427", width=int(2.2 * S))
    for sx, sy in [(0.16, 0.22), (0.34, 0.22), (0.25, 0.38)]:
        d.ellipse([bx + bw * sx - 0.8 * S, by + bh * sy - 0.8 * S, bx + bw * sx + 0.8 * S, by + bh * sy + 0.8 * S], fill="#FFFFFF")
    d.rectangle([bx, by, bx + bw, by + bh], outline="#FFFFFF", width=max(1, int(0.7 * S)))

    d.text((6 * S, 24 * S), "AUS", fill="#4D4539", font=_f("NotoSans-CondensedBold.ttf", 6.2))
    d.text((88 * S, 6 * S), "SOLOMON IS.", fill="#164A1B", font=_f("NotoSans-CondensedBold.ttf", 6.5))
    _ribbon(d, 90, 40, 182, 51, "NO FOREIGN BASE", bg="#174528", fg="#F8F4EC", font_sz=6.6, radius=1.5)
    return _finish(img, w, h)


def panel_13(w=188, h=54):
    """Card 13 (LIGHT): Cartagena coastal storefront scene, police cordon, ALL HOSTAGES FREE."""
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#A2C8DE")
    d = ImageDraw.Draw(img)

    d.rectangle([0, 32 * S, 76 * S, 41 * S], fill="#4C96BA")
    d.rectangle([0, 40 * S, W, H], fill="#C7B394")

    d.line([(20 * S, 41 * S), (16 * S, 20 * S)], fill="#6E553A", width=int(1.9 * S))
    for ang in (-150, -110, -50, -10, 20):
        rad = math.radians(ang)
        d.line([(16 * S, 20 * S), (16 * S + 11 * S * math.cos(rad), 20 * S + 7 * S * math.sin(rad))], fill="#286835", width=int(1.4 * S))

    d.rectangle([48 * S, 16 * S, 146 * S, 41 * S], fill="#E4BE7B", outline="#96733D", width=S)
    roof = [(44, 16), (52, 8), (142, 8), (150, 16)]
    d.polygon([(x * S, y * S) for x, y in roof], fill="#AD4027", outline="#7A2815", width=S)
    _text_centered(d, 97 * S, 18.2 * S, "SUPERMERCADO", _f("NotoSans-CondensedBold.ttf", 4.6), "#6E351A")
    for i in range(10):
        ax0 = (54 + i * 8.6) * S
        col = "#C4362C" if i % 2 == 0 else "#FBF8F1"
        d.rectangle([ax0, 21 * S, ax0 + 8.6 * S, 27 * S], fill=col)
    d.rectangle([54 * S, 21 * S, 140 * S, 27 * S], outline="#8E382E", width=max(1, int(0.6 * S)))
    d.rectangle([88 * S, 28 * S, 106 * S, 41 * S], fill="#246340", outline="#163D27", width=S)
    d.rectangle([60 * S, 29 * S, 80 * S, 37 * S], fill="#9EC3D6", outline="#8E7550", width=max(1, int(0.7 * S)))
    d.rectangle([114 * S, 29 * S, 134 * S, 37 * S], fill="#9EC3D6", outline="#8E7550", width=max(1, int(0.7 * S)))

    d.line([(4 * S, 44 * S), (84 * S, 44 * S)], fill="#F2C94C", width=int(2.1 * S))
    for tx in range(8, 82, 10):
        d.line([(tx * S, 43 * S), ((tx + 3) * S, 45 * S)], fill="#1E2024", width=S)

    d.text((6 * S, 4 * S), "CARTAGENA", fill="#2E4150", font=_f("NotoSans-CondensedBold.ttf", 6.6))
    _ribbon(d, 86, 40, 182, 51, "ALL HOSTAGES FREE", bg="#175434", fg="#F8F4EC", font_sz=6.5, radius=1.5)
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
