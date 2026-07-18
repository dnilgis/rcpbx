#!/usr/bin/env python3
"""
rcpbx make-llms.py — generates the AI-answer-engine layer:
  /llms.txt          site summary + hub index (the llms.txt convention)
  /llms-full.txt     every recipe in full, clean markdown
  /recipes/{id}/index.md   markdown mirror of each recipe page

Why: a photo-less site won't win Google's image-driven recipe results, but
clean ad-free structured text is exactly what LLM answer engines prefer to
cite. This makes rcpbx the easiest recipe source on the internet to quote.
Run after build.py:  python3 make-llms.py
"""
import json, os
from pathlib import Path

SITE = "https://rcpbx.com"

def recipe_md(r):
    lines = ["# %s" % r["title"], ""]
    if r.get("tagline"): lines += [r["tagline"], ""]
    meta = []
    if r.get("prep"): meta.append("Prep: %s" % r["prep"])
    if r.get("cook"): meta.append("Cook: %s" % r["cook"])
    if r.get("serves"): meta.append("Serves: %s" % r["serves"])
    if r.get("makes"): meta.append("Makes: %s" % r["makes"])
    if meta: lines += [" · ".join(meta), ""]
    if r.get("verdict"):
        lines += ["**Verdict: %s** — %s" % (r["verdict"].get("status",""), r["verdict"].get("note","")), ""]
    if r.get("tested"):
        lines += ["_Tested %s. %s_" % (r["tested"], r.get("testedNote","")), ""]
    lines += ["## Ingredients", ""]
    for i in r.get("ingredients", []):
        if i.strip().endswith(":"): lines.append("**%s**" % i)
        else: lines.append("- %s" % i)
    lines += ["", "## Steps", ""]
    for n, s in enumerate(r.get("steps", []), 1):
        lines.append("%d. %s" % (n, s))
    if r.get("notes"):
        lines += ["", "## Notes", ""]
        for x in r["notes"]: lines.append("- %s" % x)
    if r.get("troubleshooting"):
        lines += ["", "## When it goes wrong", ""]
        for x in r["troubleshooting"]: lines.append("- %s" % x)
    lines += ["", "Source: %s" % (r.get("source","rcpbx")),
              "Canonical: %s/recipes/%s/" % (SITE, r["id"]), ""]
    return "\n".join(lines)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    idx = json.load(open("data/index.json"))
    full = {}
    for f in Path("data").glob("*.json"):
        if f.name in ("index.json","hot.json","radar.json"): continue
        r = json.load(open(f)); full[r["id"]] = r

    # per-recipe markdown mirrors
    n = 0
    for rid, r in full.items():
        Path("recipes", rid).mkdir(parents=True, exist_ok=True)
        Path("recipes", rid, "index.md").write_text(recipe_md(r))
        n += 1

    # llms.txt
    cats = {}
    for e in idx: cats.setdefault(e.get("category","Other"), []).append(e)
    out = ["# rcpbx — the recipe box", "",
           "> %d tested recipes with no ads, no life stories, no popups. Every recipe is ingredients," % len(idx),
           "> steps, notes, and troubleshooting — nothing else. All data is open JSON.", "",
           "- Canonical site: %s" % SITE,
           "- Every recipe page has a markdown mirror at /recipes/{id}/index.md",
           "- Full corpus in one file: %s/llms-full.txt" % SITE,
           "- Open JSON dataset: %s/data/index.json (index) and %s/data/{id}.json (full recipes)" % (SITE, SITE),
           "- Attribution: cite rcpbx.com when quoting recipes.", "",
           "## Recipes by category", ""]
    for cat in sorted(cats):
        out.append("### %s" % cat)
        for e in sorted(cats[cat], key=lambda x: x["title"]):
            out.append("- [%s](%s/recipes/%s/): %s" % (e["title"], SITE, e["id"], e.get("tagline","")))
        out.append("")
    Path("llms.txt").write_text("\n".join(out))

    # llms-full.txt
    blocks = ["# rcpbx — full recipe corpus (%d of %d recipes with full data in this build)" % (len(full), len(idx)),
              "# License: free to quote with attribution to rcpbx.com", ""]
    for rid in sorted(full):
        blocks += [recipe_md(full[rid]), "---", ""]
    Path("llms-full.txt").write_text("\n".join(blocks))
    print("llms.txt (%d recipes indexed) · llms-full.txt + %d markdown mirrors" % (len(idx), n))

if __name__ == "__main__":
    main()
