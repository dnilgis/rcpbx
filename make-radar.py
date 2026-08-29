#!/usr/bin/env python3
"""
rcpbx make-radar.py — the Radar engine. From data/radar.json generates:
  /trends/                     live board (current edition)
  /trends/{edition}/           frozen permanent edition (e.g. /trends/2026-w35/)
  /radar/{slug}/               verdict permalink per tested trend, with FAQPage schema
  /skips/                      the SKIP File (permanent graveyard, honest empty state)
Weekly owner flow: edit data/radar.json (bump edition, add/move entries), push. CI does the rest.
"""
import json, os, html, re
from pathlib import Path

SITE = "https://rcpbx.com"
def esc(s): return html.escape(str(s), quote=True)

CSS = """
    :root { --bg:#0d0d0d; --bg-alt:#161616; --text:#e5e5e5; --text-muted:#a3a3a3; --text-dim:#8a8a8a;
      --border:#2a2a2a; --accent:#22c55e; --amber:#f59e0b; --red:#ef4444;
      --font-sans:'Inter',-apple-system,sans-serif; --font-mono:'JetBrains Mono',monospace; }
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    html{font-family:var(--font-mono);background:var(--bg);color:var(--text);line-height:1.6}
    .skip-link{position:absolute;left:-9999px;top:0;background:var(--accent);color:#000;padding:.5rem 1rem;z-index:999;font-family:var(--font-mono)}
    .skip-link:focus{left:0}
    header{border-bottom:1px solid var(--border);padding:1rem 1.5rem}
    .header-inner{max-width:760px;margin:0 auto;display:flex;justify-content:space-between;align-items:center}
    .logo{font-size:1.25rem;font-weight:600;text-decoration:none;color:var(--text)}
    .logo-prefix{color:var(--accent)}
    .header-link{font-size:.7rem;color:var(--text-muted);text-decoration:none;text-transform:uppercase;letter-spacing:.05em}
    .header-link:hover{color:var(--accent)}
    main{max-width:760px;margin:0 auto;padding:2.5rem 1.5rem}
    h1{font-family:var(--font-sans);font-size:1.7rem;font-weight:700;letter-spacing:-.02em}
    h1::before{content:"> ";color:var(--accent);font-family:var(--font-mono)}
    .sub{color:var(--text-muted);font-size:.8rem;margin:.5rem 0 .25rem;font-family:var(--font-sans)}
    .sub a{color:var(--accent)}
    .edition{font-size:.68rem;color:var(--text-dim);margin-bottom:2rem}
    .edition span{color:var(--accent)}
    .scoreline{font-size:.7rem;color:var(--text-muted);border:1px solid var(--border);border-radius:6px;
      padding:.5rem .9rem;margin-bottom:1.5rem;display:inline-block}
    .scoreline b{color:var(--accent);font-weight:500}
    .legend{display:flex;gap:1rem;flex-wrap:wrap;font-size:.65rem;color:var(--text-dim);margin-bottom:1.5rem}
    .radar{border:1px solid var(--border);border-radius:8px;overflow:hidden;margin-bottom:2rem}
    .radar-head{display:grid;grid-template-columns:1fr 80px 140px;gap:.75rem;padding:.55rem 1rem;
      background:var(--bg-alt);font-size:.6rem;text-transform:uppercase;letter-spacing:.08em;color:var(--text-dim)}
    .row{display:grid;grid-template-columns:1fr 80px 140px;gap:.75rem;padding:.7rem 1rem;
      border-top:1px solid var(--border);font-size:.78rem;align-items:baseline}
    .row a{color:var(--text);text-decoration:none}
    .row a:hover{color:var(--accent)}
    .t-name{font-weight:500}
    .t-note{display:block;color:var(--text-dim);font-size:.65rem;margin-top:.1rem}
    .heat{color:var(--accent);letter-spacing:.1em;font-size:.7rem}
    .heat.h2{color:var(--amber)}.heat.h1{color:var(--text-dim)}
    .stamp{font-size:.6rem;letter-spacing:.06em;font-weight:500;padding:.18rem .45rem;border-radius:3px;
      border:1.5px solid;white-space:nowrap;text-decoration:none;display:inline-block}
    .stamp.s-worth{color:var(--accent);border-color:var(--accent)}
    .stamp.s-hype{color:var(--amber);border-color:var(--amber)}
    .stamp.s-skip{color:var(--red);border-color:var(--red)}
    .stamp.s-kitchen{color:var(--amber);border-color:transparent;padding-left:0}
    .stamp.s-watch{color:var(--text-dim);border-color:transparent;padding-left:0}
    h2{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:var(--text-muted);margin:0 0 .75rem}
    h2::before{content:"> ";color:var(--accent)}
    .how{border:1px dashed var(--border);border-radius:8px;padding:1rem 1.25rem;font-size:.72rem;
      color:var(--text-muted);font-family:var(--font-sans);line-height:1.7;margin-bottom:2rem}
    .how a{color:var(--accent)}
    .quote{font-family:var(--font-sans);font-style:italic;color:var(--text-muted);font-size:.85rem;
      border-left:2px solid var(--accent);padding-left:1rem;margin:1.5rem 0}
    .nextweek{font-size:.75rem;color:var(--text-muted);margin-bottom:2rem}
    .nextweek span{color:var(--accent)}
    .past{font-size:.7rem;color:var(--text-dim);line-height:2}
    .past a{color:var(--text-muted);text-decoration:none}
    .past a:hover{color:var(--accent)}
    footer{border-top:1px solid var(--border);padding:1.5rem;text-align:center}
    .footer-text{font-size:.7rem;color:var(--text-muted)}
    .footer-text a{color:var(--accent);text-decoration:none}
    @media(max-width:560px){.radar-head{display:none}.row{grid-template-columns:1fr;gap:.25rem}}
    @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}}
"""

def shell(title, desc, url, body, ogimage=None):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>{esc(title)}</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90' font-family='monospace' fill='%2316a34a'>%3E</text></svg>">
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:site_name" content="rcpbx">
  <meta property="og:image" content="{ogimage or SITE + '/og-image.png'}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{ogimage or SITE + '/og-image.png'}">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-E2VNWY2BFX"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-E2VNWY2BFX');</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header>
    <div class="header-inner">
      <a href="/" class="logo"><span class="logo-prefix">&gt;</span>rcpbx</a>
      <a href="/" class="header-link">← all recipes</a>
    </div>
  </header>
  <main id="main">
{body}
  </main>
  <footer>
    <p class="footer-text"><a href="/">rcpbx.com</a> · no life stories · no ads · <a href="/feed.xml">rss</a> · <a href="/skips/">the skip file</a></p>
  </footer>
</body>
</html>
"""

STATUS_CLASS = {"WORTH IT":"s-worth","OVERHYPED":"s-hype","SKIP":"s-skip","IN THE KITCHEN":"s-kitchen","WATCHING":"s-watch"}

def row_html(e):
    name = esc(e["name"]); note = esc(e.get("note",""))
    heat = "▲" * e.get("heat",1)
    hclass = "" if e.get("heat",1) >= 3 else (" h2" if e.get("heat") == 2 else " h1")
    sc = STATUS_CLASS.get(e["status"], "s-watch")
    if e.get("recipeId"):
        left = f'<a href="/recipes/{e["recipeId"]}/" class="t-name">{name}</a>'
    else:
        left = f'<span class="t-name">{name}</span>'
    if e.get("dateTested"):
        stamp = f'<a class="stamp {sc}" href="/radar/{e["slug"]}/">{esc(e["status"])} →</a>'
    else:
        stamp = f'<span class="stamp {sc}">{esc(e["status"])}</span>'
    return (f'      <div class="row"><span>{left}<span class="t-note">{note}</span></span>'
            f'<span class="heat{hclass}" aria-label="heat {e.get("heat",1)} of 3">{heat}</span>'
            f'<span>{stamp}</span></div>')

def board_html(r, frozen=False):
    entries = r["entries"]
    tested = [e for e in entries if e.get("dateTested")]
    worth = sum(1 for e in tested if e["status"] == "WORTH IT")
    hype = sum(1 for e in tested if e["status"] == "OVERHYPED")
    skips = sum(1 for e in tested if e["status"] == "SKIP")
    rows = "\n".join(row_html(e) for e in entries)
    year = r["date"][:4]
    frozen_note = "" if not frozen else f'<p class="sub">Frozen edition — the live board is at <a href="/trends/">/trends/</a>.</p>'
    quote = f'<div class="quote">"{esc(r["pullQuote"])}"</div>' if r.get("pullQuote") else ""
    nextweek = f'<p class="nextweek"><span>&gt; next week:</span> {esc(r["nextWeek"])}</p>' if r.get("nextWeek") else ""
    past = ""
    if not frozen:
        eds = sorted([p.name for p in Path("trends").iterdir() if p.is_dir() and re.match(r"\d{4}-w\d+", p.name)], reverse=True)
        if eds:
            links = " · ".join(f'<a href="/trends/{e}/">{e.upper()}</a>' for e in eds[:12])
            past = f'<h2>Past editions</h2><p class="past">{links}</p>'
    return f"""    <h1>The Radar</h1>
    <p class="sub">Every viral recipe is a claim. We cook it and file the verdict. The trend gets 15 seconds of fame; the verdict is forever.</p>
    {frozen_note}
    <p class="edition">edition <span>{esc(r["edition"])}</span> · {esc(r["date"])} · updates weekly</p>
    <p class="scoreline">{year} scoreboard: <b>{len(tested)}</b> tested · <b>{worth}</b> worth it · <b>{hype}</b> overhyped · <b>{skips}</b> killed → <a href="/skips/" style="color:var(--red);text-decoration:none">the skip file</a></p>
    <div class="legend">
      <span><span style="color:var(--accent)">WORTH IT</span> — tested, published, deserved the hype</span>
      <span><span style="color:var(--amber)">OVERHYPED</span> — tested, published, temper expectations</span>
      <span><span style="color:var(--red)">SKIP</span> — tested, failed, buried in <a href="/skips/" style="color:var(--red)">the skip file</a></span>
      <span><span style="color:var(--amber)">IN THE KITCHEN</span> — being tested now</span>
      <span><span style="color:var(--text-dim)">WATCHING</span> — on the list</span>
    </div>
    <div class="radar" role="table" aria-label="Trend radar">
      <div class="radar-head" role="row"><span>trend</span><span>heat</span><span>verdict</span></div>
{rows}
    </div>
    {nextweek}
    {quote}
    <h2>How this works</h2>
    <div class="how">
      One person, one kitchen, one rule: nothing gets published untested. Each week we pick the loudest trend,
      cook it for real, and file a verdict. Winners join the collection with a tested date and a changelog.
      Losers get a one-line obituary in <a href="/skips/">the SKIP file</a> so you don't waste the groceries.
      Methodology and receipts: <a href="/why/">/why</a>. Want something tested? <a href="/request/">Request it.</a>
    </div>
    {past}"""

def verdict_page(e, r):
    q = f"Is {e['name'][0].lower() + e['name'][1:]} worth making?"
    status = e["status"]; line = e.get("line","")
    ans = {"WORTH IT": "Yes", "OVERHYPED": "Sort of", "SKIP": "No"}.get(status, "")
    recipe_link = f'<p style="margin-top:1.5rem"><a class="stamp s-worth" href="/recipes/{e["recipeId"]}/" style="font-size:.75rem;padding:.5rem .9rem">→ the tested recipe</a></p>' if e.get("recipeId") else ""
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{
        "@type":"Question","name": q,
        "acceptedAnswer":{"@type":"Answer","text": f"{ans}. Verdict: {status}. {line} Tested {e['dateTested']} by rcpbx."}}]}
    sc = STATUS_CLASS.get(status,"s-worth")
    og = f"{SITE}/recipes/{e['recipeId']}/card.png" if e.get("recipeId") else None
    body = f"""    <h1>{esc(q)}</h1>
    <p class="edition">verdict filed <span>{esc(e['dateTested'])}</span> · rcpbx radar</p>
    <p style="margin:1.5rem 0"><span class="stamp {sc}" style="font-size:1.1rem;padding:.5rem 1rem">{esc(status)}</span></p>
    <p class="sub" style="font-size:1rem;max-width:56ch">{esc(ans)}. {esc(line)}</p>
    {recipe_link}
    <div class="how" style="margin-top:2.5rem">
      This verdict came out of a real kitchen, not a keyboard — cooked, measured, and filed on {esc(e['dateTested'])}.
      How we test: <a href="/why/">/why</a>. The full scoreboard: <a href="/trends/">the Radar</a>.
      Everything that failed: <a href="/skips/">the SKIP file</a>.
    </div>
    <script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>"""
    return shell(f"{q} — verdict: {status} | rcpbx", f"{ans}. {line} Tested {e['dateTested']}.",
                 f"{SITE}/radar/{e['slug']}/", body, ogimage=og)

def skips_page(r):
    tested = [e for e in r["entries"] if e.get("dateTested")]
    skips = [e for e in tested if e["status"] == "SKIP"]
    if skips:
        rows = "\n".join(
            f'      <div class="row"><span><span class="t-name">{esc(e["name"])}</span>'
            f'<span class="t-note">cause of death: {esc(e.get("line",""))}</span></span>'
            f'<span class="heat h1">{esc(e["dateTested"])}</span>'
            f'<span><span class="stamp s-skip">SKIP ☠</span></span></div>' for e in skips)
        board = f'<div class="radar"><div class="radar-head"><span>trend</span><span>filed</span><span>verdict</span></div>\n{rows}\n</div>'
        counter = f"{len(skips)} recipes killed in testing — groceries you didn't waste."
    else:
        board = ""
        counter = ""
    empty = "" if skips else """    <div class="how" style="border-color:var(--red)">
      <b style="color:var(--red)">0 kills so far.</b> Statistically suspicious — we know. The graveyard opened
      {date} and nothing has died in testing yet, which either means we're picking winners or we're not being
      hard enough. The scoreboard is public; judge for yourself. The first SKIP gets buried here with full honors:
      name, date, and a one-line cause of death.
    </div>""".replace("{date}", r["date"])
    body = f"""    <h1>The SKIP File</h1>
    <p class="sub">Every viral recipe that died in testing. Tested so you don't have to. Nothing here is ever deleted.</p>
    <p class="edition">{counter or 'the graveyard · permanent record'}</p>
{board}
{empty}
    <div class="how">
      Why publish failures? Because every other food site is structurally incapable of it — a failed recipe is a
      page they can't monetize. We don't monetize anything, so the whistle gets blown. When a trend dies in our
      kitchen it gets one line here, a date, and a link to what you should make instead.
      The live scoreboard: <a href="/trends/">the Radar</a>.
    </div>"""
    return shell("The SKIP File — viral recipes that failed testing | rcpbx",
                 "Every viral recipe that died in testing, with cause of death. Tested so you don't have to.",
                 f"{SITE}/skips/", body)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    r = json.load(open("data/radar.json"))
    ed = r["edition"].lower()
    Path("trends").mkdir(exist_ok=True)
    live = shell("The Radar — viral recipes, tested weekly | rcpbx",
                 "Every viral recipe on the internet, cooked in a real kitchen and given a verdict — WORTH IT, OVERHYPED, or SKIP. Updated weekly.",
                 f"{SITE}/trends/", board_html(r, frozen=False))
    Path("trends/index.html").write_text(live)
    Path(f"trends/{ed}").mkdir(exist_ok=True)
    froz = shell(f"The Radar — edition {r['edition']} | rcpbx",
                 f"Radar edition {r['edition']}: the week's tested verdicts, frozen for the record.",
                 f"{SITE}/trends/{ed}/", board_html(r, frozen=True))
    Path(f"trends/{ed}/index.html").write_text(froz)
    n = 0
    for e in r["entries"]:
        if e.get("dateTested"):
            Path(f"radar/{e['slug']}").mkdir(parents=True, exist_ok=True)
            Path(f"radar/{e['slug']}/index.html").write_text(verdict_page(e, r))
            n += 1
    Path("skips").mkdir(exist_ok=True)
    Path("skips/index.html").write_text(skips_page(r))
    print(f"radar: live board + /trends/{ed}/ + {n} verdict permalinks + /skips/")

if __name__ == "__main__":
    main()
