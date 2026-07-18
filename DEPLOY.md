# rcpbx v2 deploy — panel-review build (2026-07-18)

## What this is

The full implementation of the expert-panel review: cook mode, serving scaler,
save-to-box + grocery list, hot-now rail, the public Radar, PNG share cards,
llms.txt, fixed SEO pages, fixed recipe data (temps, protein math, pistachio
cream), and 8 new July-2026 trend recipes. Total: **161 recipes**.

## Deploy steps — the two script runs are NOT optional

1. **Unzip everything into the repo root**, overwriting existing files.
2. **Run the build against your full data:**
   ```
   python3 build.py              # regenerates ALL 161 recipe pages with cook mode,
                                 # enriches data/index.json with times, rebuilds sitemap
   python3 generate-seo-pages.py # regenerates the 25 landing pages from full data
   python3 make-cards.py         # regenerates share cards (needs: pip install pillow)
   python3 make-llms.py          # regenerates llms.txt + markdown mirrors
   ```
   Why not optional: this zip was built where only 19 recipes had full JSON
   data, so some landing pages (15-minute-meals, what-to-make-with-*) currently
   list only those. Running the scripts in the repo — where all 161 full JSONs
   live — restores the full lists everywhere, WITH the fixes (no more frosting
   as a 15-minute meal, no more tacos under Chicken, no more " + · 4").
3. Commit and push. Resubmit `sitemap.xml` in Search Console.

## What changed (highlights)

- **Every recipe page**: tap-to-check ingredients, tap-to-focus steps, tappable
  timers with beep, wake-lock "screen on" toggle, −/+ serving scaler, save to
  box, real breadcrumbs, related recipes, troubleshooting sections, Recipe
  schema with images (rich-result eligible for the first time), real dates.
- **`/box/`** (new): saved recipes + combined checkable grocery list. localStorage only.
- **`/trends/`**: rebuilt as "The Radar" — public, honest, dated weekly editions.
  Update it weekly (it's hand-edited HTML by design — 5 minutes).
- **`data/hot.json`**: powers the homepage HOT NOW rail. Update weekly.
- **Homepage**: hot-now rail, "> tonight:" row, footer hub links (de-orphaned all
  25 landing pages), fixed search (canonical links, visible results, easter eggs
  no longer fire over real results), view counter removed.
- **Share cards**: og-image.png + per-recipe /recipes/{id}/card.png (SVG og images
  render on zero platforms; these fix every link preview + Google Recipe image requirement).
- **llms.txt / llms-full.txt / index.md mirrors**: the AI-answer-engine play.
- **Recipe fixes** (the chef's list): thigh temp 175–185°F, protein math that
  adds up, Dubai bar with real pistachio cream + temper option, flourless
  flatbread as primary, Caesar with 4–6 anchovies + neutral oil, honest salmon
  bowl attribution, salt types specified.

## Weekly cadence (replaces "deploy and forget")

Monday, ~30 min: scan Google Trends rising food queries + TikTok Creative
Center. Pick ONE trend. Cook it during the week. Friday: add `data/{id}.json`
(include `tested`, `testedNote`, `verdict`, `troubleshooting`), update
`data/hot.json` and `/trends/index.html`, run the 4 scripts, push.
Trend-to-published target: 7–14 days.

## Still yours to do (from the panel report)

- The Show HN launch ("161 recipes, zero ads, open JSON, 30KB pages") — do it
  after this deploys.
- Voice pass on the ~80 beige taglines; keep or kill the easter eggs.
- Optional: drop JetBrainsMono TTFs into `assets/fonts/` and re-run
  make-cards.py for pixel-perfect brand cards.
