# Renders 20 Pinterest pin covers (1080x1350) with pure Python + PIL.
# No browser, no headless Edge. Fonts: Comic Sans MS (closest to Baloo 2 locally).
# Output: D:\проэкт\pins\covers\pin-01.png ... pin-20.png
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1080, 1350
OUT = r"D:\проэкт\pins\covers"
os.makedirs(OUT, exist_ok=True)

ORANGE = (255, 140, 66); ORANGE_D = (232, 104, 26); PURPLE = (123, 79, 166)
PURPLE_L = (183, 156, 224); CREAM = (255, 248, 231); INK = (45, 45, 45)
LIME = (168, 217, 72); YELLOW = (255, 209, 102); TEAL = (127, 216, 216)
PINK = (255, 181, 194)

F_TITLE = r"C:\Windows\Fonts\comicbd.ttf"
F_BODY = r"C:\Windows\Fonts\comic.ttf"
F_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

# (badge, line1, line2, emoji, bg, accent, tagline)
PINS = [
 ("DECOR",     "Cozy Pumpkin",      "Porch Vibes",        "🎃", CREAM,   ORANGE,  "Spooky-cute, not scary"),
 ("WALLPAPER", "Cute Black Cat",    "Wallpaper",          "🐱", (46,42,58), PURPLE_L, "Save it for your phone"),
 ("MAGIC",     "Witch Hat &",       "Full Moon Night",    "🧙‍♀️", (239,231,251), PURPLE, "Purple moonlight vibes"),
 ("DIY",       "Friendly DIY",      "Graveyard Ideas",    "🪦", (234,246,233), (95,160,51), "Crafts for the whole yard"),
 ("PATTERN",   "Candy Corn",        "Repeat Pattern",     "🍬", CREAM,   ORANGE,  "Sweet & seamless"),
 ("COSTUMES",  "20+ Costume",       "Ideas for Adults",   "🎭", (46,42,58), PURPLE_L, "Spooky-cute looks"),
 ("WALLPAPER", "Haunted House",     "Silhouette Night",   "🏚️", (239,231,251), PURPLE, "Cozy dark-mode vibes"),
 ("PARTY",     "Trick or Treat",    "Skeleton Hand",      "💀", (255,241,216), ORANGE, "Fun & a little silly"),
 ("COZY",      "Pumpkin Spice",     "Latte Aesthetic",    "☕", CREAM,   (201,123,45), "Fall in a cup"),
 ("CLASSIC",   "Bat Meets",         "Jack-O-Lantern",     "🦇", (46,42,58), PURPLE_L, "Best Halloween duo"),
 ("CUTE",      "Ghost Blowing",     "Kisses — BOO!",      "👻", (239,231,251), PURPLE, "The sweetest little ghost"),
 ("DIY",       "Easy Spider",       "Web Craft",          "🕷️", (234,246,233), (95,160,51), "Simple & fun for kids"),
 ("DECOR",     "Vintage Trick",     "or Treat Sign",      "🪧", (255,241,216), ORANGE, "Rustic porch charm"),
 ("SPOOKY",    "Vampire Teeth",     "Close-Up",           "🧛", (46,42,58), PURPLE_L, "Classic fangs, cute style"),
 ("TEMPLATE",  "Halloween Party",   "Invitation",         "📨", (239,231,251), PURPLE, "Printable & pretty"),
 ("NIGHT",     "Witch Silhouette",  "& Big Moon",         "🌕", (234,246,233), (95,160,51), "Moonlit magic"),
 ("KIDS",      "Candy Corn",        "Family Craft",       "🍬", CREAM,   ORANGE,  "Googly-eye fun"),
 ("DIY",       "DIY Porch",         "Makeover Guide",     "🏡", (255,241,216), ORANGE, "Step by step ideas"),
 ("TUTORIAL",  "Funny Clown",       "Makeup Idea",        "🤡", (239,231,251), PURPLE, "Silly, not scary"),
 ("FREEBIE",   "50+ FREE",          "Halloween Printables", "🎁", CREAM,   ORANGE,  "Coloring, tags & games"),
]

def font(path, size):
    return ImageFont.truetype(path, size)

def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]

def draw_centered(d, cx, y, s, f, fill):
    d.text((cx - text_w(d, s, f) / 2, y), s, font=f, fill=fill)

def draw_highlight(d, cx, y, s, f, hl=YELLOW):
    """Title line with a soft yellow highlight behind it."""
    w = text_w(d, s, f)
    pad = 22
    x0, x1 = cx - w / 2 - pad, cx + w / 2 + pad
    r = 26
    d.rounded_rectangle([x0, y - 8, x1, y + 96], radius=r, fill=hl)
    draw_centered(d, cx, y + 6, s, f, PURPLE)

def draw_kawaii_face(d, cx, cy, s):
    """Friendly kawaii face: eyes, blush, smile — to glue onto any shape."""
    ew = s * 0.10
    for ex in (cx - s * 0.22, cx + s * 0.22):
        d.ellipse([ex - ew, cy - ew, ex + ew, cy + ew], fill=INK)
        d.ellipse([ex - ew * 0.45, cy - ew * 0.75, ex + ew * 0.15, cy - ew * 0.15], fill=(255, 255, 255))
    for bx in (cx - s * 0.38, cx + s * 0.38):
        d.ellipse([bx - s * 0.075, cy + s * 0.10, bx + s * 0.075, cy + s * 0.25], fill=PINK)
    d.arc([cx - s * 0.24, cy + s * 0.08, cx + s * 0.24, cy + s * 0.40], 20, 160, fill=INK, width=max(4, int(s * 0.035)))

def draw_pumpkin(d, cx, cy, s):
    d.ellipse([cx - s, cy - s * 0.82, cx + s, cy + s * 0.82], fill=ORANGE, outline=ORANGE_D, width=8)
    for k in (-0.55, 0, 0.55):
        d.line([cx + k * s, cy - s * 0.72, cx + k * s, cy + s * 0.72], fill=ORANGE_D, width=7)
    d.rounded_rectangle([cx - s * 0.09, cy - s * 1.0, cx + s * 0.09, cy - s * 0.78], radius=8, fill=(120, 180, 70))
    draw_kawaii_face(d, cx, cy, s)

def draw_ghost(d, cx, cy, s):
    d.ellipse([cx - s * 0.85, cy - s, cx + s * 0.85, cy + s * 0.1], fill=(255, 255, 255))
    d.rectangle([cx - s * 0.85, cy - s * 0.45, cx + s * 0.85, cy + s * 0.72], fill=(255, 255, 255))
    bw = s * 0.567
    for i in range(3):
        x = cx - s * 0.85 + i * bw
        d.pieslice([x, cy - s * 0.2, x + bw, cy + s * 0.85], 0, 180, fill=(255, 255, 255))
    d.ellipse([cx - s * 0.85, cy - s, cx + s * 0.85, cy + s * 0.1], outline=PURPLE, width=6)
    d.line([cx - s * 0.85, cy - s * 0.4, cx - s * 0.85, cy + s * 0.3], fill=PURPLE, width=6)
    d.line([cx + s * 0.85, cy - s * 0.4, cx + s * 0.85, cy + s * 0.3], fill=PURPLE, width=6)
    draw_kawaii_face(d, cx, cy - s * 0.25, s)

def draw_bat(d, cx, cy, s):
    d.polygon([(cx - s, cy - s * 0.5), (cx - s * 0.2, cy - s * 0.05), (cx - s * 0.55, cy + s * 0.35), (cx - s * 0.15, cy + s * 0.18)], fill=PURPLE)
    d.polygon([(cx + s, cy - s * 0.5), (cx + s * 0.2, cy - s * 0.05), (cx + s * 0.55, cy + s * 0.35), (cx + s * 0.15, cy + s * 0.18)], fill=PURPLE)
    d.ellipse([cx - s * 0.4, cy - s * 0.55, cx + s * 0.4, cy + s * 0.5], fill=PURPLE)
    d.polygon([(cx - s * 0.35, cy - s * 0.5), (cx - s * 0.5, cy - s * 0.95), (cx - s * 0.15, cy - s * 0.62)], fill=PURPLE)
    d.polygon([(cx + s * 0.35, cy - s * 0.5), (cx + s * 0.5, cy - s * 0.95), (cx + s * 0.15, cy - s * 0.62)], fill=PURPLE)
    draw_kawaii_face(d, cx, cy - s * 0.05, s * 0.9)

def draw_moon(d, cx, cy, s):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=YELLOW, outline=(224, 178, 55), width=7)
    draw_kawaii_face(d, cx, cy, s)

def draw_star(d, cx, cy, s, fill=YELLOW, rot=0):
    pts = []
    for i in range(10):
        ang = rot + i * math.pi / 5 - math.pi / 2
        r = s if i % 2 == 0 else s * 0.45
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=(224, 178, 55))

def draw_web(d, cx, cy, s, color=PURPLE_L):
    for ring in (0.35, 0.65, 1.0):
        d.ellipse([cx - s * ring, cy - s * ring, cx + s * ring, cy + s * ring], outline=color, width=5)
    for i in range(8):
        ang = i * math.pi / 4
        d.line([cx, cy, cx + s * math.cos(ang), cy + s * math.sin(ang)], fill=color, width=5)

def draw_candy(d, cx, cy, s):
    d.polygon([(cx, cy - s), (cx + s * 0.7, cy + s * 0.55), (cx - s * 0.7, cy + s * 0.55)], fill=ORANGE)
    d.line([cx, cy - s * 0.55, cx, cy + s * 0.55], fill=CREAM, width=9)
    d.polygon([(cx - s * 0.7, cy + s * 0.55), (cx, cy + s * 0.55), (cx, cy + s)], fill=YELLOW)
    draw_kawaii_face(d, cx, cy - s * 0.15, s * 0.7)

def draw_heart(d, cx, cy, s, color=PINK):
    d.ellipse([cx - s, cy - s * 0.6, cx, cy + s * 0.4], fill=color)
    d.ellipse([cx, cy - s * 0.6, cx + s, cy + s * 0.4], fill=color)
    d.polygon([(cx - s * 0.96, cy - s * 0.05), (cx + s * 0.96, cy - s * 0.05), (cx, cy + s)], fill=color)

# Art per pin: (draw_fn, scale, y_offset)
ART = {
 1: (draw_pumpkin, 1.0, 0),
 2: (draw_bat, 0.95, -10),
 3: (draw_moon, 0.95, -20),
 4: (draw_web, 1.0, 0),
 5: (draw_candy, 0.95, 0),
 6: (draw_ghost, 1.0, -10),
 7: (draw_moon, 0.9, 0),
 8: (draw_pumpkin, 0.95, 10),
 9: (draw_pumpkin, 0.9, 0),
 10: (draw_bat, 1.0, 0),
 11: (draw_ghost, 1.05, 0),
 12: (draw_web, 1.0, 0),
 13: (draw_pumpkin, 0.95, 0),
 14: (draw_bat, 0.95, 0),
 15: (draw_heart, 1.0, 0),
 16: (draw_moon, 1.0, -10),
 17: (draw_candy, 1.0, 0),
 18: (draw_pumpkin, 0.95, 0),
 19: (draw_star, 1.0, 0),
 20: (draw_heart, 1.0, 0),
}

DOTS = [LIME, YELLOW, TEAL, PINK, PURPLE_L, ORANGE]

def make(i, spec):
    badge, l1, l2, emoji, bg, accent, tagline = spec
    dark = bg == (46, 42, 58)
    fg = CREAM if dark else INK
    title_c = CREAM if dark else PURPLE
    card_bg = CREAM if dark else (255, 255, 255)
    sub_c = (232, 223, 201) if dark else (94, 90, 102)

    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    # dotted background texture
    dotcol = (255, 255, 255, 26) if dark else (123, 79, 166, 34)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for yy in range(0, H, 34):
        for xx in range(0, W, 34):
            od.ellipse([xx, yy, xx + 3, yy + 3], fill=dotcol)
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)

    # confetti dots
    spots = [(0.06, 0.10), (0.93, 0.08), (0.10, 0.88), (0.90, 0.90), (0.50, 0.055), (0.48, 0.94), (0.02, 0.50), (0.97, 0.52)]
    for j, (fx, fy) in enumerate(spots):
        s = [24, 20, 18, 24, 14, 14, 16, 16][j]
        c = DOTS[(i + j) % len(DOTS)]
        d.ellipse([fx * W - s, fy * H - s, fx * W + s, fy * H + s], fill=c)

    # number watermark
    f_num = font(F_BOLD, 40)
    d.text((W - 150, 40), f"{i+1:02d}/20", font=f_num, fill=(123, 79, 166, 120) if not dark else (183, 156, 224, 140))

    # badge pill
    f_badge = font(F_BOLD, 28)
    bw = text_w(d, badge, f_badge)
    d.rounded_rectangle([W / 2 - bw / 2 - 30, 130, W / 2 + bw / 2 + 30, 192], radius=31, fill=accent)
    draw_centered(d, W / 2, 147, badge, f_badge, (255, 255, 255))

    # art
    art_fn, sc, yoff = ART[i + 1]
    art_fn(d, W / 2, 640 + yoff, 240 * sc)

    # title (two lines, first one highlighted)
    f_t = font(F_TITLE, 92)
    draw_highlight(d, W / 2, 980, l1, f_t)
    draw_centered(d, W / 2, 1090, l2, f_t, title_c)

    # tagline
    f_tag = font(F_BODY, 44)
    draw_centered(d, W / 2, 1195, tagline, f_tag, accent if not dark else PURPLE_L)

    # bottom card
    d.rounded_rectangle([70, 1240, W - 70, H - 55], radius=28, fill=card_bg,
                        outline=(123, 79, 166, 60), width=3)
    f_brand = font(F_TITLE, 42)
    d.text((118, 1278), "Spooky Cute Printables", font=f_brand, fill=PURPLE)
    f_sub = font(F_BODY, 27)
    d.text((W - 118 - text_w(d, l1.replace("\n", " ") + " ideas →", f_sub), 1300),
           "swipe for ideas →", font=f_sub, fill=sub_c)

    img.save(os.path.join(OUT, f"pin-{i+1:02d}.png"), "PNG")
    return os.path.join(OUT, f"pin-{i+1:02d}.png")

for i, spec in enumerate(PINS):
    p = make(i, spec)
    print(f"pin-{i+1:02d}.png  {os.path.getsize(p)} bytes")
print("DONE")
