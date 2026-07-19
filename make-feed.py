#!/usr/bin/env python3
"""rcpbx make-feed.py — regenerates feed.xml from recipes carrying a `tested` date.
Run after build.py:  python3 make-feed.py"""
import json, glob, os, html
from email.utils import format_datetime
from datetime import datetime, timezone

SITE = "https://rcpbx.com"
os.chdir(os.path.dirname(os.path.abspath(__file__)))
items = []
for f in glob.glob("data/*.json"):
    if os.path.basename(f) in ("index.json","hot.json","radar.json"): continue
    r = json.load(open(f))
    if r.get("tested"): items.append(r)
items.sort(key=lambda r: (r.get("tested",""), r["id"]), reverse=True)

def esc(s): return html.escape(str(s))
now = format_datetime(datetime.now(timezone.utc))
out = ['<?xml version="1.0" encoding="UTF-8"?>',
 '<rss version="2.0" xmlns:atom="http://www.w3.org/1998/Atom">', '  <channel>',
 '    <title>rcpbx - New &amp; Tested Recipes</title>',
 '    <link>%s</link>' % SITE,
 '    <description>Recipes that work. No life stories. No ads. Viral recipes tested weekly with verdicts.</description>',
 '    <language>en-us</language>',
 '    <atom:link href="%s/feed.xml" rel="self" type="application/rss+xml"/>' % SITE,
 '    <lastBuildDate>%s</lastBuildDate>' % now]
for r in items[:30]:
    y, m = (r["tested"].split("-") + ["01"])[:2]
    pub = format_datetime(datetime(int(y), int(m), 18, tzinfo=timezone.utc))
    v = r.get("verdict")
    desc = (("[%s] " % v["status"]) if v else "") + r.get("tagline","")
    out += ['    <item>',
     '      <title>%s</title>' % esc(r["title"]),
     '      <link>%s/recipes/%s/</link>' % (SITE, r["id"]),
     '      <guid>%s/recipes/%s/</guid>' % (SITE, r["id"]),
     '      <description>%s</description>' % esc(desc),
     '      <pubDate>%s</pubDate>' % pub, '    </item>']
out += ['  </channel>', '</rss>']
open("feed.xml","w").write("\n".join(out))
print("feed.xml: %d items" % min(len(items),30))
