# >rcpbx — the recipe box

**[rcpbx.com](https://rcpbx.com)** · 164 recipes · no ads, no life stories, no popups, no accounts. Just the recipe.

Every viral recipe is a claim. **[We cook it and file the verdict.](https://rcpbx.com/trends/)** WORTH IT / OVERHYPED / SKIP — dated, permanent, and occasionally unflattering. The failures get buried in [the SKIP file](https://rcpbx.com/skips/).

## Why this exists

Recipe websites have become unbearable: 2,000 words about someone's grandmother, three popups, an autoplay video, and an ad between every step. This is the antidote — a **recipe terminal**: recipes run like software, not media. Tested before publish. Versioned. Open data. [What we refuse, in writing.](https://rcpbx.com/never/)

## The open recipe API (no key, no rate limit, CORS open)

```bash
curl -s https://rcpbx.com/data/index.json | jq length          # 164
curl -s https://rcpbx.com/data/buldak-carbonara.json | jq .verdict
curl -s https://rcpbx.com/recipes/caesar-salad/index.md        # markdown mirror
```

| Endpoint | What |
|---|---|
| `/data/index.json` | all recipes: id, title, tagline, category, times |
| `/data/{id}.json` | full recipe: ingredients, steps, notes, troubleshooting, tested date, verdict |
| `/data/radar.json` | the trend radar — verdicts on viral recipes |
| `/recipes/{id}/index.md` | markdown mirror of any recipe |
| `/llms-full.txt` | the whole corpus, one file |

**License:** data CC-BY-4.0 (credit rcpbx.com) · code MIT. Docs: [rcpbx.com/api](https://rcpbx.com/api/)

## Features

Cook mode on every recipe (tap-to-check ingredients, step focus, tappable timers, wake lock), serving scaler, save-to-box with a combined grocery list (localStorage, no account), QR print cards, full keyboard + screen-reader support, dark mode, 30KB pages. Built with Python scripts + GitHub Pages. No frameworks, no build servers, no tracking beyond basic analytics.

## Contributing

Recipe *requests* and **"I tested this"** reports are welcome via [issues](../../issues). Recipe submissions go through [rcpbx.com/request](https://rcpbx.com/request/) — the canon is curated, not accumulated: one recipe per dish, tested before it enters. Typo and clarity fixes: PRs welcome.

## Build

```bash
pip install pillow segno
python3 build.py && python3 generate-seo-pages.py && python3 make-radar.py \
  && python3 make-cards.py && python3 make-llms.py && python3 make-feed.py
```

Pushes to `main` build and deploy automatically via GitHub Actions.
