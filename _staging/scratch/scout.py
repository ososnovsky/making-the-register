"""Scout websites: python scout.py urls.txt  (lines: url or 'name | url').
Prints status, title, agenda-like links, newsletter-like links, 2026/27 count, address-ish line."""
import sys, re, html, urllib.parse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, ".")
from verify import fetch
AG = re.compile(r"program|podujat|akci[ei]|event|kalend|agenda|koncert|what.?s.?on|vystav|repertoar|repertoár|inscenac|aktualit|festival|workshop|kurz", re.I)
NL = re.compile(r"newsletter|odber|mailchimp|subscribe|prihlas.{0,12}(odber|newsletter)|nwsl|ecomail|mailerlite|smartemailing|sendinblue|brevo|eepurl", re.I)
ADDR = re.compile(r"[A-ZÁČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ][\wáäčďéíĺľňóôŕšťúýž\.\- ]{2,40}\s\d{1,4}(?:/\d+[A-Za-z]?)?[A-Za-z]?,?\s*(?:\d{3}\s?\d{2}\s)?Bratislava")
def one(line):
    name, _, url = line.rpartition(" | ")
    if not url.startswith("http"): url = "https://" + url.strip()
    st, fu, b = fetch(url)
    if st == 0 and '://www.' not in url:
        u2 = url.replace('://', '://www.', 1); st, fu, b = fetch(u2)
        if st: url = u2
    t = re.search(r"<title[^>]*>(.*?)</title>", b, re.S | re.I)
    t = html.unescape(re.sub(r"\s+", " ", t.group(1))).strip()[:60] if t else ""
    links = re.findall(r'<a [^>]*href="([^"#][^"]*)"[^>]*>(.*?)</a>', b, re.S | re.I)
    ag, nl = [], []
    base = fu
    for h, tx in links:
        tx = re.sub(r"<[^>]+>", "", tx); tx = html.unescape(re.sub(r"\s+", " ", tx)).strip()[:25]
        full = urllib.parse.urljoin(base, html.unescape(h))
        if NL.search(h) or NL.search(tx):
            if full not in nl: nl.append(full)
        elif AG.search(h) or AG.search(tx):
            if full not in ag and "facebook" not in full and "instagram" not in full: ag.append(full)
    a = ADDR.search(re.sub(r"<[^>]+>", " ", b))
    a = re.sub(r"\s+", " ", a.group(0)) if a else ""
    ig = "IG" if "instagram.com/" in b else ""; fb = "FB" if "facebook.com/" in b else ""
    y = len(re.findall(r"2026|2027", b))
    return f"{name or url} | {st} | {fu if fu.rstrip('/')!=url.rstrip('/') else ''} | [{t}] | y={y} {ig}{fb} | addr: {a} | AG: {' '.join(ag[:3])} | NL: {' '.join(nl[:2])}"
lines = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
with ThreadPoolExecutor(20) as ex:
    for r in ex.map(one, lines): print(r, flush=True)
