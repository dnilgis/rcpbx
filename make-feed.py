#!/usr/bin/env python3
"""rcpbx make-feed.py — regenerates feed.xml: the 30 newest recipes.

Dates are real: the git date a recipe's data file first appeared (or its
`tested` month when git has no record). Nothing is stamped "now" unless
something actually changed. Run after build.py:  python3 make-feed.py"""
import json, glob, os, html, re, subprocess
from email.utils import format_datetime
from datetime import datetime, timezone

SITE = "https://rcpbx.com"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

first = {}
try:
    log = subprocess.run(["git", "log", "--format=@%cI", "--name-only", "--diff-filter=A", "--", "data"],
                         capture_output=True, text=True, timeout=60).stdout
    when = None
    for line in log.splitlines():
        if line.startswith("@"): when = line[1:]; continue
        m = re.match(r"data/([a-z0-9-]+)\.json$", line.strip())
        if m and when: first[m.group(1)] = when   # oldest add wins (log is newest-first)
except Exception:
    pass

items = []
for f in glob.glob("data/*.json"):
    if os.path.basename(f) in ("index.json", "hot.json", "radar.json"): continue
    r = json.load(open(f))
    if r["id"] in first:
        dt = datetime.fromisoformat(first[r["id"]])
    elif r.get("tested"):
        y, m = (r["tested"].split("-") + ["01"])[:2]
        dt = datetime(int(y), int(m), 1, tzinfo=timezone.utc)
    else:
        dt = datetime.now(timezone.utc)   # new file not yet committed: it is new today
    items.append((dt, r))
items.sort(key=lambda x: (x[0], x[1]["id"]), reverse=True)
items = items[:30]

def esc(s): return html.escape(str(s))
newest = format_datetime(items[0][0]) if items else format_datetime(datetime.now(timezone.utc))
out = ['<?xml version="1.0" encoding="UTF-8"?>',
 '<rss version="2.0" xmlns:atom="http://www.w3.org/1998/Atom">', '  <channel>',
 '    <title>rcpbx - New Recipes &amp; Verdicts</title>',
 '    <link>%s</link>' % SITE,
 '    <description>Recipes that work. No life stories. No ads. Viral recipes cooked and given a verdict.</description>',
 '    <language>en-us</language>',
 '    <atom:link href="%s/feed.xml" rel="self" type="application/rss+xml"/>' % SITE,
 '    <lastBuildDate>%s</lastBuildDate>' % newest]
for dt, r in items:
    v = r.get("verdict")
    desc = (("[%s] " % v["status"]) if v else "") + r.get("tagline", "")
    out += ['    <item>',
     '      <title>%s</title>' % esc(r["title"]),
     '      <link>%s/recipes/%s/</link>' % (SITE, r["id"]),
     '      <guid>%s/recipes/%s/</guid>' % (SITE, r["id"]),
     '      <description>%s</description>' % esc(desc),
     '      <pubDate>%s</pubDate>' % format_datetime(dt), '    </item>']
out += ['  </channel>', '</rss>']
open("feed.xml", "w").write("\n".join(out) + "\n")
print("feed.xml: %d items (real first-published dates)" % len(items))
