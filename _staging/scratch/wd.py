import sys,json,urllib.request,urllib.parse
cls=sys.argv[2:]
vals=" ".join("wd:"+c for c in cls)
q=f"""SELECT DISTINCT ?item ?itemLabel ?web ?addr ?coord ?cls WHERE {{
 VALUES ?cls {{ {vals} }}
 ?item wdt:P31/wdt:P279* ?cls .
 ?item wdt:P131* wd:Q1780 .
 ?item wdt:P856 ?web .
 OPTIONAL {{ ?item wdt:P6375 ?addr }}
 OPTIONAL {{ ?item wdt:P625 ?coord }}
 FILTER NOT EXISTS {{ ?item wdt:P576 [] }}
 SERVICE wikibase:label {{ bd:serviceParam wikibase:language "sk,en". }}
}}"""
u="https://query.wikidata.org/sparql?format=json&query="+urllib.parse.quote(q)
r=urllib.request.Request(u,headers={"User-Agent":"EventScanner-register-curation/1.0 (contact dsosnovsky@gmail.com)"})
d=json.load(urllib.request.urlopen(r,timeout=120))["results"]["bindings"]
seen={}
for x in d:
    k=x["itemLabel"]["value"]
    seen[k]=(x["web"]["value"],x.get("addr",{}).get("value",""),x.get("coord",{}).get("value",""))
json.dump(seen,open(sys.argv[1],"w",encoding="utf-8"),ensure_ascii=False,indent=0)
for k,v in seen.items(): print(k,"|",v[0],"|",v[1])
print(len(seen))
