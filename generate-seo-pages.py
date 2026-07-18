#!/usr/bin/env python3
"""
rcpbx programmatic SEO pages — v2 (2026-07)
Fixes from the panel review:
  - pages now use the real brand shell (fonts, logo, footer) instead of a generic template
  - categorization comes from categorySlug, never keyword-matching on "chicken broth"
  - recipes with no time data are EXCLUDED from time pages (old script defaulted them to 30 min)
  - "meals" pages only contain mains — no more Buttercream Frosting as a 15-minute dinner
  - empty meta lines are omitted instead of rendering " +  · 4"
  - every page gets ItemList schema + specific intro copy + interlinks
Run AFTER build.py (build.py enriches data/index.json with times).
"""
import json, os, re, html
from pathlib import Path

SITE = "https://rcpbx.com"
MAIN_CATS = {"chicken","beef","pork","seafood","pasta","soups-stews"}
CAT_HUBS = {
    "chicken-recipes": ("chicken", "Chicken Recipes", "Chicken"),
    "beef-recipes": ("beef", "Beef Recipes", "Beef"),
    "pork-recipes": ("pork", "Pork Recipes", "Pork"),
    "seafood-recipes": ("seafood", "Seafood Recipes", "Seafood"),
    "pasta-recipes": ("pasta", "Pasta Recipes", "Pasta"),
    "breakfast-recipes": ("breakfast", "Breakfast Recipes", "Breakfast"),
    "side-dishes": ("sides", "Side Dishes", "Sides"),
    "dessert-recipes": ("baking-dessert", "Dessert & Baking Recipes", "Baking & Desserts"),
    "soup-recipes": ("soups-stews", "Soup & Stew Recipes", "Soups & Stews"),
    "basic-recipes": ("basics", "Kitchen Basics", "Basics"),
}

def esc(s): return html.escape(str(s), quote=True)

def mins(entry):
    total = 0
    for f in ("prep","cook"):
        t = str(entry.get(f,"") or "")
        m = re.search(r"(\d+)\s*(?:min)", t)
        h = re.search(r"(\d+)\s*(?:hour|hr)", t)
        if m: total += int(m.group(1))
        if h: total += int(h.group(1)) * 60
    return total if total > 0 else None  # None = unknown, NOT 30

def card(e):
    meta_bits = []
    m = mins(e)
    if m: meta_bits.append("%d min" % m)
    if e.get("makes"): meta_bits.append("makes %s" % e["makes"])
    elif e.get("serves"): meta_bits.append("serves %s" % e["serves"])
    meta = " · ".join(meta_bits)
    v = (' <span class="card-verdict">[%s]</span>' % esc(e["verdict"])) if e.get("verdict") else ""
    out = ('        <a href="/recipes/%s/" class="recipe-card">\n'
           '          <span class="recipe-title">%s%s</span>\n'
           '          <span class="recipe-tagline">%s</span>\n') % (e["id"], esc(e["title"]), v, esc(e.get("tagline","")))
    if meta:
        out += '          <span class="recipe-meta">%s</span>\n' % esc(meta)
    out += '        </a>'
    return out

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>%%META_TITLE%% | rcpbx</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90' font-family='monospace' fill='%2316a34a'>%3E</text></svg>">
  <meta name="description" content="%%DESC%%">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="%%URL%%">
  <meta property="og:type" content="website">
  <meta property="og:url" content="%%URL%%">
  <meta property="og:title" content="%%META_TITLE%% | rcpbx">
  <meta property="og:description" content="%%DESC%%">
  <meta property="og:site_name" content="rcpbx">
  <meta property="og:image" content="https://rcpbx.com/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://rcpbx.com/og-image.png">
  <script type="application/ld+json">
%%SCHEMA%%
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-E2VNWY2BFX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-E2VNWY2BFX');
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #faf9f6; --bg-alt: #f0efeb; --text: #222; --text-muted: #666; --text-dim: #999;
      --border: #ddd; --accent: #16a34a; --accent-dim: rgba(22,163,74,0.1);
      --font-sans: 'Inter', -apple-system, sans-serif; --font-mono: 'JetBrains Mono', monospace;
    }
    @media (prefers-color-scheme: dark) {
      :root { --bg: #111; --bg-alt: #1a1a1a; --text: #e5e5e5; --text-muted: #999; --text-dim: #666;
        --border: #333; --accent: #22c55e; --accent-dim: rgba(34,197,94,0.15); }
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { font-family: var(--font-sans); background: var(--bg); color: var(--text); line-height: 1.6; }
    header { border-bottom: 1px solid var(--border); padding: 1rem 1.5rem; }
    .header-inner { max-width: 800px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
    .logo { font-family: var(--font-mono); font-size: 1.25rem; font-weight: 600; text-decoration: none; color: var(--text); }
    .logo-prefix { color: var(--accent); }
    .header-link { font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); text-decoration: none; text-transform: uppercase; letter-spacing: 0.05em; }
    .header-link:hover { color: var(--accent); }
    main { max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem; }
    .breadcrumb { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 1rem; font-family: var(--font-mono); }
    .breadcrumb a { color: var(--text-muted); text-decoration: none; }
    .breadcrumb a:hover { color: var(--accent); }
    h1 { font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.5rem; }
    .intro { color: var(--text-muted); font-size: 0.95rem; margin-bottom: 1.75rem; max-width: 62ch; }
    .count-line { font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-dim); margin-bottom: 1rem; }
    .count-line span { color: var(--accent); }
    .recipe-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 0.75rem; }
    .recipe-card { display: block; padding: 0.85rem 1rem; border: 1px solid var(--border); border-radius: 6px;
      text-decoration: none; transition: border-color 0.15s, transform 0.15s; }
    .recipe-card:hover { border-color: var(--accent); transform: translateY(-1px); }
    .recipe-title { display: block; font-weight: 600; font-size: 0.95rem; color: var(--text); }
    .card-verdict { font-family: var(--font-mono); font-size: 0.6rem; color: var(--accent); font-weight: 500; }
    .recipe-tagline { display: block; font-size: 0.78rem; color: var(--text-muted); margin-top: 0.15rem; }
    .recipe-meta { display: block; font-family: var(--font-mono); font-size: 0.65rem; color: var(--text-dim); margin-top: 0.3rem; }
    .also { margin-top: 2.5rem; border-top: 1px solid var(--border); padding-top: 1.25rem;
      font-family: var(--font-mono); font-size: 0.75rem; line-height: 2.1; color: var(--text-dim); }
    .also a { color: var(--text-muted); text-decoration: none; }
    .also a:hover { color: var(--accent); }
    .also .lbl { color: var(--accent); margin-right: 0.4rem; }
    footer { border-top: 1px solid var(--border); padding: 1.5rem; text-align: center; margin-top: 3rem; }
    .footer-text { font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); }
    .footer-text a { color: var(--accent); text-decoration: none; }
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="/" class="logo"><span class="logo-prefix">&gt;</span>rcpbx</a>
      <a href="/" class="header-link">← all recipes</a>
    </div>
  </header>
  <main>
    <nav class="breadcrumb"><a href="/">home</a> / %%CRUMB%%</nav>
    <h1>%%H1%%</h1>
    <p class="intro">%%INTRO%%</p>
    <p class="count-line"><span>%%COUNT%%</span> recipes · every one opens to ingredients and steps, nothing else</p>
    <div class="recipe-grid">
%%CARDS%%
    </div>
    <div class="also"><span class="lbl">&gt; also:</span>%%ALSO%%</div>
  </main>
  <footer>
    <p class="footer-text"><a href="/">rcpbx.com</a> · no life stories · no ads · <a href="/random/">random recipe</a></p>
  </footer>
</body>
</html>
"""

ALSO_LINKS = [
    ("/15-minute-meals/","15-minute meals"), ("/30-minute-meals/","30-minute meals"),
    ("/weeknight/","weeknight dinners"), ("/no-cook/","no-cook"), ("/easy-recipes/","easy"),
    ("/chicken-recipes/","chicken"), ("/pasta-recipes/","pasta"), ("/dessert-recipes/","desserts"),
]

def write_page(slug, h1, meta_title, desc, intro, entries, crumb=None):
    if not entries:
        print("  – /%s/ skipped (0 recipes)" % slug); return False
    entries = sorted(entries, key=lambda e: e["title"])
    cards = "\n".join(card(e) for e in entries)
    also = " · ".join('<a href="%s">%s</a>' % (u, t) for u, t in ALSO_LINKS if u != "/%s/" % slug)
    schema = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": h1, "description": desc[:155], "url": "%s/%s/" % (SITE, slug),
        "mainEntity": {"@type": "ItemList", "numberOfItems": len(entries),
            "itemListElement": [{"@type": "ListItem", "position": i+1, "name": e["title"],
                "url": "%s/recipes/%s/" % (SITE, e["id"])} for i, e in enumerate(entries)]},
    }
    page = (PAGE.replace("%%META_TITLE%%", esc(meta_title))
        .replace("%%DESC%%", esc(desc[:155]))
        .replace("%%URL%%", "%s/%s/" % (SITE, slug))
        .replace("%%SCHEMA%%", json.dumps(schema, ensure_ascii=False))
        .replace("%%CRUMB%%", esc(crumb or h1.lower()))
        .replace("%%H1%%", esc(h1))
        .replace("%%INTRO%%", intro)
        .replace("%%COUNT%%", str(len(entries)))
        .replace("%%CARDS%%", cards)
        .replace("%%ALSO%%", also))
    Path(slug).mkdir(exist_ok=True)
    Path(slug, "index.html").write_text(page)
    print("  ✓ /%s/ (%d recipes)" % (slug, len(entries)))
    return True

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    idx = json.load(open("data/index.json"))
    full = {}
    for f in Path("data").glob("*.json"):
        if f.name in ("index.json","hot.json","radar.json"): continue
        r = json.load(open(f)); full[r["id"]] = r
    for e in idx:  # merge time data from full files if index not yet enriched
        r = full.get(e["id"])
        if r:
            if not e.get("prep") and r.get("prep"): e["prep"] = r["prep"]
            if not e.get("cook") and r.get("cook") is not None: e["cook"] = r["cook"]
            if not e.get("serves"): e["serves"] = r.get("serves") or r.get("makes")

    def text_of(e):
        r = full.get(e["id"], {})
        return " ".join([e.get("title","") or "", e.get("tagline","") or ""] +
                        r.get("ingredients", []) + r.get("steps", [])).lower()

    print("Category hubs:")
    for slug, (cat, h1, disp) in CAT_HUBS.items():
        entries = [e for e in idx if e.get("categorySlug") == cat]
        timed = [mins(e) for e in entries if mins(e)]
        tr = (" Most land in %d–%d minutes." % (min(timed), max(timed))) if len(timed) >= 3 else ""
        intro = ("Every %s recipe on rcpbx — %d of them, one canonical version per dish, "
                 "stripped to ingredients and steps.%s No ads, no life stories, no popups."
                 % (disp.lower(), len(entries), tr))
        write_page(slug, h1, h1,
                   "%d %s recipes with no ads and no life stories. Ingredients, steps, done." % (len(entries), disp.lower()),
                   intro, entries, crumb=disp.lower())

    print("Time pages (only recipes with real time data):")
    mains = [e for e in idx if e.get("categorySlug") in MAIN_CATS and mins(e)]
    for slug, h1, cap, blurb in [
        ("15-minute-meals", "15-Minute Meals", 15, "Real dinners on the table in a quarter hour — mains only, nothing that's secretly a condiment."),
        ("30-minute-meals", "30-Minute Meals", 30, "Weeknight-speed mains: everything here is a full dinner with a verified prep+cook time of 30 minutes or less."),
        ("under-1-hour", "Dinners Under 1 Hour", 60, "Mains that go from fridge to table inside an hour, timed for real, not rounded down."),
    ]:
        entries = [e for e in mains if mins(e) <= cap]
        write_page(slug, h1, h1, blurb, blurb + " Only recipes with verified times make this list.", entries)

    print("Method pages:")
    for slug, h1, blurb, pat in [
        ("grilled", "Grilled Recipes", "Everything that touches the grates: temps, timings, and when to stop.", r"\bgrill"),
        ("baked", "Baked Recipes", "Oven-driven recipes with real temperatures and doneness cues.", r"\boven|\bbake"),
        ("no-cook", "No-Cook Recipes", "Zero heat. Salads, assemblies, and cold things for hot days.", None),
    ]:
        if slug == "no-cook":
            entries = [e for e in idx if re.match(r"^\s*0\s*min", str(e.get("cook","")))]
        else:
            entries = [e for e in idx if full.get(e["id"]) and re.search(pat, text_of(e))]
        write_page(slug, h1, h1, blurb, blurb, entries)

    print("Ingredient pages:")
    for slug, h1, kws, blurb in [
        ("what-to-make-with-chicken-breast", "What to Make with Chicken Breast", ["chicken breast"], "Got chicken breasts and no plan? These are the tested answers — every one a full recipe, not a listicle."),
        ("what-to-make-with-ground-beef", "What to Make with Ground Beef", ["ground beef"], "A pound of ground beef becomes any of these — tested recipes with real times, no scrolling past someone's childhood."),
        ("what-to-make-with-eggs", "What to Make with Eggs", ["egg"], "Eggs in the fridge, dinner (or breakfast) on the table. Each link is straight to ingredients and steps."),
        ("what-to-make-with-potatoes", "What to Make with Potatoes", ["potato"], "Every direction a potato can go — crispy, mashed, roasted, soup — in tested, no-fluff form."),
        ("what-to-make-with-rice", "What to Make with Rice", ["rice"], "Cooked rice or a bag in the pantry: these recipes turn it into dinner."),
        ("what-to-make-with-pasta", "What to Make with Pasta", ["pasta", "spaghetti", "noodle"], "A box of pasta and one of these pages is a complete plan. Tested, timed, no ads."),
    ]:
        entries = []
        for e in idx:
            r = full.get(e["id"])
            if not r: continue  # ingredient matching needs the full recipe
            ing = " ".join(r.get("ingredients", [])).lower()
            if any(k in ing for k in kws): entries.append(e)
        write_page(slug, h1, h1, blurb, blurb, entries)

    print("Diet/skill pages:")
    MEAT = ["chicken","beef","pork","bacon","sausage","salmon","shrimp","fish","anchov","tuna","turkey","lamb","prosciutto","pancetta","ham","gelatin"]
    veg = []
    for e in idx:
        r = full.get(e["id"])
        if not r: continue
        ing = " ".join(r.get("ingredients", [])).lower()
        if not any(m in ing for m in MEAT): veg.append(e)
    write_page("vegetarian-recipes", "Vegetarian Recipes", "Vegetarian Recipes",
        "Meat-free recipes checked at the ingredient level, not the vibes level.",
        "Every recipe here is meat-free at the ingredient list level — checked against what's actually in it, not the title.", veg)

    egg_entries = []
    for e in idx:
        r = full.get(e["id"])
        if r and any("egg" in i.lower() for i in r.get("ingredients", [])): egg_entries.append(e)
    write_page("egg-recipes", "Egg Recipes", "Egg Recipes",
        "Recipes where eggs do the heavy lifting — breakfast and beyond.",
        "Everything on this page leans on eggs — from breakfast obvious to dinners you didn't expect.", egg_entries)

    easy = []
    for e in idx:
        r = full.get(e["id"])
        if r and len([i for i in r.get("ingredients",[]) if not i.strip().endswith(":")]) <= 8 and len(r.get("steps",[])) <= 7:
            easy.append(e)
    write_page("easy-recipes", "Easy Recipes", "Easy Recipes",
        "Eight ingredients or fewer, seven steps or fewer. Genuinely easy, by the numbers.",
        "“Easy” here is a measurement, not a mood: every recipe has 8 ingredients or fewer and 7 steps or fewer.", easy)

    healthy = []
    for e in idx:
        m = mins(e); r = full.get(e["id"])
        if not r or not m: continue
        ing = " ".join(r.get("ingredients",[])).lower()
        light = e.get("categorySlug") in ("sides","seafood","chicken","basics") and not any(
            k in ing for k in ["heavy cream","butter, softened","bacon","brown sugar","chocolate"])
        if light and m <= 45: healthy.append(e)
    write_page("healthy-recipes", "Healthy Recipes", "Healthy Recipes",
        "Lighter mains and sides under 45 minutes — defined by ingredients, not marketing.",
        "Lighter recipes chosen by what's actually in them — lean proteins, vegetables, no cream-and-sugar bombs — all under 45 minutes.", healthy)

    print("\nDone. Run 'python3 build.py' FIRST when you add recipes (it enriches index.json with times).")

if __name__ == "__main__":
    main()
