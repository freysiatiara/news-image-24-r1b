#!/usr/bin/env python3
"""The World in One Day - Tuesday 24 November 2026.

Single-image front page generator (Pillow). Deterministic: no clock, no
randomness, no network. Reads nothing at runtime; every string is inlined
below so two runs are byte-identical.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (22, 21, 19)
RED = (166, 30, 30)
NAVY = (29, 78, 137)
TEAL = (15, 107, 92)
GOLD = (176, 128, 24)
GREY = (104, 100, 92)
LIGHT = (232, 226, 212)
WHITE = (255, 255, 255)
SKY = (186, 214, 232)
SEA = (46, 106, 150)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
MONO_B = lambda s: font("DejaVuSansMono-Bold.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)


def wrap(d, text, f, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, width, text, f, fill=INK, leading=None):
    """Draw wrapped paragraph; return y after last line."""
    lh = leading or int(f.size * 1.28)
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def rule(d, x0, x1, y, fill=INK, wdt=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def tag_chip(d, x, y, label, fill):
    f = MONO_B(13)
    tw = int(d.textlength(label, font=f)) + 16
    d.rounded_rectangle([x, y, x + tw, y + 22], radius=4, fill=fill)
    d.text((x + 8, y + 4), label, font=f, fill=WHITE)
    return tw


# ---------------------------------------------------------------- scenes
def scene_sea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=SEA)
    for i in range(5):  # wave lines
        yy = y + int(h * 0.60) + i * 9
        d.arc([x + 8 + i * 14, yy, x + 90 + i * 14, yy + 16], 200, 340, fill=WHITE, width=2)
    # corvette hull
    d.polygon([(x + w * 0.30, y + h * 0.52), (x + w * 0.78, y + h * 0.52),
               (x + w * 0.70, y + h * 0.66), (x + w * 0.38, y + h * 0.66)], fill=(60, 60, 62))
    d.rectangle([x + w * 0.44, y + h * 0.40, x + w * 0.56, y + h * 0.52], fill=(60, 60, 62))
    d.line([x + w * 0.50, y + h * 0.40, x + w * 0.50, y + h * 0.28], fill=(60, 60, 62), width=3)
    # smoke + flame
    for r, c in [(16, (90, 90, 90)), (11, (140, 140, 140)), (7, (230, 120, 40))]:
        d.ellipse([x + w * 0.60 - r, y + h * 0.30 - r, x + w * 0.60 + r, y + h * 0.30 + r], fill=c)
    # two sea drones
    for dx in (0.12, 0.86):
        cx, cy = x + w * dx, y + h * 0.80
        d.ellipse([cx - 12, cy - 5, cx + 12, cy + 5], fill=(30, 30, 30))
        d.line([cx - 18, cy - 12, cx - 8, cy - 4], fill=(30, 30, 30), width=2)
        d.line([cx + 8, cy - 4, cx + 18, cy - 12], fill=(30, 30, 30), width=2)


def scene_market(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 44))
    # falling bars
    vals = [0.92, 0.78, 0.86, 0.62, 0.70, 0.48, 0.55, 0.34]
    bw = w / len(vals)
    for i, v in enumerate(vals):
        bh = int(h * 0.72 * v)
        bx = x + i * bw + 6
        col = RED if i in (3, 7) else (214, 178, 60)
        d.rectangle([bx, y + h - 14 - bh, bx + bw - 12, y + h - 14], fill=col)
    d.line([x + 10, y + 16, x + w - 10, y + h * 0.55], fill=(235, 80, 70), width=4)
    d.text((x + 12, y + 8), "S&P -3.7%  ·  NASDAQ -5.3%", font=MONO_B(15), fill=WHITE)


def scene_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 34, 30))
    d.rectangle([x + w * 0.08, y + h * 0.55, x + w * 0.92, y + h * 0.92], fill=(88, 80, 70))
    for i in range(4):  # windows
        d.rectangle([x + w * (0.16 + i * 0.20), y + h * 0.62,
                     x + w * (0.28 + i * 0.20), y + h * 0.78], fill=(255, 176, 66))
    # flame
    d.polygon([(x + w * 0.42, y + h * 0.55), (x + w * 0.50, y + h * 0.18),
               (x + w * 0.58, y + h * 0.55)], fill=(235, 110, 30))
    d.polygon([(x + w * 0.46, y + h * 0.55), (x + w * 0.50, y + h * 0.34),
               (x + w * 0.54, y + h * 0.55)], fill=(255, 200, 60))
    d.text((x + 12, y + 8), "BANTEN  ·  SAT 21 NOV", font=MONO_B(15), fill=(255, 220, 160))


# ---------------------------------------------------------------- map
# Rough continent blobs as (cx, cy, rx, ry) in map-box coordinates.
BLOBS = [
    (150, 52, 95, 34),    # North America
    (210, 128, 42, 34),   # South America
    (470, 58, 62, 40),    # Europe
    (520, 130, 78, 52),   # Africa
    (700, 70, 120, 55),   # Asia
    (760, 165, 55, 30),   # SE Asia / Oceania
]


def in_land(px, py, sx=1.0, sy=1.0):
    for cx, cy, rx, ry in BLOBS:
        if ((px - cx * sx) / (rx * sx)) ** 2 + ((py - cy * sy) / (ry * sy)) ** 2 <= 1.0:
            return True
    return False


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 240, 244))
    d.rectangle([x, y, x + w, y + h], outline=GREY, width=1)
    sx, sy = w / 640.0, h / 190.0
    step = 11
    for gy in range(y + 8, y + h - 6, step):
        for gx in range(x + 8, x + w - 6, step):
            if in_land(gx - x, gy - y, sx, sy):
                d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=NAVY)
    pins = [
        ("1", 0.470, 0.60), ("2", 0.505, 0.26), ("3", 0.465, 0.10),
        ("4", 0.545, 0.30), ("5", 0.800, 0.62), ("6", 0.685, 0.42),
        ("7", 0.835, 0.30), ("8", 0.565, 0.40), ("9", 0.620, 0.38),
        ("10", 0.535, 0.62), ("11", 0.145, 0.55), ("12", 0.115, 0.28),
    ]
    for num, fx, fy in pins:
        cx, cy = x + int(w * fx), y + int(h * fy)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED, outline=WHITE, width=2)
        tf = SANS_B(13)
        tw = d.textlength(num, font=tf)
        d.text((cx - tw / 2, cy - 8), num, font=tf, fill=WHITE)
    return pins


# ---------------------------------------------------------------- data
NUMBERS = [
    ("24", "dead in Banten fire"),
    ("~30", "missing, 300 workers"),
    ("7", "sea drones, Benghazi"),
    ("-5.8%", "KOSPI, Mon 23 Nov"),
    ("$8bn", "Seoul stabilisation fund"),
    ("8", "India–Nepal MoUs"),
    ("128", "Pant, India–NZ Test"),
    ("+8.7%", "Nvidia, Mon 23 Nov"),
]

HEROES = [
    ("REPORTED", RED, scene_sea,
     "UKRAINE DRONES SINK RUSSIAN WARSHIP IN LIBYA",
     "Seven sea drones sank the corvette Merkury at Benghazi on Sunday; "
     "Zelenskyy confirmed it on Monday. A Ka-27 helicopter was lost and "
     "MV Angara was hit."),
    ("REPORTED", NAVY, scene_market,
     "THE AI ROUT DEEPENS — THEN NVIDIA BOUNCES",
     "The S&P 500 fell 3.7% on Friday into correction; the Nasdaq slid 5.3%, "
     "off 20% from its peak. Seoul's KOSPI fell 5.8% on Monday; Nvidia rose 8.7%."),
    ("REPORTED", TEAL, scene_fire,
     "24 DEAD IN BANTEN CANDY-FACTORY FIRE",
     "The blaze tore through a candy factory in Banten on Saturday. Rescuers "
     "still search for around 30 missing workers of about 300 on site; 24 are dead."),
]

SECONDARY = [
    ("ONGOING", GOLD,
     "COP31 ENDS WITH NO FOSSIL-FUEL DEAL",
     "Talks in Antalya closed Sunday with no fossil-fuel deal. The EU and "
     "Panama rejected the draft; Pacific nations voiced despair."),
    ("REPORTED", NAVY,
     "INDIA–NEPAL: 8 DEALS, A NEW TRAIN, A BIG PACKAGE",
     "Modi and Nepal's Balen Shah signed 8 MoUs on Monday, flagged off the "
     "Saryu-Kamala Express and agreed a Rs 15,000 crore package."),
]

ALSO = [
    ("EUROPE", "NATO to send AWACS jets to Poland after 3 missiles land."),
    ("ASIA", "Seoul: brief evacuation alert as Russian jet enters airspace."),
    ("EUROPE", "EU proposes 22nd Russia sanctions package, banks targeted."),
    ("MIDDLE EAST", "Israeli strikes kill 3 in Gaza, incl. a UN agency worker."),
    ("N. AMERICA", "Mexico captures drug lord 'Chapo Isidro' with US help."),
    ("EUROPE", "Dymer strike: 15 missing after Russian attack on Kyiv region."),
    ("EUROPE", "Sparta II still burning off Finland after drone strike."),
    ("EUROPE", "Estonia to shut land borders with Russia."),
    ("EUROPE", "Spain drops Puigdemont charges; Lisbon marches on prices."),
    ("EUROPE", "Acropolis Museum reopens in Athens after ~20 years."),
    ("ASIA", "Seoul names new foreign minister and spy chief."),
    ("ASIA", "China sets 2030 elderly-care and childcare targets."),
    ("ASIA", "Dhaka vows to arrest Hasina if she returns; typhoid jabs."),
    ("ASIA", "SpiceJet crisis: pilots urge Delhi to act; Taiwan +2.1%."),
    ("ASIA", "Tajikistan tells UN it will quit the ICC as Putin visits."),
    ("N. AMERICA", "Two killed in shooting at a US university."),
    ("MIDDLE EAST", "Trump warns Iran of 'very traumatic' outcome."),
    ("N. AMERICA", "Carney laughs off Trump lookalike; US tightens H-1B."),
    ("MIDDLE EAST", "Iran's Guards claim radar strikes on US bases in Bahrain."),
    ("AFRICA", "UN seeks probe into Libya attack; 24 killed in S. Sudan raid."),
    ("ASIA", "Myanmar junta slams ASEAN decision."),
    ("SPORT", "Verstappen wins Las Vegas GP; Alcaraz takes ATP Finals."),
    ("SPORT", "Pant 128 as India–NZ 1st Test ends in a draw."),
    ("SPORT", "Ferrari unveils 296 Challenge Stradale; Gukesh defends title."),
    ("TECH", "Nvidia faces SEC, California probes on China chip sales."),
    ("TECH", "Waymo pulls driverless taxis from US freeways."),
]

PIN_LEGEND = [
    "1 Benghazi — Merkury sunk",
    "2 Dymer, Kyiv region",
    "3 Poland — missiles land",
    "4 Antalya — COP31",
    "5 Banten factory fire",
    "6 Delhi–Kathmandu",
    "7 Seoul — KOSPI slide",
    "8 Gaza strikes",
    "9 Tehran — US bases row",
    "10 Juba — camp raid",
    "11 Mexico City — cartel arrest",
    "12 Las Vegas GP",
]

DATE_CHECK = (
    "DATE CHECK — Merkury sunk Sun 22 Nov, confirmed Mon 23 Nov · COP31 ended Sun 22 Nov · "
    "Banten fire Sat 21 Nov, toll 24 on Mon 23 Nov · India–Nepal, KOSPI, Nvidia: Mon 23 Nov · "
    "NATO AWACS, Korea warning: Tue 24 Nov."
)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- masthead
    rule(d, M, W - M, 14, wdt=4)
    d.text((M, 26), "THE WORLD IN ONE DAY", font=SERIF_B(64), fill=INK)
    d.text((M, 96), "TUESDAY 24 NOVEMBER 2026", font=SANS_B(30), fill=RED)
    right = "No. 329  ·  31 STORIES  ·  7 REGIONS"
    d.text((W - M - d.textlength(right, font=MONO_B(15)), 108), right,
           font=MONO_B(15), fill=GREY)
    rule(d, M, W - M, 140, wdt=2)
    d.text((M, 148), "One page. One day. Everything that mattered — AP · Reuters · BBC · Bloomberg · ANI, 22–24 Nov.",
           font=SERIF(17), fill=GREY)

    # ---- numbers strip
    y = 176
    cw = (W - 2 * M) / len(NUMBERS)
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * cw
        d.text((x + 4, y), num, font=SANS_B(26), fill=RED if i % 2 == 0 else NAVY)
        para(d, x + 4, y + 34, cw - 10, lab, SANS(12), fill=GREY, leading=14)
        if i:
            d.line([(x, y + 2), (x, y + 56)], fill=LIGHT, width=2)
    rule(d, M, W - M, y + 62, fill=GREY, wdt=1)

    # ---- heroes
    y = 246
    hw = (W - 2 * M - 2 * 16) / 3
    for i, (tag, col, scene, head, deck) in enumerate(HEROES):
        x = M + i * (hw + 16)
        scene(d, int(x), y, int(hw), 96)
        tag_chip(d, int(x), y + 102, tag, col)
        yy = para(d, int(x), y + 132, int(hw), head, SERIF_B(18), leading=22)
        para(d, int(x), yy + 4, int(hw), deck, SANS(13), fill=(52, 50, 46), leading=16)

    # ---- secondary
    y = 498
    sw = (W - 2 * M - 16) / 2
    for i, (tag, col, head, deck) in enumerate(SECONDARY):
        x = M + i * (sw + 16)
        tag_chip(d, int(x), y, tag, col)
        yy = para(d, int(x), y + 28, int(sw), head, SERIF_B(18), leading=21)
        para(d, int(x), yy + 4, int(sw), deck, SANS(13), fill=(52, 50, 46), leading=16)
    rule(d, M, W - M, 610, fill=GREY, wdt=1)

    # ---- map + legend
    y = 618
    d.text((M, y), "WHERE IT HAPPENED", font=SANS_B(16), fill=INK)
    d.text((W - M - d.textlength("DOTTED MAP — 12 PINS", font=MONO(13)), y + 2),
           "DOTTED MAP — 12 PINS", font=MONO(13), fill=GREY)
    map_w, map_h = 640, 130
    draw_map(d, M, y + 22, map_w, map_h)
    lx = M + map_w + 16
    for i, item in enumerate(PIN_LEGEND):
        yy = y + 24 + i * 12
        d.text((lx, yy), item, font=SANS(11), fill=INK)

    # ---- also today
    y = 796
    rule(d, M, W - M, y, fill=INK, wdt=2)
    d.text((M, y + 8), "ALSO TODAY", font=SANS_B(16), fill=INK)
    d.text((W - M - d.textlength("26 MORE STORIES", font=MONO_B(13)), y + 10),
           "26 MORE STORIES", font=MONO_B(13), fill=RED)
    col_w = (W - 2 * M - 16) / 2
    half = (len(ALSO) + 1) // 2
    for ci, chunk in enumerate([ALSO[:half], ALSO[half:]]):
        x = M + ci * (col_w + 16)
        yy = y + 28
        for region, text in chunk:
            d.text((x, yy), "▪", font=SANS_B(11), fill=RED)
            d.text((x + 13, yy), region, font=MONO_B(10), fill=NAVY)
            tw = d.textlength(region, font=MONO_B(10))
            yy = para(d, x + 13 + tw + 7, yy, col_w - 13 - tw - 7, text, SANS(11),
                      fill=(52, 50, 46), leading=11)

    # ---- footer / date check
    fy = 982
    d.rounded_rectangle([M, fy, W - M, fy + 32], radius=6, outline=RED, width=2)
    para(d, M + 10, fy + 4, W - 2 * M - 20, DATE_CHECK, SANS(11), fill=INK, leading=13)
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
