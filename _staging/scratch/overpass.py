"""Fetch OSM objects in the Bratislava municipality. Usage: python overpass.py out.json 'nwr["amenity"="theatre"]'  (several selectors allowed)"""
import sys, json, urllib.request, urllib.parse
sels = sys.argv[2:]
body = "".join(f"{s}(area.a);" for s in sels)
q = f'[out:json][timeout:120];area(3601702499)->.a;({body});out center tags;'
req = urllib.request.Request("https://overpass-api.de/api/interpreter", data=urllib.parse.urlencode({"data": q}).encode(),
                             headers={"User-Agent": "EventScanner-register-curation/1.0 (contact dsosnovsky@gmail.com)"})
import time
for i in range(5):
    try:
        d = json.load(urllib.request.urlopen(req, timeout=180)); break
    except Exception as ex:
        print('retry', ex); time.sleep(20)
out = []
for e in d["elements"]:
    t = e.get("tags", {})
    lat = e.get("lat") or e.get("center", {}).get("lat"); lon = e.get("lon") or e.get("center", {}).get("lon")
    web = t.get("website") or t.get("contact:website") or t.get("url") or ""
    out.append(dict(name=t.get("name", ""), web=web, street=t.get("addr:street", ""), hn=t.get("addr:housenumber", ""),
                    cp=t.get("addr:conscriptionnumber", ""), pc=t.get("addr:postcode", ""), city=t.get("addr:city", ""),
                    lat=lat, lon=lon, kind=next((f"{k}={t[k]}" for k in ("amenity", "tourism", "leisure", "shop", "office", "club") if k in t), ""),
                    id=f"{e['type'][0]}{e['id']}", phone=t.get("phone", ""), ig=t.get("contact:instagram", ""), fb=t.get("contact:facebook", "")))
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "objects;", sum(1 for o in out if o["web"]), "with website")
