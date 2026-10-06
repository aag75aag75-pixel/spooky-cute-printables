# Renders 20 Pinterest pin covers (1080x1350) from HTML -> PNG via Playwright/Chromium.
# Fonts: Google Fonts (Baloo 2 + Nunito). Style matches the Spooky Cute Printables landing page.
import os
from playwright.sync_api import sync_playwright

HTML_DIR = r"C:\Users\aag75\AppData\Local\Temp\opencode\pins\html2"
PNG_DIR = r"D:\проэкт\pins\covers"
W, H = 1080, 1350
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

ORANGE = "#FF8C42"; ORANGE_D = "#E8681A"; PURPLE = "#7B4FA6"; PURPLE_L = "#B79CE0"
CREAM = "#FFF8E7"; INK = "#2D2D2D"; LIME = "#A8D948"; YELLOW = "#FFD166"
TEAL = "#7FD8D8"; PINK = "#FFB5C2"

# (kicker, line1, line2, emoji, bg, accent, badge, tagline)
PINS = [
 ("Pumpkin Porch Ideas",      "Cozy Pumpkin",      "Porch Vibes",        "🎃", "#FFF1D8", ORANGE,  "DECOR",     "Spooky-cute, not scary"),
 ("Black Cat Aesthetic",      "Cute Black Cat",    "Wallpaper",          "🐱", "#332F42", PURPLE_L,"WALLPAPER", "Save it for your phone"),
 ("Witch Hat Night",          "Witch Hat &",       "Full Moon Night",    "🧙‍♀️","#EFE7FB", PURPLE,  "MAGIC",     "Purple moonlight vibes"),
 ("Graveyard DIY",            "Friendly DIY",      "Graveyard Ideas",    "🪦", "#EAF6E9", "#5FA033","DIY",       "Crafts for the whole yard"),
 ("Candy Corn Pattern",       "Candy Corn",        "Repeat Pattern",     "🍬", "#FFF8E7", ORANGE,  "PATTERN",   "Sweet & seamless"),
 ("Costume Ideas",            "20+ Costume",       "Ideas for Adults",   "🎭", "#332F42", PURPLE_L,"COSTUMES",  "Spooky-cute looks"),
 ("Haunted House",            "Haunted House",     "Silhouette Night",   "🏚️", "#EFE7FB", PURPLE,  "WALLPAPER", "Cozy dark-mode vibes"),
 ("Skeleton Hand Candy",      "Trick or Treat",    "Skeleton Hand",      "💀", "#FFF1D8", ORANGE,  "PARTY",     "Fun & a little silly"),
 ("Pumpkin Spice Latte",      "Pumpkin Spice",     "Latte Aesthetic",    "☕", "#FFF8E7", "#C97B2D","COZY",      "Fall in a cup"),
 ("Bat & Jack-O-Lantern",     "Bat Meets",         "Jack-O-Lantern",     "🦇", "#332F42", PURPLE_L,"CLASSIC",   "Best Halloween duo"),
 ("Ghost Blowing Kisses",     "Ghost Blowing",     "Kisses — BOO!",      "👻", "#EFE7FB", PURPLE,  "CUTE",      "The sweetest little ghost"),
 ("Spider Web Craft",         "Easy Spider",       "Web Craft",          "🕷️", "#EAF6E9", "#5FA033","DIY",       "Simple & fun for kids"),
 ("Trick or Treat Sign",      "Vintage Trick",     "or Treat Sign",      "🪧", "#FFF1D8", ORANGE,  "DECOR",     "Rustic porch charm"),
 ("Vampire Teeth",            "Vampire Teeth",     "Close-Up",           "🧛", "#332F42", PURPLE_L,"SPOOKY",    "Classic fangs, cute style"),
 ("Party Invitation",         "Halloween Party",   "Invitation",         "📨", "#EFE7FB", PURPLE,  "TEMPLATE",  "Printable & pretty"),
 ("Witch Silhouette Moon",    "Witch Silhouette",  "& Big Moon",         "🌕", "#EAF6E9", "#5FA033","NIGHT",     "Moonlit magic"),
 ("Candy Corn Family",        "Candy Corn",        "Family Craft",       "🍬", "#FFF8E7", ORANGE,  "KIDS",      "Googly-eye fun"),
 ("DIY Porch Decor",          "DIY Porch",         "Makeover Guide",     "🏡", "#FFF1D8", ORANGE,  "DIY",       "Step by step ideas"),
 ("Clown Makeup",             "Funny Clown",       "Makeup Idea",        "🤡", "#EFE7FB", PURPLE,  "TUTORIAL",  "Silly, not scary"),
 ("Free Printables",          "50+ FREE",          "Halloween Printables","🎁", "#FFF8E7", ORANGE,  "FREEBIE",   "Coloring, tags & games"),
]

def pin_html(i, p):
    kicker, l1, l2, emoji, bg, accent, badge, tagline = p
    dark = bg == "#332F42"
    title_c = "#FFF8E7" if dark else PURPLE
    sub_c = "#E8DFC9" if dark else "#5E5A66"
    card_bg = "#FFF8E7" if dark else "#FFFFFF"
    dot_rgb = "255,248,231" if dark else "123,79,166"
    n = f"{i+1:02d}"
    dots = ""
    palette = [ORANGE, PURPLE_L, LIME, YELLOW, TEAL, PINK]
    spots = [(6,10,26),(93,8,22),(10,88,20),(90,90,26),(50,5.5,16),(48,94,16),(2,50,18),(97,52,18)]
    for j,(fx,fy,ds) in enumerate(spots):
        c = palette[(i+j) % len(palette)]
        dots += (f'<div class="dot" style="left:{fx}%;top:{fy}%;width:{ds}px;height:{ds}px;background:{c}"></div>')
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>Pin {n} — {kicker}</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{
  font-family:'Nunito','Segoe UI',sans-serif;color:{"#FFF8E7" if dark else INK};
  background:{bg};
  background-image:radial-gradient(rgba({dot_rgb},.15) 2px,transparent 2.2px);
  background-size:34px 34px;
}}
.pin{{position:relative;width:{W}px;height:{H}px;display:flex;flex-direction:column;align-items:center;padding:64px 70px 56px}}
.dot{{position:absolute;border-radius:50%;opacity:.85}}
.num{{position:absolute;right:34px;top:28px;font-family:'Baloo 2',cursive;font-weight:800;font-size:38px;color:rgba(123,79,166,.32)}}
.badge{{
  font-weight:900;font-size:26px;letter-spacing:.16em;color:#FFF8E7;background:{accent};
  border-radius:999px;padding:12px 30px;box-shadow:0 5px 0 rgba(0,0,0,.14);margin-top:6px;
}}
.emoji{{font-size:270px;line-height:1.05;margin:26px 0 14px;filter:drop-shadow(0 16px 24px rgba(45,45,45,.25))}}
.title{{font-family:'Baloo 2',cursive;font-weight:800;font-size:96px;line-height:1.06;color:{title_c};text-align:center;letter-spacing:-.01em}}
.hl{{background:linear-gradient(180deg,transparent 58%,{YELLOW} 58%,{YELLOW} 92%,transparent 92%);padding:0 .06em;border-radius:8px}}
.kicker{{font-family:'Baloo 2',cursive;font-weight:700;font-size:46px;color:{accent if not dark else PURPLE_L};margin-top:26px;text-align:center}}
.card{{
  margin-top:auto;width:100%;background:{card_bg};color:{INK};border-radius:26px;
  padding:28px 36px;display:flex;align-items:center;justify-content:space-between;gap:20px;
  box-shadow:0 12px 30px rgba(45,45,45,.14);border:3px solid rgba(123,79,166,.18);
}}
.brand{{font-family:'Baloo 2',cursive;font-weight:800;font-size:42px;color:{PURPLE}}}
.tag{{font-weight:800;font-size:24px;color:{sub_c};text-align:right;line-height:1.35}}
</style></head><body>
<div class="pin">
  {dots}
  <div class="num">{n}/20</div>
  <div class="badge">{badge}</div>
  <div class="emoji">{emoji}</div>
  <h1 class="title"><span class="hl">{l1}</span><br>{l2}</h1>
  <div class="kicker">{tagline}</div>
  <div class="card">
    <div class="brand">🎃 Spooky Cute Printables</div>
    <div class="tag">{kicker}<br>swipe for ideas →</div>
  </div>
</div></body></html>"""

with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--force-device-scale-factor=1"])
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    for i, p in enumerate(PINS):
        hp = os.path.join(HTML_DIR, f"pin-{i+1:02d}.html")
        with open(hp, "w", encoding="utf-8") as f:
            f.write(pin_html(i, p))
        page.goto("file:///" + hp.replace("\\", "/"))
        page.wait_for_timeout(700)  # let Google Fonts settle
        png = os.path.join(PNG_DIR, f"pin-{i+1:02d}.png")
        page.screenshot(path=png, clip={"x": 0, "y": 0, "width": W, "height": H})
        print(f"pin-{i+1:02d}.png  {os.path.getsize(png)} bytes")
    browser.close()
print("DONE")
