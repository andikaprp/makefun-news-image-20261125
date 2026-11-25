"""Cartographic world map renderer with accurate continent polygons and collision-resolved pins."""
import math
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/noto/"

# Simplified but recognizable Natural-Earth-faithful world land polygons (lon, lat)
CONTINENTS = [
    # North America
    [(-168, 66), (-162, 70), (-140, 70), (-125, 70), (-110, 68), (-95, 68), (-82, 64),
     (-78, 53), (-64, 52), (-55, 52), (-60, 45), (-67, 44), (-71, 41), (-76, 35),
     (-81, 25), (-83, 29), (-90, 29), (-97, 26), (-97, 19), (-90, 21), (-87, 16),
     (-83, 10), (-78, 8), (-83, 9), (-88, 13), (-95, 16), (-105, 20), (-110, 24),
     (-114, 31), (-118, 34), (-124, 41), (-125, 49), (-135, 57), (-150, 60), (-162, 56), (-166, 61)],
    # Greenland
    [(-52, 60), (-42, 61), (-33, 68), (-20, 74), (-18, 81), (-38, 83), (-55, 81), (-68, 76), (-56, 70)],
    # Cuba / Hispaniola
    [(-85, 22), (-79, 23), (-74, 20), (-81, 20)],
    # South America
    [(-78, 9), (-72, 11), (-62, 10), (-50, 2), (-40, -3), (-35, -7), (-38, -14),
     (-41, -22), (-48, -26), (-54, -35), (-62, -39), (-66, -44), (-68, -54),
     (-74, -52), (-74, -40), (-71, -30), (-70, -18), (-77, -12), (-81, -5), (-79, 2)],
    # Europe + Scandinavia + Russia (Eurasia continuous landmass)
    [(-9, 37), (-9, 43), (-2, 43), (-4, 48), (2, 51), (8, 54), (10, 57), (15, 55),
     (21, 56), (24, 60), (21, 65), (28, 70), (15, 68), (10, 63), (5, 60), (11, 58),
     (18, 60), (25, 66), (31, 70), (42, 68), (58, 70), (72, 73), (95, 76), (115, 74),
     (138, 72), (165, 69), (178, 66), (170, 60), (160, 56), (157, 51), (141, 53),
     (135, 44), (129, 35), (126, 38), (122, 40), (118, 38), (122, 31), (118, 24),
     (108, 21), (109, 12), (104, 10), (100, 14), (104, 2), (100, 6), (97, 16),
     (90, 22), (82, 16), (78, 8), (73, 19), (68, 23), (60, 25), (56, 27), (50, 29),
     (56, 23), (59, 22), (52, 16), (44, 13), (40, 20), (35, 29), (33, 31), (36, 36),
     (28, 37), (26, 41), (23, 37), (19, 41), (14, 45), (16, 40), (12, 42), (8, 44),
     (3, 42), (-5, 36)],
    # UK & Ireland
    [(-6, 50), (1, 51), (1, 55), (-3, 58), (-6, 57), (-5, 53)],
    [(-10, 52), (-6, 52), (-6, 55), (-9, 55)],
    # Iceland
    [(-24, 64), (-14, 64), (-15, 66), (-23, 66)],
    # Africa
    [(-17, 15), (-13, 28), (-6, 36), (3, 37), (11, 37), (12, 33), (20, 32), (25, 32),
     (32, 31), (35, 25), (40, 16), (43, 12), (51, 12), (48, 5), (41, -2), (40, -11),
     (35, -20), (32, -26), (27, -33), (18, -34), (15, -26), (12, -16), (12, -6),
     (9, 4), (3, 6), (-8, 5), (-14, 10)],
    # Madagascar
    [(44, -25), (47, -25), (50, -13), (47, -15), (44, -20)],
    # Sri Lanka
    [(80, 9), (82, 7), (80, 6), (79, 8)],
    # Japan
    [(130, 31), (135, 34), (140, 36), (141, 41), (145, 44), (141, 45), (139, 40), (136, 37), (131, 34)],
    # Taiwan
    [(120.5, 22), (121.8, 25), (121.2, 25.3), (120.1, 23)],
    # Philippines
    [(120, 14), (122, 18), (123, 14), (126, 8), (123, 7), (121, 11)],
    # Sumatra / Java / Borneo / Sulawesi / New Guinea
    [(95, 5), (100, 1), (105, -6), (103, -6), (98, 0)],
    [(106, -6), (114, -8), (114, -7), (106, -5.5)],
    [(109, 1), (115, 5), (118, 5), (117, -3), (111, -3)],
    [(131, -2), (138, -3), (146, -7), (150, -10), (145, -9), (138, -8), (133, -4)],
    # Australia
    [(114, -22), (122, -18), (130, -12), (136, -12), (137, -16), (142, -11),
     (146, -18), (153, -26), (151, -35), (146, -38), (138, -35), (131, -32),
     (122, -34), (115, -34), (114, -28)],
    # Tasmania
    [(145, -41), (148, -41), (147, -43.5), (145, -43)],
    # New Zealand
    [(173, -35), (178, -38), (175, -41), (173, -39)],
    [(171, -41), (173, -43), (168, -46), (167, -45)],
    # Solomon Islands
    [(156, -7), (161, -9.5), (160, -10.2), (155.5, -7.8)],
]

# Projection bounds: lon [-165, 180], lat [-56, 76] (cuts Antarctica & high Arctic)
LON_MIN, LON_MAX = -165.0, 180.0
LAT_MIN, LAT_MAX = -56.0, 76.0


def project(lon, lat, w, h):
    """Natural-looking pseudocylindrical / Robinson-ish blend."""
    # Gentle horizontal compression at high latitudes for authentic atlas feel
    lat_rad = math.radians(max(-80, min(80, lat)))
    cos_scale = 0.88 + 0.12 * math.cos(lat_rad)
    mid_lon = (LON_MIN + LON_MAX) / 2.0
    nx = 0.5 + ((lon - mid_lon) / (LON_MAX - LON_MIN)) * cos_scale
    ny = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN)
    return nx * w, ny * h


def resolve_pin_collisions(pins, min_dist):
    """Iterative spring repulsion so numbered map pins never overlap."""
    pts = [[p["x"], p["y"]] for p in pins]
    for _ in range(60):
        moved = False
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                d = math.hypot(dx, dy)
                if d < min_dist:
                    if d < 0.01:
                        dx, dy, d = 1.0, 0.5, 1.118
                    push = (min_dist - d) * 0.52
                    ux, uy = dx / d, dy / d
                    pts[i][0] -= ux * push
                    pts[i][1] -= uy * push
                    pts[j][0] += ux * push
                    pts[j][1] += uy * push
                    moved = True
        if not moved:
            break
    return pts


def render_world_map(w, h, cards, region_colors):
    """Render crisp 3x supersampled world map with region-colored numbered pins."""
    S = 3
    W, H = w * S, h * S
    img = Image.new("RGB", (W, H), "#B2CFE2")
    draw = ImageDraw.Draw(img)

    # Subtle cartographic graticule
    for lat in (-30, 0, 30, 60):
        pts = [project(lon, lat, W, H) for lon in range(-160, 181, 10)]
        col = "#9ABBD2" if lat == 0 else "#A5C4D8"
        draw.line(pts, fill=col, width=1 * S if lat == 0 else max(1, S // 2))
    for lon in (-120, -60, 0, 60, 120):
        pts = [project(lon, lat, W, H) for lat in range(-55, 76, 5)]
        draw.line(pts, fill="#A5C4D8", width=max(1, S // 2))

    # Draw continents
    for poly in CONTINENTS:
        pts = [project(lon, lat, W, H) for lon, lat in poly]
        draw.polygon(pts, fill="#D1C1A2", outline="#8A7E68", width=max(1, int(0.8 * S)))

    # Project pins and resolve collisions cleanly
    pin_data = []
    for c in cards:
        px, py = project(c["lon"], c["lat"], W, H)
        pin_data.append({
            "num": c["num"],
            "region": c["region"],
            "ox": px,
            "oy": py,
            "x": px,
            "y": py,
        })

    r_pin = int(6.6 * S)
    resolved = resolve_pin_collisions(pin_data, min_dist=r_pin * 2.15)

    # Clamp inside margins
    pad = r_pin + 2 * S
    for p, (rx, ry) in zip(pin_data, resolved):
        p["x"] = max(pad, min(W - pad, rx))
        p["y"] = max(pad, min(H - pad, ry))

    # Draw subtle leader ticks if a pin moved notably
    for p in pin_data:
        if math.hypot(p["x"] - p["ox"], p["y"] - p["oy"]) > r_pin * 1.1:
            draw.line([(p["ox"], p["oy"]), (p["x"], p["y"])], fill="#6C685F", width=max(1, int(0.8 * S)))
            draw.ellipse([p["ox"] - 1.5 * S, p["oy"] - 1.5 * S, p["ox"] + 1.5 * S, p["oy"] + 1.5 * S], fill="#5C574F")

    # Draw pins with crisp white halo + bold white numeral
    font_1d = ImageFont.truetype(FONT_DIR + "NotoSans-Bold.ttf", int(8.2 * S))
    font_2d = ImageFont.truetype(FONT_DIR + "NotoSans-CondensedBold.ttf", int(7.8 * S))
    for p in pin_data:
        cx, cy = p["x"], p["y"]
        fill_col = region_colors[p["region"]]["fill"]
        halo = int(1.0 * S)
        draw.ellipse([cx - r_pin - halo, cy - r_pin - halo, cx + r_pin + halo, cy + r_pin + halo], fill="#FFFFFF")
        draw.ellipse([cx - r_pin, cy - r_pin, cx + r_pin, cy + r_pin], fill=fill_col)
        txt = str(p["num"])
        fnt = font_1d if len(txt) == 1 else font_2d
        bbox = draw.textbbox((0, 0), txt, font=fnt)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), txt, fill="#FFFFFF", font=fnt)

    out = img.resize((w, h), Image.Resampling.LANCZOS)
    # Crisp 1px hairline border
    od = ImageDraw.Draw(out)
    od.rectangle([0, 0, w - 1, h - 1], outline="#C9C0B1", width=1)
    return out
