#!/usr/bin/env python3
"""
Programmatic SEO Page Generator
Generates landing pages from recipe data for long-tail keyword capture.
"""

import json
import os
from pathlib import Path
from collections import defaultdict

SITE_URL = "https://rcpbx.com"

# Load all recipes
def load_recipes():
    recipes = []
    for f in sorted(Path("data").glob("*.json")):
        if f.name == "index.json":
            continue
        with open(f) as fp:
            recipes.append(json.load(fp))
    return recipes

def extract_cook_time_minutes(recipe):
    """Extract total cook time in minutes"""
    total = 0
    for field in ['prep', 'cook']:
        t = recipe.get(field, '')
        if 'min' in t.lower():
            try:
                total += int(''.join(filter(str.isdigit, t.split('min')[0].split()[-1])))
            except:
                pass
        if 'hour' in t.lower() or 'hr' in t.lower():
            try:
                total += int(''.join(filter(str.isdigit, t.split('hour')[0].split('hr')[0].split()[-1]))) * 60
            except:
                pass
    return total if total > 0 else 30  # default 30 min

def generate_page(title, description, recipes, slug, meta_title=None):
    """Generate a landing page HTML"""
    recipe_items = "\n".join([
        f'''        <a href="/recipes/{r['id']}/" class="recipe-card">
          <span class="recipe-title">{r['title']}</span>
          <span class="recipe-meta">{r.get('prep', '')} + {r.get('cook', '')} · {r.get('serves', r.get('makes', ''))}</span>
        </a>''' for r in recipes
    ])
    
    meta_t = meta_title or title
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta_t} | rcpbx</title>
  <meta name="description" content="{description[:155]}">
  <link rel="canonical" href="{SITE_URL}/{slug}/">
  <meta property="og:title" content="{meta_t} | rcpbx">
  <meta property="og:description" content="{description[:155]}">
  <meta property="og:url" content="{SITE_URL}/{slug}/">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"CollectionPage","name":"{title}","description":"{description[:155]}","url":"{SITE_URL}/{slug}/"}}
  </script>
  <style>
    :root {{ --bg: #faf9f6; --text: #222; --text-muted: #666; --border: #ddd; --accent: #16a34a; }}
    @media (prefers-color-scheme: dark) {{ :root {{ --bg: #111; --text: #e5e5e5; --text-muted: #999; --border: #333; --accent: #22c55e; }} }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; padding: 2rem; }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
    .subtitle {{ color: var(--text-muted); margin-bottom: 2rem; font-size: 1.1rem; }}
    .count {{ color: var(--accent); font-weight: 600; }}
    .recipes {{ display: grid; gap: 0.75rem; }}
    .recipe-card {{ display: flex; flex-direction: column; gap: 0.25rem; padding: 1rem; border: 1px solid var(--border); border-radius: 8px; text-decoration: none; color: var(--text); transition: border-color 0.15s; }}
    .recipe-card:hover {{ border-color: var(--accent); }}
    .recipe-title {{ font-weight: 600; }}
    .recipe-meta {{ font-size: 0.85rem; color: var(--text-muted); }}
    .back {{ display: inline-block; margin-bottom: 2rem; color: var(--text-muted); text-decoration: none; font-size: 0.9rem; }}
    .back:hover {{ color: var(--accent); }}
    footer {{ margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border); text-align: center; font-size: 0.8rem; color: var(--text-muted); }}
    footer a {{ color: var(--accent); text-decoration: none; }}
  </style>
</head>
<body>
  <div class="container">
    <a href="/" class="back">← all recipes</a>
    <h1>{title}</h1>
    <p class="subtitle">{description} <span class="count">{len(recipes)} recipes</span></p>
    <div class="recipes">
{recipe_items}
    </div>
    <footer><a href="/">rcpbx.com</a> · no life stories · no ads</footer>
  </div>
</body>
</html>'''

def main():
    recipes = load_recipes()
    print(f"Loaded {len(recipes)} recipes")
    
    pages_created = 0
    sitemap_entries = []
    
    # === TIME-BASED PAGES ===
    time_buckets = {
        "15-minute-meals": ("15-Minute Meals", "Dinner on the table in 15 minutes or less.", 15),
        "30-minute-meals": ("30-Minute Meals", "Quick recipes ready in half an hour.", 30),
        "under-1-hour": ("Under 1 Hour", "Recipes ready in under an hour.", 60),
    }
    
    for slug, (title, desc, max_mins) in time_buckets.items():
        matching = [r for r in recipes if extract_cook_time_minutes(r) <= max_mins]
        if matching:
            Path(slug).mkdir(exist_ok=True)
            html = generate_page(title, desc, matching, slug)
            Path(f"{slug}/index.html").write_text(html)
            sitemap_entries.append(slug)
            pages_created += 1
            print(f"  ✓ /{slug}/ ({len(matching)} recipes)")
    
    # === METHOD-BASED PAGES ===
    methods = {
        "air-fryer": ("Air Fryer Recipes", "Crispy, fast, easy. Air fryer everything."),
        "instant-pot": ("Instant Pot Recipes", "Pressure cooker meals, set and forget."),
        "slow-cooker": ("Slow Cooker Recipes", "Dump it, leave it, come home to dinner."),
        "one-pot": ("One-Pot Meals", "Everything cooks together. Minimal cleanup."),
        "sheet-pan": ("Sheet Pan Dinners", "Everything on one pan. Into the oven."),
        "grilled": ("Grilled Recipes", "Fire and smoke. Summer cooking."),
        "no-cook": ("No-Cook Recipes", "Zero heat required."),
        "baked": ("Baked Recipes", "Into the oven, hands off."),
    }
    
    method_keywords = {
        "air-fryer": ["air fryer", "air-fryer"],
        "instant-pot": ["instant pot", "pressure cooker"],
        "slow-cooker": ["slow cooker", "crockpot", "crock pot"],
        "one-pot": ["one pot", "one-pot"],
        "sheet-pan": ["sheet pan", "sheet-pan"],
        "grilled": ["grill", "grilled", "bbq", "barbecue"],
        "no-cook": ["no cook", "no-cook", "raw"],
        "baked": ["bake", "baked", "roast", "roasted", "oven"],
    }
    
    for slug, (title, desc) in methods.items():
        keywords = method_keywords[slug]
        matching = []
        for r in recipes:
            text = f"{r.get('title', '')} {' '.join(r.get('steps', []))} {' '.join(r.get('notes', []))}".lower()
            if any(kw in text for kw in keywords):
                matching.append(r)
        if len(matching) >= 3:  # Only create page if 3+ recipes
            Path(slug).mkdir(exist_ok=True)
            html = generate_page(title, desc, matching, slug)
            Path(f"{slug}/index.html").write_text(html)
            sitemap_entries.append(slug)
            pages_created += 1
            print(f"  ✓ /{slug}/ ({len(matching)} recipes)")
    
    # === PROTEIN/INGREDIENT PAGES ===
    proteins = {
        "chicken-recipes": ("Chicken Recipes", "Every chicken recipe you need.", ["chicken"]),
        "beef-recipes": ("Beef Recipes", "Steaks, roasts, ground beef, and more.", ["beef", "steak", "burger"]),
        "pork-recipes": ("Pork Recipes", "Chops, tenderloin, ribs, and bacon.", ["pork", "bacon", "ham"]),
        "seafood-recipes": ("Seafood Recipes", "Fish, shrimp, and everything from the sea.", ["salmon", "shrimp", "fish", "cod", "tuna", "crab", "seafood"]),
        "vegetarian-recipes": ("Vegetarian Recipes", "No meat, all flavor.", []),  # Special handling
        "egg-recipes": ("Egg Recipes", "Scrambled, poached, baked, and beyond.", ["egg", "eggs", "omelette", "quiche"]),
        "pasta-recipes": ("Pasta Recipes", "Noodles in every form.", ["pasta", "spaghetti", "penne", "lasagna", "linguine", "fettuccine"]),
    }
    
    # Define meat keywords for vegetarian detection
    meat_keywords = ["chicken", "beef", "pork", "bacon", "ham", "steak", "burger", "salmon", "shrimp", "fish", "cod", "tuna", "crab", "seafood", "meat", "sausage", "turkey", "lamb"]
    
    for slug, (title, desc, keywords) in proteins.items():
        if slug == "vegetarian-recipes":
            # Special: recipes without meat
            matching = []
            for r in recipes:
                text = f"{r.get('title', '')} {' '.join(r.get('ingredients', []))}".lower()
                if not any(kw in text for kw in meat_keywords):
                    matching.append(r)
        else:
            matching = []
            for r in recipes:
                text = f"{r.get('title', '')} {' '.join(r.get('ingredients', []))}".lower()
                if any(kw in text for kw in keywords):
                    matching.append(r)
        
        if len(matching) >= 3:
            Path(slug).mkdir(exist_ok=True)
            html = generate_page(title, desc, matching, slug)
            Path(f"{slug}/index.html").write_text(html)
            sitemap_entries.append(slug)
            pages_created += 1
            print(f"  ✓ /{slug}/ ({len(matching)} recipes)")
    
    # === MEAL TYPE PAGES ===
    meal_types = {
        "breakfast-recipes": ("Breakfast Recipes", "Start your day right.", "breakfast"),
        "dinner-recipes": ("Dinner Recipes", "What's for dinner? This.", "dinner"),
        "dessert-recipes": ("Dessert Recipes", "Sweet endings.", "baking-dessert"),
        "side-dishes": ("Side Dishes", "The supporting cast.", "sides"),
        "soup-recipes": ("Soup Recipes", "Warm, comforting, soupy.", "soups-stews"),
    }
    
    for slug, (title, desc, cat_match) in meal_types.items():
        matching = [r for r in recipes if r.get('categorySlug') == cat_match]
        if len(matching) >= 3:
            Path(slug).mkdir(exist_ok=True)
            html = generate_page(title, desc, matching, slug)
            Path(f"{slug}/index.html").write_text(html)
            sitemap_entries.append(slug)
            pages_created += 1
            print(f"  ✓ /{slug}/ ({len(matching)} recipes)")
    
    # === EASY/BEGINNER PAGES ===
    easy_keywords = ["easy", "simple", "beginner", "quick", "basic"]
    easy_recipes = []
    for r in recipes:
        # Short ingredient list + short steps = easy
        if len(r.get('ingredients', [])) <= 8 and len(r.get('steps', [])) <= 6:
            easy_recipes.append(r)
    
    if easy_recipes:
        Path("easy-recipes").mkdir(exist_ok=True)
        html = generate_page("Easy Recipes", "Simple recipes anyone can make. Few ingredients, clear steps.", easy_recipes, "easy-recipes")
        Path("easy-recipes/index.html").write_text(html)
        sitemap_entries.append("easy-recipes")
        pages_created += 1
        print(f"  ✓ /easy-recipes/ ({len(easy_recipes)} recipes)")
    
    # === HEALTHY RECIPES (no heavy cream, less butter, etc) ===
    unhealthy_keywords = ["heavy cream", "cream cheese", "deep fry", "fried", "bacon", "sugar", "frosting", "chocolate"]
    healthy_recipes = []
    for r in recipes:
        text = f"{' '.join(r.get('ingredients', []))}".lower()
        if not any(kw in text for kw in unhealthy_keywords):
            healthy_recipes.append(r)
    
    if len(healthy_recipes) >= 10:
        Path("healthy-recipes").mkdir(exist_ok=True)
        html = generate_page("Healthy Recipes", "Lighter options. Less cream, less sugar, more vegetables.", healthy_recipes[:50], "healthy-recipes")
        Path("healthy-recipes/index.html").write_text(html)
        sitemap_entries.append("healthy-recipes")
        pages_created += 1
        print(f"  ✓ /healthy-recipes/ ({len(healthy_recipes)} recipes)")

    # === WHAT TO MAKE WITH [INGREDIENT] PAGES ===
    common_ingredients = {
        "chicken-breast": (["chicken breast"], "What to Make with Chicken Breast"),
        "ground-beef": (["ground beef"], "What to Make with Ground Beef"),
        "eggs": (["egg", "eggs"], "What to Make with Eggs"),
        "potatoes": (["potato", "potatoes"], "What to Make with Potatoes"),
        "rice": (["rice"], "What to Make with Rice"),
        "pasta": (["pasta", "spaghetti", "penne", "noodle"], "What to Make with Pasta"),
    }
    
    for slug, (keywords, title) in common_ingredients.items():
        matching = []
        for r in recipes:
            ing_text = ' '.join(r.get('ingredients', [])).lower()
            if any(kw in ing_text for kw in keywords):
                matching.append(r)
        if len(matching) >= 3:
            full_slug = f"what-to-make-with-{slug}"
            Path(full_slug).mkdir(exist_ok=True)
            html = generate_page(title, f"Got {slug.replace('-', ' ')}? Here's what to make.", matching, full_slug, meta_title=title)
            Path(f"{full_slug}/index.html").write_text(html)
            sitemap_entries.append(full_slug)
            pages_created += 1
            print(f"  ✓ /{full_slug}/ ({len(matching)} recipes)")

    print(f"\n✅ Generated {pages_created} programmatic SEO pages")
    
    # Return sitemap entries for updating
    return sitemap_entries

if __name__ == "__main__":
    entries = main()
