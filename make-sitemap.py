#!/usr/bin/env python3
"""
rcpbx make-sitemap.py — run LAST, after every other generator.

Lists every indexable page (no noindex, canonical points at itself) and stamps
<lastmod> with the date the page's content last actually changed. Change is
detected by hashing the built HTML and comparing with sitemap-ledger.json, so a
rebuild that changes nothing keeps the old date. First sight of a page uses the
git commit date of its file, or today if git has none.
"""
import os, re, json, glob, hashlib, datetime, subprocess

SITE = "https://rcpbx.com"
LEDGER = "sitemap-ledger.json"


def git_day(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                             capture_output=True, text=True, timeout=30).stdout.strip()
        return out or None
    except Exception:
        return None


def committed_day(path, sha):
    """Git date of the file if the built copy is unchanged from the committed one."""
    try:
        old = subprocess.run(["git", "show", "HEAD:" + path], capture_output=True,
                             text=True, timeout=30)
        if old.returncode != 0:
            return None
        osha = hashlib.sha1(re.sub(r"\s+", " ", old.stdout).encode("utf-8")).hexdigest()[:16]
        return git_day(path) if osha == sha else None
    except Exception:
        return None


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    today = datetime.date.today().isoformat()
    ledger = json.load(open(LEDGER)) if os.path.exists(LEDGER) else {}
    urls = []
    for f in sorted(glob.glob("**/index.html", recursive=True)):
        if f.startswith((".git/", "node_modules/")):
            continue
        h = open(f, encoding="utf-8").read()
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', h, re.I):
            continue
        path = "/" + f[:-len("index.html")]
        url = SITE + path
        m = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        if not m or m.group(1).rstrip("/") + "/" != url:
            continue  # page defers to another URL; only the canonical one is listed
        body = re.sub(r"\s+", " ", h)
        sha = hashlib.sha1(body.encode("utf-8")).hexdigest()[:16]
        prev = ledger.get(url)
        if prev and prev[0] == sha:
            day = prev[1]
        elif prev:
            day = today
        else:
            day = committed_day(f, sha) or today
        ledger[url] = [sha, day]
        urls.append((url, day))

    def order(u):
        p = u[0][len(SITE):]
        return (p != "/", p.startswith("/recipes/"), p)
    urls.sort(key=order)
    live = {u for u, _ in urls}
    ledger = {k: v for k, v in ledger.items() if k in live}
    json.dump(ledger, open(LEDGER, "w"), indent=0, sort_keys=True)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, d in urls:
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (u, d))
    lines.append("</urlset>")
    open("sitemap.xml", "w").write("\n".join(lines) + "\n")
    print("sitemap: %d indexable urls (lastmod = last real content change)" % len(urls))


if __name__ == "__main__":
    main()
