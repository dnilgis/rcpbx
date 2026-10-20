"""Shared time parsing for rcpbx generators.

Recipe JSON carries times as free text: "20 min", "2½ hrs", "1 hr + overnight",
"25 min (plus 1.5 hr rising)", "4-6 hrs". Every generator must read them the
same way, so they all import this module.

parse(text) -> (main, extra, open_ended)
  main        minutes of the stated time, before any "(plus ...)" or "+ ..." part.
              A range ("4-6 hrs") counts as its low end.
  extra       minutes of quantified passive time ("plus 1.5 hr rising").
  open_ended  True when passive time is mentioned without a number
              ("+ overnight", "+ chilling"). Callers must not print a total then.
Any value is None when nothing parses.
"""
import re

_FRAC = {"½": ".5", "¼": ".25", "¾": ".75", "⅓": ".33", "⅔": ".67"}
_TOK = re.compile(r"(\d+(?:\.\d+)?)(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*(hours?|hrs?|h\b|minutes?|mins?|m\b)", re.I)


def _norm(s):
    s = str(s or "")
    for k, v in _FRAC.items():
        s = re.sub(r"(\d)" + k, lambda m: m.group(1) + v, s)
        s = s.replace(k, "0" + v)
    return s


def _sum(s):
    total, hit = 0.0, False
    for m in _TOK.finditer(s):
        n = float(m.group(1)); u = m.group(2).lower()
        total += n * 60 if u.startswith("h") else n
        hit = True
    return (int(round(total)) if hit else None)


def parse(text):
    s = _norm(text)
    if not s.strip():
        return None, None, False
    cut = re.search(r"\(|\+|\bplus\b", s)
    head = s[:cut.start()] if cut else s
    tail = s[cut.start():] if cut else ""
    main = _sum(head)
    extra = _sum(tail) if tail else None
    open_ended = bool(tail) and extra is None
    if re.search(r"overnight|chill|marinat|rest|soak|rising|rise", tail, re.I) and extra is None:
        open_ended = True
    return main, extra, open_ended


def active_minutes(entry):
    """Hands-on + oven time (prep main + cook main, or 'time' main). None if unknown."""
    p, _, _ = parse(entry.get("prep"))
    c, _, _ = parse(entry.get("cook"))
    if p is not None or c is not None:
        return (p or 0) + (c or 0) or None
    t, _, _ = parse(entry.get("time"))
    return t


def total_minutes(entry):
    """Start-to-plate minutes including quantified passive time, or None if open-ended/unknown."""
    tot, known, open_ = 0, False, False
    fields = ("prep", "cook") if (entry.get("prep") or entry.get("cook")) else ("time",)
    for f in fields:
        m, x, o = parse(entry.get(f))
        if m is not None: tot += m; known = True
        if x is not None: tot += x
        open_ = open_ or o
    if not known or open_:
        return None
    return tot


def iso(minutes):
    if not minutes:
        return None
    h, m = divmod(int(minutes), 60)
    return "PT" + ("%dH" % h if h else "") + ("%dM" % m if m else "")


def human(minutes):
    if not minutes:
        return ""
    h, m = divmod(int(minutes), 60)
    if h and m: return "%d hr %d min" % (h, m)
    if h: return "%d hr" % h
    return "%d min" % m
