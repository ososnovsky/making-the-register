import sys,re,html,json,os
sys.path.insert(0,'.')
from verify import fetch
cache=json.load(open('vb_places.json',encoding='utf-8')) if os.path.exists('vb_places.json') else {}
for s in sys.argv[1:]:
    v=cache.get(s)
    if not v or not v.get('name'):
        st,fu,b=fetch(f"https://www.visitbratislava.com/sk/miesta/{s}/")
        if st!=200: print(s,st); continue
        w=re.search(r'class="website".*?<a href="([^"]+)"',b,re.S)
        a=re.search(r'class="address".*?class="value"[^>]*>(.*?)</span>\s*</li>',b,re.S)
        a=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",a.group(1)))).strip() if a else ""
        v=dict(web=w.group(1) if w else "",addr=a)
    print(s,"|",v.get('web'),"|",v.get('addr'))
