# Generates 20 Pinterest pin covers (1080x1350) — Spooky Cute Printables style.
# Output: ./covers/pin-01.png ... pin-20.png  (rendered by headless Edge)
import os, re, html, subprocess, sys, json

OUT_HTML = r"C:\Users\aag75\AppData\Local\Temp\opencode\pins\html"
OUT_PNG = r"D:\проэкт\pins\covers"
W, H = 1080, 1350

# Spooky-cute palette (from the landing page design system)
ORANGE="#FF8C42"; ORANGE_D="#E8681A"; PURPLE="#7B4FA6"; PURPLE_L="#B79CE0"
CREAM="#FFF8E7"; INK="#2D2D2D"; LIME="#A8D948"; YELLOW="#FFD166"
TEAL="#7FD8D8"; PINK="#FFB5C2"

F_H = "'Baloo 2','Comic Sans MS',cursive"
F_B = "'Nunito','Segoe UI',sans-serif"

# 20 pins adapted from the md files -> kid-friendly spooky-cute themes.
# (kicker, title lines, emoji, bg color, accent color, badge text, footer tagline)
PINS = [
 ("Pumpkin Porch Ideas",      ["Cozy Pumpkin","Porch Vibes"],          "🎃", "#FFF1D8", ORANGE,  "DECOR",     "Spooky-cute, not scary"),
 ("Black Cat Aesthetic",      ["Cute Black Cat","Wallpaper"],          "🐱", "#2E2A3A", PURPLE_L,"WALLPAPER", "Save it for your phone"),
 ("Witch Hat Night",          ["Witch Hat &","Full Moon Night"],       "🧙‍♀️","#EFE7FB", PURPLE,  "MAGIC",     "Purple moonlight vibes"),
 ("Graveyard DIY",            ["Friendly DIY","Graveyard Ideas"],      "🪦", "#EAF6E9", "#5FA033", "DIY",      "Crafts for the whole yard"),
 ("Candy Corn Pattern",       ["Candy Corn","Repeat Pattern"],         "🍬", "#FFF8E7", ORANGE,  "PATTERN",   "Sweet & seamless"),
 ("Costume Ideas",            ["20+ Costume","Ideas for Adults"],      "🎭", "#2E2A3A", PURPLE_L,"COSTUMES",  "Spooky-cute looks"),
 ("Haunted House",            ["Haunted House","Silhouette Night"],    "🏚️", "#EFE7FB", PURPLE,  "WALLPAPER", "Cozy dark mode vibes"),
 ("Skeleton Hand Candy",      ["Trick or Treat","Skeleton Hand"],      "💀", "#FFF1D8", ORANGE,  "PARTY",     "Fun & a little silly"),
 ("Pumpkin Spice Latte",      ["Pumpkin Spice","Latte Aesthetic"],     "☕", "#FFF8E7", "#C97B2D", "COZY",    "Fall in a cup"),
 ("Bat & Jack-O-Lantern",     ["Bat Meets","Jack-O-Lantern"],          "🦇", "#2E2A3A", PURPLE_L,"CLASSIC",   "Best Halloween duo"),
 ("Ghost Blowing Kisses",     ["Ghost Blowing","Kisses — BOO!"],       "👻", "#EFE7FB", PURPLE,  "CUTE",      "The sweetest little ghost"),
 ("Spider Web Craft",         ["Easy Spider","Web Craft"],             "🕷️", "#EAF6E9", "#5FA033", "DIY",     "Simple & fun for kids"),
 ("Trick or Treat Sign",      ["Vintage Trick","or Treat Sign"],       "🪧", "#FFF1D8", ORANGE,  "DECOR",     "Rustic porch charm"),
 ("Vampire Teeth",            ["Vampire Teeth","Close-Up"],            "🧛", "#2E2A3A", PURPLE_L,"SPOOKY",   "Classic fangs, cute style"),
 ("Party Invitation",         ["Halloween Party","Invitation"],        "📨", "#EFE7FB", PURPLE,  "TEMPLATE",  "Printable & pretty"),
 ("Witch Silhouette Moon",    ["Witch Silhouette","& Big Moon"],       "🌕", "#EAF6E9", "#5FA033", "NIGHT",   "Moonlit magic"),
 ("Candy Corn Family",        ["Candy Corn","Family Craft"],           "🍬", "#FFF8E7", ORANGE,  "KIDS",      "Googly-eye fun"),
 ("DIY Porch Decor",          ["DIY Porch","Makeover Guide"],         "🏡", "#FFF1D8", ORANGE,  "DIY",       "Step by step ideas"),
 ("Clown Makeup",             ["Funny Clown","Makeup Idea"],           "🤡", "#EFE7FB", PURPLE,  "TUTORIAL",  "Silly, not scary"),
 ("Free Printables",          ["50+ FREE","Halloween Printables"],     "🎁", "#FFF8E7", ORANGE,  "FREEBIE",   "Coloring, tags & games"),
]

def pin_doc(i, p):
    kicker, lines, emoji, bg, accent, badge, tagline = p
    dark = bg == "#2E2A3A"
    fg = "#FFF8E7" if dark else INK
    title_color = "#FFF8E7" if dark else PURPLE
    kicker_color = accent if not dark else PURPLE_L
    card_bg = "#FFF8E7" if dark else "#FFFFFF"
    sub_color = "#E8DFC9" if dark else "#5E5A66"

    n = f"{i+1:02d}"
    # decorative confetti dots
    dots = []
    palette = [ORANGE, PURPLE_L, LIME, YELLOW, TEAL, PINK]
    for j,(dx,dy,ds) in enumerate([(0.06,0.10,26),(0.93,0.08,22),(0.10,0.88,20),(0.90,0.90,26),
                                    (0.50,0.06,16),(0.48,0.94,16),(0.02,0.50,18),(0.97,0.52,18)]):
        c = palette[(i+j)%len(palette)]
        dots.append(f'<div class="dot" style="left:{dx*100}%;top:{dy*100}%;width:{ds}px;height:{ds}px;background:{c}"></div>')

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pin {n} — {html.escape(kicker)}</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ width:{W}px; height:{H}px; overflow:hidden; }}
  body {{
    font-family:{F_B}; color:{fg};
    background:{bg};
    background-image:radial-gradient(rgba(123,79,166,.14) 2px, transparent 2.2px);
    background-size:34px 34px;
  }}
  .pin {{ position:relative; width:{W}px; height:{H}px; display:flex; flex-direction:column; align-items:center; justify-content:flex-start; padding:64px 70px 56px; }}
  .badge {{
    font-family:{F_B}; font-weight:900; font-size:26px; letter-spacing:.16em;
    background:{accent}; color:#FFF8E7; border-radius:999px; padding:12px 30px;
    box-shadow:0 5px 0 rgba(0,0,0,.14); margin-bottom:8px;
  }}
  .emoji {{ font-size:250px; line-height:1.05; margin:18px 0 6px; filter:drop-shadow(0 14px 22px rgba(45,45,45,.22)); }}
  .title {{ font-family:{F_H}; font-weight:800; font-size:92px; line-height:1.06; color:{title_color}; text-align:center; letter-spacing:-.01em; }}
  .hl {{ background:linear-gradient(180deg,transparent 58%,{YELLOW} 58%,{YELLOW} 92%,transparent 92%); padding:0 .06em; border-radius:8px; }}
  .kicker {{ font-family:{F_H}; font-weight:700; font-size:44px; color:{kicker_color}; margin-top:22px; text-align:center; }}
  .card {{
    margin-top:auto; background:{card_bg}; color:{INK}; border-radius:26px; width:100%;
    padding:30px 38px; display:flex; align-items:center; justify-content:space-between; gap:24px;
    box-shadow:0 12px 30px rgba(45,45,45,.14); border:3px solid rgba(123,79,166,.18);
  }}
  .card .brand {{ font-family:{F_H}; font-weight:800; font-size:40px; color:{PURPLE}; }}
  .card .tag {{ font-family:{F_B}; font-weight:800; font-size:25px; color:{sub_color}; text-align:right; }}
  .dot {{ position:absolute; border-radius:50%; opacity:.85; }}
  .num {{ position:absolute; right:34px; top:30px; font-family:{F_H}; font-weight:800; font-size:40px; color:rgba(123,79,166,.35); }}
</style></head>
<body>
<div class="pin">
  {dots}
  <div class="num">{n}/20</div>
  <div class="badge">{badge}</div>
  <div class="emoji">{emoji}</div>
  <h1 class="title"><span class="hl">{html.escape(lines[0])}</span><br>{html.escape(lines[1])}</h1>
  <div class="kicker">{html.escape(tagline)}</div>
  <div class="card">
    <div class="brand">🎃 Spooky Cute Printables</div>
    <div class="tag">{html.escape(kicker)}<br>swipe for ideas →</div>
  </div>
</div>
</body></html>"""

os.makedirs(OUT_HTML, exist_ok=True)
os.makedirs(OUT_PNG, exist_ok=True)
manifest = []
for i, p in enumerate(PINS):
    path = os.path.join(OUT_HTML, f"pin-{i+1:02d}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(pin_doc(i, p))
    manifest.append(os.path.basename(path))
print(f"Wrote {len(manifest)} HTML files to {OUT_HTML}")
