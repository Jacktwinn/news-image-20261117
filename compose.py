#!/usr/bin/env python3
"""Compose the entry image: a newspaper front page summing up 17 Nov 2026.

Hero illustration is AI-generated (media tool); every headline/deck is
rendered here with PIL so the text is pixel-crisp. Output: entry.png,
1024x1024, under 1 MiB.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (248, 245, 238)
INK = (17, 17, 17)
RED = (163, 18, 18)
GREY = (90, 86, 78)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
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

def draw_lines(draw, lines, fnt, x, y, max_w, fill, align="left", leading=None):
    leading = leading or int(fnt.size * 1.18)
    for ln in lines:
        if align == "center":
            draw.text((x + (max_w - draw.textlength(ln, font=fnt)) / 2, y), ln,
                      font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- Masthead ----
y = 10
f_mast = font(SERIF_B, 62)
d.text(((W - d.textlength("THE WORLD", font=f_mast)) / 2, y), "THE WORLD",
       font=f_mast, fill=INK)
y += 76
f_date = font(SANS_B, 18)
dateline = "TUESDAY, 17 NOVEMBER 2026  ·  THE DAY IN ONE PICTURE"
d.text(((W - d.textlength(dateline, font=f_date)) / 2, y), dateline,
       font=f_date, fill=RED)
y += 28
d.line([(24, y), (W - 24, y)], fill=INK, width=3)
y += 5
d.line([(24, y), (W - 24, y)], fill=INK, width=1)
y += 10

# ---- Hero image (center-crop to 1024x250) ----
hero = Image.open("hero-source.webp").convert("RGB")
hw, hh = hero.size
target_ratio = 1024 / 250
if hw / hh > target_ratio:
    nw = int(hh * target_ratio)
    x0 = (hw - nw) // 2
    hero = hero.crop((x0, 0, x0 + nw, hh))
else:
    nh = int(hw / target_ratio)
    y0 = (hh - nh) // 2
    hero = hero.crop((0, y0, hw, y0 + nh))
hero = hero.resize((1024, 250), Image.LANCZOS)
img.paste(hero, (0, y))
y += 250
y += 8
f_cap = font(SERIF, 17)
cap = ("The Kerch Bridge, partly collapsed into the sea after a Ukrainian "
       "strike — Zelensky called it “unprecedented”.")
cap_lines = wrap(d, cap, f_cap, 960)
y = draw_lines(d, cap_lines, f_cap, 32, y, 960, GREY, align="center", leading=21)
y += 6
d.line([(24, y), (W - 24, y)], fill=INK, width=1)
y += 12

# ---- Main headline ----
f_head = font(SERIF_B, 37)
head = "KERCH BRIDGE PARTIALLY COLLAPSES AFTER UKRAINE STRIKE"
head_lines = wrap(d, head, f_head, 960)
y = draw_lines(d, head_lines, f_head, 32, y, 960, INK, align="center", leading=44)
y += 4
f_deck = font(SANS, 19)
deck = ("Zelensky calls the strike “unprecedented”; Russia hits Kyiv’s "
        "Dnipro bridges in return.")
deck_lines = wrap(d, deck, f_deck, 920)
y = draw_lines(d, deck_lines, f_deck, 52, y, 920, INK, align="center", leading=24)
y += 10
d.line([(24, y), (W - 24, y)], fill=INK, width=1)
y += 14

# ---- Two columns of secondary stories ----
stories_left = [
    ("ASIA DIPLOMACY", "Trump in Manila, bound for Shenzhen",
     "First-ever Trump–Xi–Putin trilateral due Thursday at APEC."),
    ("GULF TENSIONS", "US strikes Iran missile site on Qeshm",
     "Iran fires drones at a US radar in Bahrain — third attack in five days."),
    ("MARKETS", "Bitcoin falls below $65,000", None),
]
stories_right = [
    ("HEALTH", "US loses measles-free status after 26 years",
     "5,400+ cases, 10 deaths."),
    ("TECH", "Nvidia’s bumper earnings amid spy scandal",
     "Huang not reinstated as US tightens chip-export curbs."),
    ("CULTURE", "Pattinson named the next James Bond", None),
]
col_w = 452
f_kick = font(SANS_B, 14)
f_sh = font(SERIF_B, 22)
f_sd = font(SANS, 16)

def draw_column(x, stories, y0):
    y = y0
    for kick, head, deck in stories:
        d.text((x, y), kick, font=f_kick, fill=RED)
        y += 20
        lines = wrap(d, head, f_sh, col_w)
        y = draw_lines(d, lines, f_sh, x, y, col_w, INK, leading=27)
        if deck:
            y += 2
            dlines = wrap(d, deck, f_sd, col_w)
            y = draw_lines(d, dlines, f_sd, x, y, col_w, (60, 58, 52), leading=20)
        y += 12
        d.line([(x, y), (x + col_w, y)], fill=(200, 194, 182), width=1)
        y += 12
    return y

y_left = draw_column(36, stories_left, y)
y_right = draw_column(536, stories_right, y)
y = max(y_left, y_right)

# ---- Bottom strip: ALSO ----
strip_h = H - y - 6
strip = Image.new("RGB", (W, strip_h), (20, 20, 20))
sd = ImageDraw.Draw(strip)
f_also = font(SANS_B, 15)
f_items = font(SANS, 15)
items = ("Gaza aid crossings plea as cold threatens camps  •  Depardieu "
         "pleads guilty in Paris  •  Epstein death was “murder”, says "
         "forensic expert  •  Japan scrambles jets over airspace violation"
         "  •  Houthis advance toward Aden  •  Russian military plane "
         "crash kills 19  •  Phuket fire kills 11  •  EU states plan "
         "Rwanda migrant hub")
lines = wrap(sd, items, f_items, W - 72)
yy = max(8, (strip_h - (20 + len(lines) * 19)) // 2)
sd.text((36, yy), "ALSO:", font=f_also, fill=(232, 90, 79))
yy += 20
for ln in lines:
    sd.text((36, yy), ln, font=f_items, fill=(240, 238, 232))
    yy += 19
img.paste(strip, (0, y + 6))

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
