import sys,re,html,json
sys.path.insert(0,'.')
from verify import fetch
slugs=[s for s in json.load(open('vb_services.json')) if s!='feed']
out={}; orgs={}
for s in slugs:
    st,fu,b=fetch(f"https://www.visitbratislava.com/sk/sluzby/{s}/")
    if st!=200: out[s]={"st":st}; continue
    t=re.search(r"<title>(.*?) \|",b); name=html.unescape(t.group(1)).strip() if t else s
    i=b.find('Realizované s finančnou'); 
    j=b.rfind('<h1',0,i if i>0 else len(b))
    seg=b[j:i if i>0 else j+8000]
    txt=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",seg))).strip()
    org=re.search(r'href="https://www.visitbratislava.com/sk/clenovia/([^"/]+)/"',seg)
    out[s]=dict(name=name,text=txt[:1500],org=org.group(1) if org else "")
    if org and org.group(1) not in orgs:
        st2,fu2,b2=fetch(f"https://www.visitbratislava.com/sk/clenovia/{org.group(1)}/")
        w=re.search(r'class="website".*?<a href="([^"]+)"',b2,re.S) if st2==200 else None
        a=re.search(r'class="address".*?class="value"[^>]*>(.*?)</span>\s*</li>',b2,re.S) if st2==200 else None
        nm=re.search(r"<title>(.*?) \|",b2) if st2==200 else None
        orgs[org.group(1)]=dict(name=html.unescape(nm.group(1)).strip() if nm else org.group(1),web=w.group(1) if w else "",addr=html.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",a.group(1)))).strip() if a else "")
    print(s,flush=True)
json.dump({"services":out,"orgs":orgs},open('vb_services_data2.json','w',encoding='utf-8'),ensure_ascii=False)
print("done")
