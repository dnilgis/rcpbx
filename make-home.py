#!/usr/bin/env python3
"""
rcpbx make-home.py — keeps the homepage and every "N recipes" claim honest.

  - category counts and the total on index.html, from data/index.json
  - a static A-Z list of every recipe on the homepage (crawlable without JS)
  - an "in season" row that changes with the month
  - the recipe count in README.md, about/, api/, why/
Run after build.py.
"""
import json, os, re, html, datetime

def esc(s): return html.escape(str(s), quote=True)

CATS = [  # (categorySlug, hub url, label) in homepage order
    ("soups-stews", "soup-recipes/", "Soups & Stews"), ("pasta", "pasta-recipes/", "Pasta"),
    ("chicken", "chicken-recipes/", "Chicken"), ("beef", "beef-recipes/", "Beef"),
    ("pork", "pork-recipes/", "Pork"), ("seafood", "seafood-recipes/", "Seafood"),
    ("breakfast", "breakfast-recipes/", "Breakfast"), ("sides", "side-dishes/", "Sides"),
    ("baking-dessert", "dessert-recipes/", "Baking & Desserts"), ("basics", "basic-recipes/", "Basics"),
]

# month -> list of (href, label). Only links to pages that exist.
SEASON = {
    1: [("soup-recipes/", "soups"), ("recipes/chili-by-george/", "chili"), ("healthy-recipes/", "lighter")],
    2: [("soup-recipes/", "soups"), ("recipes/pot-roast/", "pot roast"), ("dessert-recipes/", "baking")],
    3: [("soup-recipes/", "soups"), ("recipes/glazed-ham/", "easter ham"), ("egg-recipes/", "eggs")],
    4: [("recipes/glazed-ham/", "easter ham"), ("egg-recipes/", "eggs"), ("healthy-recipes/", "lighter")],
    5: [("grilled/", "grilling"), ("recipes/pasta-salad/", "pasta salad"), ("no-cook/", "no-cook")],
    6: [("grilled/", "grilling"), ("no-cook/", "no-cook"), ("recipes/lemonade/", "lemonade")],
    7: [("grilled/", "grilling"), ("no-cook/", "no-cook"), ("recipes/corn-on-the-cob/", "sweet corn")],
    8: [("grilled/", "grilling"), ("no-cook/", "no-cook"), ("recipes/zucchini-bread/", "zucchini bread")],
    9: [("soup-recipes/", "soups"), ("recipes/apple-pie/", "apple pie"), ("recipes/chili-by-george/", "chili")],
    10: [("thanksgiving/", "thanksgiving"), ("recipes/roast-turkey/", "turkey"), ("soup-recipes/", "soups"),
         ("recipes/stuffed-pepper-soup/", "stuffed pepper soup")],
    11: [("thanksgiving/", "thanksgiving"), ("recipes/roast-turkey/", "turkey"), ("recipes/pumpkin-pie/", "pumpkin pie"),
         ("recipes/stuffing/", "stuffing")],
    12: [("christmas/", "christmas"), ("recipes/sugar-cookies/", "cookies"), ("recipes/glazed-ham/", "ham")],
}


def sub_between(text, start, end, body):
    a = text.find(start); b = text.find(end)
    if a == -1 or b == -1:
        raise SystemExit("marker missing: %s" % start)
    return text[:a + len(start)] + body + text[b:]


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    idx = json.load(open("data/index.json"))
    total = len(idx)
    count = {}
    for e in idx: count[e.get("categorySlug")] = count.get(e.get("categorySlug"), 0) + 1

    h = open("index.html", encoding="utf-8").read()

    cats = ['\n        <div class="categories-label"><span id="recipeCount">%d</span> recipes across %d categories</div>'
            % (total, len(CATS))]
    for slug, url, label in CATS:
        cats.append('        <a href="%s" class="category">\n          <span class="category-name">%s</span>\n'
                    '          <span class="category-count">%d recipes</span>\n        </a>' % (url, esc(label), count.get(slug, 0)))
    h = sub_between(h, "<!-- CATS:START -->", "<!-- CATS:END -->", "\n".join(cats) + "\n        ")

    month = datetime.date.today().month
    links = [(u, l) for u, l in SEASON.get(month, []) if os.path.exists(u.rstrip("/") + "/index.html")]
    season = ('\n      <nav class="tonight season" aria-label="In season">\n        <span class="t-label">&gt; in season:</span>\n'
              + "\n".join('        <a href="%s">%s</a>' % (u, esc(l)) for u, l in links)
              + "\n      </nav>\n      ") if links else "\n      "
    h = sub_between(h, "<!-- SEASON:START -->", "<!-- SEASON:END -->", season)

    by_letter = {}
    for e in sorted(idx, key=lambda e: e["title"].lower()):
        by_letter.setdefault(e["title"][0].upper(), []).append(e)
    az = ['\n      <section class="az" aria-labelledby="azTitle">',
          '        <h2 id="azTitle">All %d recipes, A–Z</h2>' % total]
    for letter in sorted(by_letter):
        az.append('        <h3>%s</h3>\n        <ul>' % esc(letter))
        az += ['          <li><a href="recipes/%s/">%s</a></li>' % (e["id"], esc(e["title"])) for e in by_letter[letter]]
        az.append('        </ul>')
    az.append('      </section>\n      ')
    h = sub_between(h, "<!-- AZ:START -->", "<!-- AZ:END -->", "\n".join(az))

    h = re.sub(r'(<title>rcpbx — the recipe box \| )\d+( Recipes)', lambda m: m.group(1) + str(total) + m.group(2), h)
    h = re.sub(r'(content=")\d+( recipes with no life stories)', lambda m: m.group(1) + str(total) + m.group(2), h)
    open("index.html", "w", encoding="utf-8").write(h)

    # every other "N recipes" claim
    for f in ("README.md", "about/index.html", "api/index.html", "why/index.html"):
        if not os.path.exists(f): continue
        t = open(f, encoding="utf-8").read()
        t2 = re.sub(r"\b1\d\d( recipes\b| acts of invention)", lambda m: str(total) + m.group(1), t)
        t2 = re.sub(r"(jq length\s+# )\d+", lambda m: m.group(1) + str(total), t2)
        if t2 != t: open(f, "w", encoding="utf-8").write(t2)
    print("home: %d recipes, %d categories, in-season row for month %d (%d links), A-Z list" % (total, len(CATS), month, len(links)))


if __name__ == "__main__":
    main()
