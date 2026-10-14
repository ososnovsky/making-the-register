import sys,re,html,json
sys.path.insert(0,'.')
from verify import fetch
slugs=[s for s in json.load(open('vb_services.json')) if s!='feed']
out={}
for s in slugs:
    st,fu,b=fetch(f"https://www.visitbratislava.com/sk/sluzby/{s}/")
    if st!=200: out[s]={"st":st}; continue
    t=re.search(r"<title>(.*?) \|",b); name=html.unescape(t.group(1)).strip() if t else s
    body=re.sub(r"(?s)<(script|style|nav|footer|header).*?</\1>","",b)
    txt=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",body))).strip()
    i=txt.find(name); txt=txt[i:] if i>=0 else txt
    web=re.findall(r'class="(?:website|web)".*?<a href="([^"]+)"',b,re.S)
    ext=[h for h in re.findall(r'href="(https?://[^"]+)"',b) if not re.search(r'visitbratislava|google|facebook|instagram|youtube|twitter|mincrs|w3\.org|schema|gstatic|cloudflare|wp\.org',h)]
    price=re.findall(r"[^.]{0,60}(?:€|EUR)[^.]{0,60}",txt)[:3]
    out[s]=dict(name=name,web=web[:1] or ext[:2],text=txt[:420],price=price)
    print(s,"|",name,"|",(web[:1] or ext[:1]),"|"," ## ".join(p.strip() for p in price[:2])[:200],flush=True)
json.dump(out,open('vb_services_data.json','w',encoding='utf-8'),ensure_ascii=False)
