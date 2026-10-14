"""Fill `coords: TODO` in an agent entries file via Nominatim (1 req/s, identifying UA).

Usage: python geocode.py in.yaml out.yaml
Only accepts a result whose address carries the queried house number; otherwise leaves the
entry without coords and prints it as an open item. Never estimates.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

import yaml

UA = "EventScanner-register-curation/1.0 (personal project; contact dsosnovsky@gmail.com)"


import os
CACHE_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geocache.json")
CACHE = json.load(open(CACHE_F, encoding="utf-8")) if os.path.exists(CACHE_F) else {}


def cached(key, fn, *a):
    if key not in CACHE:
        time.sleep(1.1)
        CACHE[key] = fn(*a)
        json.dump(CACHE, open(CACHE_F, "w", encoding="utf-8"), ensure_ascii=False)
    return CACHE[key]


def lookup(address):
    q = urllib.parse.urlencode({"q": address, "format": "jsonv2", "addressdetails": 1, "limit": 3,
                                "countrycodes": "sk"})
    req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def yq(s):
    return "'" + s.replace("'", "''") + "'" if re.search(r"[:#]|^\W", s) else s


def osm_lookup(q):
    p = urllib.parse.urlencode({"q": q, "format": "jsonv2", "addressdetails": 1, "limit": 5, "countrycodes": "sk",
                                "viewbox": "16.90,48.30,17.40,48.00", "bounded": 1})
    req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?{p}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)
    for r0 in res:
        a = r0.get("address", {})
        road = a.get("road") or a.get("pedestrian") or a.get("square")
        if not road or r0.get("category") in ("highway", "boundary", "place") or re.match(r"^[DER]\d", road):
            continue
        toks = [t.lower() for t in q.split() if len(t) >= 4 and t.lower() != "bratislava"]
        if toks and not any(t in r0.get("display_name", "").lower() for t in toks):
            continue
        hn = a.get("house_number", "")
        line = f"{road} {hn}".strip() + f", {a.get('postcode', '').strip()} Bratislava".replace(" ,", ",")
        line = line.replace(",  Bratislava", ", Bratislava")
        return r0, line
    return None


def house_number(address):
    part = address.split(",")[0].strip()
    ms = re.findall(r"(?<![\d.])(\d+)(?:/\d+)?\s*[a-zA-Z]?$", part)
    return ms[-1] if ms else None


def main(src, dst):
    """Rewrite the text of src into dst, replacing each entry's `coords: TODO` line in place
    (keeps comments and folded notes). Unmatched venues lose the coords line and get flagged."""
    text = open(src, encoding="utf-8").read()
    entries = yaml.safe_load(text)
    blocks = re.split(r"(?m)^(?=- id: )", text)
    out = []
    for block in blocks:
        m = re.match(r"- id: (\S+)", block)
        e = next((x for x in entries if m and x["id"] == m.group(1)), None)
        v = (e or {}).get("venue")
        if not v or v.get("coords") != "TODO":
            out.append(block)
            continue
        addr = v["address"]
        if addr.startswith("OSM:"):
            q = addr[4:].strip()
            custom = None
            if ">>" in q:
                q, custom = [x.strip() for x in q.split(">>", 1)]
            pass
            try:
                res = cached('osm|' + q, osm_lookup, q)
            except Exception as ex:
                res = []
            if res:
                r0, line = res
                if custom: line = custom
                block = re.sub(r"address: .*\n", lambda m: "address: " + yq(line) + "\n", block, count=1)
                c = f"[{round(float(r0['lat']), 6)}, {round(float(r0['lon']), 6)}]"
                block = re.sub(r"coords: TODO", f"coords: {c}", block, count=1)
                print(f"OSM  {e['id']}: {line} {c}")
            else:
                block = re.sub(r"coords: TODO", "coords: MISSING", block, count=1)
                print(f"OPEN {e['id']}: no OSM match for {q}")
            out.append(block)
            continue
        hn = house_number(addr)
        pass
        try:
            res = cached('addr|' + addr, lookup, addr)
        except Exception as ex:
            res, err = [], ex
        def nums(r):
            return set(re.findall(r"\d+", str(r.get("address", {}).get("house_number", ""))))
        hit = next((r for r in res if hn and hn in nums(r)), None)
        if not hit:
            # fall back to the venue's own named OSM object, accepted only on the same street
            import unicodedata
            def norm(s):
                return "".join(ch for ch in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(ch) != "Mn")
            street = norm(re.split(r"\s\d", addr.split(",")[0])[0]).strip()
            try:
                r2 = cached('osm|' + e["name"] + ' Bratislava', osm_lookup, e["name"] + ' Bratislava')
            except Exception:
                r2 = None
            if r2 and street and street in norm(r2[1]):
                hit = r2[0]
        if hit:
            c = f"[{round(float(hit['lat']), 6)}, {round(float(hit['lon']), 6)}]"
            block = re.sub(r"coords: TODO", f"coords: {c}", block, count=1)
            print(f"OK   {e['id']}: {c} <- {hit.get('display_name', '')[:90]}")
        else:
            block = re.sub(r"coords: TODO", "coords: MISSING", block, count=1)
            print(f"OPEN {e['id']}: no house-number match for {addr} "
                  f"(top: {res[0]['display_name'][:80] if res else 'none'})")
        out.append(block)
    open(dst, "w", encoding="utf-8").write("".join(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
