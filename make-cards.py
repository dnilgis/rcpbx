#!/usr/bin/env python3
"""
rcpbx make-cards.py — generates per-recipe social share cards (PNG, 1200x630)
plus the site-wide og-image.png, in the terminal brand style.

Why: SVG og:images don't render on iMessage/WhatsApp/Discord/Slack/X, and
Google Recipe rich results REQUIRE an image. These cards fix both.

Fonts: uses assets/fonts/JetBrainsMono-*.ttf if present, else DejaVu Sans Mono.
Run after build.py:  python3 make-cards.py
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (17, 17, 17)          # #111
FG = (229, 229, 229)       # #e5e5e5
MUT = (153, 153, 153)      # #999
DIM = (102, 102, 102)      # #666
ACC = (34, 197, 94)        # #22c55e

def font(size, bold=False):
    cands = (["assets/fonts/JetBrainsMono-Bold.ttf"] if bold else ["assets/fonts/JetBrainsMono-Medium.ttf","assets/fonts/JetBrainsMono-Regular.ttf"])
    cands += ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=f) <= max_w: cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

def base_card():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # top-left brand
    d.text((70, 56), ">", font=font(40, True), fill=ACC)
    d.text((100, 56), "rcpbx", font=font(40, True), fill=FG)
    # accent rule
    d.rectangle([70, 130, 190, 136], fill=ACC)
    return img, d

def recipe_card(e):
    img, d = base_card()
    title = e["title"]
    tf = font(84, True)
    lines = wrap(d, title, tf, W - 140)
    if len(lines) > 2:
        tf = font(64, True); lines = wrap(d, title, tf, W - 140)[:3]
    y = 200
    for ln in lines:
        d.text((70, y), ln, font=tf, fill=FG); y += tf.size + 14
    tag = e.get("tagline", "")
    if tag:
        gf = font(30)
        for ln in wrap(d, tag, gf, W - 140)[:2]:
            d.text((70, y + 10), ln, font=gf, fill=MUT); y += gf.size + 12
    if e.get("verdict"):
        vf = font(26, True)
        vt = "[ %s ]" % e["verdict"]
        vw = d.textlength(vt, font=vf)
        d.text((70, y + 26), vt, font=vf, fill=ACC); y += 60
    # bottom meta bar
    bits = ["rcpbx.com"]
    if e.get("prep"): bits.append("prep " + str(e["prep"]))
    if e.get("cook"): bits.append("cook " + str(e["cook"]))
    if e.get("makes"): bits.append("makes " + str(e["makes"]))
    elif e.get("serves"): bits.append("serves " + str(e["serves"]))
    mf = font(28)
    d.text((70, H - 90), "  ·  ".join(bits), font=mf, fill=DIM)
    d.text((70, H - 140), "no life stories · no ads · just the recipe", font=font(24), fill=(60, 120, 80))
    return img

def og_main(total):
    img, d = base_card()
    d.text((70, 210), ">", font=font(120, True), fill=ACC)
    d.text((160, 210), "rcpbx", font=font(120, True), fill=FG)
    d.text((70, 370), "%d recipes that actually work" % total, font=font(44, True), fill=FG)
    d.text((70, 445), "no life stories · no ads · no popups · just cook", font=font(30), fill=MUT)
    d.text((70, H - 90), "rcpbx.com", font=font(28), fill=DIM)
    return img

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    idx = json.load(open("data/index.json"))
    og_main(len(idx)).save("og-image.png", optimize=True)
    print("og-image.png")
    n = 0
    for e in idx:
        os.makedirs("recipes/%s" % e["id"], exist_ok=True)
        recipe_card(e).save("recipes/%s/card.png" % e["id"], optimize=True)
        n += 1
    print("%d recipe cards" % n)

if __name__ == "__main__":
    main()
