import sys,re,html,urllib.parse,yaml
sys.path.insert(0,'.')
from verify import fetch
from concurrent.futures import ThreadPoolExecutor
NL=re.compile(r"newsletter|odber(?!ate)|odoberat|mailchimp|subscribe|ecomail|mailerlite|smartemailing|sendinblue|brevo|eepurl|list-manage|mailpoet|feedburner|noviniek|zasielani",re.I)
E=yaml.safe_load(open('../sources.yaml',encoding='utf-8'))
def one(e):
    if any(l['channel']=='newsletter' for l in e['links']): return None
    seen=set(); out=[]
    urls=[]
    for l in e['links']:
        if l['channel'] in('instagram','facebook'): continue
        p=urllib.parse.urlparse(l['url'])
        if 'goout' in p.netloc or 'meetup.com' in p.netloc or 'eventbrite' in p.netloc or 'ra.co' in p.netloc: continue
        r=f"{p.scheme}://{p.netloc}/"
        for u in (l['url'],r):
            if u not in urls: urls.append(u)
    for u in urls[:2]:
        st,fu,b=fetch(u)
        if st!=200: continue
        for h,t in re.findall(r'<a [^>]*href="([^"#][^"]*)"[^>]*>(.*?)</a>',b,re.S|re.I):
            t=re.sub(r"<[^>]+>","",t); t=html.unescape(re.sub(r"\s+"," ",t)).strip()[:30]
            full=urllib.parse.urljoin(fu,html.unescape(h))
            if NL.search(h) or NL.search(t):
                if full not in seen and not full.startswith('mailto'): seen.add(full); out.append(f"{t}>{full}")
        for a in re.findall(r'<form[^>]*action="([^"]+)"',b,re.I):
            full=urllib.parse.urljoin(fu,html.unescape(a))
            if NL.search(full) and full not in seen: seen.add(full); out.append("FORM>"+full)
    return (e['id'],out[:3]) if out else None
with ThreadPoolExecutor(16) as ex:
    for r in ex.map(one,E):
        if r: print(r[0],"|"," ## ".join(x[:140] for x in r[1]))
