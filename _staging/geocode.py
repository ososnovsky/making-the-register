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

UA = "EventScanner-register-curation/1.0 (personal project; contact <your-email>)"


def lookup(address):
    q = urllib.parse.urlencode({"q": address, "format": "jsonv2", "addressdetails": 1, "limit": 3,
                                "countrycodes": "nl"})
    req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def house_number(address):
    m = re.search(r"\b(\d+)\s*[a-zA-Z]?\b", address.split(",")[0])
    return m.group(1) if m else None


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
        hn = house_number(addr)
        time.sleep(1.1)
        try:
            res = lookup(addr)
        except Exception as ex:
            res, err = [], ex
        hit = next((r for r in res if hn and (re.match(r"\d+", str(r.get("address", {})
                    .get("house_number", "")).strip()) or [None])[0] == hn), None)
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
