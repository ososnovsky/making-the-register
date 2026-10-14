"""Verify candidate entries: python verify.py cand.yaml [out.txt]
For every link: HTTP status, final URL, <title>, hijack words, date-ish tokens. For venue
entries: whether the street name of the written address appears on any fetched page of the entry.
Domains are spaced >=2 s apart; different domains run in parallel."""
import re, sys, ssl, time, threading, urllib.request, urllib.parse, unicodedata
from concurrent.futures import ThreadPoolExecutor
import yaml

UA = "Mozilla/5.0 (EventScanner register curation; contact dsosnovsky@gmail.com)"
CTX = ssl.create_default_context()
last = {}
lock = threading.Lock()
BAD = re.compile(r"casino|gambl|kasino|sázk|bet365|domain.{0,20}(for sale|na predaj)|parked|slot", re.I)

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def fetch(url):
    host = urllib.parse.urlparse(url).netloc
    with lock:
        wait = last.get(host, 0) + 2 - time.time()
        last[host] = max(time.time(), last.get(host, 0) + 2)
    if wait > 0: time.sleep(wait)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "sk,en;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
            body = r.read(600000).decode(r.headers.get_content_charset() or "utf-8", "replace")
            return r.status, r.geturl(), body
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:
        err = f"ERR {type(e).__name__} {str(e)[:60]}"
        try:
            import subprocess
            r = subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, "-H", "Accept-Language: sk,en;q=0.8", "-w",
                                "\n@@%{http_code} %{url_effective}", url],
                               capture_output=True, timeout=40)
            out = r.stdout.decode("utf-8", "replace")
            body, _, tail = out.rpartition("\n@@")
            code, _, eff = tail.partition(" ")
            if code.isdigit() and int(code) > 0:
                return int(code), eff.strip() or url, body[:600000]
        except Exception:
            pass
        return 0, url, err

def check(e):
    out = [f"## {e['id']} — {e['name']}"]
    bodies = []
    for l in e["links"]:
        u = l["url"]
        if l["channel"] in ("instagram", "facebook"):
            out.append(f"   skip {l['channel']} {u}"); continue
        if l["channel"] == "newsletter" and not u.startswith("http"): continue
        st, fu, body = fetch(u)
        t = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
        t = re.sub(r"\s+", " ", t.group(1)).strip()[:70] if t else ""
        flag = " HIJACK?" if BAD.search(t) else ""
        yrs = len(re.findall(r"2026|2027", body))
        mv = " MOVED" if urllib.parse.urlparse(fu).netloc.replace("www.", "") != urllib.parse.urlparse(u).netloc.replace("www.", "") else ""
        out.append(f"   {st} {l['channel']:15} {u}{mv and ' -> ' + fu}  [{t}] len={len(body)} y26/27={yrs}{flag}")
        if body.startswith("ERR"): out[-1] += " " + body
        bodies.append(norm(body))
    v = e.get("venue")
    if v:
        street = re.split(r"\s\d", v["address"])[0].split(",")[0]
        street = re.sub(r"^(ul\.|ulica)\s*", "", street.strip(), flags=re.I)
        ok = any(norm(street) in b for b in bodies)
        out.append(f"   address '{v['address']}': street '{street}' {'FOUND' if ok else 'NOT FOUND on fetched pages'}")
    return "\n".join(out)

def main(src, dst=None):
    entries = yaml.safe_load(open(src, encoding="utf-8")) or []
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(check, entries))
    text = "\n".join(res)
    if dst: open(dst, "w", encoding="utf-8").write(text)
    print(text)

if __name__ == "__main__":
    main(*sys.argv[1:3])
