"""python addr.py list.txt   lines 'id | url' -> candidate addresses from the site (homepage + contact-ish pages)"""
import sys,re,html,urllib.parse
sys.path.insert(0,'.')
from verify import fetch
from concurrent.futures import ThreadPoolExecutor
ADDR=re.compile(r"((?:ul\.|Ul\.|ulica|nám\.|Nám\.|námestie|Námestie)?\s?[A-ZÁČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ][\wáäčďéíĺľňóôŕšťúýžÁČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ\.\-' ]{2,38}?\s\d{1,4}(?:/\d{1,4}[A-Za-z]?)?[A-Za-z]?)\s*,?\s*(?:\(?[\wáäčďéíĺľňóôŕšťúýž ]{0,25}\)?\s*,?\s*)?(\d{3}\s?\d{2})?\s*,?\s*(?:Bratislava|BRATISLAVA)(?:\s*-\s*[A-ZÁČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ][\wáäčďéíĺľňóôŕšťúýž\- ]{2,20})?")
PATHS=["","/kontakt","/kontakty","/contact","/o-nas","/kontakt/","/en/contact","/sk/kontakt","/informacie","/navsteva"]
def one(line):
    eid,_,url=[x.strip() for x in line.rpartition(" | ")] if " | " in line else (line,"",line)
    if not url.startswith("http"): url="https://"+url
    found={}
    for p in PATHS[:5]:
        st,fu,b=fetch(url.rstrip("/")+p)
        if st!=200: continue
        t=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"(?s)<(script|style).*?</\1>","",b))))
        for m in ADDR.finditer(t):
            a=re.sub(r"\s+"," ",m.group(0))
            found[a]=found.get(a,0)+1
        if len(found)>=3: break
    top=sorted(found.items(),key=lambda x:-x[1])[:3]
    return f"{eid} | "+" ## ".join(f"{a} ({n})" for a,n in top)
lines=[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip() and not l.startswith("#")]
with ThreadPoolExecutor(16) as ex:
    for r in ex.map(one,lines): print(r,flush=True)
