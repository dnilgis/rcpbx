#!/usr/bin/env python3
"""
rcpbx Static Site Generator
Generates SEO-optimized static HTML for every recipe.
Run: python build.py
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

# Config
SITE_URL = "https://rcpbx.com"
BUILD_DIR = Path("recipes")
DATA_DIR = Path("data")

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def load_recipes():
    recipes = []
    for f in sorted(DATA_DIR.glob("*.json")):
        if f.name == "index.json":
            continue
        with open(f) as fp:
            recipes.append(json.load(fp))
    return recipes

def get_category_name(slug):
    names = {
        'soups-stews': 'Soups & Stews',
        'pasta': 'Pasta',
        'chicken': 'Chicken',
        'beef': 'Beef',
        'pork': 'Pork',
        'seafood': 'Seafood',
        'breakfast': 'Breakfast',
        'sides': 'Sides',
        'baking-dessert': 'Baking & Desserts',
        'basics': 'Basics'
    }
    return names.get(slug, slug.title())

def estimate_total_time(prep, cook):
    """Convert '10 min' + '30 min' to 'PT40M' ISO 8601 duration"""
    total_mins = 0
    for t in [prep, cook]:
        if not t:
            continue
        match = re.search(r'(\d+)\s*(min|hour|hr)', t.lower())
        if match:
            val = int(match.group(1))
            if 'hour' in match.group(2) or 'hr' in match.group(2):
                val *= 60
            total_mins += val
    if total_mins == 0:
        return None
    hours = total_mins // 60
    mins = total_mins % 60
    if hours and mins:
        return f"PT{hours}H{mins}M"
    elif hours:
        return f"PT{hours}H"
    else:
        return f"PT{mins}M"

def generate_recipe_schema(recipe):
    """Generate JSON-LD Recipe schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": recipe['title'],
        "description": recipe.get('description', recipe.get('tagline', '')),
        "author": {
            "@type": "Organization",
            "name": "rcpbx"
        },
        "datePublished": "2024-01-01",
        "prepTime": estimate_total_time(recipe.get('prep', ''), ''),
        "cookTime": estimate_total_time('', recipe.get('cook', '')),
        "totalTime": estimate_total_time(recipe.get('prep', ''), recipe.get('cook', '')),
        "recipeYield": recipe.get('serves', recipe.get('makes', '4 servings')),
        "recipeCategory": recipe.get('category', ''),
        "recipeIngredient": recipe.get('ingredients', []),
        "recipeInstructions": [
            {"@type": "HowToStep", "text": step} 
            for step in recipe.get('steps', [])
        ],
        "url": f"{SITE_URL}/recipes/{recipe['id']}/"
    }
    # Clean None values
    schema = {k: v for k, v in schema.items() if v is not None}
    return json.dumps(schema, indent=2)

def generate_breadcrumb_schema(recipe):
    """Generate BreadcrumbList schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": SITE_URL
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": get_category_name(recipe.get('categorySlug', '')),
                "item": f"{SITE_URL}/?category={recipe.get('categorySlug', '')}"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": recipe['title'],
                "item": f"{SITE_URL}/recipes/{recipe['id']}/"
            }
        ]
    }
    return json.dumps(schema, indent=2)

def generate_recipe_html(recipe):
    """Generate full static HTML page for a recipe"""
    
    title = recipe['title']
    recipe_id = recipe['id']
    tagline = recipe.get('tagline', '')
    description = recipe.get('description', tagline)
    category = recipe.get('category', '')
    category_slug = recipe.get('categorySlug', '')
    prep = recipe.get('prep', '')
    cook = recipe.get('cook', '')
    serves = recipe.get('serves', recipe.get('makes', ''))
    ingredients = recipe.get('ingredients', [])
    steps = recipe.get('steps', [])
    notes = recipe.get('notes', [])
    source = recipe.get('source', '')
    source_url = recipe.get('sourceUrl', '')
    
    # Meta description (max 160 chars)
    meta_desc = f"{title}: {tagline}"[:157] + "..." if len(f"{title}: {tagline}") > 160 else f"{title}: {tagline}"
    
    # Generate ingredients HTML
    ingredients_html = "\n".join([f'        <li class="ingredient">{ing}</li>' for ing in ingredients])
    
    # Generate steps HTML  
    steps_html = "\n".join([f'        <li class="step">{step}</li>' for i, step in enumerate(steps)])
    
    # Generate notes HTML
    notes_html = ""
    if notes:
        notes_items = "\n".join([f'        <li>{note}</li>' for note in notes])
        notes_html = f'''
    <section class="notes">
      <h2>Notes</h2>
      <ul>
{notes_items}
      </ul>
    </section>'''

    # Source attribution
    source_html = ""
    if source:
        if source_url:
            source_html = f'<p class="source">{source} · <a href="{source_url}" target="_blank" rel="noopener">Original</a></p>'
        else:
            source_html = f'<p class="source">{source}</p>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | rcpbx</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90' font-family='monospace' fill='%2316a34a'>%3E</text></svg>">
  
  <!-- SEO -->
  <meta name="description" content="{meta_desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE_URL}/recipes/{recipe_id}/">
  
  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE_URL}/recipes/{recipe_id}/">
  <meta property="og:title" content="{title} | rcpbx">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:site_name" content="rcpbx">
  <meta property="og:image" content="{SITE_URL}/og-image.svg">
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | rcpbx">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{SITE_URL}/og-image.svg">
  
  <!-- Recipe Schema -->
  <script type="application/ld+json">
{generate_recipe_schema(recipe)}
  </script>
  
  <!-- Breadcrumb Schema -->
  <script type="application/ld+json">
{generate_breadcrumb_schema(recipe)}
  </script>
  
  <!-- Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-E2VNWY2BFX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-E2VNWY2BFX');
  </script>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #faf9f6;
      --text: #222;
      --text-muted: #666;
      --border: #ddd;
      --accent: #16a34a;
      --accent-light: #dcfce7;
      --font-sans: 'Inter', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #111;
        --text: #e5e5e5;
        --text-muted: #999;
        --border: #333;
        --accent: #22c55e;
        --accent-light: #14532d;
      }}
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ font-family: var(--font-sans); background: var(--bg); color: var(--text); line-height: 1.6; }}
    body {{ min-height: 100vh; }}
    
    header {{
      border-bottom: 1px solid var(--border);
      padding: 1rem 1.5rem;
    }}
    .header-inner {{
      max-width: 800px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .logo {{
      font-family: var(--font-mono);
      font-size: 1.25rem;
      font-weight: 600;
      text-decoration: none;
      color: var(--text);
    }}
    .logo-prefix {{ color: var(--accent); }}
    .breadcrumb {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    .breadcrumb a {{
      color: var(--text-muted);
      text-decoration: none;
    }}
    .breadcrumb a:hover {{ color: var(--accent); }}
    
    main {{
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
    }}
    
    .recipe-header {{
      margin-bottom: 2rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid var(--border);
    }}
    h1 {{
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
    }}
    .tagline {{
      font-size: 1.1rem;
      color: var(--text-muted);
      margin-bottom: 1rem;
    }}
    .meta {{
      display: flex;
      gap: 1.5rem;
      font-size: 0.9rem;
      color: var(--text-muted);
    }}
    .meta-item {{
      display: flex;
      align-items: center;
      gap: 0.3rem;
    }}
    .meta-label {{
      font-weight: 500;
      color: var(--text);
    }}
    
    .recipe-grid {{
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 2rem;
    }}
    @media (max-width: 700px) {{
      .recipe-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    
    section {{
      margin-bottom: 2rem;
    }}
    h2 {{
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 1rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }}
    
    .ingredients ul {{
      list-style: none;
    }}
    .ingredient {{
      padding: 0.5rem 0;
      border-bottom: 1px solid var(--border);
    }}
    .ingredient:last-child {{
      border-bottom: none;
    }}
    
    .steps ol {{
      list-style: none;
      counter-reset: step;
    }}
    .step {{
      counter-increment: step;
      padding: 0.75rem 0;
      padding-left: 2.5rem;
      position: relative;
      border-bottom: 1px solid var(--border);
    }}
    .step:last-child {{
      border-bottom: none;
    }}
    .step::before {{
      content: counter(step);
      position: absolute;
      left: 0;
      top: 0.75rem;
      width: 1.75rem;
      height: 1.75rem;
      background: var(--accent);
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.8rem;
      font-weight: 600;
    }}
    
    .notes {{
      background: var(--accent-light);
      padding: 1.25rem;
      border-radius: 8px;
      margin-top: 2rem;
    }}
    .notes h2 {{
      color: var(--accent);
      margin-bottom: 0.75rem;
    }}
    .notes ul {{
      list-style: none;
    }}
    .notes li {{
      padding: 0.4rem 0;
      padding-left: 1.25rem;
      position: relative;
    }}
    .notes li::before {{
      content: "→";
      position: absolute;
      left: 0;
      color: var(--accent);
    }}
    
    .source {{
      margin-top: 2rem;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}
    .source a {{
      color: var(--accent);
      text-decoration: none;
    }}
    .source a:hover {{
      text-decoration: underline;
    }}
    
    footer {{
      border-top: 1px solid var(--border);
      padding: 1.5rem;
      text-align: center;
      margin-top: 3rem;
    }}
    .footer-text {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
    .footer-text a {{
      color: var(--accent);
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <a href="/" class="logo"><span class="logo-prefix">&gt;</span>rcpbx</a>
      <nav class="breadcrumb">
        <a href="/">Home</a> / <a href="/?category={category_slug}">{category}</a> / {title}
      </nav>
    </div>
  </header>
  
  <main>
    <article>
      <div class="recipe-header">
        <h1>{title}</h1>
        <p class="tagline">{tagline}</p>
        <div class="meta">
          <span class="meta-item"><span class="meta-label">Prep:</span> {prep}</span>
          <span class="meta-item"><span class="meta-label">Cook:</span> {cook}</span>
          <span class="meta-item"><span class="meta-label">Serves:</span> {serves}</span>
        </div>
      </div>
      
      <div class="recipe-grid">
        <section class="ingredients">
          <h2>Ingredients</h2>
          <ul>
{ingredients_html}
          </ul>
        </section>
        
        <section class="steps">
          <h2>Instructions</h2>
          <ol>
{steps_html}
          </ol>
        </section>
      </div>
      {notes_html}
      
      {source_html}
    </article>
  </main>
  
  <footer>
    <p class="footer-text">
      <a href="/">rcpbx.com</a> · 142 recipes · no life stories · no ads
    </p>
  </footer>
</body>
</html>'''
    
    return html

def generate_sitemap(recipes):
    """Generate sitemap.xml with all static recipe URLs"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.w3.org/schemas/sitemap/0.9">
  <url>
    <loc>https://rcpbx.com/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://rcpbx.com/about/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://rcpbx.com/reference/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
'''.format(today=today)

    # Categories
    categories = ['soups-stews', 'pasta', 'chicken', 'beef', 'pork', 'seafood', 'breakfast', 'sides', 'baking-dessert', 'basics']
    for cat in categories:
        xml += f'''  <url>
    <loc>https://rcpbx.com/?category={cat}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''

    # All recipes with clean URLs
    for recipe in recipes:
        xml += f'''  <url>
    <loc>https://rcpbx.com/recipes/{recipe['id']}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''

    xml += '</urlset>'
    return xml

def main():
    print("🍳 rcpbx Static Site Generator")
    print("=" * 40)
    
    recipes = load_recipes()
    print(f"📖 Loaded {len(recipes)} recipes")
    
    # Create recipe directories and HTML files
    generated = 0
    for recipe in recipes:
        recipe_dir = BUILD_DIR / recipe['id']
        recipe_dir.mkdir(parents=True, exist_ok=True)
        
        html = generate_recipe_html(recipe)
        (recipe_dir / "index.html").write_text(html)
        generated += 1
    
    print(f"✅ Generated {generated} static recipe pages")
    
    # Generate sitemap
    sitemap = generate_sitemap(recipes)
    Path("sitemap.xml").write_text(sitemap)
    print("✅ Generated sitemap.xml")
    
    print("=" * 40)
    print("🚀 Build complete!")
    print(f"   Static pages: recipes/*/index.html")
    print(f"   Clean URLs: /recipes/chicken-parmesan/")

if __name__ == "__main__":
    main()
