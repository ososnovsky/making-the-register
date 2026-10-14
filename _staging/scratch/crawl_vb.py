import sys,re,json,html,time
sys.path.insert(0,'.')
from verify import fetch
base="https://www.visitbratislava.com/sk/miesta/page/%d/"
slugs=[]
for n in range(1,40):
    st,fu,b=fetch(base%n if n>1 else "https://www.visitbratislava.com/sk/miesta/")
    if st!=200: print("stop",n,st); break
    new=[s for s in re.findall(r'href="https://www.visitbratislava.com/sk/miesta/([^"/#?]+)/"',b) if s not in slugs and s!="page"]
    if not new and n>1: print("no new",n); break
    slugs+=new
print(len(slugs),flush=True)
import os
out=json.load(open('vb_places.json',encoding='utf-8')) if os.path.exists('vb_places.json') else {}
for s in slugs:
    if s in out and out[s].get('name'): continue
    st,fu,b=fetch(f"https://www.visitbratislava.com/sk/miesta/{s}/")
    if st!=200: out[s]={"status":st}; continue
    t=re.search(r"<title>(.*?) \|",b); name=html.unescape(t.group(1)).strip() if t else s
    w=re.search(r'class="website".*?<a href="([^"]+)"',b,re.S)
    a=re.search(r'class="address".*?class="value"[^>]*>(.*?)</span>\s*</li>',b,re.S)
    a=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",a.group(1)))).strip() if a else ""
    cats=sorted(set(re.findall(r'/sk/place-categories/([^/"]+)/',b)))
    co=re.search(r"destination=([\d.]+),([\d.]+)",b)
    out[s]=dict(name=name,web=w.group(1) if w else "",addr=a,cats=cats,lat=co.group(1) if co else "",lon=co.group(2) if co else "")
    json.dump(out,open("vb_places.json","w",encoding="utf-8"),ensure_ascii=False)
print("done",len(out))
